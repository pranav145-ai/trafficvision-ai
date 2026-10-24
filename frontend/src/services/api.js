const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:5000";

export async function detectWithBackend(file) {
  const form = new FormData();
  form.append("image", file);
  const response = await fetch(`${API_BASE}/api/detect`, { method: "POST", body: form });
  if (!response.ok) throw new Error("Detection API request failed.");
  return response.json();
}
