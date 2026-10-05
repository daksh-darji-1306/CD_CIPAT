from app.compiler.lexer import tokenize
from app.compiler.errors import CompileError
import pytest

p1_src = """int main() {
    int x = 2 + 3 * 4;
    int y = x * 1;
    print(y);
    return 0;
}"""

def test_lexer_p1():
    tokens = tokenize(p1_src)
    assert len(tokens) == 31
    assert tokens[-1].type == "EOF"
    expected_first_14 = [
        ("KEYWORD", "int", 1, 1),
        ("IDENTIFIER", "main", 1, 5),
        ("DELIMITER", "(", 1, 9),
        ("DELIMITER", ")", 1, 10),
        ("DELIMITER", "{", 1, 12),
        ("KEYWORD", "int", 2, 5),
        ("IDENTIFIER", "x", 2, 9),
        ("OPERATOR", "=", 2, 11),
        ("NUMBER", "2", 2, 13),
        ("OPERATOR", "+", 2, 15),
        ("NUMBER", "3", 2, 17),
        ("OPERATOR", "*", 2, 19),
        ("NUMBER", "4", 2, 21),
        ("DELIMITER", ";", 2, 22),
    ]
    for i, (t_type, lex, line, col) in enumerate(expected_first_14):
        assert tokens[i].type == t_type
        assert tokens[i].lexeme == lex
        assert tokens[i].line == line
        assert tokens[i].col == col

def test_lexer_operators():
    tokens = tokenize(">= == != && ||")
    lexemes = [t.lexeme for t in tokens if t.type != "EOF"]
    assert lexemes == [">=", "==", "!=", "&&", "||"]

def test_lexer_comments():
    src = """// comment\nint x = /* block */ 5;"""
    tokens = tokenize(src)
    lexemes = [t.lexeme for t in tokens if t.type != "EOF"]
    assert lexemes == ["int", "x", "=", "5", ";"]

def test_lexer_errors():
    with pytest.raises(CompileError) as exc:
        tokenize("int main() {\n    int x = 5 @ 3;\n    return 0;\n}")
    assert exc.value.formatted == "Lexical error at line 2, column 15: unexpected character '@'"
    
    with pytest.raises(CompileError) as exc:
        tokenize("2147483648")
    assert exc.value.formatted == "Lexical error at line 1, column 1: integer literal out of range"
