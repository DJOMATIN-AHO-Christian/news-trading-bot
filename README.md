# 📈 News-Based Algorithmic Trading Bot

An intelligent trading bot that analyzes financial news sentiment using NLP to make automated trading decisions. The system backtests strategies against historical data and provides an interactive dashboard to visualize performance.

## 🚀 Quick Start (3 Minutes)

### 1. Get FREE API Key
👉 **https://newsapi.org/register**
- Sign up (email + password)
- Copy your API key

### 2. Configure
```bash
# Copy example config
copy .env.example .env

# Edit with your key
notepad .env
```
Replace `your_newsapi_key_here` with your actual API key.

### 3. Run
```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run backtest
python main.py --backtest --symbol AAPL --days 30

# Or launch dashboard
python start_dashboard.py
```

Open **http://localhost:5000** in your browser.

✅ **Done!** The bot now uses real news and sentiment analysis.

---

## ✨ Features

- **Sentiment Analysis**: Uses DistilBERT NLP model to analyze financial news headlines
- **Automated Trading**: Makes buy/sell decisions based on sentiment thresholds
- **Backtesting Engine**: Simulates historical trades and calculates performance metrics
- **Interactive Dashboard**: Beautiful Plotly/Dash visualization with real-time updates
- **Performance Comparison**: Strategy vs Buy & Hold benchmark
- **Multiple Assets**: Support for stocks, ETFs, and cryptocurrencies

## 🎯 Strategy

The bot implements a simple yet effective sentiment-based strategy:
- **BUY** when average news sentiment > +0.5 (positive news)
- **SELL** when average news sentiment < -0.5 (negative news)
- **HOLD** otherwise

## 📋 Prerequisites

- Python 3.8 or higher
- NewsAPI key (free tier available at [newsapi.org](https://newsapi.org/register))

## 🚀 Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your NewsAPI key
   # Get your free key at: https://newsapi.org/register
   ```

4. **Edit the `.env` file**:
   ```env
   NEWS_API_KEY=your_actual_api_key_here
   ```

## 💻 Usage

### Run a Backtest (CLI)

Test the strategy on historical data:

```bash
# Basic backtest for Apple stock (90 days)
python main.py --backtest --symbol AAPL --days 90

# Backtest Tesla with custom capital
python main.py --backtest --symbol TSLA --days 60 --capital 50000

# Backtest Bitcoin
python main.py --backtest --symbol BTC-USD --days 120
```

### Launch Interactive Dashboard

Start the web-based dashboard for visual analysis:

```bash
python main.py --dashboard
```

Then open your browser to: **http://localhost:8050**

### Dashboard Features

- 📊 **Performance Charts**: Compare strategy vs Buy & Hold
- 📈 **Sentiment Timeline**: Visualize news sentiment over time
- 🎯 **Trading Signals**: See buy/sell decisions on the chart
- 📰 **Recent News**: View latest headlines with sentiment scores
- 🎛️ **Interactive Controls**: Change symbols, periods, and capital

## 📊 Performance Metrics

The bot calculates comprehensive metrics:

- **Total Return**: Overall profit/loss percentage
- **Sharpe Ratio**: Risk-adjusted return measure
- **Max Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Outperformance**: Strategy return vs Buy & Hold

## 🎨 Dashboard Preview

The dashboard features:
- Modern dark theme (Cyborg)
- Real-time performance charts
- Sentiment analysis visualization
- Trading signal markers
- Performance metrics cards
- Recent news with sentiment scores

## ⚙️ Configuration

Edit `.env` to customize:

```env
# Trading Strategy
SENTIMENT_BUY_THRESHOLD=0.5    # Buy when sentiment > this
SENTIMENT_SELL_THRESHOLD=-0.5  # Sell when sentiment < this
INITIAL_CAPITAL=10000          # Starting capital
POSITION_SIZE=0.2              # Use 20% of portfolio per trade

# Backtesting
DEFAULT_SYMBOL=AAPL            # Default stock symbol
BACKTEST_DAYS=90               # Default backtest period
```

## 🔧 Supported Symbols

### Stocks
- AAPL (Apple)
- GOOGL (Google)
- MSFT (Microsoft)
- AMZN (Amazon)
- TSLA (Tesla)
- META (Meta/Facebook)
- NVDA (NVIDIA)

### Cryptocurrencies
- BTC-USD (Bitcoin)
- ETH-USD (Ethereum)

*Any symbol supported by Yahoo Finance can be used!*

## 📝 Example Output

```
============================================================
BACKTEST RESULTS
============================================================
Symbol: AAPL
Period: 90 days
Initial Capital: $10,000.00

PERFORMANCE METRICS:
------------------------------------------------------------
Strategy Return:           12.45%
Buy & Hold Return:          8.32%
Outperformance:             4.13%
Sharpe Ratio:               1.85
Max Drawdown:              -5.23%
Win Rate:                  65.0%
Total Trades:              12

Final Portfolio Value: $11,245.00
Final Buy & Hold Value: $10,832.00
============================================================
```

## 🧠 How It Works

1. **News Fetching**: Retrieves financial news from NewsAPI
2. **Sentiment Analysis**: Analyzes headlines using DistilBERT NLP model
3. **Signal Generation**: Compares sentiment to thresholds
4. **Trade Execution**: Simulates buy/sell orders
5. **Performance Tracking**: Calculates metrics and compares to benchmark

## ⚠️ Disclaimer

**This is for educational purposes only!** 

- This bot uses **simulated trading** only
- Past performance does not guarantee future results
- Do not use for real trading without proper risk management
- Always do your own research before investing

## 🛠️ Tech Stack

- **Python 3.8+**
- **NewsAPI**: Financial news data
- **yfinance**: Market data
- **Transformers (HuggingFace)**: NLP sentiment analysis
- **Plotly/Dash**: Interactive visualizations
- **Pandas/NumPy**: Data processing

## 📚 Project Structure

```
news-trading-bot/
├── main.py              # Entry point
├── config.py            # Configuration management
├── news_analyzer.py     # News sentiment analysis
├── market_data.py       # Market data fetching
├── trading_strategy.py  # Trading logic
├── backtester.py        # Backtesting engine
├── dashboard.py         # Interactive dashboard
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
└── README.md           # This file
```

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📄 License

MIT License - feel free to use this project for learning and experimentation.

---

**Happy Trading! 📈🚀**
