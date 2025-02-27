import re

TOKEN_SPEC = [
    ('NUMBER', r'\d+'),          # Numbers
    ('STRING', r'["\'][^"\']*["\']'),  # String literals with both single and double quotes
    ('VAR', r'සඳහන්'),         # Variable declaration
    ('PRINT', r'මුද්‍රණය'),      # Print statement
    ('IF', r'නම්'),             # If condition
    ('ELSE', r'නැතහොත්'),      # Else condition
    ('FOR', r'දක්වා'),          # For loop
    ('FUNCTION', r'ක්‍රියාව'),    # Function declaration
    ('RETURN', r'ආපසු'),        # Return statement
    ('IDENTIFIER', r'[a-zA-Zа-яА-Я_\u0D80-\u0DFF][a-zA-Zа-яА-Я0-9_\u0D80-\u0DFF]*'),  # Support Sinhala identifiers
    ('OP', r'[+\-*/]'),         # Arithmetic operators
    ('COMPARE', r'[<>]=?|==|!='),  # Comparison operators
    ('ASSIGN', r'='),           # Assignment operator
    ('LPAREN', r'\('),          # Left parenthesis
    ('RPAREN', r'\)'),          # Right parenthesis
    ('LBRACE', r'\{'),          # Left brace
    ('RBRACE', r'\}'),          # Right brace
    ('COMMA', r','),            # Comma for function parameters
    ('SEMI', r';'),             # Semicolon
    ('SKIP', r'[ \t\r]+|#[^\n]*'),  # Skip whitespace and comments
    ('NEWLINE', r'\n'),         # Newline
]

def lexer(code):
    tokens = []
    line_num = 1
    pos = 0
    
    while pos < len(code):
        match = None
        for token_name, pattern in TOKEN_SPEC:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                value = match.group(0)
                if token_name not in ['SKIP', 'NEWLINE']:
                    tokens.append((token_name, value, line_num))
                if token_name == 'NEWLINE':
                    line_num += 1
                pos = match.end()
                break
        
        if not match:
            raise SyntaxError(f"Invalid character '{code[pos]}' at line {line_num}")
            
    return tokens

code = "සඳහන් x = 10; නම් (x > 5) { මුද්‍රණය('අංකය විශාලයි!'); } # This is a comment"
tokens = lexer(code)
print(tokens)