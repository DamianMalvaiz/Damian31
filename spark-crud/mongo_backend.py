# mongo_backend.py
# Capa de utilidades para trabajar con MongoDB (PyMongo) de forma segura y consistente
# - Normaliza documentos antes de escribir (tipos y claves)
# - Upserts individuales y masivos por PK
# - Borrado por PK
# - Índices recomendados
#
# Uso rápido:
#   from mongo_backend import MongoBackend
#   m = MongoBackend()  # lee MONGO_URI, MONGO_DB, MONGO_COLL desde .env
#   m.ensure_indexes()
#   m.upsert({"id": 1, "name": "Ana", "email": "ANA@EXAMPLE.COM"})
#   m.upsert_many([{"id": 2, "name": "Luis"}, {"id": 3, "name": "Marta"}])
#   m.delete_many([2, 3])

from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
from datetime import datetime, date, time

try:
    # dateutil es flexible para parsear muchas fechas distintas
    from dateutil.parser import parse as dt_parse  # type: ignore
except Exception:  # pragma: no cover
    dt_parse = None  # type: ignore

try:
    from pymongo import MongoClient, UpdateOne, ASCENDING, HASHED  # type: ignore
    from pymongo.collection import Collection  # type: ignore
    from pymongo.errors import PyMongoError  # type: ignore
except Exception as e:  # pragma: no cover
    raise RuntimeError(
        "PyMongo no está instalado. Instala con: pip install pymongo python-dateutil"
    ) from e


# --------- ENV por defecto (coinciden con tu .env) ----------
DEFAULT_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
DEFAULT_DB = os.getenv("MONGO_DB", "cruddb")
DEFAULT_COLL = os.getenv("MONGO_COLL", "customers")


# ===================== Helpers de tipos =====================

def _to_datetime(val: Any) -> Optional[datetime]:
    """Convierte strings/fechas a datetime naive. Devuelve None si no se puede."""
    if val is None:
        return None
    if isinstance(val, datetime):
        # Aseguramos naive (sin tz) por simplicidad
        return val.replace(tzinfo=None)
    if isinstance(val, date):
        return datetime.combine(val, time.min)
    if isinstance(val, (int, float)):
        # Algunos datasets traen timestamps numéricos (segundos)
        # Si es un número razonable (1970..2100 aprox.), lo intento convertir
        try:
            if 0 < float(val) < 4102444800:  # 2100-01-01
                return datetime.fromtimestamp(float(val))
        except Exception:
            return None
        return None
    if isinstance(val, str):
        s = val.strip()
        if not s:
            return None
        # Intentar parsear ISO y formatos comunes
        if dt_parse is not None:
            try:
                dt = dt_parse(s)
                return dt.replace(tzinfo=None)
            except Exception:
                return None
        else:
            # Fallback básico a fromisoformat
            try:
                return datetime.fromisoformat(s)
            except Exception:
                return None
    return None


def _to_float(val: Any) -> Optional[float]:
    try:
        if val is None or val == "":
            return None
        return float(val)
    except Exception:
        return None


def _to_str(val: Any) -> str:
    if val is None:
        return ""
    return str(val)


def _norm_email(val: Any) -> str:
    return _to_str(val).strip().lower()


def _derive_created_ym(created_at: Optional[datetime], existing: Any) -> Optional[str]:
    if isinstance(existing, str) and existing:
        return existing
    if created_at is None:
        return None
    return created_at.strftime("%Y-%m")


def _derive_name(doc: Dict[str, Any]) -> Optional[str]:
    name = doc.get("name")
    if isinstance(name, str) and name.strip():
        return name.strip()
    # Derivar a partir de first_name / last_name si existen
    fn = doc.get("first_name")
    ln = doc.get("last_name")
    parts = []
    if isinstance(fn, str) and fn.strip():
        parts.append(fn.strip())
    if isinstance(ln, str) and ln.strip():
        parts.append(ln.strip())
    if parts:
        return " ".join(parts)
    return None


# ===================== Normalización de documento =====================

