# config/settings.py
# Configuración principal del Media Management System
# ===================================================

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ========== HELPERS ==========
def _getenv_bool(key: str, default: bool) -> bool:
    """Convierte variable de entorno a booleano"""
    val = os.getenv(key, str(default)).strip().lower()
    return val in {"1", "true", "t", "yes", "y", "on"}

def _getenv_int(key: str, default: int) -> int:
    """Convierte variable de entorno a entero"""
    try:
        return int(os.getenv(key, str(default)).strip())
    except Exception:
        return default

def _getenv_float(key: str, default: float) -> float:
    """Convierte variable de entorno a float"""
    try:
        return float(os.getenv(key, str(default)).strip())
    except Exception:
        return default

def _getenv_str(key: str, default: str) -> str:
    """Obtiene variable de entorno como string"""
    v = os.getenv(key, default)
    return v if v is not None and v != "" else default

# ========== CONFIGURACIÓN GENERAL ==========
class AppConfig:
    # Información de la aplicación
    APP_NAME = _getenv_str("APP_NAME", "Media Management System")
    APP_VERSION = _getenv_str("APP_VERSION", "2.0.0")
    DEBUG = _getenv_bool("DEBUG", False)
    
    # Directorios base
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = _getenv_str("DATA_DIR", os.path.join(BASE_DIR, "data"))
    
    # Paginación y UI
    PAGE_SIZE = _getenv_int("PAGE_SIZE", 25)
    DEFAULT_ORDER_COL = _getenv_str("DEFAULT_ORDER_COL", "id")
    DEFAULT_ORDER_DIR = _getenv_str("DEFAULT_ORDER_DIR", "asc")
    
    # Features habilitadas
    ENABLE_ANALYTICS = _getenv_bool("ENABLE_ANALYTICS", True)
    ENABLE_MEDIA = _getenv_bool("ENABLE_MEDIA", True)
    ENABLE_EXTERNAL_APIS = _getenv_bool("ENABLE_EXTERNAL_APIS", True)

# ========== CONFIGURACIÓN DE BASE DE DATOS ==========
class DatabaseConfig:
    # MongoDB
    MONGO_URI = _getenv_str("MONGO_URI", "mongodb://127.0.0.1:27017")
    MONGO_DB = _getenv_str("MONGO_DB", "media_management")
    MONGO_TIMEOUT = _getenv_int("MONGO_TIMEOUT", 4000)
    
    # Colecciones
    CUSTOMERS_COLLECTION = _getenv_str("CUSTOMERS_COLLECTION", "customers")
    VIDEOS_COLLECTION = _getenv_str("VIDEOS_COLLECTION", "videos")
    IMAGES_COLLECTION = _getenv_str("IMAGES_COLLECTION", "images")
    AUDIO_COLLECTION = _getenv_str("AUDIO_COLLECTION", "audio")
    
    # GridFS para archivos grandes
    GRIDFS_BUCKET = _getenv_str("GRIDFS_BUCKET", "media_files")
    
    # Spark
    USE_SPARK = _getenv_bool("USE_SPARK", True)
    SPARK_APP_NAME = _getenv_str("SPARK_APP_NAME", "media-management-spark")
    SPARK_MASTER = _getenv_str("SPARK_MASTER", "local[*]")
    SPARK_READ_LIMIT = _getenv_int("SPARK_READ_LIMIT", 200000)

# ========== CONFIGURACIÓN MULTIMEDIA ==========
class MediaConfig:
    # Límites de archivos (en MB)
    MAX_VIDEO_SIZE_MB = _getenv_int("MAX_VIDEO_SIZE_MB", 500)
    MAX_IMAGE_SIZE_MB = _getenv_int("MAX_IMAGE_SIZE_MB", 50)
    MAX_AUDIO_SIZE_MB = _getenv_int("MAX_AUDIO_SIZE_MB", 100)
    
    # Formatos permitidos
    ALLOWED_VIDEO_FORMATS = ["mp4", "avi", "mov", "mkv", "webm"]
    ALLOWED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "gif", "webp", "bmp"]
    ALLOWED_AUDIO_FORMATS = ["mp3", "wav", "flac", "aac", "ogg"]
    
    # Configuración de procesamiento
    VIDEO_THUMBNAIL_SIZE = (320, 240)
    IMAGE_THUMBNAIL_SIZE = (300, 300)
    IMAGE_OPTIMIZE_QUALITY = _getenv_int("IMAGE_OPTIMIZE_QUALITY", 85)
    
    # Directorios multimedia
    MEDIA_DIR = os.path.join(AppConfig.DATA_DIR, "media")
    VIDEOS_DIR = os.path.join(MEDIA_DIR, "videos")
    IMAGES_DIR = os.path.join(MEDIA_DIR, "images")
    AUDIO_DIR = os.path.join(MEDIA_DIR, "audio")
    THUMBNAILS_DIR = os.path.join(MEDIA_DIR, "thumbnails")
    TEMP_DIR = os.path.join(AppConfig.DATA_DIR, "temp")

