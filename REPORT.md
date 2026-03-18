# Laboratory Work 3

## Lexer & Scanner

**Course:** Formal Languages & Finite Automata  
**Author:** Bianca-Andreea Tataroi  
**Inspired by:** Cretu Dumitru, Vasile Drumea, Irina Cojuhari

---

## Theory

Lexical analysis is one of the first stages of language processing. Its role is to read a raw stream of characters and group them into meaningful units called lexemes. After a lexeme is recognized, the lexer assigns it a token type such as identifier, keyword, integer, float, operator, or separator.

The lexer does not execute the program and it does not verify full syntax rules. Instead, it prepares a cleaner and more structured representation of the input for the next phase, usually the parser. Because of this, lexical analysis is an essential part of compilers, interpreters, and many text-processing systems.

In this laboratory work, the implemented scanner processes a small expression-oriented language. The language is more complex than a simple calculator because it supports variables, floating-point values, comparison operators, and trigonometric keywords such as `sin` and `cos`.

---

## Objectives

- understand the role of lexical analysis in language processing
- implement a working lexer for a small custom language
- distinguish between lexemes and token categories
- support integers, floats, keywords, identifiers, operators, and separators
- demonstrate the output of the lexer on a non-trivial example

---

## Chosen Language

The implemented lexer recognizes a small language with the following elements:

- keywords: `let`, `print`, `sin`, `cos`
- identifiers: names such as `radius`, `angle`, `result`
- numeric literals: integers like `3` and floats like `10.5`
- arithmetic operators: `+`, `-`, `*`, `/`, `**`
- comparison operators: `>`, `>=`, `<`, `<=`, `==`, `!=`
- assignment operator: `=`
- separators: `(`, `)`, `,`, `;`
- comments: lines that begin with `#`

This choice keeps the project easy to understand while still being rich enough to show how a real lexer works.

---

## Program Structure

The project is organized into three main source files:

- `src/token_types.py`
- `src/lexer.py`
- `src/main.py`

The `token_types.py` file defines all token categories using an enumeration.

The `lexer.py` file contains the `Token` data class, the `Lexer` class, and the `LexerError` exception. This file implements the scanning logic and produces the sequence of tokens.

The `main.py` file contains a sample input program and runs the lexer on it, printing all discovered tokens together with their positions.

---

## Token Categories

The lexer can generate the following important token classes:

- keyword tokens
- identifier tokens
- integer tokens
- float tokens
- operator tokens
- separator tokens
- end-of-file token

Each token contains:

- the token type
- the original lexeme
- the line number
- the column number

The line and column metadata are useful for debugging and for reporting lexical or syntactic errors later.

---

## Implementation Description

The lexer scans the input from left to right one character at a time. At every step it decides what kind of token begins at the current position.

If the current character is whitespace, it is skipped. If it is a newline, the lexer moves to the next line and resets the column counter.

If the current character is a letter or underscore, the lexer reads an identifier-like sequence. After the full sequence is collected, it checks whether the lexeme is a reserved keyword such as `let`, `print`, `sin`, or `cos`. If yes, a keyword token is produced; otherwise, the result is an identifier token.

If the current character is a digit, the lexer reads a number. It first consumes all consecutive digits. Then it checks whether a decimal point is followed by at least one digit. If that pattern exists, the token becomes a float. Otherwise, the token remains an integer.

If the current character begins an operator or separator, the lexer tries to recognize either a single-character token or a compound token such as `>=`, `<=`, `==`, `!=`, or `**`.

If an unknown character appears, the lexer raises a `LexerError` and reports the exact line and column where the problem occurred.

---

## Core Algorithm

The main lexical analysis algorithm can be summarized in the following steps:

1. Start at the first character of the source code.
2. Skip spaces, tabs, carriage returns, and comments.
3. If a letter or underscore is found, scan an identifier or keyword.
4. If a digit is found, scan an integer or floating-point literal.
5. If an operator or separator is found, scan the longest valid token.
6. If an invalid character is found, stop and raise a lexical error.
7. When the entire input is consumed, append an `EOF` token.

This follows the usual maximal-match idea used in scanners: when multiple options are possible, the lexer tries to form the longest valid token.

---

## Example Input

The demonstration program used in `main.py` is:

```txt
# Sample program for the lexer
let radius = 10.5;
let angle = 0.0;
let result = cos(angle) + sin(radius / 2) * 3 ** 2;
print(result >= 1.5);
print(result != 0);
```

This example is intentionally richer than a basic calculator because it uses variables, floating-point values, trigonometric functions, arithmetic operators, and comparison operators.

---

## Example of Tokenization

For the line:

```txt
let result = cos(angle) + sin(radius / 2) * 3 ** 2;
```

the lexer identifies a sequence similar to:

- `LET`
- `IDENTIFIER(result)`
- `ASSIGN`
- `COS`
- `LPAREN`
- `IDENTIFIER(angle)`
- `RPAREN`
- `PLUS`
- `SIN`
- `LPAREN`
- `IDENTIFIER(radius)`
- `SLASH`
- `INTEGER(2)`
- `RPAREN`
- `STAR`
- `INTEGER(3)`
- `POWER`
- `INTEGER(2)`
- `SEMICOLON`

This demonstrates that the lexer converts a character stream into a structured token stream which can later be parsed into expressions or statements.

---

## Error Handling

The implementation reports lexical errors in two main situations:

- an unexpected unknown character is encountered
- a decimal point appears without digits after it when scanning a float

Instead of failing silently, the lexer raises a dedicated exception and includes the exact position of the invalid input.

---

## Conclusions

This laboratory work demonstrates how a lexer transforms raw source code into a stream of tokens. The implementation successfully recognizes keywords, identifiers, integers, floating-point literals, operators, separators, and comments. It also tracks token positions and reports lexical errors clearly.

The project shows that lexical analysis is a practical and necessary preprocessing step before syntax analysis. Even for a small custom language, the lexer already imposes structure on the input and makes later processing significantly easier.

---

## References

1. Course materials for Formal Languages & Finite Automata
2. Lecture notes and laboratory indications on lexical analysis
