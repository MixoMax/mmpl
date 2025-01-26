import re
from enum import Enum
from typing import List, Optional, Union

class TokenType(Enum):
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"
    OPERATOR = "OPERATOR"
    BRACKET = "BRACKET"
    KEYWORD = "KEYWORD"
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"
    ELLIPSIS = "ELLIPSIS"
    ARROW = "ARROW"
    NULLISH = "NULLISH"
    ERROR_HANDLE = "ERROR_HANDLE"

class Token:
    def __init__(self, type: TokenType, value: str, line: int, col: int):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.col})"

class Tokenizer:
    KEYWORDS = {"def", "if", "else", "while", "for", "in", "return", "and", "or", "not", "True", "False", "None"}
    OPERATORS = {"+", "-", "*", "/", "=", "<", ">", "!", "%", "&", "|", "^", "~", "==", "!=", "<=", ">="}
    BRACKETS = {"(", ")", "[", "]", "{", "}", ",", "."}

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []

    def add_token(self, type: TokenType, value: str):
        self.tokens.append(Token(type, value, self.line, self.col - len(value)))

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            char = self.source[self.pos]

            # Skip comments
            if char == "#":
                while self.pos < len(self.source) and self.source[self.pos] != "\n":
                    self.pos += 1
                continue

            # Handle whitespace
            if char.isspace():
                if char == "\n":
                    self.add_token(TokenType.NEWLINE, "\n")
                    self.line += 1
                    self.col = 1
                else:
                    self.add_token(TokenType.WHITESPACE, char)
                    self.col += 1
                self.pos += 1
                continue

            # Handle strings
            if char in ['"', "'"]:
                value, length = self._tokenize_string()
                self.add_token(TokenType.STRING, value)
                self.pos += length
                self.col += length
                continue

            # Handle numbers
            if char.isdigit() or (char == "-" and self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit()):
                value, length = self._tokenize_number()
                self.add_token(TokenType.NUMBER, value)
                self.pos += length
                self.col += length
                continue

            # Handle identifiers and keywords
            if char.isalpha() or char == "_":
                value, length = self._tokenize_identifier()
                type = TokenType.KEYWORD if value in self.KEYWORDS else TokenType.IDENTIFIER
                self.add_token(type, value)
                self.pos += length
                self.col += length
                continue

            # Handle ellipsis
            if char == "." and self._peek(1) == "." and self._peek(2) == ".":
                self.add_token(TokenType.ELLIPSIS, "...")
                self.pos += 3
                self.col += 3
                continue

            # Handle arrow operator
            if char == "-" and self._peek(1) == ">":
                self.add_token(TokenType.ARROW, "->")
                self.pos += 2
                self.col += 2
                continue

            # Handle null coalescing
            if char == "?" and self._peek(1) == "?":
                self.add_token(TokenType.NULLISH, "??")
                self.pos += 2
                self.col += 2
                continue

            # Handle error handling operator
            if char == "?":
                self.add_token(TokenType.ERROR_HANDLE, "?")
                self.pos += 1
                self.col += 1
                continue

            # Handle operators
            op = self._tokenize_operator()
            if op:
                self.add_token(TokenType.OPERATOR, op)
                self.pos += len(op)
                self.col += len(op)
                continue

            # Handle brackets and other single characters
            if char in self.BRACKETS:
                self.add_token(TokenType.BRACKET, char)
                self.pos += 1
                self.col += 1
                continue

            # Skip unrecognized characters
            self.pos += 1
            self.col += 1

        self.add_token(TokenType.EOF, "")
        return self.tokens

    def _peek(self, offset: int = 1) -> Optional[str]:
        if self.pos + offset < len(self.source):
            return self.source[self.pos + offset]
        return None

    def _tokenize_string(self) -> tuple[str, int]:
        quote = self.source[self.pos]
        value = quote
        pos = self.pos + 1
        while pos < len(self.source):
            char = self.source[pos]
            value += char
            if char == quote and self.source[pos - 1] != "\\":
                break
            pos += 1
        return value, len(value)

    def _tokenize_number(self) -> tuple[str, int]:
        value = ""
        pos = self.pos
        if self.source[pos] == "-":
            value += "-"
            pos += 1
        while pos < len(self.source) and (self.source[pos].isdigit() or self.source[pos] == "."):
            value += self.source[pos]
            pos += 1
        return value, len(value)

    def _tokenize_identifier(self) -> tuple[str, int]:
        value = ""
        pos = self.pos
        while pos < len(self.source) and (self.source[pos].isalnum() or self.source[pos] == "_"):
            value += self.source[pos]
            pos += 1
        return value, len(value)

    def _tokenize_operator(self) -> Optional[str]:
        for op_len in [2, 1]:  # Check multi-char operators first
            if self.pos + op_len <= len(self.source):
                op = self.source[self.pos:self.pos + op_len]
                if op in self.OPERATORS:
                    return op
        return None

