"""Configuration management for the trading bot."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # API Keys
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    
    # Trading Strategy Parameters
    SENTIMENT_BUY_THRESHOLD = float(os.getenv('SENTIMENT_BUY_THRESHOLD', '0.5'))
    SENTIMENT_SELL_THRESHOLD = float(os.getenv('SENTIMENT_SELL_THRESHOLD', '-0.5'))
    INITIAL_CAPITAL = float(os.getenv('INITIAL_CAPITAL', '10000'))
    POSITION_SIZE = float(os.getenv('POSITION_SIZE', '0.2'))
    
    # Backtesting Configuration
    DEFAULT_SYMBOL = os.getenv('DEFAULT_SYMBOL', 'AAPL')
    BACKTEST_DAYS = int(os.getenv('BACKTEST_DAYS', '90'))
    
    # NLP Configuration
    # Using VADER (lightweight, no GPU, no model download required)
    # Replaces transformers/DistilBERT (~1GB) with vaderSentiment (~500KB)

    # Dashboard Configuration
    DASHBOARD_HOST = '127.0.0.1'
    DASHBOARD_PORT = 8050
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.NEWS_API_KEY:
            raise ValueError(
                "NEWS_API_KEY not found. Please set it in .env file. "
                "Get your free key at https://newsapi.org/register"
            )
        return True
