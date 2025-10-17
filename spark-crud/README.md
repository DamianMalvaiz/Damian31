# 🔥 Media Management System v2.0 - BRUTAL EDITION

El sistema de gestión multimedia más **ÉPICO** y **BRUTAL** del universo. Desarrollado con tecnologías de vanguardia para manejar millones de archivos multimedia con estilo.

## ⚡ Características Principales

### 🎬 **Gestión Multimedia Completa**
- **Videos**: Reproductor avanzado, miniaturas automáticas, streaming optimizado
- **Imágenes**: Galería épica, optimización automática, análisis de colores
- **Audio**: Reproductor con visualizador, análisis musical, metadata automática

### 👥 **CRUD de Usuarios Avanzado**
- Gestión completa de customers con analytics
- Filtros avanzados y búsqueda inteligente
- Exportación y reportes automáticos

### 📊 **Analytics de Otro Mundo**
- Correlaciones y estadísticas avanzadas
- Series temporales con SMA/EMA
- Detección de outliers automática
- Dashboards interactivos

### 🎨 **UI Brutal**
- **4 temas épicos**: Dark, Cyberpunk, Matrix, Synthwave
- Animaciones fluidas y efectos neón
- Responsive design y accesibilidad
- Componentes reutilizables

### 🚀 **Tecnologías de Vanguardia**
- **Streamlit** para UI reactiva
- **MongoDB + GridFS** para almacenamiento masivo
- **Apache Spark** para big data
- **APIs externas** (YouTube, Unsplash, Pexels)

## 🛠️ Instalación Rápida

### Prerrequisitos
```bash
# Python 3.8+
python --version

# MongoDB (opcional)
mongod --version

# FFmpeg (para procesamiento de video)
ffmpeg -version
```

### Instalación
```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/media-management-system.git
cd media-management-system

# 2. Instalar dependencias básicas
pip install -r requirements.txt

# 3. Instalar dependencias multimedia (opcional)
pip install -r requirements-media.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 5. Ejecutar aplicación
streamlit run app.py
```

## 🚀 Uso Rápido

### Ejecutar la Aplicación
```bash
streamlit run app.py
```

### Acceso
- **URL**: http://localhost:8501
- **Usuarios**: damian, david, alexis
- **Contraseña**: Hola123

### Páginas Disponibles
- 🏠 **Dashboard**: Métricas y resumen general
- 👥 **Customers**: CRUD completo de usuarios
- 🎥 **Videos**: Centro de videos con reproductor
- 🖼️ **Imágenes**: Galería con lightbox
- 🎵 **Audio**: Reproductor con playlist
- 📊 **Analytics**: Estadísticas avanzadas
- ⚙️ **Configuración**: Ajustes del sistema

## 📁 Estructura del Proyecto

```
media-management-system/
├── app.py                      # 🚀 Aplicación principal
├── config/                     # ⚙️ Configuraciones
├── src/                        # 💻 Código fuente
│   ├── domain/                 # 🏗️ Entidades de negocio
│   ├── database/               # 🗄️ Acceso a datos
│   ├── services/               # 🔧 Lógica de negocio
│   ├── external/               # 🌐 APIs externas
│   └── utils/                  # 🛠️ Utilidades
├── ui/                         # 🎨 Interfaz de usuario
│   ├── pages/                  # 📄 Páginas
│   ├── components/             # 🧩 Componentes
│   ├── auth/                   # 🔐 Autenticación
│   └── styles/                 # 🎨 Estilos CSS
├── data/                       # 📊 Datos y archivos
└── tests/                      # 🧪 Tests
```

## 🎨 Temas Disponibles

### 🌑 **Dark Theme** (Por defecto)
Tema oscuro profesional con acentos azules y púrpuras.

### 🌈 **Cyberpunk Theme**
Neones rosas y verdes con estética futurista.

### 💚 **Matrix Theme**
Verde Matrix con efectos de código lluvia.

### 🌅 **Synthwave Theme**
Colores retro con gradientes synthwave.

## 📊 Funcionalidades Avanzadas

### Analytics y Reportes
- Correlaciones de Pearson/Spearman
- Series temporales con indicadores técnicos
- Detección de outliers (Z-score, IQR)
- Exportación automática de reportes

### Procesamiento Multimedia
- Generación automática de miniaturas
- Optimización de imágenes (WebP, compresión)
- Análisis de metadata (EXIF, ID3)
- Streaming adaptativo

### APIs Externas
- **YouTube**: Importación de videos
- **Unsplash**: Imágenes de alta calidad
- **Pexels**: Videos y fotos gratuitas
- **Pixabay**: Contenido libre de derechos

## 🔧 Configuración Avanzada

### Variables de Entorno Principales
```bash
# Base de datos
MONGO_URI=mongodb://localhost:27017
MONGO_DB=media_management

# Multimedia
MAX_VIDEO_SIZE_MB=500
MAX_IMAGE_SIZE_MB=50
IMAGE_OPTIMIZE_QUALITY=85

# APIs (obtener keys en las respectivas plataformas)
YOUTUBE_API_KEY=tu_key_aqui
UNSPLASH_ACCESS_KEY=tu_key_aqui
PEXELS_API_KEY=tu_key_aqui
```

### Personalización de Temas
Edita `ui/styles/main.css` para crear temas personalizados:
```css
:root {
    --color-primary: #tu-color;
    --color-secondary: #tu-color;
    --gradient-primary: linear-gradient(135deg, #color1, #color2);
}
```

## 🚀 Despliegue en Producción

### Docker (Recomendado)
```bash
# Construir imagen
docker build -t media-management .

# Ejecutar contenedor
docker run -p 8501:8501 media-management
```

### Streamlit Cloud
1. Subir a GitHub
2. Conectar con Streamlit Cloud
3. Configurar secrets en la plataforma

### Servidor Local
```bash
# Ejecutar en puerto específico
streamlit run app.py --server.port 8080

# Ejecutar en red
streamlit run app.py --server.address 0.0.0.0
```

## 🤝 Contribuir

### Desarrollo
```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest

# Formatear código
black .
flake8 .
```

### Reportar Issues
- 🐛 **Bugs**: Usar template de bug report
- 💡 **Features**: Usar template de feature request
- 📚 **Documentación**: Mejoras en docs

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Equipo de Desarrollo

- **Damian** - Lead Developer & Architect
- **David** - Frontend & UI/UX
- **Alexis** - Backend & Database

## 🆘 Soporte

- 📧 **Email**: soporte@mediamanagement.com
- 💬 **Discord**: [Servidor de la comunidad](https://discord.gg/mediamanagement)
- 📖 **Docs**: [Documentación completa](https://docs.mediamanagement.com)

---

<div align="center">

**🔥 Desarrollado con 💜 por el equipo más BRUTAL del universo 🔥**

[⭐ Dale una estrella](https://github.com/tu-usuario/media-management-system) | [🐛 Reportar bug](https://github.com/tu-usuario/media-management-system/issues) | [💡 Sugerir feature](https://github.com/tu-usuario/media-management-system/discussions)

</div>