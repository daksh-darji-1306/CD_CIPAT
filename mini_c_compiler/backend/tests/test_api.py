from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_examples():
    response = client.get("/api/examples")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    assert data[0]["id"] == "ex1"

def test_compile_ex1():
    source = """int main() {
    int x = 2 + 3 * 4;
    int y = x * 1;
    print(y);
    return 0;
}"""
    response = client.post("/api/compile", json={"source": source, "optimize": True, "run": True})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["optimized_tac"] == ["print 14", "return 0"]
    assert data["output"] == ["14"]
    
def test_compile_error():
    source = "int main() { int x = 5 @ 3; return 0; }"
    response = client.post("/api/compile", json={"source": source})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["phases"]["lexical"] == "error"
    assert data["phases"]["syntax"] == "skipped"

def test_compile_too_long():
    source = " " * 10001
    response = client.post("/api/compile", json={"source": source})
    assert response.status_code == 400
    assert response.json() == {"detail": "source too long"}
