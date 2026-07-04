const API_BASE = import.meta.env.VITE_API_BASE ;

async function handle(res) {
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail || JSON.stringify(body);
    } catch {
      // response wasn't JSON, keep statusText
    }
    throw new Error(detail);
  }
  return res.json();
}

export async function askChat(question) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return handle(res);
}

export async function analyzeRisk(clause) {
  const res = await fetch(`${API_BASE}/risk/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ clause }),
  });
  return handle(res);
}

export async function extractClauses(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/clause/extract`, {
    method: "POST",
    body: formData,
  });
  return handle(res);
}

export async function askAgent(question) {
  const res = await fetch(`${API_BASE}/agent/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return handle(res);
}
