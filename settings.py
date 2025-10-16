# settings.py — Parámetros de la app (tuneables por ENV)
# -------------------------------------------------------
# Todos estos valores pueden sobreescribirse con variables de entorno.
# Ej.: en tu .env ->  ENABLE_ANALYTICS=true  |  PAGE_SIZE=50

import os

# ---------- helpers ----------
def _getenv_bool(key: str, default: bool) -> bool:
    val = os.getenv(key, str(default)).strip().lower()
    return val in {"1", "true", "t", "yes", "y", "on"}

def _getenv_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, str(default)).strip())
    except Exception:
        return default

def _getenv_float(key: str, default: float) -> float:
    try:
        return float(os.getenv(key, str(default)).strip())
    except Exception:
        return default

def _getenv_str(key: str, default: str) -> str:
    v = os.getenv(key, default)
    return v if v is not None and v != "" else default


# ---------- Paginación / Orden ----------
PAGE_SIZE = _getenv_int("PAGE_SIZE", 25)                  # tamaño por página por defecto
DEFAULT_ORDER_COL = _getenv_str("DEFAULT_ORDER_COL", "id")
DEFAULT_ORDER_DIR = _getenv_str("DEFAULT_ORDER_DIR", "asc")  # asc|desc


# ---------- Features ----------
ENABLE_ANALYTICS   = _getenv_bool("ENABLE_ANALYTICS", True)     # habilita pestaña Analytics
ENABLE_MONGO_SYNC  = _getenv_bool("ENABLE_MONGO_SYNC", True)    # escribe/borra también en Mongo


# ---------- Heurísticas de tipos ----------
NUMERIC_HINTS = tuple(
    _getenv_str(
        "NUMERIC_HINTS",
        "balance,amount,price,score,salary,total,qty,count,metric,id,index"
    ).replace(" ", "").split(",")
)

DATE_HINTS = tuple(
    _getenv_str(
        "DATE_HINTS",
        "date,created,updated,dt,timestamp,time,ym,dob"
    ).replace(" ", "").split(",")
)


# ---------- Analytics ----------
ANALYTICS_CORR_METHOD   = _getenv_str("ANALYTICS_CORR_METHOD", "pearson")  # pearson|spearman|kendall
ROLLING_DEFAULT_WINDOW  = _getenv_int("ROLLING_DEFAULT_WINDOW", 6)         # SMA window
EMA_DEFAULT_SPAN        = _getenv_int("EMA_DEFAULT_SPAN", 6)               # EMA span
OUTLIER_Z_THRESHOLD     = _getenv_float("OUTLIER_Z_THRESHOLD", 3.0)        # z-score
OUTLIER_IQR_K           = _getenv_float("OUTLIER_IQR_K", 1.5)              # Tukey fence
RANK_ASCENDING_DEFAULT  = _getenv_bool("RANK_ASCENDING_DEFAULT", False)
QUANTILE_BUCKETS        = _getenv_int("QUANTILE_BUCKETS", 10)
TIME_GROUPING_FREQ      = _getenv_str("TIME_GROUPING_FREQ", "M")           # D|W|M
CACHE_TTL_SECONDS       = _getenv_int("CACHE_TTL_SECONDS", 60)             # cache de @st.cache_data
ANALYTICS_MAX_ROWS      = _getenv_int("ANALYTICS_MAX_ROWS", 500_000)       # límite de filas para cálculos pesados


# ---------- Límites anti-OOM / integración con Spark ----------
# Máximo de filas que la UI intentará colectar a pandas
MAX_PANDAS_ROWS   = _getenv_int("MAX_PANDAS_ROWS", 300_000)

# Tamaño de muestra para previews/estimaciones cuando se use Spark
SPARK_SAMPLE_SIZE = _getenv_int("SPARK_SAMPLE_SIZE", 100_000)

# Límite superior de filas al leer desde Mongo con Spark antes de hacer collect()
# 0 = sin límite (no recomendado)
SPARK_READ_LIMIT  = _getenv_int("SPARK_READ_LIMIT", 200_000)


# ---------- Notas ----------
# - La app también lee otras ENV fuera de este archivo:
#   USE_SPARK, USE_SPARK_MONGO, USE_MONGO_PIPELINE,
#   DATA_DIR, CSV_FILE, MONGO_URI, MONGO_DB, MONGO_COLL, DISABLE_MONGO.
# - Todas pueden ir en tu .env en la raíz del proyecto.
