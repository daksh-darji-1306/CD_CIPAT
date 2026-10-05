from .errors import CompileError
from .ast_nodes import (
    Program, Function, Block, VarDecl, Assign, If, While, For, Print, Return,
    BinaryOp, UnaryOp, Number, Var
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def advance(self):
        t = self.peek()
        if t.type != "EOF":
            self.pos += 1
        return t

    def expect(self, lexeme):
        t = self.peek()
        if t.lexeme == lexeme:
            return self.advance()
        val = t.lexeme if t.type != "EOF" else "end of file"
        raise CompileError("syntax", f"expected '{lexeme}' but found '{val}'", t.line, t.col)

    def parse_program(self):
        t = self.peek()
        func = self.parse_function()
        t_eof = self.peek()
        if t_eof.type != "EOF":
            raise CompileError("syntax", f"expected 'end of file' but found '{t_eof.lexeme}'", t_eof.line, t_eof.col)
        return Program(t.line, t.col, func)

    def parse_function(self):
        t = self.peek()
        self.expect("int")
        t_name = self.peek()
        if t_name.type != "IDENTIFIER":
            val = t_name.lexeme if t_name.type != "EOF" else "end of file"
            raise CompileError("syntax", f"expected identifier but found '{val}'", t_name.line, t_name.col)
        name = t_name.lexeme
        self.advance()
        self.expect("(")
        self.expect(")")
        body = self.parse_block()
        return Function(t.line, t.col, name, body)

    def parse_block(self):
        t = self.peek()
        self.expect("{")
        stmts = []
        while self.peek().lexeme != "}":
            if self.peek().type == "EOF":
                raise CompileError("syntax", f"expected '}}' but found 'end of file'", self.peek().line, self.peek().col)
            stmts.append(self.parse_statement())
        self.expect("}")
        return Block(t.line, t.col, stmts)

    def parse_statement(self):
        t = self.peek()
        lex = t.lexeme
        if lex == "int":
            return self.parse_declaration()
        elif lex == "if":
            return self.parse_if()
        elif lex == "while":
            return self.parse_while()
        elif lex == "for":
            return self.parse_for()
        elif lex == "print":
            return self.parse_print()
        elif lex == "return":
            return self.parse_return()
        elif lex == "{":
            return self.parse_block()
        elif t.type == "IDENTIFIER":
            return self.parse_assignment_stmt()
        elif lex == "else":
            raise CompileError("syntax", f"expected expression but found 'else'", t.line, t.col)
        else:
            raise CompileError("syntax", f"expected expression but found '{lex if t.type != 'EOF' else 'end of file'}'", t.line, t.col)

    def parse_declaration(self):
        t = self.expect("int")
        t_ident = self.peek()
        if t_ident.type != "IDENTIFIER":
            val = t_ident.lexeme if t_ident.type != "EOF" else "end of file"
            raise CompileError("syntax", f"expected identifier but found '{val}'", t_ident.line, t_ident.col)
        name = t_ident.lexeme
        self.advance()
        init = None
        if self.peek().lexeme == "=":
            self.advance()
            init = self.parse_expr()
        self.expect(";")
        return VarDecl(t_ident.line, t_ident.col, name, init)

    def parse_assignment_stmt(self):
        t_ident = self.peek()
        name = t_ident.lexeme
        self.advance()
        
        t_eq = self.peek()
        if t_eq.lexeme != "=":
            val = t_eq.lexeme if t_eq.type != "EOF" else "end of file"
            raise CompileError("syntax", f"expected '=' but found '{val}'", t_eq.line, t_eq.col)
        self.advance()
        
        val_expr = self.parse_expr()
        self.expect(";")
        return Assign(t_ident.line, t_ident.col, name, val_expr)

    def parse_assignment_no_semi(self):
        t_ident = self.peek()
        if t_ident.type != "IDENTIFIER":
            val = t_ident.lexeme if t_ident.type != "EOF" else "end of file"
            raise CompileError("syntax", f"expected identifier but found '{val}'", t_ident.line, t_ident.col)
        name = t_ident.lexeme
        self.advance()
        
        t_eq = self.peek()
        if t_eq.lexeme != "=":
            val = t_eq.lexeme if t_eq.type != "EOF" else "end of file"
            raise CompileError("syntax", f"expected '=' but found '{val}'", t_eq.line, t_eq.col)
        self.advance()
        
        val_expr = self.parse_expr()
        return Assign(t_ident.line, t_ident.col, name, val_expr)

    def parse_if(self):
        t = self.expect("if")
        self.expect("(")
        cond = self.parse_expr()
        self.expect(")")
        then_stmt = self.parse_statement()
        else_stmt = None
        if self.peek().lexeme == "else":
            self.advance()
            else_stmt = self.parse_statement()
        return If(t.line, t.col, cond, then_stmt, else_stmt)

    def parse_while(self):
        t = self.expect("while")
        self.expect("(")
        cond = self.parse_expr()
        self.expect(")")
        body = self.parse_statement()
        return While(t.line, t.col, cond, body)

    def parse_for(self):
        t = self.expect("for")
        self.expect("(")
        
        init = None
        if self.peek().lexeme == "int":
            init = self.parse_declaration()
        elif self.peek().lexeme == ";":
            self.advance()
        else:
            init = self.parse_assignment_no_semi()
            self.expect(";")
            
        cond = None
        if self.peek().lexeme != ";":
            cond = self.parse_expr()
        self.expect(";")
        
        step = None
        if self.peek().lexeme != ")":
            step = self.parse_assignment_no_semi()
        self.expect(")")
        
        body = self.parse_statement()
        return For(t.line, t.col, init, cond, step, body)

    def parse_print(self):
        t = self.expect("print")
        self.expect("(")
        expr = self.parse_expr()
        self.expect(")")
        self.expect(";")
        return Print(t.line, t.col, expr)

    def parse_return(self):
        t = self.expect("return")
        expr = self.parse_expr()
        self.expect(";")
        return Return(t.line, t.col, expr)

    def parse_expr(self):
        return self.parse_logic_or()

    def parse_logic_or(self):
        node = self.parse_logic_and()
        while self.peek().lexeme == "||":
            t_op = self.advance()
            right = self.parse_logic_and()
            node = BinaryOp(node.line, node.col, t_op.lexeme, node, right)
        return node

    def parse_logic_and(self):
        node = self.parse_equality()
        while self.peek().lexeme == "&&":
            t_op = self.advance()
            right = self.parse_equality()
            node = BinaryOp(node.line, node.col, t_op.lexeme, node, right)
        return node

    def parse_equality(self):
        node = self.parse_relational()
        while self.peek().lexeme in ("==", "!="):
            t_op = self.advance()
            right = self.parse_relational()
            node = BinaryOp(node.line, node.col, t_op.lexeme, node, right)
        return node

    def parse_relational(self):
        node = self.parse_additive()
        while self.peek().lexeme in ("<", "<=", ">", ">="):
            t_op = self.advance()
            right = self.parse_additive()
            node = BinaryOp(node.line, node.col, t_op.lexeme, node, right)
        return node

    def parse_additive(self):
        node = self.parse_term()
        while self.peek().lexeme in ("+", "-"):
            t_op = self.advance()
            right = self.parse_term()
            node = BinaryOp(node.line, node.col, t_op.lexeme, node, right)
        return node

    def parse_term(self):
        node = self.parse_unary()
        while self.peek().lexeme in ("*", "/", "%"):
            t_op = self.advance()
            right = self.parse_unary()
            node = BinaryOp(node.line, node.col, t_op.lexeme, node, right)
        return node

    def parse_unary(self):
        if self.peek().lexeme in ("-", "!"):
            t_op = self.advance()
            operand = self.parse_unary()
            return UnaryOp(t_op.line, t_op.col, t_op.lexeme, operand)
        return self.parse_primary()

    def parse_primary(self):
        t = self.peek()
        if t.type == "NUMBER":
            self.advance()
            return Number(t.line, t.col, int(t.lexeme))
        elif t.type == "IDENTIFIER":
            self.advance()
            return Var(t.line, t.col, t.lexeme)
        elif t.lexeme == "(":
            self.advance()
            node = self.parse_expr()
            self.expect(")")
            return node
        else:
            val = t.lexeme if t.type != "EOF" else "end of file"
            raise CompileError("syntax", f"expected expression but found '{val}'", t.line, t.col)

def parse(tokens):
    parser = Parser(tokens)
    return parser.parse_program()
