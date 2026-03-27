from __future__ import annotations

import pandas as pd
import pytest

from risk_analytics.analytics.performance.sharpe import (
    annualize_risk_free_rate,
    compute_sharpe_from_dataframe,
    compute_sharpe_ratio,
    validate_return_series,
)


def test_validate_return_series_raises_for_empty_series() -> None:
    return_series = pd.Series(dtype=float)

    with pytest.raises(ValueError, match="Return series is empty."):
        validate_return_series(return_series)


def test_validate_return_series_raises_for_all_null_series() -> None:
    return_series = pd.Series([None, None, None], dtype=float)

    with pytest.raises(ValueError, match="Return series contains only null values."):
        validate_return_series(return_series)


def test_annualize_risk_free_rate() -> None:
    annual_rf = 0.025

    result = annualize_risk_free_rate(
        annual_risk_free_rate=annual_rf,
        periods_per_year=252,
    )

    assert result == pytest.approx(0.025 / 252)


def test_compute_sharpe_ratio_returns_float() -> None:
    return_series = pd.Series([0.01, 0.015, -0.005, 0.02, 0.01])

    result = compute_sharpe_ratio(
        return_series=return_series,
        annual_risk_free_rate=0.0,
        periods_per_year=252,
    )

    assert isinstance(result, float)


def test_compute_sharpe_ratio_raises_for_zero_volatility() -> None:
    return_series = pd.Series([0.01, 0.01, 0.01, 0.01])

    with pytest.raises(
        ValueError,
        match="Return series volatility is zero; Sharpe ratio is undefined.",
    ):
        compute_sharpe_ratio(return_series)


def test_compute_sharpe_ratio_with_risk_free_rate_is_lower() -> None:
    return_series = pd.Series([0.01, 0.015, -0.005, 0.02, 0.01])

    sharpe_without_rf = compute_sharpe_ratio(
        return_series=return_series,
        annual_risk_free_rate=0.0,
        periods_per_year=252,
    )

    sharpe_with_rf = compute_sharpe_ratio(
        return_series=return_series,
        annual_risk_free_rate=0.03,
        periods_per_year=252,
    )

    assert sharpe_with_rf < sharpe_without_rf


def test_compute_sharpe_ratio_ignores_initial_nan() -> None:
    return_series = pd.Series([None, 0.01, 0.015, -0.005, 0.02], dtype=float)

    result = compute_sharpe_ratio(
        return_series=return_series,
        annual_risk_free_rate=0.0,
        periods_per_year=252,
    )

    assert isinstance(result, float)


def test_compute_sharpe_from_dataframe() -> None:
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
            ),
            "daily_return": [None, 0.01, 0.015, -0.005, 0.02],
        }
    )

    result = compute_sharpe_from_dataframe(
        df=df,
        return_column="daily_return",
        annual_risk_free_rate=0.0,
        periods_per_year=252,
    )

    assert isinstance(result, float)


def test_compute_sharpe_from_dataframe_raises_for_missing_column() -> None:
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "price": [100.0, 101.0],
        }
    )

    with pytest.raises(ValueError, match="Missing required return column"):
        compute_sharpe_from_dataframe(df=df, return_column="daily_return")