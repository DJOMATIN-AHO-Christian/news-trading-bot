"""Backtesting engine for trading strategy."""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
import logging
from news_analyzer import NewsAnalyzer
from market_data import MarketData
from trading_strategy import TradingStrategy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Backtester:
    """Backtests trading strategy against historical data."""
    
    def __init__(self):
        """Initialize backtester with required components."""
        self.news_analyzer = None  # Lazy initialization
        self.market_data = MarketData()
    
    def run_backtest(
        self,
        symbol: str,
        days: int = 90,
        initial_capital: float = 10000
    ) -> Dict:
        """
        Run backtest for a symbol over a time period.
        
        Args:
            symbol: Stock ticker symbol
            days: Number of days to backtest
            initial_capital: Starting capital
            
        Returns:
            Dictionary with backtest results
        """
        logger.info(f"Starting backtest for {symbol} over {days} days")
        
        # Initialize strategy
        strategy = TradingStrategy(initial_capital=initial_capital)
        
        # Get historical price data
        price_data = self.market_data.get_price_history(symbol, days=days)
        
        if price_data.empty:
            logger.error("No price data available")
            return self._empty_result(symbol)
        
        # Initialize news analyzer (only when needed)
        if self.news_analyzer is None:
            self.news_analyzer = NewsAnalyzer()
        
        # Prepare results storage
        results = []
        buy_hold_value = initial_capital
        buy_hold_shares = 0
        
        # Get unique dates
        price_data['date'] = pd.to_datetime(price_data['date']).dt.date
        dates = price_data['date'].unique()
        
        logger.info(f"Backtesting over {len(dates)} trading days")
        
        # Simulate Buy & Hold (buy on first day)
        first_price = price_data.iloc[0]['close']
        buy_hold_shares = initial_capital / first_price
        
        # Run backtest day by day
        for i, date in enumerate(dates):
            # Get price for this date
            day_data = price_data[price_data['date'] == date]
            if day_data.empty:
                continue
            
            current_price = day_data.iloc[0]['close']
            timestamp = pd.to_datetime(day_data.iloc[0]['date'])
            
            # Get sentiment for this date (simulate with mock data for demo)
            # In production, you'd fetch historical news for each date
            sentiment = self._get_sentiment_for_date(symbol, date, i, len(dates))
            
            # Generate signal
            signal = strategy.generate_signal(sentiment, current_price)
            
            # Execute trade
            trade = strategy.execute_trade(signal, current_price, sentiment, timestamp)
            
            # Update portfolio value
            portfolio_state = strategy.get_portfolio_state(current_price)
            
            # Calculate Buy & Hold value
            buy_hold_value = buy_hold_shares * current_price
            
            # Store results
            results.append({
                'date': timestamp,
                'price': current_price,
                'sentiment': sentiment,
                'signal': signal,
                'portfolio_value': portfolio_state['portfolio_value'],
                'buy_hold_value': buy_hold_value,
                'cash': portfolio_state['cash'],
                'holdings': portfolio_state['holdings'],
                'trade': trade
            })
        
        # Convert to DataFrame
        results_df = pd.DataFrame(results)
        
        # Calculate performance metrics
        metrics = self._calculate_metrics(results_df, strategy, initial_capital)
        
        logger.info(f"Backtest complete. Strategy return: {metrics['strategy_return']:.2%}, "
                   f"Buy & Hold return: {metrics['buy_hold_return']:.2%}")
        
        return {
            'symbol': symbol,
            'results': results_df,
            'metrics': metrics,
            'trades': strategy.trades,
            'initial_capital': initial_capital
        }
    
    def _get_sentiment_for_date(
        self,
        symbol: str,
        date,
        day_index: int,
        total_days: int
    ) -> float:
        """
        Get sentiment for a specific date.
        For demo purposes, this generates realistic sentiment patterns.
        In production, you'd fetch actual historical news.
        
        Args:
            symbol: Stock ticker
            date: Date to get sentiment for
            day_index: Index of current day
            total_days: Total number of days
            
        Returns:
            Sentiment score
        """
        # Generate realistic sentiment pattern with some randomness
        # This simulates news sentiment cycles
        np.random.seed(hash(str(date)) % 2**32)
        
        # Base trend
        trend = np.sin(day_index / total_days * 4 * np.pi) * 0.3
        
        # Random noise
        noise = np.random.normal(0, 0.3)
        
        # Occasional strong signals
        if np.random.random() < 0.1:  # 10% chance of strong signal
            noise += np.random.choice([-0.5, 0.5])
        
        sentiment = np.clip(trend + noise, -1, 1)
        
        return sentiment
    
    def _calculate_metrics(
        self,
        results_df: pd.DataFrame,
        strategy: TradingStrategy,
        initial_capital: float
    ) -> Dict:
        """Calculate performance metrics."""
        if results_df.empty:
            return {}
        
        final_portfolio = results_df.iloc[-1]['portfolio_value']
        final_buy_hold = results_df.iloc[-1]['buy_hold_value']
        
        # Returns
        strategy_return = (final_portfolio - initial_capital) / initial_capital
        buy_hold_return = (final_buy_hold - initial_capital) / initial_capital
        
        # Calculate daily returns for Sharpe ratio
        results_df['strategy_returns'] = results_df['portfolio_value'].pct_change()
        results_df['buy_hold_returns'] = results_df['buy_hold_value'].pct_change()
        
        # Sharpe ratio (assuming 252 trading days, 0% risk-free rate)
        strategy_sharpe = (
            results_df['strategy_returns'].mean() / results_df['strategy_returns'].std() * np.sqrt(252)
            if results_df['strategy_returns'].std() > 0 else 0
        )
        
        buy_hold_sharpe = (
            results_df['buy_hold_returns'].mean() / results_df['buy_hold_returns'].std() * np.sqrt(252)
            if results_df['buy_hold_returns'].std() > 0 else 0
        )
        
        # Max drawdown
        strategy_cummax = results_df['portfolio_value'].cummax()
        strategy_drawdown = (results_df['portfolio_value'] - strategy_cummax) / strategy_cummax
        max_drawdown = strategy_drawdown.min()
        
        # Win rate
        winning_trades = [t for t in strategy.trades if self._is_winning_trade(t, strategy.trades)]
        win_rate = len(winning_trades) / len(strategy.trades) if strategy.trades else 0
        
        return {
            'strategy_return': strategy_return,
            'buy_hold_return': buy_hold_return,
            'outperformance': strategy_return - buy_hold_return,
            'strategy_sharpe': strategy_sharpe,
            'buy_hold_sharpe': buy_hold_sharpe,
            'max_drawdown': max_drawdown,
            'total_trades': len(strategy.trades),
            'win_rate': win_rate,
            'final_portfolio_value': final_portfolio,
            'final_buy_hold_value': final_buy_hold
        }
    
    def _is_winning_trade(self, trade: Dict, all_trades: List[Dict]) -> bool:
        """Determine if a trade was profitable."""
        if trade['action'] != 'SELL':
            return False
        
        # Find the corresponding buy trade
        for prev_trade in reversed(all_trades):
            if prev_trade['timestamp'] < trade['timestamp'] and prev_trade['action'] == 'BUY':
                return trade['price'] > prev_trade['price']
        
        return False
    
    def _empty_result(self, symbol: str) -> Dict:
        """Return empty result structure."""
        return {
            'symbol': symbol,
            'results': pd.DataFrame(),
            'metrics': {},
            'trades': [],
            'initial_capital': 0
        }
