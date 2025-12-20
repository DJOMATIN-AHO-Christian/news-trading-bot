"""Simple launcher for the dashboard without API key requirement."""
import os
os.environ['NEWS_API_KEY'] = 'demo_key'

from dashboard import app
from config import Config

print("=" * 70)
print("  📈 LAUNCHING TRADING BOT DASHBOARD")
print("=" * 70)
print()
print(f"  Dashboard will open at: http://{Config.DASHBOARD_HOST}:{Config.DASHBOARD_PORT}")
print()
print("  Features:")
print("    - Interactive performance charts")
print("    - Sentiment analysis visualization")
print("    - Trading signals (buy/sell markers)")
print("    - Performance metrics cards")
print("    - Asset selector (AAPL, TSLA, BTC-USD, etc.)")
print()
print("  Press Ctrl+C to stop the server")
print("=" * 70)
print()

app.run_server(
    debug=False,
    host=Config.DASHBOARD_HOST,
    port=Config.DASHBOARD_PORT
)
