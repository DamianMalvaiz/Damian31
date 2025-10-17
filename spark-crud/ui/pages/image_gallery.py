# ui/pages/image_gallery.py
# Galería de imágenes con lightbox y filtros avanzados
# ===================================================

import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def render():
    """Renderiza la página de galería de imágenes"""
    
    # Header de la página
    st.markdown("""
    <div class="animate-fadeInDown">
        <h2 style="
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        ">
            🖼️ Galería de Imágenes Brutal
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Generar datos demo de imágenes
    @st.cache_data
    def generate_images_data():
        image_titles = [
            "Paisaje Montañoso", "Ciudad Nocturna", "Abstracto Colorido", "Retrato Artístico",
            "Naturaleza Salvaje", "Arquitectura Moderna", "Arte Digital", "Fotografía Macro",
            "Cielo Estrellado", "Océano Tranquilo", "Bosque Místico", "Atardecer Épico",
            "Textura Industrial", "Minimalismo Zen", "Explosión de Color", "Geometría Sagrada",
            "Vida Urbana", "Serenidad Natural", "Caos Organizado", "Belleza Simétrica"
        ]
        
        categories = ["Paisajes", "Retratos", "Abstracto", "Arquitectura", "Naturaleza", "Arte Digital"]
        formats = ["JPEG", "PNG", "WebP", "TIFF"]
        
        data = []
        for i in range(80):
            width = random.choice([1920, 2560, 3840, 4096])
            height = random.choice([1080, 1440, 2160, 2304])
            size_mb = np.random.uniform(0.5, 15)
            
            data.append({
                'id': i + 1,
                'title': f"{random.choice(image_titles)} #{i+1}",
                'category': random.choice(categories),
                'width': width,
                'height': height,
                'resolution': f"{width}x{height}",
                'megapixels': round((width * height) / 1_000_000, 1),
                'format': random.choice(formats),
                'size_mb': size_mb,
                'upload_date': datetime.now() - timedelta(days=np.random.randint(1, 365)),
                'downloads': np.random.randint(10, 5000),
                'likes': np.random.randint(5, 1000),
                'views': np.random.randint(50, 10000),
                'photographer': f"Fotógrafo {np.random.randint(1, 20)}",
                'tags': random.sample(['naturaleza', 'arte', 'color', 'luz', 'sombra', 'textura', 'forma'], 
                                    k=random.randint(2, 4))
            })
        
        return pd.DataFrame(data)
    
    images_df = generate_images_data()
    
    # Filtros de imágenes
    st.markdown("### 🎛️ Filtros Avanzados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_title = st.text_input("🔍 Buscar imagen", placeholder="Título de la imagen...")
    
    with col2:
        category_filter = st.selectbox("📂 Categoría", ["Todas"] + sorted(images_df['category'].unique()))
    
    with col3:
        format_filter = st.selectbox("📄 Formato", ["Todos"] + sorted(images_df['format'].unique()))
    
    with col4:
        size_filter = st.selectbox("📏 Tamaño", [
            "Todos", "Pequeñas (<2MB)", "Medianas (2-10MB)", "Grandes (>10MB)"
        ])
    
    # Filtros adicionales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_resolution = st.selectbox("🖥️ Resolución mínima", [
            "Cualquiera", "HD (1280x720)", "Full HD (1920x1080)", "4K (3840x2160)"
        ])
    
    with col2:
        sort_by = st.selectbox("🔄 Ordenar por", [
            "Más recientes", "Más descargadas", "Más gustadas", "Más vistas", "Tamaño"
        ])
    
    with col3:
        view_mode = st.selectbox("👁️ Modo de vista", ["Grid", "Lista", "Mosaico"])
    
    # Aplicar filtros
    filtered_df = images_df.copy()
    
    if search_title:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False, na=False)]
    
    if category_filter != "Todas":
        filtered_df = filtered_df[filtered_df['category'] == category_filter]
    
    if format_filter != "Todos":
        filtered_df = filtered_df[filtered_df['format'] == format_filter]
    
    if size_filter != "Todos":
        if size_filter == "Pequeñas (<2MB)":
            filtered_df = filtered_df[filtered_df['size_mb'] < 2]
        elif size_filter == "Medianas (2-10MB)":
            filtered_df = filtered_df[(filtered_df['size_mb'] >= 2) & (filtered_df['size_mb'] <= 10)]
        elif size_filter == "Grandes (>10MB)":
            filtered_df = filtered_df[filtered_df['size_mb'] > 10]
    
    if min_resolution != "Cualquiera":
        if min_resolution == "HD (1280x720)":
            filtered_df = filtered_df[(filtered_df['width'] >= 1280) & (filtered_df['height'] >= 720)]
        elif min_resolution == "Full HD (1920x1080)":
            filtered_df = filtered_df[(filtered_df['width'] >= 1920) & (filtered_df['height'] >= 1080)]
        elif min_resolution == "4K (3840x2160)":
            filtered_df = filtered_df[(filtered_df['width'] >= 3840) & (filtered_df['height'] >= 2160)]
    
    # Aplicar ordenamiento
    if sort_by == "Más recientes":
        filtered_df = filtered_df.sort_values('upload_date', ascending=False)
    elif sort_by == "Más descargadas":
        filtered_df = filtered_df.sort_values('downloads', ascending=False)
    elif sort_by == "Más gustadas":
        filtered_df = filtered_df.sort_values('likes', ascending=False)
    elif sort_by == "Más vistas":
        filtered_df = filtered_df.sort_values('views', ascending=False)
    elif sort_by == "Tamaño":
        filtered_df = filtered_df.sort_values('size_mb', ascending=False)
    
    # Estadísticas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🖼️ Total Imágenes", len(filtered_df), delta=f"de {len(images_df)}")
    
    with col2:
        total_downloads = filtered_df['downloads'].sum()
        st.metric("⬇️ Total Descargas", f"{total_downloads:,}")
    
    with col3:
        avg_size = filtered_df['size_mb'].mean() if len(filtered_df) > 0 else 0
        st.metric("💾 Tamaño Promedio", f"{avg_size:.1f}MB")
    
    with col4:
        total_size = filtered_df['size_mb'].sum()
        st.metric("📊 Tamaño Total", f"{total_size:.1f}MB")
    
    # Lightbox para imagen seleccionada
    if 'selected_image' not in st.session_state:
        st.session_state.selected_image = None
    
    if st.session_state.selected_image:
        selected_img = filtered_df[filtered_df['id'] == st.session_state.selected_image].iloc[0]
        
        st.markdown("### 🔍 Vista Detallada")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Simular imagen grande
            img_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3', '#54a0ff']
            img_color = random.choice(img_colors)
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(45deg, {img_color}, {random.choice(img_colors)});
                aspect-ratio: 16/10;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 6rem;
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.2);
                margin-bottom: 1rem;
                position: relative;
            ">
                🖼️
                <div style="
                    position: absolute;
                    top: 16px;
                    right: 16px;
                    background: rgba(0, 0, 0, 0.8);
                    color: white;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-size: 0.8rem;
                ">
                    {selected_img['resolution']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Controles de imagen
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                if st.button("🔍 Zoom In"):
                    st.info("🔍 Zoom aplicado")
            
            with col_b:
                if st.button("🔍 Zoom Out"):
                    st.info("🔍 Zoom reducido")
            
            with col_c:
                if st.button("🔄 Rotar"):
                    st.info("🔄 Imagen rotada")
            
            with col_d:
                if st.button("❌ Cerrar"):
                    st.session_state.selected_image = None
                    st.rerun()
        
        with col2:
            st.markdown("#### 📋 Información")
            st.markdown(f"**🖼️ {selected_img['title']}**")
            st.markdown(f"📂 {selected_img['category']}")
            st.markdown(f"👨‍🎨 {selected_img['photographer']}")
            st.markdown(f"📅 {selected_img['upload_date'].strftime('%d/%m/%Y')}")
            
            st.markdown("#### 🔧 Especificaciones")
            st.metric("📐 Resolución", selected_img['resolution'])
            st.metric("🔢 Megapíxeles", f"{selected_img['megapixels']}MP")
            st.metric("📄 Formato", selected_img['format'])
            st.metric("💾 Tamaño", f"{selected_img['size_mb']:.1f}MB")
            
            st.markdown("#### 📊 Estadísticas")
            st.metric("👁️ Vistas", f"{selected_img['views']:,}")
            st.metric("❤️ Likes", f"{selected_img['likes']:,}")
            st.metric("⬇️ Descargas", f"{selected_img['downloads']:,}")
            
            # Botones de acción
            if st.button("❤️ Me Gusta", use_container_width=True):
                st.success("💖 ¡Agregado a favoritos!")
            
            if st.button("⬇️ Descargar", use_container_width=True):
                st.success("📥 ¡Descarga iniciada!")
            
            if st.button("📤 Compartir", use_container_width=True):
                st.info("🔗 Enlace copiado")
            
            # Tags
            st.markdown("#### 🏷️ Tags")
            tags_html = " ".join([f"<span style='background: rgba(59, 130, 246, 0.2); color: #3b82f6; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; margin: 2px;'>{tag}</span>" for tag in selected_img['tags']])
            st.markdown(tags_html, unsafe_allow_html=True)
    
    # Galería principal
    st.markdown("### 🎨 Galería Principal")
    
    if len(filtered_df) > 0:
        if view_mode == "Grid":
            # Vista en grid (4 columnas)
            images_per_row = 4
            images_to_show = filtered_df.head(20)
            
            for i in range(0, len(images_to_show), images_per_row):
                cols = st.columns(images_per_row)
                
                for j in range(images_per_row):
                    if i + j < len(images_to_show):
                        img = images_to_show.iloc[i + j]
                        
                        with cols[j]:
                            # Color aleatorio para cada imagen
                            colors = ['#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43', '#10ac84', '#ee5253', '#0abde3']
                            img_color = colors[(i + j) % len(colors)]
                            
                            # Crear botón clickeable para la imagen
                            if st.button(f"img_{img['id']}", key=f"img_btn_{img['id']}", 
                                       help=f"Click para ver {img['title']}", 
                                       use_container_width=True):
                                st.session_state.selected_image = img['id']
                                st.rerun()
                            
                            st.markdown(f"""
                            <div class="animate-fadeInUp delay-{(i+j)*50}" style="
                                background: {img_color};
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
                                    font-size: 0.6rem;
                                ">
                                    {img['format']}
                                </div>
                                <div style="
                                    position: absolute;
                                    bottom: 8px;
                                    right: 8px;
                                    background: rgba(0, 0, 0, 0.8);
                                    color: white;
                                    padding: 4px 8px;
                                    border-radius: 4px;
                                    font-size: 0.6rem;
                                ">
                                    {img['megapixels']}MP
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                            <div style="text-align: center; margin-bottom: 1rem;">
                                <div style="font-weight: bold; font-size: 0.9rem; margin-bottom: 0.5rem;">
                                    {img['title'][:20]}{'...' if len(img['title']) > 20 else ''}
                                </div>
                                <div style="font-size: 0.8rem; color: #b8bcc8; margin-bottom: 0.5rem;">
                                    {img['resolution']} • {img['size_mb']:.1f}MB
                                </div>
                                <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #6b7280;">
                                    <span>👁️ {img['views']:,}</span>
                                    <span>⬇️ {img['downloads']:,}</span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
        
        elif view_mode == "Lista":
            # Vista en lista
            for _, img in filtered_df.head(10).iterrows():
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    img_color = random.choice(['#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3'])
                    st.markdown(f"""
                    <div style="
                        background: {img_color};
                        aspect-ratio: 1;
                        border-radius: 8px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 1.5rem;
                        color: white;
                    ">
                        🖼️
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{img['title']}**")
                    st.markdown(f"📂 {img['category']} • 👨‍🎨 {img['photographer']}")
                    st.markdown(f"📐 {img['resolution']} • 📄 {img['format']} • 💾 {img['size_mb']:.1f}MB")
                    
                    tags_html = " ".join([f"<span style='background: rgba(59, 130, 246, 0.2); color: #3b82f6; padding: 2px 6px; border-radius: 8px; font-size: 0.7rem; margin: 1px;'>{tag}</span>" for tag in img['tags'][:3]])
                    st.markdown(tags_html, unsafe_allow_html=True)
                
                with col3:
                    st.metric("👁️", f"{img['views']:,}")
                    st.metric("⬇️", f"{img['downloads']:,}")
                    
                    if st.button("👁️", key=f"view_{img['id']}", help="Ver imagen"):
                        st.session_state.selected_image = img['id']
                        st.rerun()
                
                st.markdown("---")
        
        else:  # Mosaico
            st.markdown("#### 🧩 Vista Mosaico")
            # Vista mosaico con tamaños variables
            cols = st.columns([2, 1, 1])
            
            for i, img in enumerate(filtered_df.head(6).iterrows()):
                _, img_data = img
                col_idx = i % 3
                
                with cols[col_idx]:
                    height = "200px" if col_idx == 0 else "150px"
                    img_color = random.choice(['#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43'])
                    
                    st.markdown(f"""
                    <div style="
                        background: {img_color};
                        height: {height};
                        border-radius: 12px;
                        margin-bottom: 1rem;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 3rem;
                        color: white;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                        🖼️
                    </div>
                    """, unsafe_allow_html=True)
        
        # Paginación
        if len(filtered_df) > 20:
            st.markdown("### 📄 Paginación")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📥 Cargar Más Imágenes", use_container_width=True):
                    st.info("🔄 Cargando más imágenes...")
    
    else:
        st.info("🔍 No se encontraron imágenes con los filtros aplicados")
    
    # Subir nueva imagen
    with st.expander("📤 Subir Nueva Imagen", expanded=False):
        st.markdown("### 🖼️ Subir Imagen")
        
        uploaded_file = st.file_uploader(
            "Selecciona una imagen",
            type=['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'],
            help="Formatos soportados: JPG, PNG, GIF, WebP, BMP (máx. 50MB)"
        )
        
        if uploaded_file:
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("🖼️ Título de la imagen", value=uploaded_file.name.split('.')[0])
                category = st.selectbox("📂 Categoría", ["Paisajes", "Retratos", "Abstracto", "Arquitectura", "Naturaleza", "Arte Digital"])
                photographer = st.text_input("👨‍🎨 Fotógrafo", placeholder="Tu nombre")
                description = st.text_area("📝 Descripción", placeholder="Describe tu imagen...")
            
            with col2:
                tags = st.text_input("🏷️ Tags", placeholder="naturaleza, paisaje, color")
                visibility = st.selectbox("👁️ Visibilidad", ["Público", "Privado"])
                optimize = st.checkbox("⚡ Optimizar automáticamente", value=True)
                generate_formats = st.checkbox("🔄 Generar formatos adicionales (WebP)", value=True)
            
            if st.button("🚀 Subir Imagen", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 40:
                        status_text.text("📤 Subiendo archivo...")
                    elif i < 70:
                        status_text.text("🖼️ Procesando imagen...")
                    elif i < 90:
                        status_text.text("⚡ Optimizando...")
                    else:
                        status_text.text("✅ Finalizando...")
                    
                    import time
                    time.sleep(0.03)
                
                st.success(f"🎉 ¡Imagen '{title}' subida exitosamente!")
                st.balloons()