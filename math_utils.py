# math_utils.py — utilidades numéricas y de series de tiempo
# ----------------------------------------------------------
# Todas las funciones son "pandas-friendly" (vectorizadas) y tolerantes a NaN.
# No dependen de Streamlit. Se enfocan en robustez y en trabajar con frames grandes.

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Literal

import numpy as np
import pandas as pd


# =========================
# Helpers de tipificación
# =========================

def _to_numeric(s: pd.Series) -> pd.Series:
    """Convierte a numérico con errors='coerce' y sin modificar el índice."""
    return pd.to_numeric(s, errors="coerce")


def _to_datetime(s: pd.Series) -> pd.Series:
    """Convierte a datetime con errors='coerce' y sin modificar el índice."""
    return pd.to_datetime(s, errors="coerce")


def _ensure_series(df: pd.DataFrame, col: str) -> pd.Series:
    if col not in df.columns:
        return pd.Series(dtype=float)
    return df[col]


# =========================
# Estadísticos básicos
# =========================

def describe_numeric(df: pd.DataFrame, col: str) -> Dict[str, float]:
    """Estadísticos clave para una columna numérica."""
    x = _to_numeric(_ensure_series(df, col)).dropna()
    if x.empty:
        return dict(count=0, mean=np.nan, median=np.nan, std=np.nan,
                    min=np.nan, max=np.nan, sum=np.nan)
    return dict(
        count=float(x.count()),
        mean=float(x.mean()),
        median=float(x.median()),
        std=float(x.std(ddof=1)) if x.count() > 1 else 0.0,
        min=float(x.min()),
        max=float(x.max()),
        sum=float(x.sum()),
    )


def percentiles_iqr(df: pd.DataFrame, col: str) -> Dict[str, float]:
    """P25, P50, P75 e IQR de una columna numérica."""
    x = _to_numeric(_ensure_series(df, col)).dropna()
    if x.empty:
        return dict(p25=np.nan, p50=np.nan, p75=np.nan, iqr=np.nan)
    q1 = float(x.quantile(0.25))
    q2 = float(x.quantile(0.50))
    q3 = float(x.quantile(0.75))
    return dict(p25=q1, p50=q2, p75=q3, iqr=q3 - q1)


def flag_outliers_z(df: pd.DataFrame, col: str, z: float = 3.0) -> pd.Series:
    """Marca outliers por Z-score absoluto > z. Devuelve serie booleana con mismo índice que df."""
    x = _to_numeric(_ensure_series(df, col))
    mu = x.mean(skipna=True)
    sd = x.std(skipna=True, ddof=1)
    if not np.isfinite(mu) or not np.isfinite(sd) or sd == 0 or len(x) == 0:
        return pd.Series(False, index=df.index)
    zscores = (x - mu) / sd
    return zscores.abs() > float(z)


def flag_outliers_iqr(df: pd.DataFrame, col: str, k: float = 1.5) -> pd.Series:
    """Marca outliers por método de Tukey (k*IQR)."""
    x = _to_numeric(_ensure_series(df, col))
    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    iqr = q3 - q1
    if not np.isfinite(iqr) or iqr == 0:
        return pd.Series(False, index=df.index)
    low = q1 - k * iqr
    high = q3 + k * iqr
    return (x < low) | (x > high)


# =========================
# Correlaciones
# =========================

def correlation_matrix(df: pd.DataFrame, method: Literal["pearson", "spearman", "kendall"] = "pearson") -> pd.DataFrame:
    """Matriz de correlación solo con columnas numéricas (coerce)."""
    numeric = {}
    for c in df.columns:
        s = _to_numeric(df[c])
        # incluir si tiene al menos 2 valores no-NaN distintos
        if s.notna().sum() >= 2 and s.nunique(dropna=True) >= 2:
            numeric[c] = s
    if not numeric:
        return pd.DataFrame()
    num_df = pd.DataFrame(numeric)
    return num_df.corr(method=method)


# =========================
# Series de tiempo
# =========================

def _aggregate_ts(
    df: pd.DataFrame,
    date_col: str,
    val_col: str,
    freq: Literal["D", "W", "M"] = "M",
    agg: Literal["sum", "mean", "count"] = "sum",
) -> pd.Series:
    """Convierte (fecha, valor) a serie por frecuencia con agregación."""
    dates = _to_datetime(_ensure_series(df, date_col))
    vals = _to_numeric(_ensure_series(df, val_col))
    ts = pd.DataFrame({"_d": dates, "_v": vals}).dropna(subset=["_d"])
    if ts.empty:
        return pd.Series(dtype=float)

    ts = ts.set_index("_d").sort_index()
    if agg == "mean":
        out = ts["_v"].resample(freq).mean()
    elif agg == "count":
        out = ts["_v"].resample(freq).count().astype(float)
    else:
        out = ts["_v"].resample(freq).sum()

    return out


