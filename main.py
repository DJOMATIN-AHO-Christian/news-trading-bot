"""Main entry point for the trading bot."""
import argparse
import sys
import logging
from config import Config
from backtester import Backtester
from news_analyzer import NewsAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_backtest_cli(args):
    """Run backtest from command line."""
    try:
        # Validate configuration
        Config.validate()
        
        logger.info("="*60)
        logger.info("NEWS-BASED ALGORITHMIC TRADING BOT")
        logger.info("="*60)
        
        # Initialize backtester
        backtester = Backtester()
        
        # Run backtest
        results = backtester.run_backtest(
            symbol=args.symbol,
            days=args.days,
            initial_capital=args.capital
        )
        
        # Display results
        print("\n" + "="*60)
        print("BACKTEST RESULTS")
        print("="*60)
        print(f"Symbol: {results['symbol']}")
        print(f"Period: {args.days} days")
        print(f"Initial Capital: ${args.capital:,.2f}")
        print("\nPERFORMANCE METRICS:")
        print("-"*60)
        
        metrics = results['metrics']
        print(f"Strategy Return:      {metrics['strategy_return']:>10.2%}")
        print(f"Buy & Hold Return:    {metrics['buy_hold_return']:>10.2%}")
        print(f"Outperformance:       {metrics['outperformance']:>10.2%}")
        print(f"Sharpe Ratio:         {metrics['strategy_sharpe']:>10.2f}")
        print(f"Max Drawdown:         {metrics['max_drawdown']:>10.2%}")
        print(f"Win Rate:             {metrics['win_rate']:>10.1%}")
        print(f"Total Trades:         {metrics['total_trades']:>10}")
        print(f"\nFinal Portfolio Value: ${metrics['final_portfolio_value']:,.2f}")
        print(f"Final Buy & Hold Value: ${metrics['final_buy_hold_value']:,.2f}")
        print("="*60)
        
        # Show recent trades
        if results['trades']:
            print("\nRECENT TRADES (Last 5):")
            print("-"*60)
            for trade in results['trades'][-5:]:
                print(f"{trade['timestamp'].strftime('%Y-%m-%d')} | "
                      f"{trade['action']:4} | "
                      f"${trade['price']:8.2f} | "
                      f"Shares: {trade['shares']:8.4f} | "
                      f"Sentiment: {trade['sentiment']:6.3f}")
        
        print("\n✓ Backtest complete! Run 'python dashboard.py' to visualize results.")
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Error: {e}")
        print("\nPlease set up your .env file with required API keys.")
        print("Copy .env.example to .env and add your NewsAPI key.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running backtest: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def launch_dashboard():
    """Launch the interactive dashboard."""
    try:
        Config.validate()
        logger.info("Launching dashboard...")
        
        # Import and run dashboard
        from dashboard import app
        app.run_server(
            debug=False,
            host=Config.DASHBOARD_HOST,
            port=Config.DASHBOARD_PORT
        )
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Error: {e}")
        print("\nPlease set up your .env file with required API keys.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error launching dashboard: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='News-Based Algorithmic Trading Bot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run backtest for Apple stock over 90 days
  python main.py --backtest --symbol AAPL --days 90
  
  # Run backtest with custom capital
  python main.py --backtest --symbol TSLA --days 60 --capital 50000
  
  # Launch interactive dashboard
  python main.py --dashboard
        """
    )
    
    parser.add_argument(
        '--backtest',
        action='store_true',
        help='Run backtest mode'
    )
    
    parser.add_argument(
        '--dashboard',
        action='store_true',
        help='Launch interactive dashboard'
    )
    
    parser.add_argument(
        '--symbol',
        type=str,
        default=Config.DEFAULT_SYMBOL,
        help=f'Stock symbol to trade (default: {Config.DEFAULT_SYMBOL})'
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=Config.BACKTEST_DAYS,
        help=f'Number of days to backtest (default: {Config.BACKTEST_DAYS})'
    )
    
    parser.add_argument(
        '--capital',
        type=float,
        default=Config.INITIAL_CAPITAL,
        help=f'Initial capital (default: ${Config.INITIAL_CAPITAL:,.0f})'
    )
    
    args = parser.parse_args()
    
    # Determine mode
    if args.dashboard:
        launch_dashboard()
    elif args.backtest:
        run_backtest_cli(args)
    else:
        parser.print_help()
        print("\n💡 Tip: Use --backtest to run a backtest or --dashboard to launch the UI")


if __name__ == '__main__':
    main()
