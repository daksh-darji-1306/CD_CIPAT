# Mini C Compiler: Viva Notes

1. **What are the phases of your compiler and what does each produce?**
   Lexical analysis (tokens), Parsing (AST), Semantic analysis (symbol table and type checking), Code generation (unoptimized TAC), Optimization (optimized TAC), Execution (VM output).

2. **Why is lexical analysis separate from parsing?**
   It simplifies the parser by removing whitespace and comments, and grouping characters into meaningful tokens. It's also more efficient to scan characters than to parse them.

3. **Which parsing technique did you use and why? How does it relate to LL(1)?**
   We used handwritten recursive descent parsing over an LL(1)-style grammar. We removed left recursion in expressions using loops (like `(op term)*`), which is similar to the E / E' transformation from the LL(1) activity.

4. **How does your grammar handle operator precedence and associativity?**
   Precedence is encoded in the grammar hierarchy (e.g., `additive` calls `term`). Left associativity is handled using `while` loops in the parser, constructing trees that group left-to-right.

5. **What is an AST and how does it differ from a parse tree?**
   An Abstract Syntax Tree represents the logical structure of the code, omitting syntactic details like parentheses and semicolons that are present in a parse tree.

6. **What does your symbol table store? How do you handle scopes and shadowing?**
   It stores variable names, their unique renamed versions, type (`int`), scope depth, and declaration line. Scopes are handled via a stack of dictionaries. Shadowing is resolved by giving variables unique names based on a counter per variable.

7. **What is three-address code and why use it?**
   TAC is an intermediate representation where each instruction has at most one operator and at most three operands. It is easy to optimize and closer to machine code.

8. **Explain constant folding, constant propagation, algebraic simplification, dead code elimination and temp forwarding with your own examples.**
   - Constant Folding/Propagation: `x = 2 + 3` becomes `x = 5`. If `y = x`, `y = 5`.
   - Algebraic Simplification: `x = a + 0` becomes `x = a`.
   - Dead Code Elimination: Removing `x = 5` if `x` is never used.
   - Temp Forwarding: `t1 = a + b; x = t1` becomes `x = a + b`.

9. **Why do you reset the constants map at labels?**
   A label can be reached from multiple paths (like loops or if statements). A variable's value known on one path may not be the same on another path.

10. **Why can the optimizer not delete a division instruction freely?**
    It might hide a divide-by-zero runtime error, changing the program's runtime semantics.

11. **How is `ifFalse` implemented in the VM?**
    The VM evaluates the operand. If it equals 0, it changes the program counter (`pc`) to the instruction index of the target label. Otherwise, it proceeds to the next instruction.

12. **How do you guarantee the optimized program behaves like the original?**
    Both use the exact same shared arithmetic module, and we use differential testing to ensure outputs match exactly with optimization on and off.

13. **Why is `&&` not short-circuit here, and what would you change to support it?**
    We evaluate both sides to simplify code generation. To support short-circuiting, we would need to generate control flow (jumps) instead of a simple binary evaluation for `&&`.

14. **How do you prevent an infinite loop from freezing the server?**
    The VM has a strict step limit (500,000 instructions) and we do not use `eval` or `exec`.

15. **How would you add functions?**
    We'd need to add parameters, call and return TAC instructions, and manage activation records (a call stack) in the VM instead of a single global environment.

16. **How would you generate real assembly from the TAC?**
    We would use register or stack allocation, mapping each TAC instruction to a sequence of machine instructions (e.g., `LOAD`, `ADD`, `STORE`).

17. **What kinds of errors does each phase detect? Give one example each.**
    Lexical: `unexpected character '@'`. Syntax: `expected ';' but found 'print'`. Semantic: `variable 'x' is not declared`. Runtime: `division by zero`.

18. **What is panic-mode error recovery and why do you report only the first error?**
    Panic-mode recovery skips tokens until a synchronization point (like `;`) to report multiple errors. We report only the first error to keep the compiler implementation simple and focused.

19. **Walk through `int x = 2 + 3 * 4;` through all phases.**
    Tokens: `int`, `x`, `=`, `2`, `+`, `3`, `*`, `4`, `;`.
    AST: VarDecl(x, BinaryOp(+, 2, BinaryOp(*, 3, 4))).
    Semantic: Symbol table gets `x`.
    TAC: `t1 = 3 * 4; t2 = 2 + t1; x = t2`.
    Optimized: `x = 14`.

20. **Which course outcomes (CO1 to CO4) does the project cover and where?**
    CO1 (Lexical): `lexer.py`, CO2 (Parsing): `parser.py`, CO3 (Semantic & Optimization): `semantic.py`, `optimizer.py`, CO4 (Runtime/Target): `vm.py` and web UI integration.
