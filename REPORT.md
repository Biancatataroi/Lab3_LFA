# Laboratory Work 3

## Lexer & Scanner

**Course:** Formal Languages & Finite Automata  
**Author:** Bianca Tataroi  
**Inspired by:** Cretu Dumitru, Vasile Drumea, Irina Cojuhari

---

## Introduction

This laboratory work is dedicated to lexical analysis, one of the earliest and most important stages in the processing of formal languages. In programming language implementation, the source code initially appears as a raw sequence of characters. Before any syntactic structure can be recognized and before any meaning can be assigned to instructions, the text must first be divided into smaller meaningful units. This task belongs to the lexer, also called scanner or tokenizer. The purpose of the lexer is to read the input character by character, identify meaningful fragments, and transform them into a stream of classified tokens that can later be used by a parser or interpreter.

The present project implements a lexer for a small expression-oriented language. The chosen language is intentionally more expressive than a basic calculator because it includes identifiers, reserved words, integer and floating-point numbers, arithmetic operators, comparison operators, separators, and trigonometric function names such as `sin` and `cos`. In this way, the project satisfies the laboratory requirement of going beyond the simplest possible tokenization task and demonstrates how lexical analysis behaves in a more realistic setting.

---

## Theoretical Background

Lexical analysis is deeply connected to the theory of formal languages. A programming language can be viewed as a formal language whose valid words are programs or program fragments. However, such a language is usually not analyzed directly at the level of individual characters. Instead, the first step is to recognize lexical categories such as identifiers, constants, keywords, and operators. These categories simplify the structure of the input and prepare it for the next stage of analysis.

An essential distinction in lexical analysis is the difference between a lexeme and a token. A lexeme is the exact sequence of characters extracted from the source text, such as `radius`, `10.5`, `!=`, or `sin`. A token, on the other hand, is the abstract category associated with that lexeme, such as `IDENTIFIER`, `FLOAT`, `BANG_EQUAL`, or `SIN`. The lexeme preserves the concrete value found in the input, while the token expresses its grammatical role. This distinction is important because later compiler phases usually reason about categories first, even though the original text is still useful for diagnostics and semantic processing.

The lexer is strongly related to regular languages and finite automata. Many lexical classes can be described using regular expressions and recognized by deterministic finite automata. For example, identifiers often follow a regular pattern consisting of a letter or underscore followed by letters, digits, or underscores. Integer literals and many operator sequences are also regular in nature. This means that a scanner can be understood theoretically as a recognizer for a family of regular languages, each corresponding to one token class. Even when a lexer is implemented manually, without explicitly constructing automata tables, its internal logic still reflects the same automata-based principles of state progression and pattern recognition.

If the input alphabet is denoted by `Σ`, then the source program is a word `w ∈ Σ*`. The purpose of lexical analysis is to transform this word into a sequence of tokens `T = (t1, t2, ..., tn)`, where each token `ti` belongs to a finite token set `Tok`. In a simplified form, the scanner can be seen as a function `L : Σ* -> Tok*`, meaning that it maps a character string to a token string whenever the input belongs to the lexical specification of the language. If the input contains a fragment that does not belong to any valid token language, then the function is undefined for that position and a lexical error is reported.

From the perspective of regular languages, each token class corresponds to a language `Li ⊆ Σ*`. The full lexical specification can therefore be expressed as a family of regular languages `L1, L2, ..., Lk`, where each one recognizes a different category such as identifiers, integers, floats, or operators. The scanner repeatedly chooses a prefix `x` of the remaining input such that `x ∈ Li` for some `i`, emits the corresponding token, and continues with the suffix that remains unread. In this sense, lexical analysis is essentially a decomposition of the input word into substrings that belong to known regular languages.

Another theoretical principle relevant to lexical analysis is the longest match rule, often called maximal munch. When more than one tokenization is possible starting from the same position, the lexer should usually choose the longest valid token. This is why an input such as `>=` should be recognized as a single comparison operator rather than as `>` followed by `=`, and `**` should be recognized as a single power operator rather than two separate multiplication symbols. This principle helps reduce ambiguity and produces a cleaner and more consistent token stream for the syntactic stage.

