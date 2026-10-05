from .lexer import tokenize
from .parser import parse
from .semantic import analyze
from .codegen import generate_code
from .optimizer import optimize as optimize_code
from .vm import execute
from .tac import format_instr
from .errors import CompileError, RuntimeErr

def compile_source(source: str, optimize: bool = True, run: bool = True) -> dict:
    res = {
        "success": True,
        "tokens": [],
        "ast": None,
        "symbol_table": [],
        "tac": [],
        "optimized_tac": [],
        "optimization_log": [],
        "stats": None,
        "output": [],
        "exit_code": None,
        "error": None,
        "phases": {
            "lexical": "skipped",
            "syntax": "skipped",
            "semantic": "skipped",
            "codegen": "skipped",
            "optimizer": "skipped",
            "execution": "skipped"
        }
    }
    
    try:
        # Lexical
        tokens = tokenize(source)
        res["tokens"] = [t.to_dict() for t in tokens]
        res["phases"]["lexical"] = "ok"
        
        # Syntax
        ast = parse(tokens)
        res["ast"] = ast.to_dict()
        res["phases"]["syntax"] = "ok"
        
        # Semantic
        symtab = analyze(ast)
        res["symbol_table"] = symtab
        res["phases"]["semantic"] = "ok"
        
        # Code Gen
        tac_instrs = generate_code(ast)
        res["tac"] = [format_instr(i) for i in tac_instrs]
        res["phases"]["codegen"] = "ok"
        
        # Optimizer
        if optimize:
            opt_instrs, log = optimize_code(tac_instrs)
            res["optimized_tac"] = [format_instr(i) for i in opt_instrs]
            res["optimization_log"] = log
            res["stats"] = {
                "tac_before": len(tac_instrs),
                "tac_after": len(opt_instrs)
            }
            res["phases"]["optimizer"] = "ok"
            to_execute = opt_instrs
        else:
            to_execute = tac_instrs
            
        # Execution
        if run:
            try:
                vm_res = execute(to_execute)
                res["output"] = vm_res["output"]
                res["exit_code"] = vm_res["exit_code"]
                res["phases"]["execution"] = "ok"
            except RuntimeErr as e:
                res["success"] = False
                res["error"] = {
                    "phase": e.phase,
                    "message": e.message,
                    "line": e.line,
                    "col": e.col,
                    "formatted": e.formatted
                }
                res["phases"]["execution"] = "error"
                if hasattr(e, 'output'):
                    res["output"] = e.output
                
    except CompileError as e:
        res["success"] = False
        res["error"] = {
            "phase": e.phase,
            "message": e.message,
            "line": e.line,
            "col": e.col,
            "formatted": e.formatted
        }
        res["phases"][e.phase] = "error"
        
    return res
