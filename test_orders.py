#!/usr/bin/env python3
"""
Test script to demonstrate trading bot functionality.
This script is for demonstration purposes only.
"""
import os
from dotenv import load_dotenv
from bot import BinanceClient, OrderManager, BinanceClientError, setup_logger
from rich.console import Console

# Load environment variables
load_dotenv()

# Initialize console and logger
console = Console()
logger = setup_logger()


def test_market_order():
    """Test placing a market order."""
    console.print("\n[bold cyan]═══ Testing MARKET Order ═══[/bold cyan]\n")
    
    try:
        # Initialize client
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            console.print("[bold red]Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file[/bold red]")
            return
        
        client = BinanceClient(api_key=api_key, api_secret=api_secret, testnet=True)
        order_manager = OrderManager(client)
        
        # Test connectivity
        console.print("[yellow]Testing API connectivity...[/yellow]")
        if not client.test_connectivity():
            console.print("[bold red]Failed to connect to API[/bold red]")
            return
        console.print("[green]✓ Connected[/green]\n")
        
        # Place market order
        response = order_manager.place_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity=0.001
        )
        
        console.print(f"\n[bold green]✓ Market order test completed successfully![/bold green]")
        console.print(f"Order ID: {response.get('orderId')}\n")
        
    except BinanceClientError as e:
        console.print(f"[bold red]API Error: {str(e)}[/bold red]")
        logger.error(f"Market order test failed: {str(e)}")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        logger.error(f"Market order test failed: {str(e)}", exc_info=True)


def test_limit_order():
    """Test placing a limit order."""
    console.print("\n[bold cyan]═══ Testing LIMIT Order ═══[/bold cyan]\n")
    
    try:
        # Initialize client
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            console.print("[bold red]Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file[/bold red]")
            return
        
        client = BinanceClient(api_key=api_key, api_secret=api_secret, testnet=True)
        order_manager = OrderManager(client)
        
        # Test connectivity
        console.print("[yellow]Testing API connectivity...[/yellow]")
        if not client.test_connectivity():
            console.print("[bold red]Failed to connect to API[/bold red]")
            return
        console.print("[green]✓ Connected[/green]\n")
        
        # Place limit order (set price very high so it doesn't fill immediately)
        response = order_manager.place_order(
            symbol="BTCUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity=0.001,
            price=100000  # High price to ensure it doesn't fill
        )
        
        console.print(f"\n[bold green]✓ Limit order test completed successfully![/bold green]")
        console.print(f"Order ID: {response.get('orderId')}\n")
        
    except BinanceClientError as e:
        console.print(f"[bold red]API Error: {str(e)}[/bold red]")
        logger.error(f"Limit order test failed: {str(e)}")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        logger.error(f"Limit order test failed: {str(e)}", exc_info=True)


def main():
    """Run all tests."""
    console.print("""
[bold cyan]╔═══════════════════════════════════════════════╗
║  Binance Futures Trading Bot - Test Suite   ║
╚═══════════════════════════════════════════════╝[/bold cyan]
    """)
    
    console.print("[yellow]This script will test both MARKET and LIMIT orders[/yellow]")
    console.print("[yellow]Make sure you have sufficient testnet balance![/yellow]\n")
    
    input("Press Enter to start tests...")
    
    # Run tests
    test_market_order()
    test_limit_order()
    
    console.print("\n[bold green]═══ All Tests Completed ═══[/bold green]")
    console.print("\n[cyan]Check the logs/ directory for detailed execution logs[/cyan]\n")


if __name__ == "__main__":
    main()
