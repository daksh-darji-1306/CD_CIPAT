class CompileError(Exception):
    def __init__(self, phase, message, line, col):
        self.phase = phase
        self.message = message
        self.line = line
        self.col = col
        self.formatted = f"{phase.capitalize()} error at line {line}, column {col}: {message}"
        super().__init__(self.formatted)

class RuntimeErr(Exception):
    def __init__(self, message):
        self.phase = "runtime"
        self.message = message
        self.line = None
        self.col = None
        self.formatted = f"Runtime error: {message}"
        super().__init__(self.formatted)
