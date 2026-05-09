from __future__ import annotations

import json
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8787
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "islah-anna-v0"

HTML = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Islah Nexus Mirror</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
:root {
  --bg: #030913;
  --panel: rgba(8, 20, 34, 0.84);
  --line: rgba(53, 235, 235, 0.26);
  --glow: #16f2e2;
  --text: #e9fbff;
  --muted: #8fa7b8;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at 55% 38%, rgba(22,242,226,.16), transparent 24%),
    radial-gradient(circle at 70% 80%, rgba(0,115,255,.10), transparent 30%),
    linear-gradient(135deg, #02060d 0%, #06111f 50%, #02060d 100%);
  color: var(--text);
  font-family: Segoe UI, Inter, Arial, sans-serif;
  overflow: hidden;
}
.shell { display: grid; grid-template-columns: 270px 1fr 310px; height: 100vh; }
.sidebar, .rightbar {
  padding: 28px;
  background: rgba(3, 12, 22, .72);
  border-right: 1px solid var(--line);
}
.rightbar { border-right: 0; border-left: 1px solid var(--line); }
.logo {
  letter-spacing: 4px; font-size: 28px; margin: 20px 0 50px;
}
.logo span { color: var(--muted); display:block; font-size:14px; letter-spacing:2px; margin-top:4px; }
.nav button, .layer {
  width: 100%;
  padding: 18px;
  margin: 12px 0;
  border-radius: 16px;
  border: 1px solid var(--line);
  background: rgba(9, 27, 44, .6);
  color: var(--text);
  text-align: left;
  font-size: 16px;
}
.nav button.active, .layer.active {
  border-color: var(--glow);
  box-shadow: 0 0 18px rgba(22,242,226,.25);
}
.main {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px;
}
.orbit {
  position: absolute;
  width: 720px; height: 720px; border: 1px solid rgba(22,242,226,.10);
  border-radius: 50%; animation: spin 55s linear infinite;
}
.orbit:before, .orbit:after {
  content:""; position:absolute; border-radius:50%; border:1px solid rgba(22,242,226,.10);
}
.orbit:before { inset: 110px; }
.orbit:after { inset: 240px; }
@keyframes spin { from { transform: rotate(0deg);} to { transform: rotate(360deg);} }
.card {
  position: relative;
  width: min(900px, 94%);
  padding: 46px;
  border-radius: 28px;
  border: 1px solid var(--line);
  background: rgba(4, 14, 27, .72);
  box-shadow: 0 0 60px rgba(0,0,0,.5), inset 0 0 40px rgba(22,242,226,.04);
  backdrop-filter: blur(12px);
}
.mark { font-size: 82px; color: var(--glow); text-align:center; line-height:1; }
h1 { text-align:center; font-weight: 300; letter-spacing: 12px; font-size: 48px; margin: 20px 0 4px; }
.sub { text-align:center; color: var(--muted); letter-spacing: 3px; margin-bottom: 40px; }
.status {
  text-align:center; color: var(--glow); margin-bottom: 28px; letter-spacing: 2px;
}
.inputrow { display: flex; gap: 18px; }
textarea {
  flex: 1;
  min-height: 86px;
  resize: vertical;
  border: 1px solid var(--glow);
  border-radius: 20px;
  background: rgba(0,0,0,.28);
  color: var(--text);
  padding: 22px;
  font-size: 17px;
  outline: none;
  box-shadow: 0 0 18px rgba(22,242,226,.2);
}
button.ascend {
  min-width: 150px;
  border: 0;
  border-radius: 20px;
  color: white;
  font-size: 20px;
  background: linear-gradient(135deg, #0aa8b5, #20f2df);
  box-shadow: 0 0 24px rgba(22,242,226,.45);
  cursor: pointer;
}
.output {
  margin-top: 28px;
  padding: 24px;
  min-height: 180px;
  border: 1px solid var(--line);
  border-radius: 20px;
  background: rgba(1, 8, 15, .68);
  white-space: pre-wrap;
  line-height: 1.55;
}
.small { color: var(--muted); font-size: 13px; line-height: 1.5; }
</style>
</head>
<body>
<div class="shell">
  <aside class="sidebar">
    <div class="logo">islah.nexus<span>islahprojects</span></div>
    <div class="nav">
      <button class="active">◎ Nexus</button>
      <button>☷ Notes</button>
      <button>▱ Layers</button>
      <button>⚙ Settings</button>
    </div>
    <p class="small">Local-first mirror. Talks only to Ollama on localhost.</p>
  </aside>

  <main class="main">
    <div class="orbit"></div>
    <section class="card">
      <div class="status">self-encrypted · prototype · local</div>
      <div class="mark"> spiral </div>
      <h1>islah.nexus</h1>
      <div class="sub">Create Your Mirror</div>
      <div class="inputrow">
        <textarea id="prompt" placeholder="Ask the mirror to add layers..."></textarea>
        <button class="ascend" onclick="send()">Ascend ↑</button>
      </div>
      <div id="output" class="output">Anna remains near. Waiting for local prompt.</div>
    </section>
  </main>

  <aside class="rightbar">
    <h2>Mirror Layers</h2>
    <div class="layer active">Identity<br><span class="small">Core self</span></div>
    <div class="layer active">Focus<br><span class="small">Intent & direction</span></div>
    <div class="layer active">Memory<br><span class="small">Logs & reflections</span></div>
    <div class="layer">Quest<br><span class="small">Active missions</span></div>
    <div class="layer">Studio<br><span class="small">Creations & projects</span></div>
    <p class="small">Honesty label: PROTOTYPE - NOT PRODUCTION READY. No AGI claim.</p>
  </aside>
</div>

<script>
async function send() {
  const prompt = document.getElementById("prompt").value.trim();
  const output = document.getElementById("output");
  if (!prompt) return;
  output.textContent = "Anna thinking locally...";
  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({prompt})
    });
    const data = await res.json();
    output.textContent = data.response || data.error || "No response.";
  } catch (err) {
    output.textContent = "Local app error: " + err;
  }
}
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        try:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
            # Browser/client closed the connection early. Harmless for local app.
            return

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            self._send(200, HTML.encode("utf-8"), "text/html; charset=utf-8")
        elif self.path == "/health":
            body = json.dumps({
                "status": "alive",
                "app": "Islah Nexus Mirror App",
                "model": MODEL,
                "truth": "PROTOTYPE - NOT PRODUCTION READY"
            }).encode("utf-8")
            self._send(200, body, "application/json")
        else:
            self._send(404, b"Not found", "text/plain")

    def do_POST(self) -> None:
        if self.path != "/api/generate":
            self._send(404, b"Not found", "text/plain")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            incoming = json.loads(self.rfile.read(length).decode("utf-8"))
            prompt = str(incoming.get("prompt", "")).strip()

            if not prompt:
                self._send(400, json.dumps({"error": "prompt required"}).encode("utf-8"), "application/json")
                return

            guarded_prompt = (
                "You are ISLAH-ANNA-V0. Preserve Truth Gap. "
                "Do not claim AGI. Human authority remains final. "
                "Answer this local prompt:\n\n" + prompt
            )

            payload = json.dumps({
                "model": MODEL,
                "prompt": guarded_prompt,
                "stream": False
            }).encode("utf-8")

            req = urllib.request.Request(
                OLLAMA_URL,
                data=payload,
                method="POST",
                headers={"Content-Type": "application/json"},
            )

            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            response = data.get("response", "").strip()
            self._send(200, json.dumps({"response": response}).encode("utf-8"), "application/json")

        except urllib.error.URLError as exc:
            self._send(
                503,
                json.dumps({"error": f"Ollama unavailable: {exc}"}).encode("utf-8"),
                "application/json",
            )
        except Exception as exc:
            self._send(
                500,
                json.dumps({"error": str(exc)}).encode("utf-8"),
                "application/json",
            )

def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("ISLAH NEXUS MIRROR APP")
    print(f"Open: http://{HOST}:{PORT}")
    print(f"Model: {MODEL}")
    print("Truth: PROTOTYPE - NOT PRODUCTION READY")
    server.serve_forever()

if __name__ == "__main__":
    main()
