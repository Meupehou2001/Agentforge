"""Wiederverwendbare Bausteine zur Datenaufbereitung mit pandas."""

from __future__ import annotations

import pandas as pd


def drop_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Entfernt doppelte Zeilen (optional nur anhand bestimmter Spalten)."""
    return df.drop_duplicates(subset=subset).reset_index(drop=True)


def fill_missing(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """Füllt fehlende numerische Werte gemäß der gewählten Strategie."""
    df = df.copy()
    numeric_cols = df.select_dtypes(include="number").columns

    if strategy == "mean":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == "median":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif strategy == "zero":
        df[numeric_cols] = df[numeric_cols].fillna(0)
    else:
        raise ValueError(f"Unbekannte Strategie: {strategy!r} (erwartet mean/median/zero)")

    return df


def remove_outliers_iqr(df: pd.DataFrame, column: str, factor: float = 1.5) -> pd.DataFrame:
    """Entfernt Ausreißer einer Spalte anhand der Interquartilsabstand-Methode (IQR)."""
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    return df[(df[column] >= lower) & (df[column] <= upper)].reset_index(drop=True)


def clean_dataset(
    df: pd.DataFrame,
    dedupe_subset: list[str] | None = None,
    fill_strategy: str = "mean",
) -> pd.DataFrame:
    """Standard-Bereinigungspipeline: Duplikate entfernen, fehlende Werte auffüllen."""
    df = drop_duplicates(df, subset=dedupe_subset)
    df = fill_missing(df, strategy=fill_strategy)
    return df
