#!/usr/bin/env bash
set -euo pipefail

echo "Building ddosint onefile binary with PyInstaller..."

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "PyInstaller not found. Installing..."
  python3 -m pip install --upgrade pip
  python3 -m pip install pyinstaller
fi

pyinstaller -F -n ddosint -m ddosint.cli

echo "Binary available in ./dist" 

