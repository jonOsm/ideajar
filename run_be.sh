#!/bin/bash
source ./backend/.venv/bin/activate
uv run fastapi dev backend/app/main.py