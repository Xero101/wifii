#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
if [ ! -f .env ]; then cp .env.example .env; fi
exec .venv/bin/python app.py
