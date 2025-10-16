# app.py 
# Usuarios: damian, david, alexis  |  Password (todos): Hola123

import os, math, re, hashlib, json, warnings, time
from contextlib import contextmanager
from datetime import datetime, date
from typing import List, Tuple, Dict, Any, Optional

import numpy as np
import pandas as pd
import streamlit as st

warnings.filterwarnings("ignore", message="Could not infer format")

from dotenv import load_dotenv
load_dotenv()

# ====== Settings ======
from settings import (
    PAGE_SIZE,
    DEFAULT_ORDER_COL,
    DEFAULT_ORDER_DIR,
    ENABLE_ANALYTICS,
    ENABLE_MONGO_SYNC,
    NUMERIC_HINTS,
    DATE_HINTS,
    ANALYTICS_CORR_METHOD,
    ROLLING_DEFAULT_WINDOW,
    EMA_DEFAULT_SPAN,
    OUTLIER_Z_THRESHOLD,
    OUTLIER_IQR_K,
    RANK_ASCENDING_DEFAULT,
    QUANTILE_BUCKETS,
    TIME_GROUPING_FREQ,
    CACHE_TTL_SECONDS,
    ANALYTICS_MAX_ROWS,
)

# ====== Mini "math_utils" interno (sin dependencia externa) ======
class _MU:
    @staticmethod
    def _num_series(df: pd.DataFrame, col: str) -> pd.Series:
        return pd.to_numeric(df[col], errors="coerce")

    @staticmethod
    def describe_numeric(df: pd.DataFrame, col: str) -> Dict[str, float]:
        s = _MU._num_series(df, col).dropna()
        if s.empty:
            return {"mean": np.nan, "median": np.nan, "std": np.nan, "sum": np.nan}
        return {
            "mean": float(s.mean()),
            "median": float(s.median()),
            "std": float(s.std(ddof=1)) if len(s) > 1 else 0.0,
            "sum": float(s.sum()),
        }

    @staticmethod
    def percentiles_iqr(df: pd.DataFrame, col: str) -> Dict[str, float]:
        s = _MU._num_series(df, col).dropna()
        if s.empty:
            return {"p25": np.nan, "p50": np.nan, "p75": np.nan, "iqr": np.nan}
        p25, p50, p75 = np.percentile(s, [25, 50, 75])
        return {"p25": float(p25), "p50": float(p50), "p75": float(p75), "iqr": float(p75 - p25)}

    @staticmethod
    def flag_outliers_z(df: pd.DataFrame, col: str, z: float = 3.0) -> pd.Series:
        s = _MU._num_series(df, col)
        m = s.mean(skipna=True)
        sd = s.std(skipna=True, ddof=1)
        if not np.isfinite(m) or not np.isfinite(sd) or sd == 0 or s.isna().all():
            return pd.Series(False, index=df.index)
        return (np.abs((s - m) / sd) > z).fillna(False)

    @staticmethod
    def flag_outliers_iqr(df: pd.DataFrame, col: str, k: float = 1.5) -> pd.Series:
        s = _MU._num_series(df, col)
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        if not np.isfinite(q1) or not np.isfinite(q3):
            return pd.Series(False, index=df.index)
        iqr = q3 - q1
        low, high = q1 - k * iqr, q3 + k * iqr
        return ((s < low) | (s > high)).fillna(False)

    @staticmethod
    def correlation_matrix(df: pd.DataFrame, method: str = "pearson") -> pd.DataFrame:
        num = df.select_dtypes(include=[np.number]).copy()
        if num.empty:
            return pd.DataFrame()
        return num.corr(method=method)

    # ---- Series de tiempo ----
    @staticmethod
    def _prep_ts(df: pd.DataFrame, date_col: str, val_col: str, freq: str, agg: str) -> pd.Series:
        d = pd.to_datetime(df[date_col], errors="coerce")
        v = pd.to_numeric(df[val_col], errors="coerce")
        ts = pd.DataFrame({"date": d, "val": v}).dropna()
        if ts.empty:
            return pd.Series(dtype=float)
        ts = ts.set_index("date").sort_index()
        if freq not in {"D", "W", "M"}:
            freq = "M"
        if agg == "sum":
            s = ts["val"].resample(freq).sum(min_count=1)
        else:
            s = ts["val"].resample(freq).mean()
        return s

    @staticmethod
    def rolling_sma(df: pd.DataFrame, date_col: str, val_col: str, window: int = 6, freq: str = "M", agg: str = "sum") -> pd.DataFrame:
        s = _MU._prep_ts(df, date_col, val_col, freq, agg)
        if s.empty:
            return pd.DataFrame()
        out = pd.DataFrame({val_col: s})
        out[f"sma_{window}"] = s.rolling(window=window, min_periods=1).mean()
        return out

    @staticmethod
    def rolling_ema(df: pd.DataFrame, date_col: str, val_col: str, span: int = 6, freq: str = "M", agg: str = "sum") -> pd.DataFrame:
        s = _MU._prep_ts(df, date_col, val_col, freq, agg)
        if s.empty:
            return pd.DataFrame()
        out = pd.DataFrame({val_col: s})
        out[f"ema_{span}"] = s.ewm(span=span, adjust=False, min_periods=1).mean()
        return out

    @staticmethod
    def monthly_growth(df: pd.DataFrame, date_col: str, val_col: str, agg: str = "sum") -> pd.DataFrame:
        s = _MU._prep_ts(df, date_col, val_col, "M", agg)
        if s.empty:
            return pd.DataFrame(columns=["value", "mom_pct"])
        out = pd.DataFrame({"value": s})
        out["mom_pct"] = out["value"].pct_change() * 100.0
        return out

    @staticmethod
    def cagr(df: pd.DataFrame, date_col: str, val_col: str, agg: str = "sum") -> Optional[float]:
        s = _MU._prep_ts(df, date_col, val_col, "M", agg)
        if s.empty or (s.first_valid_index() is None) or (s.last_valid_index() is None):
            return None
        start, end = s.iloc[0], s.iloc[-1]
        if not (np.isfinite(start) and np.isfinite(end)) or start <= 0 or end <= 0:
            return None
        n_years = max((len(s) / 12.0), 0.001)  # años aprox
        val = (end / start) ** (1.0 / n_years) - 1.0
        return float(val * 100.0)

    @staticmethod
    def linear_trend(df: pd.DataFrame, date_col: str, val_col: str, freq: str = "M", agg: str = "sum") -> Dict[str, float]:
        s = _MU._prep_ts(df, date_col, val_col, freq, agg).dropna()
        if len(s) < 2:
            return {"slope": np.nan, "r2": np.nan}
        x = np.arange(len(s), dtype=float)
        y = s.values.astype(float)
        slope, intercept = np.polyfit(x, y, 1)
        yhat = slope * x + intercept
        ss_res = float(((y - yhat) ** 2).sum())
        ss_tot = float(((y - y.mean()) ** 2).sum())
        r2 = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else np.nan
        return {"slope": float(slope), "r2": float(r2)}

mu = _MU()

# --- compat: rerun para cualquier versión de Streamlit ---
def _rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()  # type: ignore[attr-defined]

