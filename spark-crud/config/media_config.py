# config/media_config.py
# Configuración específica para multimedia
# ========================================

import os
from typing import Dict, List, Tuple
from .settings import MediaConfig

class MediaSettings:
    """Configuración centralizada para multimedia"""
    
    # Límites de archivos en bytes
    MAX_VIDEO_SIZE = MediaConfig.MAX_VIDEO_SIZE_MB * 1024 * 1024
    MAX_IMAGE_SIZE = MediaConfig.MAX_IMAGE_SIZE_MB * 1024 * 1024  
    MAX_AUDIO_SIZE = MediaConfig.MAX_AUDIO_SIZE_MB * 1024 * 1024
    
    # Formatos permitidos
    VIDEO_FORMATS = MediaConfig.ALLOWED_VIDEO_FORMATS
    IMAGE_FORMATS = MediaConfig.ALLOWED_IMAGE_FORMATS
    AUDIO_FORMATS = MediaConfig.ALLOWED_AUDIO_FORMATS
    
    # Configuración de miniaturas
    VIDEO_THUMB_SIZE = MediaConfig.VIDEO_THUMBNAIL_SIZE
    IMAGE_THUMB_SIZE = MediaConfig.IMAGE_THUMBNAIL_SIZE
    
    # Calidad de optimización
    IMAGE_QUALITY = MediaConfig.IMAGE_OPTIMIZE_QUALITY
    
    @staticmethod
    def get_file_type(filename: str) -> str:
        """Determina el tipo de archivo por extensión"""
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        
        if ext in MediaSettings.VIDEO_FORMATS:
            return 'video'
        elif ext in MediaSettings.IMAGE_FORMATS:
            return 'image'
        elif ext in MediaSettings.AUDIO_FORMATS:
            return 'audio'
        else:
            return 'unknown'
    
    @staticmethod
    def is_valid_file(filename: str, file_size: int) -> Tuple[bool, str]:
        """Valida si un archivo es válido"""
        file_type = MediaSettings.get_file_type(filename)
        
        if file_type == 'unknown':
            return False, "Formato de archivo no soportado"
        
        # Validar tamaño
        if file_type == 'video' and file_size > MediaSettings.MAX_VIDEO_SIZE:
            return False, f"Video muy grande (máx. {MediaConfig.MAX_VIDEO_SIZE_MB}MB)"
        elif file_type == 'image' and file_size > MediaSettings.MAX_IMAGE_SIZE:
            return False, f"Imagen muy grande (máx. {MediaConfig.MAX_IMAGE_SIZE_MB}MB)"
        elif file_type == 'audio' and file_size > MediaSettings.MAX_AUDIO_SIZE:
            return False, f"Audio muy grande (máx. {MediaConfig.MAX_AUDIO_SIZE_MB}MB)"
        
        return True, "Archivo válido"
    
    @staticmethod
    def ensure_media_directories():
        """Crea los directorios multimedia si no existen"""
        directories = [
            MediaConfig.MEDIA_DIR,
            MediaConfig.VIDEOS_DIR,
            MediaConfig.IMAGES_DIR,
            MediaConfig.AUDIO_DIR,
            MediaConfig.THUMBNAILS_DIR,
            MediaConfig.TEMP_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

# Configuración de FFmpeg para procesamiento de video
class FFmpegConfig:
    """Configuración para FFmpeg"""
    
    # Comandos base
    VIDEO_CODEC = "libx264"
    AUDIO_CODEC = "aac"
    
    # Presets de calidad
    QUALITY_PRESETS = {
        "low": {
            "video_bitrate": "500k",
            "audio_bitrate": "64k",
            "resolution": "480p"
        },
        "medium": {
            "video_bitrate": "1500k", 
            "audio_bitrate": "128k",
            "resolution": "720p"
        },
        "high": {
            "video_bitrate": "3000k",
            "audio_bitrate": "192k", 
            "resolution": "1080p"
        }
    }
    
    @staticmethod
    def get_thumbnail_command(input_file: str, output_file: str, time: str = "00:00:01") -> List[str]:
        """Genera comando FFmpeg para crear miniatura"""
        return [
            "ffmpeg", "-i", input_file,
            "-ss", time,
            "-vframes", "1",
            "-vf", f"scale={MediaConfig.VIDEO_THUMBNAIL_SIZE[0]}:{MediaConfig.VIDEO_THUMBNAIL_SIZE[1]}",
            "-y", output_file
        ]
    
    @staticmethod
    def get_convert_command(input_file: str, output_file: str, quality: str = "medium") -> List[str]:
        """Genera comando FFmpeg para convertir video"""
        preset = FFmpegConfig.QUALITY_PRESETS.get(quality, FFmpegConfig.QUALITY_PRESETS["medium"])
        
        return [
            "ffmpeg", "-i", input_file,
            "-c:v", FFmpegConfig.VIDEO_CODEC,
            "-c:a", FFmpegConfig.AUDIO_CODEC,
            "-b:v", preset["video_bitrate"],
            "-b:a", preset["audio_bitrate"],
            "-y", output_file
        ]

# Configuración de PIL para procesamiento de imágenes
class ImageProcessingConfig:
    """Configuración para procesamiento de imágenes"""
    
    # Formatos de salida optimizados
    OUTPUT_FORMATS = {
        "jpg": {"format": "JPEG", "quality": MediaConfig.IMAGE_OPTIMIZE_QUALITY},
        "png": {"format": "PNG", "optimize": True},
        "webp": {"format": "WEBP", "quality": MediaConfig.IMAGE_OPTIMIZE_QUALITY}
    }
    
    # Tamaños estándar para redimensionamiento
    STANDARD_SIZES = {
        "thumbnail": (150, 150),
        "small": (300, 300),
        "medium": (600, 600),
        "large": (1200, 1200)
    }
    
    @staticmethod
    def get_optimized_format(original_format: str) -> str:
        """Determina el mejor formato optimizado"""
        original_format = original_format.lower()
        
        if original_format in ["jpg", "jpeg"]:
            return "jpg"
        elif original_format == "png":
            return "webp"  # PNG -> WebP para mejor compresión
        else:
            return "jpg"  # Default a JPEG

__all__ = [
    "MediaSettings",
    "FFmpegConfig", 
    "ImageProcessingConfig"
]