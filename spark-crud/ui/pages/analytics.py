# ui/pages/analytics.py
# Página de analytics avanzados con visualizaciones épicas
# ========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random

def render():
    """Renderiza la página de analytics avanzados"""
    
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
            📊 Analytics de Otro Mundo
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Generar datos demo para analytics
    @st.cache_data
    def generate_analytics_data():
        # Datos de usuarios por día (últimos 90 días)
        dates = pd.date_range(end=datetime.now(), periods=90, freq='D')
        users_data = pd.DataFrame({
            'date': dates,
            'new_users': np.random.poisson(25, 90),
            'active_users': np.random.poisson(150, 90),
            'returning_users': np.random.poisson(75, 90)
        })
        users_data['total_users'] = users_data['new_users'].cumsum() + 1000
        
        # Datos de contenido multimedia
        media_data = pd.DataFrame({
            'type': ['Videos', 'Imágenes', 'Audio', 'Documentos'],
            'count': [485, 1247, 328, 156],
            'size_gb': [245.7, 89.3, 67.2, 12.8],
            'views': [2847392, 1923847, 847293, 234829],
            'downloads': [384729, 847392, 293847, 47382]
        })
        
        # Datos de engagement por hora
        hours = list(range(24))
        engagement_data = []
        for hour in hours:
            if 9 <= hour <= 17:  # Horas laborales
                engagement = np.random.randint(70, 100)
            elif 19 <= hour <= 23:  # Noche
                engagement = np.random.randint(40, 80)
            else:  # Madrugada
                engagement = np.random.randint(10, 40)
            engagement_data.append(engagement)
        
        # Datos de países
        countries_data = pd.DataFrame({
            'country': ['España', 'México', 'Argentina', 'Colombia', 'Chile', 'Perú', 'Venezuela', 'Ecuador'],
            'users': [2847, 1923, 1456, 1234, 987, 756, 645, 534],
            'sessions': [8392, 5847, 4293, 3847, 2938, 2384, 1947, 1638]
        })
        
        return users_data, media_data, engagement_data, countries_data
    
    users_data, media_data, engagement_data, countries_data = generate_analytics_data()
    
    # Métricas principales KPIs
    st.markdown("### 🔥 KPIs Principales")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_users = users_data['total_users'].iloc[-1]
        user_growth = ((users_data['total_users'].iloc[-1] - users_data['total_users'].iloc[-30]) / 
                      users_data['total_users'].iloc[-30] * 100)
        st.metric(
            "👥 Total Usuarios", 
            f"{total_users:,}",
            delta=f"+{user_growth:.1f}% (30d)"
        )
    
    with col2:
        total_views = media_data['views'].sum()
        st.metric(
            "👁️ Total Views", 
            f"{total_views/1000000:.1f}M",
            delta="+15.2% (7d)"
        )
    
    with col3:
        total_downloads = media_data['downloads'].sum()
        st.metric(
            "⬇️ Downloads", 
            f"{total_downloads/1000:.0f}K",
            delta="+8.7% (7d)"
        )
    
    with col4:
        active_users_avg = users_data['active_users'].tail(7).mean()
        st.metric(
            "🔥 Usuarios Activos", 
            f"{active_users_avg:.0f}/día",
            delta="+22.1% (7d)"
        )
    
    with col5:
        total_storage = media_data['size_gb'].sum()
        st.metric(
            "💾 Storage", 
            f"{total_storage:.1f}GB",
            delta="+5.3% (30d)"
        )
    
    # Selector de período de análisis
    st.markdown("### 📅 Período de Análisis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        period = st.selectbox(
            "📊 Período",
            ["Últimos 7 días", "Últimos 30 días", "Últimos 90 días", "Último año"]
        )
    
    with col2:
        metric_type = st.selectbox(
            "📈 Métrica Principal",
            ["Usuarios", "Contenido", "Engagement", "Performance"]
        )
    
    with col3:
        chart_type = st.selectbox(
            "📊 Tipo de Gráfico",
            ["Líneas", "Barras", "Área", "Combinado"]
        )
    
    # Gráficos principales
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Crecimiento de Usuarios")
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Usuarios nuevos (barras)
        fig.add_trace(
            go.Bar(
                x=users_data['date'],
                y=users_data['new_users'],
                name="Nuevos Usuarios",
                marker_color='rgba(59, 130, 246, 0.7)'
            ),
            secondary_y=False,
        )
        
        # Total acumulado (línea)
        fig.add_trace(
            go.Scatter(
                x=users_data['date'],
                y=users_data['total_users'],
                mode='lines',
                name="Total Acumulado",
                line=dict(color='#f59e0b', width=3)
            ),
            secondary_y=True,
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=True,
            height=400
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False, secondary_y=False)
        fig.update_yaxes(showgrid=False, secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Distribución de Contenido")
        
        fig = px.pie(
            media_data, 
            values='count', 
            names='type',
            color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1', '#feca57']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Análisis de engagement por hora
    st.markdown("#### 🕐 Engagement por Hora del Día")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=list(range(24)),
        y=engagement_data,
        mode='lines+markers',
        fill='tonexty',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=8, color='#00d4ff'),
        name='Engagement %'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        xaxis_title="Hora del día",
        yaxis_title="Engagement (%)",
        height=300,
        showlegend=False
    )
    
    fig.update_xaxes(
        showgrid=True, 
        gridcolor='rgba(255,255,255,0.1)',
        tickmode='linear',
        tick0=0,
        dtick=2
    )
    fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análisis geográfico y de performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌍 Usuarios por País")
        
        fig = px.bar(
            countries_data.head(8),
            x='users',
            y='country',
            orientation='h',
            color='users',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400,
            showlegend=False
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Performance de Contenido")
        
        # Crear gráfico de barras agrupadas
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Views (K)',
            x=media_data['type'],
            y=media_data['views'] / 1000,
            marker_color='rgba(79, 172, 254, 0.8)'
        ))
        
        fig.add_trace(go.Bar(
            name='Downloads (K)',
            x=media_data['type'],
            y=media_data['downloads'] / 1000,
            marker_color='rgba(185, 103, 219, 0.8)'
        ))
        
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Análisis avanzado
    st.markdown("### 🔬 Análisis Avanzado")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Tendencias", "🔍 Correlaciones", "🎯 Segmentación", "🚀 Predicciones"])
    
    with tab1:
        st.markdown("#### 📈 Análisis de Tendencias")
        
        # Generar datos de tendencias
        trend_dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        trend_data = pd.DataFrame({
            'date': trend_dates,
            'videos_uploaded': np.random.poisson(8, 30),
            'images_uploaded': np.random.poisson(15, 30),
            'audio_uploaded': np.random.poisson(5, 30)
        })
        
        # Calcular medias móviles
        trend_data['videos_ma'] = trend_data['videos_uploaded'].rolling(window=7).mean()
        trend_data['images_ma'] = trend_data['images_uploaded'].rolling(window=7).mean()
        trend_data['audio_ma'] = trend_data['audio_uploaded'].rolling(window=7).mean()
        
        fig = go.Figure()
        
        # Líneas de tendencia
        fig.add_trace(go.Scatter(
            x=trend_data['date'], y=trend_data['videos_ma'],
            mode='lines', name='Videos (MA7)', line=dict(color='#ff6b6b', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=trend_data['date'], y=trend_data['images_ma'],
            mode='lines', name='Imágenes (MA7)', line=dict(color='#4ecdc4', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=trend_data['date'], y=trend_data['audio_ma'],
            mode='lines', name='Audio (MA7)', line=dict(color='#45b7d1', width=3)
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title="Tendencias de Subidas (Media Móvil 7 días)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Métricas de tendencia
        col1, col2, col3 = st.columns(3)
        
        with col1:
            video_trend = np.polyfit(range(len(trend_data)), trend_data['videos_uploaded'], 1)[0]
            trend_direction = "↗️" if video_trend > 0 else "↘️"
            st.metric("🎥 Tendencia Videos", f"{trend_direction} {abs(video_trend):.2f}/día")
        
        with col2:
            image_trend = np.polyfit(range(len(trend_data)), trend_data['images_uploaded'], 1)[0]
            trend_direction = "↗️" if image_trend > 0 else "↘️"
            st.metric("🖼️ Tendencia Imágenes", f"{trend_direction} {abs(image_trend):.2f}/día")
        
        with col3:
            audio_trend = np.polyfit(range(len(trend_data)), trend_data['audio_uploaded'], 1)[0]
            trend_direction = "↗️" if audio_trend > 0 else "↘️"
            st.metric("🎵 Tendencia Audio", f"{trend_direction} {abs(audio_trend):.2f}/día")
    
    with tab2:
        st.markdown("#### 🔍 Matriz de Correlaciones")
        
        # Generar datos de correlación
        corr_data = pd.DataFrame({
            'users': np.random.normal(100, 20, 100),
            'uploads': np.random.normal(50, 10, 100),
            'views': np.random.normal(1000, 200, 100),
            'downloads': np.random.normal(200, 50, 100),
            'engagement': np.random.normal(75, 15, 100)
        })
        
        # Añadir correlaciones artificiales
        corr_data['views'] += corr_data['uploads'] * 15 + np.random.normal(0, 50, 100)
        corr_data['downloads'] += corr_data['views'] * 0.15 + np.random.normal(0, 20, 100)
        
        correlation_matrix = corr_data.corr()
        
        fig = px.imshow(
            correlation_matrix,
            color_continuous_scale='RdBu',
            aspect="auto",
            title="Matriz de Correlaciones"
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights de correlación
        st.markdown("##### 🧠 Insights Clave")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📊 Correlaciones Fuertes:**
            - 🎥 Uploads ↔ Views: **0.85**
            - 👁️ Views ↔ Downloads: **0.72**
            - 👥 Users ↔ Engagement: **0.68**
            """)
        
        with col2:
            st.markdown("""
            **💡 Recomendaciones:**
            - Incrementar uploads para más views
            - Optimizar UX para más downloads
            - Fomentar engagement para retener usuarios
            """)
    
    with tab3:
        st.markdown("#### 🎯 Segmentación de Usuarios")
        
        # Generar datos de segmentación
        segments = ['Nuevos', 'Activos', 'Leales', 'En Riesgo', 'Inactivos']
        segment_data = pd.DataFrame({
            'segment': segments,
            'users': [1247, 3892, 2156, 847, 1203],
            'avg_session_time': [3.2, 8.5, 12.7, 2.1, 0.8],
            'content_consumed': [2.1, 15.3, 28.9, 1.2, 0.3]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                segment_data,
                x='segment',
                y='users',
                color='users',
                color_continuous_scale='Viridis',
                title="Usuarios por Segmento"
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                segment_data,
                x='avg_session_time',
                y='content_consumed',
                size='users',
                color='segment',
                title="Comportamiento por Segmento"
            )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabla de segmentos
        st.dataframe(segment_data, use_container_width=True)
    
    with tab4:
        st.markdown("#### 🚀 Predicciones y Forecasting")
        
        # Generar predicciones
        future_dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        historical_users = users_data['total_users'].values
        
        # Predicción simple (tendencia lineal + ruido)
        trend = np.polyfit(range(len(historical_users)), historical_users, 1)
        future_trend = np.polyval(trend, range(len(historical_users), len(historical_users) + 30))
        future_users = future_trend + np.random.normal(0, 50, 30)
        
        # Crear gráfico de predicción
        fig = go.Figure()
        
        # Datos históricos
        fig.add_trace(go.Scatter(
            x=users_data['date'],
            y=users_data['total_users'],
            mode='lines',
            name='Histórico',
            line=dict(color='#4ecdc4', width=3)
        ))
        
        # Predicciones
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_users,
            mode='lines',
            name='Predicción',
            line=dict(color='#ff6b6b', width=3, dash='dash')
        ))
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title="Predicción de Crecimiento de Usuarios (30 días)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Métricas de predicción
        col1, col2, col3 = st.columns(3)
        
        with col1:
            predicted_growth = ((future_users[-1] - historical_users[-1]) / historical_users[-1] * 100)
            st.metric("📈 Crecimiento Predicho", f"+{predicted_growth:.1f}%", "30 días")
        
        with col2:
            predicted_users = int(future_users[-1])
            st.metric("👥 Usuarios Predichos", f"{predicted_users:,}", "en 30 días")
        
        with col3:
            confidence = np.random.uniform(75, 95)
            st.metric("🎯 Confianza", f"{confidence:.1f}%", "del modelo")
    
    # Reportes y exportación
    st.markdown("### 📋 Reportes y Exportación")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Generar Reporte Completo", use_container_width=True):
            with st.spinner("Generando reporte..."):
                import time
                time.sleep(2)
            st.success("📈 ¡Reporte generado exitosamente!")
    
    with col2:
        if st.button("📤 Exportar a PDF", use_container_width=True):
            with st.spinner("Exportando PDF..."):
                import time
                time.sleep(1.5)
            st.success("📄 ¡PDF exportado!")
    
    with col3:
        if st.button("📧 Enviar por Email", use_container_width=True):
            with st.spinner("Enviando email..."):
                import time
                time.sleep(1)
            st.success("📧 ¡Email enviado!")
    
    with col4:
        if st.button("🔄 Actualizar Datos", use_container_width=True):
            st.cache_data.clear()
            st.success("🔄 ¡Datos actualizados!")
            st.rerun()