from app.compiler.lexer import tokenize
from app.compiler.parser import parse
from app.compiler.semantic import analyze
from app.compiler.codegen import generate_code
from app.compiler.tac import format_instr
from app.examples import PROGRAMS

def get_program(pid):
    for p in PROGRAMS:
        if p["id"] == pid:
            return p["source"]
    return ""

def get_tac(source):
    tokens = tokenize(source)
    ast = parse(tokens)
    analyze(ast)
    tac = generate_code(ast)
    return [format_instr(i) for i in tac]

def test_codegen_p1():
    expected = [
        "t1 = 3 * 4",
        "t2 = 2 + t1",
        "x = t2",
        "t3 = x * 1",
        "y = t3",
        "print y",
        "return 0"
    ]
    assert get_tac(get_program("ex1")) == expected

def test_codegen_p2():
    expected = [
        "i = 0",
        "sum = 0",
        "L1:",
        "t1 = i < 3",
        "ifFalse t1 goto L2",
        "t2 = sum + i",
        "sum = t2",
        "t3 = i + 1",
        "i = t3",
        "goto L1",
        "L2:",
        "print sum",
        "return 0"
    ]
    assert get_tac(get_program("ex2")) == expected

def test_codegen_ex4():
    expected = [
        "a = 10",
        "b = 20",
        "t1 = a > b",
        "ifFalse t1 goto L1",
        "print a",
        "goto L2",
        "L1:",
        "print b",
        "L2:",
        "return 0"
    ]
    assert get_tac(get_program("ex4")) == expected

def test_codegen_ex10():
    expected = [
        "debug = 0",
        "ifFalse debug goto L1",
        "print 999",
        "L1:",
        "print 42",
        "return 0"
    ]
    assert get_tac(get_program("ex10")) == expected
