# src/domain/audio.py
# Entidad Audio - Lógica de negocio para archivos de audio
# =======================================================

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from pathlib import Path
import mimetypes

@dataclass
class Audio:
    """Entidad Audio con validaciones y metadata musical"""
    
    # Identificación
    id: Optional[str] = None
    title: str = ""
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    # Metadata musical
    artist: Optional[str] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    track_number: Optional[int] = None
    total_tracks: Optional[int] = None
    composer: Optional[str] = None
    
    # Archivo
    filename: Optional[str] = None
    file_path: Optional[str] = None
    file_size: Optional[int] = None  # en bytes
    mime_type: Optional[str] = None
    
    # Metadata técnica de audio
    duration: Optional[float] = None  # en segundos
    bitrate: Optional[int] = None  # kbps
    sample_rate: Optional[int] = None  # Hz (44100, 48000, etc.)
    channels: Optional[int] = None  # 1=mono, 2=stereo
    codec: Optional[str] = None  # MP3, FLAC, AAC, etc.
    bit_depth: Optional[int] = None  # 16, 24, 32 bits
    
    # Análisis de audio (opcional)
    bpm: Optional[float] = None  # Beats per minute
    key: Optional[str] = None  # Clave musical (C, D, E, etc.)
    mode: Optional[str] = None  # Major, Minor
    energy: Optional[float] = None  # 0.0 - 1.0
    valence: Optional[float] = None  # 0.0 - 1.0 (tristeza - felicidad)
    danceability: Optional[float] = None  # 0.0 - 1.0
    loudness: Optional[float] = None  # dB
    
    # Archivos relacionados
    waveform_path: Optional[str] = None  # Imagen de forma de onda
    spectrum_path: Optional[str] = None  # Espectrograma
    artwork_path: Optional[str] = None  # Carátula del álbum
    
    # Origen
    source: str = "upload"  # upload, spotify, youtube, generated, etc.
    source_url: Optional[str] = None
    source_id: Optional[str] = None
    license: Optional[str] = None
    
    # Estado
    status: str = "pending"  # pending, processing, ready, error
    processing_progress: float = 0.0
    error_message: Optional[str] = None
    
    # Auditoría
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    created_by: Optional[str] = None
    
    # Estadísticas
    play_count: int = 0
    download_count: int = 0
    like_count: int = 0
    total_play_time: float = 0.0  # Tiempo total reproducido en segundos
    
    # Formatos permitidos
    ALLOWED_FORMATS = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma']
    
    def __post_init__(self):
        """Validaciones automáticas"""
        self._validate()
        self._derive_metadata()
    
    def _validate(self):
        """Validaciones de negocio"""
        # Validar título
        if not self.title.strip():
            raise ValueError("El título del audio es obligatorio")
        
        # Validar formato si hay filename
        if self.filename:
            ext = Path(self.filename).suffix.lower()
            if ext not in self.ALLOWED_FORMATS:
                raise ValueError(f"Formato no soportado: {ext}")
        
        # Validar duración
        if self.duration is not None and self.duration <= 0:
            raise ValueError("La duración debe ser mayor a 0")
        
        # Validar año
        if self.year is not None and (self.year < 1900 or self.year > datetime.now().year + 1):
            raise ValueError("Año inválido")
        
        # Validar métricas de análisis (0.0 - 1.0)
        for metric in ['energy', 'valence', 'danceability']:
            value = getattr(self, metric)
            if value is not None and not (0.0 <= value <= 1.0):
                raise ValueError(f"{metric} debe estar entre 0.0 y 1.0")
        
        # Validar BPM
        if self.bpm is not None and (self.bpm < 20 or self.bpm > 300):
            raise ValueError("BPM debe estar entre 20 y 300")
        
        # Validar status
        valid_statuses = ["pending", "processing", "ready", "error"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status inválido: {self.status}")
    
    def _derive_metadata(self):
        """Deriva metadata automáticamente"""
        # Derivar MIME type del filename
        if self.filename and not self.mime_type:
            mime_type, _ = mimetypes.guess_type(self.filename)
            self.mime_type = mime_type or "audio/mpeg"
        
        # Limpiar tags
        if self.tags:
            self.tags = [tag.strip().lower() for tag in self.tags if tag.strip()]
        
        # Normalizar género
        if self.genre:
            self.genre = self.genre.strip().title()
    
    @property
    def file_extension(self) -> str:
        """Retorna la extensión del archivo"""
        if self.filename:
            return Path(self.filename).suffix.lower()
        return ""
    
    @property
    def duration_formatted(self) -> str:
        """Retorna duración formateada (MM:SS o HH:MM:SS)"""
        if not self.duration:
            return "00:00"
        
        total_seconds = int(self.duration)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    @property
    def file_size_mb(self) -> float:
        """Retorna tamaño en MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0.0
    
    @property
    def quality_info(self) -> str:
        """Retorna información de calidad del audio"""
        if not self.bitrate or not self.sample_rate:
            return "Desconocida"
        
        # Determinar calidad basada en bitrate y sample rate
        if self.bitrate >= 320 and self.sample_rate >= 44100:
            return "Alta Calidad"
        elif self.bitrate >= 256:
            return "Buena Calidad"
        elif self.bitrate >= 192:
            return "Calidad Media"
        elif self.bitrate >= 128:
            return "Calidad Básica"
        else:
            return "Baja Calidad"
    
    @property
    def channel_info(self) -> str:
        """Retorna información de canales"""
        if self.channels == 1:
            return "Mono"
        elif self.channels == 2:
            return "Estéreo"
        elif self.channels and self.channels > 2:
            return f"{self.channels} Canales"
        return "Desconocido"
    
    @property
    def is_ready(self) -> bool:
        """Verifica si el audio está listo"""
        return self.status == "ready"
    
    @property
    def is_processing(self) -> bool:
        """Verifica si está siendo procesado"""
        return self.status == "processing"
    
    @property
    def has_error(self) -> bool:
        """Verifica si hay errores"""
        return self.status == "error"
    
    @property
    def is_lossless(self) -> bool:
        """Verifica si es formato sin pérdida"""
        return self.file_extension in ['.flac', '.wav']
    
    @property
    def full_artist_info(self) -> str:
        """Retorna información completa del artista"""
        parts = []
        if self.artist:
            parts.append(self.artist)
        if self.composer and self.composer != self.artist:
            parts.append(f"(Compositor: {self.composer})")
        return " ".join(parts) if parts else "Artista Desconocido"
    
    @property
    def album_info(self) -> str:
        """Retorna información del álbum"""
        parts = []
        if self.album:
            parts.append(self.album)
        if self.year:
            parts.append(f"({self.year})")
        return " ".join(parts) if parts else "Álbum Desconocido"
    
    @property
    def track_info(self) -> str:
        """Retorna información de pista"""
        if self.track_number and self.total_tracks:
            return f"{self.track_number}/{self.total_tracks}"
        elif self.track_number:
            return str(self.track_number)
        return ""
    
    @property
    def mood_description(self) -> str:
        """Describe el mood basado en valence y energy"""
        if self.valence is None or self.energy is None:
            return "Desconocido"
        
        if self.energy > 0.7 and self.valence > 0.7:
            return "Energético y Feliz"
        elif self.energy > 0.7 and self.valence < 0.3:
            return "Energético y Agresivo"
        elif self.energy < 0.3 and self.valence > 0.7:
            return "Relajado y Feliz"
        elif self.energy < 0.3 and self.valence < 0.3:
            return "Melancólico"
        elif self.energy > 0.5:
            return "Energético"
        elif self.valence > 0.5:
            return "Positivo"
        else:
            return "Neutral"
    
    def add_tag(self, tag: str):
        """Agrega un tag al audio"""
        tag = tag.strip().lower()
        if tag and tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remueve un tag del audio"""
        tag = tag.strip().lower()
        if tag in self.tags:
            self.tags.remove(tag)
    
    def increment_plays(self, play_duration: Optional[float] = None):
        """Incrementa contador de reproducciones"""
        self.play_count += 1
        if play_duration:
            self.total_play_time += play_duration
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
    
    def set_audio_metadata(self, 
                          duration: Optional[float] = None,
                          bitrate: Optional[int] = None,
                          sample_rate: Optional[int] = None,
                          channels: Optional[int] = None,
                          codec: Optional[str] = None):
        """Establece metadata técnica del audio"""
        if duration is not None:
            self.duration = duration
        if bitrate is not None:
            self.bitrate = bitrate
        if sample_rate is not None:
            self.sample_rate = sample_rate
        if channels is not None:
            self.channels = channels
        if codec is not None:
            self.codec = codec
        self.updated_at = datetime.now()
    
    def set_musical_metadata(self,
                           artist: Optional[str] = None,
                           album: Optional[str] = None,
                           genre: Optional[str] = None,
                           year: Optional[int] = None,
                           track_number: Optional[int] = None):
        """Establece metadata musical"""
        if artist is not None:
            self.artist = artist
        if album is not None:
            self.album = album
        if genre is not None:
            self.genre = genre
        if year is not None:
            self.year = year
        if track_number is not None:
            self.track_number = track_number
        self.updated_at = datetime.now()
    
    def set_analysis_results(self,
                           bpm: Optional[float] = None,
                           key: Optional[str] = None,
                           energy: Optional[float] = None,
                           valence: Optional[float] = None,
                           danceability: Optional[float] = None):
        """Establece resultados del análisis musical"""
        if bpm is not None:
            self.bpm = bpm
        if key is not None:
            self.key = key
        if energy is not None:
            self.energy = energy
        if valence is not None:
            self.valence = valence
        if danceability is not None:
            self.danceability = danceability
        self.updated_at = datetime.now()
    
    def get_similar_tracks_criteria(self) -> Dict[str, Any]:
        """Retorna criterios para encontrar pistas similares"""
        criteria = {}
        
        if self.genre:
            criteria['genre'] = self.genre
        if self.bpm:
            criteria['bpm_range'] = (self.bpm - 10, self.bpm + 10)
        if self.key:
            criteria['key'] = self.key
        if self.energy is not None:
            criteria['energy_range'] = (max(0, self.energy - 0.2), min(1, self.energy + 0.2))
        if self.valence is not None:
            criteria['valence_range'] = (max(0, self.valence - 0.2), min(1, self.valence + 0.2))
        
        return criteria
    
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
    def from_dict(cls, data: Dict[str, Any]) -> 'Audio':
        """Crea instancia Audio desde diccionario"""
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
        return f"Audio(id={self.id}, title='{self.title}', artist='{self.artist}', duration={self.duration_formatted})"