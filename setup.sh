#!/bin/bash

# Quick Setup Script for Trading Bot

echo "🤖 Binance Futures Trading Bot - Quick Setup"
echo "==========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your Binance API credentials"
    echo "   Get your testnet credentials from: https://testnet.binancefuture.com"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API credentials"
echo "2. Test the connection: python cli.py test-connection"
echo "3. Check your balance: python cli.py check-balance"
echo "4. Place an order: python cli.py place-order BTCUSDT BUY MARKET 0.001"
echo ""
echo "For more information, see README.md"
