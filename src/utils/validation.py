import pandas as pd
from analytics_engine.exceptions import ValidationError


def validate_series(
    series: pd.Series,
    name: str = "series",
    allow_na: bool = False,
    require_datetime_index: bool = True,
) -> pd.Series:
    if not isinstance(series, pd.Series):
        raise ValidationError(f"{name} must be a pandas Series.")

    if series.empty:
        raise ValidationError(f"{name} must not be empty.")

    if require_datetime_index and not isinstance(series.index, pd.DatetimeIndex):
        raise ValidationError(f"{name} must have a DatetimeIndex.")

    if not allow_na and series.isna().any():
        raise ValidationError(f"{name} must not contain NaN values.")

    return series.sort_index()