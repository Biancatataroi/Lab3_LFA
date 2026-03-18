from dataclasses import dataclass

from token_types import TokenType


KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
    "sin": TokenType.SIN,
    "cos": TokenType.COS,
}


@dataclass(frozen=True)
class Token:
    token_type: TokenType
    lexeme: str
    line: int
    column: int


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.index = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens = []

        while not self._is_at_end():
            current = self._peek()

            if current in {" ", "\t", "\r"}:
                self._advance()
                continue

            if current == "\n":
                self._advance()
                self.line += 1
                self.column = 1
                continue

            if current == "#":
                self._skip_comment()
                continue

            if current.isalpha() or current == "_":
                tokens.append(self._identifier())
                continue

            if current.isdigit():
                tokens.append(self._number())
                continue

            tokens.append(self._operator_or_separator())

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    def _identifier(self) -> Token:
        start_index = self.index
        start_line = self.line
        start_column = self.column

        while not self._is_at_end() and (self._peek().isalnum() or self._peek() == "_"):
            self._advance()

        lexeme = self.source[start_index:self.index]
        token_type = KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
        return Token(token_type, lexeme, start_line, start_column)

    def _number(self) -> Token:
        start_index = self.index
        start_line = self.line
        start_column = self.column

        while not self._is_at_end() and self._peek().isdigit():
            self._advance()

        token_type = TokenType.INTEGER
        if not self._is_at_end() and self._peek() == ".":
            if self._peek_next().isdigit():
                token_type = TokenType.FLOAT
                self._advance()
                while not self._is_at_end() and self._peek().isdigit():
                    self._advance()
            else:
                raise LexerError(
                    f"Invalid float literal at line {start_line}, column {start_column}."
                )

        lexeme = self.source[start_index:self.index]
        return Token(token_type, lexeme, start_line, start_column)

    def _operator_or_separator(self) -> Token:
        start_line = self.line
        start_column = self.column
        current = self._advance()

        single_char_tokens = {
            "=": TokenType.ASSIGN,
            "+": TokenType.PLUS,
            "-": TokenType.MINUS,
            "*": TokenType.STAR,
            "/": TokenType.SLASH,
            "(": TokenType.LPAREN,
            ")": TokenType.RPAREN,
            ",": TokenType.COMMA,
            ";": TokenType.SEMICOLON,
            ">": TokenType.GREATER,
            "<": TokenType.LESS,
        }

        if current == "*" and self._match("*"):
            return Token(TokenType.POWER, "**", start_line, start_column)

        if current == "=" and self._match("="):
            return Token(TokenType.EQUAL_EQUAL, "==", start_line, start_column)

        if current == "!" and self._match("="):
            return Token(TokenType.BANG_EQUAL, "!=", start_line, start_column)

        if current == ">" and self._match("="):
            return Token(TokenType.GREATER_EQUAL, ">=", start_line, start_column)

        if current == "<" and self._match("="):
            return Token(TokenType.LESS_EQUAL, "<=", start_line, start_column)

        if current in single_char_tokens:
            return Token(single_char_tokens[current], current, start_line, start_column)

        raise LexerError(
            f"Unexpected character '{current}' at line {start_line}, column {start_column}."
        )

    def _skip_comment(self) -> None:
        while not self._is_at_end() and self._peek() != "\n":
            self._advance()

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self._peek() != expected:
            return False
        self._advance()
        return True

    def _peek(self) -> str:
        return self.source[self.index]

    def _peek_next(self) -> str:
        if self.index + 1 >= self.length:
            return "\0"
        return self.source[self.index + 1]

    def _advance(self) -> str:
        character = self.source[self.index]
        self.index += 1
        self.column += 1
        return character

    def _is_at_end(self) -> bool:
        return self.index >= self.length
