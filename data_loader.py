from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

import pandas as pd

try:
    import requests
except Exception:
    requests = None


@dataclass
class LoadResult:
    df: pd.DataFrame
    source: str


def load_csv(path: str, *, sep: str = ",", encoding: Optional[str] = None) -> LoadResult:
    df = pd.read_csv(path, sep=sep, encoding=encoding)
    return LoadResult(df=df, source=f"csv:{path}")


def load_json(path: str) -> LoadResult:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return LoadResult(df=df, source=f"json:{path}")


def load_api(url: str, *, params: Optional[Dict[str, Any]] = None, timeout: int = 20) -> LoadResult:
    if requests is None:
        raise ImportError("Пакет requests недоступен. Установи его или используй CSV/JSON.")
    r = requests.get(url, params=params, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    df = pd.DataFrame(data)
    return LoadResult(df=df, source=f"api:{url}")
