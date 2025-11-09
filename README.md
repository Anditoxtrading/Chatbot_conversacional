# 💙 Chat Motivacional - Sistema de Apoyo Emocional

Un chatbot interactivo diseñado para motivar, apoyar y acompañar a los usuarios en su bienestar emocional diario.

## ✨ Características

### 🎯 Funcionalidades Principales
- **Detección de Emociones**: Identifica automáticamente el estado emocional del usuario (tristeza, ansiedad, estrés, felicidad, etc.)
- **Respuestas Personalizadas**: Mensajes motivacionales adaptados a cada emoción detectada
- **Herramientas de Bienestar**:
  - 🧘 Ejercicios de respiración guiados (técnica 4-7-8)
  - ✨ Afirmaciones positivas personalizadas
  - 💡 Consejos de bienestar y autocuidado
- **Interfaz Moderna**: Diseño atractivo, responsivo y fácil de usar
- **Acciones Rápidas**: Botones de acceso directo para estados emocionales comunes

### 🎨 Diseño
- Interfaz moderna con degradados y animaciones suaves
- Totalmente responsivo (funciona en desktop, tablet y móvil)
- Emojis y elementos visuales que mejoran la experiencia
- Tema morado/azul relajante y profesional

## 🚀 Instalación

### Requisitos Previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd chat_motivacional
   ```

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv

   # Activar en Windows:
   venv\Scripts\activate

   # Activar en Mac/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

5. **Abrir en el navegador**
   - Abre tu navegador web
   - Visita: `http://localhost:5000`
   - ¡Listo! Ya puedes usar el chat

## 📖 Cómo Usar

### Conversación Básica
Simplemente escribe cómo te sientes o qué necesitas. El chatbot detectará tu emoción y responderá apropiadamente.

**Ejemplos:**
- "Me siento triste hoy"
- "Estoy muy estresado con el trabajo"
- "Necesito motivación"
- "Me siento feliz"

### Comandos Especiales

| Comando | Función |
|---------|---------|
| `respiración` | Inicia un ejercicio de respiración guiado |
| `afirmación` | Recibe una afirmación positiva aleatoria |
| `consejo` | Obtén un consejo de bienestar |
| `ayuda` | Muestra todas las funcionalidades disponibles |

### Botones Rápidos
Usa los botones en la parte inferior para acceso rápido:
- 😔 Triste
- 😰 Estresado
- 💪 Motivación
- 🧘 Respirar
- ✨ Afirmación

## 🏗️ Estructura del Proyecto

```
chat_motivacional/
│
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias Python
├── README.md             # Este archivo
│
├── templates/
│   └── index.html        # Interfaz HTML del chat
│
└── static/
    ├── style.css         # Estilos CSS
    └── script.js         # Lógica JavaScript del frontend
```

## 🔧 Personalización

### Agregar Nuevas Emociones
Edita el archivo `app.py` en las secciones:
- `PALABRAS_CLAVE`: Agrega palabras que identifiquen la nueva emoción
- `MENSAJES_MOTIVACIONALES`: Agrega mensajes para esa emoción

### Modificar Afirmaciones/Consejos
En `app.py`, encuentra la sección `HERRAMIENTAS` y agrega o modifica:
- `afirmaciones`: Lista de afirmaciones positivas
- `consejos`: Lista de consejos de bienestar

### Cambiar Colores/Tema
Edita `static/style.css` en la sección `:root` para cambiar:
- `--primary-color`: Color principal
- `--secondary-color`: Color secundario
- `--accent-color`: Color de acento

## 🌐 Deployment (Subir a Internet)

### Opción 1: Render (Recomendado - Gratis)
1. Crea una cuenta en [Render.com](https://render.com)
2. Conecta tu repositorio de GitHub
3. Selecciona "New Web Service"
4. Render detectará automáticamente Flask
5. ¡Listo! Tendrás una URL pública

### Opción 2: PythonAnywhere (Gratis)
1. Crea una cuenta en [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Sube los archivos del proyecto
3. Configura la web app desde el dashboard
4. Especifica `app.py` como archivo principal

### Opción 3: Heroku
1. Instala Heroku CLI
2. Crea un archivo `Procfile` con: `web: python app.py`
3. Sigue la guía de Heroku para deployment

## 💡 Ideas de Mejora

Para presentar al cliente como "features adicionales":
- 🗄️ Guardar historial de conversaciones
- 📊 Estadísticas de estado de ánimo
- 🔔 Recordatorios diarios de afirmaciones
- 🎵 Integración con música relajante
- 📱 Versión como app móvil
- 🤖 Integración con IA (GPT) para respuestas más naturales
- 👥 Sistema de usuarios/login
- 🌙 Modo oscuro/claro

## 📄 Licencia

Este proyecto es libre de usar y modificar para proyectos personales o comerciales.

## 🤝 Soporte

Para preguntas o sugerencias sobre este proyecto, puedes:
- Revisar la documentación en este README
- Modificar el código según tus necesidades
- Consultar la documentación de Flask: https://flask.palletsprojects.com/

---

**💙 Desarrollado con el objetivo de promover el bienestar emocional y el pensamiento positivo**

## 🎯 Tips para Presentar en Workana

### Qué Destacar:
1. ✅ **Sistema completamente funcional** - No es solo una demo
2. ✅ **Sin costos adicionales** - No requiere APIs de pago
3. ✅ **Fácil de personalizar** - Todo el código es claro y comentado
4. ✅ **Listo para deploy** - Se puede subir gratis a internet
5. ✅ **Diseño profesional** - Interfaz moderna y atractiva
6. ✅ **Responsive** - Funciona en todos los dispositivos

### Cómo Presentarlo:
- Captura de pantalla o video de la aplicación funcionando
- Menciona que es **escalable** (se puede agregar IA, base de datos, etc.)
- Destaca el **enfoque en UX** (experiencia de usuario)
- Ofrece **customización** según las necesidades del cliente

### Presupuesto Sugerido:
- Proyecto básico (como está): $150-$300 USD
- Con customización de marca: $250-$400 USD
- Con features adicionales (DB, IA): $400-$700 USD
