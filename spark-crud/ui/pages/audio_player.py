# ui/pages/audio_player.py
# Reproductor de audio con playlist y análisis musical
# ===================================================

import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def render():
    """Renderiza la página del reproductor de audio"""
    
    # Header de la página
    st.markdown("""
    <div class="animate-fadeInDown">
        <h2 style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        ">
            🎵 Reproductor de Audio Épico
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Generar datos demo de audio
    @st.cache_data
    def generate_audio_data():
        artists = [
            "DJ Brutal", "Synthwave Master", "Electronic Dreams", "Cyber Beats",
            "Neon Nights", "Digital Pulse", "Future Bass", "Retrowave King",
            "Ambient Space", "Techno Warrior", "House Legend", "Trance Vision"
        ]
        
        genres = ["Synthwave", "Techno", "House", "Trance", "Ambient", "Electronic", "Chillwave", "Cyberpunk"]
        
        track_names = [
            "Neon Dreams", "Cyber Highway", "Digital Sunset", "Electric Pulse",
            "Midnight Drive", "Future Memories", "Synthetic Love", "Chrome Hearts",
            "Laser Grid", "Hologram", "Binary Code", "Virtual Reality",
            "Quantum Leap", "Space Odyssey", "Time Machine", "Neural Network"
        ]
        
        data = []
        for i in range(60):
            duration = np.random.uniform(180, 420)  # 3-7 minutos
            plays = np.random.randint(100, 50000)
            likes = int(plays * np.random.uniform(0.05, 0.25))
            
            data.append({
                'id': i + 1,
                'title': f"{random.choice(track_names)} {i+1}",
                'artist': random.choice(artists),
                'album': f"Album {np.random.randint(1, 10)}",
                'genre': random.choice(genres),
                'duration': duration,
                'duration_formatted': f"{int(duration//60):02d}:{int(duration%60):02d}",
                'bpm': np.random.randint(80, 180),
                'key': random.choice(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']),
                'mode': random.choice(['Major', 'Minor']),
                'energy': np.random.uniform(0.2, 1.0),
                'valence': np.random.uniform(0.1, 0.9),
                'danceability': np.random.uniform(0.3, 1.0),
                'plays': plays,
                'likes': likes,
                'file_size_mb': np.random.uniform(3, 15),
                'bitrate': random.choice([128, 192, 256, 320]),
                'format': random.choice(['MP3', 'FLAC', 'WAV', 'AAC']),
                'upload_date': datetime.now() - timedelta(days=np.random.randint(1, 365)),
                'mood': random.choice(['Energético', 'Relajado', 'Melancólico', 'Eufórico', 'Misterioso'])
            })
        
        return pd.DataFrame(data)
    
    audio_df = generate_audio_data()
    
    # Estado del reproductor
    if 'current_track' not in st.session_state:
        st.session_state.current_track = 0
    if 'is_playing' not in st.session_state:
        st.session_state.is_playing = False
    if 'current_time' not in st.session_state:
        st.session_state.current_time = 0
    if 'volume' not in st.session_state:
        st.session_state.volume = 75
    if 'shuffle' not in st.session_state:
        st.session_state.shuffle = False
    if 'repeat' not in st.session_state:
        st.session_state.repeat = False
    
    current_track_data = audio_df.iloc[st.session_state.current_track]
    
    # Reproductor principal
    st.markdown("### 🎧 Now Playing")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Artwork animado
        artwork_colors = ['#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#38f9d7']
        artwork_color1 = random.choice(artwork_colors)
        artwork_color2 = random.choice(artwork_colors)
        
        rotation_class = "animate-rotate" if st.session_state.is_playing else ""
        
        st.markdown(f"""
        <div class="{rotation_class}" style="
            background: linear-gradient(45deg, {artwork_color1}, {artwork_color2});
            aspect-ratio: 1;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            color: white;
            border: 4px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
        ">
            🎵
        </div>
        """, unsafe_allow_html=True)
        
        # Información del track
        st.markdown(f"""
        <div style="text-align: center;">
            <h3 style="margin-bottom: 0.5rem; color: white;">{current_track_data['title']}</h3>
            <p style="color: #b8bcc8; margin-bottom: 0.5rem; font-size: 1.1rem;">{current_track_data['artist']}</p>
            <p style="color: #6b7280; font-size: 0.9rem;">{current_track_data['album']} • {current_track_data['genre']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Controles principales
        st.markdown("#### 🎛️ Controles")
        
        # Barra de progreso
        max_time = int(current_track_data['duration'])
        current_time = st.slider(
            "", 0, max_time, st.session_state.current_time,
            label_visibility="collapsed",
            key="progress_slider"
        )
        st.session_state.current_time = current_time
        
        # Tiempo actual y total
        col_time1, col_time2 = st.columns(2)
        with col_time1:
            st.markdown(f"**{current_time//60:02d}:{current_time%60:02d}**")
        with col_time2:
            st.markdown(f"<div style='text-align: right'><strong>{current_track_data['duration_formatted']}</strong></div>", 
                       unsafe_allow_html=True)
        
        # Botones de control
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("⏮️", help="Anterior", key="prev_btn"):
                if st.session_state.current_track > 0:
                    st.session_state.current_track -= 1
                    st.session_state.current_time = 0
                    st.rerun()
        
        with col2:
            play_icon = "⏸️" if st.session_state.is_playing else "▶️"
            if st.button(play_icon, help="Reproducir/Pausar", key="play_btn"):
                st.session_state.is_playing = not st.session_state.is_playing
                if st.session_state.is_playing:
                    st.success("🎵 Reproduciendo...")
                else:
                    st.info("⏸️ Pausado")
        
        with col3:
            if st.button("⏹️", help="Detener", key="stop_btn"):
                st.session_state.is_playing = False
                st.session_state.current_time = 0
                st.warning("⏹️ Detenido")
        
        with col4:
            if st.button("⏭️", help="Siguiente", key="next_btn"):
                if st.session_state.current_track < len(audio_df) - 1:
                    st.session_state.current_track += 1
                    st.session_state.current_time = 0
                    st.rerun()
        
        with col5:
            shuffle_icon = "🔀" if st.session_state.shuffle else "➡️"
            if st.button(shuffle_icon, help="Aleatorio", key="shuffle_btn"):
                st.session_state.shuffle = not st.session_state.shuffle
                status = "activado" if st.session_state.shuffle else "desactivado"
                st.info(f"🔀 Modo aleatorio {status}")
        
        # Controles adicionales
        col1, col2 = st.columns(2)
        
        with col1:
            volume = st.slider("🔊 Volumen", 0, 100, st.session_state.volume, key="volume_slider")
            st.session_state.volume = volume
        
        with col2:
            repeat_options = ["Sin repetir", "Repetir lista", "Repetir canción"]
            repeat_mode = st.selectbox("🔁 Repetir", repeat_options, key="repeat_select")
    
    # Información del track actual
    st.markdown("### 📊 Análisis Musical")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎵 BPM", current_track_data['bpm'])
        st.metric("🎼 Clave", f"{current_track_data['key']} {current_track_data['mode']}")
    
    with col2:
        energy_pct = int(current_track_data['energy'] * 100)
        st.metric("⚡ Energía", f"{energy_pct}%")
        
        valence_pct = int(current_track_data['valence'] * 100)
        st.metric("😊 Valencia", f"{valence_pct}%")
    
    with col3:
        dance_pct = int(current_track_data['danceability'] * 100)
        st.metric("💃 Bailabilidad", f"{dance_pct}%")
        st.metric("🎭 Mood", current_track_data['mood'])
    
    with col4:
        st.metric("👁️ Reproducciones", f"{current_track_data['plays']:,}")
        st.metric("❤️ Likes", f"{current_track_data['likes']:,}")
    
    # Visualizador de audio
    st.markdown("#### 🌊 Visualizador de Audio")
    
    # Simular barras de audio
    if st.session_state.is_playing:
        bars_html = ""
        for i in range(50):
            height = np.random.randint(20, 100)
            delay = i * 0.1
            bars_html += f"""
            <div style="
                width: 4px;
                height: {height}px;
                background: linear-gradient(to top, #4facfe, #00f2fe);
                margin: 0 1px;
                border-radius: 2px;
                animation: audioWave 0.8s ease-in-out infinite;
                animation-delay: {delay}s;
                box-shadow: 0 0 5px rgba(79, 172, 254, 0.5);
            "></div>
            """
        
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: end;
            justify-content: center;
            height: 100px;
            padding: 1rem;
            background: rgba(30, 30, 46, 0.5);
            border-radius: 12px;
            margin: 1rem 0;
        ">
            {bars_html}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100px;
            background: rgba(30, 30, 46, 0.5);
            border-radius: 12px;
            margin: 1rem 0;
            color: #6b7280;
            font-size: 1.2rem;
        ">
            🎵 Presiona play para ver el visualizador
        </div>
        """, unsafe_allow_html=True)
    
    # Filtros de playlist
    st.markdown("### 🎯 Filtros de Playlist")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_track = st.text_input("🔍 Buscar track", placeholder="Título o artista...")
    
    with col2:
        genre_filter = st.selectbox("🎼 Género", ["Todos"] + sorted(audio_df['genre'].unique()))
    
    with col3:
        mood_filter = st.selectbox("🎭 Mood", ["Todos"] + sorted(audio_df['mood'].unique()))
    
    with col4:
        sort_playlist = st.selectbox("🔄 Ordenar por", [
            "Orden actual", "Más reproducidos", "Más gustados", "BPM", "Energía", "Recientes"
        ])
    
    # Aplicar filtros
    filtered_audio = audio_df.copy()
    
    if search_track:
        mask = (filtered_audio['title'].str.contains(search_track, case=False, na=False) |
                filtered_audio['artist'].str.contains(search_track, case=False, na=False))
        filtered_audio = filtered_audio[mask]
    
    if genre_filter != "Todos":
        filtered_audio = filtered_audio[filtered_audio['genre'] == genre_filter]
    
    if mood_filter != "Todos":
        filtered_audio = filtered_audio[filtered_audio['mood'] == mood_filter]
    
    # Aplicar ordenamiento
    if sort_playlist == "Más reproducidos":
        filtered_audio = filtered_audio.sort_values('plays', ascending=False)
    elif sort_playlist == "Más gustados":
        filtered_audio = filtered_audio.sort_values('likes', ascending=False)
    elif sort_playlist == "BPM":
        filtered_audio = filtered_audio.sort_values('bpm', ascending=False)
    elif sort_playlist == "Energía":
        filtered_audio = filtered_audio.sort_values('energy', ascending=False)
    elif sort_playlist == "Recientes":
        filtered_audio = filtered_audio.sort_values('upload_date', ascending=False)
    
    # Playlist
    st.markdown(f"### 📜 Playlist ({len(filtered_audio)} tracks)")
    
    for i, (_, track) in enumerate(filtered_audio.head(15).iterrows()):
        is_current = track['id'] == current_track_data['id']
        
        # Color de fondo para el track actual
        bg_color = "rgba(0, 212, 255, 0.2)" if is_current else "rgba(255, 255, 255, 0.05)"
        border_color = "#00d4ff" if is_current else "transparent"
        
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col1:
            if st.button("▶️", key=f"play_track_{track['id']}", help=f"Reproducir {track['title']}"):
                # Encontrar el índice del track en el DataFrame original
                track_index = audio_df[audio_df['id'] == track['id']].index[0]
                st.session_state.current_track = track_index
                st.session_state.current_time = 0
                st.session_state.is_playing = True
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="animate-fadeInLeft delay-{i*50}" style="
                background: {bg_color};
                padding: 1rem;
                border-radius: 12px;
                border-left: 4px solid {border_color};
                margin-bottom: 0.5rem;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: bold; color: white; margin-bottom: 0.25rem;">
                            {'🎵 ' if is_current else ''}{track['title']}
                        </div>
                        <div style="color: #b8bcc8; font-size: 0.9rem;">
                            {track['artist']} • {track['album']} • {track['duration_formatted']}
                        </div>
                        <div style="color: #6b7280; font-size: 0.8rem; margin-top: 0.25rem;">
                            🎼 {track['genre']} • 🎵 {track['bpm']} BPM • 🎭 {track['mood']}
                        </div>
                    </div>
                    <div style="text-align: right; font-size: 0.8rem; color: #b8bcc8;">
                        <div>▶️ {track['plays']:,}</div>
                        <div>❤️ {track['likes']:,}</div>
                        <div>💾 {track['file_size_mb']:.1f}MB</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.button("❤️", key=f"like_track_{track['id']}", help="Me gusta"):
                st.success("💖 ¡Agregado a favoritos!")
    
    # Estadísticas de la playlist
    if len(filtered_audio) > 0:
        st.markdown("### 📊 Estadísticas de Playlist")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_duration = filtered_audio['duration'].sum() / 3600
            st.metric("⏱️ Duración Total", f"{total_duration:.1f}h")
        
        with col2:
            avg_bpm = filtered_audio['bpm'].mean()
            st.metric("🎵 BPM Promedio", f"{avg_bpm:.0f}")
        
        with col3:
            avg_energy = filtered_audio['energy'].mean() * 100
            st.metric("⚡ Energía Promedio", f"{avg_energy:.0f}%")
        
        with col4:
            total_plays = filtered_audio['plays'].sum()
            st.metric("👁️ Reproducciones Totales", f"{total_plays:,}")
        
        # Gráfico de distribución de géneros
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎼 Distribución por Género")
            genre_counts = filtered_audio['genre'].value_counts()
            st.bar_chart(genre_counts)
        
        with col2:
            st.markdown("#### 🎭 Distribución por Mood")
            mood_counts = filtered_audio['mood'].value_counts()
            st.bar_chart(mood_counts)
    
    # Subir nuevo audio
    with st.expander("📤 Subir Nuevo Audio", expanded=False):
        st.markdown("### 🎵 Subir Track")
        
        uploaded_file = st.file_uploader(
            "Selecciona un archivo de audio",
            type=['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a'],
            help="Formatos soportados: MP3, WAV, FLAC, AAC, OGG, M4A (máx. 100MB)"
        )
        
        if uploaded_file:
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("🎵 Título", value=uploaded_file.name.split('.')[0])
                artist = st.text_input("👨‍🎤 Artista", placeholder="Nombre del artista")
                album = st.text_input("💿 Álbum", placeholder="Nombre del álbum")
                genre = st.selectbox("🎼 Género", ["Synthwave", "Techno", "House", "Trance", "Ambient", "Electronic"])
            
            with col2:
                bpm = st.number_input("🎵 BPM", min_value=60, max_value=200, value=120)
                key = st.selectbox("🎼 Clave", ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
                mode = st.selectbox("🎭 Modo", ['Major', 'Minor'])
                tags = st.text_input("🏷️ Tags", placeholder="synthwave, retro, electronic")
            
            if st.button("🚀 Subir Audio", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text("📤 Subiendo archivo...")
                    elif i < 60:
                        status_text.text("🎵 Analizando audio...")
                    elif i < 85:
                        status_text.text("🎼 Extrayendo metadata...")
                    else:
                        status_text.text("✅ Finalizando...")
                    
                    import time
                    time.sleep(0.04)
                
                st.success(f"🎉 ¡Track '{title}' subido exitosamente!")
                st.balloons()