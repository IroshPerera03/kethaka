import lexer


class Node:
    pass

class Number(Node):
    def __init__(self, value):
        self.value = int(value)

class Variable(Node):
    def __init__(self, name):
        self.name = name

class StringLiteral(Node):
    def __init__(self, value):
        self.value = value.strip('"')  # Remove quotes

class BinaryOperation(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class PrintStatement(Node):
    def __init__(self, expression):
        self.expression = expression  # Ensure this is a valid expression

class FunctionCall(Node):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class IfStatement(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class ForLoop(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Function(Node):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class ReturnStatement(Node):
    def __init__(self, expression):
        self.expression = expression


def parse(tokens, code):
    def peek():
        return tokens[0] if tokens else (None, None, None)
    
    def consume():
        return tokens.pop(0) if tokens else (None, None, None)
    
    def expect(token_type):
        token = consume()
        if token[0] != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token[0]} at line {token[2]}")
        return token
    
    def parse_expression():
        return parse_comparison()
    
    def parse_comparison():
        expr = parse_term()
        
        while peek()[0] == 'COMPARE':
            op = consume()[1]
            right = parse_term()
            expr = BinaryOperation(expr, op, right)
            
        return expr
    
    def parse_term():
        expr = parse_factor()
        
        while peek()[0] == 'OP' and peek()[1] in ['+', '-']:
            op = consume()[1]
            right = parse_factor()
            expr = BinaryOperation(expr, op, right)
            
        return expr
    
    def parse_factor():
        expr = parse_primary()
        
        while peek()[0] == 'OP' and peek()[1] in ['*', '/']:
            op = consume()[1]
            right = parse_primary()
            expr = BinaryOperation(expr, op, right)
            
        return expr
    
    def parse_primary():
        token_type, value, line = peek()
        
        if token_type == 'NUMBER':
            consume()
            return Number(value)
        elif token_type == 'STRING':
            consume()
            return StringLiteral(value)
        elif token_type == 'IDENTIFIER':
            consume()
            if peek()[0] == 'LPAREN':  # Function call
                consume()  # consume LPAREN
                args = []
                if peek()[0] != 'RPAREN':
                    args.append(parse_expression())
                    while peek()[0] == 'COMMA':
                        consume()
                        args.append(parse_expression())
                expect('RPAREN')
                return FunctionCall(value, args)
            return Variable(value)
        elif token_type == 'LPAREN':
            consume()
            expr = parse_expression()
            expect('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token_type} at line {line}")
            
    def parse_statement():
        token_type, value, line = peek()
        
        if token_type == 'VAR':
            consume()
            var_name = expect('IDENTIFIER')[1]
            expect('ASSIGN')
            value = parse_expression()
            expect('SEMI')
            return (var_name, value)
            
        elif token_type == 'PRINT':
            consume()
            expect('LPAREN')
            expr = parse_expression()
            expect('RPAREN')
            expect('SEMI')
            return PrintStatement(expr)
            
        elif token_type == 'IF':
            consume()
            expect('LPAREN')
            condition = parse_expression()
            expect('RPAREN')
            expect('LBRACE')
            body = parse_statements()
            expect('RBRACE')
            
            # Check for else
            if peek()[0] == 'ELSE':
                consume()
                expect('LBRACE')
                else_body = parse_statements()
                expect('RBRACE')
                return IfStatement(condition, body, else_body)
            
            return IfStatement(condition, body)
            
        elif token_type == 'FOR':
            consume()
            expect('LPAREN')
            condition = parse_expression()
            expect('RPAREN')
            expect('LBRACE')
            body = parse_statements()
            expect('RBRACE')
            return ForLoop(condition, body)
            
        elif token_type == 'FUNCTION':
            consume()
            name = expect('IDENTIFIER')[1]
            expect('LPAREN')
            parameters = []
            if peek()[0] != 'RPAREN':
                parameters.append(expect('IDENTIFIER')[1])
                while peek()[0] == 'COMMA':
                    consume()
                    parameters.append(expect('IDENTIFIER')[1])
            expect('RPAREN')
            expect('LBRACE')
            body = parse_statements()
            expect('RBRACE')
            return Function(name, parameters, body)
            
        elif token_type == 'RETURN':
            consume()
            expr = parse_expression()
            expect('SEMI')
            return ReturnStatement(expr)
            
        else:
            raise SyntaxError(f"Unexpected token {token_type} at line {line}")
            
    def parse_statements():
        statements = []
        while tokens and peek()[0] not in ['RBRACE', None]:
            statements.append(parse_statement())
        return statements
        
    return parse_statements()


# Assuming you have some logic here to parse tokens
# Ensure that 'code' is defined before calling lexer
# For example, if you need to pass the code from the main function:
# code = "..."  # Define or retrieve the code here

# Example of how to call lexer correctly
# tokens = lexer(code)  # Ensure 'code' is defined

# Your existing parsing logic...