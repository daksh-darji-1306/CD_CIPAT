from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def add_title_slide(prs, title, subtitle):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    slide.placeholders[1].text = subtitle
    return slide

def add_bullet_slide(prs, title, bullets, notes=""):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    tf = slide.placeholders[1].text_frame
    for i, bullet in enumerate(bullets):
        if i == 0:
            tf.text = bullet
        else:
            p = tf.add_paragraph()
            p.text = bullet
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide

def main():
    prs = Presentation()
    # Slide 1
    add_title_slide(prs, "LL(1) Parser", 
                    "Compiler Design (3170701)\nC. K. Pithawala College of Engineering and Technology\nComputer Engineering\n\nTeam: [Name 1], [Name 2], [Name 3], [Name 4], [Name 5]")
    
    # Slide 2
    slide = add_bullet_slide(prs, "Where Parsing Fits", 
                             ["Pipeline:", "Source → Lexer → **Parser** → Semantic → ICG → Optimizer → Codegen", 
                              "The parser takes tokens and builds a derivation (parse tree)."], 
                             notes="The parser is the core of syntax analysis. We are focusing on the top-down parser today.")
    
    # Slide 3
    add_bullet_slide(prs, "What is LL(1)?", 
                     ["L = Left-to-right scan of input", 
                      "L = Leftmost derivation", 
                      "1 = one lookahead symbol", 
                      "Top-down predictive parsing", 
                      "No backtracking needed"], 
                     notes="LL(1) is highly efficient because it predicts the rule to use by looking at just one symbol ahead.")

    # Slide 4
    add_bullet_slide(prs, "Objectives", 
                     ["Parse without backtracking", 
                      "Use a table-driven predictive approach", 
                      "Detect syntax errors early", 
                      "Run in linear time (O(n))"], 
                     notes="Our goal with this LL(1) parser is speed and clear error detection.")

    # Slide 5
    add_bullet_slide(prs, "Architecture", 
                     ["Input buffer: contains string to parse followed by $", 
                      "Stack: holds grammar symbols, bottom is $", 
                      "Parsing table M[A,a]: 2D array predicting rules", 
                      "Driver program: executes actions", 
                      "Output: the sequence of derivations"], 
                     notes="These are the main data structures. The driver loops and checks the table.")

    # Slide 6
    add_bullet_slide(prs, "Parsing Algorithm", 
                     ["Driver rules:",
                      "(1) X = a = $ → accept", 
                      "(2) X = a ≠ $ → pop and advance", 
                      "(3) X terminal ≠ a → error", 
                      "(4) X non-terminal → look up M[X,a], pop X, push RHS in reverse", 
                      "If M[X,a] is blank → error"], 
                     notes="The algorithm simply matches terminals, or expands non-terminals using the predictive table.")

    # Slide 7
    add_bullet_slide(prs, "Grammar Preparation", 
                     ["Original: E → E+T | T; T → T*F | F; F → (E) | id", 
                      "After left recursion removal: E → TE'; E' → +TE' | ε ...", 
                      "FIRST: terminals that begin the strings derivable from a symbol", 
                      "FOLLOW: terminals that can appear immediately to the right of a non-terminal",
                      "Left factoring: required if two rules share a prefix."], 
                     notes="We must eliminate left recursion and perform left factoring to make a grammar LL(1).")

    # Slide 8 - Table
    slide8 = prs.slides.add_slide(prs.slide_layouts[5])
    slide8.shapes.title.text = "FIRST, FOLLOW and Parsing Table"
    slide8.notes_slide.notes_text_frame.text = "The table has no overlapping entries, so the grammar is LL(1)."
    
    x, y, cx, cy = Inches(0.5), Inches(1.5), Inches(9), Inches(3.5)
    shape = slide8.shapes.add_table(6, 7, x, y, cx, cy)
    table = shape.table
    table.cell(0,1).text = 'id'; table.cell(0,2).text = '+'; table.cell(0,3).text = '*'
    table.cell(0,4).text = '('; table.cell(0,5).text = ')'; table.cell(0,6).text = '$'
    
    table.cell(1,0).text = 'E'; table.cell(1,1).text = "E→TE'"; table.cell(1,4).text = "E→TE'"
    table.cell(2,0).text = "E'"; table.cell(2,2).text = "E'→+TE'"; table.cell(2,5).text = "E'→ε"; table.cell(2,6).text = "E'→ε"
    table.cell(3,0).text = 'T'; table.cell(3,1).text = "T→FT'"; table.cell(3,4).text = "T→FT'"
    table.cell(4,0).text = "T'"; table.cell(4,3).text = "T'→*FT'"; table.cell(4,5).text = "T'→ε"; table.cell(4,6).text = "T'→ε"
    table.cell(5,0).text = 'F'; table.cell(5,1).text = "F→id"; table.cell(5,4).text = "F→(E)"

    # Slide 9 - Trace
    slide9 = prs.slides.add_slide(prs.slide_layouts[5])
    slide9.shapes.title.text = "Step-by-Step Parsing: id + id * id (1-8)"
    x, y, cx, cy = Inches(0.5), Inches(1.5), Inches(9), Inches(4)
    shape = slide9.shapes.add_table(9, 4, x, y, cx, cy)
    table = shape.table
    table.cell(0,0).text = '#'; table.cell(0,1).text = 'Stack'; table.cell(0,2).text = 'Input'; table.cell(0,3).text = 'Action'
    data1 = [
        ["1", "E $", "id + id * id $", "E → T E'"],
        ["2", "T E' $", "id + id * id $", "T → F T'"],
        ["3", "F T' E' $", "id + id * id $", "F → id"],
        ["4", "id T' E' $", "id + id * id $", "match id"],
        ["5", "T' E' $", "+ id * id $", "T' → ε"],
        ["6", "E' $", "+ id * id $", "E' → + T E'"],
        ["7", "+ T E' $", "+ id * id $", "match +"],
        ["8", "T E' $", "id * id $", "T → F T'"]
    ]
    for i, row in enumerate(data1):
        for j, val in enumerate(row):
            table.cell(i+1, j).text = val
    slide9.notes_slide.notes_text_frame.text = "This shows the stack expanding and matching tokens."

    # Slide 10 - Trace part 2
    slide10 = prs.slides.add_slide(prs.slide_layouts[5])
    slide10.shapes.title.text = "Step-by-Step Parsing: id + id * id (9-17)"
    shape = slide10.shapes.add_table(10, 4, x, y, cx, cy)
    table = shape.table
    table.cell(0,0).text = '#'; table.cell(0,1).text = 'Stack'; table.cell(0,2).text = 'Input'; table.cell(0,3).text = 'Action'
    data2 = [
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
    for i, row in enumerate(data2):
        for j, val in enumerate(row):
            table.cell(i+1, j).text = val
    slide10.notes_slide.notes_text_frame.text = "The parsing concludes when the stack and input both contain only $."

    # Slide 11 - Error Case
    slide11 = prs.slides.add_slide(prs.slide_layouts[5])
    slide11.shapes.title.text = "Error Case (id + * id) & Attributes"
    x, y, cx, cy = Inches(0.2), Inches(1.5), Inches(4.5), Inches(3)
    shape = slide11.shapes.add_table(9, 3, x, y, cx, cy)
    table = shape.table
    table.cell(0,0).text = 'Stack'; table.cell(0,1).text = 'Input'; table.cell(0,2).text = 'Action'
    err_data = [
        ["E $", "id + * id $", "E → T E'"],
        ["T E' $", "id + * id $", "T → F T'"],
        ["F T' E' $", "id + * id $", "F → id"],
        ["id T' E' $", "id + * id $", "match id"],
        ["T' E' $", "+ * id $", "T' → ε"],
        ["E' $", "+ * id $", "E' → + T E'"],
        ["+ T E' $", "+ * id $", "match +"],
        ["T E' $", "* id $", "ERROR: M[T,*] empty"]
    ]
    for i, row in enumerate(err_data):
        for j, val in enumerate(row):
            table.cell(i+1, j).text = val
            
    txBox = slide11.shapes.add_textbox(Inches(5), Inches(1.5), Inches(4.5), Inches(3))
    tf = txBox.text_frame
    tf.text = "Advantages: Simple, no backtracking, O(n) time, easy to debug."
    p2 = tf.add_paragraph(); p2.text = "Limitations: No left recursion, needs left factoring, less powerful than LR, hard to recover from errors."
    p3 = tf.add_paragraph(); p3.text = "Applications: Recursive descent, data formats (JSON), teaching compilers."
    slide11.notes_slide.notes_text_frame.text = "Here we see an error caught correctly. Also summarizing advantages and limitations."

    # Slide 12 - Conclusion
    slide12 = prs.slides.add_slide(prs.slide_layouts[5])
    slide12.shapes.title.text = "Demo and Conclusion"
    txBox = slide12.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(1.5))
    tf = txBox.text_frame
    tf.text = "- Successfully implemented LL(1) parsing in Python.\n- Handled First/Follow generation and trace simulation.\n- Thank you! Questions?"
    
    try:
        slide12.shapes.add_picture("shot_accept.png", Inches(0.5), Inches(3), width=Inches(4))
        slide12.shapes.add_picture("shot_reject.png", Inches(5), Inches(3), width=Inches(4))
    except:
        pass # ignore if pictures not found
    
    slide12.notes_slide.notes_text_frame.text = "Thank you."

    prs.save("LL1_Parser_Presentation.pptx")

if __name__ == "__main__":
    main()
