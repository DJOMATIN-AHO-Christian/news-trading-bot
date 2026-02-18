"""News sentiment analysis module using VADER (lightweight, no GPU required).

Replaces the heavy transformers/torch DistilBERT model with VADER,
a rule-based sentiment analyzer optimized for social media and financial text.
- No GPU needed
- No large model downloads (~500KB vs ~1GB)
- Works offline
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from typing import List, Dict
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsAnalyzer:
    """Analyzes financial news sentiment using VADER NLP."""

    def __init__(self):
        """Initialize the news analyzer with API client and VADER sentiment model."""
        self.news_api = NewsApiClient(api_key=Config.NEWS_API_KEY)

        # VADER: lightweight rule-based sentiment analyzer (no GPU, no download)
        logger.info("Loading VADER sentiment analyzer (lightweight, no GPU needed)")
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        # Cache for sentiment results
        self.cache = {}

    def fetch_news(self, symbol: str, days: int = 1) -> List[Dict]:
        """
        Fetch news articles for a given stock symbol.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
            days: Number of days to look back

        Returns:
            List of news articles with title, description, and published date
        """
        try:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days)

            logger.info(f"Fetching news for {symbol} from {from_date.date()} to {to_date.date()}")
            response = self.news_api.get_everything(
                q=f"{symbol} OR {self._get_company_name(symbol)}",
                from_param=from_date.strftime('%Y-%m-%d'),
                to=to_date.strftime('%Y-%m-%d'),
                language='en',
                sort_by='relevancy',
                page_size=100
            )

            articles = response.get('articles', [])
            logger.info(f"Found {len(articles)} articles for {symbol}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []

    def analyze_sentiment(self, text: str) -> float:
        """
        Analyze sentiment of a text using VADER.

        Args:
            text: Text to analyze

        Returns:
            Sentiment score between -1 (negative) and 1 (positive)
        """
        if not text:
            return 0.0

        # Check cache
        if text in self.cache:
            return self.cache[text]

        try:
            # VADER returns a compound score in [-1, 1] directly
            scores = self.sentiment_analyzer.polarity_scores(text)
            sentiment = scores['compound']  # -1 (very negative) to +1 (very positive)

            self.cache[text] = sentiment
            return sentiment

        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return 0.0

    def get_aggregated_sentiment(self, symbol: str, days: int = 1) -> Dict:
        """
        Get aggregated sentiment for a symbol over a time period.

        Args:
            symbol: Stock ticker symbol
            days: Number of days to analyze

        Returns:
            Dictionary with sentiment score, article count, and details
        """
        articles = self.fetch_news(symbol, days)

        if not articles:
            return {
                'symbol': symbol,
                'sentiment': 0.0,
                'article_count': 0,
                'articles': [],
                'timestamp': datetime.now()
            }

        sentiments = []
        analyzed_articles = []

        for article in articles:
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title}. {description}"

            sentiment = self.analyze_sentiment(text)
            sentiments.append(sentiment)

            analyzed_articles.append({
                'title': title,
                'description': description,
                'url': article.get('url', ''),
                'published_at': article.get('publishedAt', ''),
                'sentiment': sentiment
            })

        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
        logger.info(f"Average sentiment for {symbol}: {avg_sentiment:.3f} ({len(articles)} articles)")

        return {
            'symbol': symbol,
            'sentiment': avg_sentiment,
            'article_count': len(articles),
            'articles': analyzed_articles[:10],  # Top 10 articles
            'timestamp': datetime.now()
        }

    def _get_company_name(self, symbol: str) -> str:
        """Map stock symbols to company names for better news search."""
        symbol_map = {
            'AAPL': 'Apple',
            'GOOGL': 'Google',
            'MSFT': 'Microsoft',
            'AMZN': 'Amazon',
            'TSLA': 'Tesla',
            'META': 'Meta Facebook',
            'NVDA': 'NVIDIA',
            'BTC-USD': 'Bitcoin',
            'ETH-USD': 'Ethereum'
        }
        return symbol_map.get(symbol, symbol)
