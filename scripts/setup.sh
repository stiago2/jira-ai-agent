#!/bin/bash

# Setup script for Jira AI Agent

echo "🚀 Setting up Jira AI Agent..."

# Check Python version
python_version=$(python3.11 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✓ Python 3.11 found: $python_version"
else
    echo "✗ Python 3.11 not found. Please install Python 3.11+"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file if not exists
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your Jira credentials"
else
    echo "✓ .env file already exists"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Jira credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Run: uvicorn app.main:app --reload"
