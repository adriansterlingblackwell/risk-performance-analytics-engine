import math
import pandas as pd
import pytest

from analytics_engine.performance.returns import (
    compute_simple_returns,
    compute_log_returns,
    cumulative_returns,
    total_return,
    annualized_return,
)


@pytest.fixture
def sample_prices():
    return pd.Series(
        [100, 110, 121],
        index=pd.date_range("2026-01-01", periods=3, freq="D"),
    )


def test_compute_simple_returns(sample_prices):
    returns = compute_simple_returns(sample_prices)
    assert len(returns) == 2
    assert math.isclose(returns.iloc[0], 0.10, rel_tol=1e-9)
    assert math.isclose(returns.iloc[1], 0.10, rel_tol=1e-9)


def test_compute_log_returns(sample_prices):
    log_returns = compute_log_returns(sample_prices)
    assert len(log_returns) == 2
    assert math.isclose(log_returns.iloc[0], math.log(1.10), rel_tol=1e-9)


def test_cumulative_returns(sample_prices):
    returns = compute_simple_returns(sample_prices)
    cum = cumulative_returns(returns)
    assert math.isclose(cum.iloc[-1], 0.21, rel_tol=1e-9)


def test_total_return(sample_prices):
    returns = compute_simple_returns(sample_prices)
    result = total_return(returns)
    assert math.isclose(result, 0.21, rel_tol=1e-9)


def test_annualized_return(sample_prices):
    returns = compute_simple_returns(sample_prices)
    result = annualized_return(returns, periods_per_year=2)
    expected = (1.21 ** (2 / 2)) - 1
    assert math.isclose(result, expected, rel_tol=1e-9)