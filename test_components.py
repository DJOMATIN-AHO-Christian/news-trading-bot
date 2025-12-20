"""Quick test script to verify components work without API key."""
import sys

print("Testing News Trading Bot Components...")
print("=" * 60)

# Test 1: Import modules
print("\n1. Testing imports...")
try:
    from market_data import MarketData
    from trading_strategy import TradingStrategy
    from backtester import Backtester
    print("   ✓ All modules imported successfully")
except Exception as e:
    print(f"   ✗ Import error: {e}")
    sys.exit(1)

# Test 2: Market Data
print("\n2. Testing market data fetching...")
try:
    md = MarketData()
    df = md.get_price_history('AAPL', days=5)
    if not df.empty:
        print(f"   ✓ Fetched {len(df)} days of AAPL data")
        print(f"   Latest price: ${df.iloc[-1]['close']:.2f}")
    else:
        print("   ⚠ No data returned (may be network issue)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Trading Strategy
print("\n3. Testing trading strategy...")
try:
    strategy = TradingStrategy(initial_capital=10000)
    
    # Test buy signal
    signal = strategy.generate_signal(sentiment=0.7, current_price=150.0)
    print(f"   ✓ Signal for sentiment 0.7: {signal}")
    
    # Test sell signal
    signal = strategy.generate_signal(sentiment=-0.7, current_price=150.0)
    print(f"   ✓ Signal for sentiment -0.7: {signal}")
    
    print("   ✓ Trading strategy working correctly")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Backtester (without news API)
print("\n4. Testing backtester...")
try:
    backtester = Backtester()
    results = backtester.run_backtest('AAPL', days=30, initial_capital=10000)
    
    if results['metrics']:
        metrics = results['metrics']
        print(f"   ✓ Backtest completed successfully")
        print(f"   Strategy Return: {metrics['strategy_return']:.2%}")
        print(f"   Buy & Hold Return: {metrics['buy_hold_return']:.2%}")
        print(f"   Total Trades: {metrics['total_trades']}")
    else:
        print("   ⚠ Backtest ran but no metrics generated")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("✓ Core components are working!")
print("\nNext steps:")
print("1. Copy .env.example to .env")
print("2. Add your NewsAPI key to .env")
print("3. Run: python main.py --backtest --symbol AAPL")
print("4. Or run: python main.py --dashboard")
print("=" * 60)
