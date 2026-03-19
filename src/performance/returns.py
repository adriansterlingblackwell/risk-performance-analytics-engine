import numpy as np
import pandas as pd

from analytics_engine.config import TRADING_DAYS_PER_YEAR
from analytics_engine.utils.validation import validate_series


def compute_simple_returns(prices: pd.Series) -> pd.Series:
    """
    Compute simple periodic returns from a price series.

    Formula:
        r_t = P_t / P_{t-1} - 1
    """
    prices = validate_series(prices, name="prices", allow_na=False)

    if (prices <= 0).any():
        raise ValueError("prices must be strictly positive to compute returns.")

    returns = prices.pct_change().dropna()
    returns.name = "simple_returns"
    return returns


def compute_log_returns(prices: pd.Series) -> pd.Series:
    """
    Compute log returns from a price series.

    Formula:
        l_t = ln(P_t / P_{t-1})
    """
    prices = validate_series(prices, name="prices", allow_na=False)

    if (prices <= 0).any():
        raise ValueError("prices must be strictly positive to compute log returns.")

    log_returns = np.log(prices / prices.shift(1)).dropna()
    log_returns.name = "log_returns"
    return log_returns


def cumulative_returns(returns: pd.Series) -> pd.Series:
    """
    Compute cumulative returns from a periodic return series.

    Formula:
        R_cum,t = Π(1 + r_i) - 1
    """
    returns = validate_series(returns, name="returns", allow_na=False)
    cumulative = (1 + returns).cumprod() - 1
    cumulative.name = "cumulative_returns"
    return cumulative


def total_return(returns: pd.Series) -> float:
    """
    Compute total return from a periodic return series.
    """
    returns = validate_series(returns, name="returns", allow_na=False)
    return float((1 + returns).prod() - 1)


def annualized_return(
    returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """
    Compute annualized return from a periodic return series.

    Formula:
        R_ann = (1 + R_total)^(periods_per_year / n) - 1
    """
    returns = validate_series(returns, name="returns", allow_na=False)

    n_periods = len(returns)
    if n_periods == 0:
        raise ValueError("returns must contain at least one observation.")

    gross_return = (1 + returns).prod()
    ann_return = gross_return ** (periods_per_year / n_periods) - 1
    return float(ann_return)