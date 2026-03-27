from __future__ import annotations

import numpy as np
import pandas as pd


def validate_return_series(return_series: pd.Series) -> None:
    """
    Validate that the input return series is suitable for Sortino ratio calculation.
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
    """
    return annual_risk_free_rate / periods_per_year


def compute_downside_deviation(
    return_series: pd.Series,
    annual_risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Compute downside deviation using returns below the per-period risk-free rate.

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
        Downside deviation.
    """
    validate_return_series(return_series)

    cleaned_returns = return_series.dropna()
    risk_free_per_period = annualize_risk_free_rate(
        annual_risk_free_rate=annual_risk_free_rate,
        periods_per_year=periods_per_year,
    )

    excess_returns = cleaned_returns - risk_free_per_period
    downside_returns = np.minimum(excess_returns, 0.0)

    downside_deviation = np.sqrt(np.mean(np.square(downside_returns)))

    return float(downside_deviation)


def compute_sortino_ratio(
    return_series: pd.Series,
    annual_risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Compute the annualized Sortino ratio from a return series.

    Formula:
        Sortino = ((mean_return - risk_free_per_period) / downside_deviation) * sqrt(periods_per_year)
    """
    validate_return_series(return_series)

    cleaned_returns = return_series.dropna()
    risk_free_per_period = annualize_risk_free_rate(
        annual_risk_free_rate=annual_risk_free_rate,
        periods_per_year=periods_per_year,
    )

    mean_excess_return = (cleaned_returns - risk_free_per_period).mean()
    downside_deviation = compute_downside_deviation(
        return_series=cleaned_returns,
        annual_risk_free_rate=annual_risk_free_rate,
        periods_per_year=periods_per_year,
    )

    if downside_deviation == 0:
        raise ValueError(
            "Downside deviation is zero; Sortino ratio is undefined."
        )

    sortino_ratio = (mean_excess_return / downside_deviation) * np.sqrt(periods_per_year)

    return float(sortino_ratio)


def compute_sortino_from_dataframe(
    df: pd.DataFrame,
    return_column: str = "daily_return",
    annual_risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Convenience wrapper to compute Sortino ratio from a DataFrame.
    """
    if return_column not in df.columns:
        raise ValueError(f"Missing required return column: '{return_column}'")

    return compute_sortino_ratio(
        return_series=df[return_column],
        annual_risk_free_rate=annual_risk_free_rate,
        periods_per_year=periods_per_year,
    )