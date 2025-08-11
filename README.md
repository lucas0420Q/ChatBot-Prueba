# 🤖 Asistente Virtual AI

## Descripción
Aplicación de escritorio moderna para interactuar con un asistente virtual basado en IA (Gemini 2.0 Flash). 
Permite análisis inteligente de documentos, generación de casos de prueba, manuales de usuario y mucho más.

## Características Principales

### 🎨 **Interfaz Moderna**
- Diseño moderno con degradados azul/violeta
- Bordes redondeados y efectos visuales
- Responsivo para escritorio (1200x800px mínimo)
- Temas oscuros optimizados

### 🧠 **IA Avanzada**
- Integración con Google Gemini 2.0 Flash
- Procesamiento de lenguaje natural
- Análisis inteligente de documentos
- Respuestas contextuales

### 📁 **Procesamiento de Archivos**
- Soporte para PDF, DOCX, TXT
- Extracción automática de texto
- Análisis de contenido
- Adjuntar múltiples archivos

### 💬 **Gestión de Conversaciones**
- Historial completo de sesiones
- Exportación de conversaciones
- Búsqueda en historial
- Guardado automático

## Estructura del Proyecto

```
ChatBot-Prueba/
├── AsistenteVirtualAI.py    # Aplicación principal (interfaz moderna)
├── Chatbot.py               # Motor del chatbot y lógica de IA
├── .env                     # Configuración (API keys)
├── historial/               # Archivos de historial de conversaciones
├── .venv/                   # Entorno virtual de Python
└── README.md               # Este archivo
```

## Requisitos del Sistema

### Software
- Python 3.8+
- PyQt5
- Conexión a Internet (para IA)

### Dependencias Python
```
PyQt5>=5.15.0
google-generativeai>=0.3.0
python-docx>=0.8.11
PyPDF2>=3.0.0
python-dotenv>=1.0.0
```

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/lucas0420Q/ChatBot-Prueba.git
   cd ChatBot-Prueba
   ```

2. **Activar entorno virtual:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar API Key:**
   - Crear archivo `.env` en la raíz del proyecto
   - Agregar: `GEMINI_API_KEY=tu_api_key_aqui`

## Uso

### Ejecutar la Aplicación
```bash
python AsistenteVirtualAI.py
```

### Funcionalidades Principales

1. **Chat Básico:**
   - Escribir mensaje y presionar Enter
   - Shift+Enter para nueva línea

2. **Adjuntar Archivos:**
   - Clic en botón "📎 Adjuntar"
   - Seleccionar archivos PDF, DOCX o TXT
   - Los archivos se procesan automáticamente

3. **Historial:**
   - Clic en "🕒 Historial"
   - Ver conversaciones pasadas
   - Exportar sesiones específicas

4. **Opciones Avanzadas:**
   - "💡 Ayuda & Tips": Mostrar ayuda
   - "⚙️ Avanzado": Guardar sesión, nueva conversación

## Características Técnicas

### Arquitectura
- **Frontend**: PyQt5 con estilos CSS modernos
- **Backend**: Google Gemini 2.0 Flash API
- **Procesamiento**: Hilos separados para respuestas
- **Almacenamiento**: JSON para historial local

### Optimizaciones
- Procesamiento asíncrono de IA
- Gestión eficiente de memoria
- Manejo robusto de errores
- Interfaz responsiva

## Comandos Útiles

### Análisis de Documentos
- "Analiza este documento"
- "Extrae los puntos principales"
- "Genera un resumen"

### Generación de Contenido
- "Crea casos de prueba para..."
- "Genera un manual de usuario"
- "Redacta documentación técnica"

### Preguntas Generales
- Cualquier pregunta sobre el contenido adjuntado
- Solicitudes de explicación o clarificación

## Solución de Problemas

### Error de API Key
- Verificar que el archivo `.env` existe
- Confirmar que la API key es válida
- Revisar conexión a Internet

### Error de Archivos
- Verificar que los archivos no estén corruptos
- Confirmar formato soportado (PDF, DOCX, TXT)
- Revisar permisos de lectura

### Error de Interfaz
- Verificar instalación de PyQt5
- Confirmar resolución mínima (1200x800)
- Reiniciar la aplicación

## Contribuir

1. Fork del repositorio
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Contacto

- **Desarrollador**: Lucas Zaracho
- **GitHub**: [@lucas0420Q](https://github.com/lucas0420Q)
- **Repositorio**: [ChatBot-Prueba](https://github.com/lucas0420Q/ChatBot-Prueba)

---

**⚡ Desarrollado con PyQt5 y Google Gemini 2.0 Flash**
