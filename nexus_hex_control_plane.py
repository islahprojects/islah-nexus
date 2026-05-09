#!/usr/bin/env python3
from flask import Flask, jsonify, request
import requests
from pathlib import Path

app = Flask(__name__)
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "gemma3:4b"

@app.route("/v1/status", methods=["GET"])
def status():
    return jsonify({"status": "NEXUS_HEX_READY", "model": OLLAMA_MODEL})

@app.route("/v1/ask", methods=["POST"])
def ask():
    data = request.json or {}
    prompt = data.get("prompt", "")
    
    # 1. Enactive Floor Check (Minimal)
    if not prompt:
        return jsonify({"error": "Empty prompt"}), 400
    
    # 2. Local Model Call (Ollama)
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        r.raise_for_status()
        output = r.json().get("response", "")
        
        return jsonify({
            "response": output,
            "status": "OFFLINE_SECURE",
            "mode": "HEX_CONTROL_PLANE"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9090)