class Transpiler:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.indentation = 0
        self.output = []

    def transpile(self) -> str:
        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]

            # Handle end of file
            if token.type == TokenType.EOF:
                break

            # Skip standalone whitespace tokens
            if token.type == TokenType.WHITESPACE:
                self.pos += 1
                continue

            # Handle range shorthand (x...y^z)
            if token.type == TokenType.ELLIPSIS:
                self._handle_range()
                continue

            # Handle arrow operator (->)
            if token.type == TokenType.ARROW:
                self._handle_arrow()
                continue

            # Handle error handling (?)
            if token.type == TokenType.ERROR_HANDLE:
                self._handle_error()
                continue

            # Handle null coalescing (??)
            if token.type == TokenType.NULLISH:
                self._handle_nullish()
                continue

            # Handle opening curly brace
            if token.type == TokenType.BRACKET and token.value == "{":
                self._add_output(":")
                self.indentation += 1
                self.pos += 1
                continue

            # Handle closing curly brace
            if token.type == TokenType.BRACKET and token.value == "}":
                self.indentation -= 1
                self.pos += 1
                continue

            # Handle newlines
            if token.type == TokenType.NEWLINE:
                self._add_output("\n" + "    " * self.indentation)
                self.pos += 1
                continue

            # Default: keep token as is
            self._add_output(token.value)
            self.pos += 1

        return "".join(self.output)

    def _add_output(self, text: str):
        self.output.append(text)

    def _handle_range(self):
        # Handle x...y^z -> range(x, y, z)
        start = self.tokens[self.pos - 1].value if self.pos > 0 else "0"
        self.pos += 1  # Skip ...
        end = self.tokens[self.pos].value
        self.pos += 1
        
        step = None
        if self.pos < len(self.tokens) and self.tokens[self.pos].value == "^":
            self.pos += 1
            step = self.tokens[self.pos].value
            self.pos += 1

        range_str = f"range({start}, {end}"
        if step:
            range_str += f", {step}"
        range_str += ")"
        self._add_output(range_str)

    def _handle_arrow(self):
        # Handle -> operator for function chaining
        self.pos += 1  # Skip ->
        func = self.tokens[self.pos].value
        self._add_output(f" {func}(")
        
        # Check if this is a lambda
        if self.tokens[self.pos].type == TokenType.BRACKET and self.tokens[self.pos].value == "(":
            self._add_output("lambda ")
            self.pos += 1  # Skip (
            while self.pos < len(self.tokens) and self.tokens[self.pos].value != ")":
                self._add_output(self.tokens[self.pos].value)
                self.pos += 1
            self.pos += 1  # Skip )
            
            # Skip =>
            while self.pos < len(self.tokens) and self.tokens[self.pos].value != "{":
                self.pos += 1
            self.pos += 1  # Skip {
            
            self._add_output(": ")
            while self.pos < len(self.tokens) and self.tokens[self.pos].value != "}":
                self._add_output(self.tokens[self.pos].value)
                self.pos += 1
            self.pos += 1  # Skip }
            
        self._add_output(")")

    def _handle_error(self):
        # Handle ? operator for error handling
        self.pos += 1
        self._add_output(", None")

    def _handle_nullish(self):
        # Handle ?? operator for null coalescing
        self.pos += 1  # Skip ??
        default_value = self.tokens[self.pos].value
        self._add_output(f" if _ is not None else {default_value}")
        self.pos += 1

def transpile_file(input_path: str, output_path: str):
    with open(input_path, 'r') as f:
        source = f.read()

    tokenizer = Tokenizer(source)
    tokens = tokenizer.tokenize()
    transpiler = Transpiler(tokens)
    python_code = transpiler.transpile()

    with open(output_path, 'w') as f:
        # Add automatic error handling wrapper
        wrapper = """
import math
from functools import partial

def handle_errors(func, default=None):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result if result is not None else default
        except Exception:
            return default
    return wrapper

class ArrowWrapper:
    def __init__(self, value):
        self.value = value

    def __gt__(self, func):
        if callable(func):
            if isinstance(self.value, (list, tuple, set)):
                return ArrowWrapper(map(func, self.value))
            return ArrowWrapper(func(self.value))
        return ArrowWrapper(self.value)

    def __iter__(self):
        return iter(self.value)

"""
        f.write(wrapper)
        f.write(python_code)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python msc_to_py.py <input.msc> <output.py>")
        sys.exit(1)
    
    transpile_file(sys.argv[1], sys.argv[2])
