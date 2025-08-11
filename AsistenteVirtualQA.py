import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                           QFrame, QFileDialog, QMessageBox, QDialog, 
                           QListWidget, QListWidgetItem, QSplitter, QTextBrowser,
                           QScrollArea, QGroupBox, QTabWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor

# Importar el chatbot
from Chatbot import ChatBot

# Importar panel QA avanzado mejorado
from panel_qa_avanzado import PanelQAAvanzado

# Importar librerías para procesar archivos
try:
    from docx import Document
    DOCX_DISPONIBLE = True
except ImportError:
    DOCX_DISPONIBLE = False

try:
    import PyPDF2
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False

class ChatThread(QThread):
    """Hilo para manejar las respuestas del chatbot"""
    respuesta_recibida = pyqtSignal(str)
    error_ocurrido = pyqtSignal(str)
    
    def __init__(self, chatbot, mensaje, archivos_adjuntos=None):
        super().__init__()
        self.chatbot = chatbot
        self.mensaje = mensaje
        self.archivos_adjuntos = archivos_adjuntos or []
        
    def run(self):
        try:
            # Procesar archivos adjuntos si existen
            contexto_archivos = ""
            if self.archivos_adjuntos:
                contexto_archivos = self.procesar_archivos()
            
            # Obtener respuesta del chatbot
            mensaje_completo = f"{contexto_archivos}\n{self.mensaje}" if contexto_archivos else self.mensaje
            respuesta = self.chatbot.procesar_mensaje(mensaje_completo)
            self.respuesta_recibida.emit(respuesta)
            
        except Exception as e:
            self.error_ocurrido.emit(f"Error al procesar mensaje: {str(e)}")
    
    def procesar_archivos(self):
        """Procesa los archivos adjuntos y extrae su contenido"""
        contenido_total = ""
        
        for archivo in self.archivos_adjuntos:
            try:
                if archivo.lower().endswith('.pdf') and PDF_DISPONIBLE:
                    contenido = self.extraer_texto_pdf(archivo)
                elif archivo.lower().endswith(('.docx', '.doc')) and DOCX_DISPONIBLE:
                    contenido = self.extraer_texto_docx(archivo)
                elif archivo.lower().endswith('.txt'):
                    contenido = self.extraer_texto_txt(archivo)
                else:
                    contenido = f"Archivo adjuntado: {os.path.basename(archivo)} (tipo no soportado para extracción automática)"
                
                contenido_total += f"\n\n--- CONTENIDO DE {os.path.basename(archivo)} ---\n{contenido}\n"
                
            except Exception as e:
                contenido_total += f"\n\nError al procesar {os.path.basename(archivo)}: {str(e)}\n"
        
        return contenido_total
    
    def extraer_texto_pdf(self, ruta_archivo):
        """Extrae texto de un archivo PDF"""
        try:
            with open(ruta_archivo, 'rb') as archivo:
                lector = PyPDF2.PdfReader(archivo)
                texto = ""
                for pagina in lector.pages:
                    texto += pagina.extract_text() + "\n"
            return texto
        except Exception as e:
            return f"Error al leer PDF: {str(e)}"
    
    def extraer_texto_docx(self, ruta_archivo):
        """Extrae texto de un archivo DOCX"""
        try:
            doc = Document(ruta_archivo)
            texto = ""
            for parrafo in doc.paragraphs:
                texto += parrafo.text + "\n"
            return texto
        except Exception as e:
            return f"Error al leer DOCX: {str(e)}"
    
    def extraer_texto_txt(self, ruta_archivo):
        """Extrae texto de un archivo TXT"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                return archivo.read()
        except Exception as e:
            return f"Error al leer TXT: {str(e)}"

class HistorialDialog(QDialog):
    """Diálogo para mostrar el historial de conversaciones"""
    def __init__(self, chatbot, parent=None):
        super().__init__(parent)
        self.chatbot = chatbot
        self.setWindowTitle("Historial de Conversaciones")
        self.setGeometry(200, 200, 1000, 700)
        self.setup_ui()
        self.aplicar_estilos()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        titulo = QLabel("Historial de Conversaciones")
        titulo.setObjectName("historialTitulo")
        layout.addWidget(titulo)
        
        # Splitter para dividir lista y contenido
        splitter = QSplitter(Qt.Horizontal)
        
        # Lista de sesiones
        self.lista_sesiones = QListWidget()
        self.lista_sesiones.setObjectName("listaSesiones")
        self.lista_sesiones.itemClicked.connect(self.mostrar_sesion)
        splitter.addWidget(self.lista_sesiones)
        
        # Área de contenido
        self.area_contenido = QTextBrowser()
        self.area_contenido.setObjectName("areaContenido")
        self.area_contenido.setReadOnly(True)
        splitter.addWidget(self.area_contenido)
        
        splitter.setSizes([300, 700])
        layout.addWidget(splitter)
        
        # Estadísticas
        self.label_stats = QLabel()
        self.label_stats.setObjectName("statsLabel")
        layout.addWidget(self.label_stats)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        btn_exportar = QPushButton("Exportar Todo")
        btn_exportar.setObjectName("botonHistorial")
        btn_exportar.clicked.connect(self.exportar_historial_completo)
        
        btn_exportar_sesion = QPushButton("Exportar Sesión")
        btn_exportar_sesion.setObjectName("botonHistorial")
        btn_exportar_sesion.clicked.connect(self.exportar_sesion_actual)
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setObjectName("botonHistorial")
        btn_cerrar.clicked.connect(self.close)
        
        botones_layout.addWidget(btn_exportar)
        botones_layout.addWidget(btn_exportar_sesion)
        botones_layout.addStretch()
        botones_layout.addWidget(btn_cerrar)
        
        layout.addLayout(botones_layout)
        
        # Cargar sesiones
        self.cargar_sesiones()
        self.actualizar_estadisticas()
    
    def cargar_sesiones(self):
        """Carga las sesiones del historial"""
        try:
            sesiones = self.chatbot.cargar_historial_sesiones()
            for sesion in sesiones:
                archivo = sesion['archivo']
                fecha_str = archivo.replace('.json', '').replace('conversacion_', '')
                try:
                    fecha_obj = datetime.strptime(fecha_str, '%Y%m%d_%H%M%S')
                    fecha_legible = fecha_obj.strftime('%d/%m/%Y %H:%M:%S')
                except:
                    fecha_legible = fecha_str
                
                item = QListWidgetItem(f"Sesión: {fecha_legible}")
                item.setData(Qt.UserRole, sesion)
                self.lista_sesiones.addItem(item)
        except Exception as e:
            self.area_contenido.setText(f"Error al cargar historial: {str(e)}")
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas del historial"""
        try:
            stats = self.chatbot.obtener_estadisticas_historial()
            if stats:
                texto_stats = f"Total: {stats['total_sesiones']} sesiones, {stats['total_conversaciones']} mensajes"
                self.label_stats.setText(texto_stats)
            else:
                self.label_stats.setText("No hay estadísticas disponibles")
        except Exception as e:
            self.label_stats.setText(f"Error en estadísticas: {str(e)}")
    
    def mostrar_sesion(self, item):
        """Muestra el contenido de una sesión"""
        sesion_data = item.data(Qt.UserRole)
        try:
            if sesion_data and 'datos' in sesion_data:
                datos = sesion_data['datos']
                contenido_html = self.generar_html_sesion(datos)
                self.area_contenido.setHtml(contenido_html)
            else:
                self.area_contenido.setText("No se pudo cargar la sesión")
        except Exception as e:
            self.area_contenido.setText(f"Error al cargar sesión: {str(e)}")
    
    def generar_html_sesion(self, sesion):
        """Genera HTML formateado para mostrar una sesión"""
        fecha_inicio = sesion.get('inicio', 'Fecha desconocida')
        try:
            fecha_obj = datetime.fromisoformat(fecha_inicio)
            fecha_legible = fecha_obj.strftime('%d de %B de %Y a las %H:%M:%S')
        except:
            fecha_legible = fecha_inicio
        
        html = f"""
        <div style='font-family: Segoe UI; color: #ffffff; background-color: #141F3C; padding: 20px; border-radius: 15px;'>
            <h2 style='color: #4C5BFF; margin-top: 0;'>Sesión del {fecha_legible}</h2>
            <p style='color: #94A3B8;'>Total de mensajes: {len(sesion['conversaciones'])}</p>
            <hr style='border: 1px solid #4C5BFF; margin: 20px 0;'>
        """
        
        for conv in sesion['conversaciones']:
            timestamp = conv.get('timestamp', 'Sin hora')
            try:
                ts_obj = datetime.fromisoformat(timestamp)
                hora = ts_obj.strftime('%H:%M')
            except:
                hora = timestamp
            
            usuario = conv.get('usuario', 'Usuario')
            bot = conv.get('bot', 'Bot')
            
            # Mensaje del usuario - alineado a la derecha y en negrita con flexbox
            html += f"""
            <div style='width: 100%; display: flex; justify-content: flex-end; margin: 15px 0;'>
                <div style='background: linear-gradient(135deg, #4C5BFF, #6366F1); 
                            color: #ffffff; padding: 15px; border-radius: 15px 15px 5px 15px; 
                            max-width: 70%; text-align: left;'>
                    <p style='margin: 0; font-size: 12px; color: rgba(255,255,255,0.8); font-weight: bold;'>[{hora}] 👤 Tú:</p>
                    <p style='margin: 5px 0 0 0; color: #ffffff; line-height: 1.4; font-weight: bold;'>{usuario}</p>
                </div>
            </div>
            """
            
            # Mensaje del bot - alineado a la izquierda con flexbox
            html += f"""
            <div style='width: 100%; display: flex; justify-content: flex-start; margin: 15px 0;'>
                <div style='background: #2D3748; color: #ffffff; 
                            padding: 15px; border-radius: 15px 15px 15px 5px; max-width: 75%;'>
                    <p style='margin: 0; font-size: 12px; color: #94A3B8;'>[{hora}] 🤖 Bot:</p>
                    <p style='margin: 5px 0 0 0; color: #ffffff; line-height: 1.4;'>{bot}</p>
                </div>
            </div>
            """
        
        return html + "</div>"
    
    def exportar_historial_completo(self):
        """Exporta el historial completo"""
        QMessageBox.information(self, "Función en desarrollo", "Esta función estará disponible próximamente")
    
    def exportar_sesion_actual(self):
        """Exporta la sesión seleccionada"""
        QMessageBox.information(self, "Función en desarrollo", "Esta función estará disponible próximamente")
    
    def aplicar_estilos(self):
        """Aplicar estilos al diálogo"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #0B1D4A, stop: 1 #1F2A56);
            }
            #historialTitulo {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
            }
            #statsLabel {
                color: #94A3B8;
                font-size: 14px;
                padding: 10px 20px;
            }
            #listaSesiones {
                background: #141F3C;
                color: #ffffff;
                border: 2px solid #4C5BFF;
                border-radius: 15px;
                font-size: 14px;
                padding: 10px;
            }
            #listaSesiones::item {
                padding: 15px;
                border-bottom: 1px solid #4C5BFF;
                border-radius: 8px;
                margin: 3px;
            }
            #listaSesiones::item:selected {
                background: #4C5BFF;
            }
            #listaSesiones::item:hover {
                background: #1E3058;
            }
            #areaContenido {
                background: #141F3C;
                color: #ffffff;
                border: 2px solid #4C5BFF;
                border-radius: 15px;
                font-size: 14px;
                padding: 15px;
            }
            #botonHistorial {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #4C5BFF, stop: 1 #5A47F3);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 15px 25px;
                min-width: 140px;
            }
            #botonHistorial:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #6366F1, stop: 1 #7C3AED);
            }
        """)

