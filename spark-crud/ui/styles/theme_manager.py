# ui/styles/theme_manager.py
# Gestor de temas y estilos dinámicos
# ==================================

import streamlit as st
from typing import Dict, Any, Optional
from pathlib import Path
import os

class ThemeManager:
    """Gestor centralizado de temas y estilos CSS"""
    
    def __init__(self):
        self.themes = {
            "dark": {
                "name": "Tema Oscuro Brutal",
                "css_file": "main.css",
                "primary_color": "#3b82f6",
                "secondary_color": "#8b5cf6",
                "accent_color": "#06d6a0",
                "background": "#0a0a0f",
                "surface": "#1e1e2e"
            },
            "cyberpunk": {
                "name": "Cyberpunk Neón",
                "css_file": "cyberpunk_theme.css",
                "primary_color": "#ff0080",
                "secondary_color": "#00ff80",
                "accent_color": "#0080ff",
                "background": "#0d0208",
                "surface": "#1a0f1a"
            },
            "matrix": {
                "name": "Matrix Verde",
                "css_file": "matrix_theme.css", 
                "primary_color": "#00ff41",
                "secondary_color": "#008f11",
                "accent_color": "#39ff14",
                "background": "#000000",
                "surface": "#0a0a0a"
            },
            "synthwave": {
                "name": "Synthwave Retro",
                "css_file": "synthwave_theme.css",
                "primary_color": "#ff006e",
                "secondary_color": "#8338ec",
                "accent_color": "#ffbe0b",
                "background": "#1a0033",
                "surface": "#2d1b69"
            }
        }
        
        self.current_theme = self._get_current_theme()
        self.styles_dir = Path(__file__).parent
    
    def _get_current_theme(self) -> str:
        """Obtiene el tema actual desde session state"""
        return st.session_state.get('current_theme', 'dark')
    
    def set_theme(self, theme_name: str):
        """Establece el tema actual"""
        if theme_name in self.themes:
            st.session_state['current_theme'] = theme_name
            self.current_theme = theme_name
            return True
        return False
    
    def get_theme_info(self, theme_name: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene información del tema"""
        theme_name = theme_name or self.current_theme
        return self.themes.get(theme_name, self.themes['dark'])
    
    def load_css_file(self, filename: str) -> str:
        """Carga contenido de archivo CSS"""
        css_path = self.styles_dir / filename
        if css_path.exists():
            return css_path.read_text(encoding='utf-8')
        return ""
    
    def apply_theme(self):
        """Aplica el tema actual a Streamlit"""
        theme_info = self.get_theme_info()
        
        # Cargar CSS principal
        main_css = self.load_css_file("main.css")
        animations_css = self.load_css_file("animations.css")
        components_css = self.load_css_file("components.css")
        media_css = self.load_css_file("media.css")
        
        # Combinar todos los CSS
        full_css = f"""
        {main_css}
        {animations_css}
        {components_css}
        {media_css}
        
        /* Tema específico: {theme_info['name']} */
        {self._generate_theme_variables(theme_info)}
        """
        
        # Aplicar CSS a Streamlit
        st.markdown(f"<style>{full_css}</style>", unsafe_allow_html=True)
    
    def _generate_theme_variables(self, theme_info: Dict[str, Any]) -> str:
        """Genera variables CSS específicas del tema"""
        return f"""
        :root {{
            --theme-primary: {theme_info['primary_color']};
            --theme-secondary: {theme_info['secondary_color']};
            --theme-accent: {theme_info['accent_color']};
            --theme-background: {theme_info['background']};
            --theme-surface: {theme_info['surface']};
        }}
        """
    
    def render_theme_selector(self):
        """Renderiza selector de temas en la UI"""
        st.markdown("### 🎨 Selector de Tema")
        
        theme_options = {info['name']: key for key, info in self.themes.items()}
        current_theme_name = self.get_theme_info()['name']
        
        selected_theme_name = st.selectbox(
            "Elige tu tema favorito:",
            options=list(theme_options.keys()),
            index=list(theme_options.keys()).index(current_theme_name),
            key="theme_selector"
        )
        
        selected_theme_key = theme_options[selected_theme_name]
        
        if selected_theme_key != self.current_theme:
            if st.button("🎯 Aplicar Tema", key="apply_theme"):
                self.set_theme(selected_theme_key)
                st.success(f"✨ Tema '{selected_theme_name}' aplicado!")
                st.rerun()
        
        # Preview del tema
        self._render_theme_preview(selected_theme_key)
    
    def _render_theme_preview(self, theme_key: str):
        """Renderiza preview del tema"""
        theme_info = self.get_theme_info(theme_key)
        
        st.markdown("#### 🎨 Preview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                f"""
                <div style="
                    background: {theme_info['primary_color']};
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                ">
                    Primario
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style="
                    background: {theme_info['secondary_color']};
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                ">
                    Secundario
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div style="
                    background: {theme_info['accent_color']};
                    padding: 1rem;
                    border-radius: 8px;
                    text-align: center;
                    color: white;
                    font-weight: bold;
                ">
                    Acento
                </div>
                """,
                unsafe_allow_html=True
            )
    
    def get_custom_css_for_component(self, component_type: str) -> str:
        """Obtiene CSS personalizado para componentes específicos"""
        theme_info = self.get_theme_info()
        
        css_templates = {
            "button_primary": f"""
                background: linear-gradient(135deg, {theme_info['primary_color']}, {theme_info['secondary_color']});
                border: none;
                color: white;
                padding: 0.75rem 2rem;
                border-radius: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            """,
            
            "card": f"""
                background: {theme_info['surface']};
                border-radius: 16px;
                padding: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
            """,
            
            "input": f"""
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                color: white;
                padding: 1rem 1.5rem;
                font-size: 1rem;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            """
        }
        
        return css_templates.get(component_type, "")
    
    def create_animated_background(self) -> str:
        """Crea fondo animado basado en el tema"""
        theme_info = self.get_theme_info()
        
        if self.current_theme == "cyberpunk":
            return """
            <style>
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(255, 0, 128, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(0, 255, 128, 0.15) 0%, transparent 50%);
                animation: cyberpunkPulse 4s ease-in-out infinite alternate;
                pointer-events: none;
                z-index: -1;
            }
            
            @keyframes cyberpunkPulse {
                0% { opacity: 0.3; }
                100% { opacity: 0.7; }
            }
            </style>
            """
        elif self.current_theme == "matrix":
            return """
            <style>
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: 
                    linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px),
                    linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px);
                background-size: 20px 20px;
                animation: matrixScroll 20s linear infinite;
                pointer-events: none;
                z-index: -1;
            }
            
            @keyframes matrixScroll {
                0% { transform: translateY(0); }
                100% { transform: translateY(20px); }
            }
            </style>
            """
        
        return ""

# Instancia global del gestor de temas
theme_manager = ThemeManager()

def apply_current_theme():
    """Función de conveniencia para aplicar el tema actual"""
    theme_manager.apply_theme()

def get_theme_manager() -> ThemeManager:
    """Obtiene la instancia del gestor de temas"""
    return theme_manager

__all__ = [
    "ThemeManager",
    "theme_manager", 
    "apply_current_theme",
    "get_theme_manager"
]