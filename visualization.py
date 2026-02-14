from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Optional

import pandas as pd
import matplotlib.pyplot as plt


@dataclass
class PlotSpec:
    kind: str
    func: Callable[[pd.DataFrame], None]
    description: str


class Visualizer:
    def __init__(self) -> None:
        self._plots: Dict[str, PlotSpec] = {}

    def list_plots(self) -> Dict[str, str]:
        return {name: spec.description for name, spec in self._plots.items()}

    def remove_plot(self, name: str) -> None:
        if name in self._plots:
            del self._plots[name]
        else:
            raise KeyError(f"Нет визуализации с именем: {name}")

    def add_hist(self, name: str, column: str, bins: int = 20) -> None:
        def _plot(df: pd.DataFrame) -> None:
            if column not in df.columns:
                raise KeyError(f"Нет столбца: {column}")
            plt.figure()
            df[column].dropna().hist(bins=bins)
            plt.title(f"Histogram: {column}")
            plt.xlabel(column)
            plt.ylabel("Count")
            plt.show()

        self._plots[name] = PlotSpec(
            kind="hist",
            func=_plot,
            description=f"Гистограмма по столбцу '{column}', bins={bins}"
        )

    def add_line(self, name: str, x: str, y: str) -> None:
        def _plot(df: pd.DataFrame) -> None:
            if x not in df.columns or y not in df.columns:
                raise KeyError(f"Нет столбцов: {x}, {y}")
            plt.figure()
            tmp = df[[x, y]].dropna()
            plt.plot(tmp[x], tmp[y])
            plt.title(f"Line: {y} vs {x}")
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()

        self._plots[name] = PlotSpec(
            kind="line",
            func=_plot,
            description=f"Линейный график y='{y}' от x='{x}'"
        )

    def add_scatter(self, name: str, x: str, y: str) -> None:
        def _plot(df: pd.DataFrame) -> None:
            if x not in df.columns or y not in df.columns:
                raise KeyError(f"Нет столбцов: {x}, {y}")
            plt.figure()
            tmp = df[[x, y]].dropna()
            plt.scatter(tmp[x], tmp[y])
            plt.title(f"Scatter: {y} vs {x}")
            plt.xlabel(x)
            plt.ylabel(y)
            plt.show()

        self._plots[name] = PlotSpec(
            kind="scatter",
            func=_plot,
            description=f"Диаграмма рассеяния y='{y}' от x='{x}'"
        )

    def show(self, name: str, df: pd.DataFrame) -> None:
        if name not in self._plots:
            raise KeyError(f"Нет визуализации с именем: {name}")
        self._plots[name].func(df)
