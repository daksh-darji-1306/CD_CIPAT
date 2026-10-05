from .errors import CompileError
from .ast_nodes import (
    Program, Function, Block, VarDecl, Assign, If, While, For, Print, Return,
    BinaryOp, UnaryOp, Number, Var
)

class SemanticAnalyzer:
    def __init__(self):
        self.scopes = []
        self.scope_counter = 1
        self.symbol_table = []
        self.name_counts = {}

    def push_scope(self, is_function_body=False):
        if is_function_body:
            scope_id = 1
        else:
            self.scope_counter += 1
            scope_id = self.scope_counter
        self.scopes.append((scope_id, {}))
        return scope_id

    def pop_scope(self):
        self.scopes.pop()

    def current_scope_id(self):
        return self.scopes[-1][0]

    def declare(self, name, line, col):
        current_scope_dict = self.scopes[-1][1]
        if name in current_scope_dict:
            raise CompileError("semantic", f"variable '{name}' is already declared in this scope", line, col)
        
        count = self.name_counts.get(name, 0)
        self.name_counts[name] = count + 1
        
        if count == 0:
            unique_name = name
        else:
            unique_name = f"{name}_{count}"
            
        current_scope_dict[name] = unique_name
        self.symbol_table.append({
            "name": name,
            "unique_name": unique_name,
            "type": "int",
            "scope": self.current_scope_id(),
            "line": line
        })
        return unique_name

    def resolve(self, name, line, col):
        for scope_id, scope_dict in reversed(self.scopes):
            if name in scope_dict:
                return scope_dict[name]
        raise CompileError("semantic", f"variable '{name}' is not declared", line, col)

    def visit(self, node):
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method")

    def visit_Program(self, node):
        self.visit(node.function)

    def visit_Function(self, node):
        if node.name != "main":
            raise CompileError("semantic", "program must define 'int main()'", node.line, node.col)
        self.push_scope(is_function_body=True)
        self.visit_Block_body(node.body)
        self.pop_scope()

    def visit_Block(self, node):
        self.push_scope()
        self.visit_Block_body(node)
        self.pop_scope()

    def visit_Block_body(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node):
        if node.init:
            self.visit(node.init)
        node.unique_name = self.declare(node.name, node.line, node.col)

    def visit_Assign(self, node):
        self.visit(node.value)
        node.unique_name = self.resolve(node.name, node.line, node.col)

    def visit_If(self, node):
        self.visit(node.cond)
        self.visit(node.then)
        if node.else_:
            self.visit(node.else_)

    def visit_While(self, node):
        self.visit(node.cond)
        self.visit(node.body)

    def visit_For(self, node):
        self.push_scope()
        if node.init:
            self.visit(node.init)
        if node.cond:
            self.visit(node.cond)
        if node.step:
            self.visit(node.step)
        self.visit(node.body)
        self.pop_scope()

    def visit_Print(self, node):
        self.visit(node.expr)

    def visit_Return(self, node):
        self.visit(node.expr)

    def visit_BinaryOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.operand)

    def visit_Number(self, node):
        pass

    def visit_Var(self, node):
        node.unique_name = self.resolve(node.name, node.line, node.col)

def analyze(ast):
    analyzer = SemanticAnalyzer()
    analyzer.visit(ast)
    return analyzer.symbol_table
