from lexer import TokenType

class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class Assign(ASTNode):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

class If(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class FunctionDef(ASTNode):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        return self.parse_statements()

    def parse_statements(self):
        statements = []
        while self.position < len(self.tokens) and self.tokens[self.position].type != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.tokens[self.position]

        if token.type == TokenType.KEYWORD and token.value == 'if':
            return self.parse_if()

        if token.type == TokenType.KEYWORD and token.value == 'while':
            return self.parse_while()

        if token.type == TokenType.KEYWORD and token.value == 'def':
            return self.parse_function_def()

        if token.type == TokenType.IDENTIFIER and self.position + 1 < len(self.tokens) and self.tokens[self.position + 1].type == TokenType.OPERATOR and self.tokens[self.position + 1].value == '=':
            return self.parse_assign()

        return self.parse_expression()

    def parse_if(self):
        self.position += 1  # Consomme 'if'
        condition = self.parse_expression()
        then_branch = self.parse_block()
        else_branch = None
        if self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.KEYWORD and self.tokens[self.position].value == 'else':
            self.position += 1  # Consomme 'else'
            else_branch = self.parse_block()
        return If(condition, then_branch, else_branch)

    def parse_while(self):
        self.position += 1  # Consomme 'while'
        condition = self.parse_expression()
        body = self.parse_block()
        return While(condition, body)

    def parse_function_def(self):
        self.position += 1  # Consomme 'def'
        name = self.tokens[self.position].value
        self.position += 1  # Consomme le nom de la fonction
        self.position += 1  # Consomme '(' 
        args = []
        while self.tokens[self.position].type != TokenType.PUNCTUATION or self.tokens[self.position].value != ')':
            args.append(self.tokens[self.position].value)
            self.position += 1
            if self.tokens[self.position].type == TokenType.PUNCTUATION and self.tokens[self.position].value == ',':
                self.position += 1
        self.position += 1  # Consomme ')'
        body = self.parse_block()
        return FunctionDef(name, args, body)

    def parse_assign(self):
        var = self.tokens[self.position].value
        self.position += 2  # Consomme le nom de la variable et '='
        expr = self.parse_expression()
        return Assign(var, expr)

    def parse_block(self):
        self.position += 1  # Consomme ':'
        block = []
        while self.position < len(self.tokens) and self.tokens[self.position].type != TokenType.EOF and self.tokens[self.position].value != ':':
            block.append(self.parse_statement())
        return block

    def parse_expression(self):
        left = self.parse_term()
        while self.position < len(self.tokens) and self.tokens[self.position].type == TokenType.OPERATOR:
            op = self.tokens[self.position].value
            self.position += 1
            right = self.parse_term()
            left = BinOp(left, op, right)
        return left

    def parse_term(self):
        token = self.tokens[self.position]
        if token.type == TokenType.INTEGER:
            self.position += 1
            return Number(token.value)
        if token.type == TokenType.STRING:
            self.position += 1
            return String(token.value)
        if token.type == TokenType.IDENTIFIER:
            if self.position + 1 < len(self.tokens) and self.tokens[self.position + 1].type == TokenType.PUNCTUATION and self.tokens[self.position + 1].value == '(':
                return self.parse_function_call()
            self.position += 1
            return Variable(token.value)
        raise SyntaxError(f"Expression inattendue : {token.value}")

    def parse_function_call(self):
        name = self.tokens[self.position].value
        self.position += 2  # Consomme le nom de la fonction et '(' 
        args = []
        while self.tokens[self.position].type != TokenType.PUNCTUATION or self.tokens[self.position].value != ')':
            args.append(self.parse_expression())
            if self.tokens[self.position].type == TokenType.PUNCTUATION and self.tokens[self.position].value == ',':
                self.position += 1
        self.position += 1  # Consomme ')'
        return FunctionCall(name, args)