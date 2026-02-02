# Quick Reference Guide - Trading Bot

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your credentials
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
```

### 3. Test Connection
```bash
python cli.py test-connection
```

### 4. Place Your First Order
```bash
# Market order
python cli.py place-order BTCUSDT BUY MARKET 0.001

# Limit order  
python cli.py place-order BTCUSDT SELL LIMIT 0.001 --price 50000
```

---

## 📝 Command Cheat Sheet

```bash
# Place market buy order
python cli.py place-order BTCUSDT BUY MARKET 0.001

# Place market sell order
python cli.py place-order ETHUSDT SELL MARKET 0.01

# Place limit buy order
python cli.py place-order BTCUSDT BUY LIMIT 0.001 --price 45000

# Place limit sell order
python cli.py place-order BTCUSDT SELL LIMIT 0.001 -p 55000

# Check account balance
python cli.py check-balance

# Test API connection
python cli.py test-connection

# Show version
python cli.py version

# Get help
python cli.py --help
python cli.py place-order --help
```

---

## 📂 Project Structure

```
trading_bot/
├── bot/                    # Core package
│   ├── client.py          # API client
│   ├── orders.py          # Order logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── cli.py                 # CLI interface
├── requirements.txt       # Dependencies
└── logs/                  # Log files
```

---

## ⚙️ Common Parameters

**Symbol**: Trading pair (e.g., BTCUSDT, ETHUSDT, BNBUSDT)
**Side**: BUY or SELL
**Order Type**: MARKET or LIMIT
**Quantity**: Amount to trade (must be positive)
**Price**: Price level (required for LIMIT orders only)

---

## 🔍 Where to Find Things

- **Logs**: `logs/trading_bot_YYYYMMDD_HHMMSS.log`
- **Config**: `.env` file in project root
- **Examples**: `test_orders.py` for demonstration
- **Docs**: `README.md` for full documentation

---

## ❗ Troubleshooting

**Problem**: "Missing API credentials"
**Solution**: Create `.env` file and add credentials

**Problem**: "Connection error"
**Solution**: Check internet connection and testnet status

**Problem**: "Validation error"
**Solution**: Check parameters (price required for LIMIT)

**Problem**: Order not filling
**Solution**: Check price is realistic for LIMIT orders

---

## 🎓 Learning Resources

- Binance Testnet: https://testnet.binancefuture.com
- API Docs: https://binance-docs.github.io/apidocs/futures/en/
- Project README: See README.md for detailed docs

---

## ⚠️ Important Notes

- ✅ This is for TESTNET only
- ✅ Use test funds, not real money
- ✅ Check minimum order sizes
- ✅ Keep API keys secure
- ✅ Review logs after each order

---

## 📧 Support

For issues or questions about this implementation:
- Check logs in `logs/` directory
- Review README.md
- See code comments in source files

For Binance API issues:
- Visit https://testnet.binancefuture.com
- Check API documentation

---

**Built with** ❤️ **for Anything.ai application**
