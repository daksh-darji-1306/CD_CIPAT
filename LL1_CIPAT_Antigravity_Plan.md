# LL(1) Parser: CIPAT Activity 1, Antigravity Implementation Plan

> Paste this whole file into Antigravity as the task. Execute the phases in order. Do not skip the verification gates. Do not change the grammar, tables or traces in Section 2, which are hand-verified ground truth.

## 0. Context and goal

- College: C. K. Pithawala College of Engineering and Technology, Computer Engineering
- Course: Compiler Design (3170701), Final Year Sem 7. Assessment: CIPAT 2026-27, Activity 1
- Task: "Select any one parser in detail with objectives and example and prepare a presentation on it." Selected parser: **LL(1)**
- Requirements from the brief:
  - A PPT **and** a report covering: objective, working principle, advantages, limitations, example.
  - The example **must include a parsing table and step-by-step string acceptance**.
- Marks: 5 = Objective, Working and Example; 5 = Presentation and Technical Explanation.
- Extra (not required, but strengthens the viva): a working Python implementation whose output matches the hand-made tables.
- Deadline: today. Work fast, but verify correctness.

### Deliverables (all saved in `./ll1_cipat/`)

| # | File | Description |
|---|---|---|
| 1 | `ll1.py` | Working LL(1) parser generator and driver |
| 2 | `output_accept.txt`, `output_reject.txt`, `output_tables.txt` | Captured real program output |
| 3 | `LL1_Parser_Presentation.pptx` | 11 slides |
| 4 | `LL1_Parser_Report.docx` | 10-12 page report |
| 5 | `VIVA_NOTES.md` | Q&A cheat sheet |
| 6 | `README.md` | How to run the code |

Tools: Python 3.10+ only. Use `python-pptx` for the PPT and `python-docx` for the report (`pip install python-pptx python-docx`). No other dependencies.

---

## 1. Phase order (checklist)

- [ ] Phase A: Create `ll1.py`, run it, and pass Gate 1
- [ ] Phase B: Capture outputs to text files
- [ ] Phase C: Generate the PPT and pass Gate 2
- [ ] Phase D: Generate the report and pass Gate 3
- [ ] Phase E: Write the viva notes and README
- [ ] Phase F: Final QA (Section 8)

---

## 2. GROUND TRUTH (do not alter)

### 2.1 Original grammar (left-recursive, NOT LL(1))

```
E → E + T | T
T → T * F | F
F → ( E ) | id
```

### 2.2 LL(1)-suitable grammar (left recursion removed)

```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → ( E ) | id
```

Left recursion removal rule: `A → Aα | β` becomes `A → βA'` and `A' → αA' | ε`.

### 2.3 FIRST sets

| Non-terminal | FIRST |
|---|---|
| E | { (, id } |
| E' | { +, ε } |
| T | { (, id } |
| T' | { *, ε } |
| F | { (, id } |

### 2.4 FOLLOW sets

| Non-terminal | FOLLOW |
|---|---|
| E | { $, ) } |
| E' | { $, ) } |
| T | { +, $, ) } |
| T' | { +, $, ) } |
| F | { *, +, $, ) } |

### 2.5 LL(1) parsing table M[A, a] (blank = error)

| | id | + | * | ( | ) | $ |
|---|---|---|---|---|---|---|
| **E** | E→TE' | | | E→TE' | | |
| **E'** | | E'→+TE' | | | E'→ε | E'→ε |
| **T** | T→FT' | | | T→FT' | | |
| **T'** | | T'→ε | T'→*FT' | | T'→ε | T'→ε |
| **F** | F→id | | | F→(E) | | |

No cell has more than one entry, so the grammar is LL(1).

### 2.6 Accepting trace for input `id + id * id $` (stack top on the LEFT)

| # | Stack | Input | Action |
|---|---|---|---|
| 1 | E $ | id + id * id $ | E → T E' |
| 2 | T E' $ | id + id * id $ | T → F T' |
| 3 | F T' E' $ | id + id * id $ | F → id |
| 4 | id T' E' $ | id + id * id $ | match id |
| 5 | T' E' $ | + id * id $ | T' → ε |
| 6 | E' $ | + id * id $ | E' → + T E' |
| 7 | + T E' $ | + id * id $ | match + |
| 8 | T E' $ | id * id $ | T → F T' |
| 9 | F T' E' $ | id * id $ | F → id |
| 10 | id T' E' $ | id * id $ | match id |
| 11 | T' E' $ | * id $ | T' → * F T' |
| 12 | * F T' E' $ | * id $ | match * |
| 13 | F T' E' $ | id $ | F → id |
| 14 | id T' E' $ | id $ | match id |
| 15 | T' E' $ | $ | T' → ε |
| 16 | E' $ | $ | E' → ε |
| 17 | $ | $ | **ACCEPT** |

