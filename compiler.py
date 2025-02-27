import ast as py_ast
from parser import parse
from lexer import lexer
import marshal
import types
from typing import List, Any

class CodeGenerator(py_ast.NodeVisitor):
    def __init__(self):
        self.code_lines: List[str] = []
        
    def visit_Module(self, node: py_ast.Module) -> None:
        for stmt in node.body:
            self.visit(stmt)
            
    def visit_Assign(self, node: py_ast.Assign) -> None:
        target = node.targets[0].id
        value = self.visit(node.value)
        self.code_lines.append(f"{target} = {value}")
        
    def visit_Call(self, node: py_ast.Call) -> str:
        func = node.func.id
        args = [self.visit(arg) for arg in node.args]
        return f"{func}({', '.join(args)})"
        
    def visit_If(self, node: py_ast.If) -> None:
        test = self.visit(node.test)
        self.code_lines.append(f"if {test}:")
        for stmt in node.body:
            self.visit(stmt)
        if node.orelse:
            self.code_lines.append("else:")
            for stmt in node.orelse:
                self.visit(stmt)
                
    def visit_Compare(self, node: py_ast.Compare) -> str:
        left = self.visit(node.left)
        op = self.visit(node.ops[0])
        right = self.visit(node.comparators[0])
        return f"{left} {op} {right}"
        
    def visit_Name(self, node: py_ast.Name) -> str:
        return node.id
        
    def visit_Constant(self, node: py_ast.Constant) -> str:
        if isinstance(node.value, str):
            return f"'{node.value}'"
        return str(node.value)
        
    def visit_Return(self, node: py_ast.Return) -> None:
        value = self.visit(node.value)
        self.code_lines.append(f"return {value}")
        
    def visit_FunctionDef(self, node: py_ast.FunctionDef) -> None:
        args = [arg.arg for arg in node.args.args]
        self.code_lines.append(f"def {node.name}({', '.join(args)}):")
        for stmt in node.body:
            self.visit(stmt)

def ast_to_python_ast(node):
    if isinstance(node, dict):
        if node['type'] == 'var_declaration':
            return py_ast.Assign(
                targets=[py_ast.Name(id=node['name'], ctx=py_ast.Store())],
                value=py_ast.Constant(value=node['value'])
            )
        elif node['type'] == 'function_definition':
            return py_ast.FunctionDef(
                name=node['name'],
                args=py_ast.arguments(
                    posonlyargs=[],
                    args=[py_ast.arg(arg=arg) for arg in node['params']],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]
                ),
                body=[ast_to_python_ast(stmt) for stmt in node['body']],
                decorator_list=[]
            )
        elif node['type'] == 'print_statement':
            return py_ast.Expr(
                value=py_ast.Call(
                    func=py_ast.Name(id='print', ctx=py_ast.Load()),
                    args=[py_ast.Name(id=node['value'], ctx=py_ast.Load()) if isinstance(node['value'], str) else py_ast.Constant(value=node['value'])],
                    keywords=[]
                )
            )
        elif node['type'] == 'function_call':
            return py_ast.Expr(
                value=py_ast.Call(
                    func=py_ast.Name(id=node['name'], ctx=py_ast.Load()),
                    args=[py_ast.Name(id=arg, ctx=py_ast.Load()) for arg in node['args']],
                    keywords=[]
                )
            )
        elif node['type'] == 'if_statement':
            return py_ast.If(
                test=ast_to_python_ast(node['condition']),
                body=[ast_to_python_ast(stmt) for stmt in node['body']],
                orelse=[ast_to_python_ast(stmt) for stmt in (node['else_body'] or [])]
            )
        elif node['type'] == 'binary_operation':
            if node['operator'] in ['<', '>', '<=', '>=', '==', '!=']:
                return py_ast.Compare(
                    left=ast_to_python_ast(node['left']),
                    ops=[py_ast.Gt() if node['operator'] == '>' else
                         py_ast.Lt() if node['operator'] == '<' else
                         py_ast.GtE() if node['operator'] == '>=' else
                         py_ast.LtE() if node['operator'] == '<=' else
                         py_ast.Eq() if node['operator'] == '==' else
                         py_ast.NotEq()],
                    comparators=[ast_to_python_ast(node['right'])]
                )
            else:
                return py_ast.BinOp(
                    left=ast_to_python_ast(node['left']),
                    op=py_ast.Add() if node['operator'] == '+' else
                       py_ast.Sub() if node['operator'] == '-' else
                       py_ast.Mult() if node['operator'] == '*' else
                       py_ast.Div(),
                    right=ast_to_python_ast(node['right'])
                )
        elif node['type'] == 'number':
            return py_ast.Constant(value=node['value'])
        elif node['type'] == 'string_literal':
            return py_ast.Constant(value=node['value'])
        elif node['type'] == 'variable':
            return py_ast.Name(id=node['name'], ctx=py_ast.Load())
        elif node['type'] == 'return_statement':
            return py_ast.Return(value=ast_to_python_ast(node['value']))
        else:
            raise ValueError(f"Unknown node type: {node['type']}")
    else:
        raise ValueError(f"Unknown node type: {type(node)}")

def compile_to_bytecode(source_file: str, output_file: str) -> None:
    try:
        # Read source code
        with open(source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
            
        # Generate tokens
        tokens = lexer(source_code)
        print(f"Tokens generated from {source_file}:", tokens)
        
        # Parse tokens into AST
        kethaka_ast = parse(tokens, source_code)
        print("AST:", kethaka_ast)
        
        # Convert Kethaka AST to Python AST
        python_ast_nodes = [ast_to_python_ast(node) for node in kethaka_ast]
        module = py_ast.Module(body=python_ast_nodes, type_ignores=[])
        
        # Add line numbers and parent references
        module = py_ast.fix_missing_locations(module)
        
        # Compile to bytecode
        code = compile(module, source_file, 'exec')
        
        # Save bytecode
        with open(output_file, 'wb') as f:
            marshal.dump(code, f)
            
    except Exception as e:
        print(f"Error compiling {source_file}: {str(e)}")
        raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source_file.snl>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    output_file = source_file.replace('.snl', '.kbc')
    compile_to_bytecode(source_file, output_file)
