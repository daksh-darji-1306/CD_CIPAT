class Instr:
    def __init__(self, op, dest=None, a=None, b=None, label=None):
        self.op = op
        self.dest = dest
        self.a = a
        self.b = b
        self.label = label

    def to_dict(self):
        return {
            "op": self.op,
            "dest": self.dest,
            "a": self.a,
            "b": self.b,
            "label": self.label
        }

def format_instr(instr):
    if instr.op == "label":
        return f"{instr.label}:"
    elif instr.op == "goto":
        return f"goto {instr.label}"
    elif instr.op == "ifFalse":
        return f"ifFalse {instr.a} goto {instr.label}"
    elif instr.op == "print":
        return f"print {instr.a}"
    elif instr.op == "return":
        return f"return {instr.a}"
    elif instr.op == "copy":
        return f"{instr.dest} = {instr.a}"
    elif instr.op in ("-", "!") and instr.b is None:
        return f"{instr.dest} = {instr.op}{instr.a}"
    else:
        # binary
        return f"{instr.dest} = {instr.a} {instr.op} {instr.b}"
