"""
Input validation for trading bot orders.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


class OrderSide(str, Enum):
    """Order side enum."""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Order type enum."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class OrderRequest(BaseModel):
    """
    Validated order request model.
    """
    symbol: str = Field(..., description="Trading pair symbol (e.g., BTCUSDT)")
    side: OrderSide = Field(..., description="Order side (BUY or SELL)")
    order_type: OrderType = Field(..., description="Order type (MARKET or LIMIT)")
    quantity: float = Field(..., gt=0, description="Order quantity (must be positive)")
    price: Optional[float] = Field(None, gt=0, description="Order price (required for LIMIT orders)")
    
    @field_validator('symbol')
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        """Validate and normalize symbol."""
        v = v.strip().upper()
        if not v:
            raise ValueError("Symbol cannot be empty")
        if not v.isalnum():
            raise ValueError("Symbol must contain only alphanumeric characters")
        return v
    
    @model_validator(mode='after')
    def validate_price_for_limit(self):
        """Ensure price is provided for LIMIT orders."""
        if self.order_type == OrderType.LIMIT and self.price is None:
            raise ValueError("Price is required for LIMIT orders")
        if self.order_type == OrderType.MARKET and self.price is not None:
            raise ValueError("Price should not be specified for MARKET orders")
        return self
    
    def to_api_params(self) -> dict:
        """
        Convert to API request parameters.
        
        Returns:
            Dictionary of API parameters
        """
        params = {
            "symbol": self.symbol,
            "side": self.side.value,
            "type": self.order_type.value,
            "quantity": self.quantity,
        }
        
        if self.price is not None:
            params["price"] = self.price
        
        return params
    
    def __str__(self) -> str:
        """String representation for logging."""
        base = f"{self.side.value} {self.quantity} {self.symbol} @ {self.order_type.value}"
        if self.price:
            base += f" price={self.price}"
        return base


def validate_order_input(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None
) -> OrderRequest:
    """
    Validate order input and return OrderRequest object.
    
    Args:
        symbol: Trading pair symbol
        side: Order side (BUY/SELL)
        order_type: Order type (MARKET/LIMIT)
        quantity: Order quantity
        price: Order price (optional, required for LIMIT)
        
    Returns:
        Validated OrderRequest object
        
    Raises:
        ValueError: If validation fails
    """
    try:
        return OrderRequest(
            symbol=symbol,
            side=OrderSide(side.upper()),
            order_type=OrderType(order_type.upper()),
            quantity=quantity,
            price=price
        )
    except ValueError as e:
        raise ValueError(f"Validation error: {str(e)}")
