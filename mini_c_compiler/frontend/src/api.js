export async function getExamples() {
  try {
    const res = await fetch('/api/examples');
    if (!res.ok) throw new Error('Failed to fetch examples');
    return await res.json();
  } catch (err) {
    throw new Error("Backend not reachable. Start it with: uvicorn app.main:app --port 8000");
  }
}

export async function compile(source, optimize) {
  try {
    const res = await fetch('/api/compile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source, optimize, run: true })
    });
    
    if (res.status === 400) {
      const data = await res.json();
      throw new Error(data.detail || "Bad request");
    }
    
    if (!res.ok) throw new Error('Failed to compile');
    return await res.json();
  } catch (err) {
    if (err.message.includes("Backend not reachable") || err.message.includes("Failed to fetch")) {
      throw new Error("Backend not reachable. Start it with: uvicorn app.main:app --port 8000");
    }
    throw err;
  }
}
