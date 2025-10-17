# ui/pages/settings.py
# Página de configuración del sistema
# ===================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

def render():
    """Renderiza la página de configuración"""
    
    # Header de la página
    st.markdown("""
    <div class="animate-fadeInDown">
        <h2 style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        ">
            ⚙️ Centro de Configuración
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Importar gestor de temas
    try:
        from ui.styles.theme_manager import theme_manager
        has_theme_manager = True
    except ImportError:
        has_theme_manager = False
    
    # Tabs de configuración
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎨 Temas", "🔧 General", "🗄️ Base de Datos", "🎬 Multimedia", "👥 Usuarios"
    ])
    
    with tab1:
        st.markdown("### 🎨 Personalización de Temas")
        
        if has_theme_manager:
            theme_manager.render_theme_selector()
        else:
            # Selector básico de temas
            col1, col2 = st.columns(2)
            
            with col1:
                current_theme = st.session_state.get('current_theme', 'dark')
                theme = st.selectbox(
                    "Selecciona tu tema favorito:",
                    ["dark", "cyberpunk", "matrix", "synthwave"],
                    index=["dark", "cyberpunk", "matrix", "synthwave"].index(current_theme)
                )
                
                if theme != current_theme:
                    st.session_state.current_theme = theme
                    st.success(f"✨ Tema '{theme}' aplicado!")
            
            with col2:
                st.markdown("#### 🎨 Personalización")
                
                primary_color = st.color_picker("Color Primario", "#3b82f6")
                secondary_color = st.color_picker("Color Secundario", "#8b5cf6")
                accent_color = st.color_picker("Color de Acento", "#06d6a0")
        
        # Configuración de animaciones
        st.markdown("#### ⚡ Animaciones")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            enable_animations = st.checkbox("🎬 Habilitar animaciones", value=True)
        
        with col2:
            animation_speed = st.selectbox("🚀 Velocidad", ["Lenta", "Normal", "Rápida"], index=1)
        
        with col3:
            enable_particles = st.checkbox("✨ Efectos de partículas", value=False)
        
        # Preview de tema
        st.markdown("#### 👁️ Preview del Tema")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #3b82f6, #8b5cf6);
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
                color: white;
                font-weight: bold;
                margin-bottom: 1rem;
            ">
                🎨 Botón Primario
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid #8b5cf6;
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
                color: #8b5cf6;
                font-weight: bold;
                margin-bottom: 1rem;
            ">
                🎯 Botón Secundario
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="
                background: rgba(30, 30, 46, 0.8);
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 1rem;
            ">
                📋 Card Ejemplo
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🔧 Configuración General")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌐 Configuración Regional")
            
            language = st.selectbox("🌍 Idioma", ["Español", "English", "Français", "Deutsch"])
            timezone = st.selectbox("🕒 Zona Horaria", [
                "UTC-6 (México)", "UTC-5 (Colombia)", "UTC-3 (Argentina)", 
                "UTC+1 (España)", "UTC+0 (GMT)"
            ])
            date_format = st.selectbox("📅 Formato de Fecha", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
            
            st.markdown("#### 🔔 Notificaciones")
            
            email_notifications = st.checkbox("📧 Notificaciones por email", value=True)
            push_notifications = st.checkbox("🔔 Notificaciones push", value=True)
            sound_notifications = st.checkbox("🔊 Sonidos de notificación", value=False)
            
            notification_frequency = st.selectbox("⏰ Frecuencia", [
                "Inmediata", "Cada hora", "Diaria", "Semanal"
            ])
        
        with col2:
            st.markdown("#### 📊 Configuración de Datos")
            
            page_size = st.number_input("📄 Elementos por página", min_value=10, max_value=100, value=25)
            auto_refresh = st.number_input("🔄 Auto-refresh (segundos)", min_value=0, max_value=300, value=30)
            cache_duration = st.number_input("💾 Duración de cache (minutos)", min_value=1, max_value=60, value=10)
            
            st.markdown("#### 🚀 Performance")
            
            lazy_loading = st.checkbox("⚡ Carga perezosa", value=True)
            compress_images = st.checkbox("🗜️ Comprimir imágenes", value=True)
            enable_cdn = st.checkbox("🌐 Usar CDN", value=False)
            
            max_concurrent = st.number_input("🔀 Máx. conexiones concurrentes", min_value=1, max_value=100, value=10)
        
        # Botones de acción
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Guardar Configuración", use_container_width=True):
                with st.spinner("Guardando configuración..."):
                    time.sleep(1)
                st.success("✅ Configuración guardada!")
        
        with col2:
            if st.button("🔄 Restaurar Defaults", use_container_width=True):
                st.warning("⚠️ Configuración restaurada a valores por defecto")
        
        with col3:
            if st.button("📤 Exportar Config", use_container_width=True):
                st.success("📄 Configuración exportada!")
    
    with tab3:
        st.markdown("### 🗄️ Configuración de Base de Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔌 Conexión")
            
            db_type = st.selectbox("🗃️ Tipo de Base de Datos", ["MongoDB", "PostgreSQL", "MySQL"])
            db_host = st.text_input("🌐 Host", value="localhost")
            db_port = st.number_input("🔌 Puerto", value=27017)
            db_name = st.text_input("🗄️ Nombre de BD", value="media_management")
            
            # Test de conexión
            if st.button("🔍 Probar Conexión", use_container_width=True):
                with st.spinner("Probando conexión..."):
                    time.sleep(2)
                    # Simular resultado aleatorio
                    if np.random.random() > 0.2:
                        st.success("✅ Conexión exitosa!")
                    else:
                        st.error("❌ Error de conexión")
        
        with col2:
            st.markdown("#### ⚙️ Configuración Avanzada")
            
            connection_pool = st.number_input("🏊 Pool de conexiones", min_value=1, max_value=100, value=10)
            timeout = st.number_input("⏰ Timeout (segundos)", min_value=1, max_value=60, value=30)
            retry_attempts = st.number_input("🔄 Intentos de reintento", min_value=1, max_value=10, value=3)
            
            enable_ssl = st.checkbox("🔒 Habilitar SSL", value=False)
            enable_compression = st.checkbox("🗜️ Compresión de datos", value=True)
            
            st.markdown("#### 📊 Colecciones")
            
            collections = ["customers", "videos", "images", "audio", "analytics"]
            for collection in collections:
                st.text_input(f"📁 {collection.title()}", value=collection, key=f"coll_{collection}")
        
        # Estado de la base de datos
        st.markdown("#### 📡 Estado de la Base de Datos")
        
        col1, col2, col3, col4 = st.columns(4)
        
        status_items = [
            ("Conexión", "✅", "Activa", "#22c55e"),
            ("Índices", "✅", "Optimizados", "#22c55e"),
            ("Respaldo", "⚠️", "Pendiente", "#f59e0b"),
            ("Performance", "✅", "Excelente", "#22c55e")
        ]
        
        for col, (item, status, detail, color) in zip([col1, col2, col3, col4], status_items):
            with col:
                st.markdown(f"""
                <div style="
                    background: rgba(255, 255, 255, 0.05);
                    border: 1px solid {color};
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                ">
                    <div style="color: {color}; font-size: 1.5rem;">{status}</div>
                    <div style="color: {color}; font-weight: bold; font-size: 0.9rem;">{item}</div>
                    <div style="color: #b8bcc8; font-size: 0.7rem;">{detail}</div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🎬 Configuración Multimedia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📁 Límites de Archivos")
            
            max_video_size = st.number_input("🎥 Máx. tamaño video (MB)", min_value=1, max_value=2000, value=500)
            max_image_size = st.number_input("🖼️ Máx. tamaño imagen (MB)", min_value=1, max_value=100, value=50)
            max_audio_size = st.number_input("🎵 Máx. tamaño audio (MB)", min_value=1, max_value=200, value=100)
            
            st.markdown("#### 🎨 Calidad y Optimización")
            
            image_quality = st.slider("🖼️ Calidad de imagen (%)", 50, 100, 85)
            auto_optimize = st.checkbox("⚡ Optimización automática", value=True)
            generate_thumbnails = st.checkbox("🖼️ Generar miniaturas", value=True)
            
            thumbnail_size = st.selectbox("📏 Tamaño de miniaturas", [
                "150x150", "200x200", "300x300", "400x400"
            ])
        
        with col2:
            st.markdown("#### 🎥 Configuración de Video")
            
            video_formats = st.multiselect(
                "📄 Formatos permitidos",
                ["MP4", "AVI", "MOV", "MKV", "WEBM", "FLV"],
                default=["MP4", "AVI", "MOV", "MKV"]
            )
            
            video_quality = st.selectbox("🎬 Calidad por defecto", ["480p", "720p", "1080p", "4K"])
            auto_convert = st.checkbox("🔄 Conversión automática a MP4", value=True)
            
            st.markdown("#### 🖼️ Configuración de Imágenes")
            
            image_formats = st.multiselect(
                "📄 Formatos permitidos",
                ["JPEG", "PNG", "GIF", "WebP", "BMP", "TIFF"],
                default=["JPEG", "PNG", "GIF", "WebP"]
            )
            
            auto_webp = st.checkbox("🔄 Conversión automática a WebP", value=True)
            
            st.markdown("#### 🎵 Configuración de Audio")
            
            audio_formats = st.multiselect(
                "📄 Formatos permitidos",
                ["MP3", "WAV", "FLAC", "AAC", "OGG", "M4A"],
                default=["MP3", "WAV", "FLAC", "AAC"]
            )
            
            audio_bitrate = st.selectbox("🎵 Bitrate por defecto", ["128 kbps", "192 kbps", "256 kbps", "320 kbps"])
        
        # Procesamiento en lotes
        st.markdown("#### 🔄 Procesamiento en Lotes")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎥 Procesar Videos Pendientes", use_container_width=True):
                with st.spinner("Procesando videos..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.02)
                st.success("✅ Videos procesados!")
        
        with col2:
            if st.button("🖼️ Optimizar Imágenes", use_container_width=True):
                with st.spinner("Optimizando imágenes..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.02)
                st.success("✅ Imágenes optimizadas!")
        
        with col3:
            if st.button("🎵 Analizar Audio", use_container_width=True):
                with st.spinner("Analizando audio..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        time.sleep(0.02)
                st.success("✅ Audio analizado!")
    
    with tab5:
        st.markdown("### 👥 Gestión de Usuarios")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Usuarios Actuales")
            
            users_data = pd.DataFrame({
                'Usuario': ['damian', 'david', 'alexis'],
                'Rol': ['Admin', 'Editor', 'Viewer'],
                'Último Acceso': ['Hace 5 min', 'Hace 2 horas', 'Hace 1 día'],
                'Estado': ['🟢 Activo', '🟡 Inactivo', '🟢 Activo']
            })
            
            st.dataframe(users_data, use_container_width=True, hide_index=True)
            
            st.markdown("#### ➕ Agregar Usuario")
            
            new_username = st.text_input("👤 Nombre de usuario")
            new_role = st.selectbox("🎭 Rol", ["Admin", "Editor", "Viewer"])
            new_password = st.text_input("🔒 Contraseña", type="password")
            
            if st.button("➕ Agregar Usuario", use_container_width=True):
                if new_username and new_password:
                    st.success(f"✅ Usuario '{new_username}' agregado!")
                else:
                    st.error("❌ Completa todos los campos")
        
        with col2:
            st.markdown("#### 🔐 Configuración de Seguridad")
            
            session_timeout = st.number_input("⏰ Timeout de sesión (horas)", min_value=1, max_value=24, value=8)
            remember_me_days = st.number_input("💭 Recordar por (días)", min_value=1, max_value=90, value=30)
            
            require_2fa = st.checkbox("🔐 Requerir 2FA", value=False)
            password_complexity = st.checkbox("🔒 Contraseñas complejas", value=True)
            
            st.markdown("#### 📊 Permisos por Rol")
            
            permissions_data = pd.DataFrame({
                'Permiso': ['Ver Dashboard', 'Gestionar Customers', 'Subir Media', 'Ver Analytics', 'Configurar Sistema'],
                'Admin': ['✅', '✅', '✅', '✅', '✅'],
                'Editor': ['✅', '✅', '✅', '✅', '❌'],
                'Viewer': ['✅', '❌', '❌', '✅', '❌']
            })
            
            st.dataframe(permissions_data, use_container_width=True, hide_index=True)
            
            st.markdown("#### 🔄 Acciones de Seguridad")
            
            if st.button("🔒 Cambiar Contraseña", use_container_width=True):
                st.info("🔒 Formulario de cambio de contraseña")
            
            if st.button("🚪 Cerrar Todas las Sesiones", use_container_width=True):
                st.warning("⚠️ Todas las sesiones cerradas")
            
            if st.button("📋 Ver Log de Accesos", use_container_width=True):
                st.info("📋 Mostrando log de accesos...")
    
    # Estado del sistema
    st.markdown("### 📡 Estado del Sistema")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    system_components = [
        ("API", "✅", "Operativo", "#22c55e"),
        ("Base de Datos", "✅", "Conectada", "#22c55e"),
        ("Almacenamiento", "⚠️", "85% Usado", "#f59e0b"),
        ("Memoria", "✅", "Normal", "#22c55e"),
        ("CPU", "🟡", "Medio", "#f59e0b")
    ]
    
    for col, (component, status, detail, color) in zip([col1, col2, col3, col4, col5], system_components):
        with col:
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid {color};
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
            ">
                <div style="color: {color}; font-size: 1.5rem;">{status}</div>
                <div style="color: {color}; font-weight: bold; font-size: 0.8rem;">{component}</div>
                <div style="color: #b8bcc8; font-size: 0.7rem;">{detail}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Acciones del sistema
    st.markdown("### 🛠️ Acciones del Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 Reiniciar Sistema", use_container_width=True):
            with st.spinner("Reiniciando sistema..."):
                time.sleep(3)
            st.success("✅ Sistema reiniciado")
    
    with col2:
        if st.button("💾 Crear Backup", use_container_width=True):
            with st.spinner("Creando backup..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                    time.sleep(0.03)
            st.success("💾 Backup creado exitosamente")
    
    with col3:
        if st.button("🧹 Limpiar Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("🧹 Cache limpiado")
    
    with col4:
        if st.button("📊 Generar Reporte", use_container_width=True):
            with st.spinner("Generando reporte del sistema..."):
                time.sleep(2)
            st.success("📈 Reporte generado")
    
    # Información del sistema
    st.markdown("### 💻 Información del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🖥️ Servidor**
        - OS: Linux Ubuntu 20.04
        - CPU: 8 cores @ 3.2GHz
        - RAM: 16GB DDR4
        - Storage: 1TB SSD
        """)
    
    with col2:
        st.markdown("""
        **📊 Base de Datos**
        - MongoDB v6.0.2
        - Conexiones activas: 12/100
        - Tamaño BD: 2.4GB
        - Índices: 15 optimizados
        """)
    
    with col3:
        st.markdown("""
        **🚀 Aplicación**
        - Versión: v2.0.0
        - Uptime: 15 días, 7 horas
        - Requests/min: 847
        - Error rate: 0.02%
        """)