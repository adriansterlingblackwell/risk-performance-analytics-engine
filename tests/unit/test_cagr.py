from __future__ import annotations

import pandas as pd
import pytest

from risk_analytics.analytics.performance.cagr import (
    compute_cagr,
    compute_cagr_from_dataframe,
    compute_years_between_dates,
)


def test_compute_years_between_dates() -> None:
    start = pd.Timestamp("2020-01-01")
    end = pd.Timestamp("2022-01-01")

    years = compute_years_between_dates(start, end)

    assert years == pytest.approx(2.0, rel=1e-2)


def test_compute_cagr_basic_case() -> None:
    price_series = pd.Series([100.0, 121.0])
    dates = pd.Series([
        pd.Timestamp("2020-01-01"),
        pd.Timestamp("2022-01-01"),
    ])

    result = compute_cagr(price_series, dates)

    # sqrt(1.21) - 1 ≈ 0.10
    assert result == pytest.approx(0.10, rel=1e-2)


def test_compute_cagr_double_in_four_years() -> None:
    price_series = pd.Series([100.0, 200.0])
    dates = pd.Series([
        pd.Timestamp("2020-01-01"),
        pd.Timestamp("2024-01-01"),
    ])

    result = compute_cagr(price_series, dates)

    # (2)^(1/4) - 1 ≈ 0.189
    assert result == pytest.approx(0.189, rel=1e-2)


def test_compute_cagr_raises_for_empty_series() -> None:
    with pytest.raises(ValueError):
        compute_cagr(pd.Series(dtype=float), pd.Series(dtype="datetime64[ns]"))


def test_compute_cagr_raises_for_negative_prices() -> None:
    price_series = pd.Series([100.0, -50.0])
    dates = pd.Series([
        pd.Timestamp("2020-01-01"),
        pd.Timestamp("2021-01-01"),
    ])

    with pytest.raises(ValueError):
        compute_cagr(price_series, dates)


def test_compute_cagr_raises_for_missing_dates() -> None:
    price_series = pd.Series([100.0, 120.0])

    with pytest.raises(ValueError):
        compute_cagr(price_series, None)


def test_compute_cagr_from_dataframe() -> None:
    df = pd.DataFrame({
        "date": pd.to_datetime(["2020-01-01", "2022-01-01"]),
        "price": [100.0, 121.0],
    })

    result = compute_cagr_from_dataframe(df)

    assert result == pytest.approx(0.10, rel=1e-2)


def test_compute_cagr_from_dataframe_missing_column() -> None:
    df = pd.DataFrame({
        "date": pd.to_datetime(["2020-01-01", "2022-01-01"]),
    })

    with pytest.raises(ValueError):
        compute_cagr_from_dataframe(df)