# ========== CONFIGURACIÓN DE ANALYTICS ==========
class AnalyticsConfig:
    # Métodos de correlación
    CORRELATION_METHOD = _getenv_str("ANALYTICS_CORR_METHOD", "pearson")
    
    # Configuración de series temporales
    ROLLING_DEFAULT_WINDOW = _getenv_int("ROLLING_DEFAULT_WINDOW", 6)
    EMA_DEFAULT_SPAN = _getenv_int("EMA_DEFAULT_SPAN", 6)
    TIME_GROUPING_FREQ = _getenv_str("TIME_GROUPING_FREQ", "M")
    
    # Detección de outliers
    OUTLIER_Z_THRESHOLD = _getenv_float("OUTLIER_Z_THRESHOLD", 3.0)
    OUTLIER_IQR_K = _getenv_float("OUTLIER_IQR_K", 1.5)
    
    # Límites de rendimiento
    ANALYTICS_MAX_ROWS = _getenv_int("ANALYTICS_MAX_ROWS", 500000)
    CACHE_TTL_SECONDS = _getenv_int("CACHE_TTL_SECONDS", 600)

# ========== CONFIGURACIÓN DE AUTENTICACIÓN ==========
class AuthConfig:
    # Usuarios permitidos
    ALLOWED_USERS = {"damian", "david", "alexis"}
    
    # Hash de contraseña (cambiar en producción)
    PASSWORD_HASH = _getenv_str("PASSWORD_HASH", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")
    
    # Configuración de sesión
    SESSION_TIMEOUT_HOURS = _getenv_int("SESSION_TIMEOUT_HOURS", 8)
    REMEMBER_ME_DAYS = _getenv_int("REMEMBER_ME_DAYS", 30)

# ========== CONFIGURACIÓN DE APIs EXTERNAS ==========
class ExternalAPIConfig:
    # YouTube API
    YOUTUBE_API_KEY = _getenv_str("YOUTUBE_API_KEY", "")
    YOUTUBE_MAX_RESULTS = _getenv_int("YOUTUBE_MAX_RESULTS", 50)
    
    # Pexels API (videos)
    PEXELS_API_KEY = _getenv_str("PEXELS_API_KEY", "")
    PEXELS_MAX_RESULTS = _getenv_int("PEXELS_MAX_RESULTS", 50)
    
    # Unsplash API (imágenes)
    UNSPLASH_ACCESS_KEY = _getenv_str("UNSPLASH_ACCESS_KEY", "")
    UNSPLASH_MAX_RESULTS = _getenv_int("UNSPLASH_MAX_RESULTS", 50)
    
    # Pixabay API
    PIXABAY_API_KEY = _getenv_str("PIXABAY_API_KEY", "")
    PIXABAY_MAX_RESULTS = _getenv_int("PIXABAY_MAX_RESULTS", 50)
    
    # Rate limiting
    API_RATE_LIMIT_PER_MINUTE = _getenv_int("API_RATE_LIMIT_PER_MINUTE", 60)

# ========== CONFIGURACIÓN DE TEMA Y UI ==========
class UIConfig:
    # Tema por defecto
    DEFAULT_THEME = _getenv_str("DEFAULT_THEME", "dark")
    
    # Colores principales
    PRIMARY_COLOR = _getenv_str("PRIMARY_COLOR", "#3b82f6")
    SECONDARY_COLOR = _getenv_str("SECONDARY_COLOR", "#8b5cf6")
    ACCENT_COLOR = _getenv_str("ACCENT_COLOR", "#06d6a0")
    
    # Animaciones
    ENABLE_ANIMATIONS = _getenv_bool("ENABLE_ANIMATIONS", True)
    ANIMATION_DURATION = _getenv_str("ANIMATION_DURATION", "0.3s")

# ========== FUNCIÓN DE VALIDACIÓN ==========
def validate_config() -> Dict[str, Any]:
    """Valida la configuración y retorna errores si los hay"""
    errors = []
    warnings = []
    
    # Validar directorios
    if not os.path.exists(AppConfig.DATA_DIR):
        try:
            os.makedirs(AppConfig.DATA_DIR, exist_ok=True)
            warnings.append(f"Creado directorio de datos: {AppConfig.DATA_DIR}")
        except Exception as e:
            errors.append(f"No se pudo crear directorio de datos: {e}")
    
    # Validar configuración multimedia
    if MediaConfig.MAX_VIDEO_SIZE_MB > 1000:
        warnings.append("Tamaño máximo de video muy alto (>1GB)")
    
    # Validar APIs
    if ExternalAPIConfig.YOUTUBE_API_KEY == "":
        warnings.append("YouTube API key no configurada")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

# ========== EXPORTAR CONFIGURACIONES ==========
__all__ = [
    "AppConfig",
    "DatabaseConfig", 
    "MediaConfig",
    "AnalyticsConfig",
    "AuthConfig",
    "ExternalAPIConfig",
    "UIConfig",
    "validate_config"
]