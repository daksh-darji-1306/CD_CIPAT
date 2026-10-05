# VIVA NOTES: LL(1) Parser

**1. What does LL(1) stand for?**
The first "L" stands for scanning the input from Left to right. The second "L" stands for producing a Leftmost derivation. The "1" means using one lookahead symbol to make parsing decisions.

**2. Why can't LL(1) handle left recursion, and how is it removed?**
Top-down parsers like LL(1) will enter an infinite loop trying to expand a left-recursive rule like `A → Aα`. It is removed by converting `A → Aα | β` into right recursion: `A → βA'` and `A' → αA' | ε`.

**3. What is left factoring and why is it needed?**
Left factoring is required when two productions share a common prefix, e.g., `A → αβ1 | αβ2`. It's needed because an LL(1) parser with 1 lookahead cannot decide which production to choose. The fix factors out the prefix: `A → αA'` and `A' → β1 | β2`.

**4. How are FIRST and FOLLOW computed? (Include a mini worked example.)**
FIRST(α) is the set of terminals that start strings derived from α. FOLLOW(A) is the set of terminals immediately right of A. Example: For `E → TE'`, `FIRST(E)` is the same as `FIRST(T)`. Because `)` follows `E` in `F → (E)`, `)` is in `FOLLOW(E)`.

**5. When is a production A → α entered in M[A, a]?**
It is entered if the terminal `a` is in `FIRST(α)`. Furthermore, if `ε` is in `FIRST(α)`, then the production is also entered in `M[A, b]` for every terminal `b` in `FOLLOW(A)`.

**6. What makes a grammar LL(1)?**
A grammar is LL(1) if its parsing table has no multiply-defined entries. This means the FIRST sets of any alternatives must be disjoint, and if one alternative derives ε, the FIRST sets of the other alternatives must be disjoint from the FOLLOW set of the non-terminal.

**7. Time and space complexity.**
The time complexity of parsing an input of length n is O(n), as each symbol is matched in constant time without backtracking. The space complexity is O(n) in the worst case, as the parsing stack may grow proportionally to the input size.

**8. LL(1) versus recursive descent versus LR (SLR, LALR, CLR).**
Recursive descent uses recursive function calls, while LL(1) uses an explicit stack and a predictive table. LR parsers (SLR, LALR, CLR) are bottom-up and more powerful (they handle left recursion and a larger class of grammars), but their tables are much more complex to construct.

**9. What is panic-mode error recovery?**
Panic-mode error recovery involves discarding input symbols one by one until a "synchronizing token" (like a semicolon, `)`, or `$`) is found. This helps the parser to resume parsing the rest of the file rather than aborting immediately on the first error.

**10. Is every context-free grammar LL(1)?**
No. Ambiguous grammars and left-recursive grammars are never LL(1). For example, `E → E + E` is both left-recursive and ambiguous, meaning its parsing table would have multiple entries per cell, violating the LL(1) condition.

**11. What is the role of `$`?**
The `$` symbol represents the end-of-input marker. It is placed at the end of the input buffer and at the bottom of the parsing stack to indicate when parsing has successfully completed.

**12. Walk through steps 1-5 of the trace on the board.**
1. Stack: `E$`, Input: `id...$`. Pop `E`, push `T E'` (since M[E, id] is `E → TE'`).
2. Stack: `T E'$`, Input: `id...$`. Pop `T`, push `F T'`.
3. Stack: `F T' E'$`, Input: `id...$`. Pop `F`, push `id`.
4. Stack: `id T' E'$`, Input: `id...$`. Match `id`. Pop `id`, advance input.
5. Stack: `T' E'$`, Input: `+...$`. Pop `T'`, push `ε` (since M[T', +] is `T' → ε`).

**13. Why does the parser push the RHS in reverse order?**
The parser pushes the right-hand side (RHS) of a production in reverse order so that the first symbol of the RHS ends up at the top of the stack. This aligns perfectly with the left-to-right scanning of the input string.

**14. What would happen if the grammar were ambiguous?**
If the grammar were ambiguous, multiple derivations would be possible for the same input string. In the LL(1) construction, this causes "conflicts," meaning a cell in the predictive parsing table M[A, a] would contain more than one production rule.
