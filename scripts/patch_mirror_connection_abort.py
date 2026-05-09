from pathlib import Path
import re

path = Path("mirror_app/app.py")
text = path.read_text(encoding="utf-8")

new_send = '''    def _send(self, status: int, body: bytes, content_type: str) -> None:
        try:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
            # Browser/client closed the connection early. Harmless for local app.
            return
'''

pattern = r'    def _send\(self, status: int, body: bytes, content_type: str\) -> None:\n.*?        self\.wfile\.write\(body\)\n'

updated, count = re.subn(pattern, new_send, text, count=1, flags=re.DOTALL)

if count != 1:
    raise SystemExit("PATCH FAILED: could not replace _send function.")

path.write_text(updated, encoding="utf-8")
print("PATCH OK: Mirror app now ignores aborted browser connections.")
