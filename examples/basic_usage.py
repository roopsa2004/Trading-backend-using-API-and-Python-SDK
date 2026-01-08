# File: examples/basic_usage.py
"""
Basic usage examples for the Trading SDK.
Demonstrates common trading operations.
"""

import sys
import os

# Add parent directory to path so we can import sdk
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sdk.trading_sdk import TradingSDK, TradingSDKException


def main():
    # Initialize SDK
    sdk = TradingSDK(base_url='http://localhost:5000')
    
    try:
        print("=" * 60)
        print("TRADING PLATFORM SDK - BASIC USAGE EXAMPLES")
        print("=" * 60)
        
        # 1. Health Check
        print("\n1. Checking API Health...")
        health = sdk.health_check()
        print(f"   Status: {health['status']}")
        
        # 2. Get All Instruments
        print("\n2. Fetching Available Instruments...")
        instruments = sdk.get_instruments()
        print(f"   Found {len(instruments)} tradable instruments:")
        for inst in instruments[:5]:  # Show first 5
            print(f"   - {inst['symbol']:6s} | {inst['name']:30s} | ${inst['lastTradedPrice']:.2f}")
        
        # 3. Get Specific Instrument
        print("\n3. Getting AAPL Details...")
        aapl = sdk.get_instrument('AAPL')
        print(f"   Name: {aapl['name']}")
        print(f"   Price: ${aapl['lastTradedPrice']:.2f}")
        print(f"   Exchange: {aapl['exchange']}")
        
        # 4. Place a Market Buy Order
        print("\n4. Placing Market BUY Order (AAPL, 10 shares)...")
        buy_result = sdk.place_buy_order('AAPL', 10)
        order = buy_result['order']
        trade = buy_result.get('trade')
        print(f"   Order ID: {order['id']}")
        print(f"   Status: {order['status']}")
        if trade:
            print(f"   Executed at: ${trade['executedPrice']:.2f}")
            print(f"   Total Value: ${trade['totalValue']:.2f}")
        
        # 5. View Portfolio
        print("\n5. Viewing Portfolio...")
        portfolio = sdk.get_portfolio()
        print(f"   Total Holdings: {portfolio['count']}")
        print(f"   Total Invested: ${portfolio['totalInvested']:.2f}")
        print(f"   Current Value: ${portfolio['totalCurrentValue']:.2f}")
        print(f"   Profit/Loss: ${portfolio['totalProfitLoss']:.2f}")
        print("\n   Holdings:")
        for holding in portfolio['holdings']:
            print(f"   - {holding['symbol']:6s}: {holding['quantity']:4d} shares @ ${holding['averagePrice']:.2f}")
        
        # 6. Place Another Buy Order (Different Stock)
        print("\n6. Buying GOOGL (5 shares)...")
        googl_result = sdk.place_buy_order('GOOGL', 5)
        print(f"   Order Status: {googl_result['order']['status']}")
        
        # 7. View All Orders
        print("\n7. Viewing All Orders...")
        orders = sdk.get_orders()
        print(f"   Total Orders: {len(orders)}")
        for order in orders[-3:]:  # Show last 3
            print(f"   - Order #{order['id']}: {order['orderType']} {order['quantity']} {order['symbol']} - {order['status']}")
        
        # 8. View All Trades
        print("\n8. Viewing Executed Trades...")
        trades = sdk.get_trades()
        print(f"   Total Trades: {len(trades)}")
        for trade in trades[-3:]:  # Show last 3
            print(f"   - {trade['tradeType']} {trade['quantity']} {trade['symbol']} @ ${trade['executedPrice']:.2f}")
        
        # 9. Place a Limit Order
        print("\n9. Placing Limit BUY Order (MSFT, 3 shares @ $380)...")
        limit_result = sdk.place_buy_order('MSFT', 3, price=380.00)
        print(f"   Order Status: {limit_result['order']['status']}")
        print(f"   Limit Price: ${limit_result['order']['price']:.2f}")
        
        # 10. Sell Some Holdings
        print("\n10. Selling AAPL (5 shares)...")
        sell_result = sdk.place_sell_order('AAPL', 5)
        print(f"   Order Status: {sell_result['order']['status']}")
        if sell_result.get('trade'):
            print(f"   Sold at: ${sell_result['trade']['executedPrice']:.2f}")
        
        # 11. View Updated Portfolio
        print("\n11. Updated Portfolio...")
        portfolio = sdk.get_portfolio()
        print(f"   Total Current Value: ${portfolio['totalCurrentValue']:.2f}")
        print(f"   Profit/Loss: ${portfolio['totalProfitLoss']:.2f}")
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except TradingSDKException as e:
        print(f"\nError: {e.message}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
    
    finally:
        sdk.close()


if __name__ == '__main__':
    main()