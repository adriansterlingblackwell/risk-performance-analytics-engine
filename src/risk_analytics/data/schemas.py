from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final


# ---------------------------------------------------------------------
# Source-to-normalized column mapping
# ---------------------------------------------------------------------

YFINANCE_COLUMN_MAPPING: Final[dict[str, str]] = {
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume",
    "Ticker": "ticker",
}


# ---------------------------------------------------------------------
# Canonical column groups
# ---------------------------------------------------------------------

MARKET_DATA_COLUMNS: Final[list[str]] = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "adj_close",
    "volume",
    "ticker",
]

REQUIRED_MARKET_DATA_COLUMNS: Final[list[str]] = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "ticker",
]

OPTIONAL_MARKET_DATA_COLUMNS: Final[list[str]] = [
    "adj_close",
]

PRICE_COLUMN_PRIORITY: Final[list[str]] = [
    "adj_close",
    "close",
]


# ---------------------------------------------------------------------
# Schema definition
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class DataSchema:
    """
    Canonical schema definition for market data used in the analytics engine.

    Attributes
    ----------
    name:
        Human-readable schema name.
    required_columns:
        Columns that must exist for the dataset to be considered valid.
    optional_columns:
        Columns that are accepted but not mandatory.
    price_column_priority:
        Ordered list of preferred price columns for return calculations.
    """

    name: str
    required_columns: list[str] = field(default_factory=list)
    optional_columns: list[str] = field(default_factory=list)
    price_column_priority: list[str] = field(default_factory=list)

    @property
    def all_columns(self) -> list[str]:
        """Return the full accepted schema column set."""
        return self.required_columns + [
            col for col in self.optional_columns if col not in self.required_columns
        ]


MARKET_DATA_SCHEMA = DataSchema(
    name="market_data",
    required_columns=REQUIRED_MARKET_DATA_COLUMNS,
    optional_columns=OPTIONAL_MARKET_DATA_COLUMNS,
    price_column_priority=PRICE_COLUMN_PRIORITY,
)