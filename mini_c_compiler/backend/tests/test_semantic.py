from app.compiler.lexer import tokenize
from app.compiler.parser import parse
from app.compiler.semantic import analyze
from app.compiler.errors import CompileError
import pytest

def test_semantic_e3():
    src = """int main() {
    int x = 1;
    print(y);
    return 0;
}"""
    tokens = tokenize(src)
    ast = parse(tokens)
    with pytest.raises(CompileError) as exc:
        analyze(ast)
    assert exc.value.formatted == "Semantic error at line 3, column 11: variable 'y' is not declared"

def test_semantic_e4():
    src = """int main() {
    int x = 1;
    int x = 2;
    return 0;
}"""
    tokens = tokenize(src)
    ast = parse(tokens)
    with pytest.raises(CompileError) as exc:
        analyze(ast)
    assert exc.value.formatted == "Semantic error at line 3, column 9: variable 'x' is already declared in this scope"

def test_semantic_ex8():
    src = """int main() {
    int x = 1;
    {
        int x = 2;
        print(x);
    }
    print(x);
    return 0;
}"""
    tokens = tokenize(src)
    ast = parse(tokens)
    symtab = analyze(ast)
    
    # Check that x is declared twice, with unique names x and x_1
    assert len(symtab) == 2
    assert symtab[0]["name"] == "x"
    assert symtab[0]["unique_name"] == "x"
    assert symtab[0]["scope"] == 1
    
    assert symtab[1]["name"] == "x"
    assert symtab[1]["unique_name"] == "x_1"
    assert symtab[1]["scope"] == 2

def test_semantic_p1_scopes():
    src = """int main() {
    int x = 2 + 3 * 4;
    int y = x * 1;
    print(y);
    return 0;
}"""
    tokens = tokenize(src)
    ast = parse(tokens)
    symtab = analyze(ast)
    
    assert len(symtab) == 2
    assert symtab[0]["name"] == "x"
    assert symtab[0]["scope"] == 1
    assert symtab[0]["unique_name"] == "x"
    assert symtab[1]["name"] == "y"
    assert symtab[1]["scope"] == 1
    assert symtab[1]["unique_name"] == "y"
