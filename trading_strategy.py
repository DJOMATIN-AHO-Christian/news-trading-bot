"""Trading strategy based on news sentiment."""
from typing import Dict, List, Optional
from datetime import datetime
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradingStrategy:
    """Implements sentiment-based trading strategy."""
    
    def __init__(
        self,
        initial_capital: float = None,
        position_size: float = None,
        buy_threshold: float = None,
        sell_threshold: float = None
    ):
        """
        Initialize trading strategy.
        
        Args:
            initial_capital: Starting capital
            position_size: Fraction of portfolio to use per trade (0-1)
            buy_threshold: Sentiment threshold for buy signal
            sell_threshold: Sentiment threshold for sell signal
        """
        self.initial_capital = initial_capital or Config.INITIAL_CAPITAL
        self.position_size = position_size or Config.POSITION_SIZE
        self.buy_threshold = buy_threshold or Config.SENTIMENT_BUY_THRESHOLD
        self.sell_threshold = sell_threshold or Config.SENTIMENT_SELL_THRESHOLD
        
        # Portfolio state
        self.cash = self.initial_capital
        self.holdings = 0  # Number of shares
        self.portfolio_value = self.initial_capital
        
        # Trade history
        self.trades = []
        
        logger.info(
            f"Strategy initialized: Capital=${self.initial_capital:,.2f}, "
            f"Buy>{self.buy_threshold}, Sell<{self.sell_threshold}"
        )
    
    def generate_signal(self, sentiment: float, current_price: float) -> str:
        """
        Generate trading signal based on sentiment.
        
        Args:
            sentiment: Sentiment score (-1 to 1)
            current_price: Current asset price
            
        Returns:
            'BUY', 'SELL', or 'HOLD'
        """
        if sentiment > self.buy_threshold:
            # Only buy if we have cash
            if self.cash > 0:
                return 'BUY'
        elif sentiment < self.sell_threshold:
            # Only sell if we have holdings
            if self.holdings > 0:
                return 'SELL'
        
        return 'HOLD'
    
    def execute_trade(
        self,
        signal: str,
        price: float,
        sentiment: float,
        timestamp: datetime
    ) -> Optional[Dict]:
        """
        Execute a trade based on signal.
        
        Args:
            signal: Trading signal ('BUY', 'SELL', 'HOLD')
            price: Current price
            sentiment: Sentiment score
            timestamp: Trade timestamp
            
        Returns:
            Trade details or None if no trade executed
        """
        if signal == 'BUY' and self.cash > 0:
            # Calculate number of shares to buy
            trade_amount = self.cash * self.position_size
            shares = trade_amount / price
            
            # Execute buy
            self.holdings += shares
            self.cash -= trade_amount
            
            trade = {
                'timestamp': timestamp,
                'action': 'BUY',
                'price': price,
                'shares': shares,
                'amount': trade_amount,
                'sentiment': sentiment,
                'cash_after': self.cash,
                'holdings_after': self.holdings
            }
            
            self.trades.append(trade)
            logger.info(f"BUY: {shares:.4f} shares @ ${price:.2f} (sentiment: {sentiment:.3f})")
            return trade
            
        elif signal == 'SELL' and self.holdings > 0:
            # Sell all holdings
            shares = self.holdings
            trade_amount = shares * price
            
            # Execute sell
            self.cash += trade_amount
            self.holdings = 0
            
            trade = {
                'timestamp': timestamp,
                'action': 'SELL',
                'price': price,
                'shares': shares,
                'amount': trade_amount,
                'sentiment': sentiment,
                'cash_after': self.cash,
                'holdings_after': self.holdings
            }
            
            self.trades.append(trade)
            logger.info(f"SELL: {shares:.4f} shares @ ${price:.2f} (sentiment: {sentiment:.3f})")
            return trade
        
        return None
    
    def update_portfolio_value(self, current_price: float):
        """
        Update portfolio value based on current price.
        
        Args:
            current_price: Current asset price
        """
        self.portfolio_value = self.cash + (self.holdings * current_price)
    
    def get_portfolio_state(self, current_price: float) -> Dict:
        """
        Get current portfolio state.
        
        Args:
            current_price: Current asset price
            
        Returns:
            Dictionary with portfolio details
        """
        self.update_portfolio_value(current_price)
        
        return {
            'cash': self.cash,
            'holdings': self.holdings,
            'portfolio_value': self.portfolio_value,
            'total_return': (self.portfolio_value - self.initial_capital) / self.initial_capital,
            'total_trades': len(self.trades)
        }
    
    def reset(self):
        """Reset strategy to initial state."""
        self.cash = self.initial_capital
        self.holdings = 0
        self.portfolio_value = self.initial_capital
        self.trades = []
        logger.info("Strategy reset to initial state")
