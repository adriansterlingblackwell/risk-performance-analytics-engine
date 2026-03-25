from __future__ import annotations

import pandas as pd

from risk_analytics.data.schemas import DataSchema, MARKET_DATA_SCHEMA


def validate_non_empty_dataframe(df: pd.DataFrame) -> None:
    """Ensure the input DataFrame is not empty."""
    if df.empty:
        raise ValueError("Input DataFrame is empty.")


def validate_required_columns(df: pd.DataFrame, schema: DataSchema) -> None:
    """Ensure all required schema columns are present."""
    missing_columns = [col for col in schema.required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}. "
            f"Available columns: {list(df.columns)}"
        )


def validate_date_column(df: pd.DataFrame, date_column: str = "date") -> None:
    """Ensure the date column exists and can be parsed as datetime."""
    if date_column not in df.columns:
        raise ValueError(f"Missing date column: '{date_column}'")

    try:
        pd.to_datetime(df[date_column], errors="raise")
    except Exception as exc:
        raise ValueError(
            f"Column '{date_column}' cannot be parsed as datetime."
        ) from exc


def validate_no_duplicate_dates(df: pd.DataFrame, date_column: str = "date") -> None:
    """Ensure there are no duplicate dates in the dataset."""
    if df[date_column].duplicated().any():
        duplicate_rows = df[df[date_column].duplicated()][date_column].tolist()
        raise ValueError(f"Duplicate dates found in '{date_column}': {duplicate_rows}")


def validate_sorted_dates(df: pd.DataFrame, date_column: str = "date") -> None:
    """Ensure the dataset is sorted in ascending date order."""
    parsed_dates = pd.to_datetime(df[date_column], errors="raise")
    if not parsed_dates.is_monotonic_increasing:
        raise ValueError(f"Column '{date_column}' is not sorted in ascending order.")


def validate_no_nulls_in_required_columns(df: pd.DataFrame, schema: DataSchema) -> None:
    """Ensure required columns do not contain null values."""
    null_columns = [col for col in schema.required_columns if df[col].isnull().any()]
    if null_columns:
        raise ValueError(f"Null values found in required columns: {null_columns}")


def validate_positive_price_columns(df: pd.DataFrame) -> None:
    """Ensure available price columns contain strictly positive values."""
    price_columns = [col for col in ["open", "high", "low", "close", "adj_close"] if col in df.columns]

    invalid_columns = []
    for col in price_columns:
        if (df[col] <= 0).any():
            invalid_columns.append(col)

    if invalid_columns:
        raise ValueError(
            f"Non-positive values found in price columns: {invalid_columns}"
        )


def validate_non_negative_volume(df: pd.DataFrame, volume_column: str = "volume") -> None:
    """Ensure volume values are not negative."""
    if volume_column in df.columns and (df[volume_column] < 0).any():
        raise ValueError(f"Negative values found in '{volume_column}' column.")


def validate_market_data(df: pd.DataFrame, schema: DataSchema = MARKET_DATA_SCHEMA) -> None:
    """
    Run the full validation pipeline for market data.

    This function raises ValueError if any validation check fails.
    """
    validate_non_empty_dataframe(df)
    validate_required_columns(df, schema)
    validate_date_column(df, date_column="date")
    validate_no_nulls_in_required_columns(df, schema)
    validate_no_duplicate_dates(df, date_column="date")
    validate_sorted_dates(df, date_column="date")
    validate_positive_price_columns(df)
    validate_non_negative_volume(df, volume_column="volume")