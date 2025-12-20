// API Configuration
const API_BASE = 'http://localhost:5000/api';

// Chart instances
let performanceChart = null;
let sentimentChart = null;

// DOM Elements
const runBacktestBtn = document.getElementById('runBacktest');
const loading = document.getElementById('loading');
const metricsSection = document.getElementById('metricsSection');
const chartsSection = document.getElementById('chartsSection');

// Event Listeners
runBacktestBtn.addEventListener('click', runBacktest);

// Run Backtest
async function runBacktest() {
    const symbol = document.getElementById('symbol').value;
    const days = document.getElementById('days').value;
    const capital = document.getElementById('capital').value;

    // Show loading
    loading.classList.remove('hidden');
    metricsSection.classList.add('hidden');
    chartsSection.classList.add('hidden');

    try {
        const response = await fetch(`${API_BASE}/backtest/${symbol}?days=${days}&capital=${capital}`);
        const result = await response.json();

        if (result.success) {
            // Hide loading
            loading.classList.add('hidden');
            
            // Update metrics
            updateMetrics(result.metrics);
            
            // Update charts
            updatePerformanceChart(result.data, symbol);
            updateSentimentChart(result.data, symbol);
            
            // Update trades table
            updateTradesTable(result.data);
            
            // Show results
            metricsSection.classList.remove('hidden');
            chartsSection.classList.remove('hidden');
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        loading.classList.add('hidden');
        alert('Error running backtest: ' + error.message);
        console.error(error);
    }
}

// Update Metrics Cards
function updateMetrics(metrics) {
    // Strategy Return
    const strategyReturn = document.getElementById('strategyReturn');
    strategyReturn.textContent = formatPercent(metrics.strategy_return);
    strategyReturn.className = 'metric-value ' + (metrics.strategy_return >= 0 ? 'positive' : 'negative');

    // Buy & Hold Return
    const buyHoldReturn = document.getElementById('buyHoldReturn');
    buyHoldReturn.textContent = formatPercent(metrics.buy_hold_return);
    buyHoldReturn.className = 'metric-value ' + (metrics.buy_hold_return >= 0 ? 'positive' : 'negative');

    // Outperformance
    const outperformance = document.getElementById('outperformance');
    outperformance.textContent = formatPercent(metrics.outperformance);
    outperformance.className = 'metric-value ' + (metrics.outperformance >= 0 ? 'positive' : 'negative');

    // Sharpe Ratio
    document.getElementById('sharpeRatio').textContent = metrics.strategy_sharpe.toFixed(2);

    // Max Drawdown
    const maxDrawdown = document.getElementById('maxDrawdown');
    maxDrawdown.textContent = formatPercent(metrics.max_drawdown);
    maxDrawdown.className = 'metric-value negative';

    // Win Rate
    document.getElementById('winRate').textContent = formatPercent(metrics.win_rate);

    // Total Trades
    document.getElementById('totalTrades').textContent = metrics.total_trades;

    // Final Value
    document.getElementById('finalValue').textContent = formatCurrency(metrics.final_portfolio_value);
}

// Update Performance Chart
function updatePerformanceChart(data, symbol) {
    const ctx = document.getElementById('performanceChart').getContext('2d');

    // Prepare data
    const dates = data.map(d => new Date(d.date).toLocaleDateString());
    const strategyValues = data.map(d => d.portfolio_value);
    const buyHoldValues = data.map(d => d.buy_hold_value);

    // Find buy/sell signals
    const buySignals = data.filter(d => d.signal === 'BUY');
    const sellSignals = data.filter(d => d.signal === 'SELL');

    // Destroy existing chart
    if (performanceChart) {
        performanceChart.destroy();
    }

    // Create new chart
    performanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Strategy',
                    data: strategyValues,
                    borderColor: '#00d4ff',
                    backgroundColor: 'rgba(0, 212, 255, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6
                },
                {
                    label: 'Buy & Hold',
                    data: buyHoldValues,
                    borderColor: '#ff4757',
                    backgroundColor: 'rgba(255, 71, 87, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 6
                },
                {
                    label: 'Buy Signal',
                    data: buySignals.map(s => ({
                        x: new Date(s.date).toLocaleDateString(),
                        y: s.portfolio_value
                    })),
                    backgroundColor: '#00ff88',
                    borderColor: '#00ff88',
                    pointStyle: 'triangle',
                    pointRadius: 8,
                    pointHoverRadius: 10,
                    showLine: false
                },
                {
                    label: 'Sell Signal',
                    data: sellSignals.map(s => ({
                        x: new Date(s.date).toLocaleDateString(),
                        y: s.portfolio_value
                    })),
                    backgroundColor: '#ff4757',
                    borderColor: '#ff4757',
                    pointStyle: 'triangle',
                    pointRotation: 180,
                    pointRadius: 8,
                    pointHoverRadius: 10,
                    showLine: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#a0a8c5',
                        font: {
                            size: 12
                        },
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: '#1a2142',
                    titleColor: '#ffffff',
                    bodyColor: '#a0a8c5',
                    borderColor: '#00d4ff',
                    borderWidth: 1,
                    padding: 12,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += formatCurrency(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#6c7293',
                        maxTicksLimit: 10
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#6c7293',
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

// Update Sentiment Chart
function updateSentimentChart(data, symbol) {
    const ctx = document.getElementById('sentimentChart').getContext('2d');

    // Prepare data
    const dates = data.map(d => new Date(d.date).toLocaleDateString());
    const sentiments = data.map(d => d.sentiment);
    const prices = data.map(d => d.price);

    // Color sentiments
    const sentimentColors = sentiments.map(s => s > 0 ? '#00ff88' : '#ff4757');

    // Destroy existing chart
    if (sentimentChart) {
        sentimentChart.destroy();
    }

    // Create new chart
    sentimentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Sentiment Score',
                    data: sentiments,
                    backgroundColor: sentimentColors,
                    borderColor: sentimentColors,
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: 'Price',
                    data: prices,
                    type: 'line',
                    borderColor: '#a29bfe',
                    backgroundColor: 'rgba(162, 155, 254, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#a0a8c5',
                        font: {
                            size: 12
                        },
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: '#1a2142',
                    titleColor: '#ffffff',
                    bodyColor: '#a0a8c5',
                    borderColor: '#00d4ff',
                    borderWidth: 1,
                    padding: 12
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#6c7293',
                        maxTicksLimit: 10
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Sentiment',
                        color: '#a0a8c5'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#6c7293'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Price ($)',
                        color: '#a0a8c5'
                    },
                    grid: {
                        drawOnChartArea: false
                    },
                    ticks: {
                        color: '#6c7293',
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

// Update Trades Table
function updateTradesTable(data) {
    const tbody = document.getElementById('tradesBody');
    tbody.innerHTML = '';

    // Get trades (filter for BUY/SELL signals)
    const trades = data.filter(d => d.signal === 'BUY' || d.signal === 'SELL');
    
    // Show last 10 trades
    const recentTrades = trades.slice(-10).reverse();

    recentTrades.forEach(trade => {
        const row = document.createElement('tr');
        
        const date = new Date(trade.date).toLocaleDateString();
        const action = trade.signal;
        const price = trade.price;
        const shares = trade.holdings || 0;
        const amount = price * shares;
        const sentiment = trade.sentiment;

        row.innerHTML = `
            <td>${date}</td>
            <td class="trade-${action.toLowerCase()}">${action === 'BUY' ? '🟢' : '🔴'} ${action}</td>
            <td>${formatCurrency(price)}</td>
            <td>${shares.toFixed(4)}</td>
            <td>${formatCurrency(amount)}</td>
            <td>${sentiment.toFixed(3)}</td>
        `;

        tbody.appendChild(row);
    });
}

// Utility Functions
function formatPercent(value) {
    return (value * 100).toFixed(2) + '%';
}

function formatCurrency(value) {
    return '$' + value.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    console.log('📈 Trading Bot Dashboard Loaded');
    console.log('Ready to run backtests!');
});
