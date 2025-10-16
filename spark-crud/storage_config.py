# storage_config.py
# Utilidades de almacenamiento local (y opcional S3) para tu CRUD.
# - Administra DATA_DIR / CSV_FILE desde .env
# - Lectura/Escritura robusta de CSV con backups y escritura atómica
# - Lock de archivo (si portalocker está disponible) para evitar corrupciones en concurrencia
# - Helpers opcionales para S3 (si boto3 está instalado y se configuran credenciales)
#
# No depende de Streamlit. Puedes usarlo desde app.py o desde scripts CLI.

from __future__ import annotations

import os
import io
import shutil
import hashlib
from datetime import datetime
from typing import Optional, Tuple, List

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# ========= ENV =========
DATA_DIR = os.getenv("DATA_DIR", "./data")
CSV_FILE = os.getenv("CSV_FILE", "people-1000000.csv")  # mismo default que app.py
BACKUP_ON_WRITE = os.getenv("BACKUP_ON_WRITE", "true").lower() == "true"
BACKUP_KEEP = int(os.getenv("BACKUP_KEEP", "7"))  # cuántos backups rotar

# Opcional S3
USE_S3 = os.getenv("USE_S3", "false").lower() == "true"
S3_BUCKET = os.getenv("S3_BUCKET", "")
S3_PREFIX = os.getenv("S3_PREFIX", "")  # p.ej. "datasets/"
S3_REGION = os.getenv("S3_REGION", None)

# ========= Locks =========
# Usamos portalocker si está disponible; si no, hacemos un no-op lock.
try:
    import portalocker  # type: ignore
    _HAS_PORTALOCKER = True
except Exception:
    _HAS_PORTALOCKER = False


class _NullLock:
    def __init__(self, *_a, **_kw): ...
    def __enter__(self): return self
    def __exit__(self, *exc): return False


def file_lock(path: str):
    """
    Devuelve un context manager de lock de archivo, si portalocker está disponible.
    Caso contrario, un lock no-op (para Windows funciona bien con portalocker).
    """
    lock_path = f"{os.path.abspath(path)}.lock"
    os.makedirs(os.path.dirname(lock_path), exist_ok=True)
    if _HAS_PORTALOCKER:
        # timeout de 10s para evitar deadlocks
        return portalocker.Lock(lock_path, timeout=10)
    return _NullLock()


# ========= Paths & util =========

def ensure_data_dir() -> str:
    """Crea DATA_DIR si no existe y devuelve su ruta absoluta."""
    ab = os.path.abspath(DATA_DIR)
    os.makedirs(ab, exist_ok=True)
    return ab


def get_csv_path() -> str:
    """Ruta absoluta del CSV principal."""
    base = ensure_data_dir()
    return os.path.join(base, CSV_FILE)


def get_backup_dir() -> str:
    """Subcarpeta para backups dentro de DATA_DIR."""
    base = ensure_data_dir()
    bdir = os.path.join(base, "backups")
    os.makedirs(bdir, exist_ok=True)
    return bdir


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def sha256_file(path: str) -> Optional[str]:
    """Hash SHA256 de un archivo (si existe)."""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


# ========= Backups =========

def make_backup(path: str) -> Optional[str]:
    """Crea un backup timestamped del archivo 'path' en backups/ y devuelve su ruta."""
    if not os.path.isfile(path):
        return None
    bdir = get_backup_dir()
    base = os.path.basename(path)
    dest = os.path.join(bdir, f"{base}.{timestamp()}.bak")
    shutil.copy2(path, dest)
    return dest


def rotate_backups(keep: int = BACKUP_KEEP) -> None:
    """Mantiene solamente 'keep' backups más recientes por cada archivo base."""
    bdir = get_backup_dir()
    try:
        files = [os.path.join(bdir, f) for f in os.listdir(bdir) if f.endswith(".bak")]
        # Agrupar por base (todo antes del primer '.YYYYMMDD-...')
        def _key(p: str) -> Tuple[str, float]:
            return (os.path.basename(p).split(".")[0], os.path.getmtime(p))
        # Orden por base y por fecha descendente
        files.sort(key=lambda p: (_key(p)[0], _key(p)[1]), reverse=True)

        # Mantener por grupo
        seen = {}
        for p in files:
            base = os.path.basename(p).split(".")[0]
            seen.setdefault(base, []).append(p)
        for base, group in seen.items():
            for old in group[keep:]:
                try:
                    os.remove(old)
                except Exception:
                    pass
    except Exception:
        pass


# ========= Lectura / Escritura robustas =========

