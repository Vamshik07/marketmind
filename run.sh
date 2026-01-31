#!/bin/bash
# MarketAI Suite - Quick Start Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          MarketAI Suite - Quick Start Guide               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "✓ Creating virtual environment..."
    python -m venv .venv
    echo "  Virtual environment created!"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/Scripts/activate || .venv\Scripts\activate.bat
echo ""

# Install dependencies
echo "✓ Installing dependencies..."
pip install -r requirements.txt -q
echo "  Dependencies installed!"
echo ""

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠ Warning: .env file not found!"
    echo "  Please create a .env file with your Groq API key:"
    echo "  GROQ_API_KEY=your_api_key_here"
    echo ""
fi

# Start the Flask app
echo "✓ Starting MarketAI Suite..."
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║          Server is running at http://127.0.0.1:5000       ║"
echo "║          Press CTRL+C to stop the server                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

python app.py