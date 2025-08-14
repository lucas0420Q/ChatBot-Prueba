import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QProgressBar, QScrollArea, QWidget, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer
from notion_integration import NotionConfigManager

class NotionConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Estado de conexión
        self.conexion_en_progreso = False
        
        # Configurar ventana
        self.setWindowTitle("�️ Configurar Base de Datos de Notion")
        self.setModal(True)
        self.setMinimumSize(520, 600)
        self.setMaximumSize(520, 800)
        self.resize(520, 700)
        
        # Aplicar estilos modernos
        self.aplicar_estilos()
        
        # Configurar UI
        self.configurar_ui()
        
        # Cargar configuración existente
        self.cargar_configuracion()
    
    def aplicar_estilos(self):
        """Aplicar estilos modernos al diálogo"""
        styles = """
        QDialog {
            background-color: #f8f9fa;
            border: none;
        }
        
        /* HEADER */
        #headerModerno {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #ffffff, stop:1 #f8f9fa);
            border-bottom: 1px solid #e9ecef;
        }
        
        #tituloHeader {
            font-size: 18px;
            font-weight: 600;
            color: #212529;
            margin: 0px;
        }
        
        #textoEstado {
            font-size: 12px;
            font-weight: 500;
            color: #6c757d;
        }
        
        /* SCROLL AREA */
        #scrollPrincipal {
            border: none;
            background-color: transparent;
        }
        
        #scrollPrincipal QScrollBar:vertical {
            background-color: #f8f9fa;
            width: 8px;
            border-radius: 4px;
        }
        
        #scrollPrincipal QScrollBar::handle:vertical {
            background-color: #dee2e6;
            border-radius: 4px;
            min-height: 20px;
        }
        
        #scrollPrincipal QScrollBar::handle:vertical:hover {
            background-color: #adb5bd;
        }
        
        /* CARD PRINCIPAL */
        #cardPrincipal {
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            margin: 0px;
        }
        
        #tituloCard {
            font-size: 16px;
            font-weight: 600;
            color: #495057;
            margin: 0px 0px 4px 0px;
        }
        
        /* CAMPOS DE ENTRADA */
        #labelCampo {
            font-size: 14px;
            font-weight: 500;
            color: #495057;
            margin: 0px 0px 6px 0px;
        }
        
        #inputToken, #inputDatabase {
            padding: 12px 16px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 14px;
            background-color: #ffffff;
            color: #495057;
        }
        
        #inputToken:focus, #inputDatabase:focus {
            border-color: #0d6efd;
            outline: none;
            background-color: #ffffff;
        }
        
        #toggleToken {
            border: 2px solid #e9ecef;
            border-radius: 8px;
            background-color: #f8f9fa;
            color: #6c757d;
            font-size: 14px;
        }
        
        #toggleToken:hover {
            background-color: #e9ecef;
            border-color: #adb5bd;
        }
        
        /* BOTONES */
        #botonPruebaRapida {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #0d6efd, stop:1 #0056b3);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
        }
        
        #botonPruebaRapida:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #0056b3, stop:1 #004494);
        }
        
        #botonPruebaRapida:pressed {
            background: #004494;
        }
        
        /* ÁREA DE FEEDBACK */
        #areaFeedback {
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-top: 8px;
        }
        
        #resultadoPrueba {
            font-size: 14px;
            font-weight: 500;
            margin: 0px;
        }
        
        #progressModerno {
            border: none;
            border-radius: 4px;
            background-color: #e9ecef;
            text-align: center;
        }
        
        #progressModerno::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 #0d6efd, stop:1 #6610f2);
            border-radius: 4px;
        }
        
        /* TUTORIAL */
        #tutorialExpandible {
            margin-top: 16px;
        }
        
        #tutorialHeader {
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 16px;
            font-size: 14px;
            font-weight: 500;
            color: #495057;
            text-align: left;
        }
        
        #tutorialHeader:hover {
            background-color: #f8f9fa;
            border-color: #adb5bd;
        }
        
        #tutorialContent {
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-top: none;
            border-radius: 0px 0px 8px 8px;
        }
        
        #pasoTutorial {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            margin: 4px 0px;
        }
        
        #numeroPaso {
            background-color: #0d6efd;
            color: white;
            border-radius: 16px;
            font-weight: 600;
            font-size: 12px;
        }
        
        #tituloPaso {
            font-weight: 600;
            color: #495057;
            font-size: 13px;
            margin: 0px;
        }
        
        #descripcionPaso {
            color: #6c757d;
            font-size: 12px;
            line-height: 1.4;
            margin: 0px;
        }
        
        #enlaceDirecto {
            background-color: #e7f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 6px;
            margin: 8px 0px;
        }
        
        #enlaceNotion {
            color: #0066cc;
            font-size: 13px;
            font-weight: 500;
        }
        
        /* FOOTER */
        #footerModerno {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #f8f9fa, stop:1 #ffffff);
            border-top: 1px solid #e9ecef;
        }
        
        #botonPrincipal {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #28a745, stop:1 #1e7e34);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 32px;
            font-size: 14px;
            font-weight: 600;
        }
        
        #botonPrincipal:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #1e7e34, stop:1 #155724);
        }
        
        #botonSecundario {
            background-color: transparent;
            color: #6c757d;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
        }
        
        #botonSecundario:hover {
            background-color: #f8f9fa;
            border-color: #adb5bd;
            color: #495057;
        }
        """
        
        self.setStyleSheet(styles)
    
    def configurar_ui(self):
        """Configurar la interfaz con diseño moderno y flujo único"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # HEADER MODERNO
        header_widget = self.crear_header()
        layout.addWidget(header_widget)
        
        # CONTENIDO PRINCIPAL (SCROLL)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("scrollPrincipal")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        contenido_widget = QWidget()
        contenido_layout = QVBoxLayout(contenido_widget)
        contenido_layout.setSpacing(24)
        contenido_layout.setContentsMargins(32, 32, 32, 32)
        
        # Card principal de configuración
        self.card_principal = self.crear_card_configuracion()
        contenido_layout.addWidget(self.card_principal)
        
        # Área de feedback
        self.area_feedback = self.crear_area_feedback()
        contenido_layout.addWidget(self.area_feedback)
        
        # Tutorial expandible
        self.tutorial_widget = self.crear_tutorial_expandible()
        contenido_layout.addWidget(self.tutorial_widget)
        
        contenido_layout.addStretch()
        scroll_area.setWidget(contenido_widget)
        layout.addWidget(scroll_area)
        
        # FOOTER CON BOTONES
        footer_widget = self.crear_footer()
        layout.addWidget(footer_widget)
    
    def crear_header(self):
        """Crear header moderno con título y estado"""
        header = QWidget()
        header.setObjectName("headerModerno")
        header.setFixedHeight(80)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(32, 16, 32, 16)
        
        # Título principal
        titulo = QLabel("�️ Configurar Base de Datos de Notion")
        titulo.setObjectName("tituloHeader")
        
        # Estado de conexión
        self.estado_widget = QWidget()
        estado_layout = QHBoxLayout(self.estado_widget)
        estado_layout.setContentsMargins(0, 0, 0, 0)
        estado_layout.setSpacing(8)
        
        self.icono_estado = QLabel("⚪")
        self.texto_estado = QLabel("Sin configurar")
        self.texto_estado.setObjectName("textoEstado")
        
        estado_layout.addWidget(self.icono_estado)
        estado_layout.addWidget(self.texto_estado)
        
        layout.addWidget(titulo)
        layout.addStretch()
        layout.addWidget(self.estado_widget)
        
        return header
    
    def crear_card_configuracion(self):
        """Crear card principal de configuración"""
        card = QWidget()
        card.setObjectName("cardPrincipal")
        
        layout = QVBoxLayout(card)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Título del card
        titulo_card = QLabel("Configuración Simplificada")
        titulo_card.setObjectName("tituloCard")
        layout.addWidget(titulo_card)
        
        # Formulario
        form_layout = QVBoxLayout()
        form_layout.setSpacing(16)
        
        # ID de la base de datos
        label_db = QLabel("🗃️ ID de Base de Datos de Notion")
        label_db.setObjectName("labelCampo")
        
        self.input_database_id = QLineEdit()
        self.input_database_id.setObjectName("inputDatabase")
        self.input_database_id.setPlaceholderText("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        
        form_layout.addWidget(label_db)
        form_layout.addWidget(self.input_database_id)
        
        # Botón de prueba rápida
        self.btn_prueba_rapida = QPushButton("⚡ Verificar Base de Datos")
        self.btn_prueba_rapida.setObjectName("botonPruebaRapida")
        self.btn_prueba_rapida.clicked.connect(self.probar_conexion_rapida)
        
        form_layout.addWidget(self.btn_prueba_rapida)
        
        layout.addLayout(form_layout)
        
        return card
    
    def crear_area_feedback(self):
        """Crear área de feedback y resultados"""
        area = QWidget()
        area.setObjectName("areaFeedback")
        area.hide()  # Inicialmente oculta
        
        layout = QVBoxLayout(area)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(12)
        
        self.resultado_widget = QLabel()
        self.resultado_widget.setObjectName("resultadoPrueba")
        self.resultado_widget.setWordWrap(True)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressModerno")
        self.progress_bar.hide()
        
        layout.addWidget(self.resultado_widget)
        layout.addWidget(self.progress_bar)
        
        return area
    
    def crear_tutorial_expandible(self):
        """Crear tutorial expandible"""
        tutorial = QWidget()
        tutorial.setObjectName("tutorialExpandible")
        
        layout = QVBoxLayout(tutorial)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header del tutorial (clickeable)
        self.tutorial_header = QPushButton("📚 ¿Necesitas ayuda? Ver guía paso a paso")
        self.tutorial_header.setObjectName("tutorialHeader")
        self.tutorial_header.clicked.connect(self.toggle_tutorial)
        
        # Contenido del tutorial (inicialmente oculto)
        self.tutorial_content = QWidget()
        self.tutorial_content.setObjectName("tutorialContent")
        self.tutorial_content.hide()
        
        self.configurar_contenido_tutorial()
        
        layout.addWidget(self.tutorial_header)
        layout.addWidget(self.tutorial_content)
        
        return tutorial
    
    def configurar_contenido_tutorial(self):
        """Configurar el contenido del tutorial expandible"""
        layout = QVBoxLayout(self.tutorial_content)
        layout.setContentsMargins(24, 16, 24, 24)
        layout.setSpacing(16)
        
        # Pasos del tutorial
        pasos = [
            {
                "numero": "1️⃣",
                "titulo": "Crear Base de Datos en Notion",
                "contenido": "Crea una nueva página en Notion y agrega una base de datos con vista de tablero que incluya estas columnas:\n• Título (title) - Para el nombre del caso de prueba\n• Estado (select) - Opciones: Pendiente, En Progreso, Completado\n• Prioridad (select) - Opciones: Alta, Media, Baja\n• Descripción (text) - Para los detalles del caso\n• Pasos (text) - Para los pasos de ejecución\n• Resultado Esperado (text) - Para el resultado esperado"
            },
            {
                "numero": "2️⃣", 
                "titulo": "Configurar Vista de Tablero",
                "contenido": "Cambia la vista de tu base de datos a 'Tablero' (Board) y configura las columnas por Estado:\n• Columna 'Pendiente' para casos nuevos\n• Columna 'En Progreso' para casos en ejecución\n• Columna 'Completado' para casos finalizados\nEsto te permitirá gestionar los casos como tarjetas Kanban."
            },
            {
                "numero": "3️⃣",
                "titulo": "Hacer la Base de Datos Pública",
                "contenido": "Para poder acceder sin token de integración:\n• Ve a 'Compartir' en la esquina superior derecha\n• Activa 'Compartir en la web'\n• Configura los permisos como 'Puede editar' o 'Puede comentar'\n• Esto permitirá el acceso directo desde el ChatBot"
            },
            {
                "numero": "4️⃣",
                "titulo": "Obtener ID de Base de Datos",
                "contenido": "Copia la URL de tu base de datos. El ID está entre las barras después de notion.so/\nEjemplo: notion.so/miworkspace/1234567890abcdef1234567890abcdef → ID: 1234567890abcdef1234567890abcdef\n\n💡 El ID es la cadena de 32 caracteres hexadecimales en la URL"
            },
            {
                "numero": "5️⃣",
                "titulo": "Configurar Integración",
                "contenido": "Pega el ID de la base de datos en el campo de arriba y haz clic en 'Verificar Base de Datos' para confirmar que sea accesible desde el ChatBot."
            }
        ]
        
        for paso in pasos:
            paso_widget = QWidget()
            paso_widget.setObjectName("pasoTutorial")
            
            paso_layout = QHBoxLayout(paso_widget)
            paso_layout.setContentsMargins(16, 12, 16, 12)
            
            # Número del paso
            numero_label = QLabel(paso["numero"])
            numero_label.setObjectName("numeroPaso")
            numero_label.setFixedSize(32, 32)
            numero_label.setAlignment(Qt.AlignCenter)
            
            # Contenido del paso
            contenido_widget = QWidget()
            contenido_layout = QVBoxLayout(contenido_widget)
            contenido_layout.setContentsMargins(0, 0, 0, 0)
            contenido_layout.setSpacing(4)
            
            titulo_paso = QLabel(paso["titulo"])
            titulo_paso.setObjectName("tituloPaso")
            
            descripcion_paso = QLabel(paso["contenido"])
            descripcion_paso.setObjectName("descripcionPaso")
            descripcion_paso.setWordWrap(True)
            
            contenido_layout.addWidget(titulo_paso)
            contenido_layout.addWidget(descripcion_paso)
            
            paso_layout.addWidget(numero_label)
            paso_layout.addWidget(contenido_widget)
            
            layout.addWidget(paso_widget)
        
        # Enlace directo
        enlace_widget = QWidget()
        enlace_widget.setObjectName("enlaceDirecto")
        enlace_layout = QHBoxLayout(enlace_widget)
        enlace_layout.setContentsMargins(16, 12, 16, 12)
        
        enlace_label = QLabel("🔗 <a href='https://notion.so' style='color: #0066cc; text-decoration: none;'>Ir a Notion para crear tu base de datos</a>")
        enlace_label.setOpenExternalLinks(True)
        enlace_label.setObjectName("enlaceNotion")
        
        enlace_layout.addWidget(enlace_label)
        enlace_layout.addStretch()
        
        layout.addWidget(enlace_widget)
    
    def crear_footer(self):
        """Crear footer con botones de acción"""
        footer = QWidget()
        footer.setObjectName("footerModerno")
        footer.setFixedHeight(72)
        
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(32, 16, 32, 16)
        
        # Botón principal
        self.btn_guardar = QPushButton("💾 Guardar Configuración")
        self.btn_guardar.setObjectName("botonPrincipal")
        
        # Botón secundario
        btn_cerrar = QPushButton("Cancelar")
        btn_cerrar.setObjectName("botonSecundario")
        btn_cerrar.clicked.connect(self.close)
        
        layout.addWidget(btn_cerrar)
        layout.addStretch()
        layout.addWidget(self.btn_guardar)
        
        self.btn_guardar.clicked.connect(self.guardar_configuracion)
        
        return footer
    
    def toggle_tutorial(self):
        """Mostrar/ocultar tutorial"""
        if self.tutorial_content.isVisible():
            self.tutorial_content.hide()
            self.tutorial_header.setText("📚 ¿Necesitas ayuda? Ver guía paso a paso")
        else:
            self.tutorial_content.show()
            self.tutorial_header.setText("📚 Ocultar guía")
    
    def actualizar_estado(self, icono, texto, color="#666666"):
        """Actualizar estado de conexión"""
        self.icono_estado.setText(icono)
        self.texto_estado.setText(texto)
        self.texto_estado.setStyleSheet(f"color: {color};")
    
    def mostrar_feedback(self, mensaje, tipo="info"):
        """Mostrar feedback al usuario"""
        colores = {
            "success": "#28a745",
            "error": "#dc3545", 
            "warning": "#ffc107",
            "info": "#17a2b8"
        }
        
        iconos = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        color = colores.get(tipo, colores["info"])
        icono = iconos.get(tipo, iconos["info"])
        
        self.resultado_widget.setText(f"{icono} {mensaje}")
        self.resultado_widget.setStyleSheet(f"color: {color}; font-weight: 500;")
        self.area_feedback.show()
    
    def probar_conexion_rapida(self):
        """Prueba rápida de validación del ID de base de datos"""
        if self.conexion_en_progreso:
            return
            
        self.conexion_en_progreso = True
        self.btn_prueba_rapida.setEnabled(False)
        
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0)  # Modo indeterminado
        
        self.actualizar_estado("🔄", "Verificando base de datos...", "#17a2b8")
        self.mostrar_feedback("Validando ID de base de datos...", "info")
        
        # Simular validación asíncrona
        QTimer.singleShot(1500, self.completar_prueba_rapida)
    
    def completar_prueba_rapida(self):
        """Completar validación de base de datos"""
        database_id = self.input_database_id.text().strip()
        
        self.conexion_en_progreso = False
        self.btn_prueba_rapida.setEnabled(True)
        self.progress_bar.hide()
        
        if not database_id:
            self.actualizar_estado("❌", "Falta ID", "#dc3545")
            self.mostrar_feedback("Por favor ingresa el ID de la base de datos", "error")
            return
        
        # Validar formato del ID (32 caracteres hexadecimales)
        if len(database_id) != 32 or not all(c in '0123456789abcdefABCDEF' for c in database_id):
            self.actualizar_estado("❌", "ID inválido", "#dc3545")
            self.mostrar_feedback("El ID debe tener 32 caracteres hexadecimales", "error")
            return
        
        # ID válido en formato
        try:
            self.actualizar_estado("✅", "ID válido", "#28a745")
            self.mostrar_feedback("ID de base de datos válido. Configuración lista para guardar.", "success")
                
        except Exception as e:
            self.actualizar_estado("❌", "Error", "#dc3545")
            self.mostrar_feedback(f"Error de validación: {str(e)}", "error")
    
    def cargar_configuracion(self):
        """Cargar configuración existente"""
        try:
            config_manager = NotionConfigManager()
            config = config_manager.cargar_configuracion()
            
            if config.get('database_id'):
                self.input_database_id.setText(config['database_id'])
                self.actualizar_estado("✅", "Configurado", "#28a745")
                
        except Exception as e:
            print(f"Error cargando configuración: {e}")
    
    def guardar_configuracion(self):
        """Guardar configuración"""
        database_id = self.input_database_id.text().strip()
        
        if not database_id:
            self.mostrar_feedback("Por favor ingresa el ID de la base de datos", "error")
            return
        
        # Validar formato del ID
        if len(database_id) != 32 or not all(c in '0123456789abcdefABCDEF' for c in database_id):
            self.mostrar_feedback("El ID debe tener 32 caracteres hexadecimales", "error")
            return
        
        try:
            config_manager = NotionConfigManager()
            config_manager.guardar_configuracion("", database_id)  # Token vacío
            
            self.mostrar_feedback("Configuración guardada exitosamente", "success")
            self.actualizar_estado("✅", "Configurado", "#28a745")
            
            # Cerrar diálogo después de un momento
            QTimer.singleShot(1500, self.accept)
            
        except Exception as e:
            self.mostrar_feedback(f"Error guardando configuración: {str(e)}", "error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = NotionConfigDialog()
    dialog.show()
    sys.exit(app.exec_())
