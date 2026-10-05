from .ast_nodes import (
    Program, Function, Block, VarDecl, Assign, If, While, For, Print, Return,
    BinaryOp, UnaryOp, Number, Var
)
from .tac import Instr

class CodeGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 1
        self.label_counter = 1

    def new_temp(self):
        t = f"t{self.temp_counter}"
        self.temp_counter += 1
        return t

    def new_label(self):
        l = f"L{self.label_counter}"
        self.label_counter += 1
        return l

    def emit(self, instr):
        self.instructions.append(instr)

    def generate(self, ast):
        self.visit(ast)
        return self.instructions

    def visit(self, node):
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method in CodeGenerator")

    def visit_Program(self, node):
        self.visit(node.function)

    def visit_Function(self, node):
        self.visit(node.body)
        
        # Add implicit return 0 if the last statement isn't a return
        if not self.instructions or self.instructions[-1].op != "return":
            self.emit(Instr("return", a=0))

    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node):
        if node.init:
            val = self.gen_expr(node.init)
            self.emit(Instr("copy", dest=node.unique_name, a=val))
        else:
            self.emit(Instr("copy", dest=node.unique_name, a=0))

    def visit_Assign(self, node):
        val = self.gen_expr(node.value)
        self.emit(Instr("copy", dest=node.unique_name, a=val))

    def visit_If(self, node):
        if node.else_:
            l_else = self.new_label()
            l_end = self.new_label()
            cond = self.gen_expr(node.cond)
            self.emit(Instr("ifFalse", a=cond, label=l_else))
            self.visit(node.then)
            self.emit(Instr("goto", label=l_end))
            self.emit(Instr("label", label=l_else))
            self.visit(node.else_)
            self.emit(Instr("label", label=l_end))
        else:
            l_end = self.new_label()
            cond = self.gen_expr(node.cond)
            self.emit(Instr("ifFalse", a=cond, label=l_end))
            self.visit(node.then)
            self.emit(Instr("label", label=l_end))

    def visit_While(self, node):
        l_start = self.new_label()
        l_end = self.new_label()
        self.emit(Instr("label", label=l_start))
        cond = self.gen_expr(node.cond)
        self.emit(Instr("ifFalse", a=cond, label=l_end))
        self.visit(node.body)
        self.emit(Instr("goto", label=l_start))
        self.emit(Instr("label", label=l_end))

    def visit_For(self, node):
        if node.init:
            self.visit(node.init)
        l_start = self.new_label()
        l_end = self.new_label()
        self.emit(Instr("label", label=l_start))
        if node.cond:
            cond = self.gen_expr(node.cond)
            self.emit(Instr("ifFalse", a=cond, label=l_end))
        self.visit(node.body)
        if node.step:
            self.visit(node.step)
        self.emit(Instr("goto", label=l_start))
        self.emit(Instr("label", label=l_end))

    def visit_Print(self, node):
        val = self.gen_expr(node.expr)
        self.emit(Instr("print", a=val))

    def visit_Return(self, node):
        val = self.gen_expr(node.expr)
        self.emit(Instr("return", a=val))

    def gen_expr(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, Var):
            return node.unique_name
        elif isinstance(node, BinaryOp):
            left = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            t = self.new_temp()
            self.emit(Instr(node.op, dest=t, a=left, b=right))
            return t
        elif isinstance(node, UnaryOp):
            operand = self.gen_expr(node.operand)
            t = self.new_temp()
            self.emit(Instr(node.op, dest=t, a=operand))
            return t
        else:
            raise Exception(f"Unexpected expr node: {node.__class__.__name__}")

def generate_code(ast):
    generator = CodeGenerator()
    return generator.generate(ast)
