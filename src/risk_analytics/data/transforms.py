from __future__ import annotations

from pathlib import Path

import pandas as pd

from risk_analytics.data.schemas import MARKET_DATA_SCHEMA
from risk_analytics.data.validators import validate_market_data


def parse_date_column(df: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    """
    Convert the date column to pandas datetime.
    """
    transformed_df = df.copy()
    transformed_df[date_column] = pd.to_datetime(transformed_df[date_column], errors="raise")
    return transformed_df


def sort_by_date(df: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    """
    Sort the dataset by date in ascending order.
    """
    transformed_df = df.copy()
    transformed_df = transformed_df.sort_values(by=date_column, ascending=True)
    transformed_df = transformed_df.reset_index(drop=True)
    return transformed_df


def drop_duplicate_dates(df: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    """
    Drop duplicate dates, keeping the last occurrence.

    Assumes a single-ticker dataset in the current project stage.
    """
    transformed_df = df.copy()
    transformed_df = transformed_df.drop_duplicates(subset=[date_column], keep="last")
    transformed_df = transformed_df.reset_index(drop=True)
    return transformed_df


def select_price_column(
    df: pd.DataFrame,
    price_column_priority: list[str] | None = None,
) -> str:
    """
    Select the preferred price column for analytics.

    Defaults to schema-defined priority:
    adj_close -> close
    """
    priorities = price_column_priority or MARKET_DATA_SCHEMA.price_column_priority

    for column in priorities:
        if column in df.columns:
            return column

    raise ValueError(
        f"No valid price column found. Expected one of: {priorities}. "
        f"Available columns: {list(df.columns)}"
    )


def build_processed_market_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build an analytics-ready processed market dataset.

    Output columns:
    - date
    - ticker
    - price
    - volume
    """
    transformed_df = df.copy()

    price_column = select_price_column(transformed_df)

    required_output_columns = ["date", "ticker", "volume"]
    missing_columns = [col for col in required_output_columns if col not in transformed_df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns for processed dataset: {missing_columns}"
        )

    processed_df = transformed_df[["date", "ticker", price_column, "volume"]].copy()
    processed_df = processed_df.rename(columns={price_column: "price"})

    return processed_df


def build_processed_data_filename(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str,
) -> str:
    """
    Build a deterministic processed CSV filename.
    """
    safe_ticker = ticker.lower().strip()
    return f"{safe_ticker}_{start_date}_{end_date}_{interval}_processed.csv"


def save_processed_csv(
    df: pd.DataFrame,
    output_dir: str | Path,
    filename: str,
) -> Path:
    """
    Save processed market data to CSV.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / filename
    df.to_csv(file_path, index=False)

    return file_path


def transform_market_data(
    df: pd.DataFrame,
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "1d",
    output_dir: str | Path = "data/processed",
) -> pd.DataFrame:
    """
    Transform raw normalized market data into analytics-ready processed data.

    Steps:
    1. Validate input market data
    2. Parse date column
    3. Sort ascending by date
    4. Drop duplicate dates
    5. Build processed dataset with canonical price series
    6. Save processed CSV

    Returns
    -------
    pd.DataFrame
        Processed market data with columns: date, ticker, price, volume
    """
    validate_market_data(df)

    transformed_df = parse_date_column(df)
    transformed_df = sort_by_date(transformed_df)
    transformed_df = drop_duplicate_dates(transformed_df)

    processed_df = build_processed_market_data(transformed_df)

    filename = build_processed_data_filename(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
    )
    save_processed_csv(df=processed_df, output_dir=output_dir, filename=filename)

    return processed_df