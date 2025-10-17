# app.py
# MEDIA MANAGEMENT SYSTEM v2.0 - BRUTAL EDITION
# =============================================
# Sistema de gestión multimedia más épico del universo

import streamlit as st
import sys
import os
from pathlib import Path

# Agregar paths al sistema
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))
sys.path.append(str(current_dir / "ui" / "styles"))
sys.path.append(str(current_dir / "config"))
sys.path.append(str(current_dir / "src"))

# Importaciones principales
try:
    from ui.styles.theme_manager import theme_manager, apply_current_theme
    from config.settings import AppConfig, DatabaseConfig, MediaConfig
    from ui.pages import dashboard, customers, video_gallery, image_gallery, audio_player, analytics, settings_page
    from ui.auth.login import render_login, check_authentication
    from ui.components.sidebar import render_sidebar
except ImportError as e:
    st.error(f"Error importando módulos: {e}")
    st.info("Asegúrate de que todos los archivos estén en su lugar")

# ================== CONFIGURACIÓN DE PÁGINA ==================
st.set_page_config(
    page_title=f"🔥 {AppConfig.APP_NAME}",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/tu-usuario/media-management',
        'Report a bug': 'https://github.com/tu-usuario/media-management/issues',
        'About': f"# {AppConfig.APP_NAME} v{AppConfig.APP_VERSION}\n¡El sistema multimedia más BRUTAL!"
    }
)

# ================== APLICAR TEMA BRUTAL ==================
apply_current_theme()

# ================== INICIALIZACIÓN DE ESTADO ==================
def initialize_session_state():
    """Inicializa el estado de la sesión"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "🏠 Dashboard"
    if 'theme' not in st.session_state:
        st.session_state.theme = "dark"

initialize_session_state()

# ================== AUTENTICACIÓN ==================
if not st.session_state.authenticated:
    render_login()
    st.stop()

# ================== NAVEGACIÓN PRINCIPAL ==================
def main():
    """Función principal de la aplicación"""
    
    # Sidebar de navegación
    page = render_sidebar()
    st.session_state.current_page = page
    
    # Header principal
    st.markdown(f"""
    <div class="animate-fadeInDown" style="
        text-align: center; 
        margin-bottom: 2rem;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    ">
        <h1 style="
            font-size: 3rem; 
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        ">
            🎬 {AppConfig.APP_NAME}
        </h1>
        <p style="
            font-size: 1.2rem; 
            color: #b8bcc8; 
            margin: 0;
        ">
            v{AppConfig.APP_VERSION} - Usuario: <strong>{st.session_state.user.title()}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enrutamiento de páginas
    try:
        if page == "🏠 Dashboard":
            dashboard.render()
        elif page == "👥 Customers":
            customers.render()
        elif page == "🎥 Videos":
            video_gallery.render()
        elif page == "🖼️ Imágenes":
            image_gallery.render()
        elif page == "🎵 Audio":
            audio_player.render()
        elif page == "📊 Analytics":
            analytics.render()
        elif page == "⚙️ Configuración":
            settings_page.render()
        else:
            st.error(f"Página no encontrada: {page}")
    
    except Exception as e:
        st.error(f"Error cargando página: {e}")
        st.info("Refresca la página o contacta al administrador")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="
        text-align: center; 
        padding: 1rem;
        color: #6b7280; 
        font-size: 0.9rem;
    ">
        🔥 <strong>{AppConfig.APP_NAME} v{AppConfig.APP_VERSION}</strong> 🔥<br>
        Desarrollado con 💜 por el equipo más BRUTAL
    </div>
    """, unsafe_allow_html=True)

# ================== EJECUTAR APLICACIÓN ==================
if __name__ == "__main__":
    main()