from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Optional, Tuple

import numpy as np
import pandas as pd


FillStrategy = Literal["mean", "median", "mode", "constant"]


@dataclass
class MissingReport:
    total_rows: int
    total_cols: int
    missing_by_col: pd.Series
    missing_percent_by_col: pd.Series

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame({
            "missing_count": self.missing_by_col,
            "missing_percent": self.missing_percent_by_col.round(2)
        }).sort_values("missing_count", ascending=False)


def basic_info(df: pd.DataFrame) -> Dict[str, object]:
    return {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }


def count_missing(df: pd.DataFrame) -> pd.Series:
    return df.isna().sum()


def missing_report(df: pd.DataFrame) -> MissingReport:
    miss = count_missing(df)
    pct = (miss / len(df) * 100) if len(df) > 0 else miss.astype(float)
    return MissingReport(
        total_rows=int(df.shape[0]),
        total_cols=int(df.shape[1]),
        missing_by_col=miss,
        missing_percent_by_col=pct
    )


def fill_missing(
    df: pd.DataFrame,
    *,
    strategy: FillStrategy = "mean",
    columns: Optional[list[str]] = None,
    constant_value: object = 0
) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """
    Возвращает: (новый_df, словарь что заполнили)
    """
    df2 = df.copy()
    info: Dict[str, object] = {}

    cols = columns if columns is not None else list(df2.columns)

    for col in cols:
        if col not in df2.columns:
            continue

        n_missing = int(df2[col].isna().sum())
        if n_missing == 0:
            continue

        if strategy in ["mean", "median"]:
            if not pd.api.types.is_numeric_dtype(df2[col]):
                # Для нечисловых mean/median не подходит → fallback на mode
                val = df2[col].mode(dropna=True)
                fill_val = val.iloc[0] if len(val) > 0 else constant_value
                used = "mode_fallback"
            else:
                fill_val = float(df2[col].mean()) if strategy == "mean" else float(df2[col].median())
                used = strategy

        elif strategy == "mode":
            val = df2[col].mode(dropna=True)
            fill_val = val.iloc[0] if len(val) > 0 else constant_value
            used = "mode"

        elif strategy == "constant":
            fill_val = constant_value
            used = "constant"

        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        df2[col] = df2[col].fillna(fill_val)
        info[col] = {"filled_missing": n_missing, "strategy_used": used, "fill_value": fill_val}

    return df2, info


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()


def convert_object_to_category(df: pd.DataFrame, max_unique: int = 50) -> pd.DataFrame:
    """
    Пример предобработки: если столбец object и мало уникальных значений — переводим в category.
    """
    df2 = df.copy()
    for col in df2.columns:
        if df2[col].dtype == "object":
            nunique = df2[col].nunique(dropna=True)
            if nunique <= max_unique:
                df2[col] = df2[col].astype("category")
    return df2
