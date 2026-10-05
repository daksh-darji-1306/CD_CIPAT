from .errors import RuntimeErr
from .arith import eval_binop, eval_unop

def execute(instructions):
    labels = {}
    for i, instr in enumerate(instructions):
        if instr.op == "label":
            labels[instr.label] = i

    env = {}
    output = []
    
    def get_val(operand):
        if isinstance(operand, int):
            return operand
        return env.get(operand, 0)
        
    pc = 0
    step_count = 0
    
    while pc < len(instructions):
        step_count += 1
        if step_count > 500000:
            err = RuntimeErr("step limit exceeded (possible infinite loop)")
            err.output = output
            raise err
            
        instr = instructions[pc]
        
        if instr.op == "label":
            pc += 1
        elif instr.op == "goto":
            pc = labels[instr.label]
        elif instr.op == "ifFalse":
            if get_val(instr.a) == 0:
                pc = labels[instr.label]
            else:
                pc += 1
        elif instr.op == "print":
            output.append(str(get_val(instr.a)))
            pc += 1
        elif instr.op == "return":
            return {"output": output, "exit_code": get_val(instr.a)}
        elif instr.op == "copy":
            env[instr.dest] = get_val(instr.a)
            pc += 1
        elif instr.op in ("-", "!") and instr.b is None:
            val = eval_unop(instr.op, get_val(instr.a))
            env[instr.dest] = val
            pc += 1
        else:
            # binary
            try:
                val = eval_binop(instr.op, get_val(instr.a), get_val(instr.b))
                env[instr.dest] = val
                pc += 1
            except ZeroDivisionError:
                err = RuntimeErr("division by zero")
                err.output = output
                raise err
                
    return {"output": output, "exit_code": 0}