### 2.7 Rejecting trace for `id + * id $`

| # | Stack | Input | Action |
|---|---|---|---|
| 1 | E $ | id + * id $ | E → T E' |
| 2 | T E' $ | id + * id $ | T → F T' |
| 3 | F T' E' $ | id + * id $ | F → id |
| 4 | id T' E' $ | id + * id $ | match id |
| 5 | T' E' $ | + * id $ | T' → ε |
| 6 | E' $ | + * id $ | E' → + T E' |
| 7 | + T E' $ | + * id $ | match + |
| 8 | T E' $ | * id $ | **ERROR**: M[T, *] is empty, so syntax error |

---

## 3. Phase A: `ll1.py` (create exactly this, then run)

```python
"""
LL(1) Parser: CIPAT Activity 1, Compiler Design (3170701)
Computes FIRST, FOLLOW, builds the predictive parsing table,
detects non-LL(1) conflicts, and runs a stack-based table-driven parser.
"""
import re
import sys

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
```

### Gate 1 (must pass before continuing)

Run `python ll1.py tables` and `python ll1.py` and confirm ALL of the following:
1. FIRST and FOLLOW printed by the code are identical to Sections 2.3 and 2.4.
2. The printed parsing table has exactly the 12 non-empty cells in Section 2.5 and no others.
3. `id+id*id` gives exactly 17 steps ending in ACCEPT, with the same actions as Section 2.6.
4. `id+*id` stops at step 8 with an error at M[T,*], matching Section 2.7.
5. Extra test: `(id+id)*id` returns ACCEPT and `id id` returns an error.

If any check fails, fix the code and never edit the ground truth.

---

## 4. Phase B: capture outputs

```
python ll1.py tables            > output_tables.txt
python ll1.py "id+id*id"        > output_accept.txt
python ll1.py "id+*id"          > output_reject.txt
```

Also render each of these three outputs to a clean PNG screenshot (monospace, dark background, using Pillow or matplotlib text rendering) for the PPT and report. Save them as `shot_tables.png`, `shot_accept.png` and `shot_reject.png`.

---

## 5. Phase C: PPT (`LL1_Parser_Presentation.pptx`, 11 slides)

Design rules:
- 16:9 layout. One accent colour (deep blue) plus a neutral background. Fonts: Calibri, titles 32 pt, body 20 pt or larger.
- Tables and diagrams instead of paragraphs. At most 5 bullets per slide. No walls of text.
- Every table is drawn as a real PPT table, not an image. Build the tables from the data in Section 2.
- Add short speaker notes (2-3 sentences) to every slide.

| # | Title | Content |
|---|---|---|
| 1 | LL(1) Parser | Title, course (Compiler Design 3170701), college, department, team names (leave placeholders `[Name 1]` ... `[Name 5]`) |
| 2 | Where Parsing Fits | Pipeline diagram (Source → Lexer → **Parser** → Semantic → ICG → Optimizer → Codegen) with Parser highlighted; one line on what the parser does |
| 3 | What is LL(1)? | L = Left-to-right scan, L = Leftmost derivation, 1 = one lookahead symbol; top-down predictive parsing, no backtracking |
| 4 | Objectives | Parse without backtracking; use a table-driven predictive approach; detect syntax errors early; run in linear time |
| 5 | Architecture | Diagram with Input buffer, Stack, Parsing table M[A,a], Driver program and Output (derivation) |
| 6 | Parsing Algorithm | Driver rules: (1) X = a = $ → accept; (2) X = a ≠ $ → pop and advance; (3) X terminal ≠ a → error; (4) X non-terminal → look up M[X,a], pop X, push RHS in reverse; blank → error |
| 7 | Grammar Preparation | Section 2.1 vs 2.2 side by side (before and after left recursion removal); the FIRST and FOLLOW rules in 3 lines each; note on left factoring |
| 8 | FIRST, FOLLOW and Parsing Table | Sections 2.3, 2.4 (compact) and the 2.5 table; note "No cell has 2 entries → LL(1)" |
| 9 | Step-by-Step Parsing: `id + id * id` | The 17-row trace from 2.6. If it does not fit, split into two slides (rows 1-9 and 10-17) and renumber the remaining slides |
| 10 | Error Case + Advantages / Limitations / Applications | Short reject trace (2.7) on the left; Advantages, Limitations and Applications in three compact columns on the right |
| 11 | Demo and Conclusion | Screenshots `shot_accept.png` and `shot_reject.png`; 3 conclusion bullets; "Thank you / Questions?" |

Content for slide 10:
- Advantages: simple, no backtracking, O(n) time, easy to implement and debug, good error detection.
- Limitations: cannot handle left-recursive or ambiguous grammars, needs left factoring, covers a smaller class of grammars than LR, difficult to recover from errors.
- Applications: recursive-descent parsers, configuration and data formats such as JSON, and teaching and simple compilers. ANTLR uses the extended LL(*) family.

