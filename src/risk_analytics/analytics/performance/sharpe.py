from __future__ import annotations

import numpy as np
import pandas as pd


def validate_return_series(return_series: pd.Series) -> None:
    """
    Validate that the input return series is suitable for Sharpe ratio calculation.
    """
    if return_series.empty:
        raise ValueError("Return series is empty.")

    cleaned_returns = return_series.dropna()

    if cleaned_returns.empty:
        raise ValueError("Return series contains only null values.")


def annualize_risk_free_rate(
    annual_risk_free_rate: float,
    periods_per_year: int = 252,
) -> float:
    """
    Convert an annual risk-free rate into a per-period risk-free rate.

    Parameters
    ----------
    annual_risk_free_rate:
        Annual risk-free rate as a decimal (e.g. 0.02 for 2%).
    periods_per_year:
        Number of periods per year. Default is 252 for trading days.

    Returns
    -------
    float
        Per-period risk-free rate.
    """
    return annual_risk_free_rate / periods_per_year


def compute_sharpe_ratio(
    return_series: pd.Series,
    annual_risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Compute the annualized Sharpe ratio from a return series.

    Formula:
        Sharpe = ((mean_return - risk_free_per_period) / std_return) * sqrt(periods_per_year)

    Parameters
    ----------
    return_series:
        Periodic returns series.
    annual_risk_free_rate:
        Annual risk-free rate as a decimal.
    periods_per_year:
        Number of periods per year.

    Returns
    -------
    float
        Annualized Sharpe ratio.
    """
    validate_return_series(return_series)

    cleaned_returns = return_series.dropna()

    risk_free_per_period = annualize_risk_free_rate(
        annual_risk_free_rate=annual_risk_free_rate,
        periods_per_year=periods_per_year,
    )

    excess_returns = cleaned_returns - risk_free_per_period

    mean_excess_return = excess_returns.mean()
    volatility = cleaned_returns.std(ddof=1)

    if volatility == 0:
        raise ValueError("Return series volatility is zero; Sharpe ratio is undefined.")

    sharpe_ratio = (mean_excess_return / volatility) * np.sqrt(periods_per_year)

    return float(sharpe_ratio)


def compute_sharpe_from_dataframe(
    df: pd.DataFrame,
    return_column: str = "daily_return",
    annual_risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Convenience wrapper to compute Sharpe ratio from a DataFrame.
    """
    if return_column not in df.columns:
        raise ValueError(f"Missing required return column: '{return_column}'")

    return compute_sharpe_ratio(
        return_series=df[return_column],
        annual_risk_free_rate=annual_risk_free_rate,
        periods_per_year=periods_per_year,
    )