from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_LINE_SPACING

def set_normal_style(doc):
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.style.font.name = 'Times New Roman'
    h.style.font.color.rgb = None # default black
    return h

def main():
    doc = Document()
    set_normal_style(doc)

    # Title Page
    doc.add_paragraph('\n'*5)
    p = doc.add_paragraph('C. K. Pithawala College of Engineering and Technology')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].bold = True
    p.runs[0].font.size = Pt(16)
    
    p = doc.add_paragraph('Computer Engineering Department')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph('\n'*2)
    p = doc.add_paragraph('Compiler Design (3170701)\nCIPAT 2026-27, Activity 1')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].bold = True
    
    doc.add_paragraph('\n'*3)
    p = doc.add_paragraph('LL(1) Parser Report')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].font.size = Pt(20)
    p.runs[0].bold = True
    
    doc.add_paragraph('\n'*4)
    p = doc.add_paragraph('Team Members:\n[Name 1]\n[Name 2]\n[Name 3]\n[Name 4]\n[Name 5]')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p = doc.add_paragraph('\nDate: September 2026')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_page_break()

    # Table of Contents
    add_heading(doc, 'Table of Contents', level=1)
    doc.add_paragraph('1. Introduction')
    doc.add_paragraph('2. Objective of the LL(1) Parser')
    doc.add_paragraph('3. Meaning of LL(1)')
    doc.add_paragraph('4. Working Principle')
    doc.add_paragraph('5. Prerequisites')
    doc.add_paragraph('   5.1 Left recursion and its removal')
    doc.add_paragraph('   5.2 Left factoring')
    doc.add_paragraph('   5.3 FIRST and FOLLOW rules')
    doc.add_paragraph('   5.4 Table construction rules')
    doc.add_paragraph('6. Worked Example')
    doc.add_paragraph('7. Implementation')
    doc.add_paragraph('8. Advantages')
    doc.add_paragraph('9. Limitations')
    doc.add_paragraph('10. Applications')
    doc.add_paragraph('11. Conclusion')
    doc.add_paragraph('12. References')
    
    doc.add_page_break()

    # 1. Introduction
    add_heading(doc, '1. Introduction', level=1)
    doc.add_paragraph('Syntax analysis, also known as parsing, is the second phase of a compiler. It takes the token stream from the lexical analyzer and checks whether the expression made by the tokens is syntactically correct according to the rules of a context-free grammar (CFG). If it is correct, it constructs a parse tree or a derivation; otherwise, it reports syntax errors.')
    doc.add_paragraph('Top-down parsing starts from the root node (start symbol) and proceeds down to the leaves (terminals). In contrast, bottom-up parsing starts from the leaves and works up to the root. LL(1) is a widely used predictive top-down parsing method.')

    # 2. Objective
    add_heading(doc, '2. Objective of the LL(1) Parser', level=1)
    doc.add_paragraph('The primary objective of the LL(1) parser is to parse the input without backtracking. It achieves this by using a table-driven predictive approach. By looking at just one symbol ahead in the input, the parser knows exactly which production rule to apply. This enables the parser to run efficiently in linear time, O(n), and allows for early and precise detection of syntax errors.')

    # 3. Meaning of LL(1)
    add_heading(doc, '3. Meaning of LL(1)', level=1)
    doc.add_paragraph('The term LL(1) stands for:')
    doc.add_paragraph('• The first "L" stands for scanning the input from Left to right.')
    doc.add_paragraph('• The second "L" stands for producing a Leftmost derivation.')
    doc.add_paragraph('• The "1" stands for using one lookahead symbol of input at each step to make parsing action decisions.')

    doc.add_page_break()

    # 4. Working Principle
    add_heading(doc, '4. Working Principle', level=1)
    doc.add_paragraph('An LL(1) parser consists of four main components:')
    doc.add_paragraph('1. Input Buffer: Contains the string to be parsed, followed by the end-of-input marker, $.')
    doc.add_paragraph('2. Stack: Contains a sequence of grammar symbols with $ on the bottom. It holds the symbols needed to derive the input.')
    doc.add_paragraph('3. Parsing Table: A two-dimensional array M[A, a], where A is a non-terminal, and a is a terminal or $.')
    doc.add_paragraph('4. Driver Program: A loop that determines the next action based on the top of the stack and the current input symbol.')
    doc.add_paragraph('Algorithm rules:')
    doc.add_paragraph('- If top is $ and input is $, parsing is successful (ACCEPT).')
    doc.add_paragraph('- If top matches input terminal, pop top and advance input pointer.')
    doc.add_paragraph('- If top is a non-terminal, look up M[top, input]. If it contains a production, pop the top and push the right-hand side of the production in reverse order. If M[top, input] is blank, report an ERROR.')

    # 5. Prerequisites
    add_heading(doc, '5. Prerequisites', level=1)
    add_heading(doc, '5.1 Left Recursion and its Removal', level=2)
    doc.add_paragraph('A grammar is left-recursive if it has a non-terminal A such that there is a derivation A → Aα for some string α. Top-down parsers cannot handle left-recursive grammars as they can enter infinite loops.')
    doc.add_paragraph('Removal Rule: A → Aα | β becomes A → βA\' and A\' → αA\' | ε.')
    doc.add_paragraph('Original Grammar (Left-recursive):\nE → E + T | T\nT → T * F | F\nF → ( E ) | id')
    doc.add_paragraph('LL(1)-suitable Grammar (Left recursion removed):\nE → T E\'\nE\' → + T E\' | ε\nT → F T\'\nT\' → * F T\' | ε\nF → ( E ) | id')

    add_heading(doc, '5.2 Left Factoring', level=2)
    doc.add_paragraph('Left factoring is required when two or more productions of a non-terminal share a common prefix. Example: A → αβ1 | αβ2 becomes A → αA\' and A\' → β1 | β2.')

    add_heading(doc, '5.3 FIRST and FOLLOW Rules', level=2)
    doc.add_paragraph('FIRST(α) is the set of terminals that begin the strings derivable from α.')
    doc.add_paragraph('FOLLOW(A) is the set of terminals that can appear immediately to the right of A in some sentential form.')

    add_heading(doc, '5.4 Table Construction Rules', level=2)
    doc.add_paragraph('For each production A → α:')
    doc.add_paragraph('1. For each terminal a in FIRST(α), add A → α to M[A, a].')
    doc.add_paragraph('2. If ε is in FIRST(α), add A → α to M[A, b] for each terminal b in FOLLOW(A).')

    doc.add_page_break()

    # 6. Worked Example
    add_heading(doc, '6. Worked Example', level=1)
    
    doc.add_paragraph('FIRST Sets:')
    doc.add_paragraph('E: { (, id }\nE\': { +, ε }\nT: { (, id }\nT\': { *, ε }\nF: { (, id }')
    
    doc.add_paragraph('FOLLOW Sets:')
    doc.add_paragraph('E: { $, ) }\nE\': { $, ) }\nT: { +, $, ) }\nT\': { +, $, ) }\nF: { *, +, $, ) }')

    doc.add_paragraph('Parsing Table M[A, a]:')
    table = doc.add_table(rows=6, cols=7)
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    hdr_cells[1].text = 'id'; hdr_cells[2].text = '+'; hdr_cells[3].text = '*'; hdr_cells[4].text = '('; hdr_cells[5].text = ')'; hdr_cells[6].text = '$'
    table.rows[1].cells[0].text = 'E'; table.rows[1].cells[1].text = "E→TE'"; table.rows[1].cells[4].text = "E→TE'"
    table.rows[2].cells[0].text = "E'"; table.rows[2].cells[2].text = "E'→+TE'"; table.rows[2].cells[5].text = "E'→ε"; table.rows[2].cells[6].text = "E'→ε"
    table.rows[3].cells[0].text = 'T'; table.rows[3].cells[1].text = "T→FT'"; table.rows[3].cells[4].text = "T→FT'"
    table.rows[4].cells[0].text = "T'"; table.rows[4].cells[3].text = "T'→*FT'"; table.rows[4].cells[5].text = "T'→ε"; table.rows[4].cells[6].text = "T'→ε"
    table.rows[5].cells[0].text = 'F'; table.rows[5].cells[1].text = "F→id"; table.rows[5].cells[4].text = "F→(E)"
    doc.add_paragraph('No cell has more than one entry, so the grammar is LL(1).')
    
    doc.add_paragraph('\nAccepting trace for input "id + id * id $"')
    acc_table = doc.add_table(rows=18, cols=4)
    acc_table.style = 'Table Grid'
    data1 = [
        ["#", "Stack", "Input", "Action"],
        ["1", "E $", "id + id * id $", "E → T E'"],
        ["2", "T E' $", "id + id * id $", "T → F T'"],
        ["3", "F T' E' $", "id + id * id $", "F → id"],
        ["4", "id T' E' $", "id + id * id $", "match id"],
        ["5", "T' E' $", "+ id * id $", "T' → ε"],
        ["6", "E' $", "+ id * id $", "E' → + T E'"],
        ["7", "+ T E' $", "+ id * id $", "match +"],
        ["8", "T E' $", "id * id $", "T → F T'"],
        ["9", "F T' E' $", "id * id $", "F → id"],
        ["10", "id T' E' $", "id * id $", "match id"],
        ["11", "T' E' $", "* id $", "T' → * F T'"],
        ["12", "* F T' E' $", "* id $", "match *"],
        ["13", "F T' E' $", "id $", "F → id"],
        ["14", "id T' E' $", "id $", "match id"],
        ["15", "T' E' $", "$", "T' → ε"],
        ["16", "E' $", "$", "E' → ε"],
        ["17", "$", "$", "ACCEPT"]
    ]
    for i, row in enumerate(data1):
        for j, val in enumerate(row):
            acc_table.cell(i, j).text = val

    doc.add_page_break()

    doc.add_paragraph('\nRejecting trace for input "id + * id $"')
    rej_table = doc.add_table(rows=9, cols=4)
    rej_table.style = 'Table Grid'
    data2 = [
        ["#", "Stack", "Input", "Action"],
        ["1", "E $", "id + * id $", "E → T E'"],
        ["2", "T E' $", "id + * id $", "T → F T'"],
        ["3", "F T' E' $", "id + * id $", "F → id"],
        ["4", "id T' E' $", "id + * id $", "match id"],
        ["5", "T' E' $", "+ * id $", "T' → ε"],
        ["6", "E' $", "+ * id $", "E' → + T E'"],
        ["7", "+ T E' $", "+ * id $", "match +"],
        ["8", "T E' $", "* id $", "ERROR: M[T, *] is empty, so syntax error"]
    ]
    for i, row in enumerate(data2):
        for j, val in enumerate(row):
            rej_table.cell(i, j).text = val

    # 7. Implementation
    doc.add_page_break()
    add_heading(doc, '7. Implementation', level=1)
    doc.add_paragraph('The parser was implemented in Python using a modular design. The ll1.py script features:')
    doc.add_paragraph('- compute_first(): Calculates the FIRST set for each non-terminal.')
    doc.add_paragraph('- compute_follow(): Calculates the FOLLOW set using the FIRST sets.')
    doc.add_paragraph('- build_table(): Constructs the M[A, a] table and checks for LL(1) conflicts.')
    doc.add_paragraph('- parse(): Acts as the driver program implementing the stack-based parsing logic.')
    
    try:
        doc.add_picture('shot_accept.png', width=Inches(6))
        doc.add_paragraph('Figure 1: Screenshot showing successful parsing of valid input.', style='Caption')
    except:
        pass
        
    try:
        doc.add_picture('shot_reject.png', width=Inches(6))
        doc.add_paragraph('Figure 2: Screenshot showing syntax error handling for invalid input.', style='Caption')
    except:
        pass

    # 8. Advantages
    add_heading(doc, '8. Advantages', level=1)
    doc.add_paragraph('LL(1) parsers are simple, easy to implement, and execute in linear time O(n). They do not require backtracking. Error detection is robust and pinpoints exactly where the input diverges from the expected grammar rules.')

    # 9. Limitations
    add_heading(doc, '9. Limitations', level=1)
    doc.add_paragraph('They cannot handle ambiguous or left-recursive grammars. The grammar must often be transformed (left factored and left-recursion removed), which can make it less intuitive. Furthermore, LL(1) recognizes a smaller class of languages compared to bottom-up parsers like LR.')

    # 10. Applications
    add_heading(doc, '10. Applications', level=1)
    doc.add_paragraph('LL(1) parsing is widely used in recursive descent parsers, configuration file processing (e.g. JSON parsers), and educational compilers. Advanced variants like LL(*) are used by tools like ANTLR.')

    # 11. Conclusion
    add_heading(doc, '11. Conclusion', level=1)
    doc.add_paragraph('The LL(1) parser is a foundational top-down parsing technique that provides efficient and predictable parsing for an important subset of context-free languages. In this activity, we successfully implemented an LL(1) parser in Python, demonstrating its predictive parsing table and stack trace operations.')

    # 12. References
    add_heading(doc, '12. References', level=1)
    doc.add_paragraph('1. Aho, Lam, Sethi, Ullman, Compilers: Principles, Techniques, and Tools (2nd ed.).')
    doc.add_paragraph('2. Compiler Design course notes (GTU 3170701).')

    doc.save('LL1_Parser_Report.docx')

if __name__ == "__main__":
    main()
