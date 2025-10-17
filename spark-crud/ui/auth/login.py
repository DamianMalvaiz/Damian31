# ui/auth/login.py
# Sistema de autenticación con diseño brutal
# ==========================================

import streamlit as st
import hashlib
import time
from datetime import datetime

# Configuración de usuarios
ALLOWED_USERS = {"damian", "david", "alexis"}
PASSWORD_HASH = "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"  # SHA256 de "Hola123"

def check_credentials(username: str, password: str) -> bool:
    """Verifica las credenciales del usuario"""
    if not username or not password:
        return False
    
    # Verificar usuario
    if username.strip().lower() not in ALLOWED_USERS:
        return False
    
    # Verificar contraseña
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password_hash == PASSWORD_HASH

def check_authentication() -> bool:
    """Verifica si el usuario está autenticado"""
    return st.session_state.get('authenticated', False)

def render_login():
    """Renderiza la página de login con diseño brutal"""
    
    # CSS específico para login
    st.markdown("""
    <style>
    .login-container {
        max-width: 480px;
        margin: 80px auto;
        padding: 3rem;
        background: rgba(30, 30, 46, 0.95);
        border-radius: 24px;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.5),
            0 0 40px rgba(59, 130, 246, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        animation: loginFloat 6s ease-in-out infinite;
    }
    
    @keyframes loginFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .login-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    .login-subtitle {
        text-align: center;
        color: #b8bcc8;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    
    .login-form {
        margin-bottom: 2rem;
    }
    
    .login-footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Partículas de fondo */
    .login-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background: 
            radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.15) 0%, transparent 50%);
        animation: particlesFloat 20s ease-in-out infinite;
    }
    
    @keyframes particlesFloat {
        0%, 100% { 
            background-position: 0% 0%, 100% 100%; 
        }
        50% { 
            background-position: 100% 100%, 0% 0%; 
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Fondo de partículas
    st.markdown('<div class="login-particles"></div>', unsafe_allow_html=True)
    
    # Contenedor principal de login
    st.markdown("""
    <div class="login-container">
        <div class="login-title">🔥 ACCESO BRUTAL</div>
        <div class="login-subtitle">
            Ingresa tus credenciales para acceder al sistema más épico
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulario de login centrado
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### 🔐 Credenciales")
            
            # Campo de usuario
            username = st.text_input(
                "👤 Usuario",
                placeholder="damian / david / alexis",
                help="Usuarios disponibles: damian, david, alexis"
            )
            
            # Campo de contraseña
            password = st.text_input(
                "🔒 Contraseña",
                type="password",
                placeholder="••••••••",
                help="Contraseña: Hola123"
            )
            
            # Checkbox recordar sesión
            remember_me = st.checkbox("💭 Recordar sesión", value=True)
            
            # Botón de login
            login_button = st.form_submit_button(
                "🚀 ENTRAR AL SISTEMA",
                use_container_width=True
            )
            
            # Procesar login
            if login_button:
                if check_credentials(username, password):
                    # Login exitoso
                    with st.spinner("🔓 Verificando credenciales..."):
                        time.sleep(1)
                    
                    # Establecer estado de sesión
                    st.session_state.authenticated = True
                    st.session_state.user = username.strip().lower()
                    st.session_state.login_time = datetime.now()
                    st.session_state.remember_me = remember_me
                    
                    # Mensaje de éxito
                    st.success(f"🎉 ¡Bienvenido {username.title()}!")
                    st.balloons()
                    
                    # Recargar página
                    time.sleep(1)
                    st.rerun()
                    
                else:
                    # Login fallido
                    st.error("❌ Credenciales inválidas")
                    st.markdown("""
                    <div style="
                        background: rgba(239, 68, 68, 0.1);
                        border: 1px solid #ef4444;
                        border-radius: 8px;
                        padding: 1rem;
                        margin-top: 1rem;
                        text-align: center;
                    ">
                        <strong>🔐 Usuarios válidos:</strong><br>
                        damian, david, alexis<br>
                        <strong>🔒 Contraseña:</strong> Hola123
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer de login
    st.markdown("""
    <div style="
        text-align: center;
        margin-top: 3rem;
        color: #6b7280;
        font-size: 0.9rem;
    ">
        <p>🔥 <strong>Media Management System v2.0</strong> 🔥</p>
        <p>Desarrollado con 💜 por el equipo más BRUTAL</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Información de demo
    with st.expander("ℹ️ Información de Acceso", expanded=False):
        st.markdown("""
        ### 🔑 Credenciales de Demo
        
        **Usuarios disponibles:**
        - 👨‍💻 **damian** - Administrador principal
        - 👨‍🎨 **david** - Editor de contenido  
        - 👨‍🔬 **alexis** - Analista de datos
        
        **Contraseña para todos:** `Hola123`
        
        ### 🚀 Funcionalidades
        
        Una vez autenticado tendrás acceso a:
        - 🏠 **Dashboard**: Métricas en tiempo real
        - 👥 **Customers**: CRUD completo de usuarios
        - 🎥 **Videos**: Galería y reproductor
        - 🖼️ **Imágenes**: Galería con lightbox
        - 🎵 **Audio**: Reproductor con playlist
        - 📊 **Analytics**: Estadísticas avanzadas
        - ⚙️ **Configuración**: Ajustes del sistema
        
        ### 🎨 Temas Disponibles
        - 🌑 **Dark**: Tema oscuro profesional
        - 🌈 **Cyberpunk**: Neones futuristas
        - 💚 **Matrix**: Verde código
        - 🌅 **Synthwave**: Retro 80s
        """)

def logout():
    """Cierra la sesión del usuario"""
    # Limpiar estado de sesión
    keys_to_clear = ['authenticated', 'user', 'login_time', 'remember_me']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    st.success("👋 Sesión cerrada exitosamente")
    time.sleep(1)
    st.rerun()

def get_current_user() -> str:
    """Obtiene el usuario actual"""
    return st.session_state.get('user', 'guest')

def is_admin() -> bool:
    """Verifica si el usuario actual es administrador"""
    return st.session_state.get('user') == 'damian'

def get_user_permissions() -> dict:
    """Obtiene los permisos del usuario actual"""
    user = get_current_user()
    
    permissions = {
        'damian': {
            'view_dashboard': True,
            'manage_customers': True,
            'upload_media': True,
            'view_analytics': True,
            'system_config': True,
            'user_management': True
        },
        'david': {
            'view_dashboard': True,
            'manage_customers': True,
            'upload_media': True,
            'view_analytics': True,
            'system_config': False,
            'user_management': False
        },
        'alexis': {
            'view_dashboard': True,
            'manage_customers': False,
            'upload_media': False,
            'view_analytics': True,
            'system_config': False,
            'user_management': False
        }
    }
    
    return permissions.get(user, {})

__all__ = [
    'render_login',
    'check_authentication',
    'logout',
    'get_current_user',
    'is_admin',
    'get_user_permissions'
]