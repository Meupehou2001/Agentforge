"""Tests für die Datenaufbereitung (data/cleaning.py)."""

import pandas as pd

from agentforge.data.cleaning import clean_dataset, drop_duplicates, fill_missing, remove_outliers_iqr


def test_drop_duplicates_removes_exact_duplicates() -> None:
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    result = drop_duplicates(df)
    assert len(result) == 2


def test_fill_missing_mean_strategy() -> None:
    df = pd.DataFrame({"a": [1.0, None, 3.0]})
    result = fill_missing(df, strategy="mean")
    assert result["a"].iloc[1] == 2.0


def test_fill_missing_zero_strategy() -> None:
    df = pd.DataFrame({"a": [1.0, None, 3.0]})
    result = fill_missing(df, strategy="zero")
    assert result["a"].iloc[1] == 0.0


def test_remove_outliers_iqr_drops_extreme_values() -> None:
    df = pd.DataFrame({"a": [10, 11, 12, 13, 1000]})
    result = remove_outliers_iqr(df, column="a")
    assert 1000 not in result["a"].values


def test_clean_dataset_pipeline_dedupes_and_fills() -> None:
    df = pd.DataFrame({"a": [1.0, 1.0, None], "b": ["x", "x", "y"]})
    result = clean_dataset(df, dedupe_subset=["a", "b"], fill_strategy="zero")
    assert len(result) == 2
    assert result["a"].isna().sum() == 0
