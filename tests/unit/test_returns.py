from __future__ import annotations

import pandas as pd
import pytest

from risk_analytics.analytics.performance.returns import (
    build_returns_dataframe,
    compute_cumulative_returns,
    compute_daily_returns,
    compute_total_return,
    validate_price_series,
)


def test_validate_price_series_raises_for_empty_series() -> None:
    price_series = pd.Series(dtype=float)

    with pytest.raises(ValueError, match="Price series is empty."):
        validate_price_series(price_series)


def test_validate_price_series_raises_for_null_values() -> None:
    price_series = pd.Series([100.0, None, 110.0])

    with pytest.raises(ValueError, match="Price series contains null values."):
        validate_price_series(price_series)


def test_validate_price_series_raises_for_non_positive_values() -> None:
    price_series = pd.Series([100.0, 0.0, 110.0])

    with pytest.raises(ValueError, match="Price series contains non-positive values."):
        validate_price_series(price_series)


def test_compute_daily_returns() -> None:
    price_series = pd.Series([100.0, 110.0, 121.0])

    result = compute_daily_returns(price_series)

    assert pd.isna(result.iloc[0])
    assert result.iloc[1] == pytest.approx(0.10)
    assert result.iloc[2] == pytest.approx(0.10)


def test_compute_cumulative_returns() -> None:
    return_series = pd.Series([None, 0.10, 0.10])

    result = compute_cumulative_returns(return_series)

    assert result.iloc[0] == pytest.approx(0.00)
    assert result.iloc[1] == pytest.approx(0.10)
    assert result.iloc[2] == pytest.approx(0.21)


def test_compute_total_return() -> None:
    price_series = pd.Series([100.0, 110.0, 121.0])

    result = compute_total_return(price_series)

    assert result == pytest.approx(0.21)


def test_build_returns_dataframe_adds_expected_columns() -> None:
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "ticker": ["AAPL", "AAPL", "AAPL"],
            "price": [100.0, 110.0, 121.0],
            "volume": [1000, 1200, 1500],
        }
    )

    result = build_returns_dataframe(df)

    assert "daily_return" in result.columns
    assert "cumulative_return" in result.columns

    assert pd.isna(result.loc[0, "daily_return"])
    assert result.loc[1, "daily_return"] == pytest.approx(0.10)
    assert result.loc[2, "daily_return"] == pytest.approx(0.10)

    assert result.loc[0, "cumulative_return"] == pytest.approx(0.00)
    assert result.loc[1, "cumulative_return"] == pytest.approx(0.10)
    assert result.loc[2, "cumulative_return"] == pytest.approx(0.21)


def test_build_returns_dataframe_raises_for_missing_columns() -> None:
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "ticker": ["AAPL", "AAPL"],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        build_returns_dataframe(df)


def test_total_return_matches_final_cumulative_return() -> None:
    price_series = pd.Series([100.0, 110.0, 121.0])

    daily_returns = compute_daily_returns(price_series)
    cumulative_returns = compute_cumulative_returns(daily_returns)
    total_return = compute_total_return(price_series)

    assert cumulative_returns.iloc[-1] == pytest.approx(total_return)