# --- Spark + Mongo (opcional) ---
USE_SPARK = os.getenv("USE_SPARK", "false").strip().lower() == "true"
USE_SPARK_MONGO = os.getenv("USE_SPARK_MONGO", "false").strip().lower() == "true"

SPARK_AVAILABLE = False
_spark_import_error = ""
if USE_SPARK and USE_SPARK_MONGO:
    try:
        from spark_mongo import get_spark, read_mongo, write_mongo  # type: ignore
        SPARK_AVAILABLE = True
    except Exception as e:
        SPARK_AVAILABLE = False
        _spark_import_error = str(e)

# ================== APP CONFIG ==================
st.set_page_config(page_title="Datos de Trabajadores", page_icon="🧑‍💼", layout="wide")

# --------- ENV / defaults ----------
DATA_DIR  = os.getenv("DATA_DIR", "./data")
CSV_FILE  = os.getenv("CSV_FILE", "people-1000000.csv")
CSV_PATH  = os.path.abspath(os.path.join(DATA_DIR, CSV_FILE))

MONGO_URI  = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
MONGO_DB   = os.getenv("MONGO_DB", "cruddb")
MONGO_COLL = os.getenv("MONGO_COLL", "customers")
DISABLE_MONGO = os.getenv("DISABLE_MONGO", "false").strip().lower() == "true"

# === Límites anti-OOM para lectura con Spark ===
USE_MONGO_PIPELINE = os.getenv("USE_MONGO_PIPELINE", "true").strip().lower() == "true"
SPARK_READ_LIMIT = int(os.getenv("SPARK_READ_LIMIT", "200000"))  # 0 = sin límite (no recomendado)

os.makedirs(DATA_DIR, exist_ok=True)
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

# ================== THEME ==================
# ================== THEME ==================
st.markdown("""
<style>
/*
================================================================================
|                                                                              |
|                       C L A R I T Y   U I                                    |
|                                                                              |
|               DESIGN SYSTEM FOR MODERN DATA APPLICATIONS                     |
|               VERSION: 1.0.0                                                 |
|               AUTHOR: GEMINI ADVANCED DESIGN LABS                          |
|                                                                              |
================================================================================
*/

/* -------------------------------------------------------------------------- */
/* --- [ 00 ] F U N D A M E N T O S : FUENTES Y VARIABLES GLOBALES --------- */
/* -------------------------------------------------------------------------- */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    /* --- Paleta de Colores --- */
    --color-background: #f0f2f5; /* Gris muy claro */
    --color-surface: #ffffff;
    --color-text-primary: #1f2937; /* Gris oscuro */
    --color-text-secondary: #6b7280; /* Gris medio */
    --color-accent-primary: #3b82f6; /* Azul */
    --color-accent-primary-hover: #2563eb;
    --color-accent-danger: #ef4444;
    --color-accent-danger-hover: #dc2626;
    --color-accent-success: #22c55e;
    --color-border: #e5e7eb; /* Gris claro */

    /* --- Tipografía --- */
    --font-family: 'Inter', sans-serif;

    /* --- Métricas y Espaciado --- */
    --radius-xl: 16px;
    --radius-l: 12px;
    --radius-m: 8px;
    --radius-s: 4px;
    --spacing-unit: 8px;
    --spacing-xs: calc(var(--spacing-unit) * 0.5);   /* 4px */
    --spacing-s:  calc(var(--spacing-unit) * 1);    /* 8px */
    --spacing-m:  calc(var(--spacing-unit) * 2);    /* 16px */
    --spacing-l:  calc(var(--spacing-unit) * 3);    /* 24px */
    --spacing-xl: calc(var(--spacing-unit) * 4);    /* 32px */

    /* --- Sombras --- */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);

    /* --- Animaciones --- */
    --anim-duration: 0.2s;
    --anim-ease: ease-in-out;
}

/* -------------------------------------------------------------------------- */
/* --- [ 01 ] G L O B A L : BODY, SCROLLBAR, FONDOS ----------------------- */
/* -------------------------------------------------------------------------- */

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: var(--color-background) !important;
    font-family: var(--font-family);
    color: var(--color-text-primary);
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--color-background); }
::-webkit-scrollbar-thumb {
    background-color: var(--color-border);
    border-radius: 8px;
    border: 2px solid var(--color-background);
}
::-webkit-scrollbar-thumb:hover {
    background-color: #d1d5db; /* Gris un poco más oscuro */
}

/* -------------------------------------------------------------------------- */
/* --- [ 02 ] T I P O G R A F Í A : CABECERAS Y TEXTO --------------------- */
/* -------------------------------------------------------------------------- */

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-family);
    font-weight: 700;
    color: var(--color-text-primary);
}

h1 { font-size: 2.25rem; }
h2 { font-size: 1.875rem; }
h3 { font-size: 1.5rem; }

p, span, div, label {
    font-family: var(--font-family);
}

/* -------------------------------------------------------------------------- */
/* --- [ 03 ] L A Y O U T : SIDEBAR Y CONTENEDORES PRINCIPALES ------------ */
/* -------------------------------------------------------------------------- */

[data-testid="stSidebar"] {
    background: var(--color-surface);
    border-right: 1px solid var(--color-border);
    padding: var(--spacing-l);
}

.st-emotion-cache-10trblm { /* Título del sidebar */
    font-weight: 600;
}

/* -------------------------------------------------------------------------- */
/* --- [ 04 ] C O M P O N E N T E S : TARJETAS (CARDS) --------------------- */
/* -------------------------------------------------------------------------- */

.card {
    background: var(--color-surface);
    border-radius: var(--radius-l);
    padding: var(--spacing-l);
    border: 1px solid var(--color-border);
    box-shadow: var(--shadow-sm);
    transition: box-shadow var(--anim-duration) var(--anim-ease), transform var(--anim-duration) var(--anim-ease);
    margin-bottom: var(--spacing-l);
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

/* -------------------------------------------------------------------------- */
/* --- [ 05 ] C O M P O N E N T E S : INDICADORES (KPIs) ------------------ */
/* -------------------------------------------------------------------------- */

.kpi {
    background: #f9fafb; /* Gris extra claro */
    padding: var(--spacing-s) var(--spacing-m);
    border-radius: var(--radius-m);
    text-align: center;
    border: 1px solid var(--color-border);
}

.kpi .big {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--color-accent-primary);
    line-height: 1.2;
}

.kpi .lbl {
    font-size: 0.75rem;
    color: var(--color-text-secondary);
    text-transform: uppercase;
    font-weight: 500;
    letter-spacing: 0.05em;
}

/* -------------------------------------------------------------------------- */
/* --- [ 06 ] I N T E R A C T I V O S : NAVEGACIÓN (SIDEBAR) --------------- */
/* -------------------------------------------------------------------------- */

[data-testid="stSidebar"] .stRadio > div {
    gap: var(--spacing-xs);
}

[data-testid="stSidebar"] .stRadio label {
    padding: var(--spacing-s) var(--spacing-m);
    border-radius: var(--radius-m);
    cursor: pointer;
    color: var(--color-text-secondary);
    font-weight: 500;
    transition: all var(--anim-duration) var(--anim-ease);
}

[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--color-text-primary);
    background: var(--color-background);
}

[data-testid="stSidebar"] .stRadio input:checked + div {
    color: var(--color-accent-primary);
    font-weight: 600;
    background-color: #eff6ff; /* Azul muy claro */
}

/* -------------------------------------------------------------------------- */
/* --- [ 07 ] I N T E R A C T I V O S : BOTONES --------------------------- */
/* -------------------------------------------------------------------------- */

[data-testid="stButton"] button,
[data-testid="stFormSubmitButton"] button {
    background: var(--color-accent-primary);
    color: white;
    border: 1px solid transparent;
    border-radius: var(--radius-m);
    padding: calc(var(--spacing-s) + 2px) var(--spacing-l);
    font-weight: 600;
    transition: all var(--anim-duration) var(--anim-ease);
}

[data-testid="stButton"] button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background: var(--color-accent-primary-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

[data-testid="stButton"] button:active,
[data-testid="stFormSubmitButton"] button:active {
    transform: scale(0.98);
}

/* Botón secundario/de borrado */
[data-testid="stButton"] button.secondary {
    background: var(--color-surface);
    color: var(--color-text-primary);
    border-color: var(--color-border);
}
[data-testid="stButton"] button.secondary:hover {
    background: var(--color-background);
    border-color: #d1d5db;
}

/* Botón de peligro */
[data-testid="stButton"] button.danger {
    background: var(--color-accent-danger);
    color: white;
}
[data-testid="stButton"] button.danger:hover {
    background: var(--color-accent-danger-hover);
}

/* -------------------------------------------------------------------------- */
/* --- [ 08 ] I N T E R A C T I V O S : CAMPOS DE FORMULARIO -------------- */
/* -------------------------------------------------------------------------- */

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: var(--color-surface) !important;
    border: 1px solid var(--color-border) !important;
    border-radius: var(--radius-m) !important;
    color: var(--color-text-primary);
    transition: border-color var(--anim-duration) var(--anim-ease), box-shadow var(--anim-duration) var(--anim-ease);
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stDateInput"] input:focus,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
    border-color: var(--color-accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

/* Labels de los inputs */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stDateInput"] label,
[data-testid="stSelectbox"] label {
    font-weight: 500;
    color: var(--color-text-secondary);
}

/* -------------------------------------------------------------------------- */
/* --- [ 09 ] V I S U A L I Z A C I Ó N : TABLA DE DATOS ------------------ */
/* -------------------------------------------------------------------------- */

[data-testid="stDataEditor"],
[data-testid="stDataFrame"] {
    border: 1px solid var(--color-border);
    border-radius: var(--radius-l);
    overflow: hidden; /* Para que los bordes redondeados se apliquen a la tabla interna */
}

[data-testid="stDataEditor"] .glide-header,
[data-testid="stDataFrame"] .glide-header {
    background: #f9fafb; /* Gris extra claro */
    color: var(--color-text-secondary) !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.8rem;
}

[data-testid="stDataEditor"] .dvn-scroller,
[data-testid="stDataFrame"] .dvn-scroller {
    background: var(--color-surface);
}

[data-testid="stDataEditor"] .glide-cell {
    color: var(--color-text-primary) !important;
}

[data-testid="stDataEditor"] .dvn-row:hover .glide-cell {
    background-color: #eff6ff !important; /* Azul muy claro */
}

[data-testid="stDataEditor"] .glide-cell.is-focused {
    box-shadow: 0 0 0 2px var(--color-accent-primary) inset !important;
}

/* --- Fin del Sistema de Diseño --- */
</style>
""", unsafe_allow_html=True)
# ================== LOGIN ==================
ALLOWED_USERS = {"damian", "david", "alexis"}
PASSWORD_HASH = hashlib.sha256("Hola123".encode("utf-8")).hexdigest()

