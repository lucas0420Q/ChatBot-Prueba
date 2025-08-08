import sys
import os
import threading
import json
import tempfile
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton, 
                           QScrollArea, QFrame, QSizePolicy, QSpacerItem, QFileDialog,
                           QMessageBox, QDialog, QListWidget, QListWidgetItem,
                           QSplitter, QTreeWidget, QTreeWidgetItem, QProgressBar, QTextBrowser)
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon, QTextCursor

# Importar el chatbot original
from Chatbot import ChatBot

# Importar librerías para leer diferentes tipos de archivos
try:
    from docx import Document
    DOCX_DISPONIBLE = True
except ImportError:
    DOCX_DISPONIBLE = False
    Document = None

try:
    import PyPDF2
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False
    PyPDF2 = None

try:
    from PIL import Image, ImageGrab
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False
    Image = None
    ImageGrab = None

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
        with open(ruta_archivo, 'rb') as archivo:
            lector = PyPDF2.PdfReader(archivo)
            texto = ""
            for pagina in lector.pages:
                texto += pagina.extract_text() + "\n"
        return texto
    
    def extraer_texto_docx(self, ruta_archivo):
        """Extrae texto de un archivo DOCX"""
        doc = Document(ruta_archivo)
        texto = ""
        for parrafo in doc.paragraphs:
            texto += parrafo.text + "\n"
        return texto
    
    def extraer_texto_txt(self, ruta_archivo):
        """Extrae texto de un archivo TXT"""
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()