The lexer does not verify whether the entire program is syntactically correct. That responsibility belongs to the parser. Nevertheless, lexical analysis already performs an important form of validation because it must decide whether the input can be decomposed into valid lexical units. If a character sequence does not belong to any token class, then the source fails even before syntax is considered. For this reason, the scanner is both a recognizer and a preprocessor for the language.

---

## Objectives

The main objective of this laboratory work is to understand how lexical analysis functions in practice and how theoretical concepts from formal languages are applied in software. More precisely, the project aims to implement a working lexer for a custom language, to distinguish clearly between lexemes and tokens, to recognize several meaningful token classes, and to demonstrate the output of the scanner on a non-trivial example. Another important objective is to show that the implementation can correctly handle both integers and floating-point literals, as well as reserved words for trigonometric operations, in accordance with the requirements of the assignment.

---

## Chosen Language And Motivation

The language selected for this project is a small expression-based language with simple declaration and output instructions. It supports the reserved words `let` and `print`, as well as the trigonometric names `sin` and `cos`. It recognizes user-defined identifiers such as variable names, integer and floating-point numeric constants, arithmetic operators including `+`, `-`, `*`, `/`, and `**`, comparison operators such as `>`, `>=`, `<`, `<=`, `==`, and `!=`, as well as separators including parentheses, commas, and semicolons. The language also supports line comments that begin with the `#` character.

This choice was made deliberately. A lexer designed only for a minimal calculator would not highlight enough aspects of lexical analysis. By extending the language with identifiers, floating-point values, comparison operators, and trigonometric keywords, the project becomes more illustrative while remaining easy to understand. The result is a compact but meaningful example of how source code can be transformed into a structured token stream.

The lexical vocabulary of the chosen language can be described more formally. If `Letter = {a, ..., z, A, ..., Z}` and `Digit = {0, 1, ..., 9}`, then identifiers follow the pattern `(Letter ∪ {_})(Letter ∪ Digit ∪ {_})*`. Integer literals follow the pattern `Digit+`, while floating-point literals follow the pattern `Digit+ . Digit+`. Reserved words form a finite set of fixed strings, namely `{let, print, sin, cos}`. Operators and separators also belong to finite sets of fixed lexical forms. This formalization helps show that the lexical layer of the language is regular and therefore suitable for automata-based recognition.

---

## Technologies And Implementation Choices

The implementation was written in Python 3. This language was chosen because it is concise, expressive, and very suitable for educational projects that focus on algorithms and symbolic processing. Python allows the lexical analysis logic to remain readable, which is especially helpful in a laboratory work where the code should be easy to explain during evaluation or presentation.

Only standard Python features were used. The `Enum` class was employed to define token categories in a clean and readable form, while the `dataclass` decorator was used to represent tokens with minimal boilerplate code. No external libraries were needed, since the focus of the assignment is the lexical analysis algorithm itself rather than framework integration or dependency management.

The project is organized in a simple and clear way. The file `src/token_types.py` defines the enumeration of token types. The file `src/lexer.py` contains the `Token` data class, the `Lexer` class responsible for scanning, and the `LexerError` exception used for invalid input. The file `src/main.py` contains the demonstration program that feeds sample source code into the lexer and prints the resulting token stream.

If the scanner state is viewed abstractly as a tuple `(i, line, column)`, then `i` represents the current index in the source string, while `line` and `column` describe the current source position. Every successful recognition step transforms one state into another by consuming a non-empty prefix of the unread input. In this sense, the implementation is deterministic because, once the current character and the recognition rule are known, the next action is fully determined.

---

## Implementation Description

The scanner processes the source code from left to right while maintaining an index in the input text together with line and column counters. These counters allow the lexer to attach positional metadata to every token, which is useful both for debugging and for future compiler phases. At each step, the lexer inspects the current character and decides which recognition rule should be applied.

Whitespace characters such as spaces, tabs, and carriage returns are ignored because they do not contribute directly to the token stream in this language. Newline characters are handled separately so that the lexer can increment the current line number and reset the column counter. This ensures that each token begins with an accurate source position.