class PanelAyuda(QDialog):
    """Panel de ayuda y tips del sistema"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("💡 Ayuda & Tips - Asistente Virtual QA")
        self.setGeometry(200, 200, 900, 700)
        self.setMinimumSize(800, 650)
        self.configurar_ui()
        self.aplicar_estilos()
        
    def configurar_ui(self):
        """Configurar la interfaz del panel de ayuda"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # ENCABEZADO
        header_layout = QVBoxLayout()
        
        titulo = QLabel("💡 AYUDA & TIPS")
        titulo.setObjectName("tituloAyuda")
        titulo.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(titulo)
        
        subtitulo = QLabel("Guía completa para usar el Asistente Virtual QA de manera efectiva")
        subtitulo.setObjectName("subtituloAyuda")
        subtitulo.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitulo)
        
        layout.addLayout(header_layout)
        
        # TABS DE AYUDA
        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabsAyuda")
        
        # Tab 1: Primeros Pasos
        tab_inicio = QWidget()
        self.configurar_tab_inicio(tab_inicio)
        self.tabs.addTab(tab_inicio, "🚀 Primeros Pasos")
        
        # Tab 2: Funciones Principales
        tab_funciones = QWidget()
        self.configurar_tab_funciones(tab_funciones)
        self.tabs.addTab(tab_funciones, "⚡ Funciones")
        
        # Tab 3: Panel QA Avanzado
        tab_qa = QWidget()
        self.configurar_tab_qa(tab_qa)
        self.tabs.addTab(tab_qa, "🎯 Panel QA")
        
        # Tab 4: Tips y Trucos
        tab_tips = QWidget()
        self.configurar_tab_tips(tab_tips)
        self.tabs.addTab(tab_tips, "💎 Tips")
        
        # Tab 5: Solución de Problemas
        tab_problemas = QWidget()
        self.configurar_tab_problemas(tab_problemas)
        self.tabs.addTab(tab_problemas, "🔧 Soluciones")
        
        layout.addWidget(self.tabs)
        
        # BOTONES INFERIORES
        botones_layout = QHBoxLayout()
        
        btn_cerrar = QPushButton("❌ Cerrar")
        btn_cerrar.setObjectName("botonCerrarAyuda")
        btn_cerrar.clicked.connect(self.close)
        
        botones_layout.addStretch()
        botones_layout.addWidget(btn_cerrar)
        
        layout.addLayout(botones_layout)
    
    def crear_seccion_contenido(self, parent, contenido_html):
        """Crear sección de contenido con scroll"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollAyuda")
        
        contenido_widget = QLabel()
        contenido_widget.setWordWrap(True)
        contenido_widget.setTextFormat(Qt.RichText)
        contenido_widget.setText(contenido_html)
        contenido_widget.setObjectName("contenidoAyuda")
        contenido_widget.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(contenido_widget)
        
        layout = QVBoxLayout(parent)
        layout.addWidget(scroll)
    
    def configurar_tab_inicio(self, tab):
        """Tab de primeros pasos"""
        contenido = """
        <h2 style='color: #4C5BFF; margin-top: 0;'>🚀 Bienvenido al Asistente Virtual QA</h2>
        
        <p style='font-size: 16px; color: #1F2937; line-height: 1.6;'>
        Este asistente está diseñado para ayudarte en todas las tareas relacionadas con <strong>Quality Assurance</strong> y <strong>Testing de Software</strong>.
        </p>
        
        <h3 style='color: #6366F1;'>📋 ¿Qué puedes hacer?</h3>
        <ul style='color: #1F2937; line-height: 1.8;'>
            <li><strong>Generar casos de prueba</strong> para cualquier tipo de aplicación</li>
            <li><strong>Crear documentación QA</strong> como planes de prueba, RTM, etc.</li>
            <li><strong>Desarrollar scripts de automatización</strong> en Selenium, Cypress, etc.</li>
            <li><strong>Analizar requisitos</strong> adjuntando documentos PDF/DOCX</li>
            <li><strong>Obtener mejores prácticas</strong> de testing y QA</li>
            <li><strong>Generar reportes profesionales</strong> de testing</li>
        </ul>
        
        <h3 style='color: #6366F1;'>🎯 Cómo empezar</h3>
        <ol style='color: #1F2937; line-height: 1.8;'>
            <li>Escribe tu pregunta en el campo de texto</li>
            <li>Usa <strong>Shift+Enter</strong> para nueva línea, <strong>Enter</strong> para enviar</li>
            <li>Explora el <strong>Panel QA Avanzado</strong> para herramientas especializadas</li>
            <li>Adjunta documentos para análisis automático</li>
            <li>Revisa el historial para ver conversaciones anteriores</li>
        </ol>
        """
        self.crear_seccion_contenido(tab, contenido)
    
    def configurar_tab_funciones(self, tab):
        """Tab de funciones principales"""
        contenido = """
        <h2 style='color: #4C5BFF; margin-top: 0;'>⚡ Funciones Principales</h2>
        
        <div style='background: #F3F4F6; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #4C5BFF;'>
            <h3 style='color: #DC2626; margin-top: 0;'>💬 Chat Inteligente</h3>
            <p style='color: #1F2937;'>Haz preguntas en lenguaje natural sobre testing, QA, automatización, etc.</p>
            <strong style='color: #4C5BFF;'>Ejemplos:</strong>
            <ul style='color: #374151;'>
                <li>"Genera casos de prueba para una API de login"</li>
                <li>"Crea un plan de pruebas para una app móvil"</li>
                <li>"Explícame cómo hacer testing de performance"</li>
            </ul>
        </div>
        
        <div style='background: #F3F4F6; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #4C5BFF;'>
            <h3 style='color: #DC2626; margin-top: 0;'>📎 Análisis de Documentos</h3>
            <p style='color: #1F2937;'>Adjunta archivos PDF, DOCX para análisis automático de requisitos.</p>
            <strong style='color: #4C5BFF;'>Funcionalidades:</strong>
            <ul style='color: #374151;'>
                <li>Extracción automática de requisitos</li>
                <li>Generación de casos de prueba basados en documentos</li>
                <li>Análisis de gap de testing</li>
            </ul>
        </div>
        
        <div style='background: #F3F4F6; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #4C5BFF;'>
            <h3 style='color: #DC2626; margin-top: 0;'>🎯 Panel QA Avanzado</h3>
            <p style='color: #1F2937;'>Herramientas especializadas categorizadas por tipo de testing.</p>
            <strong style='color: #4C5BFF;'>Incluye:</strong>
            <ul style='color: #374151;'>
                <li>API Testing & Automation</li>
                <li>Test Cases & Documentation</li>
                <li>Security & Performance Testing</li>
                <li>Mobile & Accessibility Testing</li>
                <li>CI/CD Integration</li>
                <li>Reports & Analytics</li>
            </ul>
        </div>
        
        <div style='background: #F3F4F6; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #4C5BFF;'>
            <h3 style='color: #DC2626; margin-top: 0;'>📚 Historial</h3>
            <p style='color: #1F2937;'>Todas las conversaciones se guardan automáticamente.</p>
            <strong style='color: #4C5BFF;'>Características:</strong>
            <ul style='color: #374151;'>
                <li>Búsqueda en conversaciones anteriores</li>
                <li>Estadísticas de uso</li>
                <li>Exportación de sesiones</li>
            </ul>
        </div>
        """
        self.crear_seccion_contenido(tab, contenido)
    
    def configurar_tab_qa(self, tab):
        """Tab del panel QA"""
        contenido = """
        <h2 style='color: #4C5BFF; margin-top: 0;'>🎯 Panel QA Avanzado</h2>
        
        <p style='font-size: 16px; color: #1F2937; line-height: 1.6;'>
        El Panel QA Avanzado contiene herramientas especializadas organizadas en categorías para profesionales de QA.
        </p>
        
        <h3 style='color: #6366F1;'>📋 Categorías Disponibles</h3>
        
        <div style='background: #F3F4F6; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #4C5BFF;'>
            <h4 style='color: #DC2626; margin-top: 0;'>🔌 API Testing</h4>
            <p style='color: #1F2937;'>Casos de prueba REST, colecciones Postman, scripts cURL, tests de performance y seguridad API.</p>
        </div>
        
        <div style='background: #F3F4F6; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #6366F1;'>
            <h4 style='color: #DC2626; margin-top: 0;'>📋 Test Cases</h4>
            <p style='color: #1F2937;'>Planes de prueba IEEE 829, casos BDD, matriz de trazabilidad, checklists pre-deploy.</p>
        </div>
        
        <div style='background: #F3F4F6; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #7C3AED;'>
            <h4 style='color: #DC2626; margin-top: 0;'>🤖 Automation</h4>
            <p style='color: #1F2937;'>Scripts Selenium, Cypress, Playwright, frameworks TestNG/PyTest, Page Object Model.</p>
        </div>
        
        <div style='background: #F3F4F6; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #EF4444;'>
            <h4 style='color: #DC2626; margin-top: 0;'>🔒 Security & Performance</h4>
            <p style='color: #1F2937;'>Tests JMeter/K6, análisis vulnerabilidades OWASP, penetration testing, monitoreo.</p>
        </div>
        
        <div style='background: #F3F4F6; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #10B981;'>
            <h4 style='color: #DC2626; margin-top: 0;'>📱 Mobile & Accessibility</h4>
            <p style='color: #1F2937;'>Automation Appium, auditorías WCAG, tests responsive, usabilidad UX/UI.</p>
        </div>
        
        <div style='background: #F3F4F6; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #F59E0B;'>
            <h4 style='color: #DC2626; margin-top: 0;'>⚙️ CI/CD</h4>
            <p style='color: #1F2937;'>Pipelines Jenkins, Docker testing, tests en cloud, Git hooks, quality gates.</p>
        </div>
        
        <div style='background: #F3F4F6; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 5px solid #8B5CF6;'>
            <h4 style='color: #DC2626; margin-top: 0;'>📊 Reports</h4>
            <p style='color: #1F2937;'>Dashboards QA, reportes Allure, análisis de tendencias, ROI testing.</p>
        </div>
        
        <h3 style='color: #6366F1;'>🚀 Cómo usar las herramientas</h3>
        <ol style='color: #1F2937; line-height: 1.8;'>
            <li>Haz clic en <strong>"Panel QA Avanzado"</strong></li>
            <li>Selecciona la categoría apropiada</li>
            <li>Haz clic en la herramienta deseada</li>
            <li>El prompt se colocará en el campo de texto</li>
            <li>Presiona Enter para obtener la respuesta profesional</li>
        </ol>
        """
        self.crear_seccion_contenido(tab, contenido)
    
    def configurar_tab_tips(self, tab):
        """Tab de tips y trucos"""
        contenido = """
        <h2 style='color: #4C5BFF; margin-top: 0;'>💎 Tips y Trucos Avanzados</h2>
        
        <div style='background: #FEF3C7; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #F59E0B;'>
            <h3 style='color: #92400E; margin-top: 0;'>⚡ Prompts Efectivos</h3>
            <ul style='color: #1F2937; line-height: 1.8;'>
                <li><strong>Sea específico:</strong> "Genera casos de prueba para API REST de autenticación con JWT"</li>
                <li><strong>Incluya contexto:</strong> "Para una app móvil de e-commerce en Android"</li>
                <li><strong>Mencione tecnologías:</strong> "Usando Selenium WebDriver con Java y TestNG"</li>
                <li><strong>Especifique formato:</strong> "En formato Gherkin para Cucumber"</li>
            </ul>
        </div>
        
        <div style='background: #D1FAE5; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #10B981;'>
            <h3 style='color: #065F46; margin-top: 0;'>📋 Mejores Prácticas</h3>
            <ul style='color: #1F2937; line-height: 1.8;'>
                <li><strong>Adjunte documentos:</strong> Suba PDFs de requisitos para análisis automático</li>
                <li><strong>Use el historial:</strong> Revise conversaciones anteriores para referencia</li>
                <li><strong>Combine herramientas:</strong> Use múltiples herramientas del panel QA</li>
                <li><strong>Itere:</strong> Refine los resultados con preguntas de seguimiento</li>
            </ul>
        </div>
        
        <div style='background: #EDE9FE; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #8B5CF6;'>
            <h3 style='color: #581C87; margin-top: 0;'>🎯 Casos de Uso Comunes</h3>
            <ul style='color: #1F2937; line-height: 1.8;'>
                <li><strong>Testing de API:</strong> "Genera colección Postman completa para API REST"</li>
                <li><strong>Automation:</strong> "Crea framework Selenium con Page Object Model"</li>
                <li><strong>Performance:</strong> "Diseña test plan JMeter para 1000 usuarios concurrentes"</li>
                <li><strong>Security:</strong> "Implementa checklist OWASP Top 10 para web app"</li>
                <li><strong>Mobile:</strong> "Crea strategy testing para app iOS/Android"</li>
            </ul>
        </div>
        
        <div style='background: #FEE2E2; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #EF4444;'>
            <h3 style='color: #991B1B; margin-top: 0;'>⌨️ Atajos de Teclado</h3>
            <ul style='color: #1F2937; line-height: 1.8;'>
                <li><strong>Shift + Enter:</strong> Nueva línea sin enviar</li>
                <li><strong>Enter:</strong> Enviar mensaje</li>
                <li><strong>Ctrl + N:</strong> Nueva conversación</li>
                <li><strong>Ctrl + H:</strong> Abrir historial</li>
            </ul>
        </div>
        """
        self.crear_seccion_contenido(tab, contenido)
    
    def configurar_tab_problemas(self, tab):
        """Tab de solución de problemas"""
        contenido = """
        <h2 style='color: #4C5BFF; margin-top: 0;'>🔧 Solución de Problemas</h2>
        
        <div style='background: #FEE2E2; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #EF4444;'>
            <h3 style='color: #991B1B; margin-top: 0;'>❗ Problemas Comunes</h3>
            
            <h4 style='color: #DC2626;'>El asistente no responde</h4>
            <ul style='color: #1F2937;'>
                <li>Verifique su conexión a internet</li>
                <li>Intente con una pregunta más simple</li>
                <li>Reinicie la aplicación si es necesario</li>
            </ul>
            
            <h4 style='color: #DC2626;'>No se pueden adjuntar archivos</h4>
            <ul style='color: #1F2937;'>
                <li>Asegúrese de que el archivo sea PDF o DOCX</li>
                <li>Verifique que el archivo no esté corrupto</li>
                <li>El tamaño máximo recomendado es 10MB</li>
            </ul>
            
            <h4 style='color: #DC2626;'>Panel QA no se abre</h4>
            <ul style='color: #1F2937;'>
                <li>Cierre cualquier ventana modal abierta</li>
                <li>Reinicie la aplicación</li>
                <li>Verifique que no haya errores en la consola</li>
            </ul>
        </div>
        
        <div style='background: #D1FAE5; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #10B981;'>
            <h3 style='color: #065F46; margin-top: 0;'>✅ Consejos de Rendimiento</h3>
            <ul style='color: #1F2937; line-height: 1.8;'>
                <li><strong>Consultas específicas:</strong> Preguntas más específicas obtienen mejores respuestas</li>
                <li><strong>Contexto relevante:</strong> Proporcione toda la información necesaria</li>
                <li><strong>Uso de herramientas:</strong> Use las herramientas del panel QA para resultados optimizados</li>
                <li><strong>Formato claro:</strong> Organice sus preguntas de manera estructurada</li>
            </ul>
        </div>
        
        <div style='background: #FEF3C7; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #F59E0B;'>
            <h3 style='color: #92400E; margin-top: 0;'>⚙️ Configuración Recomendada</h3>
            <ul style='color: #1F2937; line-height: 1.8;'>
                <li><strong>Pantalla:</strong> Resolución mínima 1200x800 para mejor experiencia</li>
                <li><strong>Sistema:</strong> Windows 10/11, 8GB RAM recomendado</li>
                <li><strong>Internet:</strong> Conexión estable para consultas a la IA</li>
                <li><strong>Archivos:</strong> Mantenga documentos organizados para fácil acceso</li>
            </ul>
        </div>
        
        <div style='background: #EDE9FE; padding: 20px; border-radius: 15px; margin: 15px 0; border: 2px solid #8B5CF6;'>
            <h3 style='color: #581C87; margin-top: 0;'>📞 Soporte</h3>
            <p style='color: #1F2937; line-height: 1.6;'>
            Si experimenta problemas persistentes:
            </p>
            <ul style='color: #1F2937; line-height: 1.8;'>
                <li>Revise el historial para ver si el problema se repite</li>
                <li>Anote el mensaje de error exacto si aparece</li>
                <li>Intente reproducir el problema paso a paso</li>
                <li>Documente las acciones que llevaron al problema</li>
            </ul>
        </div>
        """
        self.crear_seccion_contenido(tab, contenido)
    
    def aplicar_estilos(self):
        """Aplicar estilos CSS al panel de ayuda"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #0B1D4A, stop: 1 #1F2A56);
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            #tituloAyuda {
                font-size: 32px;
                font-weight: bold;
                color: #FFFFFF;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #4C5BFF, stop: 1 #6366F1);
                padding: 25px;
                border-radius: 20px;
                border: 3px solid #FFFFFF;
                margin: 15px;
            }
            
            #subtituloAyuda {
                font-size: 18px;
                color: #E2E8F0;
                background: #1E3058;
                padding: 18px;
                border-radius: 12px;
                border: 2px solid #4C5BFF;
                margin: 10px;
            }
            
            #tabsAyuda::pane {
                border: 3px solid #4C5BFF;
                border-radius: 20px;
                background: #141F3C;
                padding: 20px;
                margin-top: 15px;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #1E3058, stop: 1 #2D4A7B);
                color: #FFFFFF;
                padding: 20px 30px;
                margin: 4px;
                border-radius: 15px;
                font-weight: bold;
                font-size: 15px;
                border: 2px solid #4C5BFF;
                min-width: 140px;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #4C5BFF, stop: 1 #6366F1);
                border: 3px solid #FFFFFF;
                color: #FFFFFF;
                font-weight: bold;
            }
            
            QTabBar::tab:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #2D4A7B, stop: 1 #3D5998);
                border: 2px solid #FFD700;
            }
            
            #scrollAyuda {
                border: 2px solid #4C5BFF;
                border-radius: 15px;
                background: #FFFFFF;
                padding: 10px;
            }
            
            #contenidoAyuda {
                background: #FFFFFF;
                color: #1F2937;
                padding: 20px;
                font-size: 16px;
                line-height: 1.7;
                font-weight: 500;
            }
            
            #botonCerrarAyuda {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #DC2626, stop: 1 #EF4444);
                color: #FFFFFF;
                border: 2px solid #FFFFFF;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                padding: 18px 30px;
                min-width: 120px;
            }
            
            #botonCerrarAyuda:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #EF4444, stop: 1 #F87171);
                border: 2px solid #FFD700;
            }
            
            QScrollBar:vertical {
                background: #1B243A;
                width: 18px;
                border-radius: 9px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #4C5BFF;
                border-radius: 9px;
                min-height: 40px;
                margin: 3px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #6366F1;
            }
        """)

class AsistenteVirtualModernUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asistente Virtual AI - Interfaz Moderna QA")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1200, 800)
        
        # Inicializar el chatbot
        self.chatbot = ChatBot("Asistente Virtual")
        
        # Lista de archivos adjuntos
        self.archivos_adjuntos = []
        
        # Contador de mensajes
        self.contador_mensajes = 0
        
        # Configurar ventana principal
        self.setup_ui()
        self.apply_modern_styles()
        
        # Mensaje de bienvenida inicial
        self.mostrar_mensaje_bienvenida()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario moderna"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # ENCABEZADO SUPERIOR
        header_widget = self.create_modern_header()
        main_layout.addWidget(header_widget)
        
        # CAJA DE CONVERSACIÓN
        chat_widget = self.create_modern_chat()
        main_layout.addWidget(chat_widget, 1)  # Expandible
        
        # ÁREA DE ENTRADA DE MENSAJE
        input_widget = self.create_modern_input()
        main_layout.addWidget(input_widget)
        
        # BOTONES INFERIORES
        buttons_widget = self.create_modern_buttons()
        main_layout.addWidget(buttons_widget)
        
        # PIE DE PÁGINA
        footer_widget = self.create_modern_footer()
        main_layout.addWidget(footer_widget)
        
    def create_modern_header(self):
        """Crear el encabezado moderno"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 20, 25, 20)
        header_layout.setSpacing(20)
        
        # Icono del bot (circular)
        bot_icon = QLabel("🤖")
        bot_icon.setObjectName("botIcon")
        bot_icon.setAlignment(Qt.AlignCenter)
        bot_icon.setFixedSize(70, 70)
        
        # Contenedor de títulos
        titles_layout = QVBoxLayout()
        titles_layout.setSpacing(5)
        
        # Título principal
        title = QLabel("Asistente Virtual AI - QA Professional")
        title.setObjectName("mainTitle")
        titles_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Herramientas especializadas para Quality Assurance y Testing")
        subtitle.setObjectName("subtitle")
        titles_layout.addWidget(subtitle)
        
        # Agregar elementos al header
        header_layout.addWidget(bot_icon)
        header_layout.addLayout(titles_layout)
        header_layout.addStretch()
        
        return header_frame
        
    def create_modern_chat(self):
        """Crear la caja de conversación moderna"""
        chat_frame = QFrame()
        chat_frame.setObjectName("chatFrame")
        
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setContentsMargins(25, 25, 25, 25)
        
        # Área de texto para el chat
        self.area_chat = QTextBrowser()
        self.area_chat.setObjectName("areaChat")
        self.area_chat.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.area_chat.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.area_chat.setOpenExternalLinks(True)
        self.area_chat.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        
        # Configurar para renderizar HTML y Markdown correctamente
        self.area_chat.setAcceptRichText(True)
        
        chat_layout.addWidget(self.area_chat)
        
        return chat_frame
    
    def create_modern_input(self):
        """Crear el área de entrada moderna estable"""
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(25, 20, 25, 20)
        input_layout.setSpacing(15)
        
        # Campo de texto estable con altura fija
        self.entrada_texto = QTextEdit()
        self.entrada_texto.setObjectName("entradaTexto")
        self.entrada_texto.setPlaceholderText("Escribe tu mensaje aquí... (Enter para enviar, Shift+Enter para nueva línea)")
        self.entrada_texto.setFixedHeight(100)  # Altura fija más grande
        
        # Configurar scrollbar y wrap
        self.entrada_texto.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.entrada_texto.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.entrada_texto.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Configurar eventos de teclado
        self.entrada_texto.keyPressEvent = self.manejar_teclas
        
        # Botones
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Botón adjuntar
        self.attach_btn = QPushButton("📎 Adjuntar")
        self.attach_btn.setObjectName("attachButton")
        self.attach_btn.setFixedHeight(35)
        self.attach_btn.clicked.connect(self.adjuntar_archivo)
        
        # Botón enviar
        self.send_btn = QPushButton("➤ Enviar")
        self.send_btn.setObjectName("sendButton")
        self.send_btn.setFixedHeight(35)
        self.send_btn.clicked.connect(self.enviar_mensaje)
        
        buttons_layout.addWidget(self.attach_btn)
        buttons_layout.addWidget(self.send_btn)
        
        input_layout.addWidget(self.entrada_texto)
        input_layout.addLayout(buttons_layout)
        
        return input_frame
    
    def create_modern_buttons(self):
        """Crear los botones inferiores modernos"""
        buttons_frame = QFrame()
        buttons_frame.setObjectName("buttonsFrame")
        
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(25, 15, 25, 15)
        buttons_layout.setSpacing(20)
        
        # Botón Ayuda & Tips
        help_btn = QPushButton("💡 Ayuda & Tips")
        help_btn.setObjectName("helpButton")
        help_btn.setMinimumHeight(45)
        help_btn.clicked.connect(self.mostrar_ayuda)
        
        # Botón Historial
        history_btn = QPushButton("🕒 Historial")
        history_btn.setObjectName("historyButton")
        history_btn.setMinimumHeight(45)
        history_btn.clicked.connect(self.abrir_historial)
        
        # Botón Avanzado QA
        advanced_btn = QPushButton("⚙️ Panel QA Avanzado")
        advanced_btn.setObjectName("advancedButton")
        advanced_btn.setMinimumHeight(45)
        advanced_btn.clicked.connect(self.opciones_avanzadas)
        
        buttons_layout.addWidget(help_btn)
        buttons_layout.addWidget(history_btn)
        buttons_layout.addWidget(advanced_btn)
        
        return buttons_frame
        
    def create_modern_footer(self):
        """Crear el pie de página moderno"""
        footer_frame = QFrame()
        footer_frame.setObjectName("footerFrame")
        
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(25, 10, 25, 10)
        
        # Texto de estado
        self.status_label = QLabel("0 mensajes en esta sesión")
        self.status_label.setObjectName("statusLabel")
        
        footer_layout.addWidget(self.status_label)
        footer_layout.addStretch()
        
        return footer_frame
    
    def mostrar_mensaje_bienvenida(self):
        """Mostrar mensaje de bienvenida inicial"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Usar método separado para generar HTML
        html_bienvenida = self.generar_html_mensaje_bienvenida(timestamp)
        
        self.area_chat.setHtml(html_bienvenida)
        self.contador_mensajes += 1
        self.actualizar_status()
    
    def generar_html_mensaje_usuario(self, mensaje, timestamp):
        """Genera el HTML para un mensaje del usuario"""
        return f"""
        <div style="width: 100%; margin: 15px 0; font-family: 'Segoe UI', Arial, sans-serif; clear: both;">
            <div style="float: left; background: linear-gradient(135deg, #4C5BFF, #6366F1); 
                        color: #ffffff; padding: 15px 20px; border-radius: 20px 20px 20px 8px; 
                        box-shadow: 0 3px 12px rgba(76, 91, 255, 0.3); max-width: 70%; 
                        text-align: left; margin-left: 10px;">
                <div style="font-size: 16px; color: rgba(255,255,255,0.8); margin-bottom: 8px; 
                           font-weight: bold;">
                    [{timestamp}] 👤 Tú
                </div>
                <div style="font-size: 19px; line-height: 1.4; font-weight: bold; color: #ffffff;">
                    {mensaje}
                </div>
            </div>
            <div style="clear: both;"></div>
        </div>
        """
    
    def generar_html_mensaje_bot(self, mensaje, timestamp):
        """Genera el HTML para un mensaje del bot"""
        # Convertir markdown básico a HTML
        mensaje_html = self.convertir_markdown_a_html(mensaje)
        
        return f"""
        <div style="width: 100%; margin: 8px 0; font-family: 'Segoe UI', Arial, sans-serif; clear: both;">
            <div style="float: left; background: linear-gradient(135deg, #1E3058, #2D3748); 
                        color: #ffffff; padding: 15px 20px; border-radius: 20px 20px 20px 8px; 
                        box-shadow: 0 3px 12px rgba(0,0,0,0.15); max-width: 75%; 
                        text-align: left; margin-left: 10px;">
                <div style="font-size: 14px; color: #94A3B8; margin-bottom: 8px;">
                    [{timestamp}] 🤖
                </div>
                <div style="font-size: 17px; line-height: 1.5; color: #ffffff;">
                    {mensaje_html}
                </div>
            </div>
            <div style="clear: both;"></div>
        </div>
        """
    
    def convertir_markdown_a_html(self, texto):
        """Convierte markdown básico a HTML"""
        import re
        
        # Convertir **negrita** a <strong>
        texto = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', texto)
        
        # Convertir títulos # a HTML
        texto = re.sub(r'^# (.*?)$', r'<h1 style="color: #4C5BFF; font-size: 20px; margin: 10px 0;">\1</h1>', texto, flags=re.MULTILINE)
        texto = re.sub(r'^## (.*?)$', r'<h2 style="color: #6366F1; font-size: 18px; margin: 8px 0;">\1</h2>', texto, flags=re.MULTILINE)
        texto = re.sub(r'^### (.*?)$', r'<h3 style="color: #7C3AED; font-size: 16px; margin: 6px 0;">\1</h3>', texto, flags=re.MULTILINE)
        
        # Convertir saltos de línea
        texto = texto.replace('\n', '<br>')
        
        # Convertir listas con -
        texto = re.sub(r'^- (.*?)$', r'<li style="margin: 4px 0;">\1</li>', texto, flags=re.MULTILINE)
        
        # Convertir emojis de números en encabezados
        texto = re.sub(r'(\d+️⃣)', r'<span style="color: #FFD700;">\1</span>', texto)
        
        return texto
    
    def generar_html_mensaje_bienvenida(self, timestamp):
        """Genera el HTML para el mensaje de bienvenida"""
        return f"""
        <div style="width: 100%; padding: 20px; font-family: 'Segoe UI', Arial, sans-serif; clear: both;">
            <div style="float: left; background: linear-gradient(135deg, #1E3058, #2D3748); 
                        color: #ffffff; padding: 20px; border-radius: 20px; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2); max-width: 80%; 
                        margin-left: 10px;">
                <div style="font-size: 14px; color: #94A3B8; margin-bottom: 12px;">
                    [{timestamp}] 🤖
                </div>
                <div style="font-size: 18px; line-height: 1.5; margin-bottom: 15px;">
                    ¡Hola! Soy tu Asistente Virtual especializado en QA y Testing. ¿En qué puedo ayudarte hoy?
                </div>
                <div style="font-size: 16px; line-height: 1.4; color: #E2E8F0;">
                    ✦ Genero casos de prueba, planes de testing y documentación QA profesional<br>
                    ✦ Analizo documentos y genero estrategias de testing<br>
                    ✦ Creo scripts de automatización y checklists especializados<br>
                    ✦ Usa el Panel QA Avanzado para acceder a herramientas especializadas
                </div>
            </div>
            <div style="clear: both;"></div>
        </div>
        """
        
    def mostrar_mensaje_usuario(self, mensaje):
        """Mostrar mensaje del usuario con diseño moderno alineado a la derecha y en negrita"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Agregar conversación al chatbot
        self.chatbot.guardar_conversacion(mensaje, "")
        
        # Usar método separado para generar HTML
        html_mensaje = self.generar_html_mensaje_usuario(mensaje, timestamp)
        
        self.area_chat.append(html_mensaje)
        self.scroll_to_bottom()
        self.contador_mensajes += 1
        self.actualizar_status()
    
    def mostrar_mensaje_bot(self, mensaje):
        """Mostrar mensaje del bot con diseño moderno alineado a la izquierda"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Usar método separado para generar HTML
        html_mensaje = self.generar_html_mensaje_bot(mensaje, timestamp)
        
        self.area_chat.append(html_mensaje)
        self.scroll_to_bottom()
        self.contador_mensajes += 1
        self.actualizar_status()
    
    def actualizar_status(self):
        """Actualizar el estado del pie de página"""
        self.status_label.setText(f"{self.contador_mensajes} mensajes en esta sesión")
    
    def scroll_to_bottom(self):
        """Hacer scroll hacia abajo"""
        scrollbar = self.area_chat.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def manejar_teclas(self, evento):
        """Manejar eventos de teclado"""
        if evento.key() == Qt.Key_Return and not (evento.modifiers() & Qt.ShiftModifier):
            # Enter sin Shift: enviar mensaje
            self.enviar_mensaje()
            evento.accept()
        else:
            # Comportamiento normal (incluyendo Shift+Enter para nueva línea)
            QTextEdit.keyPressEvent(self.entrada_texto, evento)
    
    def enviar_mensaje(self):
        """Enviar mensaje al chatbot"""
        mensaje = self.entrada_texto.toPlainText().strip()
        if not mensaje:
            return
        
        # Guardar referencia del último mensaje para la respuesta
        self._ultimo_mensaje_usuario = mensaje
        
        # Mostrar mensaje del usuario
        self.mostrar_mensaje_usuario(mensaje)
        self.entrada_texto.clear()
        
        # Deshabilitar envío mientras se procesa
        self.send_btn.setEnabled(False)
        self.entrada_texto.setEnabled(False)
        
        # Mostrar mensaje de "escribiendo..."
        self.mostrar_mensaje_bot("✍️ Escribiendo...")
        
        # Crear y ejecutar hilo para respuesta
        self.chat_thread = ChatThread(self.chatbot, mensaje, self.archivos_adjuntos.copy())
        self.chat_thread.respuesta_recibida.connect(self.procesar_respuesta)
        self.chat_thread.error_ocurrido.connect(self.procesar_error)
        self.chat_thread.start()
        
        # Limpiar archivos adjuntos después de enviar
        if self.archivos_adjuntos:
            self.archivos_adjuntos.clear()
    
    def procesar_respuesta(self, respuesta):
        """Procesar respuesta del chatbot"""
        self.remover_mensaje_escribiendo()
        
        # Guardar respuesta en el chatbot
        if hasattr(self, '_ultimo_mensaje_usuario') and self.chatbot.sesion_actual['conversaciones']:
            self.chatbot.sesion_actual['conversaciones'][-1]['respuesta'] = respuesta
        
        # Mostrar respuesta real
        self.mostrar_mensaje_bot(respuesta)
        self.habilitar_envio()
    
    def procesar_error(self, error):
        """Procesar error del chatbot"""
        self.remover_mensaje_escribiendo()
        self.mostrar_mensaje_bot(f"❌ Error: {error}")
        self.habilitar_envio()
    
    def remover_mensaje_escribiendo(self):
        """Remover el mensaje de 'escribiendo...'"""
        contenido_html = self.area_chat.toHtml()
        
        if "✍️ Escribiendo..." in contenido_html:
            cursor = self.area_chat.textCursor()
            cursor.movePosition(QTextCursor.End)
            
            documento = self.area_chat.document()
            bloque = documento.lastBlock()
            while bloque.isValid():
                if "✍️ Escribiendo..." in bloque.text():
                    bloque_inicio = bloque
                    while bloque_inicio.previous().isValid():
                        if "[" in bloque_inicio.previous().text() and "] 🤖" in bloque_inicio.previous().text():
                            bloque_inicio = bloque_inicio.previous()
                            break
                        bloque_inicio = bloque_inicio.previous()
                    
                    cursor.setPosition(bloque_inicio.position())
                    cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
                    cursor.removeSelectedText()
                    break
                bloque = bloque.previous()
    
    def habilitar_envio(self):
        """Rehabilitar el envío de mensajes"""
        self.send_btn.setEnabled(True)
        self.entrada_texto.setEnabled(True)
        self.entrada_texto.setFocus()
    
    def adjuntar_archivo(self):
        """Adjuntar archivos al chat"""
        archivos, _ = QFileDialog.getOpenFileNames(
            self, 
            "Seleccionar archivos", 
            "", 
            "Documentos (*.txt *.pdf *.docx);;Imágenes (*.png *.jpg *.jpeg);;Todos (*.*)"
        )
        
        if archivos:
            self.archivos_adjuntos.extend(archivos)
            nombres = [os.path.basename(archivo) for archivo in archivos]
            mensaje = f"📎 {len(archivos)} archivo(s) adjuntado(s): {', '.join(nombres)}"
            self.mostrar_mensaje_bot(mensaje)
    
    def abrir_historial(self):
        """Abrir ventana de historial"""
        dialog = HistorialDialog(self.chatbot, self)
        dialog.exec_()
    
    def mostrar_ayuda(self):
        """Mostrar panel de ayuda separado"""
        panel_ayuda = PanelAyuda(self)
        panel_ayuda.exec_()
    
    def opciones_avanzadas(self):
        """Abrir panel de opciones avanzadas para QA"""
        panel = PanelQAAvanzado(self)
        panel.exec_()
    
    def nueva_conversacion(self):
        """Iniciar nueva conversación"""
        reply = QMessageBox.question(self, 'Nueva Conversación', 
                                   '¿Deseas guardar la conversación actual antes de iniciar una nueva?',
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        
        if reply == QMessageBox.Cancel:
            return
        elif reply == QMessageBox.Yes:
            self.guardar_conversacion()
        
        # Limpiar chat
        self.area_chat.clear()
        
        # Reiniciar sesión del chatbot
        self.chatbot.sesion_actual = {
            'inicio': datetime.now().isoformat(),
            'conversaciones': []
        }
        
        # Limpiar historial de conversación en memoria
        self.chatbot.historial_conversacion = []
        
        # Resetear contador
        self.contador_mensajes = 0
        self.actualizar_status()
        
        # Mensaje de bienvenida
        self.mostrar_mensaje_bienvenida()
        
        # Limpiar archivos adjuntos
        self.archivos_adjuntos.clear()
    
    def guardar_conversacion(self):
        """Guardar la conversación actual"""
        try:
            if len(self.chatbot.sesion_actual['conversaciones']) > 0:
                ruta_archivo = self.chatbot.guardar_sesion_completa()
                if ruta_archivo:
                    QMessageBox.information(self, "Éxito", "💾 Conversación guardada correctamente en el historial")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo guardar la conversación")
            else:
                QMessageBox.warning(self, "Advertencia", "No hay conversaciones para guardar")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al guardar: {str(e)}")
    
    def closeEvent(self, event):
        """Manejar cierre de la aplicación"""
        try:
            # Guardar sesión actual si hay conversaciones
            if len(self.chatbot.sesion_actual['conversaciones']) > 0:
                reply = QMessageBox.question(self, 'Guardar sesión', 
                                           '¿Deseas guardar la sesión actual antes de salir?',
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                
                if reply == QMessageBox.Cancel:
                    event.ignore()
                    return
                elif reply == QMessageBox.Yes:
                    self.chatbot.guardar_sesion_completa()
            
            event.accept()
        except Exception as e:
            print(f"Error al cerrar aplicación: {e}")
            event.accept()
    
    def apply_modern_styles(self):
        """Aplicar estilos modernos CSS"""
        style = """
        QMainWindow {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #0B1D4A, stop: 1 #1F2A56);
        }
        
        #headerFrame {
            background: transparent;
            border: none;
        }
        
        #botIcon {
            font-size: 36px;
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #4C5BFF, stop: 1 #6366F1);
            border-radius: 35px;
            color: white;
            font-weight: bold;
        }
        
        #mainTitle {
            font-size: 32px;
            font-weight: bold;
            color: #ffffff;
            margin: 0px;
        }
        
        #subtitle {
            font-size: 16px;
            color: #94A3B8;
            margin: 0px;
        }
        
        #chatFrame {
            background: #141F3C;
            border-radius: 20px;
            border: 2px solid #4C5BFF;
        }
        
        #areaChat {
            background: #141F3C;
            border: none;
            border-radius: 15px;
            padding: 20px;
            font-size: 14px;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #ffffff;
        }
        
        #areaChat QScrollBar:vertical {
            background: #1B243A;
            width: 12px;
            border-radius: 6px;
            margin: 0px;
        }
        
        #areaChat QScrollBar::handle:vertical {
            background: #4C5BFF;
            border-radius: 6px;
            min-height: 25px;
        }
        
        #areaChat QScrollBar::handle:vertical:hover {
            background: #6366F1;
        }
        
        #inputFrame {
            background: transparent;
            border: none;
        }
        
        #entradaTexto {
            background: #1B243A;
            color: #ffffff;
            border: 2px solid #4C5BFF;
            border-radius: 15px;
            padding: 15px 20px;
            font-size: 16px;
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.5;
            selection-background-color: #4C5BFF;
        }
        
        #entradaTexto:focus {
            border: 2px solid #6366F1;
            background: #1E2A40;
            outline: none;
        }
        
        #entradaTexto QScrollBar:vertical {
            background: #1B243A;
            width: 10px;
            border-radius: 5px;
            margin: 2px;
            border: 1px solid #4C5BFF;
        }
        
        #entradaTexto QScrollBar::handle:vertical {
            background: #4C5BFF;
            border-radius: 5px;
            min-height: 25px;
            margin: 1px;
        }
        
        #entradaTexto QScrollBar::handle:vertical:hover {
            background: #6366F1;
        }
        
        #entradaTexto QScrollBar::add-line:vertical,
        #entradaTexto QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        #attachButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #4C5BFF, stop: 1 #6366F1);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
            padding: 8px 15px;
            min-width: 100px;
        }
        
        #attachButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #6366F1, stop: 1 #7C3AED);
        }
        
        #sendButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #2EC877, stop: 1 #10B981);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 14px;
            font-weight: bold;
            padding: 8px 15px;
            min-width: 100px;
        }
        
        #sendButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #34D399, stop: 1 #059669);
        }
        
        #buttonsFrame {
            background: transparent;
        }
        
        #helpButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #5A47F3, stop: 1 #7C3AED);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 16px;
            font-weight: bold;
            padding: 15px 25px;
        }
        
        #helpButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #7C3AED, stop: 1 #A855F7);
        }
        
        #historyButton, #advancedButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #1E3058, stop: 1 #2D3748);
            color: white;
            border: 2px solid #4C5BFF;
            border-radius: 15px;
            font-size: 16px;
            font-weight: bold;
            padding: 15px 25px;
        }
        
        #historyButton:hover, #advancedButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #4C5BFF, stop: 1 #6366F1);
            border: 2px solid #6366F1;
        }
        
        #footerFrame {
            background: transparent;
        }
        
        #statusLabel {
            color: #94A3B8;
            font-size: 14px;
            font-weight: normal;
        }
        """
        
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    
    # Configurar fuente por defecto
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Crear y mostrar la ventana principal
    window = AsistenteVirtualModernUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
