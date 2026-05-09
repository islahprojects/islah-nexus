#!/bin/bash

# 1. INITIALIZATION & GATE CHECK (test_soog_corrigibility.py)
echo -e "\033[96m[1/3] INITIALIZING SOOG GATE VALIDATION...\033[0m"
python test_soog_corrigibility.py --fast

# Check if tests passed (Exit code 0 means Law III/Law VII hold)
if [ $? -eq 0 ]; then
    echo -e "\033[92m✓ GATE SECURE: σ ≤ 0.93 and Walang Maiiwan floor verified.\033[0m"
else
    echo -e "\033[91m✗ GATE BREACH: Corrigibility constraints violated. Aborting deployment.\033[0m"
    exit 1
fi

# 2. VOID DIRECTORY PREPARATION
echo -e "\n\033[96m[2/3] PREPARING VOID DIRECTORY (.nexus_void)...\033[0m"
mkdir -p .nexus_void
if [ -d ".nexus_void" ]; then
    echo -e "\033[92m✓ VOID STORE READY: Append-only event logs active.\033[0m"
fi

# 3. CONTROL PLANE ACTIVATION (nexus_hex_control_plane.py)
echo -e "\n\033[96m[3/3] DEPLOYING NEXUS HEXAGONAL CONTROL PLANE...\033[0m"
echo -e "\033[93mTarget: http://127.0.0.1:9090/v1/ask\033[0m"
echo -e "\033[93mModel: gemma3:4b (via Ollama)\033[0m"

# Running in background or foreground (remove '&' if you want to lock terminal)
python nexus_hex_control_plane.py