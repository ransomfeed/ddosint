#!/usr/bin/env bash
set -euo pipefail

echo "Building ddosint onefile binary with PyInstaller..."

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "PyInstaller not found. Installing..."
  python3 -m pip install --upgrade pip
  python3 -m pip install pyinstaller
fi

# Install package in editable mode so PyInstaller can find modules
python3 -m pip install -e .

pyinstaller --onefile --name ddosint \
  --hidden-import ddosint \
  --hidden-import ddosint.cli \
  --hidden-import ddosint.api_client \
  --hidden-import ddosint.export \
  --collect-all ddosint \
  ddosint/cli.py

echo "Binary available in ./dist" 

