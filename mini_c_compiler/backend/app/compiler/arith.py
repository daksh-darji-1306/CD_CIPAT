def wrap32(x):
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x & 0x80000000 else x

def c_div(a, b):            # truncate toward zero; caller guarantees b != 0
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q

def c_mod(a, b):
    return a - c_div(a, b) * b

def eval_binop(op, a, b):
    if op == '+':
        return wrap32(a + b)
    elif op == '-':
        return wrap32(a - b)
    elif op == '*':
        return wrap32(a * b)
    elif op == '/':
        if b == 0:
            raise ZeroDivisionError()
        return wrap32(c_div(a, b))
    elif op == '%':
        if b == 0:
            raise ZeroDivisionError()
        return wrap32(c_mod(a, b))
    elif op == '<':
        return 1 if a < b else 0
    elif op == '<=':
        return 1 if a <= b else 0
    elif op == '>':
        return 1 if a > b else 0
    elif op == '>=':
        return 1 if a >= b else 0
    elif op == '==':
        return 1 if a == b else 0
    elif op == '!=':
        return 1 if a != b else 0
    elif op == '&&':
        return 1 if (a != 0 and b != 0) else 0
    elif op == '||':
        return 1 if (a != 0 or b != 0) else 0
    else:
        raise ValueError(f"Unknown binary operator {op}")

def eval_unop(op, a):
    if op == '-':
        return wrap32(-a)
    elif op == '!':
        return 1 if a == 0 else 0
    else:
        raise ValueError(f"Unknown unary operator {op}")
