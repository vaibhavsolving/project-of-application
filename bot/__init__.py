"""
Trading Bot package for Binance Futures Testnet.
"""
from .client import BinanceClient, BinanceClientError
from .orders import OrderManager
from .validators import OrderRequest, OrderSide, OrderType, validate_order_input
from .logging_config import setup_logger, get_logger

__version__ = "1.0.0"

__all__ = [
    'BinanceClient',
    'BinanceClientError',
    'OrderManager',
    'OrderRequest',
    'OrderSide',
    'OrderType',
    'validate_order_input',
    'setup_logger',
    'get_logger',
]
