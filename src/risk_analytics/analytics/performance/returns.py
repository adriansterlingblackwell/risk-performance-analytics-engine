from __future__ import annotations

import pandas as pd


def validate_price_series(price_series: pd.Series) -> None:
    """
    Validate that the input price series is suitable for return calculations.
    """
    if price_series.empty:
        raise ValueError("Price series is empty.")

    if price_series.isnull().any():
        raise ValueError("Price series contains null values.")

    if (price_series <= 0).any():
        raise ValueError("Price series contains non-positive values.")


def compute_daily_returns(price_series: pd.Series) -> pd.Series:
    """
    Compute simple daily returns from a price series.

    Formula:
        r_t = (P_t / P_{t-1}) - 1
    """
    validate_price_series(price_series)

    daily_returns = price_series.pct_change()

    return daily_returns


def compute_cumulative_returns(return_series: pd.Series) -> pd.Series:
    """
    Compute cumulative returns from a return series.

    Formula:
        cumulative_t = (1 + r_1) * (1 + r_2) * ... * (1 + r_t) - 1
    """
    if return_series.empty:
        raise ValueError("Return series is empty.")

    cumulative_returns = (1 + return_series.fillna(0)).cumprod() - 1

    return cumulative_returns


def compute_total_return(price_series: pd.Series) -> float:
    """
    Compute total return from the first and last price point.

    Formula:
        total_return = (P_final / P_initial) - 1
    """
    validate_price_series(price_series)

    initial_price = price_series.iloc[0]
    final_price = price_series.iloc[-1]

    return float((final_price / initial_price) - 1)


def build_returns_dataframe(
    df: pd.DataFrame,
    price_column: str = "price",
) -> pd.DataFrame:
    """
    Build a return analytics DataFrame from an input market data DataFrame.

    Expected input columns:
    - date
    - ticker
    - price

    Output columns:
    - date
    - ticker
    - price
    - daily_return
    - cumulative_return
    """
    required_columns = ["date", "ticker", price_column]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Missing required columns for returns DataFrame: {missing_columns}"
        )

    returns_df = df.copy()

    daily_returns = compute_daily_returns(returns_df[price_column])
    cumulative_returns = compute_cumulative_returns(daily_returns)

    returns_df["daily_return"] = daily_returns
    returns_df["cumulative_return"] = cumulative_returns

    return returns_df