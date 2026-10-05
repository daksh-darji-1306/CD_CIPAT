KEYWORDS = {"int", "if", "else", "while", "for", "print", "return"}

class Token:
    def __init__(self, type_, lexeme, line, col):
        self.type = type_
        self.lexeme = lexeme
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type}, {repr(self.lexeme)}, {self.line}, {self.col})"
        
    def to_dict(self):
        return {
            "type": self.type,
            "lexeme": self.lexeme,
            "line": self.line,
            "col": self.col
        }