### Gate 2

Open the generated PPTX (convert to PDF with LibreOffice if available and inspect the pages). Check that no text overflows or is cut off, tables are readable, the trace matches 2.6 exactly, and the slide count is 11 (or 12 if slide 9 was split).

---

## 6. Phase D: Report (`LL1_Parser_Report.docx`, 10-12 pages)

Formatting: Times New Roman 12 pt, 1.5 line spacing, headings numbered, page numbers in the footer, figure and table captions. Title page has the college name, course, activity, topic, team placeholders and the date. Include a table of contents.

Sections:

1. **Introduction**: the role of syntax analysis, CFG basics, top-down versus bottom-up parsing (short comparison table).
2. **Objective of the LL(1) Parser**
3. **Meaning of LL(1)**
4. **Working Principle**: components (input buffer, stack, table, driver) and the algorithm from slide 6, with a block diagram.
5. **Prerequisites**:
   - 5.1 Left recursion and its removal, with the rule and the worked example from 2.1 to 2.2.
   - 5.2 Left factoring, with a small separate example: `A → αβ1 | αβ2` becomes `A → αA'` and `A' → β1 | β2`.
   - 5.3 FIRST rules and FOLLOW rules (numbered).
   - 5.4 Rules to construct the table, and the condition for a grammar to be LL(1).
6. **Worked Example**:
   - the grammar, FIRST and FOLLOW tables, and the parsing table (from Section 2);
   - the accepting trace for `id + id * id` (2.6);
   - the rejecting trace for `id + * id` (2.7).
7. **Implementation**: an overview of `ll1.py` (functions and their roles), a code listing in an appendix, and the screenshots with captions.
8. **Advantages**
9. **Limitations**
10. **Applications**
11. **Conclusion**
12. **References**: Aho, Lam, Sethi, Ullman, *Compilers: Principles, Techniques, and Tools* (2nd ed.); Compiler Design course notes (GTU 3170701).

Use simple academic English and original wording. Do not copy text from websites.

### Gate 3

Verify that every table and trace in the report is identical to Section 2, that heading numbers and the table of contents are correct, and that the page count is 10-12 (a small overrun is acceptable). Check figure and table captions.

---

## 7. Phase E: `VIVA_NOTES.md` and `README.md`

`README.md`: what the project is, requirements (Python 3.10+), and the commands `python ll1.py`, `python ll1.py tables` and `python ll1.py "<string>"`, with example output.

`VIVA_NOTES.md` must contain concise, correct answers (2-4 lines each) to:
1. What does LL(1) stand for?
2. Why can't LL(1) handle left recursion, and how is it removed?
3. What is left factoring and why is it needed?
4. How are FIRST and FOLLOW computed? (Include a mini worked example.)
5. When is a production A → α entered in M[A, a]? (a in FIRST(α), or ε in FIRST(α) and a in FOLLOW(A).)
6. What makes a grammar LL(1)? (No multiply defined table entries: FIRST sets of alternatives are disjoint, and if one alternative derives ε then the other alternatives' FIRST sets are disjoint from FOLLOW(A).)
7. Time and space complexity. (Time O(n); the stack is O(n) at worst.)
8. LL(1) versus recursive descent versus LR (SLR, LALR, CLR).
9. What is panic-mode error recovery?
10. Is every context-free grammar LL(1)? (No; give the ambiguous-grammar and left-recursive examples.)
11. What is the role of `$`?
12. Walk through steps 1-5 of the trace on the board.
13. Why does the parser push the RHS in reverse order?
14. What would happen if the grammar were ambiguous? (Conflicts appear in the table.)

---

## 8. Final QA checklist

- [ ] `ll1.py` output matches Section 2 exactly (Gate 1)
- [ ] The three output text files and three screenshots exist
- [ ] PPT: 11-12 slides, tables are native, no overflow, speaker notes present (Gate 2)
- [ ] Report: all tables and traces match Section 2, TOC and captions present (Gate 3)
- [ ] Both files contain accept and reject examples
- [ ] Team-name placeholders are visible and easy to replace
- [ ] `VIVA_NOTES.md` and `README.md` exist
- [ ] Everything is inside `./ll1_cipat/` and runs on a fresh machine with `python ll1.py`
- [ ] Final message lists every file created, plus any deviations from this plan

## 9. Rules for the agent

- Never modify the grammar, FIRST/FOLLOW, table or traces in Section 2.
- Whenever the code and Section 2 disagree, the code is wrong.
- Do not invent extra features. Do not add libraries beyond `python-pptx`, `python-docx` (and Pillow or matplotlib for screenshots).
- If a tool is missing, tell the user what to install instead of silently skipping the step.
