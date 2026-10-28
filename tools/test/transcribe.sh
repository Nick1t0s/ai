#!/bin/bash
# Whisper рядом с ComfyUI: сначала выгрузить модели ComfyUI, иначе OOM; без LD_LIBRARY_PATH — «libcublas.so.12 not found».
#   transcribe.sh [--lang ru] [--words] file …
set -euo pipefail
curl --noproxy "*" -s -X POST http://127.0.0.1:8188/free -H "Content-Type: application/json" \
    -d '{"unload_models":true,"free_memory":true}' >/dev/null 2>&1 || true
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
SP="$(echo "$VENV_DIR"/lib/python*/site-packages/nvidia)"
LD_LIBRARY_PATH="${SP}/cublas/lib:${SP}/cudnn/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
    "$VENV_DIR/bin/python" -I "$SCRIPT_DIR/transcribe.py" "$@"
