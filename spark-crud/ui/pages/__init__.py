# ui/pages/__init__.py
# Inicialización del módulo de páginas
# ====================================

from . import dashboard
from . import customers  
from . import video_gallery
from . import image_gallery
from . import audio_player
from . import analytics
from . import settings as settings_page

__all__ = [
    'dashboard',
    'customers', 
    'video_gallery',
    'image_gallery', 
    'audio_player',
    'analytics',
    'settings_page'
]