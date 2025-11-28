from lexer import Lexer
from parser import Parser
from vm import VM

def run_code(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    vm = VM()
    vm.execute(ast)

if __name__ == "__main__":
    code = """
    def fact(n):
        if n == 0:
            return 1
        else:
            return n * fact(n - 1)

    result = fact(5)
    """
    run_code(code)