When the current character is a letter or underscore, the lexer begins scanning a word-like sequence. It continues reading characters for as long as they remain letters, digits, or underscores. Once the full lexeme has been collected, the scanner compares it against the reserved word table. If the lexeme matches one of the language keywords such as `let`, `print`, `sin`, or `cos`, a keyword token is produced. Otherwise, the lexeme is classified as an identifier.

When the current character is a digit, the lexer begins scanning a numeric literal. It first consumes the integer part by reading consecutive digits. After that, it checks whether the number continues with a decimal point followed by at least one additional digit. If so, the token is classified as a floating-point literal. If not, the lexeme remains an integer token. This distinction is especially important for the present assignment, since one of the required extensions beyond a trivial calculator is the support for both integers and floats.

When the current character belongs to the operator or separator vocabulary, the lexer determines whether it forms a single-character token or a compound token. For example, `+`, `-`, `(`, and `;` are recognized immediately as single-character symbols, while `>=`, `<=`, `==`, `!=`, and `**` are recognized through a longer lookahead-based match. This reflects the longest match principle discussed earlier in the theoretical section.

The implementation also handles comments that start with `#`. Once such a character is found, the lexer ignores all remaining characters on the current line. This behavior shows that a lexer is not limited to recognizing useful tokens; it is also responsible for filtering out irrelevant textual elements that should not influence later stages of the program.

If the scanner encounters an unknown character or a malformed floating-point literal, it raises a `LexerError`. The error message includes the exact line and column where the problem occurred. This behavior is important because a lexical analyzer must not only accept valid inputs but also reject invalid ones in a clear and informative manner.

---

## Recognition Logic From A Formal Perspective

From a formal point of view, the implemented scanner can be understood as a collection of recognizers for different regular patterns. The identifier recognizer accepts words that begin with a letter or underscore and continue with alphanumeric characters or underscores. The integer recognizer accepts one or more digits. The floating-point recognizer accepts a sequence of digits followed by a decimal point and another non-empty sequence of digits. The operator recognizers accept fixed strings such as `+`, `-`, `!=`, or `**`. Because all these patterns are regular, they can in principle be described by regular expressions or finite automata.

The implementation does not explicitly build automata tables, yet its behavior remains equivalent to automaton-based recognition. Each helper method of the lexer corresponds to a controlled transition through a lexical pattern. The method for identifiers continues consuming symbols while they belong to the identifier alphabet. The method for numbers continues consuming digits and optionally transitions into the floating-point form. The method for operators distinguishes between shorter and longer valid alternatives. In this way, the scanner is a practical embodiment of the regular-language concepts studied in Formal Languages & Finite Automata.

The identifier language can be written with the regular expression `(_|Letter)(_ | Letter | Digit)*` if spaces are ignored for readability, while the integer language can be written as `Digit+` and the floating-point language as `Digit+ "." Digit+`. Fixed tokens such as `let`, `sin`, `+`, `!=`, or `**` correspond to singleton regular languages containing exactly one word each. The total token language is therefore not one single arbitrary construction, but a finite union of regular languages. Since regular languages are closed under union, the lexical specification remains regular as a whole.

The same idea can be stated using a deterministic finite automaton. A DFA is usually defined as the 5-tuple `A = (Q, Σ, δ, q0, F)`, where `Q` is the set of states, `Σ` is the alphabet, `δ : Q × Σ -> Q` is the transition function, `q0` is the initial state, and `F ⊆ Q` is the set of accepting states. In the context of lexical analysis, different accepting states may correspond to different token categories. For instance, after reading a valid identifier, the automaton reaches an accepting state associated with the identifier class, after reading a valid integer it reaches a numeric accepting state, and after reading `>=` it reaches an accepting state associated with the `GREATER_EQUAL` token. In practice, the implemented Python methods simulate this transition logic directly, without needing to explicitly store the automaton in tabular form.

