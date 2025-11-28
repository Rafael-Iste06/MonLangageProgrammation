import re
from enum import Enum, auto

class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    PUNCTUATION = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, column={self.column})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.keywords = {'if', 'else', 'while', 'def', 'return', 'Tree', 'Stack', 'Queue'}
        self.operators = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
        self.punctuation = {'(', ')', '{', '}', '[', ']', ',', ';', ':'}

    def tokenize(self):
        while self.position < len(self.code):
            char = self.code[self.position]

            if char.isspace():
                if char == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.position += 1
                continue

            if char in self.punctuation:
                self.tokens.append(Token(TokenType.PUNCTUATION, char, self.line, self.column))
                self.position += 1
                self.column += 1
                continue

            if char in self.operators or (char + self.code[self.position + 1]) in self.operators:
                if (char + self.code[self.position + 1]) in self.operators:
                    op = char + self.code[self.position + 1]
                    self.tokens.append(Token(TokenType.OPERATOR, op, self.line, self.column))
                    self.position += 2
                    self.column += 2
                else:
                    self.tokens.append(Token(TokenType.OPERATOR, char, self.line, self.column))
                    self.position += 1
                    self.column += 1
                continue

            if char.isdigit():
                start = self.position
                while self.position < len(self.code) and self.code[self.position].isdigit():
                    self.position += 1
                    self.column += 1
                if self.position < len(self.code) and self.code[self.position] == '.':
                    self.position += 1
                    self.column += 1
                    while self.position < len(self.code) and self.code[self.position].isdigit():
                        self.position += 1
                        self.column += 1
                    value = self.code[start:self.position]
                    self.tokens.append(Token(TokenType.FLOAT, float(value), self.line, self.column - len(value)))
                else:
                    value = self.code[start:self.position]
                    self.tokens.append(Token(TokenType.INTEGER, int(value), self.line, self.column - len(value)))
                continue

            if char == '"':
                start = self.position + 1
                self.position += 1
                self.column += 1
                while self.position < len(self.code) and self.code[self.position] != '"':
                    if self.code[self.position] == '\n':
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += 1
                    self.position += 1
                value = self.code[start:self.position]
                self.tokens.append(Token(TokenType.STRING, value, self.line, self.column - len(value) - 1))
                self.position += 1
                self.column += 1
                continue

            if char.isalpha() or char == '_':
                start = self.position
                while self.position < len(self.code) and (self.code[self.position].isalnum() or self.code[self.position] == '_'):
                    self.position += 1
                    self.column += 1
                value = self.code[start:self.position]
                if value in self.keywords:
                    self.tokens.append(Token(TokenType.KEYWORD, value, self.line, self.column - len(value)))
                else:
                    self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, self.column - len(value)))
                continue

            raise SyntaxError(f"Caractère inattendu : {char} (ligne {self.line}, colonne {self.column})")

        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens