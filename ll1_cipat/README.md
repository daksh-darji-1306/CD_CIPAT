# LL(1) Parser Implementation

This project implements a complete LL(1) predictive top-down parser in Python. It includes a grammar for arithmetic expressions, FIRST and FOLLOW set computation, parsing table construction, and a stack-based driver to trace valid and invalid input strings step-by-step.

## Requirements
- Python 3.10+

## Usage

1. **Print the parsing tables (FIRST sets, FOLLOW sets, and the M[A,a] matrix):**
   ```bash
   python ll1.py tables
   ```
   **Example Output:**
   ```
   FIRST sets
     FIRST(E) = { (, id }
   ...
   ```

2. **Parse the default strings (one valid, one invalid):**
   ```bash
   python ll1.py
   ```

3. **Parse a custom string:**
   ```bash
   python ll1.py "(id+id)*id"
   ```
   **Example Output:**
   ```
   Parsing: (id+id)*id
   #   STACK                   INPUT                 ACTION
   ----------------------------------------------------------------------
   1   E $                     ( id + id ) * id $    E → T E'
   ...
   24  $                       $                     ACCEPT
   ```
