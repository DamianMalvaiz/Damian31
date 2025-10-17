# ui/pages/dashboard.py
# Dashboard principal con métricas y resumen
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render():
    """Renderiza la página del dashboard principal"""
    
    # Header de la página
    st.markdown("""
    <div class="animate-fadeInDown">
        <h2 style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        ">
            🏠 Dashboard de Control Central
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Generar datos demo
    customers_count = np.random.randint(1200, 1500)
    videos_count = np.random.randint(450, 550)
    images_count = np.random.randint(800, 1200)
    audio_count = np.random.randint(200, 350)
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="card animate-zoomIn delay-100" style="text-align: center;">
            <div style="
                font-size: 3rem; 
                font-weight: 900;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">
                {customers_count:,}
            </div>
            <div style="color: #b8bcc8; text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem;">
                👥 USUARIOS TOTALES
            </div>
            <div style="color: #22c55e; font-size: 0.8rem; margin-top: 0.5rem;">
                ↗️ +12.5% este mes
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card animate-zoomIn delay-200" style="text-align: center;">
            <div style="
                font-size: 3rem; 
                font-weight: 900;
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">
                {videos_count:,}
            </div>
            <div style="color: #b8bcc8; text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem;">
                🎥 VIDEOS ÉPICOS
            </div>
            <div style="color: #22c55e; font-size: 0.8rem; margin-top: 0.5rem;">
                ↗️ +8.3% este mes
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card animate-zoomIn delay-300" style="text-align: center;">
            <div style="
                font-size: 3rem; 
                font-weight: 900;
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">
                {images_count:,}
            </div>
            <div style="color: #b8bcc8; text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem;">
                🖼️ IMÁGENES BRUTALES
            </div>
            <div style="color: #22c55e; font-size: 0.8rem; margin-top: 0.5rem;">
                ↗️ +15.7% este mes
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="card animate-zoomIn delay-500" style="text-align: center;">
            <div style="
                font-size: 3rem; 
                font-weight: 900;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">
                {audio_count:,}
            </div>
            <div style="color: #b8bcc8; text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem;">
                🎵 TRACKS SALVAJES
            </div>
            <div style="color: #22c55e; font-size: 0.8rem; margin-top: 0.5rem;">
                ↗️ +22.1% este mes
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Crecimiento de Usuarios (Últimos 30 días)")
        
        # Generar datos de crecimiento
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        growth_data = pd.DataFrame({
            'Fecha': dates,
            'Nuevos Usuarios': np.random.poisson(15, 30),
            'Usuarios Activos': np.random.poisson(85, 30)
        })
        growth_data['Usuarios Acumulados'] = growth_data['Nuevos Usuarios'].cumsum()
        
        fig = px.line(growth_data, x='Fecha', y=['Nuevos Usuarios', 'Usuarios Activos'],
                     title="", color_discrete_sequence=['#00d4ff', '#b967db'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Distribución de Contenido")
        
        # Datos de distribución
        content_data = pd.DataFrame({
            'Tipo': ['Videos', 'Imágenes', 'Audio', 'Documentos'],
            'Cantidad': [videos_count, images_count, audio_count, 125],
            'Porcentaje': [35, 42, 18, 5]
        })
        
        fig = px.pie(content_data, values='Cantidad', names='Tipo',
                    color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1', '#feca57'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Métricas de rendimiento
    st.markdown("### ⚡ Métricas de Rendimiento en Tiempo Real")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("🔥 Views/min", f"{np.random.randint(450, 650):,}", "↗️ +5.2%"),
        ("⬇️ Downloads/hr", f"{np.random.randint(120, 180):,}", "↗️ +12.8%"),
        ("💾 Storage Used", f"{np.random.uniform(1.2, 1.8):.1f}TB", "↗️ +3.1%"),
        ("🚀 Response Time", f"{np.random.randint(45, 85)}ms", "↘️ -8.5%"),
        ("🔄 Uptime", "99.97%", "🟢 Estable")
    ]
    
    for i, (col, (label, value, delta)) in enumerate(zip([col1, col2, col3, col4, col5], metrics)):
        with col:
            st.metric(label, value, delta=delta)
    
    # Actividad reciente
    st.markdown("### 🔥 Actividad Reciente")
    
    activities = [
        ("🎥", "Nuevo video subido", "'Tutorial Épico de Python'", "hace 2 min"),
        ("👥", "Usuario registrado", "'CodingMaster' se unió", "hace 5 min"),
        ("🖼️", "Imagen optimizada", "'Landscape_Brutal.jpg'", "hace 8 min"),
        ("🎵", "Track añadido", "'Synthwave Dreams'", "hace 12 min"),
        ("📊", "Reporte generado", "Analytics mensual", "hace 15 min"),
        ("🔧", "Sistema actualizado", "v2.0.1 desplegado", "hace 1 hora")
    ]
    
    for i, (icon, action, detail, time) in enumerate(activities):
        st.markdown(f"""
        <div class="animate-fadeInLeft delay-{i*100}" style="
            background: rgba(255, 255, 255, 0.05);
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 0.5rem;
            border-left: 4px solid #00d4ff;
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div>
                    <div style="font-weight: 600; color: white;">{action}</div>
                    <div style="color: #b8bcc8; font-size: 0.9rem;">{detail}</div>
                </div>
            </div>
            <div style="color: #6b7280; font-size: 0.8rem;">{time}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de heatmap de actividad
    st.markdown("### 🔥 Mapa de Calor - Actividad por Hora")
    
    # Generar datos de heatmap
    hours = list(range(24))
    days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    
    # Crear matriz de actividad
    activity_matrix = []
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
        activity_matrix.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=activity_matrix,
        x=hours,
        y=days,
        colorscale='Viridis',
        hoveronclick=False
    ))
    
    fig.update_layout(
        title="Actividad de usuarios por día y hora",
        xaxis_title="Hora del día",
        yaxis_title="Día de la semana",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Estado del sistema
    st.markdown("### 📡 Estado del Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    system_status = [
        ("API", "✅", "Operativo", "#22c55e"),
        ("Base de Datos", "✅", "Conectada", "#22c55e"),
        ("Almacenamiento", "⚠️", f"{np.random.randint(82, 88)}% Usado", "#fb923c"),
        ("Rendimiento", "✅", "Excelente", "#22c55e")
    ]
    
    for col, (component, status, detail, color) in zip([col1, col2, col3, col4], system_status):
        with col:
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid {color};
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
            ">
                <div style="color: {color}; font-size: 2rem;">{status}</div>
                <div style="color: {color}; font-weight: bold;">{component}</div>
                <div style="color: #b8bcc8; font-size: 0.8rem;">{detail}</div>
            </div>
            """, unsafe_allow_html=True)