def read_csv_resilient(path: Optional[str] = None) -> pd.DataFrame:
    """
    Lee CSV con varios fallbacks de encoding/engine.
    Devuelve DataFrame (puede ser vacío si no existe).
    """
    if path is None:
        path = get_csv_path()

    if not os.path.isfile(path):
        # Crear archivo vacío para evitar errores aguas arriba
        pd.DataFrame().to_csv(path, index=False)
        return pd.DataFrame()

    # Intentos de lectura
    attempts = [
        dict(encoding="utf-8", engine="c"),
        dict(encoding="utf-8", engine="python"),
        dict(encoding="utf-8-sig", engine="c"),
        dict(encoding="latin-1", engine="c"),
        dict(encoding="cp1252", engine="c"),
    ]
    with file_lock(path):
        for opts in attempts:
            try:
                return pd.read_csv(path, low_memory=False, **opts)
            except Exception:
                continue
    # Si todo falla: DataFrame vacío
    return pd.DataFrame()


def write_csv_atomic(df: pd.DataFrame, path: Optional[str] = None, backups: bool = BACKUP_ON_WRITE) -> str:
    """
    Escritura atómica de CSV:
      - opcionalmente crea backup previo
      - escribe a archivo temporal y luego hace replace
      - usa lock para evitar corridas simultáneas

    Devuelve la ruta final escrita.
    """
    if path is None:
        path = get_csv_path()

    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.tmp"

    with file_lock(path):
        # Backup (si existe)
        if backups and os.path.isfile(path):
            make_backup(path)
            rotate_backups(BACKUP_KEEP)

        # Escribir temporal
        # utf-8 sin BOM para compatibilidad amplia
        df.to_csv(tmp, index=False, encoding="utf-8")
        # Reemplazo atómico (en Windows os.replace también sobreescribe)
        os.replace(tmp, path)

    return path


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convierte DataFrame a bytes CSV (utf-8) para descargas en Streamlit."""
    buf = io.StringIO()
    df.to_csv(buf, index=False, encoding="utf-8")
    return buf.getvalue().encode("utf-8")


# ========= S3 (opcional) =========

def _get_s3_client():
    import boto3  # type: ignore
    if S3_REGION:
        return boto3.client("s3", region_name=S3_REGION)
    return boto3.client("s3")


def s3_key_for_local(path: Optional[str] = None) -> str:
    """
    Genera una key S3 basada en S3_PREFIX + nombre de archivo.
    """
    if path is None:
        path = get_csv_path()
    name = os.path.basename(path)
    prefix = S3_PREFIX or ""
    if prefix and not prefix.endswith("/"):
        prefix += "/"
    return f"{prefix}{name}"


def s3_upload_file(path: Optional[str] = None) -> Optional[str]:
    """
    Sube un archivo local a S3 (si USE_S3=true y boto3 está disponible).
    Devuelve la key S3 o None si no aplica.
    """
    if not USE_S3 or not S3_BUCKET:
        return None
    try:
        import boto3  # type: ignore
        _ = boto3  # solo para linter
    except Exception:
        return None

    if path is None:
        path = get_csv_path()
    if not os.path.isfile(path):
        return None

    key = s3_key_for_local(path)
    s3 = _get_s3_client()
    s3.upload_file(path, S3_BUCKET, key)
    return key


def s3_download_file(dest_path: Optional[str] = None, key: Optional[str] = None) -> Optional[str]:
    """
    Descarga un archivo de S3 a 'dest_path'.
    Si no se pasa key, usa la generada por s3_key_for_local().
    Devuelve ruta descargada o None si no aplica/fracasa.
    """
    if not USE_S3 or not S3_BUCKET:
        return None
    try:
        import boto3  # type: ignore
        _ = boto3
    except Exception:
        return None

    if dest_path is None:
        dest_path = get_csv_path()
    if key is None:
        key = s3_key_for_local(dest_path)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    s3 = _get_s3_client()
    try:
        with file_lock(dest_path):
            s3.download_file(S3_BUCKET, key, dest_path)
        return dest_path
    except Exception:
        return None


__all__ = [
    "DATA_DIR",
    "CSV_FILE",
    "ensure_data_dir",
    "get_csv_path",
    "get_backup_dir",
    "read_csv_resilient",
    "write_csv_atomic",
    "df_to_csv_bytes",
    "make_backup",
    "rotate_backups",
    "sha256_file",
    "file_lock",
    # S3 opcional
    "USE_S3",
    "S3_BUCKET",
    "S3_PREFIX",
    "S3_REGION",
    "s3_upload_file",
    "s3_download_file",
]
