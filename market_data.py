"""Market data integration using yfinance."""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketData:
    """Fetches and processes market data using yfinance."""
    
    def __init__(self):
        """Initialize the market data handler."""
        self.cache = {}
    
    def get_price_history(
        self, 
        symbol: str, 
        days: int = 90,
        interval: str = '1d'
    ) -> pd.DataFrame:
        """
        Get historical price data for a symbol.
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'BTC-USD')
            days: Number of days of historical data
            interval: Data interval ('1d', '1h', etc.)
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            logger.info(f"Fetching {days} days of data for {symbol}")
            
            # Fetch data from yfinance
            ticker = yf.Ticker(symbol)
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval
            )
            
            if df.empty:
                logger.warning(f"No data found for {symbol}")
                return pd.DataFrame()
            
            # Clean and prepare data
            df = df.reset_index()
            df.columns = [col.lower() for col in df.columns]
            
            logger.info(f"Retrieved {len(df)} data points for {symbol}")
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching price data: {e}")
            return pd.DataFrame()
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get the current price for a symbol.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Current price or None if unavailable
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            
            if data.empty:
                return None
            
            current_price = data['Close'].iloc[-1]
            return float(current_price)
            
        except Exception as e:
            logger.error(f"Error fetching current price: {e}")
            return None
    
    def calculate_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate daily returns.
        
        Args:
            df: DataFrame with price data
            
        Returns:
            DataFrame with added 'returns' column
        """
        if df.empty or 'close' not in df.columns:
            return df
        
        df = df.copy()
        df['returns'] = df['close'].pct_change()
        return df
    
    def calculate_moving_average(
        self, 
        df: pd.DataFrame, 
        window: int = 20
    ) -> pd.DataFrame:
        """
        Calculate moving average.
        
        Args:
            df: DataFrame with price data
            window: Moving average window
            
        Returns:
            DataFrame with added MA column
        """
        if df.empty or 'close' not in df.columns:
            return df
        
        df = df.copy()
        df[f'ma_{window}'] = df['close'].rolling(window=window).mean()
        return df
    
    def get_ticker_info(self, symbol: str) -> dict:
        """
        Get ticker information.
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary with ticker info
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'USD')
            }
            
        except Exception as e:
            logger.error(f"Error fetching ticker info: {e}")
            return {'symbol': symbol, 'name': symbol}
