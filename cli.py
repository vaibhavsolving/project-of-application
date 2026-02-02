#!/usr/bin/env python3
"""
Trading Bot CLI - Command-line interface for Binance Futures Testnet trading.
"""
import os
import sys
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

from bot import (
    BinanceClient,
    BinanceClientError,
    OrderManager,
    setup_logger,
    get_logger
)


# Load environment variables
load_dotenv()

# Initialize CLI app
app = typer.Typer(
    name="trading-bot",
    help="Trading Bot for Binance Futures Testnet",
    add_completion=False
)

console = Console()
logger = None  # Will be initialized when needed


def initialize_logger():
    """Initialize logger if not already initialized."""
    global logger
    if logger is None:
        logger = setup_logger()


def get_client() -> BinanceClient:
    """
    Get initialized Binance client from environment variables.
    
    Returns:
        BinanceClient instance
        
    Raises:
        typer.Exit: If credentials are not configured
    """
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        console.print(
            Panel(
                "[bold red]Missing API credentials![/bold red]\n\n"
                "Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.\n"
                "You can create a .env file in the project root with:\n\n"
                "BINANCE_API_KEY=your_api_key_here\n"
                "BINANCE_API_SECRET=your_api_secret_here",
                title="❌ Configuration Error",
                border_style="red"
            )
        )
        raise typer.Exit(code=1)
    
    return BinanceClient(api_key=api_key, api_secret=api_secret, testnet=True)


@app.command()
def place_order(
    symbol: str = typer.Argument(..., help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side: BUY or SELL"),
    order_type: str = typer.Argument(..., help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Argument(..., help="Order quantity"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Order price (required for LIMIT orders)"),
):
    """
    Place an order on Binance Futures Testnet.
    
    Examples:
    
    \b
    # Place a market buy order
    python cli.py place-order BTCUSDT BUY MARKET 0.001
    
    \b
    # Place a limit sell order
    python cli.py place-order BTCUSDT SELL LIMIT 0.001 --price 50000
    """
    initialize_logger()
    
    console.print(Panel(
        "[bold cyan]Binance Futures Testnet Trading Bot[/bold cyan]\n"
        "Starting order placement...",
        border_style="cyan"
    ))
    
    try:
        # Initialize client and order manager
        client = get_client()
        order_manager = OrderManager(client)
        
        # Test connectivity
        console.print("[yellow]Testing API connectivity...[/yellow]")
        if not client.test_connectivity():
            console.print("[bold red]Failed to connect to Binance API[/bold red]")
            raise typer.Exit(code=1)
        console.print("[green]✓ Connected successfully[/green]\n")
        
        # Place order
        response = order_manager.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        logger.info(f"Order completed: {response}")
        
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {str(e)}")
        logger.error(f"Validation error: {str(e)}")
        raise typer.Exit(code=1)
    except BinanceClientError as e:
        console.print(f"[bold red]API Error:[/bold red] {str(e)}")
        logger.error(f"API error: {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {str(e)}")
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise typer.Exit(code=1)


@app.command()
def check_balance():
    """
    Check account balance on Binance Futures Testnet.
    """
    initialize_logger()
    
    console.print(Panel(
        "[bold cyan]Checking Account Balance[/bold cyan]",
        border_style="cyan"
    ))
    
    try:
        client = get_client()
        
        console.print("[yellow]Fetching account balance...[/yellow]\n")
        balance_data = client.get_account_balance()
        
        from rich.table import Table
        
        table = Table(title="Account Balance", show_header=True, header_style="bold cyan")
        table.add_column("Asset", style="yellow")
        table.add_column("Wallet Balance", justify="right", style="green")
        table.add_column("Available Balance", justify="right", style="cyan")
        
        for asset in balance_data:
            if float(asset['balance']) > 0:  # Only show non-zero balances
                table.add_row(
                    asset['asset'],
                    asset['balance'],
                    asset['availableBalance']
                )
        
        console.print(table)
        logger.info("Balance check completed")
        
    except BinanceClientError as e:
        console.print(f"[bold red]API Error:[/bold red] {str(e)}")
        logger.error(f"API error: {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {str(e)}")
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise typer.Exit(code=1)


@app.command()
def test_connection():
    """
    Test connection to Binance Futures Testnet API.
    """
    initialize_logger()
    
    console.print(Panel(
        "[bold cyan]Testing API Connection[/bold cyan]",
        border_style="cyan"
    ))
    
    try:
        client = get_client()
        
        console.print("[yellow]Testing connectivity...[/yellow]")
        if client.test_connectivity():
            console.print("[bold green]✓ Connection successful![/bold green]")
            
            # Get server time
            server_time = client.get_server_time()
            from datetime import datetime
            server_datetime = datetime.fromtimestamp(server_time['serverTime'] / 1000)
            console.print(f"[cyan]Server time: {server_datetime.strftime('%Y-%m-%d %H:%M:%S')}[/cyan]")
            
            logger.info("Connection test successful")
        else:
            console.print("[bold red]✗ Connection failed[/bold red]")
            raise typer.Exit(code=1)
            
    except BinanceClientError as e:
        console.print(f"[bold red]API Error:[/bold red] {str(e)}")
        logger.error(f"API error: {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {str(e)}")
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise typer.Exit(code=1)


@app.command()
def version():
    """
    Show version information.
    """
    from bot import __version__
    console.print(f"[bold cyan]Trading Bot v{__version__}[/bold cyan]")
    console.print("Binance Futures Testnet Trading Bot")


if __name__ == "__main__":
    app()
