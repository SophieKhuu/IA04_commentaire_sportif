#!/bin/bash
# Installation script for Volleyball Commentary Analyzer on Linux/Mac

echo "============================================================"
echo "  Volleyball Commentary Analyzer - Installation Script"
echo "============================================================"
echo ""

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

echo ""
echo "Creating .env file from example..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env and add your GROQ_API_KEY"
else
    echo ".env already exists"
fi

echo ""
echo "============================================================"
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your GROQ_API_KEY"
echo "  2. Run: streamlit run main.py"
echo "============================================================"
