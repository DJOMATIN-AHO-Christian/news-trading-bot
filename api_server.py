"""Flask API server for the HTML dashboard."""
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
from backtester import Backtester
from news_analyzer import NewsAnalyzer
from market_data import MarketData

app = Flask(__name__, static_folder='dashboard')
CORS(app)

# Initialize components
backtester = Backtester()
market_data = MarketData()
news_analyzer = None

@app.route('/')
def index():
    """Serve the main dashboard page."""
    return send_from_directory('dashboard', 'index.html')

@app.route('/style.css')
def serve_css():
    """Serve the CSS file."""
    return send_from_directory('dashboard', 'style.css')

@app.route('/app.js')
def serve_js():
    """Serve the JavaScript file."""
    return send_from_directory('dashboard', 'app.js')

@app.route('/api/backtest/<symbol>')
def run_backtest_api(symbol):
    """Run backtest for a symbol and return results."""
    try:
        days = int(request.args.get('days', 90))
        capital = float(request.args.get('capital', 10000))
        
        results = backtester.run_backtest(symbol, days=days, initial_capital=capital)
        
        # Convert DataFrame to JSON-serializable format
        results_data = results['results'].to_dict('records')
        
        # Format dates and handle NaN/Inf values
        for item in results_data:
            item['date'] = item['date'].isoformat()
            # Replace NaN and Inf with None for JSON compatibility
            for key, value in item.items():
                if isinstance(value, float):
                    import math
                    if math.isnan(value) or math.isinf(value):
                        item[key] = None
        
        # Clean metrics too
        clean_metrics = {}
        for key, value in results['metrics'].items():
            if isinstance(value, float):
                import math
                if math.isnan(value) or math.isinf(value):
                    clean_metrics[key] = 0.0
                else:
                    clean_metrics[key] = value
            else:
                clean_metrics[key] = value
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'metrics': clean_metrics,
            'data': results_data,
            'trades': results['trades']
        })
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/price/<symbol>')
def get_price(symbol):
    """Get current price for a symbol."""
    try:
        price = market_data.get_current_price(symbol)
        return jsonify({
            'success': True,
            'symbol': symbol,
            'price': price
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news/<symbol>')
def get_news(symbol):
    """Get news sentiment for a symbol."""
    global news_analyzer
    
    try:
        if news_analyzer is None:
            news_analyzer = NewsAnalyzer()
        
        news_data = news_analyzer.get_aggregated_sentiment(symbol, days=1)
        
        # Format timestamp
        news_data['timestamp'] = news_data['timestamp'].isoformat()
        
        return jsonify({
            'success': True,
            'data': news_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create dashboard directory if it doesn't exist
    os.makedirs('dashboard', exist_ok=True)
    
    print("=" * 70)
    print("  📈 TRADING BOT API SERVER")
    print("=" * 70)
    print()
    print("  Dashboard: http://localhost:5000")
    print("  API Endpoints:")
    print("    - GET /api/backtest/<symbol>?days=90&capital=10000")
    print("    - GET /api/price/<symbol>")
    print("    - GET /api/news/<symbol>")
    print()
    print("  Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=False)
