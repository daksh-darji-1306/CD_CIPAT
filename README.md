<div align="center">
  <h1>🚀 Compiler Design (3170701) CIPAT</h1>
  <p><strong>A collection of compiler design implementations and visualizations.</strong></p>
  <p>Built for the Compiler Design course at <b>C. K. Pithawala College of Engineering and Technology</b>.</p>
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite" />
  </p>
</div>

---

## 📁 Repository Structure

This repository contains two major activities for the Continuous Internal Practical Assessment Test (CIPAT).

### 1. [Mini C Compiler (`/mini_c_compiler`)](./mini_c_compiler)
A full-stack, handwritten compiler pipeline demonstrating compilation phases from raw text to execution via an intermediate representation (Three-Address Code). 

**Features:**
- **Lexical Analysis:** Custom tokenizer mapping keywords, identifiers, operators, and delimiters.
- **Syntax Analysis:** Recursive descent parsing that constructs a structured Abstract Syntax Tree (AST).
- **Semantic Analysis:** Symbol table generation, type checking, and scope validation.
- **Code Generation:** Converts the AST into unoptimized Three-Address Code (TAC).
- **Optimizer:** A 5-pass optimizer executing constant folding, algebraic simplification, dead code elimination, copy propagation, and jump optimization.
- **VM Execution:** A custom virtual machine to execute the generated instructions.
- **Stunning Frontend UI:** A beautifully crafted, responsive React interface. It features:
  - An interactive code editor with live error highlighting.
  - A dark-mode, Vercel-inspired interactive **AST Tree Viewer** with glowing nodes, SVG animated links, and vertical/horizontal layout toggles.
  - Detailed tabs for Token tables, Symbol tables, TAC comparisons, and VM Output.

### 2. [LL(1) Parser (`/ll1_cipat`)](./ll1_cipat)
A complete LL(1) predictive top-down parser implemented in Python. 

**Features:**
- Computes **FIRST** and **FOLLOW** sets from a defined grammar for arithmetic expressions.
- Constructs the predictive parsing table (`M[A, a]`).
- Includes a stack-based driver script to step-by-step trace valid and invalid input strings and display the parsing steps in a neat terminal table.

---

## 🚀 Getting Started

### Running the Mini C Compiler

The Mini C Compiler requires both the FastAPI backend and the React frontend to be running simultaneously.

#### **Backend (Python)**
1. Navigate to the backend directory:
   ```bash
   cd mini_c_compiler/backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\Activate.ps1
   # Mac/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies and start the server:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

#### **Frontend (React/Vite)**
1. Open a **new** terminal and navigate to the frontend directory:
   ```bash
   cd mini_c_compiler/frontend
   ```
2. Install dependencies and start the dev server:
   ```bash
   npm install
   npm run dev
   ```
3. Open your browser to `http://localhost:5173`. Load an example, hit **Run**, and explore the beautiful AST visualizer!

---

### Running the LL(1) Parser

The LL(1) parser is a standalone Python script designed for the terminal.

1. Navigate to the `ll1_cipat` directory:
   ```bash
   cd ll1_cipat
   ```
2. To print the computed FIRST/FOLLOW sets and the Parsing Table:
   ```bash
   python ll1.py tables
   ```
3. To parse a custom string step-by-step:
   ```bash
   python ll1.py "(id+id)*id"
   ```

---

## 🎓 Academic Details
- **Course:** Compiler Design (3170701)
- **Institution:** C. K. Pithawala College of Engineering and Technology
