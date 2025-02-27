import lexer


def parse(tokens, source_code):
    ast = []
    
    while tokens:
        # Skip newlines
        while tokens and tokens[0][0] == 'NEWLINE':
            tokens.pop(0)
            
        if not tokens:
            break
            
        # Parse statement
        if tokens[0][0] in ['VAR', 'FUNCTION', 'IF', 'PRINT', 'RETURN', 'IDENTIFIER']:
            statement = parse_statement(tokens, source_code)
            ast.append(statement)
        else:
            token = tokens[0]
            raise SyntaxError(f"Unexpected token {token[0]} at line {token[2]}")
            
    return ast

def parse_statement(tokens, source_code):
    token = tokens[0]
    
    if token[0] == 'VAR':
        return parse_var_declaration(tokens, source_code)
    elif token[0] == 'FUNCTION':
        return parse_function_definition(tokens, source_code)
    elif token[0] == 'IF':
        return parse_if_statement(tokens, source_code)
    elif token[0] == 'PRINT':
        return parse_print_statement(tokens, source_code)
    elif token[0] == 'RETURN':
        return parse_return_statement(tokens, source_code)
    elif token[0] == 'IDENTIFIER':
        # Check if it's a function call
        if len(tokens) > 1 and tokens[1][0] == 'LPAREN':
            return parse_function_call(tokens, source_code)
        else:
            raise SyntaxError(f"Unexpected identifier at line {token[2]}")
    else:
        raise SyntaxError(f"Unexpected token {token[0]} at line {token[2]}")

def parse_function_call(tokens, source_code):
    function_name = tokens.pop(0)[1]  # Get function name
    tokens.pop(0)  # Remove LPAREN
    
    args = []
    while tokens and tokens[0][0] != 'RPAREN':
        if tokens[0][0] == 'IDENTIFIER':
            args.append(tokens.pop(0)[1])
        elif tokens[0][0] == 'COMMA':
            tokens.pop(0)
        else:
            break
            
    if not tokens or tokens[0][0] != 'RPAREN':
        raise SyntaxError("Expected closing parenthesis")
        
    tokens.pop(0)  # Remove RPAREN
    
    # Remove semicolon if present
    if tokens and tokens[0][0] == 'SEMI':
        tokens.pop(0)
        
    return {
        'type': 'function_call',
        'name': function_name,
        'args': args
    }

def parse_var_declaration(tokens, source_code):
    tokens.pop(0)  # Remove VAR
    
    # Get variable name
    if not tokens or tokens[0][0] != 'IDENTIFIER':
        raise SyntaxError("Expected variable name")
    var_name = tokens.pop(0)[1]
    
    # Parse assignment
    if not tokens or tokens[0][0] != 'ASSIGN':
        raise SyntaxError("Expected assignment operator")
    tokens.pop(0)  # Remove ASSIGN
    
    # Parse value
    if not tokens:
        raise SyntaxError("Expected value")
    
    if tokens[0][0] == 'STRING':
        value = tokens.pop(0)[1].strip('"\'')  # Remove quotes
    elif tokens[0][0] == 'NUMBER':
        value = int(tokens.pop(0)[1])
    else:
        raise SyntaxError(f"Expected string or number, got {tokens[0][0]}")
    
    # Parse semicolon
    if not tokens or tokens[0][0] != 'SEMI':
        raise SyntaxError("Expected semicolon")
    tokens.pop(0)  # Remove SEMI
    
    return {
        'type': 'var_declaration',
        'name': var_name,
        'value': value
    }

def parse_function_definition(tokens, source_code):
    tokens.pop(0)  # Remove FUNCTION
    
    # Get function name
    if not tokens or tokens[0][0] != 'IDENTIFIER':
        raise SyntaxError("Expected function name")
    function_name = tokens.pop(0)[1]
    
    # Parse parameters
    if not tokens or tokens[0][0] != 'LPAREN':
        raise SyntaxError("Expected opening parenthesis")
    tokens.pop(0)  # Remove LPAREN
    
    parameters = []
    while tokens and tokens[0][0] != 'RPAREN':
        if tokens[0][0] == 'IDENTIFIER':
            parameters.append(tokens.pop(0)[1])
        elif tokens[0][0] == 'COMMA':
            tokens.pop(0)
        else:
            break
            
    if not tokens or tokens[0][0] != 'RPAREN':
        raise SyntaxError("Expected closing parenthesis")
    tokens.pop(0)  # Remove RPAREN
    
    # Parse function body
    if not tokens or tokens[0][0] != 'LBRACE':
        raise SyntaxError("Expected opening brace")
    tokens.pop(0)  # Remove LBRACE
    
    body = []
    while tokens and tokens[0][0] != 'RBRACE':
        statement = parse_statement(tokens, source_code)
        body.append(statement)
        
    if not tokens or tokens[0][0] != 'RBRACE':
        raise SyntaxError("Expected closing brace")
    tokens.pop(0)  # Remove RBRACE
    
    return {
        'type': 'function_definition',
        'name': function_name,
        'params': parameters,
        'body': body
    }

