from app.compiler.arith import wrap32, c_div, c_mod, eval_binop, eval_unop

def test_wrap32():
    assert wrap32(2**31) == -2**31
    assert wrap32(2**31 - 1) == 2**31 - 1
    assert wrap32(-2**31 - 1) == 2**31 - 1

def test_c_div():
    assert c_div(7, 2) == 3
    assert c_div(-7, 2) == -3
    assert c_div(7, -2) == -3
    assert c_div(-7, -2) == 3

def test_c_mod():
    assert c_mod(7, 2) == 1
    assert c_mod(-7, 2) == -1
    assert c_mod(7, -2) == 1

def test_eval_binop():
    assert eval_binop('<', 2, 3) == 1
    assert eval_binop('&&', 2, 0) == 0
    assert eval_binop('||', 0, 5) == 1

def test_eval_unop():
    assert eval_unop('!', 0) == 1
    assert eval_unop('-', 5) == -5
