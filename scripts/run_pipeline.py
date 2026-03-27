from __future__ import annotations

from pathlib import Path

import pandas as pd

from risk_analytics.analytics.performance.cagr import compute_cagr_from_dataframe
from risk_analytics.analytics.performance.returns import (
    build_returns_dataframe,
    compute_total_return,
)
from risk_analytics.analytics.performance.sharpe import compute_sharpe_from_dataframe
from risk_analytics.data.loaders import load_market_data
from risk_analytics.data.transforms import transform_market_data


def save_returns_csv(
    returns_df: pd.DataFrame,
    output_dir: str | Path,
    filename: str,
) -> Path:
    """
    Save returns analytics output to CSV.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / filename
    returns_df.to_csv(file_path, index=False)

    return file_path


def build_returns_filename(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str,
) -> str:
    """
    Build a deterministic filename for returns analytics output.
    """
    safe_ticker = ticker.lower().strip()
    return f"{safe_ticker}_{start_date}_{end_date}_{interval}_returns.csv"


def main() -> None:
    """
    Run the end-to-end market data pipeline.

    Steps:
    1. Download and validate raw market data
    2. Transform data into analytics-ready processed format
    3. Compute return-based analytics
    4. Compute summary performance metrics
    5. Save returns analytics output
    6. Print execution summary
    """
    ticker = "AAPL"
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    interval = "1d"

    raw_output_dir = "data/raw"
    processed_output_dir = "data/processed"
    returns_output_dir = "reports/exports"

    annual_risk_free_rate = 0.02

    raw_df = load_market_data(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
        output_dir=raw_output_dir,
    )

    processed_df = transform_market_data(
        df=raw_df,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
        output_dir=processed_output_dir,
    )

    returns_df = build_returns_dataframe(
        df=processed_df,
        price_column="price",
    )

    total_return = compute_total_return(returns_df["price"])
    cagr = compute_cagr_from_dataframe(returns_df)
    sharpe_ratio = compute_sharpe_from_dataframe(
        df=returns_df,
        return_column="daily_return",
        annual_risk_free_rate=annual_risk_free_rate,
        periods_per_year=252,
    )

    summary_metrics = {
        "total_return": total_return,
        "cagr": cagr,
        "sharpe_ratio": sharpe_ratio,
    }

    returns_filename = build_returns_filename(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
    )

    returns_file_path = save_returns_csv(
        returns_df=returns_df,
        output_dir=returns_output_dir,
        filename=returns_filename,
    )

    print("=" * 60)
    print("Risk & Performance Analytics Engine - Pipeline Run")
    print("=" * 60)
    print(f"Ticker          : {ticker}")
    print(f"Date Range      : {start_date} -> {end_date}")
    print(f"Interval        : {interval}")
    print(f"Rows Processed  : {len(returns_df)}")
    print(f"Risk-Free Rate  : {annual_risk_free_rate:.2%}")
    print(f"Total Return    : {summary_metrics['total_return']:.4%}")
    print(f"CAGR            : {summary_metrics['cagr']:.4%}")
    print(f"Sharpe Ratio    : {summary_metrics['sharpe_ratio']:.4f}")
    print(f"Returns Output  : {returns_file_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()