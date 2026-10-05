# Mini C Compiler: CIPAT Activity 2, Antigravity Implementation Plan

> Paste this whole file into Antigravity as the task. Execute the phases in order and do not skip the verification gates. Section 5 (GROUND TRUTH) is hand-verified. If your code disagrees with it, the code is wrong. Never edit Section 5 to match the code.

## 0. Context and goal

- College: C. K. Pithawala College of Engineering and Technology, Computer Engineering
- Course: Compiler Design (3170701), Final Year Sem 7. Assessment: CIPAT 2026-27, Activity 2
- Problem statement chosen: **#6 Mini C Compiler**, with phases: Tokens → Parser → AST → Intermediate Code → Optimization → Execute
- What the brief requires: source code, PPT, report, and a working **demonstration** of the implementation (C or any suitable language is allowed).
- Marks: 5 = Explanation of compiler phases; 5 = Code demonstration, report and viva.
- CO coverage the project must visibly show:

| Topic | CO | Where it appears in this project |
|---|---|---|
| Lexical analysis | CO1 | `lexer.py`, Tokens tab |
| Parser and grammar design | CO2 | `parser.py`, AST tab, grammar in the report |
| Semantic analysis | CO3 | `semantic.py`, Symbol Table tab |
| Intermediate code and optimization | CO3 | `codegen.py`, `optimizer.py`, TAC and Optimized TAC tabs |
| Runtime, target code and integration | CO4 | `vm.py` (execution), web app integration, optional pseudo-assembly |

- Architecture decision (fixed): **Python FastAPI backend** that contains the whole compiler, and a **React + Vite frontend** that visualizes every phase. The compiler is hand-written (no lex/yacc/ANTLR/PLY, no parser libraries), so it can be explained in the viva.
- Link to Activity 1: the parser is a recursive-descent predictive parser over an LL(1)-style grammar. Left recursion in expressions is removed by the `( op term )*` loop form, the same idea as the E / E' transformation from the LL(1) activity.

---

## 1. Deliverables and repository layout

All work lives in `./mini_c_compiler/`:

```
mini_c_compiler/
├── README.md
├── VIVA_NOTES.md
├── DEMO_SCRIPT.md
├── backend/
│   ├── requirements.txt            # fastapi, uvicorn[standard], pytest, httpx
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app, routes, CORS
│   │   ├── examples.py             # the example programs from Section 5.6
│   │   └── compiler/
│   │       ├── __init__.py
│   │       ├── arith.py            # wrap32, c_div, c_mod, eval_binop, eval_unop
│   │       ├── errors.py           # CompileError, RuntimeErr
│   │       ├── tokens.py           # Token, KEYWORDS
│   │       ├── lexer.py
│   │       ├── ast_nodes.py
│   │       ├── parser.py
│   │       ├── semantic.py
│   │       ├── tac.py              # Instr model, format_instr
│   │       ├── codegen.py
│   │       ├── optimizer.py
│   │       ├── vm.py
│   │       └── pipeline.py         # compile_source(...)
│   └── tests/
│       ├── test_arith.py
│       ├── test_lexer.py
│       ├── test_parser.py
│       ├── test_semantic.py
│       ├── test_codegen.py
│       ├── test_optimizer.py
│       ├── test_vm.py
│       ├── test_programs.py        # all examples and errors from Section 5
│       └── test_api.py
├── frontend/                        # Vite + React (JavaScript, not TypeScript)
│   ├── package.json
│   ├── vite.config.js               # proxy /api to http://localhost:8000
│   ├── index.html
│   └── src/ (see Section 7)
└── docs/
    ├── Mini_C_Compiler_Presentation.pptx
    ├── Mini_C_Compiler_Report.docx
    └── screenshots/
```

Tooling: Python 3.10+, Node 18+. Python deps: `fastapi`, `uvicorn[standard]`, `pytest`, `httpx`. Docs: `python-pptx`, `python-docx` (install in a separate step for Phase J only).

---

## 2. Phase checklist and timeline

- [ ] Phase A: `arith.py`, `errors.py`, `tokens.py`, `lexer.py`
- [ ] Phase B: `ast_nodes.py`, `parser.py`
- [ ] Phase C: `semantic.py`
- [ ] Phase D: `tac.py`, `codegen.py`
- [ ] Phase E: `optimizer.py`
- [ ] Phase F: `vm.py`
- [ ] Phase G: `pipeline.py`, `main.py`, `examples.py`
- [ ] **Gate 1**: backend tests all pass (Section 6, Phase H)
- [ ] Phase I: frontend, then **Gate 2** (manual checklist, Section 7)
- [ ] Phase J: docs (PPT, report, viva notes, demo script, README), then **Gate 3**

Suggested schedule (evaluation window is 05/10 to 09/10):

| Day | Goal |
|---|---|
| Thu 01/10 (today) | Phases A to E |
| Fri 02/10 | Phases F to H (Gate 1) |
| Sat 03/10 | Phase I (frontend, Gate 2) |
| Sun 04/10 | Phase J (docs, Gate 3), two full demo rehearsals |
| Mon 05/10 onward | Buffer and evaluation |

---

## 3. Mini C language specification

### 3.1 Supported features

