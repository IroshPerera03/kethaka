import sys
from lexer import lexer
from parser import parse
from compiler import compile_to_python

def main():
    if len(sys.argv) != 2:
        print("භාවිතය: python sinhala_compiler.py <file.snl>")
        return
    
    # Check if Python is available
    try:
        import subprocess
        subprocess.run(["python", "--version"], check=True)
    except FileNotFoundError:
        try:
            subprocess.run(["python3", "--version"], check=True)
        except FileNotFoundError:
            print("Error: Neither 'python' nor 'python3' command found.")
            print("Please ensure Python is installed and available in your PATH.")
            return
    
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        code = f.read()
    
    tokens = lexer(code)
    ast = parse(tokens, code)
    compiled_code = compile_to_python(ast)

    with open("output.py", "w", encoding="utf-8") as f:
        f.write(compiled_code)
    
    print("Compiled Successfully! Running output...")
    exec(compiled_code)  # Execute compiled Python code

if __name__ == "__main__":
    main()