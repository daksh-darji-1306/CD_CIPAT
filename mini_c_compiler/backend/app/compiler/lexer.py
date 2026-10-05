from .tokens import Token, KEYWORDS
from .errors import CompileError

def tokenize(source):
    tokens = []
    line = 1
    col = 1
    i = 0
    n = len(source)
    
    while i < n:
        c = source[i]
        
        # Newline
        if c == '\n':
            line += 1
            col = 1
            i += 1
            continue
            
        # Whitespace
        if c.isspace():
            col += 1
            i += 1
            continue
            
        # Comments
        if c == '/':
            if i + 1 < n and source[i+1] == '/':
                # Line comment
                i += 2
                col += 2
                while i < n and source[i] != '\n':
                    i += 1
                    col += 1
                continue
            elif i + 1 < n and source[i+1] == '*':
                # Block comment
                start_line = line
                start_col = col
                i += 2
                col += 2
                closed = False
                while i < n:
                    if source[i] == '\n':
                        line += 1
                        col = 1
                        i += 1
                    elif source[i] == '*' and i + 1 < n and source[i+1] == '/':
                        i += 2
                        col += 2
                        closed = True
                        break
                    else:
                        i += 1
                        col += 1
                if not closed:
                    raise CompileError("lexical", "unterminated comment", start_line, start_col)
                continue
                
        # Numbers
        if c.isdigit():
            start_col = col
            val_str = ""
            while i < n and source[i].isdigit():
                val_str += source[i]
                i += 1
                col += 1
            if int(val_str) > 2147483647:
                raise CompileError("lexical", "integer literal out of range", line, start_col)
            tokens.append(Token("NUMBER", val_str, line, start_col))
            continue
            
        # Identifiers and Keywords
        if c.isalpha() or c == '_':
            start_col = col
            val_str = ""
            while i < n and (source[i].isalnum() or source[i] == '_'):
                val_str += source[i]
                i += 1
                col += 1
            if val_str in KEYWORDS:
                tokens.append(Token("KEYWORD", val_str, line, start_col))
            else:
                tokens.append(Token("IDENTIFIER", val_str, line, start_col))
            continue
            
        # Operators and Delimiters
        if c in "(){};":
            tokens.append(Token("DELIMITER", c, line, col))
            i += 1
            col += 1
            continue
            
        # Two-char operators
        if i + 1 < n:
            two_char = source[i:i+2]
            if two_char in ("==", "!=", "<=", ">=", "&&", "||"):
                tokens.append(Token("OPERATOR", two_char, line, col))
                i += 2
                col += 2
                continue
                
        # Single-char operators
        if c in "+-*/%=<>!":
            tokens.append(Token("OPERATOR", c, line, col))
            i += 1
            col += 1
            continue
            
        if c == '&' or c == '|':
            raise CompileError("lexical", f"unexpected character '{c}'", line, col)
            
        # Any other character
        raise CompileError("lexical", f"unexpected character '{c}'", line, col)
        
    tokens.append(Token("EOF", "", line, col))
    return tokens
