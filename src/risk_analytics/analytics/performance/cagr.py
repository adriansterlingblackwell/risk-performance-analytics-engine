from __future__ import annotations

import pandas as pd


def compute_years_between_dates(
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
) -> float:
    """
    Compute the time difference in years between two dates.
    """
    if end_date <= start_date:
        raise ValueError("End date must be after start date.")

    delta_days = (end_date - start_date).days
    return delta_days / 365.25


def compute_cagr(
    price_series: pd.Series,
    date_index: pd.Series | None = None,
) -> float:
    """
    Compute Compound Annual Growth Rate (CAGR).

    Parameters
    ----------
    price_series : pd.Series
        Price series (must be positive and ordered)
    date_index : pd.Series, optional
        Corresponding date series

    Returns
    -------
    float
        Annualized return (CAGR)
    """
    if price_series.empty:
        raise ValueError("Price series is empty.")

    if (price_series <= 0).any():
        raise ValueError("Price series contains non-positive values.")

    initial_price = price_series.iloc[0]
    final_price = price_series.iloc[-1]

    if date_index is not None:
        start_date = pd.to_datetime(date_index.iloc[0])
        end_date = pd.to_datetime(date_index.iloc[-1])
        years = compute_years_between_dates(start_date, end_date)
    else:
        raise ValueError("Date index is required for CAGR calculation.")

    if years <= 0:
        raise ValueError("Invalid time period for CAGR calculation.")

    cagr = (final_price / initial_price) ** (1 / years) - 1

    return float(cagr)


def compute_cagr_from_dataframe(
    df: pd.DataFrame,
    price_column: str = "price",
    date_column: str = "date",
) -> float:
    """
    Convenience wrapper to compute CAGR from a DataFrame.
    """
    required_columns = [price_column, date_column]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return compute_cagr(
        price_series=df[price_column],
        date_index=df[date_column],
    )