#!/bin/bash

# Development server runner

echo "Starting Jira AI Agent in development mode..."

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