def check_credentials(user: str, password: str) -> bool:
    if not user or not password:
        return False
    u = user.strip().lower()
    if u not in ALLOWED_USERS:
        return False
    ph = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return ph == PASSWORD_HASH

def render_login():
    st.markdown(
        """
        <div style="max-width: 480px; margin: 80px auto; padding: 2rem;" class="card">
            <h1 style="text-align: center; margin-bottom: 0.5rem;">Acceso</h1>
            <p style="text-align: center; color: var(--color-text-secondary); margin-bottom: 2rem;">
                Ingresa tus credenciales para administrar los datos.
            </p>
        """,
        unsafe_allow_html=True,
    )
    with st.container():
        with st.form("login_form", clear_on_submit=False):
            user = st.text_input("Usuario", placeholder="damian / david / alexis")
            pwd = st.text_input("Contraseña", type="password", placeholder="••••••••")
            submit = st.form_submit_button("Entrar", use_container_width=True)

        if submit:
            if check_credentials(user, pwd):
                st.session_state.authenticated = True
                st.session_state.user = user.strip().lower()
                _rerun()
            else:
                st.error("Credenciales inválidas.")
    st.markdown('</div>', unsafe_allow_html=True)

# ================== MONGO (PyMongo para upserts finos) ==================
mongo_ok = False
mongo_err = ""
collection = None
if not DISABLE_MONGO and ENABLE_MONGO_SYNC:
    try:
        from pymongo import MongoClient, UpdateOne  # type: ignore
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=4000)
        _client.admin.command("ping")
        collection = _client[MONGO_DB][MONGO_COLL]
        mongo_ok = True
    except Exception as e:
        mongo_ok = False
        mongo_err = str(e)
else:
    mongo_err = "Mongo deshabilitado por DISABLE_MONGO=true o ENABLE_MONGO_SYNC=false"

def mongo_upsert(doc: Dict[str, Any], pk: str):
    if not mongo_ok: return
    key = doc.get(pk)
    if key is None: return
    collection.update_one({pk: key}, {"$set": doc}, upsert=True)

def mongo_upsert_many(rows: List[Dict[str, Any]], pk: str):
    if not mongo_ok or not rows: return
    from pymongo import UpdateOne  # type: ignore
    ops = []
    for d in rows:
        k = d.get(pk)
        if k is None: continue
        ops.append(UpdateOne({pk: k}, {"$set": d}, upsert=True))
    if ops: collection.bulk_write(ops, ordered=False)

def mongo_delete_many(keys: List[Any], pk: str):
    if not mongo_ok or not keys: return
    collection.delete_many({pk: {"$in": list(keys)}})

# ================== CSV I/O (fallback) ==================
def read_csv_any() -> pd.DataFrame:
    if not os.path.isfile(CSV_PATH):
        pd.DataFrame().to_csv(CSV_PATH, index=False)
        return pd.DataFrame()
    try:
        return pd.read_csv(CSV_PATH, low_memory=False)
    except Exception:
        return pd.DataFrame()

def write_csv_any(df: pd.DataFrame) -> None:
    df.to_csv(CSV_PATH, index=False)

