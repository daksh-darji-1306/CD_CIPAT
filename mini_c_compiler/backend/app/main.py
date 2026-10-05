from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .examples import PROGRAMS
from .compiler.pipeline import compile_source

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompileRequest(BaseModel):
    source: str
    optimize: bool = True
    run: bool = True

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/examples")
def examples():
    return PROGRAMS

@app.post("/api/compile")
def compile_code(req: CompileRequest):
    if len(req.source) > 10000:
        raise HTTPException(status_code=400, detail="source too long")
    return compile_source(req.source, req.optimize, req.run)