- Program = exactly one function: `int main() { ... }` (no parameters).
- Type: `int` only (32-bit signed, wraps on overflow like two's complement).
- Statements: declaration (`int x;` or `int x = expr;`), assignment (`x = expr;`), `if` / `else`, `while`, `for`, `print(expr);`, `return expr;`, nested blocks `{ ... }`.
- Expressions: integer literals, variables, parentheses, unary `-` and `!`, binary `* / %`, `+ -`, `< <= > >=`, `== !=`, `&&`, `||`.
- Comments: `// line` and `/* block */`.
- Block scoping with shadowing: an inner block may redeclare a name from an outer block. Redeclaring in the **same** scope is an error.

### 3.2 Deliberate deviations and limits (document these in the report)

- `int x;` initializes `x` to 0.
- `&&` and `||` are **not short-circuit**. Both operands are always evaluated, and the result is 1 or 0.
- No functions other than `main`, no arrays, no pointers, no floats, no `break` / `continue`, no `++`, no `+=`, no `printf` (`print(expr)` is the built-in output statement).
- Division truncates toward zero and `%` takes the sign of the dividend, like C.
- Only the **first** error is reported (no error recovery).
- If `main` ends without `return`, an implicit `return 0` is added.
- The program name must be `main`; otherwise a semantic error.

### 3.3 Lexical rules

- Whitespace and comments are skipped.
- Keywords: `int if else while for print return`.
- Identifier: `[A-Za-z_][A-Za-z0-9_]*` (a keyword is a KEYWORD token, not an identifier).
- Number: one or more digits. A literal larger than 2147483647 is a lexical error: `integer literal out of range`.
- Operators: `+ - * / % = == != < <= > >= ! && ||`. Delimiters: `( ) { } ;`.
- A single `&` or `|` is a lexical error: `unexpected character '&'`.
- An unterminated `/*` is a lexical error: `unterminated comment`.
- Token categories (the `type` field): `KEYWORD`, `IDENTIFIER`, `NUMBER`, `OPERATOR`, `DELIMITER`, `EOF`. Line and column are 1-based. The EOF token carries the position just after the last character.

### 3.4 Grammar (EBNF, recursive-descent friendly)

```
program      → function EOF
function     → 'int' IDENT '(' ')' block
block        → '{' statement* '}'
statement    → declaration
             | assignment ';'
             | ifStmt | whileStmt | forStmt
             | printStmt | returnStmt | block
declaration  → 'int' IDENT ( '=' expr )? ';'
assignment   → IDENT '=' expr
ifStmt       → 'if' '(' expr ')' statement ( 'else' statement )?
whileStmt    → 'while' '(' expr ')' statement
forStmt      → 'for' '(' forInit expr? ';' assignment? ')' statement
forInit      → declaration | assignment ';' | ';'
printStmt    → 'print' '(' expr ')' ';'
returnStmt   → 'return' expr ';'
expr         → logicOr
logicOr      → logicAnd ( '||' logicAnd )*
logicAnd     → equality ( '&&' equality )*
equality     → relational ( ( '==' | '!=' ) relational )*
relational   → additive ( ( '<' | '<=' | '>' | '>=' ) additive )*
additive     → term ( ( '+' | '-' ) term )*
term         → unary ( ( '*' | '/' | '%' ) unary )*
unary        → ( '-' | '!' ) unary | primary
primary      → NUMBER | IDENT | '(' expr ')'
```

Notes: a `declaration` consumes its own `;`. Dangling `else` binds to the nearest `if`. A statement starting with an identifier must be an assignment (otherwise: `expected '=' but found ...`). All binary operators are left-associative.

---

## 4. Architecture and API contract

### 4.1 Core pipeline (`pipeline.compile_source(source: str, optimize: bool = True, run: bool = True) -> dict`)

Phases run in order and each phase's result is kept. If a phase raises an error, **all earlier results are still returned**, `success` is false, and `error` is filled in.

1. Lexer → tokens
2. Parser → AST
3. Semantic analyzer → symbol table, resolved unique names
4. Code generator → TAC (three-address code)
5. Optimizer → optimized TAC and log
6. VM → output, exit code (skipped when `run` is false or when `optimize` is true and the result is executed from the optimized TAC; **execute the optimized TAC when `optimize` is true, otherwise the unoptimized TAC**)

### 4.2 Errors

```python
class CompileError(Exception):   # phase in {"lexical","syntax","semantic"}
    phase, message, line, col
class RuntimeErr(Exception):     # phase = "runtime", line/col = None
```

`formatted` strings (exact formats):
- `Lexical error at line {line}, column {col}: {message}`
- `Syntax error at line {line}, column {col}: {message}`
- `Semantic error at line {line}, column {col}: {message}`
- `Runtime error: {message}`

### 4.3 API (FastAPI, prefix `/api`)

- `GET /api/health` → `{"status": "ok"}`
- `GET /api/examples` → `[{"id","name","source"}]` (from `examples.py`; do not send expected outputs)
- `POST /api/compile` with body `{"source": str, "optimize": bool = true, "run": bool = true}`. Source longer than 10000 characters returns HTTP 400 with `{"detail": "source too long"}`.

Response (always HTTP 200 for compile and runtime errors):

```json
{
  "success": true,
  "tokens": [{"type": "KEYWORD", "lexeme": "int", "line": 1, "col": 1}],
  "ast": {"type": "Program", "...": "..."},
  "symbol_table": [{"name": "x", "unique_name": "x", "type": "int", "scope": 1, "line": 2}],
  "tac": ["t1 = 3 * 4"],
  "optimized_tac": ["print 14", "return 0"],
  "optimization_log": [{"iteration": 1, "pass": "Constant Folding & Propagation", "tac": ["..."]}],
  "stats": {"tac_before": 7, "tac_after": 2},
  "output": ["14"],
  "exit_code": 0,
  "error": null,
  "phases": {"lexical": "ok", "syntax": "ok", "semantic": "ok", "codegen": "ok", "optimizer": "ok", "execution": "ok"}
}
```

- On error: `success=false`, `error = {"phase","message","line","col","formatted"}`. Phases before the failing one are `"ok"`, the failing one is `"error"`, and later ones are `"skipped"`. Fields for phases that did not run are empty (`[]` or `null`).
- On a **runtime** error the compile phases are `ok`, `execution` is `"error"`, `output` holds the lines printed before the error, and `exit_code` is null.
- When `optimize=false`: `optimized_tac` = `[]`, `optimization_log` = `[]`, `stats` = null and the `optimizer` phase is `"skipped"`.
- `stats.tac_before` and `tac_after` count **all lines including labels**.

### 4.4 AST JSON format

Each node is a dict with `type`, `line`, `col` plus these fields:

| type | fields |
|---|---|
| Program | `function` |
| Function | `name`, `body` (Block) |
| Block | `statements` (list) |
| VarDecl | `name`, `init` (expr or null) |
| Assign | `name`, `value` |
| If | `cond`, `then`, `else_` (node or null) |
| While | `cond`, `body` |
| For | `init` (VarDecl / Assign / null), `cond` (expr / null), `step` (Assign / null), `body` |
| Print | `expr` |
| Return | `expr` |
| BinaryOp | `op`, `left`, `right` |
| UnaryOp | `op`, `operand` |
| Number | `value` |
| Var | `name` |

The semantic phase stores `unique_name` on VarDecl, Assign and Var nodes (also serialized).

### 4.5 Three-address code (TAC) format (exact text of each instruction)

| Form | Example |
|---|---|
| binary | `t1 = a + b` (ops: `+ - * / % < <= > >= == != && \|\|`) |
| unary | `t1 = -a`, `t1 = !a` |
| copy | `x = t1`, `x = 5` |
| label | `L1:` |
| jump | `goto L1` |
| conditional jump | `ifFalse t1 goto L2` (jumps when the operand equals 0) |
| output | `print a` |
| return | `return a` |

Operands are a variable name, a temp (`t1`, `t2`, ...) or an integer literal (negative literals appear as `-5`). Use one structured `Instr` class internally and one `format_instr` function for the text.

---

## 5. GROUND TRUTH (do not alter)

### 5.1 Program P1 (constant folding)

```c
int main() {
    int x = 2 + 3 * 4;
    int y = x * 1;
    print(y);
    return 0;
}
```

**Tokens**: 30 tokens plus EOF = 31 entries. The first 14 are:

| # | type | lexeme | line | col |
|---|---|---|---|---|
| 1 | KEYWORD | int | 1 | 1 |
| 2 | IDENTIFIER | main | 1 | 5 |
| 3 | DELIMITER | ( | 1 | 9 |
| 4 | DELIMITER | ) | 1 | 10 |
| 5 | DELIMITER | { | 1 | 12 |
| 6 | KEYWORD | int | 2 | 5 |
| 7 | IDENTIFIER | x | 2 | 9 |
| 8 | OPERATOR | = | 2 | 11 |
| 9 | NUMBER | 2 | 2 | 13 |
| 10 | OPERATOR | + | 2 | 15 |
| 11 | NUMBER | 3 | 2 | 17 |
| 12 | OPERATOR | * | 2 | 19 |
| 13 | NUMBER | 4 | 2 | 21 |
| 14 | DELIMITER | ; | 2 | 22 |

**AST**:

```
Program
└─ Function main
   └─ Block
      ├─ VarDecl x
      │  └─ BinaryOp +
      │     ├─ Number 2
      │     └─ BinaryOp *
      │        ├─ Number 3
      │        └─ Number 4
      ├─ VarDecl y
      │  └─ BinaryOp *
      │     ├─ Var x
      │     └─ Number 1
      ├─ Print
      │  └─ Var y
      └─ Return
         └─ Number 0
```

**Symbol table**: `x` (int, scope 1, line 2, unique `x`), `y` (int, scope 1, line 3, unique `y`). The function body block is scope 1; nested blocks get 2, 3, ... in order of appearance.

**TAC (unoptimized, 7 lines)**:

```
t1 = 3 * 4
t2 = 2 + t1
x = t2
t3 = x * 1
y = t3
print y
return 0
```

**Optimized TAC (2 lines)**:

```
print 14
return 0
```

Pass-by-pass in iteration 1 (use this as the log content):
- After Constant Folding & Propagation:
```
t1 = 12
t2 = 14
x = 14
t3 = 14
y = 14
print 14
return 0
```
- Passes 2 to 4 change nothing.
- After Dead Code Elimination: `print 14` / `return 0`. Iteration 2 changes nothing, so the optimizer stops.

**Output**: `["14"]`, exit code 0. Stats: 7 → 2.

### 5.2 Program P2 (while loop)

```c
int main() {
    int i = 0;
    int sum = 0;
    while (i < 3) {
        sum = sum + i;
        i = i + 1;
    }
    print(sum);
    return 0;
}
```

**TAC (unoptimized, 13 lines)**:

```
i = 0
sum = 0
L1:
t1 = i < 3
ifFalse t1 goto L2
t2 = sum + i
sum = t2
t3 = i + 1
i = t3
goto L1
L2:
print sum
return 0
```

**Optimized TAC (11 lines)**:

```
i = 0
sum = 0
L1:
t1 = i < 3
ifFalse t1 goto L2
sum = sum + i
i = i + 1
goto L1
L2:
print sum
return 0
```

(Only Temp Forwarding changes anything. Constants are never propagated into the loop because the constants map is reset at labels.) **Output**: `["3"]`. Stats: 13 → 11.

### 5.3 Program EX4 (if / else)

```c
int main() {
    int a = 10;
    int b = 20;
    if (a > b) { print(a); } else { print(b); }
    return 0;
}
```

**TAC (unoptimized, 9 lines)**:

```
a = 10
b = 20
t1 = a > b
ifFalse t1 goto L1
print a
goto L2
L1:
print b
L2:
return 0
```

**Optimized TAC (final, 2 lines)**:

```
print 20
return 0
```

**Output**: `["20"]`. Stats: 9 → 2. (Needs two optimizer iterations: constant `ifFalse 0` resolves the branch, then `b` propagates into `print b`.)

### 5.4 Program EX10 (dead branch)

```c
int main() {
    int debug = 0;
    if (debug) {
        print(999);
    }
    print(42);
    return 0;
}
```

**TAC (unoptimized, 6 lines)**:

```
debug = 0
ifFalse debug goto L1
print 999
L1:
print 42
return 0
```

**Optimized TAC (final, 2 lines)**:

```
print 42
return 0
```

**Output**: `["42"]`. Stats: 6 → 2.

### 5.5 TAC generation rules (these make labels and temps deterministic)

- Temps `t1, t2, ...` and labels `L1, L2, ...` use two separate counters that start at 1 and are never reused within the program.
- `genExpr(node)` returns an **operand**: for Number and Var it returns the literal / unique variable name without emitting anything; for BinaryOp it generates the left operand, then the right operand, then emits `tN = left op right` with a fresh temp; for UnaryOp it generates the operand and emits `tN = -x` or `tN = !x`.
- `VarDecl` with init: `name = operand`. Without init: `name = 0`. `Assign`: `name = operand`.
- `Print`: `print operand`. `Return`: `return operand`.
- **If without else**: allocate `Lend`; emit cond; `ifFalse c goto Lend`; then-branch; `Lend:`.
- **If with else**: allocate `Lelse`, then `Lend` (in that order, at entry); emit cond; `ifFalse c goto Lelse`; then-branch; `goto Lend`; `Lelse:`; else-branch; `Lend:`.
- **While**: allocate `Lstart`, then `Lend` (at entry); `Lstart:`; cond; `ifFalse c goto Lend`; body; `goto Lstart`; `Lend:`.
- **For**: init; allocate `Lstart`, `Lend`; `Lstart:`; if cond exists: cond, `ifFalse c goto Lend`; body; step; `goto Lstart`; `Lend:`.
- Block: just its statements in order.
- Unique names: the first declaration of a name in the function keeps its name; the second, third, ... declaration of the same name in a different scope become `name_1`, `name_2`, ... (assigned by the semantic phase in order of declaration).
- Implicit `return 0` is appended at the end of `main` unless the last statement of the body is a Return.

### 5.6 Example programs and expected outputs (these go in `examples.py` and the tests)

| id | name | expected output lines |
|---|---|---|
| ex1 | Constant folding (P1) | `14` |
| ex2 | While loop sum (P2) | `3` |
| ex3 | Factorial | `120` |
| ex4 | If / else (EX4) | `20` |
| ex5 | For loop | `15` |
| ex6 | Operator precedence | `11` |
| ex7 | Logical and unary | `6`, `1`, `1` |
| ex8 | Scope shadowing | `2`, `1` |
| ex9 | Nested loops | `6`, `12`, `18` |
| ex10 | Dead branch (EX10) | `42` |

ex1, ex2, ex4 and ex10 are exactly the programs in Sections 5.1 to 5.4. The others:

```c
// ex3: Factorial
int main() {
    int n = 5;
    int f = 1;
    int i = 1;
    while (i <= n) {
        f = f * i;
        i = i + 1;
    }
    print(f);
    return 0;
}
```

```c
// ex5: For loop
int main() {
    int s = 0;
    for (int i = 1; i <= 5; i = i + 1) {
        s = s + i;
    }
    print(s);
    return 0;
}
```

```c
// ex6: Operator precedence (2 + 12 - ((6/2) % 4) = 11)
int main() {
    print(2 + 3 * 4 - 6 / 2 % 4);
    return 0;
}
```

```c
// ex7: Logical and unary
int main() {
    print(-4 + 10);
    print((5 > 3) && !(2 == 3));
    print(7 % 3 == 1 || 0);
    return 0;
}
```

```c
// ex8: Scope shadowing (TAC uses x and x_1)
int main() {
    int x = 1;
    {
        int x = 2;
        print(x);
    }
    print(x);
    return 0;
}
```

```c
// ex9: Nested loops
int main() {
    int i = 1;
    while (i <= 3) {
        int j = 1;
        int row = 0;
        while (j <= 3) {
            row = row + i * j;
            j = j + 1;
        }
        print(row);
        i = i + 1;
    }
    return 0;
}
```

### 5.7 Error programs and exact expected messages (`formatted`)

| id | Program | Expected `formatted` |
|---|---|---|
| e1 | `int main() {` / `    int x = 5 @ 3;` / `    return 0;` / `}` | `Lexical error at line 2, column 15: unexpected character '@'` |
| e2 | `int main() {` / `    int x = 5` / `    print(x);` / `    return 0;` / `}` | `Syntax error at line 3, column 5: expected ';' but found 'print'` |
| e3 | `int main() {` / `    int x = 1;` / `    print(y);` / `    return 0;` / `}` | `Semantic error at line 3, column 11: variable 'y' is not declared` |
| e4 | `int main() {` / `    int x = 1;` / `    int x = 2;` / `    return 0;` / `}` | `Semantic error at line 3, column 9: variable 'x' is already declared in this scope` |
| e5 | `int main() {` / `    int z = 0;` / `    print(10 / z);` / `    return 0;` / `}` | `Runtime error: division by zero` (output `[]`) |
| e6 | `int main() {` / `    while (1) { }` / `    return 0;` / `}` | `Runtime error: step limit exceeded (possible infinite loop)` |

Each `/` above is a line break and indentation is 4 spaces. Error e5 and e6 must also occur with optimization on and off. The VM step limit is 500000 executed instructions.

### 5.8 Arithmetic reference values (`test_arith.py`)

- `wrap32(2**31) == -2**31`, `wrap32(2**31 - 1) == 2**31 - 1`, `wrap32(-2**31 - 1) == 2**31 - 1`
- `c_div(7, 2) == 3`, `c_div(-7, 2) == -3`, `c_div(7, -2) == -3`, `c_div(-7, -2) == 3`
- `c_mod(7, 2) == 1`, `c_mod(-7, 2) == -1`, `c_mod(7, -2) == 1`
- `eval_binop('<', 2, 3) == 1`, `eval_binop('&&', 2, 0) == 0`, `eval_binop('||', 0, 5) == 1`
- `eval_unop('!', 0) == 1`, `eval_unop('-', 5) == -5`

---

## 6. Phase-by-phase build instructions

### Phase A: foundations and lexer

`arith.py` (single source of truth, used by both the optimizer's folding and the VM, so the optimized and unoptimized results always agree):

```python
def wrap32(x):
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x & 0x80000000 else x

def c_div(a, b):            # truncate toward zero; caller guarantees b != 0
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q

def c_mod(a, b):
    return a - c_div(a, b) * b
```

`eval_binop(op, a, b)`: `+ - *` use `wrap32`; `/` and `%` raise `ZeroDivisionError` when `b == 0`, else `wrap32(c_div(...))` / `wrap32(c_mod(...))`; comparisons return 1 or 0; `&&` is 1 if both nonzero else 0; `||` is 1 if either nonzero else 0. `eval_unop('-', a)` is `wrap32(-a)`; `eval_unop('!', a)` is 1 if `a == 0` else 0.

`lexer.py`: single pass over the characters with line and column tracking (a newline resets col to 1). Longest match for two-character operators. Raise `CompileError("lexical", ...)` for the cases in Section 3.3. Always append an EOF token. Messages: `unexpected character 'X'`, `integer literal out of range`, `unterminated comment`.

### Phase B: parser and AST

- Hand-written recursive descent, one method per grammar rule in Section 3.4, with one-token lookahead (`peek`, `advance`, `expect(lexeme)`).
- Binary levels use loops (`while peek in ops`) and build left-associative trees.
- Error message formats:
  - `expect` failure: `expected 'X' but found 'Y'` (Y is the lexeme of the offending token; for EOF use `end of file`). Position = the offending token.
  - Failure inside `primary`: `expected expression but found 'Y'`.
  - A statement starting with an identifier not followed by `=`: `expected '=' but found 'Y'`.
  - Missing function name: `expected identifier but found 'Y'`.
- Every node records line and col of its first token. A `to_dict()` (or a generic serializer) produces the JSON in Section 4.4.
- A statement-level `else` without `if` is a syntax error (falls out of the grammar naturally: `expected expression but found 'else'`... if the generic path produces a different text, that is acceptable, but it must be a syntax error with a position).

### Phase C: semantic analyzer

- Scope stack of dicts. The function body block is scope 1; every nested block (and the `for` statement as a whole) opens a new scope with the next id (2, 3, ...). The `for` init declaration lives in the `for` scope.
- Checks: (1) variable used or assigned but not declared → `variable 'NAME' is not declared` (position of the identifier use); (2) redeclaration in the same scope → `variable 'NAME' is already declared in this scope` (position of the identifier in the declaration); (3) the function must be named `main` → `program must define 'int main()'` (position of the function name). The variable being declared is NOT visible inside its own initializer (`int x = x + 1;` with no outer `x` is an undeclared-variable error).
- Assign `unique_name` as described in Section 5.5. Fill the symbol table list (one row per declaration, in order of declaration).
- Type checking: there is a single type, so every expression is `int`. Record this in the report as "type checking is trivial because the language has only int".

### Phase D: TAC and code generation

Implement `tac.Instr` (fields: `op`, `dest`, `a`, `b`, `label`) and `format_instr`. Implement codegen exactly per Section 5.5. Verify against Sections 5.1 to 5.4 (unoptimized TAC).

### Phase E: optimizer

Operates on the list of `Instr`. Keep every pass a separate function that returns a new list, so the log can show each pass. Run the passes in this order, repeating the whole sequence until a full iteration changes nothing (maximum 10 iterations):

1. **Constant Folding & Propagation** (basic-block local). Keep a dict `consts` of name → literal. Reset `consts` at every label and after every `goto`, `ifFalse` and `return`. For each instruction: (a) replace every operand that is a name found in `consts` with its literal; (b) if it is a binary instruction with two literals and it is not `/` or `%` with a zero divisor, fold with `eval_binop` into `dest = literal`; unary with a literal operand likewise via `eval_unop`; (c) if the result is `dest = literal`, set `consts[dest] = literal`, else `consts.pop(dest, None)`.
2. **Algebraic Simplification**: `x = a + 0`, `x = 0 + a`, `x = a - 0`, `x = a * 1`, `x = 1 * a`, `x = a / 1` become `x = a`; `x = a * 0` and `x = 0 * a` become `x = 0`. (Do not simplify when the operand `a` is the only thing that could matter for a runtime error; there is none for these patterns.)
3. **Branch Simplification and Unreachable Code Removal**, in this exact sequence: (a) `ifFalse L goto X` where the operand is a literal: nonzero literal → remove the instruction; zero literal → replace with `goto X`; (b) after any `goto` or `return`, remove instructions up to (not including) the next label; (c) remove `goto L` when the very next instruction is `L:`; (d) remove labels that no `goto` or `ifFalse` references.
4. **Temp Forwarding**: for adjacent instructions `tN = <rhs>` followed by `v = tN` (copy), where `tN` is a temp and is read exactly once in the whole function (by that copy), replace both with `v = <rhs>`.
5. **Dead Code Elimination**: compute the set of all names that are read as operands anywhere in the function. Remove every assignment (binary, unary or copy) whose destination is not in that set. Never remove a `/` or `%` instruction whose divisor is not a nonzero literal (it could raise a runtime error). Repeat inside the pass until nothing more is removed.

Return the final list plus a log entry `{iteration, pass, tac}` for each pass that changed something. Verify against Sections 5.1 to 5.4 (final optimized TAC must match exactly).

### Phase F: virtual machine

- Execute TAC text-free from the `Instr` list (do not parse strings, and **never use `eval`, `exec` or `subprocess`**).
- Pre-compute a label → index map. Variables and temps live in one dict that defaults to 0 for unread names.
- Loop: `pc` from 0; `step_count` increases per executed instruction; if it exceeds 500000 raise `RuntimeErr("step limit exceeded (possible infinite loop)")`.
- `binary` and `unary` use `eval_*`; `ZeroDivisionError` becomes `RuntimeErr("division by zero")`. `ifFalse` jumps when the operand value is 0. `print` appends `str(value)` to the output list. `return` stops and sets the exit code. Reaching the end of the list means exit code 0.
- On `RuntimeErr`, the output already collected must be returned along with the error.

### Phase G: pipeline, API, examples

- Implement `compile_source` and the response shape of Section 4.3. Catch `CompileError` and `RuntimeErr` and map them to the `error` object and the `phases` map.
- `main.py`: FastAPI app with CORS for `http://localhost:5173`, the three routes of Section 4.3, and the 10000-character limit.
- `examples.py`: the ten programs of Section 5.6 with ids and display names (expected outputs are used by the tests via a separate dict in the test file or in `examples.py` under a name not exposed by the API).
- Run command: `cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000`

### Phase H: tests, **Gate 1**

Write and run `pytest`. Everything below must pass:

1. `test_arith.py`: all values of Section 5.8.
2. `test_lexer.py`: P1 yields exactly 31 tokens (including EOF) and the first 14 match the table in 5.1; `>=`, `==`, `!=`, `&&`, `||` are single tokens; comments are skipped; error e1 and `integer literal out of range` for `2147483648`.
3. `test_parser.py`: P1 AST structure equals the tree in 5.1; `1 - 2 - 3` is `(1 - 2) - 3`; the `1 + 2 * 3` tree has `*` below `+`; the dangling-else case attaches to the inner `if`; error e2.
4. `test_semantic.py`: e3, e4; ex8 produces unique names `x` and `x_1`; symbol-table scope ids for P1.
5. `test_codegen.py`: unoptimized TAC of P1, P2, EX4 and EX10 equals Section 5 **line by line**.
6. `test_optimizer.py`: final optimized TAC of P1, P2, EX4 and EX10 equals Section 5 line by line; stats match (7→2, 13→11, 9→2, 6→2).
7. `test_programs.py`: for each of ex1 to ex10, output equals Section 5.6 **with `optimize=true` and with `optimize=false`** (differential test, both must be identical including exit code 0); e1 to e6 produce exactly the `formatted` strings of Section 5.7 with optimization both on and off.
8. `test_api.py` (FastAPI `TestClient`): `/api/health`, `/api/examples` returns 10 entries, `/api/compile` for ex1 returns the response in 5.1 (`optimized_tac == ["print 14", "return 0"]`, `output == ["14"]`), error responses have the phase map of Section 4.3, source over 10000 characters returns 400.

**Gate 1 is passed only when all tests are green.** If a test fails because Section 5 and the code disagree, fix the code. If you believe Section 5 contains a genuine mistake, stop and report the exact discrepancy to the user instead of silently changing it.

---

## 7. Phase I: frontend (React + Vite, JavaScript)

Setup: `npm create vite@latest frontend -- --template react`, no UI library and no CSS framework (plain CSS in `styles.css`; a dark theme with one accent colour). `vite.config.js` proxies `/api` to `http://localhost:8000`. Run: `cd frontend && npm install && npm run dev` (port 5173).

Files in `src/`:

| File | Responsibility |
|---|---|
| `api.js` | `getExamples()`, `compile(source, optimize)`; `fetch` with try/catch; on network failure return a synthetic error "Backend not reachable. Start it with: uvicorn app.main:app --port 8000" |
| `App.jsx` | State, layout, toolbar, tab switching |
| `components/Editor.jsx` | `<textarea>` with a line-number gutter, monospace, Tab key inserts 4 spaces, error line highlighted |
| `components/PipelineBar.jsx` | Six boxes: Lexical → Syntax → Semantic → Code Gen → Optimizer → Execution. Colours: green ok, red error, grey skipped |
| `components/TokensTable.jsx` | Table: #, type, lexeme, line, col; token type shown as a coloured badge |
| `components/AstTree.jsx` | Collapsible tree of the AST JSON (expand and collapse all buttons) |
| `components/SymbolTable.jsx` | Table of name, unique name, type, scope, line |
| `components/TacView.jsx` | Two columns: Unoptimized TAC and Optimized TAC with line numbers, plus a stats chip such as "7 → 2 instructions (71% fewer)" and a collapsible Optimization Log listing each pass and its TAC |
| `components/OutputPanel.jsx` | Console-style output lines, exit code, and the runtime error if any |
| `components/ErrorBanner.jsx` | Red banner showing `error.formatted`; clicking it focuses the error line |

Layout and behaviour:
- Header: project title and course.
- Toolbar: Example dropdown (loads source into the editor), **Optimize** toggle (default on), **Run** button (Ctrl+Enter also runs), **Clear**.
- Left half: Editor. Right half: PipelineBar on top, then tabs **Tokens | AST | Symbol Table | TAC | Output**. After a run, the default tab is Output when execution succeeded; if an error occurred, the tab of the failing phase (Output for runtime errors).
- Tabs for phases that were skipped show an empty-state message ("This phase did not run because of an earlier error").
- Compile shows a loading state; the Run button is disabled while waiting.
- Responsive enough for a projector (1280×720) without horizontal page scroll.

**Gate 2 (manual, Antigravity must actually run the app and confirm):**
1. Selecting each of ex1 to ex10 and pressing Run shows the Output of Section 5.6.
2. ex1: the TAC tab shows 7 lines before and `print 14` / `return 0` after, with chip "7 → 2".
3. ex2: the optimized TAC equals Section 5.2.
4. Each error program e1 to e6 shows the exact message of Section 5.7, the pipeline bar turns red at the right phase, and later phases are grey.
5. Turning Optimize off hides the optimized column but the output stays the same.
6. Stopping the backend and pressing Run shows the "Backend not reachable" message instead of a crash.

---

## 8. Phase J: documents (after Gate 2)

Take screenshots with a real browser session (Antigravity's browser): editor plus pipeline bar, Tokens, AST, TAC before and after, Output, and one error case. Save them in `docs/screenshots/`. If screenshots cannot be captured, put clearly labelled placeholders and tell the user.

### 8.1 PPT (`Mini_C_Compiler_Presentation.pptx`, about 16 slides, 10-12 minutes)

Design: 16:9, Calibri, one accent colour, short bullets, native tables and diagrams, speaker notes (2-3 sentences) on every slide, team placeholders `[Name 1]` ... `[Name 5]`.

| # | Slide |
|---|---|
| 1 | Title: Mini C Compiler (Compiler Design 3170701, CIPAT Activity 2), college, team |
| 2 | Problem statement and objectives |
| 3 | What is supported: language features and limits (Section 3.1, 3.2) |
| 4 | Compiler pipeline overview diagram (six phases with CO labels) |
| 5 | Phase 1 Lexical analysis: token categories, P1 token excerpt |
| 6 | Phase 2 Parsing: the grammar (condensed), recursive descent, link to the LL(1) activity |
| 7 | AST for `int x = 2 + 3 * 4;` (tree diagram from 5.1) |
| 8 | Phase 3 Semantic analysis: symbol table, scopes, errors detected (e3, e4) |
| 9 | Phase 4 Intermediate code: three-address code forms, P2 unoptimized TAC beside the source |
| 10 | Phase 5 Optimization: the five passes, one line each |
| 11 | Optimization walkthrough on P1 (7 → 2 lines, with the pass log) |
| 12 | Branch optimization walkthrough on EX4 or EX10 |
| 13 | Phase 6 Execution: TAC virtual machine, 32-bit and C division semantics, step limit |
| 14 | System architecture: React frontend, FastAPI backend, API contract diagram |
| 15 | Live demo (screenshots as backup) and error handling for e1 to e6 |
| 16 | Limitations, future scope (functions, short-circuit, arrays, target code) and conclusion |

### 8.2 Report (`Mini_C_Compiler_Report.docx`, 18 to 25 pages)

Format: Times New Roman 12 pt, 1.5 spacing, numbered headings, table of contents, page numbers, captions for every figure and table. Title page with college, department, course, activity, group placeholders and date. Simple academic English, original wording.

1. Introduction and objectives
2. Problem statement and scope
3. Language specification (features, limits, deviations from C)
4. System architecture (diagram, technologies, API contract)
5. Lexical analysis (token table, error handling, with the P1 token excerpt)
6. Syntax analysis (grammar, recursive descent, AST design, AST of P1)
7. Semantic analysis (symbol table, scope rules, unique names, errors)
8. Intermediate code generation (TAC forms, generation rules, worked P2 example)
9. Code optimization (each pass with before and after example, optimizer iteration, P1 and EX4 walkthroughs)
10. Execution (VM design, arithmetic semantics, safety limits)
11. Frontend design and screenshots
12. Testing (test strategy, the ten programs and six error cases with results, differential testing of optimized versus unoptimized runs)
13. Mapping to course outcomes CO1 to CO4 (the table from Section 0)
14. Limitations and future work
15. Conclusion
16. References (Aho, Lam, Sethi, Ullman, *Compilers: Principles, Techniques, and Tools*, 2nd ed.; course notes)
- Appendix A: complete source code listing of the compiler modules. Appendix B: sample inputs and outputs.

### 8.3 `VIVA_NOTES.md`

Short, correct answers (2-4 lines each) to at least these questions:
1. What are the phases of your compiler and what does each produce?
2. Why is lexical analysis separate from parsing?
3. Which parsing technique did you use and why? How does it relate to LL(1)? (Recursive descent over an LL(1)-style grammar; left recursion avoided with loops.)
4. How does your grammar handle operator precedence and associativity?
5. What is an AST and how does it differ from a parse tree?
6. What does your symbol table store? How do you handle scopes and shadowing?
7. What is three-address code and why use it?
8. Explain constant folding, constant propagation, algebraic simplification, dead code elimination and temp forwarding with your own examples.
9. Why do you reset the constants map at labels? (A label can be reached from several places, so a value known on one path may not hold on another.)
10. Why can the optimizer not delete a division instruction freely? (It might hide a divide-by-zero runtime error.)
11. How is `ifFalse` implemented in the VM?
12. How do you guarantee the optimized program behaves like the original? (Shared arithmetic module and differential tests.)
13. Why is `&&` not short-circuit here, and what would you change to support it?
14. How do you prevent an infinite loop from freezing the server? (Step limit; no eval or exec.)
15. How would you add functions? (Parameters, call and return TAC, activation records or a call stack.)
16. How would you generate real assembly from the TAC? (Register or stack allocation, one TAC instruction to a few machine instructions.)
17. What kinds of errors does each phase detect? Give one example each.
18. What is panic-mode error recovery and why do you report only the first error?
19. Walk through `int x = 2 + 3 * 4;` through all phases.
20. Which course outcomes (CO1 to CO4) does the project cover and where?

### 8.4 `DEMO_SCRIPT.md` (5 minutes, exact steps)

1. Start backend and frontend (commands in README). Show the pipeline bar and the layout (20 s).
2. Load **ex1**, press Run: show Tokens (point out `2 + 3 * 4`), AST, Symbol Table, TAC (7 lines), Optimized TAC (`print 14`), Output `14` (90 s).
3. Load **ex2** (while loop): show labels and jumps in TAC and how only temp forwarding applies inside the loop (60 s).
4. Load **ex4** or **ex10**: show the branch disappearing in the optimized TAC (45 s).
5. Show errors: type e1, e2, e3 live, one per phase, and point at the red phase in the pipeline bar (60 s).
6. Show runtime error e5 and the infinite-loop guard e6 (30 s).
7. Close with architecture and limitations (15 s).

### 8.5 `README.md`

Purpose, features, requirements, install and run commands for both parts, the API summary, how to run the tests (`cd backend && pytest -q`), project structure, and the limitations list from Section 3.2.

### Gate 3

All documents exist; tables, TAC and outputs in the PPT and report are identical to Section 5; slide and page counts are within range; no text overflow when the PPT is converted to PDF; team placeholders are visible.

---

## 9. Optional stretch (only after Gate 3, never at the cost of the above)

**S1: pseudo-assembly tab (strengthens CO4).** Add a `codegen_asm.py` that translates the optimized TAC into a simple accumulator-style assembly, shown in a new "Assembly" tab. Mapping: `x = a op b` → `LOAD a`, `OP b`, `STORE x` (OP in ADD, SUB, MUL, DIV, MOD, CMPLT, CMPLE, CMPGT, CMPGE, CMPEQ, CMPNE, AND, OR); `x = -a` → `LOAD a`, `NEG`, `STORE x`; `x = !a` → `LOAD a`, `NOT`, `STORE x`; `x = a` → `LOAD a`, `STORE x`; `L:` → `L:`; `goto L` → `JMP L`; `ifFalse a goto L` → `LOAD a`, `JZ L`; `print a` → `LOAD a`, `PRINT`; `return a` → `LOAD a`, `HALT`. Optimized P1 becomes `LOAD 14`, `PRINT`, `LOAD 0`, `HALT`. Display only; execution still uses the TAC VM.

---

## 10. Final QA checklist

- [ ] `pytest -q` is fully green (Gate 1)
- [ ] Frontend manual checklist passed with the real running app (Gate 2)
- [ ] Docs complete and consistent with Section 5 (Gate 3)
- [ ] Final TAC and optimized TAC of P1, P2, EX4 and EX10 match Section 5 exactly
- [ ] Optimized and unoptimized runs agree on every example and error case
- [ ] No use of `eval`, `exec`, `subprocess` or `os.system` anywhere in the backend
- [ ] The app starts from scratch on a clean machine using only the README commands
- [ ] Team placeholders are visible and easy to replace
- [ ] The final message lists every file created, how to start the app, and any deviation from this plan

## 11. Rules for the agent

- Never modify the ground truth in Section 5 or the language rules in Section 3 to make a test pass.
- When code and Section 5 disagree, the code is wrong. If the plan itself is internally inconsistent, stop and describe the exact inconsistency to the user.
- Do not add libraries beyond those named. Do not add features beyond Section 3 (extras go only in Section 9, after Gate 3).
- Keep each compiler module readable and commented in simple English, because the team will explain the code in the viva.
- If a tool is missing (Node, Python version, a browser for screenshots), tell the user what to install instead of silently skipping the step.
