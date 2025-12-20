# 🚀 Guide de Configuration - Bot Fonctionnel

## 📋 Étapes pour Rendre le Bot Fonctionnel

### 1️⃣ Obtenir une Clé API NewsAPI (GRATUIT)

#### Inscription
1. Allez sur **https://newsapi.org/register**
2. Remplissez le formulaire :
   - Prénom et Nom
   - Email
   - Mot de passe
3. Cliquez sur "Submit"
4. Vérifiez votre email et confirmez votre compte

#### Récupérer votre Clé
1. Connectez-vous sur https://newsapi.org/account
2. Copiez votre **API Key** (elle ressemble à : `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

**Plan Gratuit :**
- ✅ 100 requêtes par jour
- ✅ Accès aux nouvelles des 30 derniers jours
- ✅ Parfait pour tester et apprendre
- ✅ Pas de carte bancaire requise

---

### 2️⃣ Configurer le Bot

#### Option A : Fichier .env (Recommandé)

1. **Créez le fichier `.env`** dans le dossier du projet :
```bash
cd C:\Users\hp\.gemini\antigravity\scratch\news-trading-bot
copy .env.example .env
```

2. **Éditez le fichier `.env`** avec Notepad :
```bash
notepad .env
```

3. **Remplacez `your_newsapi_key_here` par votre vraie clé** :
```env
# NewsAPI Configuration
NEWS_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

# Trading Strategy Parameters
SENTIMENT_BUY_THRESHOLD=0.5
SENTIMENT_SELL_THRESHOLD=-0.5
INITIAL_CAPITAL=10000
POSITION_SIZE=0.2

# Backtesting Configuration
DEFAULT_SYMBOL=AAPL
BACKTEST_DAYS=90
```

4. **Sauvegardez et fermez**

#### Option B : Variable d'Environnement Windows

```powershell
# Temporaire (session actuelle seulement)
$env:NEWS_API_KEY="votre_clé_ici"

# Permanent (système)
[System.Environment]::SetEnvironmentVariable('NEWS_API_KEY', 'votre_clé_ici', 'User')
```

---

### 3️⃣ Tester le Bot

#### Test 1 : Vérifier la Configuration
```bash
python -c "from config import Config; Config.validate(); print('✓ Configuration OK!')"
```

**Résultat attendu :** `✓ Configuration OK!`

#### Test 2 : Tester l'Analyse de Sentiment
```bash
python -c "from news_analyzer import NewsAnalyzer; na = NewsAnalyzer(); result = na.get_aggregated_sentiment('AAPL', days=1); print(f'Sentiment: {result[\"sentiment\"]:.3f}, Articles: {result[\"article_count\"]}')"
```

**Résultat attendu :** 
```
Sentiment: 0.234, Articles: 15
```

#### Test 3 : Backtest Complet
```bash
python main.py --backtest --symbol AAPL --days 30
```

**Résultat attendu :**
```
============================================================
BACKTEST RESULTS
============================================================
Symbol: AAPL
Period: 30 days
...
```

---

### 4️⃣ Lancer le Dashboard

```bash
python start_dashboard.py
```

Puis ouvrez : **http://localhost:5000**

**Maintenant le bot utilisera :**
- ✅ Vraies nouvelles financières de NewsAPI
- ✅ Analyse de sentiment réelle avec NLP
- ✅ Signaux de trading basés sur le sentiment actuel
- ✅ Données de marché en temps réel via yfinance

---

## 🎯 Fonctionnalités Actives

### Avec la Clé API NewsAPI

| Fonctionnalité | Sans Clé | Avec Clé |
|----------------|----------|----------|
| **Données de marché** | ✅ Réel | ✅ Réel |
| **Sentiment des news** | ❌ Simulé | ✅ Réel |
| **Signaux de trading** | ⚠️ Basique | ✅ Intelligent |
| **Backtesting** | ✅ Fonctionne | ✅ Précis |
| **Dashboard** | ✅ Fonctionne | ✅ Complet |

---

## ⚙️ Personnalisation de la Stratégie

### Modifier les Seuils de Sentiment

Éditez `.env` :
```env
# Plus agressif (trade plus souvent)
SENTIMENT_BUY_THRESHOLD=0.3
SENTIMENT_SELL_THRESHOLD=-0.3

# Plus conservateur (trade moins souvent)
SENTIMENT_BUY_THRESHOLD=0.7
SENTIMENT_SELL_THRESHOLD=-0.7
```

### Modifier la Taille des Positions

```env
# Utiliser 10% du capital par trade (plus prudent)
POSITION_SIZE=0.1

# Utiliser 50% du capital par trade (plus agressif)
POSITION_SIZE=0.5
```

### Changer le Capital Initial

```env
INITIAL_CAPITAL=5000   # Pour débuter
INITIAL_CAPITAL=50000  # Pour tester avec plus
```

---

## 📊 Exemples d'Utilisation

### Backtest sur Apple (30 jours)
```bash
python main.py --backtest --symbol AAPL --days 30
```

### Backtest sur Tesla (60 jours, 20k capital)
```bash
python main.py --backtest --symbol TSLA --days 60 --capital 20000
```

### Backtest sur Bitcoin (90 jours)
```bash
python main.py --backtest --symbol BTC-USD --days 90
```

### Comparer Plusieurs Actifs
```bash
# AAPL
python main.py --backtest --symbol AAPL --days 60

# TSLA
python main.py --backtest --symbol TSLA --days 60

# BTC-USD
python main.py --backtest --symbol BTC-USD --days 60
```

---

## 🔍 Interpréter les Résultats

### Métriques Clés

**Strategy Return** : Rendement de votre stratégie
- Positif = Profit ✅
- Négatif = Perte ❌

**Outperformance** : Différence vs Buy & Hold
- Positif = Votre stratégie bat le marché ✅
- Négatif = Mieux vaut acheter et garder ❌

**Sharpe Ratio** : Rendement ajusté au risque
- > 1.0 = Bon ✅
- > 2.0 = Excellent ✅✅
- < 0 = Mauvais ❌

**Win Rate** : % de trades gagnants
- > 50% = Plus de gagnants que de perdants ✅
- > 60% = Très bon ✅✅

**Max Drawdown** : Perte maximale
- Plus petit = Moins risqué ✅
- > -20% = Risque élevé ⚠️

---

## 🎓 Conseils d'Utilisation

### Pour Débuter
1. Testez avec **AAPL** (stable, beaucoup de news)
2. Utilisez **30-60 jours** pour voir les patterns
3. Capital initial : **$10,000** (standard)
4. Gardez les seuils par défaut (0.5 / -0.5)

### Pour Optimiser
1. Testez différents seuils de sentiment
2. Comparez plusieurs périodes (30j, 60j, 90j)
3. Essayez différents actifs
4. Notez quels paramètres donnent les meilleurs résultats

### Pour Analyser
1. Regardez la corrélation sentiment/prix dans le dashboard
2. Identifiez les faux signaux
3. Vérifiez si les news correspondent aux mouvements
4. Comparez le Sharpe ratio entre actifs

---

## ⚠️ Limites du Plan Gratuit NewsAPI

- **100 requêtes/jour** : Suffisant pour ~10-15 backtests
- **News des 30 derniers jours** : Pas d'historique ancien
- **Pas de trading en temps réel** : Seulement backtesting

**Solution :** Utilisez le bot pour apprendre et tester. Si vous voulez trader réellement, passez au plan payant ou utilisez d'autres sources de news.

---

## 🐛 Dépannage

### Erreur : "NEWS_API_KEY not found"
➡️ Vérifiez que le fichier `.env` existe et contient votre clé

### Erreur : "Invalid API key"
➡️ Vérifiez que vous avez copié la clé complète depuis newsapi.org

### Erreur : "Rate limit exceeded"
➡️ Vous avez dépassé 100 requêtes/jour. Attendez demain ou passez au plan payant

### Pas de nouvelles trouvées
➡️ Normal pour certains actifs peu médiatisés. Essayez AAPL, TSLA, ou BTC-USD

### Sentiment toujours à 0
➡️ Vérifiez votre connexion internet et votre clé API

---

## 📚 Ressources

- **NewsAPI Docs** : https://newsapi.org/docs
- **yfinance Docs** : https://pypi.org/project/yfinance/
- **Transformers (NLP)** : https://huggingface.co/docs/transformers

---

## ✅ Checklist de Configuration

- [ ] Compte NewsAPI créé
- [ ] Clé API récupérée
- [ ] Fichier `.env` créé
- [ ] Clé API ajoutée dans `.env`
- [ ] Test de configuration réussi
- [ ] Test d'analyse de sentiment réussi
- [ ] Premier backtest exécuté
- [ ] Dashboard lancé et testé

---

**Votre bot est maintenant 100% fonctionnel ! 🎉**

Bon trading ! 📈🚀
