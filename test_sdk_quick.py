# Quick SDK Test
from sdk.trading_sdk import TradingSDK

# Initialize SDK
sdk = TradingSDK(base_url='http://localhost:5000')

print("🧪 Testing Trading Platform SDK\n")

# 1. Health check
print("1. Health Check:")
health = sdk.health_check()
print(f"   Status: {health}\n")

# 2. Get instruments
print("2. Get Instruments:")
instruments = sdk.get_instruments()
print(f"   Found {len(instruments)} instruments")
for inst in instruments[:3]:
    print(f"   - {inst['symbol']}: ${inst['lastTradedPrice']}\n")

# 3. Get specific instrument
print("3. Get AAPL Details:")
aapl = sdk.get_instrument('AAPL')
print(f"   Name: {aapl['name']}")
print(f"   Price: ${aapl['lastTradedPrice']}\n")

# 4. Place a buy order
print("4. Placing Market BUY Order (AAPL, 10 shares):")
result = sdk.place_buy_order('AAPL', 10)
print(f"   Order ID: {result['order']['id']}")
print(f"   Status: {result['order']['status']}")
if 'trade' in result:
    print(f"   Executed at: ${result['trade']['executedPrice']}")
    print(f"   Total: ${result['trade']['totalValue']}\n")

# 5. View portfolio
print("5. Portfolio:")
portfolio = sdk.get_portfolio()
print(f"   Total Value: ${portfolio['totalCurrentValue']:.2f}")
print(f"   P/L: ${portfolio['totalProfitLoss']:.2f}")
for holding in portfolio['holdings']:
    print(f"   - {holding['symbol']}: {holding['quantity']} shares\n")

# 6. View trades
print("6. Recent Trades:")
trades = sdk.get_trades()
print(f"   Total trades: {len(trades)}")
for trade in trades[-3:]:
    print(f"   - {trade['tradeType']} {trade['quantity']} {trade['symbol']} @ ${trade['executedPrice']}")

sdk.close()
print("\n✅ SDK Test Complete!")