import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                           QFrame, QFileDialog, QMessageBox, QDialog, 
                           QListWidget, QListWidgetItem, QSplitter, QTextBrowser)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QTextCursor

# Importar el chatbot
from Chatbot import ChatBot

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
        <div style='font-family: Segoe UI; color: #ffffff; background-color: #141F3C; padding: 20px; border-radius: 15px;'>
            <h2 style='color: #4C5BFF; margin-top: 0;'>📅 Sesión del {fecha_legible}</h2>
            <p style='color: #94A3B8;'>💬 Total de mensajes: {len(sesion['conversaciones'])}</p>
            <hr style='border: 1px solid #4C5BFF; margin: 20px 0;'>
        """
        
        for conv in sesion['conversaciones']:
            timestamp = conv.get('timestamp', 'Sin hora')
            try:
                ts_obj = datetime.fromisoformat(timestamp)
                hora = ts_obj.strftime('%H:%M')
            except:
                hora = timestamp
            
            tipo = conv.get('tipo', 'desconocido')
            contenido = conv.get('contenido', '')
            
            if tipo == 'usuario':
                icon, color, align = '👤', '#1E3058', 'right'
            else:
                icon, color, align = '🤖', '#2D3748', 'left'
            
            html += f"""
            <div style='margin: 15px 0; padding: 15px; background-color: {color}; border-radius: 15px; text-align: {align};'>
                <p style='margin: 0; font-size: 12px; color: #94A3B8;'>{icon} [{hora}]</p>
                <p style='margin: 5px 0 0 0; color: #ffffff; line-height: 1.4;'>{contenido}</p>
            </div>
            """
        
        return html + "</div>"
    
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

class AsistenteVirtualModernUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 Asistente Virtual AI - Interfaz Moderna")
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
        title = QLabel("Asistente Virtual AI")
        title.setObjectName("mainTitle")
        titles_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Análisis inteligente de documentos con IA avanzada")
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
        chat_layout.addWidget(self.area_chat)
        
        return chat_frame
    
    def create_modern_input(self):
        """Crear el área de entrada moderna"""
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(25, 20, 25, 20)
        input_layout.setSpacing(15)
        
        # Campo de texto
        self.entrada_texto = QTextEdit()
        self.entrada_texto.setObjectName("entradaTexto")
        self.entrada_texto.setPlaceholderText("Escribe tu mensaje aquí...")
        self.entrada_texto.setMaximumHeight(80)
        self.entrada_texto.setMinimumHeight(50)
        
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
        
        # Botón Avanzado
        advanced_btn = QPushButton("⚙️ Avanzado")
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
        
        # HTML del mensaje de bienvenida
        html_bienvenida = f"""
        <div style="padding: 20px; font-family: 'Segoe UI', Arial, sans-serif;">
            <div style="background: linear-gradient(135deg, #1E3058, #2D3748); 
                        color: #ffffff; padding: 20px; border-radius: 20px; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2); max-width: 85%;">
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
                    [{timestamp}] 🤖
                </div>
                <div style="font-size: 16px; line-height: 1.5; margin-bottom: 15px;">
                    ¡Hola! Soy tu Asistente Virtual con IA avanzada. ¿En qué puedo ayudarte hoy?
                </div>
                <div style="font-size: 14px; line-height: 1.4; color: #E2E8F0;">
                    ✦ Puedo analizar documentos, generar casos de prueba, crear manuales de usuario y mucho más. 
                    ¡Adjunta archivos o simplemente pregúntame!
                </div>
            </div>
        </div>
        """
        
        self.area_chat.setHtml(html_bienvenida)
        self.contador_mensajes += 1
        self.actualizar_status()
        
    def mostrar_mensaje_usuario(self, mensaje):
        """Mostrar mensaje del usuario con diseño moderno"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # Agregar conversación al chatbot
        self.chatbot.guardar_conversacion(mensaje, "")
        
        # HTML del mensaje del usuario
        html_mensaje = f"""
        <div style="text-align: right; margin: 20px 0; font-family: 'Segoe UI', Arial, sans-serif;">
            <div style="display: inline-block; background: linear-gradient(135deg, #4C5BFF, #6366F1); 
                        color: #ffffff; padding: 15px 20px; border-radius: 20px 20px 8px 20px; 
                        box-shadow: 0 3px 12px rgba(76, 91, 255, 0.3); max-width: 70%; text-align: left;">
                <div style="font-size: 12px; color: rgba(255,255,255,0.8); margin-bottom: 8px;">
                    [{timestamp}] 👤
                </div>
                <div style="font-size: 15px; line-height: 1.4;">
                    {mensaje}
                </div>
            </div>
        </div>
        """
        
        self.area_chat.append(html_mensaje)
        self.scroll_to_bottom()
        self.contador_mensajes += 1
        self.actualizar_status()
    
    def mostrar_mensaje_bot(self, mensaje):
        """Mostrar mensaje del bot con diseño moderno"""
        timestamp = datetime.now().strftime("%H:%M")
        
        # HTML del mensaje del bot
        html_mensaje = f"""
        <div style="text-align: left; margin: 20px 0; font-family: 'Segoe UI', Arial, sans-serif;">
            <div style="display: inline-block; background: linear-gradient(135deg, #1E3058, #2D3748); 
                        color: #ffffff; padding: 15px 20px; border-radius: 20px 20px 20px 8px; 
                        box-shadow: 0 3px 12px rgba(0,0,0,0.15); max-width: 75%; text-align: left;">
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 8px;">
                    [{timestamp}] 🤖
                </div>
                <div style="font-size: 15px; line-height: 1.5;">
                    {mensaje}
                </div>
            </div>
        </div>
        """
        
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
        """Mostrar ayuda y tips"""
        ayuda_texto = """
        💡 **Consejos para usar el Asistente Virtual:**
        
        • Adjunta documentos PDF, DOCX para análisis automático
        • Usa comandos como 'analizar', 'resumir', 'extraer' para funciones específicas
        • El historial guarda todas tus conversaciones automáticamente
        • Puedes generar casos de prueba y manuales de usuario
        • Shift+Enter para nueva línea, Enter para enviar
        • Los archivos adjuntos se procesan automáticamente con tu mensaje
        """
        self.mostrar_mensaje_bot(ayuda_texto)
    
    def opciones_avanzadas(self):
        """Mostrar opciones avanzadas"""
        reply = QMessageBox.question(self, 'Opciones Avanzadas', 
                                   '¿Qué acción deseas realizar?\n\n'
                                   '• Guardar conversación actual\n'
                                   '• Nueva conversación\n'
                                   '• Configurar IA',
                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        
        if reply == QMessageBox.Yes:
            self.guardar_conversacion()
        elif reply == QMessageBox.No:
            self.nueva_conversacion()
    
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
            font-size: 15px;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        #entradaTexto:focus {
            border: 2px solid #6366F1;
            background: #1E2A40;
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
