import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

# ── CONFIGURATION ──────────────────────────────
TICKERS = ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN"]
START   = "2023-01-01"
END     = "2025-01-01"

# ── DOWNLOAD & CLEAN DATA ──────────────────────
print("Downloading stock data...")
data  = yf.download(TICKERS, start=START, end=END, auto_adjust=True, progress=False)
close = data["Close"]
close.ffill(inplace=True)
print(f"Downloaded {len(close)} trading days!")
print(close.head())
print(close.isnull().sum())

# ── DAILY RETURNS(DT) ──────────────────────────────
daily_return = close.pct_change() * 100

# ── FUNC ──────────────────────────────────
def plot_stock(ticker):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=close.index, y=close[ticker],
                             name=f"{ticker} Price",
                             line=dict(color="royalblue", width=2)))

    fig.add_trace(go.Scatter(x=close.index, y=close[ticker].rolling(20).mean(),
                             name="MA20",
                             line=dict(color="orange", dash="dash")))

    fig.add_trace(go.Scatter(x=close.index, y=close[ticker].rolling(50).mean(),
                             name="MA50",
                             line=dict(color="red", dash="dot")))

    fig.update_layout(
        title=f"{ticker} — Price vs Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        template="plotly_dark"
    )
    fig.show()

def plot_volatility(ticker):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=close.index,
                             y=daily_return[ticker].rolling(20).std(),
                             name=f"{ticker}",
                             line=dict(color="red", width=2)))

    for other in TICKERS:
        if other != ticker:
            fig.add_trace(go.Scatter(x=close.index,
                                     y=daily_return[other].rolling(20).std(),
                                     name=other,
                                     line=dict(dash="dash"),
                                     opacity=0.5))

    fig.update_layout(
        title=f"{ticker} Volatility vs All Stocks",
        xaxis_title="Date",
        yaxis_title="Volatility (%)",
        hovermode="x unified",
        template="plotly_dark"
    )
    fig.show()

    print(f"\n📊 Volatility Comparison:")
    for t in TICKERS:
        avg = daily_return[t].rolling(20).std().mean()
        tag = "  ← you selected" if t == ticker else ""
        print(f"  {t:6s}  →  {avg:.2f}%{tag}")

# ── RUN ────────────────────────────────────────
ticker_input = input("Enter stock name (AAPL / TSLA / GOOGL / MSFT / AMZN): ").upper()
plot_stock(ticker_input)
plot_volatility(ticker_input)