def rolling_sma(
    df: pd.DataFrame,
    date_col: str,
    val_col: str,
    window: int = 6,
    freq: Literal["D", "W", "M"] = "M",
    agg: Literal["sum", "mean", "count"] = "sum",
) -> pd.DataFrame:
    """SMA sobre serie agregada. Devuelve DataFrame con columnas ['value', f'sma_{window}']"""
    base = _aggregate_ts(df, date_col, val_col, freq=freq, agg=agg)
    if base.empty:
        return pd.DataFrame(columns=["value", f"sma_{int(window)}"])
    sma = base.rolling(window=int(max(1, window)), min_periods=1).mean()
    out = pd.DataFrame({"value": base, f"sma_{int(window)}": sma})
    return out


def rolling_ema(
    df: pd.DataFrame,
    date_col: str,
    val_col: str,
    span: int = 6,
    freq: Literal["D", "W", "M"] = "M",
    agg: Literal["sum", "mean", "count"] = "sum",
) -> pd.DataFrame:
    """EMA sobre serie agregada. Devuelve DataFrame con columnas ['value', f'ema_{span}']"""
    base = _aggregate_ts(df, date_col, val_col, freq=freq, agg=agg)
    if base.empty:
        return pd.DataFrame(columns=["value", f"ema_{int(span)}"])
    ema = base.ewm(span=int(max(1, span)), adjust=False).mean()
    out = pd.DataFrame({"value": base, f"ema_{int(span)}": ema})
    return out


def monthly_growth(
    df: pd.DataFrame,
    date_col: str,
    val_col: str,
    agg: Literal["sum", "mean", "count"] = "sum",
) -> pd.DataFrame:
    """
    Crecimiento MoM (% y absoluto) usando frecuencia mensual.
    mom_pct se devuelve en porcentaje (0..100).
    """
    s = _aggregate_ts(df, date_col, val_col, freq="M", agg=agg)
    if s.empty:
        return pd.DataFrame(columns=["value", "mom_abs", "mom_pct"])
    prev = s.shift(1)
    abs_diff = s - prev
    pct = (s / prev - 1.0) * 100.0
    out = pd.DataFrame({"value": s, "mom_abs": abs_diff, "mom_pct": pct})
    return out


def cagr(
    df: pd.DataFrame,
    date_col: str,
    val_col: str,
    agg: Literal["sum", "mean", "count"] = "sum",
) -> Optional[float]:
    """
    CAGR aproximado anualizado en % usando la serie mensual agregada.
    Si el periodo es < 1 mes válido o la serie está vacía → None.
    """
    s = _aggregate_ts(df, date_col, val_col, freq="M", agg=agg).dropna()
    if s.empty or s.count() < 2:
        return None

    # usar primer y último valor positivo (evita divisiones raras)
    first_idx = s.first_valid_index()
    last_idx = s.last_valid_index()
    v0 = float(s.loc[first_idx])
    v1 = float(s.loc[last_idx])
    # Si v0 <= 0 o v1 <= 0, no tiene sentido el CAGR clásico
    if v0 <= 0 or v1 <= 0:
        return None

    # años entre puntos (meses/12)
    months = max(1, (last_idx.to_period("M") - first_idx.to_period("M")).n)
    years = months / 12.0
    cagr_val = (v1 / v0) ** (1.0 / years) - 1.0
    return float(cagr_val * 100.0)


def linear_trend(
    df: pd.DataFrame,
    date_col: str,
    val_col: str,
    freq: Literal["D", "W", "M"] = "M",
    agg: Literal["sum", "mean", "count"] = "sum",
) -> Dict[str, float]:
    """
    Ajuste lineal y = a + b*t sobre serie agregada.
    Devuelve dict con slope (b) y r2.
    """
    s = _aggregate_ts(df, date_col, val_col, freq=freq, agg=agg).dropna()
    if s.empty or s.count() < 2:
        return dict(slope=np.nan, r2=np.nan)

    # eje temporal como 0..n-1 (evita overflow de timestamps)
    t = np.arange(len(s), dtype=float)
    y = s.values.astype(float)

    # Ajuste por mínimos cuadrados
    # coef [b, a] para y ~ b*t + a
    b, a = np.polyfit(t, y, 1)

    # R^2
    y_hat = a + b * t
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot != 0 else np.nan

    return dict(slope=float(b), r2=float(r2))