def parse_if_statement(tokens, source_code):
    tokens.pop(0)  # Remove IF
    
    # Parse condition
    if not tokens or tokens[0][0] != 'LPAREN':
        raise SyntaxError("Expected opening parenthesis")
    tokens.pop(0)  # Remove LPAREN
    
    condition = parse_expression(tokens, source_code)
    
    if not tokens or tokens[0][0] != 'RPAREN':
        raise SyntaxError("Expected closing parenthesis")
    tokens.pop(0)  # Remove RPAREN
    
    # Parse if body
    if not tokens or tokens[0][0] != 'LBRACE':
        raise SyntaxError("Expected opening brace")
    tokens.pop(0)  # Remove LBRACE
    
    body = []
    while tokens and tokens[0][0] != 'RBRACE':
        statement = parse_statement(tokens, source_code)
        body.append(statement)
        
    if not tokens or tokens[0][0] != 'RBRACE':
        raise SyntaxError("Expected closing brace")
    tokens.pop(0)  # Remove RBRACE
    
    # Parse else block if present
    else_body = None
    if tokens and tokens[0][0] == 'ELSE':
        tokens.pop(0)  # Remove ELSE
        
        if not tokens or tokens[0][0] != 'LBRACE':
            raise SyntaxError("Expected opening brace")
        tokens.pop(0)  # Remove LBRACE
        
        else_body = []
        while tokens and tokens[0][0] != 'RBRACE':
            statement = parse_statement(tokens, source_code)
            else_body.append(statement)
            
        if not tokens or tokens[0][0] != 'RBRACE':
            raise SyntaxError("Expected closing brace")
        tokens.pop(0)  # Remove RBRACE
    
    return {
        'type': 'if_statement',
        'condition': condition,
        'body': body,
        'else_body': else_body
    }

def parse_print_statement(tokens, source_code):
    tokens.pop(0)  # Remove PRINT
    
    # Parse opening parenthesis
    if not tokens or tokens[0][0] != 'LPAREN':
        raise SyntaxError("Expected opening parenthesis")
    tokens.pop(0)  # Remove LPAREN
    
    # Parse value to print
    if not tokens:
        raise SyntaxError("Expected value to print")
        
    if tokens[0][0] == 'IDENTIFIER':
        value = tokens.pop(0)[1]
    elif tokens[0][0] == 'STRING':
        value = tokens.pop(0)[1].strip('"\'')  # Remove quotes
    elif tokens[0][0] == 'NUMBER':
        value = int(tokens.pop(0)[1])
    else:
        raise SyntaxError(f"Expected identifier, string or number, got {tokens[0][0]}")
    
    # Parse closing parenthesis
    if not tokens or tokens[0][0] != 'RPAREN':
        raise SyntaxError("Expected closing parenthesis")
    tokens.pop(0)  # Remove RPAREN
    
    # Parse semicolon
    if not tokens or tokens[0][0] != 'SEMI':
        raise SyntaxError("Expected semicolon")
    tokens.pop(0)  # Remove SEMI
    
    return {
        'type': 'print_statement',
        'value': value
    }

def parse_return_statement(tokens, source_code):
    tokens.pop(0)  # Remove RETURN
    
    expression = parse_expression(tokens, source_code)
    
    # Parse semicolon
    if not tokens or tokens[0][0] != 'SEMI':
        raise SyntaxError("Expected semicolon")
    tokens.pop(0)  # Remove SEMI
    
    return {
        'type': 'return_statement',
        'value': expression
    }

def parse_expression(tokens, source_code):
    return parse_comparison(tokens, source_code)

def parse_comparison(tokens, source_code):
    expr = parse_term(tokens, source_code)
    
    while tokens and tokens[0][0] == 'COMPARE':
        op = tokens.pop(0)[1]
        right = parse_term(tokens, source_code)
        expr = {
            'type': 'binary_operation',
            'left': expr,
            'operator': op,
            'right': right
        }
            
    return expr

def parse_term(tokens, source_code):
    expr = parse_factor(tokens, source_code)
    
    while tokens and tokens[0][0] == 'OP' and tokens[0][1] in ['+', '-']:
        op = tokens.pop(0)[1]
        right = parse_factor(tokens, source_code)
        expr = {
            'type': 'binary_operation',
            'left': expr,
            'operator': op,
            'right': right
        }
            
    return expr

def parse_factor(tokens, source_code):
    expr = parse_primary(tokens, source_code)
    
    while tokens and tokens[0][0] == 'OP' and tokens[0][1] in ['*', '/']:
        op = tokens.pop(0)[1]
        right = parse_primary(tokens, source_code)
        expr = {
            'type': 'binary_operation',
            'left': expr,
            'operator': op,
            'right': right
        }
            
    return expr

def parse_primary(tokens, source_code):
    token_type, value, line = tokens[0]
        
    if token_type == 'NUMBER':
        tokens.pop(0)
        return {
            'type': 'number',
            'value': int(value)
        }
    elif token_type == 'STRING':
        tokens.pop(0)
        return {
            'type': 'string_literal',
            'value': value.strip('"')  # Remove quotes
        }
    elif token_type == 'IDENTIFIER':
        tokens.pop(0)
        if tokens and tokens[0][0] == 'LPAREN':  # Function call
            return parse_function_call(tokens, source_code)
        return {
            'type': 'variable',
            'name': value
        }
    elif token_type == 'LPAREN':
        tokens.pop(0)
        expr = parse_expression(tokens, source_code)
        expect(tokens, 'RPAREN')
        return expr
    else:
        raise SyntaxError(f"Unexpected token {token_type} at line {line}")

def parse_statements(tokens, source_code):
    statements = []
    while tokens and tokens[0][0] not in ['RBRACE', None]:
        statements.append(parse_statement(tokens, source_code))
    return statements

def expect(tokens, token_type):
    token = tokens.pop(0)
    if token[0] != token_type:
        raise SyntaxError(f"Expected {token_type}, got {token[0]} at line {token[2]}")
    return token


