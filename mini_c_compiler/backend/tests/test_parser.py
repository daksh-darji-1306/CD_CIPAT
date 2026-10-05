from app.compiler.lexer import tokenize
from app.compiler.parser import parse
from app.compiler.errors import CompileError
from app.compiler.ast_nodes import BinaryOp, If
import pytest

p1_src = """int main() {
    int x = 2 + 3 * 4;
    int y = x * 1;
    print(y);
    return 0;
}"""

def test_parser_p1():
    tokens = tokenize(p1_src)
    ast = parse(tokens)
    
    assert ast.__class__.__name__ == "Program"
    assert ast.function.name == "main"
    assert len(ast.function.body.statements) == 4
    
    stmt1 = ast.function.body.statements[0]
    assert stmt1.__class__.__name__ == "VarDecl"
    assert stmt1.name == "x"
    assert stmt1.init.__class__.__name__ == "BinaryOp"
    assert stmt1.init.op == "+"
    assert stmt1.init.left.value == 2
    assert stmt1.init.right.op == "*"
    assert stmt1.init.right.left.value == 3
    assert stmt1.init.right.right.value == 4

def test_parser_associativity():
    tokens = tokenize("int main() { print(1 - 2 - 3); return 0; }")
    ast = parse(tokens)
    expr = ast.function.body.statements[0].expr
    assert isinstance(expr, BinaryOp)
    assert expr.op == "-"
    assert isinstance(expr.left, BinaryOp)
    assert expr.left.op == "-"
    assert expr.left.left.value == 1
    assert expr.left.right.value == 2
    assert expr.right.value == 3

def test_parser_precedence():
    tokens = tokenize("int main() { print(1 + 2 * 3); return 0; }")
    ast = parse(tokens)
    expr = ast.function.body.statements[0].expr
    assert isinstance(expr, BinaryOp)
    assert expr.op == "+"
    assert expr.left.value == 1
    assert isinstance(expr.right, BinaryOp)
    assert expr.right.op == "*"

def test_parser_dangling_else():
    tokens = tokenize("int main() { if (1) if (2) print(3); else print(4); return 0; }")
    ast = parse(tokens)
    stmt = ast.function.body.statements[0]
    assert isinstance(stmt, If)
    assert stmt.cond.value == 1
    assert stmt.else_ is None
    
    inner_if = stmt.then
    assert isinstance(inner_if, If)
    assert inner_if.cond.value == 2
    assert inner_if.else_ is not None

def test_parser_error_e2():
    src = """int main() {
    int x = 5
    print(x);
    return 0;
}"""
    tokens = tokenize(src)
    with pytest.raises(CompileError) as exc:
        parse(tokens)
    assert exc.value.formatted == "Syntax error at line 3, column 5: expected ';' but found 'print'"
