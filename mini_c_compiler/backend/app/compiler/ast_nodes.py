class Node:
    def __init__(self, line, col):
        self.line = line
        self.col = col

    def to_dict(self):
        d = {"name": self.__class__.__name__}
        return d

class Program(Node):
    def __init__(self, line, col, function):
        super().__init__(line, col)
        self.function = function
    def to_dict(self):
        d = super().to_dict()
        d["children"] = [self.function.to_dict()]
        return d

class Function(Node):
    def __init__(self, line, col, name, body):
        super().__init__(line, col)
        self.name = name
        self.body = body
    def to_dict(self):
        d = super().to_dict()
        d["name"] = f"Function: {self.name}"
        d["children"] = [self.body.to_dict()]
        return d

class Block(Node):
    def __init__(self, line, col, statements):
        super().__init__(line, col)
        self.statements = statements
    def to_dict(self):
        d = super().to_dict()
        d["children"] = [stmt.to_dict() for stmt in self.statements]
        return d

class VarDecl(Node):
    def __init__(self, line, col, name, init):
        super().__init__(line, col)
        self.name = name
        self.init = init
        self.unique_name = None
    def to_dict(self):
        d = super().to_dict()
        d["name"] = f"VarDecl: {self.name}"
        d["children"] = []
        if self.init:
            d["children"].append(self.init.to_dict())
        if hasattr(self, 'unique_name') and self.unique_name is not None:
            d["unique_name"] = self.unique_name
        return d

class Assign(Node):
    def __init__(self, line, col, name, value):
        super().__init__(line, col)
        self.name = name
        self.value = value
        self.unique_name = None
    def to_dict(self):
        d = super().to_dict()
        d["name"] = f"Assign: {self.name}"
        d["children"] = [self.value.to_dict()]
        if hasattr(self, 'unique_name') and self.unique_name is not None:
            d["unique_name"] = self.unique_name
        return d

class If(Node):
    def __init__(self, line, col, cond, then, else_):
        super().__init__(line, col)
        self.cond = cond
        self.then = then
        self.else_ = else_
    def to_dict(self):
        d = super().to_dict()
        d["children"] = [self.cond.to_dict(), self.then.to_dict()]
        if self.else_:
            d["children"].append(self.else_.to_dict())
        return d

class While(Node):
    def __init__(self, line, col, cond, body):
        super().__init__(line, col)
        self.cond = cond
        self.body = body
    def to_dict(self):
        d = super().to_dict()
        d["children"] = [self.cond.to_dict(), self.body.to_dict()]
        return d

class For(Node):
    def __init__(self, line, col, init, cond, step, body):
        super().__init__(line, col)
        self.init = init
        self.cond = cond
        self.step = step
        self.body = body
    def to_dict(self):
        d = super().to_dict()
        d["children"] = []
        if self.init:
            d["children"].append(self.init.to_dict())
        if self.cond:
            d["children"].append(self.cond.to_dict())
        if self.step:
            d["children"].append(self.step.to_dict())
        d["children"].append(self.body.to_dict())
        return d

class Print(Node):
    def __init__(self, line, col, expr):
        super().__init__(line, col)
        self.expr = expr
    def to_dict(self):
        d = super().to_dict()
        d["children"] = [self.expr.to_dict()]
        return d

class Return(Node):
    def __init__(self, line, col, expr):
        super().__init__(line, col)
        self.expr = expr
    def to_dict(self):
        d = super().to_dict()
        d["children"] = [self.expr.to_dict()]
        return d

class BinaryOp(Node):
    def __init__(self, line, col, op, left, right):
        super().__init__(line, col)
        self.op = op
        self.left = left
        self.right = right
    def to_dict(self):
        d = super().to_dict()
        d["name"] = f"BinaryOp: {self.op}"
        d["children"] = [self.left.to_dict(), self.right.to_dict()]
        return d

class UnaryOp(Node):
    def __init__(self, line, col, op, operand):
        super().__init__(line, col)
        self.op = op
        self.operand = operand
    def to_dict(self):
        d = super().to_dict()
        d["name"] = f"UnaryOp: {self.op}"
        d["children"] = [self.operand.to_dict()]
        return d

class Number(Node):
    def __init__(self, line, col, value):
        super().__init__(line, col)
        self.value = value
    def to_dict(self):
        d = super().to_dict()
        d["name"] = f"Number: {self.value}"
        return d

class Var(Node):
    def __init__(self, line, col, name):
        super().__init__(line, col)
        self.name = name
        self.unique_name = None
    def to_dict(self):
        d = super().to_dict()
        d["name"] = f"Var: {self.name}"
        if hasattr(self, 'unique_name') and self.unique_name is not None:
            d["unique_name"] = self.unique_name
        return d
