# ui/components/sidebar.py
# Sidebar de navegación con diseño brutal
# =======================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from ui.auth.login import logout, get_current_user, get_user_permissions

def render_sidebar() -> str:
    """Renderiza el sidebar de navegación y retorna la página seleccionada"""
    
    with st.sidebar:
        # Header del sidebar
        st.markdown("""
        <div style="
            text-align: center; 
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <h2 style="
                font-size: 1.8rem; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
                font-weight: 900;
            ">
                🔥 BRUTAL SYSTEM
            </h2>
            <p style="color: #b8bcc8; font-size: 0.9rem; margin: 0;">
                Media Management v2.0
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Información del usuario actual
        current_user = get_current_user()
        permissions = get_user_permissions()
        
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.05);
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        ">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.2rem;
                ">
                    👤
                </div>
                <div>
                    <div style="font-weight: bold; color: white;">{current_user.title()}</div>
                    <div style="color: #b8bcc8; font-size: 0.8rem;">
                        {'🔑 Administrador' if current_user == 'damian' else '✏️ Editor' if current_user == 'david' else '👁️ Viewer'}
                    </div>
                </div>
            </div>
            <div style="color: #6b7280; font-size: 0.7rem;">
                Conectado: {datetime.now().strftime('%H:%M:%S')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navegación principal
        st.markdown("### 🧭 Navegación")
        
        # Páginas disponibles según permisos
        available_pages = []
        
        if permissions.get('view_dashboard', True):
            available_pages.append("🏠 Dashboard")
        
        if permissions.get('manage_customers', True):
            available_pages.append("👥 Customers")
        
        if permissions.get('upload_media', True):
            available_pages.extend(["🎥 Videos", "🖼️ Imágenes", "🎵 Audio"])
        
        if permissions.get('view_analytics', True):
            available_pages.append("📊 Analytics")
        
        if permissions.get('system_config', True):
            available_pages.append("⚙️ Configuración")
        
        # Selector de página
        page = st.radio(
            "Selecciona una página:",
            available_pages,
            key="navigation_radio",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Stats rápidas del sistema
        st.markdown("### 📈 Stats en Vivo")
        
        # Generar stats aleatorias
        stats = {
            "👥 Users": (np.random.randint(1200, 1500), "+12"),
            "🎥 Videos": (np.random.randint(450, 550), "+3"),
            "🖼️ Images": (np.random.randint(800, 1200), "+8"),
            "🎵 Tracks": (np.random.randint(200, 350), "+2")
        }
        
        col1, col2 = st.columns(2)
        
        for i, (label, (value, delta)) in enumerate(stats.items()):
            col = col1 if i % 2 == 0 else col2
            with col:
                st.metric(label, f"{value:,}", delta=delta)
        
        st.markdown("---")
        
        # Actividad reciente mini
        st.markdown("### 🔥 Actividad")
        
        recent_activities = [
            ("🎥", "Video subido", "hace 2m"),
            ("👥", "Nuevo usuario", "hace 5m"),
            ("🖼️", "Imagen optimizada", "hace 8m"),
            ("📊", "Reporte generado", "hace 15m")
        ]
        
        for icon, activity, time_ago in recent_activities:
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.05);
                padding: 0.5rem;
                border-radius: 8px;
                margin-bottom: 0.5rem;
                font-size: 0.8rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span style="font-size: 1rem;">{icon}</span>
                <div style="flex: 1;">
                    <div style="color: white; font-weight: 500;">{activity}</div>
                    <div style="color: #6b7280;">{time_ago}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Configuración rápida
        st.markdown("### ⚡ Acceso Rápido")
        
        # Botones de acción rápida
        if st.button("🎨 Cambiar Tema", use_container_width=True):
            st.info("🎨 Accede a Configuración → Temas")
        
        if st.button("📊 Reporte Rápido", use_container_width=True):
            with st.spinner("Generando reporte..."):
                time.sleep(1)
            st.success("📈 ¡Reporte generado!")
        
        if st.button("🔄 Refrescar Datos", use_container_width=True):
            st.cache_data.clear()
            st.success("🔄 ¡Datos actualizados!")
            st.rerun()
        
        st.markdown("---")
        
        # Estado del sistema mini
        st.markdown("### 📡 Estado Sistema")
        
        # Indicadores de estado
        system_status = [
            ("🟢", "API", "OK"),
            ("🟢", "MongoDB", "OK"),
            ("🟡", "Storage", "85%"),
            ("🟢", "Spark", "OK")
        ]
        
        for status_color, component, status in system_status:
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.25rem 0;
                font-size: 0.8rem;
            ">
                <span>{status_color}</span>
                <span style="color: #b8bcc8;">{component}:</span>
                <span style="color: white; font-weight: 500;">{status}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Botón de logout
        if st.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
            logout()
    
    return page

def render_mini_stats():
    """Renderiza estadísticas mini para el sidebar"""
    
    # Generar datos aleatorios para demo
    stats = {
        "online_users": np.random.randint(45, 85),
        "active_sessions": np.random.randint(12, 28),
        "system_load": np.random.uniform(15, 45),
        "memory_usage": np.random.uniform(60, 85)
    }
    
    return stats

def get_navigation_history():
    """Obtiene el historial de navegación del usuario"""
    if 'nav_history' not in st.session_state:
        st.session_state.nav_history = []
    
    return st.session_state.nav_history

def add_to_navigation_history(page: str):
    """Agrega una página al historial de navegación"""
    if 'nav_history' not in st.session_state:
        st.session_state.nav_history = []
    
    # Evitar duplicados consecutivos
    if not st.session_state.nav_history or st.session_state.nav_history[-1] != page:
        st.session_state.nav_history.append(page)
        
        # Mantener solo los últimos 10 elementos
        if len(st.session_state.nav_history) > 10:
            st.session_state.nav_history = st.session_state.nav_history[-10:]

__all__ = [
    'render_sidebar',
    'render_mini_stats',
    'get_navigation_history',
    'add_to_navigation_history'
]