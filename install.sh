#!/bin/zsh
# Set up the virtual environment and install the PejWrite Quick Action.
set -e
cd "$(dirname "$0")"

python3 -m venv .venv
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt
.venv/bin/python make_services.py

echo
echo "Done. Store your API key with:"
echo '  security add-generic-password -a "$USER" -s ai-rewrite -w'
