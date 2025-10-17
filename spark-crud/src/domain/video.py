# src/domain/video.py
# Entidad Video - Lógica de negocio para videos
# =============================================

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path
import mimetypes

@dataclass
class Video:
    """Entidad Video con validaciones y metadata"""
    
    # Identificación
    id: Optional[str] = None
    title: str = ""
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    # Archivo
    filename: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None  # en bytes
    mime_type: Optional[str] = None
    
    # Metadata de video
    duration: Optional[float] = None  # en segundos
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    bitrate: Optional[int] = None
    codec: Optional[str] = None
    
    # Miniaturas
    thumbnail_path: Optional[str] = None
    preview_gif_path: Optional[str] = None
    
    # Origen
    source: str = "upload"  # upload, youtube, pexels, etc.
    source_url: Optional[str] = None
    source_id: Optional[str] = None
    
    # Estado
    status: str = "pending"  # pending, processing, ready, error
    processing_progress: float = 0.0
    error_message: Optional[str] = None
    
    # Auditoría
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[str] = None
    
    # Estadísticas
    view_count: int = 0
    download_count: int = 0
    
    # Formatos permitidos
    ALLOWED_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv']
    
    def __post_init__(self):
        """Validaciones automáticas"""
        self._validate()
        self._derive_metadata()
    
    def _validate(self):
        """Validaciones de negocio"""
        # Validar título
        if not self.title.strip():
            raise ValueError("El título del video es obligatorio")
        
        # Validar formato si hay filename
        if self.filename:
            ext = Path(self.filename).suffix.lower()
            if ext not in self.ALLOWED_FORMATS:
                raise ValueError(f"Formato no soportado: {ext}")
        
        # Validar duración
        if self.duration is not None and self.duration <= 0:
            raise ValueError("La duración debe ser mayor a 0")
        
        # Validar dimensiones
        if self.width is not None and self.width <= 0:
            raise ValueError("El ancho debe ser mayor a 0")
        if self.height is not None and self.height <= 0:
            raise ValueError("La altura debe ser mayor a 0")
        
        # Validar status
        valid_statuses = ["pending", "processing", "ready", "error"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status inválido: {self.status}")
    
    def _derive_metadata(self):
        """Deriva metadata automáticamente"""
        # Derivar MIME type del filename
        if self.filename and not self.mime_type:
            mime_type, _ = mimetypes.guess_type(self.filename)
            self.mime_type = mime_type or "video/mp4"
        
        # Limpiar tags
        if self.tags:
            self.tags = [tag.strip().lower() for tag in self.tags if tag.strip()]
    
    @property
    def file_extension(self) -> str:
        """Retorna la extensión del archivo"""
        if self.filename:
            return Path(self.filename).suffix.lower()
        return ""
    
    @property
    def duration_formatted(self) -> str:
        """Retorna duración formateada (HH:MM:SS)"""
        if not self.duration:
            return "00:00:00"
        
        hours = int(self.duration // 3600)
        minutes = int((self.duration % 3600) // 60)
        seconds = int(self.duration % 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    @property
    def resolution(self) -> str:
        """Retorna resolución como string"""
        if self.width and self.height:
            return f"{self.width}x{self.height}"
        return "Desconocida"
    
    @property
    def file_size_mb(self) -> float:
        """Retorna tamaño en MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0.0
    
    @property
    def is_ready(self) -> bool:
        """Verifica si el video está listo para reproducir"""
        return self.status == "ready"
    
    @property
    def is_processing(self) -> bool:
        """Verifica si el video está siendo procesado"""
        return self.status == "processing"
    
    @property
    def has_error(self) -> bool:
        """Verifica si hay errores"""
        return self.status == "error"
    
    def add_tag(self, tag: str):
        """Agrega un tag al video"""
        tag = tag.strip().lower()
        if tag and tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remueve un tag del video"""
        tag = tag.strip().lower()
        if tag in self.tags:
            self.tags.remove(tag)
    
    def increment_views(self):
        """Incrementa contador de visualizaciones"""
        self.view_count += 1
        self.updated_at = datetime.now()
    
    def increment_downloads(self):
        """Incrementa contador de descargas"""
        self.download_count += 1
        self.updated_at = datetime.now()
    
    def set_processing_status(self, progress: float = 0.0):
        """Establece estado de procesamiento"""
        self.status = "processing"
        self.processing_progress = max(0.0, min(100.0, progress))
        self.updated_at = datetime.now()
    
    def set_ready_status(self):
        """Establece estado listo"""
        self.status = "ready"
        self.processing_progress = 100.0
        self.error_message = None
        self.updated_at = datetime.now()
    
    def set_error_status(self, error_message: str):
        """Establece estado de error"""
        self.status = "error"
        self.error_message = error_message
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a diccionario"""
        data = {}
        
        for field_name, field_value in self.__dict__.items():
            if field_value is not None:
                if isinstance(field_value, datetime):
                    data[field_name] = field_value.isoformat()
                else:
                    data[field_name] = field_value
        
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Video':
        """Crea instancia Video desde diccionario"""
        clean_data = {}
        
        for key, value in data.items():
            if value is not None:
                # Convertir strings a datetime
                if key in ['created_at', 'updated_at'] and isinstance(value, str):
                    try:
                        clean_data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except:
                        clean_data[key] = value
                else:
                    clean_data[key] = value
        
        return cls(**clean_data)
    
    def __str__(self) -> str:
        return f"Video(id={self.id}, title='{self.title}', duration={self.duration_formatted})"