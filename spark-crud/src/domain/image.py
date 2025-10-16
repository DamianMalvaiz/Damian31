# src/domain/image.py
# Entidad Image - Lógica de negocio para imágenes
# ===============================================

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import mimetypes

@dataclass
class Image:
    """Entidad Image con validaciones y metadata"""
    
    # Identificación
    id: Optional[str] = None
    title: str = ""
    description: Optional[str] = None
    alt_text: Optional[str] = None  # Para accesibilidad
    tags: List[str] = field(default_factory=list)
    
    # Archivo
    filename: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None  # en bytes
    mime_type: Optional[str] = None
    
    # Metadata de imagen
    width: Optional[int] = None
    height: Optional[int] = None
    color_mode: Optional[str] = None  # RGB, RGBA, CMYK, etc.
    has_transparency: bool = False
    dpi: Optional[int] = None
    color_profile: Optional[str] = None
    
    # Versiones optimizadas
    thumbnail_path: Optional[str] = None
    webp_path: Optional[str] = None  # Versión WebP optimizada
    optimized_path: Optional[str] = None  # Versión comprimida
    
    # Análisis de imagen (opcional)
    dominant_colors: List[str] = field(default_factory=list)  # Colores hex dominantes
    brightness: Optional[float] = None  # 0.0 - 1.0
    contrast: Optional[float] = None   # 0.0 - 1.0
    has_faces: bool = False  # Detección facial
    
    # Origen
    source: str = "upload"  # upload, unsplash, pixabay, generated, etc.
    source_url: Optional[str] = None
    source_id: Optional[str] = None
    photographer: Optional[str] = None
    license: Optional[str] = None  # CC0, MIT, etc.
    
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
    like_count: int = 0
    
    # Formatos permitidos
    ALLOWED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.svg']
    
    def __post_init__(self):
        """Validaciones automáticas"""
        self._validate()
        self._derive_metadata()
    
    def _validate(self):
        """Validaciones de negocio"""
        # Validar título
        if not self.title.strip():
            raise ValueError("El título de la imagen es obligatorio")
        
        # Validar formato si hay filename
        if self.filename:
            ext = Path(self.filename).suffix.lower()
            if ext not in self.ALLOWED_FORMATS:
                raise ValueError(f"Formato no soportado: {ext}")
        
        # Validar dimensiones
        if self.width is not None and self.width <= 0:
            raise ValueError("El ancho debe ser mayor a 0")
        if self.height is not None and self.height <= 0:
            raise ValueError("La altura debe ser mayor a 0")
        
        # Validar brightness y contrast
        if self.brightness is not None and not (0.0 <= self.brightness <= 1.0):
            raise ValueError("El brillo debe estar entre 0.0 y 1.0")
        if self.contrast is not None and not (0.0 <= self.contrast <= 1.0):
            raise ValueError("El contraste debe estar entre 0.0 y 1.0")
        
        # Validar status
        valid_statuses = ["pending", "processing", "ready", "error"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status inválido: {self.status}")
        
        # Validar colores dominantes (formato hex)
        for color in self.dominant_colors:
            if not color.startswith('#') or len(color) != 7:
                raise ValueError(f"Color inválido: {color}")
    
    def _derive_metadata(self):
        """Deriva metadata automáticamente"""
        # Derivar MIME type del filename
        if self.filename and not self.mime_type:
            mime_type, _ = mimetypes.guess_type(self.filename)
            self.mime_type = mime_type or "image/jpeg"
        
        # Derivar alt_text del título si no existe
        if not self.alt_text and self.title:
            self.alt_text = self.title
        
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
    def resolution(self) -> str:
        """Retorna resolución como string"""
        if self.width and self.height:
            return f"{self.width}x{self.height}"
        return "Desconocida"
    
    @property
    def aspect_ratio(self) -> Optional[float]:
        """Calcula la relación de aspecto"""
        if self.width and self.height:
            return round(self.width / self.height, 2)
        return None
    
    @property
    def megapixels(self) -> Optional[float]:
        """Calcula los megapíxeles"""
        if self.width and self.height:
            return round((self.width * self.height) / 1_000_000, 2)
        return None
    
    @property
    def file_size_mb(self) -> float:
        """Retorna tamaño en MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0.0
    
    @property
    def is_ready(self) -> bool:
        """Verifica si la imagen está lista"""
        return self.status == "ready"
    
    @property
    def is_processing(self) -> bool:
        """Verifica si está siendo procesada"""
        return self.status == "processing"
    
    @property
    def has_error(self) -> bool:
        """Verifica si hay errores"""
        return self.status == "error"
    
    @property
    def is_landscape(self) -> bool:
        """Verifica si es horizontal"""
        if self.width and self.height:
            return self.width > self.height
        return False
    
    @property
    def is_portrait(self) -> bool:
        """Verifica si es vertical"""
        if self.width and self.height:
            return self.height > self.width
        return False
    
    @property
    def is_square(self) -> bool:
        """Verifica si es cuadrada"""
        if self.width and self.height:
            return self.width == self.height
        return False
    
    @property
    def quality_score(self) -> str:
        """Calcula puntuación de calidad basada en resolución"""
        if not self.megapixels:
            return "Desconocida"
        
        if self.megapixels >= 12:
            return "Excelente"
        elif self.megapixels >= 8:
            return "Muy Buena"
        elif self.megapixels >= 5:
            return "Buena"
        elif self.megapixels >= 2:
            return "Regular"
        else:
            return "Baja"
    
    def add_tag(self, tag: str):
        """Agrega un tag a la imagen"""
        tag = tag.strip().lower()
        if tag and tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remueve un tag de la imagen"""
        tag = tag.strip().lower()
        if tag in self.tags:
            self.tags.remove(tag)
    
    def add_dominant_color(self, color: str):
        """Agrega un color dominante"""
        if color.startswith('#') and len(color) == 7:
            if color not in self.dominant_colors:
                self.dominant_colors.append(color)
    
    def increment_views(self):
        """Incrementa contador de visualizaciones"""
        self.view_count += 1
        self.updated_at = datetime.now()
    
    def increment_downloads(self):
        """Incrementa contador de descargas"""
        self.download_count += 1
        self.updated_at = datetime.now()
    
    def increment_likes(self):
        """Incrementa contador de likes"""
        self.like_count += 1
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
    
    def set_dimensions(self, width: int, height: int):
        """Establece dimensiones de la imagen"""
        self.width = width
        self.height = height
        self.updated_at = datetime.now()
    
    def set_analysis_results(self, 
                           brightness: Optional[float] = None,
                           contrast: Optional[float] = None,
                           dominant_colors: Optional[List[str]] = None,
                           has_faces: bool = False):
        """Establece resultados del análisis de imagen"""
        if brightness is not None:
            self.brightness = brightness
        if contrast is not None:
            self.contrast = contrast
        if dominant_colors:
            self.dominant_colors = dominant_colors
        self.has_faces = has_faces
        self.updated_at = datetime.now()
    
    def get_optimization_suggestions(self) -> List[str]:
        """Retorna sugerencias de optimización"""
        suggestions = []
        
        # Sugerencias basadas en tamaño
        if self.file_size_mb > 5:
            suggestions.append("Considera comprimir la imagen para reducir el tamaño")
        
        # Sugerencias basadas en formato
        if self.file_extension in ['.png', '.bmp'] and not self.has_transparency:
            suggestions.append("Considera convertir a JPEG para mejor compresión")
        
        # Sugerencias basadas en resolución
        if self.megapixels and self.megapixels > 20:
            suggestions.append("Resolución muy alta, considera redimensionar para web")
        
        # Sugerencias basadas en calidad
        if self.brightness and self.brightness < 0.3:
            suggestions.append("La imagen parece muy oscura")
        elif self.brightness and self.brightness > 0.8:
            suggestions.append("La imagen parece muy brillante")
        
        if self.contrast and self.contrast < 0.3:
            suggestions.append("Bajo contraste, considera ajustar")
        
        return suggestions
    
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
    def from_dict(cls, data: Dict[str, Any]) -> 'Image':
        """Crea instancia Image desde diccionario"""
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
        return f"Image(id={self.id}, title='{self.title}', resolution={self.resolution})"