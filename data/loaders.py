import pandas as pd
import yfinance as yf


def load_prices_from_yfinance(
    ticker: str,
    start: str,
    end: str,
    price_col: str = "Adj Close",
) -> pd.Series:
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)

    if df.empty:
        raise ValueError(f"No data returned for ticker={ticker}")

    if price_col not in df.columns:
        raise ValueError(f"{price_col} column not found in downloaded data.")

    prices = df[price_col].dropna().astype(float)
    prices.index = pd.to_datetime(prices.index)
    prices = prices.sort_index()
    prices.name = f"{ticker}_price"
    return prices