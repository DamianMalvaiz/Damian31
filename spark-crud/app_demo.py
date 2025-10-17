# app_demo.py
# DEMO TEMPORAL - MEDIA MANAGEMENT SYSTEM BRUTAL
# ==============================================
# ¡Prepárate para ver la BRUTALIDAD visual más épica!

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import time
import random

# Importar nuestro gestor de temas épico
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui', 'styles'))

try:
    from theme_manager import theme_manager, apply_current_theme
except ImportError:
    # Fallback si no se puede importar
    class DummyThemeManager:
        def apply_theme(self): pass
        def render_theme_selector(self): pass
    theme_manager = DummyThemeManager()
    def apply_current_theme(): pass

# ================== CONFIGURACIÓN DE PÁGINA ==================
st.set_page_config(
    page_title="🔥 Media Management System - BRUTAL DEMO",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== APLICAR TEMA BRUTAL ==================
apply_current_theme()

# ================== DATOS DEMO ==================
@st.cache_data
def generate_demo_data():
    """Genera datos de demostración épicos"""
    
    # Datos de customers
    customers_data = {
        'id': range(1, 101),
        'name': [f"Usuario Épico {i}" for i in range(1, 101)],
        'email': [f"user{i}@brutal.com" for i in range(1, 101)],
        'balance': np.random.uniform(100, 10000, 100),
        'created_at': pd.date_range('2023-01-01', periods=100, freq='D'),
        'sex': np.random.choice(['M', 'F'], 100),
        'job_title': np.random.choice(['Developer', 'Designer', 'Manager', 'Analyst'], 100)
    }
    
    # Datos de videos
    videos_data = {
        'id': range(1, 51),
        'title': [f"Video Épico {i}" for i in range(1, 51)],
        'duration': np.random.uniform(30, 600, 50),
        'views': np.random.randint(100, 100000, 50),
        'likes': np.random.randint(10, 5000, 50),
        'status': np.random.choice(['ready', 'processing', 'pending'], 50, p=[0.8, 0.1, 0.1])
    }
    
    # Datos de imágenes
    images_data = {
        'id': range(1, 51),
        'title': [f"Imagen Brutal {i}" for i in range(1, 51)],
        'width': np.random.randint(800, 4000, 50),
        'height': np.random.randint(600, 3000, 50),
        'size_mb': np.random.uniform(0.5, 15, 50),
        'downloads': np.random.randint(50, 10000, 50)
    }
    
    # Datos de audio
    audio_data = {
        'id': range(1, 31),
        'title': [f"Track Épico {i}" for i in range(1, 31)],
        'artist': [f"Artista {i}" for i in range(1, 31)],
        'duration': np.random.uniform(120, 300, 30),
        'plays': np.random.randint(100, 50000, 30),
        'bpm': np.random.randint(60, 180, 30)
    }
    
    return (
        pd.DataFrame(customers_data),
        pd.DataFrame(videos_data), 
        pd.DataFrame(images_data),
        pd.DataFrame(audio_data)
    )

# Cargar datos
customers_df, videos_df, images_df, audio_df = generate_demo_data()

# ================== SIDEBAR ÉPICO ==================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="
            font-size: 2rem; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        ">
            🔥 BRUTAL DEMO
        </h1>
        <p style="color: #b8bcc8; font-size: 0.9rem;">Media Management System v2.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de página
    page = st.radio(
        "🧭 Navegación",
        [
            "🏠 Dashboard Épico",
            "👥 Customers Brutales", 
            "🎥 Videos Center",
            "🖼️ Galería de Imágenes",
            "🎵 Audio Player",
            "📊 Analytics Salvajes",
            "🎨 Temas & Estilos",
            "⚙️ Configuración"
        ],
        key="navigation"
    )
    
    st.markdown("---")
    
    # Stats rápidas
    st.markdown("### 📈 Stats en Vivo")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👥 Users", len(customers_df), delta="+12")
        st.metric("🎥 Videos", len(videos_df), delta="+3")
    
    with col2:
        st.metric("🖼️ Images", len(images_df), delta="+8")
        st.metric("🎵 Tracks", len(audio_df), delta="+2")
    
    st.markdown("---")
    
    # Selector de tema
    if st.button("🎨 Cambiar Tema", use_container_width=True):
        theme_manager.render_theme_selector()

# ================== HEADER ÉPICO ==================
st.markdown("""
<div class="animate-fadeInDown" style="
    text-align: center; 
    margin-bottom: 3rem;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
">
    <h1 style="
        font-size: 4rem; 
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        animation: titleGlow 3s ease-in-out infinite alternate;
    ">
        🎬 MEDIA MANAGEMENT SYSTEM
    </h1>
    <p style="
        font-size: 1.5rem; 
        color: #b8bcc8; 
        margin-bottom: 0;
        font-weight: 300;
    ">
        ⚡ La plataforma multimedia más BRUTAL del universo ⚡
    </p>
</div>
""", unsafe_allow_html=True)

# ================== PÁGINAS ==================

if page == "🏠 Dashboard Épico":
    st.markdown("## 🚀 Dashboard de Control Central")
    
    # KPIs Brutales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="card animate-zoomIn delay-100" style="text-align: center;">
            <div style="
                font-size: 3rem; 
                font-weight: 900;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">
                {total_users}
            </div>
            <div style="color: #b8bcc8; text-transform: uppercase; letter-spacing: 2px;">
                👥 USUARIOS TOTALES
            </div>
        </div>
        """.format(total_users=len(customers_df)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card animate-zoomIn delay-200" style="text-align: center;">
            <div style="
                font-size: 3rem; 
                font-weight: 900;
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">
                {total_videos}
            </div>
            <div style="color: #b8bcc8; text-transform: uppercase; letter-spacing: 2px;">
                🎥 VIDEOS ÉPICOS
            </div>
        </div>
        """.format(total_videos=len(videos_df)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card animate-zoomIn delay-300" style="text-align: center;">
            <div style="
                font-size: 3rem; 
                font-weight: 900;
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">
                {total_images}
            </div>
            <div style="color: #b8bcc8; text-transform: uppercase; letter-spacing: 2px;">
                🖼️ IMÁGENES BRUTALES
            </div>
        </div>
        """.format(total_images=len(images_df)), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="card animate-zoomIn delay-500" style="text-align: center;">
            <div style="
                font-size: 3rem; 
                font-weight: 900;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">
                {total_audio}
            </div>
            <div style="color: #b8bcc8; text-transform: uppercase; letter-spacing: 2px;">
                🎵 TRACKS SALVAJES
            </div>
        </div>
        """.format(total_audio=len(audio_df)), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos épicos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Crecimiento de Usuarios")
        
        # Generar datos de crecimiento
        dates = pd.date_range('2023-01-01', periods=30, freq='D')
        growth_data = pd.DataFrame({
            'Fecha': dates,
            'Usuarios': np.cumsum(np.random.randint(1, 10, 30))
        })
        
        st.line_chart(growth_data.set_index('Fecha'))
    
    with col2:
        st.markdown("### 🎯 Distribución de Contenido")
        
        content_data = pd.DataFrame({
            'Tipo': ['Videos', 'Imágenes', 'Audio', 'Documentos'],
            'Cantidad': [len(videos_df), len(images_df), len(audio_df), 25]
        })
        
        st.bar_chart(content_data.set_index('Tipo'))
    
    # Actividad reciente
    st.markdown("### 🔥 Actividad Reciente")
    
    activities = [
        "🎥 Nuevo video subido: 'Tutorial Épico de Python'",
        "👥 Usuario 'CodingMaster' se registró",
        "🖼️ Imagen optimizada: 'Landscape Brutal.jpg'",
        "🎵 Track añadido: 'Synthwave Dreams'",
        "📊 Reporte de analytics generado",
        "🔧 Sistema actualizado a v2.0"
    ]
    
    for i, activity in enumerate(activities):
        st.markdown(f"""
        <div class="animate-fadeInLeft delay-{i*100}" style="
            background: rgba(255, 255, 255, 0.05);
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            border-left: 4px solid #00d4ff;
        ">
            {activity}
        </div>
        """, unsafe_allow_html=True)

elif page == "👥 Customers Brutales":
    st.markdown("## 👥 Gestión de Customers Épica")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_name = st.text_input("🔍 Buscar por nombre", placeholder="Ingresa nombre...")
    
    with col2:
        filter_sex = st.selectbox("⚧ Filtrar por sexo", ["Todos", "M", "F"])
    
    with col3:
        min_balance = st.number_input("💰 Balance mínimo", min_value=0.0, value=0.0)
    
    # Aplicar filtros
    filtered_df = customers_df.copy()
    
    if search_name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False)]
    
    if filter_sex != "Todos":
        filtered_df = filtered_df[filtered_df['sex'] == filter_sex]
    
    if min_balance > 0:
        filtered_df = filtered_df[filtered_df['balance'] >= min_balance]
    
    st.markdown(f"### 📋 Mostrando {len(filtered_df)} de {len(customers_df)} customers")
    
    # Tabla épica con estilos
    st.markdown("""
    <style>
    .stDataFrame {
        background: rgba(30, 30, 46, 0.8);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        filtered_df.head(20),
        use_container_width=True,
        height=400
    )
    
    # Botones de acción
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Agregar Customer", use_container_width=True):
            st.success("🎉 ¡Customer agregado con éxito!")
    
    with col2:
        if st.button("📊 Generar Reporte", use_container_width=True):
            st.info("📈 Generando reporte épico...")
    
    with col3:
        if st.button("📤 Exportar CSV", use_container_width=True):
            st.success("💾 ¡Datos exportados!")

elif page == "🎥 Videos Center":
    st.markdown("## 🎥 Centro de Videos Épico")
    
    # Grid de videos
    st.markdown("### 🔥 Videos Más Populares")
    
    # Crear grid de 3 columnas
    cols = st.columns(3)
    
    for i, (_, video) in enumerate(videos_df.head(9).iterrows()):
        col_idx = i % 3
        
        with cols[col_idx]:
            # Simular thumbnail
            thumbnail_color = random.choice(['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'])
            
            st.markdown(f"""
            <div class="card animate-fadeInUp delay-{i*100}" style="
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                <div style="
                    width: 100%;
                    height: 150px;
                    background: {thumbnail_color};
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-bottom: 1rem;
                    position: relative;
                ">
                    <div style="
                        width: 60px;
                        height: 60px;
                        background: rgba(255, 255, 255, 0.9);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.5rem;
                    ">
                        ▶️
                    </div>
                    <div style="
                        position: absolute;
                        bottom: 8px;
                        right: 8px;
                        background: rgba(0, 0, 0, 0.8);
                        color: white;
                        padding: 4px 8px;
                        border-radius: 4px;
                        font-size: 0.8rem;
                    ">
                        {int(video['duration']//60)}:{int(video['duration']%60):02d}
                    </div>
                </div>
                <h4 style="margin-bottom: 0.5rem;">{video['title']}</h4>
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #b8bcc8;">
                    <span>👁️ {video['views']:,}</span>
                    <span>❤️ {video['likes']:,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Controles de video
    st.markdown("### 🎛️ Reproductor de Video")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div style="
            background: #000;
            aspect-ratio: 16/9;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            color: #666;
            border: 2px solid rgba(255, 255, 255, 0.1);
        ">
            🎬
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Controles")
        
        if st.button("▶️ Play", use_container_width=True):
            st.success("🎬 Reproduciendo...")
        
        if st.button("⏸️ Pause", use_container_width=True):
            st.info("⏸️ Pausado")
        
        if st.button("⏹️ Stop", use_container_width=True):
            st.warning("⏹️ Detenido")
        
        volume = st.slider("🔊 Volumen", 0, 100, 50)
        
        st.markdown("#### 📊 Info")
        st.metric("Duración", "05:42")
        st.metric("Calidad", "1080p")
        st.metric("FPS", "60")

elif page == "🖼️ Galería de Imágenes":
    st.markdown("## 🖼️ Galería de Imágenes Brutal")
    
    # Filtros de imágenes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        size_filter = st.selectbox("📏 Filtrar por tamaño", ["Todas", "Pequeñas (<2MB)", "Medianas (2-10MB)", "Grandes (>10MB)"])
    
    with col2:
        resolution_filter = st.selectbox("🖥️ Resolución", ["Todas", "HD (1280x720)", "Full HD (1920x1080)", "4K (3840x2160)"])
    
    with col3:
        sort_by = st.selectbox("🔄 Ordenar por", ["Más recientes", "Más descargadas", "Más grandes"])
    
    # Grid de imágenes
    st.markdown("### 🎨 Galería Principal")
    
    # Crear grid de 4 columnas
    cols = st.columns(4)
    
    colors = ['#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43', '#10ac84', '#ee5253', '#0abde3']
    
    for i in range(16):  # Mostrar 16 imágenes
        col_idx = i % 4
        
        with cols[col_idx]:
            color = colors[i % len(colors)]
            
            st.markdown(f"""
            <div class="animate-fadeInUp delay-{i*50}" style="
                background: {color};
                aspect-ratio: 1;
                border-radius: 12px;
                margin-bottom: 1rem;
                position: relative;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                color: white;
                font-weight: bold;
            " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                🖼️
                <div style="
                    position: absolute;
                    bottom: 8px;
                    left: 8px;
                    background: rgba(0, 0, 0, 0.8);
                    color: white;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 0.7rem;
                ">
                    IMG_{i+1:03d}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Lightbox demo
    st.markdown("### 🔍 Vista Detallada")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(45deg, #667eea, #764ba2);
            aspect-ratio: 16/10;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 6rem;
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.2);
        ">
            🌟
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📋 Metadata")
        st.metric("Resolución", "3840x2160")
        st.metric("Tamaño", "8.5 MB")
        st.metric("Formato", "JPEG")
        st.metric("Descargas", "1,247")
        
        if st.button("⬇️ Descargar", use_container_width=True):
            st.success("📥 ¡Descarga iniciada!")
        
        if st.button("❤️ Me Gusta", use_container_width=True):
            st.success("💖 ¡Agregado a favoritos!")

elif page == "🎵 Audio Player":
    st.markdown("## 🎵 Reproductor de Audio Épico")
    
    # Player principal
    st.markdown("### 🎧 Now Playing")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(45deg, #f093fb, #f5576c);
            aspect-ratio: 1;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            color: white;
            animation: rotate 10s linear infinite;
            border: 4px solid rgba(255, 255, 255, 0.2);
        ">
            🎵
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎤 Track Épico #1")
        st.markdown("**Artista:** DJ Brutal")
        st.markdown("**Álbum:** Synthwave Dreams")
        st.markdown("**Duración:** 04:32")
        
        # Progress bar
        progress = st.slider("", 0, 272, 45, label_visibility="collapsed")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown("01:45")
        with col_b:
            st.markdown("<center>🎵</center>", unsafe_allow_html=True)
        with col_c:
            st.markdown("<div style='text-align: right'>04:32</div>", unsafe_allow_html=True)
    
    # Controles
    st.markdown("### 🎛️ Controles")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("⏮️ Anterior", use_container_width=True):
            st.info("⏮️ Pista anterior")
    
    with col2:
        if st.button("▶️ Play", use_container_width=True):
            st.success("🎵 Reproduciendo...")
    
    with col3:
        if st.button("⏸️ Pause", use_container_width=True):
            st.warning("⏸️ Pausado")
    
    with col4:
        if st.button("⏭️ Siguiente", use_container_width=True):
            st.info("⏭️ Siguiente pista")
    
    with col5:
        if st.button("🔀 Aleatorio", use_container_width=True):
            st.success("🔀 Modo aleatorio")
    
    # Playlist
    st.markdown("### 📜 Playlist Brutal")
    
    for i, (_, track) in enumerate(audio_df.head(10).iterrows()):
        is_playing = i == 0
        
        st.markdown(f"""
        <div class="animate-fadeInLeft delay-{i*50}" style="
            background: {'rgba(0, 212, 255, 0.2)' if is_playing else 'rgba(255, 255, 255, 0.05)'};
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            border-left: 4px solid {'#00d4ff' if is_playing else 'transparent'};
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            <div>
                <strong>{'🎵 ' if is_playing else ''}{track['title']}</strong><br>
                <small style="color: #b8bcc8;">{track['artist']} • {int(track['duration']//60)}:{int(track['duration']%60):02d}</small>
            </div>
            <div style="text-align: right; font-size: 0.9rem; color: #b8bcc8;">
                ▶️ {track['plays']:,}<br>
                🎵 {track['bpm']} BPM
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "📊 Analytics Salvajes":
    st.markdown("## 📊 Analytics de Otro Mundo")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🔥 Total Views", 
            "2.4M", 
            delta="↗️ +15.2%",
            help="Visualizaciones totales este mes"
        )
    
    with col2:
        st.metric(
            "⬇️ Downloads", 
            "847K", 
            delta="↗️ +8.7%",
            help="Descargas totales"
        )
    
    with col3:
        st.metric(
            "👥 Active Users", 
            "12.8K", 
            delta="↗️ +22.1%",
            help="Usuarios activos diarios"
        )
    
    with col4:
        st.metric(
            "💾 Storage Used", 
            "1.2TB", 
            delta="↗️ +5.3%",
            help="Almacenamiento utilizado"
        )
    
    # Gráficos avanzados
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Engagement por Tipo de Contenido")
        
        engagement_data = pd.DataFrame({
            'Videos': np.random.randint(50, 100, 30),
            'Imágenes': np.random.randint(30, 80, 30),
            'Audio': np.random.randint(20, 60, 30)
        }, index=pd.date_range('2023-01-01', periods=30, freq='D'))
        
        st.area_chart(engagement_data)
    
    with col2:
        st.markdown("### 🎯 Top Formatos")
        
        format_data = pd.DataFrame({
            'Formato': ['MP4', 'JPEG', 'PNG', 'MP3', 'WEBP'],
            'Uso (%)': [35, 28, 18, 12, 7]
        })
        
        st.bar_chart(format_data.set_index('Formato'))
    
    # Heatmap de actividad
    st.markdown("### 🔥 Mapa de Calor - Actividad por Hora")
    
    # Generar datos de heatmap
    hours = list(range(24))
    days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    heatmap_data = []
    for day in days:
        row = []
        for hour in hours:
            # Simular más actividad en horas laborales
            if 9 <= hour <= 17:
                activity = np.random.randint(60, 100)
            elif 19 <= hour <= 23:
                activity = np.random.randint(40, 80)
            else:
                activity = np.random.randint(10, 40)
            row.append(activity)
        heatmap_data.append(row)
    
    heatmap_df = pd.DataFrame(heatmap_data, columns=hours, index=days)
    
    st.markdown("""
    <div style="
        background: rgba(30, 30, 46, 0.8);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    ">
        <p style="text-align: center; color: #b8bcc8;">
            🔥 Actividad más intensa en horarios laborales y nocturnos
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "🎨 Temas & Estilos":
    st.markdown("## 🎨 Centro de Control de Temas")
    
    # Selector de temas
    theme_manager.render_theme_selector()
    
    st.markdown("---")
    
    # Demostración de componentes
    st.markdown("### 🧪 Demostración de Componentes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔘 Botones Épicos")
        
        if st.button("🚀 Botón Primario", use_container_width=True):
            st.balloons()
        
        if st.button("⚡ Botón Secundario", use_container_width=True, type="secondary"):
            st.snow()
        
        st.markdown("#### 📊 Métricas")
        st.metric("🔥 Poder Brutal", "9000+", delta="↗️ OVER 9000!")
        
    with col2:
        st.markdown("#### 🎛️ Controles")
        
        slider_val = st.slider("🌈 Intensidad de Brutalidad", 0, 100, 85)
        
        option = st.selectbox(
            "🎯 Nivel de Épico",
            ["Brutal", "Épico", "Legendario", "OVER 9000"]
        )
        
        st.text_input("💬 Mensaje Brutal", placeholder="Escribe algo épico...")
    
    # Paleta de colores
    st.markdown("### 🎨 Paleta de Colores Actual")
    
    colors = [
        ("#3b82f6", "Primario"),
        ("#8b5cf6", "Secundario"), 
        ("#06d6a0", "Acento"),
        ("#ff6b6b", "Peligro"),
        ("#feca57", "Advertencia"),
        ("#48dbfb", "Info")
    ]
    
    cols = st.columns(len(colors))
    
    for i, (color, name) in enumerate(colors):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background: {color};
                height: 100px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                margin-bottom: 0.5rem;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            ">
                {name}
            </div>
            <div style="text-align: center; font-size: 0.8rem; color: #b8bcc8;">
                {color}
            </div>
            """, unsafe_allow_html=True)

else:  # Configuración
    st.markdown("## ⚙️ Centro de Configuración")
    
    # Configuración del sistema
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 Configuración General")
        
        st.checkbox("🔔 Notificaciones push", value=True)
        st.checkbox("🌙 Modo oscuro automático", value=True)
        st.checkbox("⚡ Animaciones habilitadas", value=True)
        st.checkbox("🔊 Sonidos de interfaz", value=False)
        
        st.selectbox("🌍 Idioma", ["Español", "English", "Français"])
        st.selectbox("🕒 Zona horaria", ["UTC-6 (México)", "UTC-5 (Colombia)", "UTC-3 (Argentina)"])
    
    with col2:
        st.markdown("### 📊 Configuración de Datos")
        
        st.number_input("📄 Elementos por página", min_value=10, max_value=100, value=25)
        st.number_input("💾 Límite de subida (MB)", min_value=1, max_value=500, value=50)
        st.number_input("🔄 Intervalo de sync (min)", min_value=1, max_value=60, value=5)
        
        st.selectbox("🗃️ Base de datos", ["MongoDB", "PostgreSQL", "MySQL"])
        st.selectbox("☁️ Almacenamiento", ["Local", "AWS S3", "Google Cloud"])
    
    # Estado del sistema
    st.markdown("### 📡 Estado del Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid #22c55e;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        ">
            <div style="color: #22c55e; font-size: 2rem;">✅</div>
            <div style="color: #22c55e; font-weight: bold;">API</div>
            <div style="color: #b8bcc8; font-size: 0.8rem;">Operativo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid #22c55e;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        ">
            <div style="color: #22c55e; font-size: 2rem;">💾</div>
            <div style="color: #22c55e; font-weight: bold;">Base de Datos</div>
            <div style="color: #b8bcc8; font-size: 0.8rem;">Conectada</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background: rgba(251, 146, 60, 0.2);
            border: 1px solid #fb923c;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        ">
            <div style="color: #fb923c; font-size: 2rem;">⚠️</div>
            <div style="color: #fb923c; font-weight: bold;">Almacenamiento</div>
            <div style="color: #b8bcc8; font-size: 0.8rem;">85% Usado</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid #22c55e;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        ">
            <div style="color: #22c55e; font-size: 2rem;">🚀</div>
            <div style="color: #22c55e; font-weight: bold;">Rendimiento</div>
            <div style="color: #b8bcc8; font-size: 0.8rem;">Excelente</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Botones de acción
    st.markdown("### 🛠️ Acciones del Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reiniciar Sistema", use_container_width=True):
            with st.spinner("Reiniciando sistema..."):
                time.sleep(2)
            st.success("✅ Sistema reiniciado correctamente")
    
    with col2:
        if st.button("💾 Crear Backup", use_container_width=True):
            with st.spinner("Creando backup..."):
                time.sleep(3)
            st.success("💾 Backup creado exitosamente")
    
    with col3:
        if st.button("🧹 Limpiar Cache", use_container_width=True):
            with st.spinner("Limpiando cache..."):
                time.sleep(1)
            st.success("🧹 Cache limpiado")

# ================== FOOTER ÉPICO ==================
st.markdown("---")
st.markdown("""
<div style="
    text-align: center; 
    padding: 2rem;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
    border-radius: 16px;
    margin-top: 3rem;
">
    <p style="
        color: #b8bcc8; 
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    ">
        🔥 <strong>Media Management System v2.0</strong> 🔥
    </p>
    <p style="
        color: #6b7280; 
        font-size: 0.9rem;
        margin: 0;
    ">
        Desarrollado con 💜 por el equipo más BRUTAL del universo
    </p>
</div>
""", unsafe_allow_html=True)

# ================== EFECTOS ESPECIALES ==================
# Partículas flotantes (opcional)
if st.session_state.get('show_particles', False):
    st.markdown("""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background: 
            radial-gradient(circle at 25% 25%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(185, 103, 219, 0.1) 0%, transparent 50%);
        animation: backgroundShift 20s ease-in-out infinite;
    ">
    </div>
    """, unsafe_allow_html=True)