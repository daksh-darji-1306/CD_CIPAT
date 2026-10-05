PROGRAMS = [
    {
        "id": "ex1",
        "name": "Constant folding (P1)",
        "source": """int main() {
    int x = 2 + 3 * 4;
    int y = x * 1;
    print(y);
    return 0;
}"""
    },
    {
        "id": "ex2",
        "name": "While loop sum (P2)",
        "source": """int main() {
    int i = 0;
    int sum = 0;
    while (i < 3) {
        sum = sum + i;
        i = i + 1;
    }
    print(sum);
    return 0;
}"""
    },
    {
        "id": "ex3",
        "name": "Factorial",
        "source": """int main() {
    int n = 5;
    int f = 1;
    int i = 1;
    while (i <= n) {
        f = f * i;
        i = i + 1;
    }
    print(f);
    return 0;
}"""
    },
    {
        "id": "ex4",
        "name": "If / else (EX4)",
        "source": """int main() {
    int a = 10;
    int b = 20;
    if (a > b) { print(a); } else { print(b); }
    return 0;
}"""
    },
    {
        "id": "ex5",
        "name": "For loop",
        "source": """int main() {
    int s = 0;
    for (int i = 1; i <= 5; i = i + 1) {
        s = s + i;
    }
    print(s);
    return 0;
}"""
    },
    {
        "id": "ex6",
        "name": "Operator precedence",
        "source": """int main() {
    print(2 + 3 * 4 - 6 / 2 % 4);
    return 0;
}"""
    },
    {
        "id": "ex7",
        "name": "Logical and unary",
        "source": """int main() {
    print(-4 + 10);
    print((5 > 3) && !(2 == 3));
    print(7 % 3 == 1 || 0);
    return 0;
}"""
    },
    {
        "id": "ex8",
        "name": "Scope shadowing",
        "source": """int main() {
    int x = 1;
    {
        int x = 2;
        print(x);
    }
    print(x);
    return 0;
}"""
    },
    {
        "id": "ex9",
        "name": "Nested loops",
        "source": """int main() {
    int i = 1;
    while (i <= 3) {
        int j = 1;
        int row = 0;
        while (j <= 3) {
            row = row + i * j;
            j = j + 1;
        }
        print(row);
        i = i + 1;
    }
    return 0;
}"""
    },
    {
        "id": "ex10",
        "name": "Dead branch (EX10)",
        "source": """int main() {
    int debug = 0;
    if (debug) {
        print(999);
    }
    print(42);
    return 0;
}"""
    },
    {
        "id": "err1",
        "name": "[ERROR] Lexical Error",
        "source": """int main() {
    int x = 5 @ 3;
    return 0;
}"""
    },
    {
        "id": "err2",
        "name": "[ERROR] Syntax Error",
        "source": """int main() {
    int x = 5
    print(x);
    return 0;
}"""
    },
    {
        "id": "err3",
        "name": "[ERROR] Semantic Error",
        "source": """int main() {
    int x = 1;
    print(y);
    return 0;
}"""
    }
]

EXPECTED_OUTPUTS = {
    "ex1": ["14"],
    "ex2": ["3"],
    "ex3": ["120"],
    "ex4": ["20"],
    "ex5": ["15"],
    "ex6": ["11"],
    "ex7": ["6", "1", "1"],
    "ex8": ["2", "1"],
    "ex9": ["6", "12", "18"],
    "ex10": ["42"]
}
