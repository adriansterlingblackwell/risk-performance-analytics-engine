from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf

from risk_analytics.data.schemas import MARKET_DATA_SCHEMA, YFINANCE_COLUMN_MAPPING
from risk_analytics.data.validators import validate_market_data


def download_market_data(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Download historical market data for a single ticker from yfinance.

    Parameters
    ----------
    ticker:
        Asset ticker symbol (e.g. 'AAPL').
    start_date:
        Start date in YYYY-MM-DD format.
    end_date:
        End date in YYYY-MM-DD format.
    interval:
        Data interval. Default is '1d'.

    Returns
    -------
    pd.DataFrame
        Raw DataFrame returned by yfinance.
    """
    df = yf.download(
        tickers=ticker,
        start=start_date,
        end=end_date,
        interval=interval,
        progress=False,
        auto_adjust=False,
    )

    if df.empty:
        raise ValueError(
            f"No data returned from yfinance for ticker='{ticker}', "
            f"start_date='{start_date}', end_date='{end_date}', interval='{interval}'."
        )

    return df


def normalize_yfinance_columns(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Normalize yfinance output into the engine's canonical market data schema.
    """
    normalized_df = df.copy()

    if isinstance(normalized_df.columns, pd.MultiIndex):
        normalized_df.columns = normalized_df.columns.get_level_values(0)

    normalized_df = normalized_df.reset_index()
    normalized_df = normalized_df.rename(columns=YFINANCE_COLUMN_MAPPING)

    normalized_df["ticker"] = ticker.upper()

    expected_columns = MARKET_DATA_SCHEMA.all_columns
    available_columns = [col for col in expected_columns if col in normalized_df.columns]

    normalized_df = normalized_df[available_columns]

    return normalized_df


def build_raw_data_filename(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str,
) -> str:
    """
    Build a deterministic raw CSV filename for downloaded market data.
    """
    safe_ticker = ticker.lower().strip()
    return f"{safe_ticker}_{start_date}_{end_date}_{interval}_raw.csv"


def save_raw_csv(
    df: pd.DataFrame,
    output_dir: str | Path,
    filename: str,
) -> Path:
    """
    Save normalized raw market data to CSV.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / filename
    df.to_csv(file_path, index=False)

    return file_path


def load_market_data(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "1d",
    output_dir: str | Path = "data/raw",
) -> pd.DataFrame:
    """
    Download, normalize, validate, and persist single-ticker market data.

    Parameters
    ----------
    ticker:
        Asset ticker symbol.
    start_date:
        Start date in YYYY-MM-DD format.
    end_date:
        End date in YYYY-MM-DD format.
    interval:
        Data interval. Default is '1d'.
    output_dir:
        Directory where raw CSV files will be saved.

    Returns
    -------
    pd.DataFrame
        Normalized and validated market data DataFrame.
    """
    raw_df = download_market_data(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
    )

    normalized_df = normalize_yfinance_columns(df=raw_df, ticker=ticker)

    validate_market_data(normalized_df)

    filename = build_raw_data_filename(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
    )
    save_raw_csv(df=normalized_df, output_dir=output_dir, filename=filename)

    return normalized_df