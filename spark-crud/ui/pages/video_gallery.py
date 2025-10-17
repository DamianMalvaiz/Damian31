# ui/pages/video_gallery.py
# Galería de videos con reproductor integrado
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def render():
    """Renderiza la página de galería de videos"""
    
    # Header de la página
    st.markdown("""
    <div class="animate-fadeInDown">
        <h2 style="
            background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        ">
            🎥 Centro de Videos Épico
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Generar datos demo de videos
    @st.cache_data
    def generate_videos_data():
        video_titles = [
            "Tutorial Python Avanzado", "Introducción a Machine Learning", "React para Principiantes",
            "Docker y Kubernetes", "Bases de Datos NoSQL", "Desarrollo Full Stack",
            "Inteligencia Artificial", "Blockchain Explicado", "Cybersecurity Básico",
            "DevOps Fundamentals", "Cloud Computing AWS", "Data Science con Python",
            "Mobile Development", "UI/UX Design Principles", "Microservicios Architecture",
            "GraphQL vs REST", "Testing Automatizado", "Git y GitHub Avanzado",
            "Algoritmos y Estructuras", "Programación Funcional"
        ]
        
        categories = ["Programación", "Data Science", "DevOps", "Design", "Seguridad"]
        
        data = []
        for i in range(50):
            duration = np.random.uniform(300, 3600)  # 5 min a 1 hora
            views = np.random.randint(100, 100000)
            likes = int(views * np.random.uniform(0.02, 0.15))
            
            data.append({
                'id': i + 1,
                'title': f"{random.choice(video_titles)} #{i+1}",
                'category': random.choice(categories),
                'duration': duration,
                'duration_formatted': f"{int(duration//60):02d}:{int(duration%60):02d}",
                'views': views,
                'likes': likes,
                'upload_date': datetime.now() - timedelta(days=np.random.randint(1, 365)),
                'resolution': random.choice(['720p', '1080p', '4K']),
                'size_mb': np.random.uniform(50, 500),
                'status': random.choice(['ready', 'processing', 'pending'], p=[0.85, 0.10, 0.05])
            })
        
        return pd.DataFrame(data)
    
    videos_df = generate_videos_data()
    
    # Filtros de videos
    st.markdown("### 🎛️ Filtros y Controles")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_title = st.text_input("🔍 Buscar video", placeholder="Título del video...")
    
    with col2:
        category_filter = st.selectbox("📂 Categoría", ["Todas"] + sorted(videos_df['category'].unique()))
    
    with col3:
        resolution_filter = st.selectbox("🖥️ Resolución", ["Todas"] + sorted(videos_df['resolution'].unique()))
    
    with col4:
        sort_by = st.selectbox("🔄 Ordenar por", ["Más recientes", "Más vistos", "Más gustados", "Duración"])
    
    # Aplicar filtros
    filtered_df = videos_df.copy()
    
    if search_title:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False, na=False)]
    
    if category_filter != "Todas":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    if resolution_filter != "Todas":
        filtered_df = filtered_df[filtered_df['resolution'] == resolution_filter]
    
    # Aplicar ordenamiento
    if sort_by == "Más recientes":
        filtered_df = filtered_df.sort_values('upload_date', ascending=False)
    elif sort_by == "Más vistos":
        filtered_df = filtered_df.sort_values('views', ascending=False)
    elif sort_by == "Más gustados":
        filtered_df = filtered_df.sort_values('likes', ascending=False)
    elif sort_by == "Duración":
        filtered_df = filtered_df.sort_values('duration', ascending=False)
    
    # Estadísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎥 Total Videos", len(filtered_df), delta=f"de {len(videos_df)}")
    
    with col2:
        total_views = filtered_df['views'].sum()
        st.metric("👁️ Total Views", f"{total_views:,}")
    
    with col3:
        total_duration = filtered_df['duration'].sum() / 3600  # en horas
        st.metric("⏱️ Duración Total", f"{total_duration:.1f}h")
    
    with col4:
        avg_size = filtered_df['size_mb'].mean()
        st.metric("💾 Tamaño Promedio", f"{avg_size:.0f}MB")
    
    # Reproductor principal
    st.markdown("### 🎬 Reproductor Principal")
    
    if len(filtered_df) > 0:
        # Seleccionar video destacado (el primero de la lista filtrada)
        featured_video = filtered_df.iloc[0]
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Simular reproductor de video
            video_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#feca57', '#ff9ff3', '#54a0ff']
            video_color = random.choice(video_colors)
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(45deg, {video_color}, {random.choice(video_colors)});
                aspect-ratio: 16/9;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                margin-bottom: 1rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            ">
                <div style="
                    width: 80px;
                    height: 80px;
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 2rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                " onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                    ▶️
                </div>
                <div style="
                    position: absolute;
                    bottom: 16px;
                    right: 16px;
                    background: rgba(0, 0, 0, 0.8);
                    color: white;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-weight: bold;
                ">
                    {featured_video['duration_formatted']}
                </div>
                <div style="
                    position: absolute;
                    top: 16px;
                    left: 16px;
                    background: rgba(0, 0, 0, 0.8);
                    color: white;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 0.8rem;
                ">
                    {featured_video['resolution']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Controles del reproductor
            col_a, col_b, col_c, col_d, col_e = st.columns(5)
            
            with col_a:
                if st.button("⏮️", help="Anterior"):
                    st.info("⏮️ Video anterior")
            
            with col_b:
                if st.button("▶️", help="Reproducir"):
                    st.success("🎬 Reproduciendo...")
            
            with col_c:
                if st.button("⏸️", help="Pausar"):
                    st.warning("⏸️ Pausado")
            
            with col_d:
                if st.button("⏹️", help="Detener"):
                    st.error("⏹️ Detenido")
            
            with col_e:
                if st.button("⏭️", help="Siguiente"):
                    st.info("⏭️ Siguiente video")
            
            # Barra de progreso
            progress = st.slider("", 0, 100, 25, label_visibility="collapsed")
            
            col_time1, col_time2 = st.columns([1, 1])
            with col_time1:
                current_time = int(featured_video['duration'] * progress / 100)
                st.markdown(f"**{current_time//60:02d}:{current_time%60:02d}**")
            with col_time2:
                st.markdown(f"<div style='text-align: right'><strong>{featured_video['duration_formatted']}</strong></div>", 
                           unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📋 Info del Video")
            st.markdown(f"**🎬 {featured_video['title']}**")
            st.markdown(f"📂 {featured_video['category']}")
            st.markdown(f"📅 {featured_video['upload_date'].strftime('%d/%m/%Y')}")
            
            st.markdown("#### 📊 Estadísticas")
            st.metric("👁️ Views", f"{featured_video['views']:,}")
            st.metric("❤️ Likes", f"{featured_video['likes']:,}")
            st.metric("💾 Tamaño", f"{featured_video['size_mb']:.0f}MB")
            
            # Botones de acción
            if st.button("❤️ Me Gusta", use_container_width=True):
                st.success("💖 ¡Agregado a favoritos!")
            
            if st.button("⬇️ Descargar", use_container_width=True):
                st.success("📥 ¡Descarga iniciada!")
            
            if st.button("📤 Compartir", use_container_width=True):
                st.info("🔗 Enlace copiado al portapapeles")
    
    # Grid de videos
    st.markdown("### 🎯 Galería de Videos")
    
    if len(filtered_df) > 0:
        # Mostrar videos en grid de 3 columnas
        videos_per_row = 3
        videos_to_show = filtered_df.head(12)  # Mostrar máximo 12 videos
        
        for i in range(0, len(videos_to_show), videos_per_row):
            cols = st.columns(videos_per_row)
            
            for j in range(videos_per_row):
                if i + j < len(videos_to_show):
                    video = videos_to_show.iloc[i + j]
                    
                    with cols[j]:
                        # Color aleatorio para cada thumbnail
                        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3']
                        thumbnail_color = random.choice(colors)
                        
                        # Status badge color
                        status_colors = {
                            'ready': '#22c55e',
                            'processing': '#f59e0b', 
                            'pending': '#6b7280'
                        }
                        
                        st.markdown(f"""
                        <div class="card animate-fadeInUp delay-{(i+j)*100}" style="
                            text-align: center;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            margin-bottom: 1rem;
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
                                    width: 50px;
                                    height: 50px;
                                    background: rgba(255, 255, 255, 0.9);
                                    border-radius: 50%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    font-size: 1.2rem;
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
                                    font-size: 0.7rem;
                                ">
                                    {video['duration_formatted']}
                                </div>
                                <div style="
                                    position: absolute;
                                    top: 8px;
                                    left: 8px;
                                    background: {status_colors[video['status']]};
                                    color: white;
                                    padding: 2px 6px;
                                    border-radius: 4px;
                                    font-size: 0.6rem;
                                    text-transform: uppercase;
                                ">
                                    {video['status']}
                                </div>
                            </div>
                            <h4 style="
                                margin-bottom: 0.5rem; 
                                font-size: 0.9rem;
                                height: 2.4rem;
                                overflow: hidden;
                                display: -webkit-box;
                                -webkit-line-clamp: 2;
                                -webkit-box-orient: vertical;
                            ">{video['title']}</h4>
                            <div style="
                                display: flex; 
                                justify-content: space-between; 
                                font-size: 0.8rem; 
                                color: #b8bcc8;
                                margin-bottom: 0.5rem;
                            ">
                                <span>👁️ {video['views']:,}</span>
                                <span>❤️ {video['likes']:,}</span>
                            </div>
                            <div style="
                                font-size: 0.7rem; 
                                color: #6b7280;
                            ">
                                📂 {video['category']} • {video['resolution']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Paginación
        if len(filtered_df) > 12:
            st.markdown("### 📄 Más Videos")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📥 Cargar Más Videos", use_container_width=True):
                    st.info("🔄 Cargando más videos...")
    
    else:
        st.info("🔍 No se encontraron videos con los filtros aplicados")
    
    # Subir nuevo video
    with st.expander("📤 Subir Nuevo Video", expanded=False):
        st.markdown("### 🎬 Subir Video")
        
        uploaded_file = st.file_uploader(
            "Selecciona un archivo de video",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Formatos soportados: MP4, AVI, MOV, MKV (máx. 500MB)"
        )
        
        if uploaded_file:
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("🎬 Título del video", value=uploaded_file.name.split('.')[0])
                category = st.selectbox("📂 Categoría", ["Programación", "Data Science", "DevOps", "Design", "Seguridad"])
                description = st.text_area("📝 Descripción", placeholder="Describe tu video...")
            
            with col2:
                tags = st.text_input("🏷️ Tags", placeholder="python, tutorial, beginner")
                visibility = st.selectbox("👁️ Visibilidad", ["Público", "Privado", "No listado"])
                generate_thumbnail = st.checkbox("🖼️ Generar miniatura automática", value=True)
            
            if st.button("🚀 Subir Video", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text("📤 Subiendo archivo...")
                    elif i < 60:
                        status_text.text("🎬 Procesando video...")
                    elif i < 90:
                        status_text.text("🖼️ Generando miniatura...")
                    else:
                        status_text.text("✅ Finalizando...")
                    
                    # Simular tiempo de procesamiento
                    import time
                    time.sleep(0.05)
                
                st.success(f"🎉 ¡Video '{title}' subido exitosamente!")
                st.balloons()