# ========= Normalización de schema =========
RENAMES_MAP = {
    "_id": "mongo_id",
    "phone": "phone",
    "telefono": "phone",
    "user id": "user_id",
    "first name": "first_name",
    "last name": "last_name",
    "sex": "sex",
    "email": "email",
    "e-mail": "email",
    "date of birth": "dob",
    "job title": "job_title",
    "index": "index_original",
}

def _rename_columns_loose(pdf: pd.DataFrame) -> pd.DataFrame:
    if pdf is None or pdf.empty:
        return pd.DataFrame()
    m = {}
    for c in pdf.columns:
        lc = str(c).strip().lower()
        m[c] = RENAMES_MAP.get(lc, c)
    out = pdf.rename(columns=m)
    out = out.loc[:, ~out.columns.duplicated()].copy()
    return out

def _unify_email(df: pd.DataFrame) -> pd.DataFrame:
    alt_cols = [c for c in df.columns if c.lower() in ("email", "e-mail")]
    if "email" not in df.columns and alt_cols:
        df["email"] = df[alt_cols[0]]
    if "email" in df.columns:
        df["email"] = df["email"].astype(str).str.strip().str.lower()
    return df

def _normalize_customers_df(pdf: pd.DataFrame) -> pd.DataFrame:
    cols_target = ["id","name","email","phone","sex","dob","job_title",
                   "balance","created_at","created_ym",
                   "user_id","first_name","last_name","mongo_id"]

    if pdf is None or pdf.empty:
        return pd.DataFrame(columns=cols_target)

    df = _rename_columns_loose(pdf).copy()
    df = _unify_email(df)

    if "name" not in df.columns:
        if "first_name" in df.columns or "last_name" in df.columns:
            fn = df["first_name"].fillna("").astype(str) if "first_name" in df.columns else ""
            ln = df["last_name"].fillna("").astype(str) if "last_name" in df.columns else ""
            df["name"] = (fn + " " + ln).str.strip()
        else:
            df["name"] = np.nan

    if "phone" in df.columns:
        df["phone"] = df["phone"].astype(str)

    if "dob" in df.columns:
        df["dob"] = pd.to_datetime(df["dob"], errors="coerce")
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    if "created_ym" in df.columns:
        df["created_ym"] = df["created_ym"].astype(str)

    if "balance" in df.columns:
        df["balance"] = pd.to_numeric(df["balance"], errors="coerce")

    need_auto = ("id" not in df.columns)
    if not need_auto:
        tmp = pd.to_numeric(df["id"], errors="coerce")
        need_auto = tmp.isna().any() or tmp.duplicated().any()
    if need_auto:
        df["id"] = pd.RangeIndex(1, len(df) + 1)
    else:
        df["id"] = pd.to_numeric(df["id"], errors="coerce")
        if df["id"].isna().any() or df["id"].duplicated().any():
            df["id"] = pd.RangeIndex(1, len(df) + 1)

    ordered = [c for c in cols_target if c in df.columns]
    df = df[ordered + [c for c in df.columns if c not in ordered]]

    return df

def _next_id(current_df: pd.DataFrame) -> int:
    if current_df is None or current_df.empty or "id" not in current_df.columns:
        return 1
    m = pd.to_numeric(current_df["id"], errors="coerce").max()
    if pd.isna(m): return 1
    return int(m) + 1

# ================== Barra de progreso (visual, genérica) ==================
@contextmanager
def ui_progress(task: str, est_steps: int = 5):
    holder = st.empty()
    bar = holder.progress(0, text=f"🔄 {task} — preparando…")
    step = {"v": 0}
    def tick(msg: str, add_steps: int = 1):
        step["v"] += max(add_steps, 1)
        p = min(int(step["v"] / max(est_steps,1) * 100), 99)
        bar.progress(p, text=f"🔄 {task} — {msg}")
    try:
        yield tick
        bar.progress(100, text=f"✅ {task} — listo")
        time.sleep(0.25)
    except Exception as e:
        bar.progress(100, text=f"❌ {task} — error: {e}")
        raise
    finally:
        time.sleep(0.15)
        holder.empty()

# ================== Carga de datos ==================
def _build_pipeline_json() -> Optional[str]:
    # (Se mantiene por compatibilidad Spark-Mongo si lo activas luego)
    if not USE_MONGO_PIPELINE:
        return None
    pipeline = [
        {"$addFields": {
            "Phone": {
                "$cond": [
                    {"$isArray": "$Phone"},
                    {"$arrayElemAt": ["$Phone", 0]},
                    "$Phone"
                ]
            }
        }},
        {"$addFields": {
            "Phone": {"$convert": {"input": "$Phone", "to": "string", "onError": "", "onNull": ""}},
            "id":          {"$convert": {"input": "$id",          "to": "string", "onError": "",   "onNull": ""}},
            "Index":       {"$convert": {"input": "$Index",       "to": "string", "onError": "",   "onNull": ""}},
            "User Id":     {"$convert": {"input": "$User Id",     "to": "string", "onError": "",   "onNull": ""}},
            "balance":     {"$convert": {"input": "$balance",     "to": "double", "onError": None, "onNull": None}},
            "created_at":  {"$convert": {"input": "$created_at",  "to": "date",   "onError": None, "onNull": None}},
            "Date of birth":{"$convert":{"input":"$Date of birth","to":"date",    "onError": None, "onNull": None}},
        }},
        {"$project": {
            "_id": 1, "Index": 1, "User Id": 1, "First Name": 1, "Last Name": 1,
            "Sex": 1, "Email": 1, "Phone": 1, "Date of birth": 1, "Job Title": 1,
            "id": 1, "balance": 1, "created_at": 1, "created_ym": 1, "email": 1, "name": 1
        }}
    ]
    if SPARK_READ_LIMIT and SPARK_READ_LIMIT > 0:
        pipeline.append({"$limit": int(SPARK_READ_LIMIT)})
    return json.dumps(pipeline)

def load_dataframe() -> pd.DataFrame:
    """Carga desde Mongo con Spark si está disponible; si no, cae a CSV con barra de progreso."""
    # Spark + Mongo (opcional)
    if USE_SPARK and USE_SPARK_MONGO and SPARK_AVAILABLE and (not DISABLE_MONGO) and ENABLE_MONGO_SYNC:
        try:
            with ui_progress("Leyendo desde Mongo (Spark)", est_steps=6) as tick:
                tick("creando sesión")
                spark = get_spark()  # type: ignore

                tick("preparando pipeline")
                pipe = _build_pipeline_json()

                tick("ejecutando lectura")
                sdf = read_mongo(MONGO_DB, MONGO_COLL, pipeline=pipe)  # type: ignore

                try:
                    from pyspark.sql import DataFrame as SparkDF  # type: ignore
                    is_spark_df = isinstance(sdf, SparkDF)
                except Exception:
                    is_spark_df = False

                if (not pipe) and SPARK_READ_LIMIT and SPARK_READ_LIMIT > 0 and is_spark_df:
                    tick(f"aplicando límite {SPARK_READ_LIMIT:,}")
                    sdf = sdf.limit(int(SPARK_READ_LIMIT))  # type: ignore

                tick("convirtiendo a pandas")
                pdf = sdf.toPandas() if is_spark_df else pd.DataFrame(sdf)  # type: ignore

                if not pdf.empty:
                    tick("normalizando schema")
                    pdf = _normalize_customers_df(pdf)
                    if SPARK_READ_LIMIT and SPARK_READ_LIMIT > 0:
                        st.caption(f"⚠️ Cargadas máximo {len(pdf):,} filas (SPARK_READ_LIMIT). Ajusta en .env si quieres más.")
                    return pdf
        except Exception as e:
            st.warning(f"No pude leer Mongo con Spark: {e}. Fallback a CSV.")

    # CSV (fallback) — aquí añadimos barra de progreso
    with ui_progress("Leyendo CSV", est_steps=4) as tick:
        tick("verificando archivo")
        if not os.path.isfile(CSV_PATH):
            tick("creando CSV vacío")
            pd.DataFrame().to_csv(CSV_PATH, index=False)
            return pd.DataFrame()

        tick("leyendo datos")
        pdf = read_csv_any()

        tick("normalizando")
        out = _normalize_customers_df(pdf) if not pdf.empty else pdf

    return out

