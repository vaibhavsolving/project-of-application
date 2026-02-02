"""
Binance Futures Testnet API client wrapper.
"""
import time
import hmac
import hashlib
from typing import Dict, Optional
from urllib.parse import urlencode
import requests

from .logging_config import get_logger


logger = get_logger(__name__)


class BinanceClientError(Exception):
    """Custom exception for Binance client errors."""
    pass


class BinanceClient:
    """
    Binance Futures Testnet API client.
    
    Handles authentication, request signing, and API communication.
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize Binance client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Whether to use testnet (default: True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://fapi.binance.com"
        
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/json'
        })
        
        logger.info(f"Initialized BinanceClient (testnet={testnet})")
    
    def _generate_signature(self, params: Dict) -> str:
        """
        Generate HMAC SHA256 signature for request.
        
        Args:
            params: Request parameters
            
        Returns:
            Signature string
        """
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        signed: bool = False
    ) -> Dict:
        """
        Make API request.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint
            params: Request parameters
            signed: Whether request requires signature
            
        Returns:
            Response JSON
            
        Raises:
            BinanceClientError: If request fails
        """
        if params is None:
            params = {}
        
        url = f"{self.base_url}{endpoint}"
        
        # Add timestamp and signature for signed requests
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)
        
        logger.debug(f"{method} {endpoint} - Params: {params}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params, timeout=10)
            elif method == 'POST':
                response = self.session.post(url, params=params, timeout=10)
            elif method == 'DELETE':
                response = self.session.delete(url, params=params, timeout=10)
            else:
                raise BinanceClientError(f"Unsupported HTTP method: {method}")
            
            logger.debug(f"Response Status: {response.status_code}")
            
            # Try to parse JSON response
            try:
                data = response.json()
            except ValueError:
                logger.error(f"Failed to parse JSON response: {response.text}")
                raise BinanceClientError(f"Invalid JSON response: {response.text}")
            
            # Check for API errors
            if response.status_code != 200:
                error_msg = data.get('msg', 'Unknown error')
                error_code = data.get('code', 'N/A')
                logger.error(f"API Error [{error_code}]: {error_msg}")
                raise BinanceClientError(f"API Error [{error_code}]: {error_msg}")
            
            logger.debug(f"Response Data: {data}")
            return data
            
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            raise BinanceClientError("Request timeout - please try again")
        except requests.exceptions.ConnectionError:
            logger.error("Connection error")
            raise BinanceClientError("Connection error - please check your internet connection")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise BinanceClientError(f"Request failed: {str(e)}")
    
    def test_connectivity(self) -> bool:
        """
        Test API connectivity.
        
        Returns:
            True if connection successful
        """
        try:
            self._request('GET', '/fapi/v1/ping')
            logger.info("API connectivity test passed")
            return True
        except BinanceClientError as e:
            logger.error(f"API connectivity test failed: {str(e)}")
            return False
    
    def get_server_time(self) -> Dict:
        """
        Get server time.
        
        Returns:
            Server time information
        """
        return self._request('GET', '/fapi/v1/time')
    
    def get_exchange_info(self, symbol: Optional[str] = None) -> Dict:
        """
        Get exchange information.
        
        Args:
            symbol: Optional symbol to filter
            
        Returns:
            Exchange information
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        
        return self._request('GET', '/fapi/v1/exchangeInfo', params=params)
    
    def get_account_balance(self) -> Dict:
        """
        Get account balance.
        
        Returns:
            Account balance information
        """
        return self._request('GET', '/fapi/v2/balance', signed=True)
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC"
    ) -> Dict:
        """
        Place an order on Binance Futures.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (required for LIMIT)
            time_in_force: Time in force (default: GTC - Good Till Cancel)
            
        Returns:
            Order response data
            
        Raises:
            BinanceClientError: If order placement fails
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        
        # Add price and timeInForce for LIMIT orders
        if order_type == 'LIMIT':
            if price is None:
                raise BinanceClientError("Price is required for LIMIT orders")
            params['price'] = price
            params['timeInForce'] = time_in_force
        
        logger.info(f"Placing order: {side} {quantity} {symbol} @ {order_type}" + 
                   (f" price={price}" if price else ""))
        
        return self._request('POST', '/fapi/v1/order', params=params, signed=True)
    
    def get_order(self, symbol: str, order_id: int) -> Dict:
        """
        Get order details.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Order details
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        return self._request('GET', '/fapi/v1/order', params=params, signed=True)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """
        Cancel an order.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Cancellation response
        """
        params = {
            'symbol': symbol,
            'orderId': order_id
        }
        
        logger.info(f"Cancelling order {order_id} for {symbol}")
        return self._request('DELETE', '/fapi/v1/order', params=params, signed=True)