Another way to view correctness is through decomposition. If the input is `w`, then successful lexical analysis means that there exists a factorization `w = x1 x2 ... xn` such that every factor `xi` belongs to one valid lexical language and each factor is mapped to a token `ti`. Symbolically, one may write `xi ∈ Li` and `token(xi) = ti` for some token class `Li`. The token stream is then `(t1, t2, ..., tn)`. If no such factorization exists because some prefix cannot be assigned to any legal lexical class, then the input is lexically invalid. This description makes clear that tokenization is not arbitrary splitting, but a constrained decomposition guided by formal recognition rules.

---

## Demonstration Input

To show how the lexer behaves on a realistic example, the file `src/main.py` uses the following source fragment:

```txt
# Sample program for the lexer
let radius = 10.5;
let angle = 0.0;
let result = cos(angle) + sin(radius / 2) * 3 ** 2;
print(result >= 1.5);
print(result != 0);
```

This sample was chosen because it contains a wide range of lexical situations in a very compact space. It includes comments, variable declarations, floating-point literals, function-like keywords, arithmetic expressions, comparison expressions, separators, and statement terminators. For that reason, it is suitable for demonstrating that the scanner handles more than a single narrow use case.

When the lexer processes this input, it produces a token stream in which each item contains a token type, the matched lexeme, and its exact source position. For example, the word `let` becomes a `LET` token, the sequence `10.5` becomes a `FLOAT` token, the text `cos` becomes a `COS` token, and the operator `>=` becomes a `GREATER_EQUAL` token. This output confirms that the lexer transforms an unstructured character sequence into a representation that is both more abstract and more useful for further analysis.

---

## Error Handling And Correctness

Correctness in lexical analysis does not mean only recognizing valid tokens. It also means rejecting invalid inputs precisely and consistently. In this implementation, correctness is supported by explicit recognition rules for each token class, by the use of positional tracking, and by immediate failure when the current input cannot be assigned to any valid lexical category.

Two particularly relevant error scenarios are handled directly. The first occurs when the scanner encounters an unexpected character that is not part of any valid token pattern. The second occurs when a decimal point appears in a numeric literal without being followed by digits, which would make the floating-point representation incomplete. In both situations, the lexer raises a clear exception rather than continuing with ambiguous behavior. This is important from both a practical and a theoretical perspective, since a recognizer must make a clear distinction between accepted and rejected inputs.

The longest match rule also contributes to correctness. Suppose that the current unread input begins with a prefix that could belong either to a shorter token or to a longer one. If the scanner were to choose the shorter form too early, the resulting factorization could be incorrect or at least inconvenient for the parser. By preferring the longest valid prefix, the lexer ensures that forms such as `>=`, `<=`, `==`, `!=`, and `**` are recognized in the intended way. Formally, if several prefixes `p1, p2, ..., pm` beginning at the same position satisfy `pi ∈ Li` for some lexical classes, the chosen prefix is one with maximal length, that is a prefix `pj` such that `|pj| >= |pi|` for all `i`.

---

## How To Run The Program

The implementation can be executed from the root of the project with the command:

```bash
python3 src/main.py
```

After execution, the program prints the original sample input followed by the generated tokens. For each token, the output includes the token category, the concrete lexeme, and the line and column where that lexeme begins. This makes the behavior of the lexer easy to inspect and verify.

---

## Conclusion

This laboratory work demonstrates both the theoretical and practical dimensions of lexical analysis. On the practical side, the project implements a working lexer in Python for a custom expression-oriented language that includes identifiers, integers, floating-point literals, reserved words, trigonometric operations, comparison operators, comments, and separators. On the theoretical side, the project illustrates how lexical categories can be viewed as regular languages and how the behavior of a scanner reflects finite-automaton-based recognition.

The final result shows that lexical analysis is not merely a preprocessing convenience, but a fundamental stage in language processing. By converting raw source text into a structured stream of tokens, the lexer creates the foundation for syntax analysis and all later phases of compilation or interpretation. Through this implementation, the concepts discussed in the course are applied in a concrete and understandable way, demonstrating the close relationship between formal language theory and practical software construction.

---

## References

Course materials for Formal Languages & Finite Automata, together with lecture and laboratory notes on lexical analysis, scanners, tokens, regular languages, and finite automata, were used as the main theoretical basis for this work.
