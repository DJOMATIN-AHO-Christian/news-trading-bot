"""Interactive dashboard for visualizing trading bot performance."""
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import logging
from backtester import Backtester
from news_analyzer import NewsAnalyzer
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Dash app with modern theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True
)

# Popular symbols for dropdown
SYMBOLS = [
    'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 
    'META', 'NVDA', 'BTC-USD', 'ETH-USD'
]

# Global state
backtester = Backtester()
news_analyzer = None
current_results = None


def create_layout():
    """Create the dashboard layout."""
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("📈 News-Based Trading Bot", className="text-center mb-2"),
                html.P(
                    "Algorithmic trading powered by sentiment analysis",
                    className="text-center text-muted mb-4"
                )
            ])
        ]),
        
        # Controls
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Select Asset", className="fw-bold"),
                                dcc.Dropdown(
                                    id='symbol-dropdown',
                                    options=[{'label': s, 'value': s} for s in SYMBOLS],
                                    value='AAPL',
                                    clearable=False,
                                    className="mb-3"
                                )
                            ], md=4),
                            dbc.Col([
                                html.Label("Backtest Period (days)", className="fw-bold"),
                                dcc.Input(
                                    id='days-input',
                                    type='number',
                                    value=90,
                                    min=30,
                                    max=365,
                                    className="form-control mb-3"
                                )
                            ], md=4),
                            dbc.Col([
                                html.Label("Initial Capital ($)", className="fw-bold"),
                                dcc.Input(
                                    id='capital-input',
                                    type='number',
                                    value=10000,
                                    min=1000,
                                    max=1000000,
                                    className="form-control mb-3"
                                )
                            ], md=4)
                        ]),
                        dbc.Button(
                            "Run Backtest",
                            id='run-button',
                            color="primary",
                            size="lg",
                            className="w-100"
                        )
                    ])
                ], className="mb-4")
            ])
        ]),
        
        # Loading spinner
        dcc.Loading(
            id="loading",
            type="default",
            children=[
                # Performance metrics cards
                html.Div(id='metrics-cards', className="mb-4"),
                
                # Main chart
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Portfolio Performance")),
                            dbc.CardBody([
                                dcc.Graph(id='performance-chart', config={'displayModeBar': False})
                            ])
                        ])
                    ])
                ], className="mb-4"),
                
                # Sentiment and signals chart
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader(html.H4("Sentiment & Trading Signals")),
                            dbc.CardBody([
                                dcc.Graph(id='sentiment-chart', config={'displayModeBar': False})
                            ])
                        ])
                    ])
                ], className="mb-4"),
                
                # Recent news
                html.Div(id='news-section')
            ]
        )
    ], fluid=True, className="p-4")


def create_metrics_cards(metrics):
    """Create performance metrics cards."""
    if not metrics:
        return html.Div()
    
    cards = [
        {
            'title': 'Strategy Return',
            'value': f"{metrics['strategy_return']:.2%}",
            'color': 'success' if metrics['strategy_return'] > 0 else 'danger'
        },
        {
            'title': 'Buy & Hold Return',
            'value': f"{metrics['buy_hold_return']:.2%}",
            'color': 'info'
        },
        {
            'title': 'Outperformance',
            'value': f"{metrics['outperformance']:.2%}",
            'color': 'success' if metrics['outperformance'] > 0 else 'danger'
        },
        {
            'title': 'Sharpe Ratio',
            'value': f"{metrics['strategy_sharpe']:.2f}",
            'color': 'primary'
        },
        {
            'title': 'Max Drawdown',
            'value': f"{metrics['max_drawdown']:.2%}",
            'color': 'warning'
        },
        {
            'title': 'Win Rate',
            'value': f"{metrics['win_rate']:.1%}",
            'color': 'success'
        },
        {
            'title': 'Total Trades',
            'value': f"{metrics['total_trades']}",
            'color': 'secondary'
        },
        {
            'title': 'Final Value',
            'value': f"${metrics['final_portfolio_value']:,.0f}",
            'color': 'primary'
        }
    ]
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6(card['title'], className="text-muted mb-2"),
                    html.H3(card['value'], className=f"text-{card['color']}")
                ])
            ], className="text-center")
        ], md=3, sm=6, className="mb-3")
        for card in cards
    ])


def create_performance_chart(results_df):
    """Create portfolio performance comparison chart."""
    if results_df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Strategy performance
    fig.add_trace(go.Scatter(
        x=results_df['date'],
        y=results_df['portfolio_value'],
        name='Strategy',
        line=dict(color='#00d4ff', width=3),
        hovertemplate='<b>Strategy</b><br>Value: $%{y:,.2f}<br>Date: %{x}<extra></extra>'
    ))
    
    # Buy & Hold performance
    fig.add_trace(go.Scatter(
        x=results_df['date'],
        y=results_df['buy_hold_value'],
        name='Buy & Hold',
        line=dict(color='#ff6b6b', width=2, dash='dash'),
        hovertemplate='<b>Buy & Hold</b><br>Value: $%{y:,.2f}<br>Date: %{x}<extra></extra>'
    ))
    
    # Add buy/sell markers
    buy_signals = results_df[results_df['signal'] == 'BUY']
    sell_signals = results_df[results_df['signal'] == 'SELL']
    
    if not buy_signals.empty:
        fig.add_trace(go.Scatter(
            x=buy_signals['date'],
            y=buy_signals['portfolio_value'],
            mode='markers',
            name='Buy Signal',
            marker=dict(color='#00ff00', size=12, symbol='triangle-up'),
            hovertemplate='<b>BUY</b><br>Price: $%{customdata:.2f}<extra></extra>',
            customdata=buy_signals['price']
        ))
    
    if not sell_signals.empty:
        fig.add_trace(go.Scatter(
            x=sell_signals['date'],
            y=sell_signals['portfolio_value'],
            mode='markers',
            name='Sell Signal',
            marker=dict(color='#ff0000', size=12, symbol='triangle-down'),
            hovertemplate='<b>SELL</b><br>Price: $%{customdata:.2f}<extra></extra>',
            customdata=sell_signals['price']
        ))
    
    fig.update_layout(
        template='plotly_dark',
        hovermode='x unified',
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis_title='Date',
        yaxis_title='Portfolio Value ($)'
    )
    
    return fig


