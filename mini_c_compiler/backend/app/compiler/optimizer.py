from .tac import Instr, format_instr
from .arith import eval_binop, eval_unop

def pass_constant_folding(instructions):
    consts = {}
    new_instructions = []
    
    for instr in instructions:
        # Copy instruction so we don't mutate the original
        new_instr = Instr(instr.op, instr.dest, instr.a, instr.b, instr.label)
        
        # Propagate constants
        if isinstance(new_instr.a, str) and new_instr.a in consts:
            new_instr.a = consts[new_instr.a]
        if isinstance(new_instr.b, str) and new_instr.b in consts:
            new_instr.b = consts[new_instr.b]
            
        # Fold
        folded = False
        if new_instr.op in ("+", "-", "*", "/", "%", "<", "<=", ">", ">=", "==", "!=", "&&", "||"):
            if isinstance(new_instr.a, int) and isinstance(new_instr.b, int):
                if new_instr.op in ("/", "%") and new_instr.b == 0:
                    pass # Don't fold division by zero
                else:
                    val = eval_binop(new_instr.op, new_instr.a, new_instr.b)
                    new_instr = Instr("copy", dest=new_instr.dest, a=val)
                    folded = True
        elif new_instr.op in ("-", "!") and new_instr.b is None:
            if isinstance(new_instr.a, int):
                val = eval_unop(new_instr.op, new_instr.a)
                new_instr = Instr("copy", dest=new_instr.dest, a=val)
                folded = True
                
        # Update consts
        if new_instr.op == "copy" and isinstance(new_instr.a, int):
            consts[new_instr.dest] = new_instr.a
        elif new_instr.dest:
            consts.pop(new_instr.dest, None)
            
        new_instructions.append(new_instr)
        
        # Reset consts on control flow (after processing the instruction)
        if new_instr.op in ("label", "goto", "ifFalse", "return"):
            consts.clear()
        
    return new_instructions

def pass_algebraic_simplification(instructions):
    new_instructions = []
    for instr in instructions:
        new_instr = Instr(instr.op, instr.dest, instr.a, instr.b, instr.label)
        
        if new_instr.op == "+":
            if new_instr.b == 0:
                new_instr = Instr("copy", dest=new_instr.dest, a=new_instr.a)
            elif new_instr.a == 0:
                new_instr = Instr("copy", dest=new_instr.dest, a=new_instr.b)
        elif new_instr.op == "-":
            if new_instr.b == 0:
                new_instr = Instr("copy", dest=new_instr.dest, a=new_instr.a)
        elif new_instr.op == "*":
            if new_instr.b == 1:
                new_instr = Instr("copy", dest=new_instr.dest, a=new_instr.a)
            elif new_instr.a == 1:
                new_instr = Instr("copy", dest=new_instr.dest, a=new_instr.b)
            elif new_instr.b == 0 or new_instr.a == 0:
                new_instr = Instr("copy", dest=new_instr.dest, a=0)
        elif new_instr.op == "/":
            if new_instr.b == 1:
                new_instr = Instr("copy", dest=new_instr.dest, a=new_instr.a)
                
        new_instructions.append(new_instr)
    return new_instructions

def pass_branch_simplification(instructions):
    # a: ifFalse literal goto L
    step1 = []
    for instr in instructions:
        if instr.op == "ifFalse" and isinstance(instr.a, int):
            if instr.a != 0:
                continue # remove
            else:
                step1.append(Instr("goto", label=instr.label))
        else:
            step1.append(instr)
            
    # b: unreachable code after goto/return
    step2 = []
    skip = False
    for instr in step1:
        if instr.op == "label":
            skip = False
        if not skip:
            step2.append(instr)
        if instr.op in ("goto", "return"):
            skip = True
            
    # c: goto L immediately followed by L:
    step3 = []
    for i, instr in enumerate(step2):
        if instr.op == "goto":
            if i + 1 < len(step2) and step2[i+1].op == "label" and step2[i+1].label == instr.label:
                continue # remove
        step3.append(instr)
        
    # d: unused labels
    used_labels = set()
    for instr in step3:
        if instr.op in ("goto", "ifFalse"):
            used_labels.add(instr.label)
            
    step4 = []
    for instr in step3:
        if instr.op == "label" and instr.label not in used_labels:
            continue
        step4.append(instr)
        
    return step4

def pass_temp_forwarding(instructions):
    # We need to count occurrences of tN as an operand (read) in all instructions
    def get_reads(instr):
        reads = []
        if isinstance(instr.a, str) and not (instr.op == "label" or instr.op == "goto"):
            reads.append(instr.a)
        if isinstance(instr.b, str):
            reads.append(instr.b)
        return reads

    read_counts = {}
    for instr in instructions:
        for r in get_reads(instr):
            if r.startswith('t'):
                read_counts[r] = read_counts.get(r, 0) + 1

    new_instructions = []
    skip_next = False
    for i in range(len(instructions)):
        if skip_next:
            skip_next = False
            continue
            
        instr = instructions[i]
        
        # Check for pattern: tN = <rhs> followed by v = tN
        if instr.dest and instr.dest.startswith('t') and read_counts.get(instr.dest, 0) == 1:
            if i + 1 < len(instructions):
                next_instr = instructions[i+1]
                if next_instr.op == "copy" and next_instr.a == instr.dest:
                    # Forwarding: replace both with v = <rhs>
                    fwd = Instr(instr.op, dest=next_instr.dest, a=instr.a, b=instr.b, label=instr.label)
                    new_instructions.append(fwd)
                    skip_next = True
                    continue
                    
        new_instructions.append(instr)
        
    return new_instructions

def pass_dead_code_elimination(instructions):
    while True:
        read_set = set()
        for instr in instructions:
            if isinstance(instr.a, str) and instr.op not in ("label", "goto"):
                read_set.add(instr.a)
            if isinstance(instr.b, str):
                read_set.add(instr.b)
                
        new_instructions = []
        changed = False
        
        for instr in instructions:
            if instr.dest and instr.dest not in read_set:
                # Is it / or % where divisor is NOT a nonzero literal?
                if instr.op in ("/", "%"):
                    is_safe = isinstance(instr.b, int) and instr.b != 0
                    if not is_safe:
                        new_instructions.append(instr)
                        continue
                changed = True
                continue
            new_instructions.append(instr)
            
        if not changed:
            return new_instructions
        instructions = new_instructions

def optimize(instructions):
    passes = [
        ("Constant Folding & Propagation", pass_constant_folding),
        ("Algebraic Simplification", pass_algebraic_simplification),
        ("Branch Simplification", pass_branch_simplification),
        ("Temp Forwarding", pass_temp_forwarding),
        ("Dead Code Elimination", pass_dead_code_elimination)
    ]
    
    current = instructions
    log = []
    
    for iteration in range(1, 11):
        iteration_changed = False
        for pass_name, pass_fn in passes:
            new_instrs = pass_fn(current)
            
            # Compare formatting to check for changes
            old_formatted = [format_instr(i) for i in current]
            new_formatted = [format_instr(i) for i in new_instrs]
            
            if old_formatted != new_formatted:
                current = new_instrs
                iteration_changed = True
                log.append({
                    "iteration": iteration,
                    "pass": pass_name,
                    "tac": new_formatted
                })
                
        if not iteration_changed:
            break
            
    return current, log
