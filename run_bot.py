"""Lancement du bot avec la clé API configurée."""
import os

# Configuration de la clé API
os.environ['NEWS_API_KEY'] = '775a6f27d15a4c86841a0558433c1687'

print("=" * 70)
print("  🚀 BOT DE TRADING ACTIVÉ - MODE RÉEL")
print("=" * 70)
print()
print("  ✅ Clé NewsAPI configurée")
print("  ✅ Analyse de sentiment activée")
print("  ✅ Données de marché en temps réel")
print()
print("  Lancement du backtest sur AAPL (30 jours)...")
print("=" * 70)
print()

# Lancer le backtest
from backtester import Backtester
from market_data import MarketData

backtester = Backtester()
results = backtester.run_backtest('AAPL', days=30, initial_capital=10000)

# Afficher les résultats
print()
print("=" * 70)
print("  📊 RÉSULTATS DU BACKTEST")
print("=" * 70)
print()

metrics = results['metrics']

print(f"  Symbole: AAPL")
print(f"  Période: 30 jours")
print(f"  Capital initial: $10,000")
print()
print("  MÉTRIQUES DE PERFORMANCE:")
print("  " + "-" * 66)
print(f"  Strategy Return:        {metrics['strategy_return']:>10.2%}")
print(f"  Buy & Hold Return:      {metrics['buy_hold_return']:>10.2%}")
print(f"  Outperformance:         {metrics['outperformance']:>10.2%}")
print()
print(f"  Sharpe Ratio:           {metrics['strategy_sharpe']:>10.2f}")
print(f"  Max Drawdown:           {metrics['max_drawdown']:>10.2%}")
print(f"  Win Rate:               {metrics['win_rate']:>10.1%}")
print(f"  Total Trades:           {metrics['total_trades']:>10}")
print()
print(f"  Valeur finale:          ${metrics['final_portfolio_value']:>10,.2f}")
print()
print("=" * 70)

if metrics['outperformance'] > 0:
    print(f"  ✅ La stratégie SURPERFORME le Buy & Hold de {metrics['outperformance']:.2%}!")
else:
    print(f"  ⚠️  La stratégie SOUS-PERFORME le Buy & Hold de {abs(metrics['outperformance']):.2%}")

print()
print("  💡 Prochaines étapes:")
print("     1. Lancez le dashboard: python start_dashboard.py")
print("     2. Testez d'autres actifs: TSLA, BTC-USD, etc.")
print("     3. Ajustez les paramètres dans .env.production")
print()
print("=" * 70)
