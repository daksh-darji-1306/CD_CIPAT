from app.compiler.lexer import tokenize
from app.compiler.parser import parse
from app.compiler.semantic import analyze
from app.compiler.codegen import generate_code
from app.compiler.optimizer import optimize
from app.compiler.tac import format_instr
from app.examples import PROGRAMS

def get_program(pid):
    for p in PROGRAMS:
        if p["id"] == pid:
            return p["source"]
    return ""

def get_opt_tac_and_stats(source):
    tokens = tokenize(source)
    ast = parse(tokens)
    analyze(ast)
    tac = generate_code(ast)
    opt_tac, log = optimize(tac)
    return [format_instr(i) for i in opt_tac], len(tac), len(opt_tac)

def test_optimizer_p1():
    expected = [
        "print 14",
        "return 0"
    ]
    opt_tac, bef, aft = get_opt_tac_and_stats(get_program("ex1"))
    assert opt_tac == expected
    assert bef == 7 and aft == 2

def test_optimizer_p2():
    expected = [
        "i = 0",
        "sum = 0",
        "L1:",
        "t1 = i < 3",
        "ifFalse t1 goto L2",
        "sum = sum + i",
        "i = i + 1",
        "goto L1",
        "L2:",
        "print sum",
        "return 0"
    ]
    opt_tac, bef, aft = get_opt_tac_and_stats(get_program("ex2"))
    assert opt_tac == expected
    assert bef == 13 and aft == 11

def test_optimizer_ex4():
    expected = [
        "print 20",
        "return 0"
    ]
    opt_tac, bef, aft = get_opt_tac_and_stats(get_program("ex4"))
    assert opt_tac == expected
    assert bef == 10 and aft == 2

def test_optimizer_ex10():
    expected = [
        "print 42",
        "return 0"
    ]
    opt_tac, bef, aft = get_opt_tac_and_stats(get_program("ex10"))
    assert opt_tac == expected
    assert bef == 6 and aft == 2