class HistorialDialog(QDialog):
    """Diálogo para mostrar el historial de conversaciones"""
    def __init__(self, chatbot, parent=None):
        super().__init__(parent)
        self.chatbot = chatbot
        self.setWindowTitle("📂 Historial de Conversaciones")
        self.setGeometry(200, 200, 1000, 700)
        self.setup_ui()
        self.aplicar_estilos()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        titulo = QLabel("📂 Historial de Conversaciones")
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
        
        btn_exportar = QPushButton("📤 Exportar Todo")
        btn_exportar.setObjectName("botonHistorial")
        btn_exportar.clicked.connect(self.exportar_historial_completo)
        
        btn_exportar_sesion = QPushButton("💾 Exportar Sesión")
        btn_exportar_sesion.setObjectName("botonHistorial")
        btn_exportar_sesion.clicked.connect(self.exportar_sesion_actual)
        
        btn_cerrar = QPushButton("❌ Cerrar")
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
                
                item = QListWidgetItem(f"📅 {fecha_legible}")
                item.setData(Qt.UserRole, sesion)
                self.lista_sesiones.addItem(item)
        except Exception as e:
            self.area_contenido.setText(f"Error al cargar historial: {str(e)}")
    
    def actualizar_estadisticas(self):
        """Actualiza las estadísticas del historial"""
        try:
            stats = self.chatbot.obtener_estadisticas_historial()
            if stats:
                texto_stats = f"📊 Total: {stats['total_sesiones']} sesiones, {stats['total_conversaciones']} mensajes"
                self.label_stats.setText(texto_stats)
            else:
                self.label_stats.setText("📊 No hay estadísticas disponibles")
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
        <div style='font-family: Segoe UI; color: #ffffff; background-color: #273A69; padding: 20px; border-radius: 10px;'>
            <h2 style='color: #3b82f6; margin-top: 0;'>📅 Sesión del {fecha_legible}</h2>
            <p style='color: #a0a9c0;'>💬 Total de mensajes: {len(sesion['conversaciones'])}</p>
            <hr style='border: 1px solid #3b82f6; margin: 20px 0;'>
        """
        
        for i, conv in enumerate(sesion['conversaciones'], 1):
            timestamp = conv.get('timestamp', 'Sin hora')
            try:
                ts_obj = datetime.fromisoformat(timestamp)
                hora = ts_obj.strftime('%H:%M:%S')
            except:
                hora = timestamp
            
            tipo = conv.get('tipo', 'desconocido')
            contenido = conv.get('contenido', '')
            
            if tipo == 'usuario':
                icon = '👤'
                color = '#2E6F93'
                align = 'right'
            else:
                icon = '🤖'
                color = '#1C2A4D'
                align = 'left'
            
            html += f"""
            <div style='margin: 15px 0; padding: 15px; background-color: {color}; border-radius: 15px; text-align: {align};'>
                <p style='margin: 0; font-size: 12px; color: #a0a9c0;'>{icon} {hora}</p>
                <p style='margin: 5px 0 0 0; color: #ffffff; line-height: 1.4;'>{contenido}</p>
            </div>
            """
        
        html += "</div>"
        return html
    
    def exportar_historial_completo(self):
        """Exporta el historial completo"""
        try:
            ruta, _ = QFileDialog.getSaveFileName(self, "Guardar historial completo", 
                                                "historial_completo.txt", 
                                                "Text files (*.txt)")
            if ruta:
                contenido = self.chatbot.generar_reporte_historial_completo()
                with open(ruta, 'w', encoding='utf-8') as archivo:
                    archivo.write(contenido)
                QMessageBox.information(self, "Éxito", "Historial exportado correctamente")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al exportar: {str(e)}")
    
    def exportar_sesion_actual(self):
        """Exporta la sesión seleccionada"""
        item_actual = self.lista_sesiones.currentItem()
        if not item_actual:
            QMessageBox.warning(self, "Advertencia", "Selecciona una sesión para exportar")
            return
        
        try:
            archivo = item_actual.data(Qt.UserRole)
            ruta, _ = QFileDialog.getSaveFileName(self, "Guardar sesión", 
                                                f"sesion_{archivo.replace('.json', '.txt')}", 
                                                "Text files (*.txt)")
            if ruta:
                contenido = self.chatbot.obtener_contenido_sesion(archivo)
                with open(ruta, 'w', encoding='utf-8') as archivo_salida:
                    archivo_salida.write(contenido)
                QMessageBox.information(self, "Éxito", "Sesión exportada correctamente")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al exportar sesión: {str(e)}")
    
    def aplicar_estilos(self):
        """Aplicar estilos al diálogo"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #0A0F2C, stop: 1 #1a1f3a);
            }
            #historialTitulo {
                color: #ffffff;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
            }
            #statsLabel {
                color: #a0a9c0;
                font-size: 14px;
                padding: 5px 15px;
            }
            #listaSesiones {
                background: #1C2A4D;
                color: #ffffff;
                border: 2px solid #3b82f6;
                border-radius: 10px;
                font-size: 13px;
                padding: 5px;
            }
            #listaSesiones::item {
                padding: 10px;
                border-bottom: 1px solid #3b82f6;
                border-radius: 5px;
                margin: 2px;
            }
            #listaSesiones::item:selected {
                background: #3b82f6;
            }
            #listaSesiones::item:hover {
                background: #273A69;
            }
            #areaContenido {
                background: #273A69;
                color: #ffffff;
                border: 2px solid #3b82f6;
                border-radius: 10px;
                font-size: 13px;
                padding: 10px;
            }
            #botonHistorial {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #3b82f6, stop: 1 #6366f1);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 20px;
                min-width: 120px;
            }
            #botonHistorial:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #60a5fa, stop: 1 #8b5cf6);
            }
        """)

class AsistenteVirtualAI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 Asistente Virtual AI - Análisis Inteligente de Documentos")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)
        
        # Inicializar el chatbot (igual que en tkinter)
        self.chatbot = ChatBot("Asistente Virtual")
        
        # Lista de archivos adjuntos
        self.archivos_adjuntos = []
        
        # Estado del modo oscuro (por defecto: claro)
        self.modo_oscuro = False
        
        # Configurar ventana principal
        self.setup_ui()
        self.apply_styles()
        
        # Mensaje de bienvenida (igual que en tkinter)
        self.mostrar_mensaje_bot("🎉 ¡Hola! Soy tu Asistente Virtual con IA avanzada. ¿En qué puedo ayudarte hoy? \n\n✨ Puedo analizar documentos, generar casos de prueba, crear manuales de usuario y mucho más. ¡Adjunta archivos o simplemente pregúntame!")
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # ENCABEZADO SUPERIOR
        header_widget = self.create_header()
        main_layout.addWidget(header_widget)
        
        # SECCIÓN DE CONVERSACIÓN
        chat_widget = self.create_chat_section()
        main_layout.addWidget(chat_widget, 1)  # Expandible
        
        # SECCIÓN DE ARCHIVOS ADJUNTOS
        archivos_widget = self.create_archivos_section()
        main_layout.addWidget(archivos_widget)
        
        # ENTRADA DE TEXTO
        input_widget = self.create_input_section()
        main_layout.addWidget(input_widget)
        
        # BOTONES INFERIORES
        buttons_widget = self.create_bottom_buttons()
        main_layout.addWidget(buttons_widget)
        
        # AYUDA & TIPS
        help_widget = self.create_help_section()
        main_layout.addWidget(help_widget)
        
    def create_header(self):
        """Crear el encabezado superior"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Ícono del bot
        bot_icon = QLabel("🤖")
        bot_icon.setObjectName("botIcon")
        bot_icon.setAlignment(Qt.AlignCenter)
        bot_icon.setFixedSize(60, 60)
        
        # Contenedor de títulos
        titles_layout = QVBoxLayout()
        titles_layout.setSpacing(5)
        
        # Título principal
        title = QLabel("Asistente Virtual AI")
        title.setObjectName("mainTitle")
        titles_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Análisis inteligente de documentos con IA avanzada")
        subtitle.setObjectName("subtitle")
        titles_layout.addWidget(subtitle)
        
        # Estado de la IA
        estado_ia = "🟢 IA Conectada (Gemini 2.0 Flash)" if self.chatbot.usar_ia else "🔴 IA Desconectada"
        ia_status = QLabel(estado_ia)
        ia_status.setObjectName("iaStatus")
        titles_layout.addWidget(ia_status)
        
        # Agregar elementos al header
        header_layout.addWidget(bot_icon)
        header_layout.addLayout(titles_layout)
        header_layout.addStretch()
        
        # Botón de modo oscuro
        self.dark_mode_btn = QPushButton("🌙")
        self.dark_mode_btn.setObjectName("darkModeButton")
        self.dark_mode_btn.setFixedSize(50, 50)
        self.dark_mode_btn.setToolTip("Cambiar a modo oscuro/claro")
        self.dark_mode_btn.clicked.connect(self.toggle_dark_mode)
        header_layout.addWidget(self.dark_mode_btn)
        
        return header_frame
        
    def create_chat_section(self):
        """Crear la sección de conversación"""
        chat_frame = QFrame()
        chat_frame.setObjectName("chatFrame")
        
        chat_layout = QVBoxLayout(chat_frame)
        chat_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título del chat
        chat_title = QLabel("💬 Conversación")
        chat_title.setObjectName("chatTitle")
        chat_layout.addWidget(chat_title)
        
        # Área de texto para el chat (similar a tkinter)
        self.area_chat = QTextBrowser()
        self.area_chat.setObjectName("areaChat")
        self.area_chat.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.area_chat.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        chat_layout.addWidget(self.area_chat)
        
        return chat_frame
    
    def create_archivos_section(self):
        """Crear la sección de archivos adjuntos"""
        archivos_frame = QFrame()
        archivos_frame.setObjectName("archivosFrame")
        
        archivos_layout = QVBoxLayout(archivos_frame)
        archivos_layout.setContentsMargins(15, 10, 15, 10)
        
        # Título
        titulo_archivos = QLabel("📎 Archivos Adjuntos")
        titulo_archivos.setObjectName("archivosTitle")
        archivos_layout.addWidget(titulo_archivos)
        
        # Lista de archivos
        self.lista_archivos = QLabel("No hay archivos adjuntos")
        self.lista_archivos.setObjectName("listaArchivos")
        self.lista_archivos.setWordWrap(True)
        archivos_layout.addWidget(self.lista_archivos)
        
        # Ocultar inicialmente
        archivos_frame.hide()
        self.archivos_frame = archivos_frame
        
        return archivos_frame
        
    def create_input_section(self):
        """Crear la sección de entrada de texto"""
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(20, 15, 20, 15)
        input_layout.setSpacing(15)
        
        # Botón adjuntar archivos
        self.attach_btn = QPushButton("📎")
        self.attach_btn.setObjectName("attachButton")
        self.attach_btn.setFixedSize(45, 45)
        self.attach_btn.setToolTip("Adjuntar archivos")
        self.attach_btn.clicked.connect(self.adjuntar_archivo)
        
        # Campo de texto multilínea (como en tkinter)
        self.entrada_texto = QTextEdit()
        self.entrada_texto.setObjectName("entradaTexto")
        self.entrada_texto.setPlaceholderText("Escribe tu mensaje aquí... (Shift+Enter para nueva línea, Enter para enviar)")
        self.entrada_texto.setMaximumHeight(100)
        self.entrada_texto.setMinimumHeight(45)
        
        # Configurar eventos de teclado
        self.entrada_texto.keyPressEvent = self.manejar_teclas
        
        # Botón enviar
        self.send_btn = QPushButton("✈️")
        self.send_btn.setObjectName("sendButton")
        self.send_btn.setFixedSize(45, 45)
        self.send_btn.setToolTip("Enviar mensaje")
        self.send_btn.clicked.connect(self.enviar_mensaje)
        
        input_layout.addWidget(self.attach_btn)
        input_layout.addWidget(self.entrada_texto)
        input_layout.addWidget(self.send_btn)
        
        return input_frame
    
    def manejar_teclas(self, evento):
        """Manejar eventos de teclado (como en tkinter)"""
        if evento.key() == Qt.Key_Return and not (evento.modifiers() & Qt.ShiftModifier):
            # Enter sin Shift: enviar mensaje
            self.enviar_mensaje()
            evento.accept()
        else:
            # Comportamiento normal (incluyendo Shift+Enter para nueva línea)
            QTextEdit.keyPressEvent(self.entrada_texto, evento)
        
    def create_bottom_buttons(self):
        """Crear los botones inferiores"""
        buttons_frame = QFrame()
        buttons_frame.setObjectName("buttonsFrame")
        
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(20, 15, 20, 15)
        buttons_layout.setSpacing(20)
        
        # Botón Limpiar Chat
        clear_btn = QPushButton("🗑️ Nueva Conversación")
        clear_btn.setObjectName("actionButton")
        clear_btn.setMinimumHeight(50)
        clear_btn.clicked.connect(self.nueva_conversacion)
        
        # Botón Historial
        history_btn = QPushButton("🕒 Historial")
        history_btn.setObjectName("actionButton")
        history_btn.setMinimumHeight(50)
        history_btn.clicked.connect(self.abrir_historial)
        
        # Botón Guardar
        save_btn = QPushButton("💾 Guardar Sesión")
        save_btn.setObjectName("actionButton")
        save_btn.setMinimumHeight(50)
        save_btn.clicked.connect(self.guardar_conversacion)
        
        buttons_layout.addWidget(clear_btn)
        buttons_layout.addWidget(history_btn)
        buttons_layout.addWidget(save_btn)
        
        return buttons_frame
        
    def create_help_section(self):
        """Crear la sección de ayuda"""
        help_frame = QFrame()
        help_frame.setObjectName("helpFrame")
        
        help_layout = QVBoxLayout(help_frame)
        help_layout.setContentsMargins(20, 10, 20, 10)
        
        help_title = QLabel("💡 Ayuda & Tips")
        help_title.setObjectName("helpTitle")
        
        help_text = QLabel("• Adjunta documentos PDF, DOCX para análisis automático\n"
                          "• Usa comandos como 'analizar', 'resumir', 'extraer' para funciones específicas\n"
                          "• El historial guarda todas tus conversaciones automáticamente\n"
                          "• Puedes generar casos de prueba y manuales de usuario\n"
                          "• Shift+Enter para nueva línea, Enter para enviar")
        help_text.setObjectName("helpText")
        help_text.setWordWrap(True)
        
        help_layout.addWidget(help_title)
        help_layout.addWidget(help_text)
        
        return help_frame
    
    def mostrar_mensaje_usuario(self, mensaje):
        """Mostrar mensaje del usuario con diseño moderno"""
        timestamp = datetime.now().strftime("%H:%M")
        # Agregar conversación al chatbot
        self.chatbot.guardar_conversacion(mensaje, "")
        
        # Colores para modo claro y oscuro
        if self.modo_oscuro:
            user_bg = "linear-gradient(135deg, #2E6F93, #3b82f6)"
            user_color = "#ffffff"
        else:
            user_bg = "linear-gradient(135deg, #3b82f6, #60a5fa)"
            user_color = "#ffffff"
        
        # Usar HTML para un diseño más atractivo
        html_mensaje = f"""
        <div style="margin: 15px 0; text-align: right;">
            <div style="display: inline-block; max-width: 70%; background: {user_bg}; 
                        color: {user_color}; padding: 12px 18px; border-radius: 18px 18px 4px 18px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.15); font-weight: bold;">
                <div style="font-size: 11px; opacity: 0.8; margin-bottom: 4px;">👤 Tú • {timestamp}</div>
                <div>{mensaje}</div>
            </div>
        </div>
        """
        
        self.area_chat.append(html_mensaje)
        self.scroll_to_bottom()
    
    def mostrar_mensaje_bot(self, mensaje):
        """Mostrar mensaje del bot con diseño moderno"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Colores para modo claro y oscuro
        if self.modo_oscuro:
            bot_bg = "linear-gradient(135deg, #374151, #4b5563)"
            bot_color = "#ffffff"
            border_color = "#3b82f6"
        else:
            bot_bg = "linear-gradient(135deg, #f8f9fa, #e9ecef)"
            bot_color = "#343a40"
            border_color = "#3b82f6"
        
        # Usar HTML para un diseño más atractivo
        html_mensaje = f"""
        <div style="margin: 15px 0; text-align: left;">
            <div style="display: inline-block; max-width: 70%; background: {bot_bg}; 
                        color: {bot_color}; padding: 12px 18px; border-radius: 18px 18px 18px 4px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid {border_color};">
                <div style="font-size: 11px; opacity: 0.7; margin-bottom: 4px;">🤖 Asistente • {timestamp}</div>
                <div style="line-height: 1.4;">{mensaje}</div>
            </div>
        </div>
        """
        
        self.area_chat.append(html_mensaje)
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Hacer scroll hacia abajo"""
        scrollbar = self.area_chat.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def enviar_mensaje(self):
        """Enviar mensaje al chatbot (igual lógica que tkinter)"""
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
            self.actualizar_lista_archivos()
    
    def procesar_respuesta(self, respuesta):
        """Procesar respuesta del chatbot"""
        # Remover último mensaje (el de "escribiendo...")
        contenido_actual = self.area_chat.toHtml()
        
        # Buscar el último mensaje que contenga "✍️ Escribiendo..."
        if "✍️ Escribiendo..." in contenido_actual:
            # Encontrar la última aparición del mensaje de escribiendo
            ultimo_index = contenido_actual.rfind("✍️ Escribiendo...")
            if ultimo_index != -1:
                # Buscar el div que contiene este mensaje
                div_inicio = contenido_actual.rfind('<div style="margin: 15px 0; text-align: left;">', 0, ultimo_index)
                if div_inicio != -1:
                    # Buscar el cierre del div completo
                    div_cierre = contenido_actual.find('</div>\n        </div>', ultimo_index)
                    if div_cierre != -1:
                        # Remover todo el div del mensaje
                        contenido_sin_ultimo = contenido_actual[:div_inicio] + contenido_actual[div_cierre + 21:]
                        self.area_chat.setHtml(contenido_sin_ultimo)
        
        # Guardar respuesta en el chatbot
        if hasattr(self, '_ultimo_mensaje_usuario') and self.chatbot.sesion_actual['conversaciones']:
            self.chatbot.sesion_actual['conversaciones'][-1]['respuesta'] = respuesta
        
        # Mostrar respuesta real
        self.mostrar_mensaje_bot(respuesta)
        
        # Rehabilitar envío
        self.send_btn.setEnabled(True)
        self.entrada_texto.setEnabled(True)
        self.entrada_texto.setFocus()
    
    def procesar_error(self, error):
        """Procesar error del chatbot"""
        # Remover mensaje de "escribiendo..." (igual que arriba)
        contenido_actual = self.area_chat.toHtml()
        
        if "✍️ Escribiendo..." in contenido_actual:
            ultimo_index = contenido_actual.rfind("✍️ Escribiendo...")
            if ultimo_index != -1:
                div_inicio = contenido_actual.rfind('<div style="margin: 15px 0; text-align: left;">', 0, ultimo_index)
                if div_inicio != -1:
                    div_cierre = contenido_actual.find('</div>\n        </div>', ultimo_index)
                    if div_cierre != -1:
                        contenido_sin_ultimo = contenido_actual[:div_inicio] + contenido_actual[div_cierre + 21:]
                        self.area_chat.setHtml(contenido_sin_ultimo)
        
        # Mostrar error
        self.mostrar_mensaje_bot(f"❌ Error: {error}")
        
        # Rehabilitar envío
        self.send_btn.setEnabled(True)
        self.entrada_texto.setEnabled(True)
        self.entrada_texto.setFocus()
    
    def adjuntar_archivo(self):
        """Adjuntar archivos al chat (igual que tkinter)"""
        tipos_archivo = [
            ("Todos los archivos soportados", "*.txt *.pdf *.docx *.doc *.png *.jpg *.jpeg *.gif *.bmp *.json *.xml *.csv"),
            ("Documentos de texto", "*.txt *.pdf *.docx *.doc"),
            ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("Datos", "*.json *.xml *.csv"),
            ("Todos los archivos", "*.*")
        ]
        
        archivos, _ = QFileDialog.getOpenFileNames(
            self, 
            "Seleccionar archivos", 
            "", 
            ";;".join([f"{desc} ({ext})" for desc, ext in tipos_archivo])
        )
        
        if archivos:
            self.archivos_adjuntos.extend(archivos)
            self.actualizar_lista_archivos()
            
            # Mostrar mensaje de confirmación
            nombres = [os.path.basename(archivo) for archivo in archivos]
            mensaje_archivos = f"📎 {len(archivos)} archivo(s) adjuntado(s): {', '.join(nombres)}"
            self.mostrar_mensaje_bot(mensaje_archivos)
    
    def actualizar_lista_archivos(self):
        """Actualizar la lista de archivos adjuntos"""
        if self.archivos_adjuntos:
            nombres = [os.path.basename(archivo) for archivo in self.archivos_adjuntos]
            texto = f"📎 {len(self.archivos_adjuntos)} archivo(s): " + ", ".join(nombres)
            self.lista_archivos.setText(texto)
            self.archivos_frame.show()
        else:
            self.lista_archivos.setText("No hay archivos adjuntos")
            self.archivos_frame.hide()
    
    def nueva_conversacion(self):
        """Iniciar nueva conversación (igual que tkinter)"""
        reply = QMessageBox.question(self, 'Nueva Conversación', 
                                   '¿Deseas guardar la conversación actual antes de iniciar una nueva?',
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        
        if reply == QMessageBox.Cancel:
            return
        elif reply == QMessageBox.Yes:
            self.guardar_conversacion()
        
        # Limpiar chat
        self.area_chat.clear()
        
        # Reiniciar sesión del chatbot (crear nueva sesión)
        self.chatbot.sesion_actual = {
            'inicio': datetime.now().isoformat(),
            'conversaciones': []
        }
        
        # Limpiar historial de conversación en memoria
        self.chatbot.historial_conversacion = []
        
        # Mensaje de bienvenida
        self.mostrar_mensaje_bot("🎉 Nueva conversación iniciada. ¿En qué puedo ayudarte?")
        
        # Limpiar archivos adjuntos
        self.archivos_adjuntos.clear()
        self.actualizar_lista_archivos()
    
    def abrir_historial(self):
        """Abrir ventana de historial (igual que tkinter)"""
        dialog = HistorialDialog(self.chatbot, self)
        dialog.exec_()
    
    def guardar_conversacion(self):
        """Guardar la conversación actual (igual que tkinter)"""
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
        """Manejar cierre de la aplicación (igual que tkinter)"""
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
    
    def toggle_dark_mode(self):
        """Alternar entre modo oscuro y claro"""
        self.modo_oscuro = not self.modo_oscuro
        
        # Cambiar icono del botón
        if self.modo_oscuro:
            self.dark_mode_btn.setText("☀️")
            self.dark_mode_btn.setToolTip("Cambiar a modo claro")
        else:
            self.dark_mode_btn.setText("🌙")
            self.dark_mode_btn.setToolTip("Cambiar a modo oscuro")
        
        # Aplicar nuevos estilos
        self.apply_styles()
        
        # Mostrar mensaje informativo
        modo_texto = "modo oscuro" if self.modo_oscuro else "modo claro"
        self.mostrar_mensaje_bot(f"🎨 Cambiado a {modo_texto}")
        
    def get_chat_background_color(self):
        """Obtener color de fondo del área de chat según el modo"""
        if self.modo_oscuro:
            return "#1e293b"  # Gris oscuro
        else:
            return "#ffffff"  # Blanco
        
    def apply_styles(self):
        """Aplicar estilos CSS a la aplicación"""
        
        # Colores base según el modo
        if self.modo_oscuro:
            # Colores para modo oscuro
            main_bg = "qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #0A0F2C, stop: 1 #1a1f3a)"
            header_bg = "qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #1C2A4D, stop: 1 #273A69)"
            frame_bg = "#1C2A4D"
            input_bg = "#273A69"
            chat_bg = "#1e293b"
            text_color = "#ffffff"
            secondary_color = "#a0a9c0"
            accent_color = "#3b82f6"
        else:
            # Colores para modo claro
            main_bg = "qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #f8fafc, stop: 1 #e2e8f0)"
            header_bg = "qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffffff, stop: 1 #f1f5f9)"
            frame_bg = "#ffffff"
            input_bg = "#f8fafc"
            chat_bg = "#ffffff"
            text_color = "#1e293b"
            secondary_color = "#64748b"
            accent_color = "#3b82f6"
        
        style = f"""
        QMainWindow {{
            background: {main_bg};
        }}
        
        #headerFrame {{
            background: {header_bg};
            border-radius: 15px;
            border: 2px solid {accent_color};
        }}
        
        #botIcon {{
            font-size: 32px;
            background: {accent_color};
            border-radius: 30px;
            color: white;
        }}
        
        #mainTitle {{
            font-size: 28px;
            font-weight: bold;
            color: {text_color};
            margin: 0px;
        }}
        
        #subtitle {{
            font-size: 14px;
            color: {secondary_color};
            margin: 0px;
        }}
        
        #iaStatus {{
            font-size: 12px;
            color: #10b981;
            margin: 0px;
        }}
        
        #darkModeButton {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 {accent_color}, stop: 1 #6366f1);
            color: white;
            border: none;
            border-radius: 25px;
            font-size: 20px;
            font-weight: bold;
        }}
        
        #darkModeButton:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #60a5fa, stop: 1 #8b5cf6);
        }}
        
        #chatFrame {{
            background: {frame_bg};
            border-radius: 20px;
            border: 2px solid {accent_color};
        }}
        
        #chatTitle {{
            color: {accent_color};
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        #areaChat {{
            background: {chat_bg};
            border: none;
            border-radius: 10px;
            padding: 15px;
            font-size: 14px;
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.4;
        }}
        
        #areaChat QScrollBar:vertical {{
            background: #273A69;
            width: 10px;
            border-radius: 5px;
        }}
        
        #areaChat QScrollBar::handle:vertical {{
            background: {accent_color};
            border-radius: 5px;
            min-height: 20px;
        }}
        
        #archivosFrame {{
            background: {frame_bg};
            border-radius: 10px;
            border: 2px solid {accent_color};
        }}
        
        #archivosTitle {{
            color: {accent_color};
            font-size: 14px;
            font-weight: bold;
        }}
        
        #listaArchivos {{
            color: {secondary_color};
            font-size: 12px;
        }}
        
        #inputFrame {{
            background: {frame_bg};
            border-radius: 15px;
            border: 2px solid {accent_color};
        }}
        
        #entradaTexto {{
            background: {input_bg};
            color: {text_color};
            border: 2px solid {accent_color};
            border-radius: 10px;
            padding: 10px 15px;
            font-size: 14px;
        }}
        
        #entradaTexto:focus {{
            border: 2px solid #60a5fa;
        }}
        
        #attachButton {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 {accent_color}, stop: 1 #6366f1);
            color: white;
            border: none;
            border-radius: 22px;
            font-size: 18px;
            font-weight: bold;
        }}
        
        #attachButton:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #60a5fa, stop: 1 #8b5cf6);
        }}
        
        #sendButton {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #10b981, stop: 1 #059669);
            color: white;
            border: none;
            border-radius: 22px;
            font-size: 18px;
            font-weight: bold;
        }}
        
        #sendButton:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #34d399, stop: 1 #10b981);
        }}
        
        #buttonsFrame {{
            background: transparent;
        }}
        
        #actionButton {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 {accent_color}, stop: 1 #6366f1);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            padding: 15px 25px;
        }}
        
        #actionButton:hover {{
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #60a5fa, stop: 1 #8b5cf6);
        }}
        
        #helpFrame {{
            background: rgba(28, 42, 77, 0.5);
            border-radius: 10px;
            border: 1px solid {accent_color};
        }}
        
        #helpTitle {{
            color: {accent_color};
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        #helpText {{
            color: {secondary_color};
            font-size: 12px;
            line-height: 1.5;
        }}
        """
        
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    
    # Configurar fuente por defecto
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Crear y mostrar la ventana principal
    window = AsistenteVirtualAI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
