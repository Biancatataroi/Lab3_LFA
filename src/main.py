from lexer import Lexer, LexerError


SAMPLE_PROGRAM = """
# Sample program for the lexer
let radius = 10.5;
let angle = 0.0;
let result = cos(angle) + sin(radius / 2) * 3 ** 2;
print(result >= 1.5);
print(result != 0);
""".strip()


def print_tokens(source: str) -> None:
    lexer = Lexer(source)

    try:
        tokens = lexer.tokenize()
    except LexerError as error:
        print("Lexer error:", error)
        return

    print("Source program:\n")
    print(source)
    print("\nTokens:\n")

    for token in tokens:
        print(
            f"{token.token_type.name:<15} "
            f"lexeme={token.lexeme!r:<12} "
            f"line={token.line:<3} "
            f"column={token.column}"
        )


def main() -> None:
    print_tokens(SAMPLE_PROGRAM)


if __name__ == "__main__":
    main()