# ================== PK/VALIDACIÓN ==================
def detect_pk(df: pd.DataFrame) -> str:
    if df.empty: return "id"
    pri = [c for c in df.columns if c.lower() == "id"]
    if pri: return pri[0]
    for name in ["person_id", "customer_id", "_id"]:
        for c in df.columns:
            if c.lower() == name:
                return c
    return df.columns[0]

def is_na(val: Any) -> bool:
    try:
        return pd.isna(val)
    except Exception:
        return False

def validate_row(row: Dict[str, Any], pk: str) -> Tuple[bool, str]:
    val = row.get(pk)
    if val is None or (isinstance(val, str) and val.strip() == "") or is_na(val):
        return False, f"La PK '{pk}' no puede ir vacía."
    for k, v in row.items():
        if v is None or is_na(v): continue
        if "mail" in k.lower():
            s = str(v).strip()
            if s and not EMAIL_RE.match(s):
                return False, f"Email inválido en columna '{k}'."
    return True, ""

def normalize_new_row(inputs: Dict[str, Any], schema_cols: List[str]) -> Dict[str, Any]:
    row = {c: inputs.get(c, None) for c in schema_cols}
    for c in schema_cols:
        lc = c.lower()
        v = row[c]
        if isinstance(v, date) and not isinstance(v, datetime):
            row[c] = datetime.combine(v, datetime.min.time())
        elif any(tok in lc for tok in ["date", "created", "updated", "dob"]):
            if isinstance(v, str) and v.strip():
                parsed = pd.to_datetime(v, errors="coerce")
                if not is_na(parsed): row[c] = parsed
    return row

# ================== CACHE UTILS (Analytics) ==================
@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def _coerce_numeric_cols(df: pd.DataFrame) -> pd.DataFrame:
    out = {}
    for c in df.columns:
        s = pd.to_numeric(df[c], errors="coerce")
        if s.notna().sum() > 0:
            out[c] = s
    return pd.DataFrame(out)

@st.cache_data(ttl=CACHE_TTL_SECONDS, show_spinner=False)
def _coerce_datetime_cols(df: pd.DataFrame) -> pd.DataFrame:
    out = {}
    for c in df.columns:
        d = pd.to_datetime(df[c], errors="coerce")
        if d.notna().sum() > 0:
            out[c] = d
    return pd.DataFrame(out)

def _guess_date_col(df: pd.DataFrame) -> Optional[str]:
    candidates = [c for c in df.columns if any(tok in c.lower() for tok in DATE_HINTS)]
    for c in candidates:
        if pd.to_datetime(df[c], errors="coerce").notna().any():
            return c
    for c in df.columns:
        if pd.to_datetime(df[c], errors="coerce").notna().any():
            return c
    return None

# ================== STATE ==================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "pk" not in st.session_state:
    st.session_state.pk = None

# ================== GATE ==================
if not st.session_state.authenticated:
    render_login()
    st.stop()