def create_sentiment_chart(results_df):
    """Create sentiment timeline with price overlay."""
    if results_df.empty:
        return go.Figure()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Sentiment Score', 'Asset Price'),
        row_heights=[0.4, 0.6]
    )
    
    # Sentiment score
    colors = ['#00ff00' if s > 0 else '#ff0000' for s in results_df['sentiment']]
    fig.add_trace(
        go.Bar(
            x=results_df['date'],
            y=results_df['sentiment'],
            name='Sentiment',
            marker_color=colors,
            hovertemplate='Sentiment: %{y:.3f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Price
    fig.add_trace(
        go.Scatter(
            x=results_df['date'],
            y=results_df['price'],
            name='Price',
            line=dict(color='#00d4ff', width=2),
            hovertemplate='Price: $%{y:.2f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Add threshold lines
    fig.add_hline(y=0.5, line_dash='dash', line_color='green', opacity=0.5, row=1, col=1)
    fig.add_hline(y=-0.5, line_dash='dash', line_color='red', opacity=0.5, row=1, col=1)
    
    fig.update_layout(
        template='plotly_dark',
        height=600,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    
    fig.update_yaxes(title_text='Sentiment', row=1, col=1)
    fig.update_yaxes(title_text='Price ($)', row=2, col=1)
    fig.update_xaxes(title_text='Date', row=2, col=1)
    
    return fig


@app.callback(
    [Output('metrics-cards', 'children'),
     Output('performance-chart', 'figure'),
     Output('sentiment-chart', 'figure'),
     Output('news-section', 'children')],
    [Input('run-button', 'n_clicks')],
    [State('symbol-dropdown', 'value'),
     State('days-input', 'value'),
     State('capital-input', 'value')]
)
def run_backtest(n_clicks, symbol, days, capital):
    """Run backtest and update all visualizations."""
    global current_results, news_analyzer
    
    if n_clicks is None:
        return html.Div(), go.Figure(), go.Figure(), html.Div()
    
    try:
        logger.info(f"Running backtest: {symbol}, {days} days, ${capital}")
        
        # Run backtest
        results = backtester.run_backtest(symbol, days, capital)
        current_results = results
        
        # Create visualizations
        metrics_cards = create_metrics_cards(results['metrics'])
        performance_chart = create_performance_chart(results['results'])
        sentiment_chart = create_sentiment_chart(results['results'])
        
        # Get recent news
        if news_analyzer is None:
            news_analyzer = NewsAnalyzer()
        
        news_data = news_analyzer.get_aggregated_sentiment(symbol, days=1)
        news_section = create_news_section(news_data)
        
        return metrics_cards, performance_chart, sentiment_chart, news_section
        
    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        error_msg = dbc.Alert(f"Error: {str(e)}", color="danger")
        return error_msg, go.Figure(), go.Figure(), html.Div()


def create_news_section(news_data):
    """Create recent news section."""
    if not news_data or not news_data.get('articles'):
        return html.Div()
    
    articles = news_data['articles'][:5]  # Top 5 articles
    
    return dbc.Card([
        dbc.CardHeader(html.H4("Recent News & Sentiment")),
        dbc.CardBody([
            dbc.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Headline"),
                        html.Th("Sentiment", className="text-center"),
                        html.Th("Published", className="text-center")
                    ])
                ]),
                html.Tbody([
                    html.Tr([
                        html.Td([
                            html.A(
                                article['title'],
                                href=article['url'],
                                target='_blank',
                                className="text-decoration-none"
                            )
                        ]),
                        html.Td(
                            f"{article['sentiment']:.3f}",
                            className=f"text-center text-{'success' if article['sentiment'] > 0 else 'danger'}"
                        ),
                        html.Td(
                            article['published_at'][:10] if article['published_at'] else 'N/A',
                            className="text-center text-muted"
                        )
                    ])
                    for article in articles
                ])
            ], striped=True, hover=True, responsive=True)
        ])
    ])


# Set layout
app.layout = create_layout()


if __name__ == '__main__':
    logger.info(f"Starting dashboard on {Config.DASHBOARD_HOST}:{Config.DASHBOARD_PORT}")
    app.run_server(
        debug=True,
        host=Config.DASHBOARD_HOST,
        port=Config.DASHBOARD_PORT
    )