def normalize_document(doc: Dict[str, Any], pk: str = "id") -> Dict[str, Any]:
    """
    Regresa una COPIA normalizada del documento, con:
      - pk forzada a string para evitar duplicados '15' vs 15 en Mongo
      - id_num (int) como apoyo para ordenar en queries (opcional)
      - email normalizado (lowercase)
      - phone/string limpio
      - dob y created_at a datetime naive
      - created_ym (YYYY-MM) derivado si falta
      - name derivado si falta
    """
    d = dict(doc) if doc is not None else {}
    key = d.get(pk, None)

    # --- PK como string + auxiliar numérico
    id_str = _to_str(key).strip() if key is not None else ""
    d[pk] = id_str
    try:
        d["id_num"] = int(float(key)) if key not in (None, "") else None
    except Exception:
        d["id_num"] = None

    # --- Campos comunes
    if "email" in d:
        d["email"] = _norm_email(d.get("email"))

    if "phone" in d:
        d["phone"] = _to_str(d.get("phone")).strip()

    # dob / created_at
    dob = _to_datetime(d.get("dob"))
    if dob is not None:
        d["dob"] = dob
    else:
        # limpiar si venía vacío
        d["dob"] = None

    created_at = _to_datetime(d.get("created_at"))
    if created_at is not None:
        d["created_at"] = created_at
    else:
        d["created_at"] = None

    # created_ym
    d["created_ym"] = _derive_created_ym(created_at, d.get("created_ym"))

    # balance a float
    if "balance" in d:
        d["balance"] = _to_float(d.get("balance"))

    # Derivar name si falta
    name = _derive_name(d)
    if name:
        d["name"] = name

    return d


# ===================== Conexión e índices =====================

def get_client(uri: Optional[str] = None, timeout_ms: int = 4000) -> MongoClient:
    uri = uri or DEFAULT_URI
    client = MongoClient(uri, serverSelectionTimeoutMS=timeout_ms)
    # ping para validar conexión
    client.admin.command("ping")
    return client


def get_collection(
    db_name: Optional[str] = None,
    coll_name: Optional[str] = None,
    uri: Optional[str] = None,
    timeout_ms: int = 4000,
) -> Collection:
    db_name = db_name or DEFAULT_DB
    coll_name = coll_name or DEFAULT_COLL
    client = get_client(uri, timeout_ms=timeout_ms)
    return client[db_name][coll_name]


def ensure_indexes(coll: Collection) -> None:
    """
    Crea índices útiles. No marcamos 'unique' por compatibilidad con datasets sucios,
    pero puedes activarlo si tu 'id' está limpio.
    """
    try:
        # Igualdad rápida por id (string normalizada)
        coll.create_index([("id", HASHED)], background=True, name="id_hashed")
    except Exception:
        # fallback si HASHED no está permitido (p.ej. free-tier antiguos)
        coll.create_index([("id", ASCENDING)], background=True, name="id_idx")

    # Ordenación por id_num (si lo usamos)
    coll.create_index([("id_num", ASCENDING)], background=True, name="id_num_idx")

    # Búsqueda por email y por fecha
    coll.create_index([("email", ASCENDING)], background=True, name="email_idx", sparse=True)
    coll.create_index([("created_at", ASCENDING)], background=True, name="created_at_idx", sparse=True)
    coll.create_index([("created_ym", ASCENDING)], background=True, name="created_ym_idx", sparse=True)


# ===================== Backend OO =====================

