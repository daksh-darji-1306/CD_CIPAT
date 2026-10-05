import pytest
from app.examples import PROGRAMS, EXPECTED_OUTPUTS
from app.compiler.pipeline import compile_source

ERRORS = {
    "e1": {
        "source": "int main() {\n    int x = 5 @ 3;\n    return 0;\n}",
        "expected": "Lexical error at line 2, column 15: unexpected character '@'"
    },
    "e2": {
        "source": "int main() {\n    int x = 5\n    print(x);\n    return 0;\n}",
        "expected": "Syntax error at line 3, column 5: expected ';' but found 'print'"
    },
    "e3": {
        "source": "int main() {\n    int x = 1;\n    print(y);\n    return 0;\n}",
        "expected": "Semantic error at line 3, column 11: variable 'y' is not declared"
    },
    "e4": {
        "source": "int main() {\n    int x = 1;\n    int x = 2;\n    return 0;\n}",
        "expected": "Semantic error at line 3, column 9: variable 'x' is already declared in this scope"
    },
    "e5": {
        "source": "int main() {\n    int z = 0;\n    print(10 / z);\n    return 0;\n}",
        "expected": "Runtime error: division by zero"
    },
    "e6": {
        "source": "int main() {\n    while (1) { }\n    return 0;\n}",
        "expected": "Runtime error: step limit exceeded (possible infinite loop)"
    }
}

@pytest.mark.parametrize("prog_id", EXPECTED_OUTPUTS.keys())
def test_programs_valid(prog_id):
    source = next(p["source"] for p in PROGRAMS if p["id"] == prog_id)
    expected_output = EXPECTED_OUTPUTS[prog_id]
    
    # Opt true
    res_opt = compile_source(source, optimize=True, run=True)
    assert res_opt["success"] is True
    assert res_opt["exit_code"] == 0
    assert res_opt["output"] == expected_output
    
    # Opt false
    res_noopt = compile_source(source, optimize=False, run=True)
    assert res_noopt["success"] is True
    assert res_noopt["exit_code"] == 0
    assert res_noopt["output"] == expected_output

@pytest.mark.parametrize("err_id", ERRORS.keys())
def test_programs_errors(err_id):
    err = ERRORS[err_id]
    
    # Opt true
    res_opt = compile_source(err["source"], optimize=True, run=True)
    assert res_opt["success"] is False
    assert res_opt["error"]["formatted"] == err["expected"]
    
    # Opt false
    res_noopt = compile_source(err["source"], optimize=False, run=True)
    assert res_noopt["success"] is False
    assert res_noopt["error"]["formatted"] == err["expected"]

    if err_id == "e5":
        assert res_opt["output"] == []
        assert res_noopt["output"] == []
