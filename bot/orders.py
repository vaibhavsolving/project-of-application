"""
Order placement and management logic.
"""
from typing import Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .client import BinanceClient, BinanceClientError
from .validators import OrderRequest, validate_order_input
from .logging_config import get_logger


logger = get_logger(__name__)
console = Console()


class OrderManager:
    """
    Manages order placement and execution on Binance Futures.
    """
    
    def __init__(self, client: BinanceClient):
        """
        Initialize OrderManager.
        
        Args:
            client: BinanceClient instance
        """
        self.client = client
        logger.info("OrderManager initialized")
    
    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> Dict:
        """
        Place an order with validation and error handling.
        
        Args:
            symbol: Trading pair symbol
            side: Order side (BUY/SELL)
            order_type: Order type (MARKET/LIMIT)
            quantity: Order quantity
            price: Order price (optional, required for LIMIT)
            
        Returns:
            Order response data
            
        Raises:
            ValueError: If validation fails
            BinanceClientError: If order placement fails
        """
        # Validate input
        try:
            order_request = validate_order_input(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )
        except ValueError as e:
            logger.error(f"Order validation failed: {str(e)}")
            raise
        
        # Display order request summary
        self._display_order_request(order_request)
        
        # Place order
        try:
            response = self.client.place_order(
                symbol=order_request.symbol,
                side=order_request.side.value,
                order_type=order_request.order_type.value,
                quantity=order_request.quantity,
                price=order_request.price
            )
            
            logger.info(f"Order placed successfully: Order ID {response.get('orderId')}")
            
            # Display order response
            self._display_order_response(response, success=True)
            
            return response
            
        except BinanceClientError as e:
            logger.error(f"Order placement failed: {str(e)}")
            self._display_error(str(e))
            raise
    
    def _display_order_request(self, order_request: OrderRequest):
        """
        Display order request summary in a formatted table.
        
        Args:
            order_request: Validated order request
        """
        console.print("\n[bold cyan]📋 Order Request Summary[/bold cyan]")
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold yellow")
        table.add_column("Value", style="white")
        
        table.add_row("Symbol", order_request.symbol)
        table.add_row("Side", order_request.side.value)
        table.add_row("Type", order_request.order_type.value)
        table.add_row("Quantity", str(order_request.quantity))
        
        if order_request.price:
            table.add_row("Price", str(order_request.price))
        
        console.print(table)
    
    def _display_order_response(self, response: Dict, success: bool = True):
        """
        Display order response details.
        
        Args:
            response: Order response from API
            success: Whether order was successful
        """
        if success:
            console.print("\n[bold green]✅ Order Placed Successfully[/bold green]")
        else:
            console.print("\n[bold red]❌ Order Failed[/bold red]")
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Field", style="bold cyan")
        table.add_column("Value", style="white")
        
        # Key fields to display
        fields_to_display = [
            ('orderId', 'Order ID'),
            ('symbol', 'Symbol'),
            ('status', 'Status'),
            ('side', 'Side'),
            ('type', 'Type'),
            ('origQty', 'Original Quantity'),
            ('executedQty', 'Executed Quantity'),
            ('price', 'Price'),
            ('avgPrice', 'Average Price'),
            ('timeInForce', 'Time In Force'),
            ('updateTime', 'Update Time'),
        ]
        
        for api_field, display_name in fields_to_display:
            if api_field in response and response[api_field]:
                value = response[api_field]
                # Format timestamps
                if api_field in ['updateTime', 'transactTime']:
                    from datetime import datetime
                    value = datetime.fromtimestamp(value / 1000).strftime('%Y-%m-%d %H:%M:%S')
                table.add_row(display_name, str(value))
        
        console.print(table)
        
        # Display success message with key info
        if success and response.get('status') == 'FILLED':
            avg_price = response.get('avgPrice', response.get('price', 'N/A'))
            console.print(
                f"\n[bold green]Order {response['orderId']} filled at average price: {avg_price}[/bold green]"
            )
        elif success and response.get('status') == 'NEW':
            console.print(
                f"\n[bold yellow]Order {response['orderId']} created and waiting to be filled[/bold yellow]"
            )
    
    def _display_error(self, error_message: str):
        """
        Display error message.
        
        Args:
            error_message: Error message to display
        """
        console.print(
            Panel(
                f"[bold red]{error_message}[/bold red]",
                title="❌ Error",
                border_style="red"
            )
        )
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """
        Get order status.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Order details
        """
        try:
            order = self.client.get_order(symbol=symbol, order_id=order_id)
            logger.info(f"Retrieved order {order_id} status: {order.get('status')}")
            return order
        except BinanceClientError as e:
            logger.error(f"Failed to get order status: {str(e)}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """
        Cancel an order.
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
            
        Returns:
            Cancellation response
        """
        try:
            response = self.client.cancel_order(symbol=symbol, order_id=order_id)
            logger.info(f"Order {order_id} cancelled successfully")
            console.print(f"[bold green]✅ Order {order_id} cancelled successfully[/bold green]")
            return response
        except BinanceClientError as e:
            logger.error(f"Failed to cancel order: {str(e)}")
            self._display_error(str(e))
            raise
