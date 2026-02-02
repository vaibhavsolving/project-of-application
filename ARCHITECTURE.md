# Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Trading Bot System                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│             │         │              │         │              │
│     CLI     │────────▶│    Order     │────────▶│   Binance    │
│  (cli.py)   │         │   Manager    │         │    Client    │
│             │         │ (orders.py)  │         │ (client.py)  │
└─────────────┘         └──────────────┘         └──────────────┘
      │                        │                        │
      │                        │                        │
      ▼                        ▼                        ▼
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│  Validator  │         │   Logger     │         │ Binance API  │
│(validators) │         │   System     │         │  (Testnet)   │
└─────────────┘         └──────────────┘         └──────────────┘
```

## Component Details

### 1. CLI Layer (cli.py)
**Responsibility**: User interaction and command routing

**Functions**:
- Parse command-line arguments
- Display formatted output
- Handle user commands
- Coordinate between components

**Key Features**:
- Typer framework for CLI
- Rich library for beautiful output
- Command validation
- Help system

---

### 2. Order Manager (orders.py)
**Responsibility**: Business logic for order placement

**Functions**:
- Orchestrate order placement workflow
- Format order requests
- Display order information
- Handle order status queries

**Key Methods**:
```python
- place_order(): Main order placement
- get_order_status(): Query order status
- cancel_order(): Cancel pending orders
- _display_order_request(): Format request display
- _display_order_response(): Format response display
```

---

### 3. Binance Client (client.py)
**Responsibility**: API communication with Binance

**Functions**:
- HTTP request management
- Authentication & signing
- Error handling
- Response parsing

**Key Methods**:
```python
- place_order(): Send order to API
- get_order(): Retrieve order details
- cancel_order(): Cancel order
- test_connectivity(): Test API connection
- get_account_balance(): Fetch balance
- _generate_signature(): HMAC signing
- _request(): Generic HTTP handler
```

**Security Features**:
- HMAC SHA256 request signing
- Timestamp validation
- API key header authentication

---

### 4. Validators (validators.py)
**Responsibility**: Input validation and data models

**Components**:
- `OrderRequest`: Pydantic model for orders
- `OrderSide`: Enum for BUY/SELL
- `OrderType`: Enum for MARKET/LIMIT
- `validate_order_input()`: Validation function

**Validation Rules**:
```python
✓ Symbol must be alphanumeric
✓ Quantity must be positive
✓ Price required for LIMIT orders
✓ Price not allowed for MARKET orders
✓ Side must be BUY or SELL
✓ Type must be MARKET or LIMIT
```

---

### 5. Logging System (logging_config.py)
**Responsibility**: Logging configuration and management

**Features**:
- Timestamped log files
- Dual handlers (file + console)
- Different log levels
- Structured format

**Log Levels**:
- DEBUG: Detailed info (file only)
- INFO: General info (file + console)
- ERROR: Error messages (file + console)

---

## Data Flow

### Order Placement Flow

```
1. User Input
   │
   ├─▶ CLI parses arguments
   │   └─▶ Extracts: symbol, side, type, quantity, price
   │
2. Validation
   │
   ├─▶ Validator checks inputs
   │   ├─▶ Symbol format
   │   ├─▶ Quantity > 0
   │   └─▶ Price for LIMIT
   │
3. Order Manager
   │
   ├─▶ Creates OrderRequest
   ├─▶ Displays request summary
   └─▶ Calls client
   │
4. Binance Client
   │
   ├─▶ Adds timestamp
   ├─▶ Generates signature
   ├─▶ Sends HTTP request
   └─▶ Receives response
   │
5. Response Handling
   │
   ├─▶ Parse JSON response
   ├─▶ Check for errors
   ├─▶ Log response
   └─▶ Display to user
```

---

## Error Handling Flow

```
┌─────────────┐
│ User Input  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Validation      │───▶ ValueError ───▶ Display & Log
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ API Request     │───▶ NetworkError ──▶ Display & Log
└──────┬──────────┘      BinanceError
       │
       ▼
┌─────────────────┐
│ Response Parse  │───▶ JSONError ────▶ Display & Log
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Success Display │
└─────────────────┘
```

---

## Module Dependencies

```
cli.py
├── bot.BinanceClient
├── bot.OrderManager
├── bot.setup_logger
├── typer
├── rich
└── dotenv

orders.py
├── bot.BinanceClient
├── bot.validators
├── bot.logging_config
└── rich

client.py
├── requests
├── hmac/hashlib
└── bot.logging_config

validators.py
└── pydantic
```

---

## Configuration Flow

```
1. .env File
   ├── BINANCE_API_KEY
   └── BINANCE_API_SECRET
   
2. dotenv.load_env()
   │
   ▼
   
3. os.getenv()
   │
   ▼
   
4. BinanceClient(api_key, api_secret)
   │
   ▼
   
5. HTTP Headers
   └── X-MBX-APIKEY: {api_key}
```

---

## Extension Points

### Easy to Add:

1. **New Order Types**
   - Add enum in `validators.py`
   - Update validation logic
   - Add handling in `client.py`

2. **New Commands**
   - Add `@app.command()` in `cli.py`
   - Implement logic in appropriate module

3. **Additional Validation**
   - Add validators in `validators.py`
   - Use Pydantic's built-in validators

4. **Custom Logging**
   - Modify `logging_config.py`
   - Add new handlers or formatters

---

## Security Architecture

```
┌──────────────────────┐
│  Environment (.env)  │  ◀── Not in Git
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Python Process     │
│  (loads credentials) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  HMAC SHA256 Signing │  ◀── Every request
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   HTTPS Request      │  ◀── Encrypted
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Binance Testnet    │
└──────────────────────┘
```

---

## Performance Considerations

1. **Connection Pooling**: Using `requests.Session()`
2. **Timeout Handling**: 10-second timeout on requests
3. **Minimal Dependencies**: Only essential packages
4. **Lazy Logging**: Logger initialized only when needed
5. **Efficient Validation**: Pydantic's fast validators

---

## Testing Strategy

1. **Unit Tests** (Future):
   - Test validators independently
   - Mock API responses
   - Test error handling

2. **Integration Tests** (Future):
   - Test full order flow
   - Test with real testnet API

3. **Manual Testing** (Current):
   - `test_orders.py` script
   - CLI command testing
   - Log file verification

---

## Deployment Checklist

- [x] Python 3.8+ required
- [x] Virtual environment recommended
- [x] Dependencies in requirements.txt
- [x] Configuration via .env file
- [x] Logs directory auto-created
- [x] Testnet-only (safe for practice)
- [x] No hardcoded credentials
- [x] Comprehensive error handling

---

## Future Enhancements

### Phase 1: More Order Types
- Stop-Loss orders
- Take-Profit orders
- OCO (One-Cancels-Other)

### Phase 2: Position Management
- Open position tracking
- Position closing
- PnL calculation

### Phase 3: Automation
- Scheduled orders
- Strategy execution
- Market monitoring

### Phase 4: Advanced Features
- WebSocket for real-time data
- Multi-symbol support
- Risk management
- Backtesting

---

**Documentation Version**: 1.0  
**Last Updated**: February 2, 2026  
**Author**: Application Submission for Anything.ai