# ================== NAV (solo si autenticado) ==================
with st.sidebar:
    st.markdown("### 🧭 Navegación")
    page = st.radio("Navegación", ["🏠 Dashboard", "📚 Registros", "📈 Analytics", "⚙️ Configuración"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"Conectado como **{st.session_state.user.capitalize()}**")
    if st.button("Cerrar sesión", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        _rerun()

# ================== DATA + PK ==================
df = load_dataframe()
pk_default = detect_pk(df)
if st.session_state.pk is None:
    st.session_state.pk = pk_default
pk = st.session_state.pk

# ================== HEADER ==================
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap; margin-bottom: 24px;">
  <div>
    <h1 style="margin-bottom: 0;">Gestor de Trabajadores</h1>
    <p style="color: var(--color-text-secondary); margin-top: 4px;">CRUD completo con Analytics y conexión a Mongo/Spark.</p>
  </div>
  <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-top: 8px;">
    <span class="kpi"><div class="big">{pk}</div><div class="lbl">PK</div></span>
    <span class="kpi"><div class="big">{len(df):,}</div><div class="lbl">Filas</div></span>
    <span class="kpi"><div class="big">{len(df.columns) if not df.empty else 0}</div><div class="lbl">Cols</div></span>
  </div>
</div>
""", unsafe_allow_html=True)

# ================== HELPERS UI ==================
def paginate(view: pd.DataFrame, page: int, page_size: int) -> pd.DataFrame:
    start = (page-1)*page_size
    end = start + page_size
    return view.iloc[start:end].reset_index(drop=True)

def _contains_ci(s: pd.Series, q: str) -> pd.Series:
    if q is None or str(q).strip() == "":
        return pd.Series(True, index=s.index)
    return s.astype(str).str.contains(str(q), case=False, na=False)

def _between_num(s: pd.Series, vmin: Optional[float], vmax: Optional[float]) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    mask = pd.Series(True, index=s.index)
    if vmin is not None:
        mask &= x >= vmin
    if vmax is not None:
        mask &= x <= vmax
    return mask.fillna(False)

def _between_date(s: pd.Series, dmin: Optional[date], dmax: Optional[date]) -> pd.Series:
    x = pd.to_datetime(s, errors="coerce")
    mask = pd.Series(True, index=s.index)
    if dmin is not None:
        mask &= x >= pd.Timestamp(dmin)
    if dmax is not None:
        mask &= x <= pd.Timestamp(dmax) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    return mask.fillna(False)

def _apply_advanced_filters(df: pd.DataFrame, f: Dict[str, Any]) -> pd.DataFrame:
    if df.empty: return df
    m = pd.Series(True, index=df.index)

    for key in ["name","first_name","last_name","email","phone","job_title","user_id","mongo_id"]:
        if key in df.columns and f.get(key):
            m &= _contains_ci(df[key], f[key])

    if "sex" in df.columns and f.get("sex") and f["sex"] != "Todos":
        m &= df["sex"].astype(str).str.lower() == str(f["sex"]).lower()

    if "created_ym" in df.columns and f.get("created_ym") and f["created_ym"] != "Todos":
        m &= df["created_ym"].astype(str) == str(f["created_ym"])

    if "id" in df.columns:
        m &= _between_num(df["id"], f.get("id_min"), f.get("id_max"))
    if "balance" in df.columns:
        m &= _between_num(df["balance"], f.get("bal_min"), f.get("bal_max"))

    if "dob" in df.columns:
        m &= _between_date(df["dob"], f.get("dob_min"), f.get("dob_max"))
    if "created_at" in df.columns:
        m &= _between_date(df["created_at"], f.get("crt_min"), f.get("crt_max"))

    return df[m].copy()

def _filters_ui(df: pd.DataFrame) -> Dict[str, Any]:
    st.markdown("### 🎯 Filtros avanzados")
    f: Dict[str, Any] = {}

    r1 = st.columns(4)
    if "name" in df.columns:       f["name"] = r1[0].text_input("Nombre contiene", "")
    if "first_name" in df.columns:  f["first_name"] = r1[1].text_input("First Name contiene", "")
    if "last_name" in df.columns:   f["last_name"] = r1[2].text_input("Last Name contiene", "")
    if "job_title" in df.columns:   f["job_title"] = r1[3].text_input("Job Title contiene", "")

    r2 = st.columns(4)
    if "email" in df.columns:       f["email"] = r2[0].text_input("Email contiene", "")
    if "phone" in df.columns:       f["phone"] = r2[1].text_input("Phone contiene", "")
    if "user_id" in df.columns:     f["user_id"] = r2[2].text_input("User Id contiene", "")
    if "mongo_id" in df.columns:    f["mongo_id"] = r2[3].text_input("Mongo _id contiene", "")

    r3 = st.columns(4)
    if "sex" in df.columns:
        sex_opts = ["Todos"] + sorted([s for s in df["sex"].dropna().astype(str).str.strip().unique().tolist() if s])
        f["sex"] = r3[0].selectbox("Sexo", options=sex_opts, index=0)
    if "created_ym" in df.columns:
        ym_opts = ["Todos"] + sorted([s for s in df["created_ym"].dropna().astype(str).unique().tolist() if s])
        f["created_ym"] = r3[1].selectbox("created_ym (YYYY-MM)", options=ym_opts, index=0)
    if "id" in df.columns:
        f["id_min"] = r3[2].number_input("ID mín.", value=0, step=1)
        f["id_max"] = r3[3].number_input("ID máx.", value=int(df["id"].max()) if not df.empty else 0, step=1)

    r4 = st.columns(4)
    if "balance" in df.columns:
        f["bal_min"] = r4[0].number_input("Balance mín.", value=0.0, step=100.0, format="%.2f")
        max_bal = float(np.nan_to_num(df["balance"].max(), nan=0.0)) if "balance" in df.columns else 0.0
        f["bal_max"] = r4[1].number_input("Balance máx.", value=max_bal, step=100.0, format="%.2f")
    if "dob" in df.columns:
        f["dob_min"] = r4[2].date_input("DOB desde", value=None)
        f["dob_max"] = r4[3].date_input("DOB hasta", value=None)

    r5 = st.columns(2)
    if "created_at" in df.columns:
        f["crt_min"] = r5[0].date_input("created_at desde", value=None)
        f["crt_max"] = r5[1].date_input("created_at hasta", value=None)

    return f

# ================== PAGES ==================
def page_dashboard():
    if df.empty:
        st.info("Tu CSV/Mongo está vacío. Ve a **Registros** para crear el primer trabajador.")
        return

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔎 Búsqueda rápida")
    c1, c2, c3 = st.columns([1.4,1.4,1])
    with c1:
        col = st.selectbox("Columna", options=list(df.columns),
                           index=(list(df.columns).index(pk) if pk in df.columns else 0))
    with c2:
        q = st.text_input("Valor contiene", "")
    with c3:
        page_size = st.selectbox("Filas/página", [10,25,50,100], index=1)

    view = df.copy()
    if q.strip():
        view = view[view[col].astype(str).str.contains(q, case=False, na=False)]

    total = len(view)
    total_pages = max(1, math.ceil(total / page_size))
    if "dash_page" not in st.session_state:
        st.session_state.dash_page = 1
    st.number_input("Página", min_value=1, max_value=total_pages, step=1, key="dash_page")
    st.caption(f"Total: {total:,} • Páginas: {total_pages}")

    page_df = paginate(view, st.session_state.dash_page, page_size)
    st.dataframe(page_df, width='stretch', height=420)  # <- reemplazo de use_container_width
    st.download_button("⬇️ Exportar vista (CSV)",
                       data=view.to_csv(index=False).encode("utf-8"),
                       file_name="trabajadores_vista.csv", mime="text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

def page_registros():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("➕ Alta / Upsert")
    with st.form("create_form", clear_on_submit=True):
        inputs: Dict[str, Any] = {}
        cols_to_render = list(df.columns) if not df.empty else ["id","name","email","phone","sex","dob","job_title","balance","created_at","created_ym"]
        grid = st.columns(3) if cols_to_render else []
        for i, col in enumerate(cols_to_render):
            box = grid[i % 3]
            lc = col.lower()
            if col == "id":
                nxt = _next_id(df)
                inputs[col] = box.text_input(col, value=str(nxt), disabled=True)
                continue
            if lc in ("dob","created_at","updated_at","date"):
                inputs[col] = box.date_input(col, value=date.today())
            elif "mail" in lc:
                inputs[col] = box.text_input(col, value="")
            elif lc in ("balance","amount","price","score","salary"):
                inputs[col] = box.number_input(col, value=0.0, step=100.0, format="%.2f")
            else:
                inputs[col] = box.text_input(col, value="")
        submitted = st.form_submit_button("💾 Guardar")
        if submitted:
            with ui_progress("Guardando registro", est_steps=3) as tick:
                tick("preparando datos")
                work = df.copy()
                schema = list(work.columns) if not work.empty else list(dict.fromkeys(["id", *inputs.keys()]))
                inputs["id"] = _next_id(work)
                row = normalize_new_row(inputs, schema)
                ok, msg = validate_row(row, "id")
                if not ok:
                    st.error(msg)
                else:
                    tick("aplicando cambios")
                    if work.empty:
                        work = pd.DataFrame(columns=schema)
                    if "id" not in work.columns:
                        work["id"] = pd.NA
                    mask = work["id"].astype(str) == str(row["id"])
                    if mask.any():
                        for c in schema:
                            if c not in work.columns: work[c] = pd.NA
                            work.loc[mask, c] = row.get(c, None)
                    else:
                        for c in schema:
                            if c not in work.columns: work[c] = pd.NA
                        work = pd.concat([work, pd.DataFrame([row])], ignore_index=True)
                    tick("escribiendo CSV / Mongo")
                    write_csv_any(work)
                    mongo_upsert(row, "id")
                    st.success(f"Upsert OK (id={row['id']}).")
                    _rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("No hay registros aún.")
        return

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧹 Filtrar, ordenar y editar")
    filters = _filters_ui(df)
    v = _apply_advanced_filters(df, filters)

    f1, f2 = st.columns([1,1])
    with f1:
        sort_by = st.selectbox("Ordenar por", options=list(v.columns),
                               index=(list(v.columns).index("id") if "id" in v.columns else 0))
    with f2:
        page_size = st.selectbox("Filas/página", [10,25,50,100], index=1)

    v = v.sort_values(sort_by, na_position="last").reset_index(drop=True)

    total = len(v)
    total_pages = max(1, math.ceil(total / page_size))
    if "reg_page" not in st.session_state:
        st.session_state.reg_page = 1
    st.number_input("Página", min_value=1, max_value=total_pages, step=1, key="reg_page")
    st.caption(f"Total (filtrado): {total:,} • Páginas: {total_pages}")

    SEL = "__select__"
    page_df = paginate(v, st.session_state.reg_page, page_size)
    if SEL not in page_df.columns: page_df.insert(0, SEL, False)

    # Bloquear edición de 'id' y 'mongo_id'
    colcfg = {}
    if "id" in page_df.columns:
        colcfg["id"] = st.column_config.NumberColumn("id", disabled=True)
    if "mongo_id" in page_df.columns:
        colcfg["mongo_id"] = st.column_config.TextColumn("mongo_id", disabled=True)

    edited = st.data_editor(
        page_df,
        width='stretch',         # <- reemplazo de use_container_width
        height=460,
        num_rows="dynamic",
        column_config=colcfg,
        key=f"grid_{st.session_state.reg_page}_{page_size}_{sort_by}"
    )

    a1, a2, a3 = st.columns([1,1,1])
    with a1:
        if st.button("✅ Guardar cambios (CSV + Mongo)", key="save_changes"):
            try:
                with ui_progress("Guardando cambios", est_steps=3) as tick:
                    tick("preparando merge")
                    base = df.set_index("id").copy()
                    upd = edited.drop(columns=[SEL]).set_index("id")
                    tick("aplicando a DataFrame")
                    base.update(upd)
                    base = base.reset_index()
                    tick("escribiendo CSV/Mongo")
                    write_csv_any(base)
                    if mongo_ok:
                        keys = upd.index.dropna().tolist()
                        docs = base[base["id"].isin(keys)].to_dict(orient="records")
                        mongo_upsert_many(docs, "id")
                st.success("Cambios guardados.")
                _rerun()
            except Exception as e:
                st.error(f"No pude guardar: {e}")
    with a2:
        if st.button("🗑️ Eliminar seleccionados (CSV + Mongo)", key="delete_sel"):
            try:
                with ui_progress("Eliminando filas", est_steps=3) as tick:
                    tick("detectando selección")
                    keys = edited.loc[edited[SEL] == True, "id"]
                    if keys.empty:
                        st.warning("Selecciona al menos 1 fila.")
                    else:
                        keys = keys.dropna()
                        tick("borrando en DataFrame")
                        df2 = df[~(df["id"].isin(keys))]
                        tick("escribiendo CSV/Mongo")
                        write_csv_any(df2)
                        if mongo_ok: mongo_delete_many(list(keys), "id")
                        st.success(f"Eliminados: {len(keys)}.")
                        _rerun()
            except Exception as e:
                st.error(f"No pude eliminar: {e}")
    with a3:
        st.download_button("⬇️ Exportar vista (CSV)",
                           data=v.to_csv(index=False).encode("utf-8"),
                           file_name="trabajadores_filtrado.csv", mime="text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

def page_analytics():
    if not ENABLE_ANALYTICS:
        st.warning("Analytics deshabilitado en settings.py / ENV.")
        return
    if df.empty:
        st.info("No hay datos para analizar. Carga o crea registros primero.")
        return

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Descriptivos & Outliers")

    num_df = _coerce_numeric_cols(df)
    if num_df.empty:
        st.info("No se detectaron columnas numéricas.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        col_default = "balance" if "balance" in num_df.columns else list(num_df.columns)[0]
        col_num = st.selectbox(
            "Columna numérica",
            options=list(num_df.columns),
            index=list(num_df.columns).index(col_default)
        )

        stats = mu.describe_numeric(df, col_num)
        pct = mu.percentiles_iqr(df, col_num)
        out_z = mu.flag_outliers_z(df, col_num, z=OUTLIER_Z_THRESHOLD)
        out_i = mu.flag_outliers_iqr(df, col_num, k=OUTLIER_IQR_K)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Promedio", f"{stats['mean']:.2f}" if np.isfinite(stats['mean']) else "—")
        k2.metric("Mediana", f"{stats['median']:.2f}" if np.isfinite(stats['median']) else "—")
        k3.metric("σ (std)", f"{stats['std']:.2f}" if np.isfinite(stats['std']) else "—")
        k4.metric("Suma", f"{stats['sum']:.2f}" if np.isfinite(stats['sum']) else "—")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("P25", f"{pct['p25']:.2f}" if np.isfinite(pct['p25']) else "—")
        c2.metric("P50", f"{pct['p50']:.2f}" if np.isfinite(pct['p50']) else "—")
        c3.metric("P75", f"{pct['p75']:.2f}" if np.isfinite(pct['p75']) else "—")
        c4.metric("IQR", f"{pct['iqr']:.2f}" if np.isfinite(pct['iqr']) else "—")

        zc, ic, tc = int(out_z.sum()), int(out_i.sum()), len(df)
        st.caption(f"Outliers (Z>{OUTLIER_Z_THRESHOLD}): **{zc:,}**  •  Outliers (IQR*k, k={OUTLIER_IQR_K}): **{ic:,}**  •  Total filas: **{tc:,}**")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔗 Correlaciones")

    method = st.selectbox(
        "Método",
        options=["pearson", "spearman", "kendall"],
        index=["pearson", "spearman", "kendall"].index(
            ANALYTICS_CORR_METHOD if ANALYTICS_CORR_METHOD in ["pearson", "spearman", "kendall"] else "pearson"
        ),
    )
    corr = mu.correlation_matrix(df, method=method)
    if corr.empty:
        st.info("No hay suficientes columnas numéricas para correlación.")
    else:
        st.dataframe(corr, width='stretch', height=380)  # <- reemplazo de use_container_width
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⏱️ Series de tiempo: SMA / EMA / Crecimiento / Tendencia")

    date_guess = _guess_date_col(df)
    date_cols = [date_guess] + [c for c in df.columns if c != date_guess] if date_guess else list(df.columns)
    date_col = st.selectbox("Columna de fecha", options=date_cols, index=0 if date_guess else 0)

    num_df2 = _coerce_numeric_cols(df)
    if num_df2.empty:
        st.info("No hay métricas numéricas para series.")
    else:
        val_default = "balance" if "balance" in num_df2.columns else list(num_df2.columns)[0]
        val_col = st.selectbox("Métrica numérica", options=list(num_df2.columns),
                               index=list(num_df2.columns).index(val_default))
        freq = st.selectbox("Frecuencia", options=["D","W","M"],
                            index=["D","W","M"].index(TIME_GROUPING_FREQ if TIME_GROUPING_FREQ in ["D","W","M"] else "M"))
        w = st.number_input("Ventana SMA (periodos)", min_value=2, max_value=365, value=ROLLING_DEFAULT_WINDOW, step=1)
        s = st.number_input("Span EMA", min_value=2, max_value=365, value=EMA_DEFAULT_SPAN, step=1)

        try:
            with ui_progress("Calculando series", est_steps=4) as tick:
                tick("SMA")
                sma = mu.rolling_sma(df, date_col, val_col, window=int(w), freq=freq, agg="sum")
                tick("EMA")
                ema = mu.rolling_ema(df, date_col, val_col, span=int(s), freq=freq, agg="sum")
                tick("uniendo y graficando")
                ts = sma.join(ema[[f"ema_{int(s)}"]], how="outer")
                st.line_chart(ts, height=320, width='stretch')  # <- ancho estirable
                tick("indicadores")
                mg = mu.monthly_growth(df, date_col, val_col, agg="sum")
                last_mom = float(mg["mom_pct"].iloc[-1]) if not mg.empty and np.isfinite(mg["mom_pct"].iloc[-1]) else np.nan
                kpi1, kpi2 = st.columns(2)
                kpi1.metric("MoM (último mes)", f"{last_mom:.2f}%" if np.isfinite(last_mom) else "—")
                _cagr = mu.cagr(df, date_col, val_col, agg="sum")
                kpi2.metric("CAGR (aprox.)", f"{_cagr:.2f}%" if (_cagr is not None and np.isfinite(_cagr)) else "—")
                trend = mu.linear_trend(df, date_col, val_col, freq=freq, agg="sum")
                st.caption(f"Tendencia: slope={trend['slope']:.4f} • R²={trend['r2']:.4f}" if np.isfinite(trend["slope"]) else "Tendencia: —")
        except Exception as e:
            st.error(f"No pude calcular series de tiempo: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

def page_config():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Configuración")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        new_pk = st.selectbox("Columna clave (PK)", options=(list(df.columns) if not df.empty else ["id"]),
                              index=(list(df.columns).index(pk) if (not df.empty and pk in df.columns) else 0))
        if new_pk != pk:
            st.session_state.pk = new_pk
            st.success(f"PK actualizada a: {new_pk}")
    with c2:
        if mongo_ok:
            st.success(f"Mongo conectado\nDB: {MONGO_DB} • Coll: {MONGO_COLL}")
        else:
            st.warning(f"Mongo no activo: {mongo_err or '—'}")

    st.markdown("---")
    st.subheader("🧩 Integración Spark ⇄ Mongo (opcional)")

    if USE_SPARK and USE_SPARK_MONGO and SPARK_AVAILABLE:
        cA, cB, cC = st.columns([1,1,1])

        with cA:
            if st.button("⬆️ CSV → Mongo (Spark)"):
                try:
                    with ui_progress("CSV → Mongo (Spark)", est_steps=4) as tick:
                        tick("creando sesión")
                        spark = get_spark()  # type: ignore
                        tick("armando Spark DF")
                        sdf = spark.createDataFrame(df)  # type: ignore
                        pk_col = "id" if ("id" in df.columns) else None
                        if pk_col and "_id" not in df.columns:
                            sdf = sdf.withColumnRenamed(pk_col, "_id")  # type: ignore
                        tick("escribiendo en Mongo")
                        write_mongo(sdf, MONGO_DB, MONGO_COLL, mode="append", replace_document=True)  # type: ignore
                    st.success("Sync OK: CSV → Mongo via Spark.")
                except Exception as e:
                    st.error(f"Falló sync a Mongo con Spark: {e}")

        with cB:
            if st.button("⬇️ Mongo → CSV (Spark)"):
                try:
                    with ui_progress("Mongo → CSV (Spark)", est_steps=5) as tick:
                        tick("preparando pipeline")
                        pipe = _build_pipeline_json()
                        tick("leyendo desde Mongo")
                        sdf = read_mongo(MONGO_DB, MONGO_COLL, pipeline=pipe)  # type: ignore

                        try:
                            from pyspark.sql import DataFrame as SparkDF  # type: ignore
                            is_spark_df = isinstance(sdf, SparkDF)
                        except Exception:
                            is_spark_df = False

                        if (not pipe) and SPARK_READ_LIMIT and SPARK_READ_LIMIT > 0 and is_spark_df:
                            tick(f"aplicando límite {SPARK_READ_LIMIT:,}")
                            sdf = sdf.limit(int(SPARK_READ_LIMIT))  # type: ignore

                        tick("convirtiendo a pandas")
                        pdf = sdf.toPandas() if is_spark_df else pd.DataFrame(sdf)  # type: ignore
                        if not pdf.empty:
                            tick("normalizando y guardando CSV")
                            pdf = _normalize_customers_df(pdf)
                            write_csv_any(pdf)
                            st.success(f"Exportado {len(pdf):,} filas de Mongo → CSV.")
                        else:
                            st.info("Mongo vacío o sin datos legibles.")
                except Exception as e:
                    st.error(f"No pude leer de Mongo con Spark: {e}")

        with cC:
            if st.button("🔁 Refrescar DF desde Mongo (Spark)"):
                try:
                    with ui_progress("Refrescar desde Mongo", est_steps=5) as tick:
                        tick("preparando pipeline")
                        pipe = _build_pipeline_json()
                        tick("leyendo dataset")
                        sdf = read_mongo(MONGO_DB, MONGO_COLL, pipeline=pipe)  # type: ignore

                        try:
                            from pyspark.sql import DataFrame as SparkDF  # type: ignore
                            is_spark_df = isinstance(sdf, SparkDF)
                        except Exception:
                            is_spark_df = False

                        if (not pipe) and SPARK_READ_LIMIT and SPARK_READ_LIMIT > 0 and is_spark_df:
                            tick(f"aplicando límite {SPARK_READ_LIMIT:,}")
                            sdf = sdf.limit(int(SPARK_READ_LIMIT))  # type: ignore

                        tick("toPandas")
                        pdf = sdf.toPandas() if is_spark_df else pd.DataFrame(sdf)  # type: ignore
                        if not pdf.empty:
                            tick("normalizando")
                            pdf = _normalize_customers_df(pdf)
                            st.session_state.pk = detect_pk(pdf)
                            globals()['df'] = pdf
                            st.success(f"Datos refrescados desde Mongo ({len(pdf):,} filas).")
                            _rerun()
                        else:
                            st.info("Mongo sin datos.")
                except Exception as e:
                    st.error(f"Falló refresco desde Mongo con Spark: {e}")
    else:
        msg = "Spark-Mongo desactivado"
        if USE_SPARK and USE_SPARK_MONGO and not SPARK_AVAILABLE:
            msg += f" (import falló: {_spark_import_error or 'spark_mongo.py no encontrado'})"
        st.info(msg + ". La app funciona con CSV.")

    st.markdown('</div>', unsafe_allow_html=True)

# ================== ROUTER ==================
if page == "🏠 Dashboard":
    page_dashboard()
elif page == "📚 Registros":
    page_registros()
elif page == "📈 Analytics":
    page_analytics()
else:
    page_config()
