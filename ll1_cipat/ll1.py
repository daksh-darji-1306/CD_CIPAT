"""
LL(1) Parser: CIPAT Activity 1, Compiler Design (3170701)
Computes FIRST, FOLLOW, builds the predictive parsing table,
detects non-LL(1) conflicts, and runs a stack-based table-driven parser.
"""
import re
import sys

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

EPS, START = 'ε', 'E'
grammar = {
    'E':  [['T', "E'"]],
    "E'": [['+', 'T', "E'"], [EPS]],
    'T':  [['F', "T'"]],
    "T'": [['*', 'F', "T'"], [EPS]],
    'F':  [['(', 'E', ')'], ['id']],
}
NT = set(grammar)
TERMINALS = ['id', '+', '*', '(', ')', '$']


def first_seq(seq, FIRST):
    """FIRST of a sequence of grammar symbols."""
    res = set()
    for s in seq:
        f = FIRST[s] if s in NT else {s}
        res |= f - {EPS}
        if EPS not in f:
            return res
    res.add(EPS)
    return res


def compute_first():
    FIRST = {n: set() for n in NT}
    changed = True
    while changed:
        changed = False
        for A, prods in grammar.items():
            for p in prods:
                f = first_seq(p, FIRST)
                if not f <= FIRST[A]:
                    FIRST[A] |= f
                    changed = True
    return FIRST


def compute_follow(FIRST):
    FOLLOW = {n: set() for n in NT}
    FOLLOW[START].add('$')
    changed = True
    while changed:
        changed = False
        for A, prods in grammar.items():
            for p in prods:
                for i, B in enumerate(p):
                    if B not in NT:
                        continue
                    f = first_seq(p[i + 1:], FIRST)
                    add = f - {EPS}
                    if EPS in f:
                        add |= FOLLOW[A]
                    if not add <= FOLLOW[B]:
                        FOLLOW[B] |= add
                        changed = True
    return FOLLOW


def build_table(FIRST, FOLLOW):
    table = {}

    def put(A, a, p):
        if (A, a) in table:
            raise ValueError(f"Grammar is NOT LL(1): conflict at M[{A},{a}]")
        table[(A, a)] = p

    for A, prods in grammar.items():
        for p in prods:
            f = first_seq(p, FIRST)
            for a in f - {EPS}:
                put(A, a, p)
            if EPS in f:
                for b in FOLLOW[A]:
                    put(A, b, p)
    return table


def tokenize(s):
    return re.findall(r'id|[+*()]', s.replace(' ', ''))


def parse(text, table):
    tokens = tokenize(text) + ['$']
    stack, i, step = ['$', START], 0, 1
    print(f"{'#':<4}{'STACK':<24}{'INPUT':<22}ACTION")
    print('-' * 70)
    while True:
        top, a = stack[-1], tokens[i]
        row = f"{step:<4}{' '.join(reversed(stack)):<24}{' '.join(tokens[i:]):<22}"
        if top == '$' and a == '$':
            print(row + "ACCEPT")
            return True
        if top not in NT:
            if top == a:
                print(row + f"match {a}")
                stack.pop()
                i += 1
            else:
                print(row + f"ERROR: expected {top}, found {a}")
                return False
        else:
            p = table.get((top, a))
            if p is None:
                print(row + f"ERROR: M[{top},{a}] is empty")
                return False
            print(row + f"{top} → {' '.join(p)}")
            stack.pop()
            if p != [EPS]:
                stack.extend(reversed(p))
        step += 1


def print_tables(FIRST, FOLLOW, table):
    print("FIRST sets")
    for n in ['E', "E'", 'T', "T'", 'F']:
        print(f"  FIRST({n}) = {{ {', '.join(sorted(FIRST[n]))} }}")
    print("\nFOLLOW sets")
    for n in ['E', "E'", 'T', "T'", 'F']:
        print(f"  FOLLOW({n}) = {{ {', '.join(sorted(FOLLOW[n]))} }}")
    print("\nParsing table M[A, a]")
    print(f"{'':<5}" + ''.join(f"{t:<14}" for t in TERMINALS))
    for n in ['E', "E'", 'T', "T'", 'F']:
        cells = []
        for t in TERMINALS:
            p = table.get((n, t))
            cells.append(f"{n}→{''.join(p)}" if p else '')
        print(f"{n:<5}" + ''.join(f"{c:<14}" for c in cells))


if __name__ == '__main__':
    FIRST = compute_first()
    FOLLOW = compute_follow(FIRST)
    table = build_table(FIRST, FOLLOW)
    if len(sys.argv) > 1 and sys.argv[1] == 'tables':
        print_tables(FIRST, FOLLOW, table)
    else:
        inputs = sys.argv[1:] or ["id+id*id", "id+*id"]
        for s in inputs:
            print(f"\nParsing: {s}")
            parse(s, table)
