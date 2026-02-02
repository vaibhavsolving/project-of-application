# Binance Futures Trading Bot 🤖

A professional, well-structured Python trading bot for Binance Futures Testnet (USDT-M) with comprehensive logging, error handling, and a clean CLI interface.

## ✨ Features

- **Order Types**: Market and Limit orders
- **Order Sides**: BUY and SELL
- **Input Validation**: Comprehensive validation using Pydantic models
- **Error Handling**: Robust exception handling for API errors, network failures, and invalid inputs
- **Structured Logging**: Detailed logging to timestamped files with console output
- **Clean Architecture**: Separation of concerns with distinct modules for client, orders, validation, and logging
- **Rich CLI Interface**: Beautiful terminal UI with tables and formatted output using Rich library
- **Type Safety**: Full type hints throughout the codebase

## 📋 Requirements

- Python 3.8 or higher
- Binance Futures Testnet account and API credentials

## 🚀 Setup Instructions

### 1. Clone or Download the Repository

```bash
git clone <your-repo-url>
cd trading_bot
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials

1. Register for a Binance Futures Testnet account: https://testnet.binancefuture.com
2. Generate API Key and Secret from your testnet account
3. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

4. Edit `.env` and add your credentials:

```env
BINANCE_API_KEY=your_actual_api_key_here
BINANCE_API_SECRET=your_actual_api_secret_here
```

### 5. Verify Installation

Test the connection to the API:

```bash
python cli.py test-connection
```

## 📖 Usage

### Basic Command Structure

```bash
python cli.py place-order <SYMBOL> <SIDE> <ORDER_TYPE> <QUANTITY> [--price PRICE]
```

### Examples

#### 1. Place a Market BUY Order

```bash
python cli.py place-order BTCUSDT BUY MARKET 0.001
```

This will:
- Buy 0.001 BTC using a market order
- Execute immediately at the current market price

#### 2. Place a Limit SELL Order

```bash
python cli.py place-order BTCUSDT SELL LIMIT 0.001 --price 50000
```

This will:
- Sell 0.001 BTC at a limit price of $50,000
- Order will only execute if the market reaches this price

#### 3. Check Account Balance

```bash
python cli.py check-balance
```

Displays your testnet account balance for all assets.

#### 4. Test API Connection

```bash
python cli.py test-connection
```

Verifies connectivity to Binance Futures Testnet API.

#### 5. Show Version

```bash
python cli.py version
```

### Additional Examples

```bash
# Market sell order
python cli.py place-order ETHUSDT SELL MARKET 0.01

# Limit buy order for Ethereum
python cli.py place-order ETHUSDT BUY LIMIT 0.01 --price 3000

# Market buy order for Solana
python cli.py place-order SOLUSDT BUY MARKET 1.0

# Limit sell order for BNB
python cli.py place-order BNBUSDT SELL LIMIT 0.5 --price 600
```

### Getting Help

```bash
# General help
python cli.py --help

# Command-specific help
python cli.py place-order --help
```

## 📁 Project Structure

```
trading_bot/
│
├── bot/                          # Core bot package
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance API client wrapper
│   ├── orders.py                # Order placement logic
│   ├── validators.py            # Input validation with Pydantic
│   └── logging_config.py        # Logging configuration
│
├── cli.py                       # CLI entry point (Typer)
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

## 🔧 Architecture

### Components

1. **BinanceClient** (`client.py`)
   - Handles all API communication
   - Manages authentication and request signing
   - Implements error handling and retry logic

2. **OrderManager** (`orders.py`)
   - Orchestrates order placement workflow
   - Formats and displays order information
   - Manages order status and cancellation

3. **Validators** (`validators.py`)
   - Validates all user inputs using Pydantic models
   - Ensures data integrity before API calls
   - Provides clear error messages

4. **Logging** (`logging_config.py`)
   - Configures structured logging
   - Creates timestamped log files
   - Separates console and file output

5. **CLI** (`cli.py`)
   - Provides user-friendly command-line interface
   - Uses Typer for argument parsing
   - Displays rich formatted output

## 📝 Logging

Logs are automatically created in the `logs/` directory with timestamps:

```
logs/
├── trading_bot_20260202_143022.log
├── trading_bot_20260202_145533.log
└── ...
```

Each log file contains:
- Timestamp for each operation
- API request details
- API response data
- Error messages with full context
- Order placement results

### Log Example

