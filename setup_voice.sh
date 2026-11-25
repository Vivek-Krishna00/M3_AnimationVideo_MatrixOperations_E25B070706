#!/bin/bash
# Installs the Kokoro neural voice inside this project folder only.
set -e
cd "$(dirname "$0")"
[ -d .ttsvenv ] || python3.12 -m venv .ttsvenv
.ttsvenv/bin/pip install -q kokoro-onnx soundfile
mkdir -p .ttsmodel
URL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -f .ttsmodel/$f ] || { curl -fL -o .ttsmodel/$f.part $URL/$f && mv .ttsmodel/$f.part .ttsmodel/$f; }
done
ls -lh .ttsmodel
echo DONE
