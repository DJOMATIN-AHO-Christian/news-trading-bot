"""Demo script to showcase the trading bot without requiring API keys."""
import sys
import pandas as pd
from datetime import datetime, timedelta
from market_data import MarketData
from trading_strategy import TradingStrategy
from backtester import Backtester

print("=" * 70)
print("  📈 NEWS-BASED ALGORITHMIC TRADING BOT - DEMO")
print("=" * 70)
print()

# Configuration
SYMBOL = 'AAPL'
DAYS = 60
INITIAL_CAPITAL = 10000

print(f"Running backtest demonstration...")
print(f"  Symbol: {SYMBOL}")
print(f"  Period: {DAYS} days")
print(f"  Initial Capital: ${INITIAL_CAPITAL:,}")
print()

# Run backtest
print("Fetching market data and simulating trades...")
print("-" * 70)

backtester = Backtester()
results = backtester.run_backtest(SYMBOL, days=DAYS, initial_capital=INITIAL_CAPITAL)

# Display results
print()
print("=" * 70)
print("  BACKTEST RESULTS")
print("=" * 70)
print()

metrics = results['metrics']

print("📊 PERFORMANCE METRICS:")
print("-" * 70)
print(f"  Strategy Return:        {metrics['strategy_return']:>10.2%}")
print(f"  Buy & Hold Return:      {metrics['buy_hold_return']:>10.2%}")
print(f"  Outperformance:         {metrics['outperformance']:>10.2%}")
print()
print(f"  Sharpe Ratio:           {metrics['strategy_sharpe']:>10.2f}")
print(f"  Max Drawdown:           {metrics['max_drawdown']:>10.2%}")
print(f"  Win Rate:               {metrics['win_rate']:>10.1%}")
print(f"  Total Trades:           {metrics['total_trades']:>10}")
print()
print(f"  Final Portfolio Value:  ${metrics['final_portfolio_value']:>10,.2f}")
print(f"  Final Buy & Hold Value: ${metrics['final_buy_hold_value']:>10,.2f}")
print()

# Show recent trades
if results['trades']:
    print("📝 RECENT TRADES (Last 10):")
    print("-" * 70)
    print(f"{'Date':<12} {'Action':<6} {'Price':>10} {'Shares':>10} {'Sentiment':>10}")
    print("-" * 70)
    
    for trade in results['trades'][-10:]:
        date_str = trade['timestamp'].strftime('%Y-%m-%d')
        action = trade['action']
        price = trade['price']
        shares = trade['shares']
        sentiment = trade['sentiment']
        
        # Color coding (won't show in terminal but good for reference)
        action_display = f"{'🟢' if action == 'BUY' else '🔴'} {action}"
        
        print(f"{date_str:<12} {action:<6} ${price:>9.2f} {shares:>10.4f} {sentiment:>10.3f}")

print()
print("=" * 70)

# Performance summary
if metrics['outperformance'] > 0:
    print(f"✅ Strategy OUTPERFORMED Buy & Hold by {metrics['outperformance']:.2%}!")
else:
    print(f"⚠️  Strategy UNDERPERFORMED Buy & Hold by {abs(metrics['outperformance']):.2%}")

print()
print("💡 Next Steps:")
print("  1. Get a free NewsAPI key at: https://newsapi.org/register")
print("  2. Copy .env.example to .env and add your key")
print("  3. Run: python main.py --dashboard")
print("  4. Open browser to: http://localhost:8050")
print()
print("=" * 70)