class MongoBackend:
    def __init__(
        self,
        uri: Optional[str] = None,
        db_name: Optional[str] = None,
        coll_name: Optional[str] = None,
        timeout_ms: int = 4000,
    ) -> None:
        self.uri = uri or DEFAULT_URI
        self.db_name = db_name or DEFAULT_DB
        self.coll_name = coll_name or DEFAULT_COLL
        self.timeout_ms = timeout_ms

        self.client: MongoClient = get_client(self.uri, timeout_ms=self.timeout_ms)
        self.collection: Collection = self.client[self.db_name][self.coll_name]

    # --------- Utilidades ---------

    def ping(self) -> bool:
        try:
            self.client.admin.command("ping")
            return True
        except Exception:
            return False

    def ensure_indexes(self) -> None:
        ensure_indexes(self.collection)

    # --------- CRUD ---------

    def upsert(self, doc: Dict[str, Any], pk: str = "id") -> None:
        ndoc = normalize_document(doc, pk=pk)
        key = ndoc.get(pk, "")
        if not key:
            raise ValueError(f"La PK '{pk}' no puede ir vacía en upsert().")
        self.collection.update_one({pk: str(key)}, {"$set": ndoc}, upsert=True)

    def upsert_many(self, docs: Iterable[Dict[str, Any]], pk: str = "id", batch_size: int = 1000) -> Tuple[int, int]:
        """
        Inserta/actualiza en lotes. Devuelve (n_docs, n_batches_enviados).
        """
        ops: List[UpdateOne] = []
        n = 0
        batches = 0
        for d in docs:
            nd = normalize_document(d, pk=pk)
            key = nd.get(pk, "")
            if not key:
                # saltar doc sin PK
                continue
            ops.append(UpdateOne({pk: str(key)}, {"$set": nd}, upsert=True))
            n += 1
            if len(ops) >= batch_size:
                self.collection.bulk_write(ops, ordered=False)
                ops.clear()
                batches += 1
        if ops:
            self.collection.bulk_write(ops, ordered=False)
            batches += 1
        return n, batches

    def delete_many(self, keys: Iterable[Union[str, int]], pk: str = "id") -> int:
        ks = [str(k) for k in keys if k is not None and str(k) != ""]
        if not ks:
            return 0
        res = self.collection.delete_many({pk: {"$in": ks}})
        return int(res.deleted_count)

    # --------- Lecturas auxiliares ---------

    def find(
        self,
        query: Optional[Dict[str, Any]] = None,
        projection: Optional[Dict[str, int]] = None,
        limit: int = 1000,
        sort: Optional[List[Tuple[str, int]]] = None,
    ) -> List[Dict[str, Any]]:
        q = query or {}
        cur = self.collection.find(q, projection)
        if sort:
            cur = cur.sort(sort)
        if limit and limit > 0:
            cur = cur.limit(int(limit))
        return list(cur)


# ===================== API procedural (drop-in con tu app.py) =====================

# Estas funciones imitan los helpers inline que tenías en app.py,
# pero centralizados aquí. Si quieres usarlas tal cual:
#   from mongo_backend import get_default_collection, mongo_upsert, mongo_upsert_many, mongo_delete_many

def get_default_collection() -> Collection:
    return get_collection(DEFAULT_DB, DEFAULT_COLL, DEFAULT_URI)


def mongo_upsert(doc: Dict[str, Any], pk: str = "id", coll: Optional[Collection] = None) -> None:
    coll = coll or get_default_collection()
    nd = normalize_document(doc, pk=pk)
    key = nd.get(pk, "")
    if not key:
        raise ValueError(f"La PK '{pk}' no puede ir vacía en mongo_upsert().")
    coll.update_one({pk: str(key)}, {"$set": nd}, upsert=True)


def mongo_upsert_many(rows: Iterable[Dict[str, Any]], pk: str = "id", coll: Optional[Collection] = None, batch_size: int = 1000) -> Tuple[int, int]:
    coll = coll or get_default_collection()
    ops: List[UpdateOne] = []
    n = 0
    batches = 0
    for d in rows:
        nd = normalize_document(d, pk=pk)
        key = nd.get(pk, "")
        if not key:
            continue
        ops.append(UpdateOne({pk: str(key)}, {"$set": nd}, upsert=True))
        n += 1
        if len(ops) >= batch_size:
            coll.bulk_write(ops, ordered=False)
            ops.clear()
            batches += 1
    if ops:
        coll.bulk_write(ops, ordered=False)
        batches += 1
    return n, batches


def mongo_delete_many(keys: Iterable[Union[str, int]], pk: str = "id", coll: Optional[Collection] = None) -> int:
    coll = coll or get_default_collection()
    ks = [str(k) for k in keys if k is not None and str(k) != ""]
    if not ks:
        return 0
    res = coll.delete_many({pk: {"$in": ks}})
    return int(res.deleted_count)


__all__ = [
    "MongoBackend",
    "normalize_document",
    "get_client",
    "get_collection",
    "ensure_indexes",
    "mongo_upsert",
    "mongo_upsert_many",
    "mongo_delete_many",
    "get_default_collection",
]