```
2026-02-02 14:30:22 - trading_bot - INFO - Initialized BinanceClient (testnet=True)
2026-02-02 14:30:22 - trading_bot - INFO - OrderManager initialized
2026-02-02 14:30:23 - trading_bot - DEBUG - GET /fapi/v1/ping - Params: {}
2026-02-02 14:30:23 - trading_bot - DEBUG - Response Status: 200
2026-02-02 14:30:23 - trading_bot - INFO - API connectivity test passed
2026-02-02 14:30:24 - trading_bot - INFO - Placing order: BUY 0.001 BTCUSDT @ MARKET
2026-02-02 14:30:24 - trading_bot - DEBUG - POST /fapi/v1/order - Params: {...}
2026-02-02 14:30:24 - trading_bot - DEBUG - Response Status: 200
2026-02-02 14:30:24 - trading_bot - INFO - Order placed successfully: Order ID 12345678
```

## 🛡️ Error Handling

The bot handles various error scenarios:

- **Validation Errors**: Invalid input parameters
- **API Errors**: Binance API error responses
- **Network Errors**: Connection timeouts and failures
- **Authentication Errors**: Invalid API credentials
- **Rate Limiting**: API rate limit exceeded

All errors are logged with full context and displayed to the user with clear messages.

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BINANCE_API_KEY` | Your Binance Futures Testnet API key | Yes |
| `BINANCE_API_SECRET` | Your Binance Futures Testnet API secret | Yes |

## 🧪 Testing

The bot can be tested on Binance Futures Testnet without risking real funds.

### Test Workflow

1. **Test Connection**
   ```bash
   python cli.py test-connection
   ```

2. **Check Balance**
   ```bash
   python cli.py check-balance
   ```

3. **Place Test Orders**
   ```bash
   # Small market order
   python cli.py place-order BTCUSDT BUY MARKET 0.001
   
   # Limit order
   python cli.py place-order BTCUSDT SELL LIMIT 0.001 --price 60000
   ```

4. **Review Logs**
   - Check the `logs/` directory for detailed execution logs

## 📊 Sample Output

### Market Order
```
╭─────────────────────────────────────────────╮
│ Binance Futures Testnet Trading Bot        │
│ Starting order placement...                 │
╰─────────────────────────────────────────────╯

Testing API connectivity...
✓ Connected successfully

📋 Order Request Summary
Field     Value
Symbol    BTCUSDT
Side      BUY
Type      MARKET
Quantity  0.001

✅ Order Placed Successfully
Field               Value
Order ID           123456789
Symbol             BTCUSDT
Status             FILLED
Side               BUY
Type               MARKET
Original Quantity  0.001
Executed Quantity  0.001
Average Price      48532.50
Update Time        2026-02-02 14:30:24

Order 123456789 filled at average price: 48532.50
```

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It contains sensitive API credentials
2. **Use testnet only** - Practice with testnet before using real funds
3. **Restrict API permissions** - Only enable necessary permissions on your API keys
4. **Keep dependencies updated** - Regularly update packages for security patches
5. **Review logs regularly** - Monitor for unusual activity

## 🐛 Troubleshooting

### Common Issues

1. **"Missing API credentials"**
   - Ensure `.env` file exists and contains valid credentials
   - Check that variable names match exactly: `BINANCE_API_KEY` and `BINANCE_API_SECRET`

2. **"Connection error"**
   - Verify internet connection
   - Check if testnet URL is accessible: https://testnet.binancefuture.com

3. **"API Error [code]"**
   - Check Binance API documentation for error code meaning
   - Verify API key permissions
   - Ensure sufficient testnet balance

4. **"Validation error"**
   - Check input parameters match requirements
   - Ensure price is provided for LIMIT orders
   - Verify quantity is positive

## 📚 Dependencies

- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management
- **typer**: CLI framework
- **rich**: Terminal formatting and tables
- **pydantic**: Data validation

## 🔄 Future Enhancements

Potential additions (not implemented):
- Stop-Loss/Take-Profit orders
- OCO (One-Cancels-Other) orders
- TWAP (Time-Weighted Average Price) execution
- Grid trading strategy
- Order history and tracking
- WebSocket for real-time data
- Backtesting capabilities

## 📄 License

This project is for educational purposes. Use at your own risk.

## 👤 Author

Application task submission for Junior Python Developer position at Anything.ai

## 📧 Contact

For questions or issues, please contact via the application email.

---

**⚠️ Disclaimer**: This bot is designed for Binance Futures Testnet only. Always practice with testnet funds before trading with real money. Cryptocurrency trading carries risk.
