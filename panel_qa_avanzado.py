"""
Panel de Opciones Avanzadas para QA
"""
import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QTabWidget, QWidget, QComboBox,
                           QCheckBox, QSlider, QLineEdit, QMessageBox, QFormLayout,
                           QGroupBox, QScrollArea, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class PanelQAAvanzado(QDialog):
    """Panel avanzado de opciones QA con mejor visibilidad"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("🚀 Panel QA Avanzado - Herramientas Profesionales")
        self.setGeometry(150, 150, 1000, 700)
        self.setMinimumSize(900, 650)
        self.configurar_ui()
        self.aplicar_estilos_mejorados()
        
    def configurar_ui(self):
        """Configurar la interfaz con mejor visibilidad"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # ENCABEZADO MEJORADO
        header_layout = QVBoxLayout()
        
        titulo_principal = QLabel("🎯 PANEL QA PROFESIONAL")
        titulo_principal.setObjectName("tituloPrincipal")
        titulo_principal.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(titulo_principal)
        
        subtitulo = QLabel("Herramientas especializadas para Quality Assurance y Testing")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitulo)
        
        layout.addLayout(header_layout)
        
        # TABS MEJORADOS
        self.tabs = QTabWidget()
        self.tabs.setObjectName("tabsQA")
        
        # Tab 1: API Testing & Automation
        tab_api = QWidget()
        self.configurar_tab_api(tab_api)
        self.tabs.addTab(tab_api, "🔌 API Testing")
        
        # Tab 2: Test Cases & Documentation
        tab_docs = QWidget()
        self.configurar_tab_documentacion(tab_docs)
        self.tabs.addTab(tab_docs, "📋 Test Cases")
        
        # Tab 3: Automation Scripts
        tab_auto = QWidget()
        self.configurar_tab_automatizacion(tab_auto)
        self.tabs.addTab(tab_auto, "🤖 Automation")
        
        # Tab 4: Security & Performance
        tab_perf = QWidget()
        self.configurar_tab_performance(tab_perf)
        self.tabs.addTab(tab_perf, "🔒 Security & Perf")
        
        # Tab 5: Mobile & Accessibility
        tab_mobile = QWidget()
        self.configurar_tab_mobile(tab_mobile)
        self.tabs.addTab(tab_mobile, "📱 Mobile & A11y")
        
        # Tab 6: Integration & CI/CD
        tab_cicd = QWidget()
        self.configurar_tab_cicd(tab_cicd)
        self.tabs.addTab(tab_cicd, "⚙️ CI/CD")
        
        # Tab 7: Reports & Analytics
        tab_reports = QWidget()
        self.configurar_tab_reports(tab_reports)
        self.tabs.addTab(tab_reports, "📊 Reports")
        
        layout.addWidget(self.tabs)
        
        # BOTONES INFERIORES MEJORADOS
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(15)
        
        btn_help = QPushButton("💡 Ayuda QA")
        btn_help.setObjectName("botonHelp")
        btn_help.clicked.connect(self.mostrar_ayuda)
        
        btn_export = QPushButton("📤 Exportar Configuración")
        btn_export.setObjectName("botonExport")
        btn_export.clicked.connect(self.exportar_config)
        
        btn_cerrar = QPushButton("❌ Cerrar")
        btn_cerrar.setObjectName("botonCerrar")
        btn_cerrar.clicked.connect(self.close)
        
        botones_layout.addWidget(btn_help)
        botones_layout.addWidget(btn_export)
        botones_layout.addStretch()
        botones_layout.addWidget(btn_cerrar)
        
        layout.addLayout(botones_layout)
    
    def crear_seccion_herramientas(self, parent, titulo, herramientas):
        """Crear una sección de herramientas con mejor organización"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollArea")
        
        contenido = QWidget()
        layout = QVBoxLayout(contenido)
        layout.setSpacing(15)
        
        # Título de sección
        titulo_seccion = QLabel(titulo)
        titulo_seccion.setObjectName("tituloSeccion")
        layout.addWidget(titulo_seccion)
        
        # Botones de herramientas
        for nombre, descripcion, metodo in herramientas:
            grupo = QGroupBox()
            grupo.setObjectName("grupoHerramienta")
            
            grupo_layout = QVBoxLayout(grupo)
            
            btn = QPushButton(nombre)
            btn.setObjectName("botonHerramienta")
            btn.clicked.connect(metodo)
            
            desc_label = QLabel(descripcion)
            desc_label.setObjectName("descripcionHerramienta")
            desc_label.setWordWrap(True)
            
            grupo_layout.addWidget(btn)
            grupo_layout.addWidget(desc_label)
            
            layout.addWidget(grupo)
        
        layout.addStretch()
        scroll.setWidget(contenido)
        
        main_layout = QVBoxLayout(parent)
        main_layout.addWidget(scroll)
    
    def configurar_tab_api(self, tab):
        """Tab para API Testing & Automation"""
        herramientas = [
            ("🔍 Casos de Prueba API REST", "Genera casos de prueba completos para APIs REST con validaciones", self.generar_casos_api),
            ("📝 Colección Postman", "Crea colecciones de Postman con tests automatizados", self.generar_postman),
            ("🔧 Scripts cURL", "Genera scripts cURL para testing manual y CI/CD", self.generar_curl),
            ("⚡ Tests de Performance API", "Diseña tests de carga y stress para APIs", self.generar_api_performance),
            ("🛡️ Security Testing API", "Implementa tests de seguridad para endpoints", self.generar_api_security),
            ("📊 Documentación API", "Genera documentación técnica de APIs", self.generar_api_docs)
        ]
        self.crear_seccion_herramientas(tab, "🔌 API Testing & Automation Tools", herramientas)
    
    def configurar_tab_documentacion(self, tab):
        """Tab para Test Cases & Documentation"""
        herramientas = [
            ("📋 Plan de Pruebas Completo", "Crea plan de pruebas siguiendo IEEE 829", self.generar_plan_pruebas),
            ("✅ Casos de Prueba BDD", "Genera casos en formato Gherkin/Cucumber", self.generar_casos_bdd),
            ("🎯 Matriz de Trazabilidad", "Crea RTM (Requirements Traceability Matrix)", self.generar_rtm),
            ("📑 Checklist Pre-Deploy", "Lista de verificación antes de producción", self.generar_checklist),
            ("📈 Estrategia de Testing", "Desarrolla estrategia integral de QA", self.generar_estrategia),
            ("🔍 Test Cases Exploratorios", "Diseña sesiones de testing exploratorio", self.generar_exploratoria)
        ]
        self.crear_seccion_herramientas(tab, "📋 Test Cases & Documentation", herramientas)
    
    def configurar_tab_automatizacion(self, tab):
        """Tab para Automation Scripts"""
        herramientas = [
            ("🕷️ Scripts Selenium", "Genera automation con Selenium WebDriver", self.generar_selenium),
            ("🌲 Tests Cypress", "Crea tests end-to-end con Cypress", self.generar_cypress),
            ("🎭 Scripts Playwright", "Automation moderna con Playwright", self.generar_playwright),
            ("🔄 Framework TestNG/JUnit", "Estructura de testing para Java", self.generar_java_framework),
            ("🐍 PyTest Framework", "Framework de testing para Python", self.generar_pytest),
            ("⚙️ Page Object Model", "Implementa patrón POM", self.generar_pom)
        ]
        self.crear_seccion_herramientas(tab, "🤖 Automation Scripts & Frameworks", herramientas)
    
    def configurar_tab_performance(self, tab):
        """Tab para Security & Performance"""
        herramientas = [
            ("⚡ Tests JMeter", "Scripts de performance con Apache JMeter", self.generar_jmeter),
            ("📊 Tests K6", "Modern load testing con Grafana K6", self.generar_k6),
            ("🔒 Análisis de Vulnerabilidades", "Tests de seguridad OWASP", self.generar_security_scan),
            ("🛡️ Penetration Testing", "Guías de pentesting manual", self.generar_pentest),
            ("🔐 Tests de Autenticación", "Validación de sistemas de auth", self.generar_auth_tests),
            ("📈 Monitoreo de Performance", "Métricas y alertas de rendimiento", self.generar_monitoring)
        ]
        self.crear_seccion_herramientas(tab, "🔒 Security & Performance Testing", herramientas)
    
    def configurar_tab_mobile(self, tab):
        """Tab para Mobile & Accessibility"""
        herramientas = [
            ("📱 Tests Mobile Automation", "Appium para iOS/Android", self.generar_appium),
            ("♿ Auditoría WCAG", "Tests de accesibilidad web", self.generar_accessibility),
            ("📐 Tests Responsive", "Validación de diseño responsive", self.generar_responsive),
            ("🔋 Performance Mobile", "Tests de batería y recursos", self.generar_mobile_perf),
            ("🌐 Cross-Browser Testing", "Compatibilidad entre navegadores", self.generar_cross_browser),
            ("👥 Tests de Usabilidad", "Evaluación UX/UI", self.generar_usability)
        ]
        self.crear_seccion_herramientas(tab, "📱 Mobile & Accessibility Testing", herramientas)
    
    def configurar_tab_cicd(self, tab):
        """Tab para Integration & CI/CD"""
        herramientas = [
            ("🔄 Pipeline Jenkins", "Configuración CI/CD con Jenkins", self.generar_jenkins),
            ("🐳 Docker Testing", "Containerización de tests", self.generar_docker_tests),
            ("☁️ Tests en Cloud", "AWS/Azure testing automation", self.generar_cloud_tests),
            ("🔀 Git Hooks QA", "Hooks de calidad en commits", self.generar_git_hooks),
            ("🎯 Quality Gates", "Configuración de quality gates", self.generar_quality_gates),
            ("📦 Tests de Integración", "Integration testing strategies", self.generar_integration_tests)
        ]
        self.crear_seccion_herramientas(tab, "⚙️ Integration & CI/CD Testing", herramientas)
    
    def configurar_tab_reports(self, tab):
        """Tab para Reports & Analytics"""
        herramientas = [
            ("📊 Dashboard QA", "Métricas y KPIs de calidad", self.generar_dashboard),
            ("📈 Reportes Allure", "Reports avanzados con Allure", self.generar_allure),
            ("📋 Test Summary Report", "Resumen ejecutivo de testing", self.generar_test_summary),
            ("🔍 Root Cause Analysis", "Análisis de causas raíz", self.generar_rca),
            ("📉 Trend Analysis", "Análisis de tendencias QA", self.generar_trends),
            ("🎯 ROI Testing Report", "Retorno de inversión en QA", self.generar_roi)
        ]
        self.crear_seccion_herramientas(tab, "📊 Reports & Analytics", herramientas)
    
    def enviar_comando(self, comando):
        """Enviar comando al campo de texto principal SIN enviar automáticamente"""
        prompt_qa = f"""🎯 EXPERTO QA PROFESIONAL ACTIVADO

CONTEXTO: Actúa como un Senior QA Engineer con 10+ años de experiencia en testing de software, especializado en metodologías ágiles, automation, performance testing y security testing.

SOLICITUD: {comando}

INSTRUCCIONES:
✅ Responde con nivel profesional y detallado siguiendo SIEMPRE este formato estructurado:

# 📌 [TÍTULO PRINCIPAL DE LA RESPUESTA]
Breve introducción explicativa (máximo 2-3 líneas).

## 1️⃣ **Objetivo**
Descripción breve y clara del propósito.

## 2️⃣ **Alcance** 
Qué está incluido y excluido.

## 3️⃣ **Estructura Detallada**
Lista de puntos principales con títulos y descripciones.

## 4️⃣ **Recomendaciones**
Consejos prácticos y buenas prácticas.

## 5️⃣ **Conclusión**
Resumen de lo más importante.

✅ Incluye mejores prácticas de la industria
✅ Proporciona ejemplos prácticos y código cuando sea relevante
✅ Considera aspectos de CI/CD y DevOps
✅ Incluye métricas y KPIs cuando sea aplicable
✅ Usa terminología técnica apropiada de QA"""
        
        if self.parent_window and hasattr(self.parent_window, 'entrada_texto'):
            self.close()
            self.parent_window.entrada_texto.setPlainText(prompt_qa)
            # NO llamar a enviar_mensaje() automáticamente
            self.parent_window.entrada_texto.setFocus()  # Enfocar el campo de texto
        else:
            QMessageBox.information(self, "Comando QA Profesional", prompt_qa)
    
    # Métodos para cada herramienta QA
    def generar_casos_api(self):
        self.enviar_comando("Genera casos de prueba completos para testing de API REST, incluyendo casos positivos, negativos, de borde, validaciones de esquema JSON, códigos de estado HTTP, autenticación y manejo de errores.")
    
    def generar_postman(self):
        self.enviar_comando("Crea una colección completa de Postman con tests automatizados, variables de entorno, scripts pre-request, validaciones de respuesta y documentación de API.")
    
    def generar_curl(self):
        self.enviar_comando("Genera scripts cURL para testing manual de APIs, incluyendo diferentes métodos HTTP, headers, autenticación y ejemplos para CI/CD pipelines.")
    
    def generar_api_performance(self):
        self.enviar_comando("Diseña tests de performance para APIs usando JMeter o K6, incluyendo tests de carga, stress, spike y endurance con métricas y thresholds.")
    
    def generar_api_security(self):
        self.enviar_comando("Implementa tests de seguridad para APIs basados en OWASP API Security Top 10, incluyendo authentication, authorization, injection, y rate limiting.")
    
    def generar_api_docs(self):
        self.enviar_comando("Genera documentación técnica completa de API incluyendo especificación OpenAPI/Swagger, ejemplos de uso y guías de testing.")
    
    def generar_plan_pruebas(self):
        self.enviar_comando("Crea un plan de pruebas completo siguiendo el estándar IEEE 829, incluyendo scope, approach, resources, schedule, risks y criterios de entrada/salida.")
    
    def generar_casos_bdd(self):
        self.enviar_comando("Genera casos de prueba en formato BDD usando Gherkin (Given-When-Then), incluyendo escenarios, ejemplos y integración con Cucumber/SpecFlow.")
    
    def generar_rtm(self):
        self.enviar_comando("Crea una Matriz de Trazabilidad de Requisitos (RTM) que mapee requirements con test cases, incluyendo coverage analysis y gap identification.")
    
    def generar_checklist(self):
        self.enviar_comando("Genera un checklist completo de QA para revisión pre-deploy, incluyendo functional, performance, security, usability y compatibility testing.")
    
    def generar_estrategia(self):
        self.enviar_comando("Desarrolla una estrategia integral de testing incluyendo test pyramid, shift-left approach, automation strategy y risk-based testing.")
    
    def generar_exploratoria(self):
        self.enviar_comando("Diseña sesiones de testing exploratorio estructuradas con charter, time-boxing, note-taking templates y session-based test management.")
    
    def generar_selenium(self):
        self.enviar_comando("Genera framework de automation con Selenium WebDriver, incluyendo Page Object Model, TestNG/JUnit, reporting y CI/CD integration.")
    
    def generar_cypress(self):
        self.enviar_comando("Crea tests end-to-end con Cypress incluyendo custom commands, fixtures, intercepts, visual testing y parallel execution.")
    
    def generar_playwright(self):
        self.enviar_comando("Implementa automation moderna con Playwright incluyendo cross-browser testing, auto-waiting, mobile emulation y trace viewer.")
    
    def generar_java_framework(self):
        self.enviar_comando("Crea framework de testing en Java con TestNG/JUnit, Maven/Gradle, Allure reporting y integration con Selenium/RestAssured.")
    
    def generar_pytest(self):
        self.enviar_comando("Desarrolla framework de testing en Python con PyTest, fixtures, parameterization, plugins y integration con CI/CD.")
    
    def generar_pom(self):
        self.enviar_comando("Implementa Page Object Model pattern con encapsulation, reusability, maintainability y integration con automation frameworks.")
    
    def generar_jmeter(self):
        self.enviar_comando("Crea scripts de performance testing con Apache JMeter incluyendo thread groups, listeners, assertions y distributed testing.")
    
    def generar_k6(self):
        self.enviar_comando("Desarrolla tests de performance con Grafana K6 incluyendo load testing, stress testing, spike testing y integration con monitoring.")
    
    def generar_security_scan(self):
        self.enviar_comando("Implementa análisis de vulnerabilidades basado en OWASP Top 10, incluyendo SAST, DAST, dependency scanning y security testing automation.")
    
    def generar_pentest(self):
        self.enviar_comando("Crea guías de penetration testing manual incluyendo reconnaissance, scanning, exploitation, post-exploitation y reporting.")
    
    def generar_auth_tests(self):
        self.enviar_comando("Desarrolla tests de sistemas de autenticación y autorización incluyendo OAuth, JWT, session management y security headers.")
    
    def generar_monitoring(self):
        self.enviar_comando("Implementa monitoreo de performance con métricas, alertas, dashboards y integration con APM tools como New Relic, DataDog.")
    
    def generar_appium(self):
        self.enviar_comando("Crea automation para mobile testing con Appium incluyendo iOS/Android, gestures, device farms y parallel execution.")
    
    def generar_accessibility(self):
        self.enviar_comando("Implementa auditoría de accesibilidad WCAG 2.1/2.2 incluyendo automated tools, manual testing y compliance reporting.")
    
    def generar_responsive(self):
        self.enviar_comando("Desarrolla tests de diseño responsive incluyendo breakpoints, cross-device testing y visual regression testing.")
    
    def generar_mobile_perf(self):
        self.enviar_comando("Crea tests de performance móvil incluyendo battery usage, memory consumption, network efficiency y app startup time.")
    
    def generar_cross_browser(self):
        self.enviar_comando("Implementa cross-browser testing strategy incluyendo browser matrix, cloud testing platforms y automation frameworks.")
    
    def generar_usability(self):
        self.enviar_comando("Desarrolla evaluación de usabilidad UX/UI incluyendo heuristic evaluation, user journey testing y accessibility considerations.")
    
    def generar_jenkins(self):
        self.enviar_comando("Configura pipeline CI/CD con Jenkins incluyendo automated testing, quality gates, parallel execution y reporting integration.")
    
    def generar_docker_tests(self):
        self.enviar_comando("Implementa containerización de tests con Docker incluyendo test environments, database setup y microservices testing.")
    
    def generar_cloud_tests(self):
        self.enviar_comando("Desarrolla testing automation en cloud (AWS/Azure/GCP) incluyendo infrastructure testing, scalability y cost optimization.")
    
    def generar_git_hooks(self):
        self.enviar_comando("Crea Git hooks para quality assurance incluyendo pre-commit tests, code quality checks y automated testing triggers.")
    
    def generar_quality_gates(self):
        self.enviar_comando("Configura quality gates incluyendo code coverage thresholds, security scans, performance benchmarks y compliance checks.")
    
    def generar_integration_tests(self):
        self.enviar_comando("Implementa integration testing strategy incluyendo API integration, database testing, message queues y microservices testing.")
    
    def generar_dashboard(self):
        self.enviar_comando("Crea dashboard de métricas QA incluyendo test execution trends, defect analysis, coverage metrics y team productivity KPIs.")
    
    def generar_allure(self):
        self.enviar_comando("Implementa reporting avanzado con Allure incluyendo test results, historical trends, flaky tests analysis y team collaboration.")
    
    def generar_test_summary(self):
        self.enviar_comando("Genera resumen ejecutivo de testing incluyendo test execution summary, quality metrics, risk assessment y recommendations.")
    
    def generar_rca(self):
        self.enviar_comando("Desarrolla análisis de causas raíz (RCA) para defectos incluyendo 5 whys, fishbone diagram y preventive actions.")
    
    def generar_trends(self):
        self.enviar_comando("Crea análisis de tendencias QA incluyendo defect trends, test execution patterns, automation ROI y quality improvements.")
    
    def generar_roi(self):
        self.enviar_comando("Calcula ROI de testing automation incluyendo cost-benefit analysis, time savings, quality improvements y business impact.")
    
    def mostrar_ayuda(self):
        """Mostrar ayuda del panel QA con mejor contraste"""
        # Crear diálogo personalizado
        dialog = QDialog(self)
        dialog.setWindowTitle("💡 Ayuda del Panel QA")
        dialog.setGeometry(300, 300, 700, 600)
        dialog.setMinimumSize(650, 550)
        
        # Layout principal
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Título
        titulo = QLabel("💡 AYUDA DEL PANEL QA AVANZADO")
        titulo.setObjectName("tituloAyudaQA")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Área de contenido con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("scrollAyudaQA")
        
        contenido_html = """
        <div style='font-family: Segoe UI; color: #1F2937; background-color: #FFFFFF; padding: 20px; border-radius: 15px;'>
            <h2 style='color: #4C5BFF; margin-top: 0;'>🎯 Este panel contiene herramientas profesionales para QA</h2>
            
            <h3 style='color: #DC2626;'>📋 TABS DISPONIBLES:</h3>
            <ul style='color: #1F2937; line-height: 1.8; font-size: 15px;'>
                <li><strong>🔌 API Testing:</strong> Herramientas para testing de APIs</li>
                <li><strong>📋 Test Cases:</strong> Documentación y casos de prueba</li>
                <li><strong>🤖 Automation:</strong> Scripts y frameworks de automation</li>
                <li><strong>🔒 Security & Perf:</strong> Testing de seguridad y performance</li>
                <li><strong>📱 Mobile & A11y:</strong> Testing móvil y accesibilidad</li>
                <li><strong>⚙️ CI/CD:</strong> Integración continua y deployment</li>
                <li><strong>📊 Reports:</strong> Reportes y análisis de métricas</li>
            </ul>
            
            <h3 style='color: #DC2626;'>🚀 CÓMO USAR:</h3>
            <ol style='color: #1F2937; line-height: 1.8; font-size: 15px;'>
                <li>Selecciona el tab correspondiente a tu necesidad</li>
                <li>Haz clic en la herramienta deseada</li>
                <li>El comando se colocará en el campo de texto del chat</li>
                <li>Presiona Enter para obtener una respuesta profesional y detallada</li>
            </ol>
            
            <h3 style='color: #DC2626;'>⭐ TIPS:</h3>
            <ul style='color: #1F2937; line-height: 1.8; font-size: 15px;'>
                <li>Cada herramienta genera contenido profesional</li>
                <li>Incluye mejores prácticas de la industria</li>
                <li>Proporciona ejemplos prácticos y código</li>
                <li>Considera aspectos de CI/CD y DevOps</li>
                <li>Las respuestas siguen formato estructurado profesional</li>
            </ul>
        </div>
        """
        
        contenido_label = QLabel()
        contenido_label.setWordWrap(True)
        contenido_label.setTextFormat(Qt.RichText)
        contenido_label.setText(contenido_html)
        contenido_label.setObjectName("contenidoAyudaQA")
        
        scroll.setWidget(contenido_label)
        layout.addWidget(scroll)
        
        # Botón cerrar
        btn_cerrar = QPushButton("❌ Cerrar")
        btn_cerrar.setObjectName("botonCerrarAyudaQA")
        btn_cerrar.clicked.connect(dialog.close)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cerrar)
        layout.addLayout(btn_layout)
        
        # Aplicar estilos
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #0B1D4A, stop: 1 #1F2A56);
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            #tituloAyudaQA {
                font-size: 24px;
                font-weight: bold;
                color: #FFFFFF;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #4C5BFF, stop: 1 #6366F1);
                padding: 20px;
                border-radius: 15px;
                border: 2px solid #FFFFFF;
                margin: 10px;
            }
            
            #scrollAyudaQA {
                border: 2px solid #4C5BFF;
                border-radius: 15px;
                background: #FFFFFF;
            }
            
            #contenidoAyudaQA {
                background: #FFFFFF;
                color: #1F2937;
                padding: 15px;
                font-size: 16px;
                line-height: 1.6;
            }
            
            #botonCerrarAyudaQA {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #DC2626, stop: 1 #EF4444);
                color: #FFFFFF;
                border: 2px solid #FFFFFF;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 15px 25px;
                min-width: 100px;
            }
            
            #botonCerrarAyudaQA:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #EF4444, stop: 1 #F87171);
                border: 2px solid #FFD700;
            }
            
            QScrollBar:vertical {
                background: #1B243A;
                width: 15px;
                border-radius: 7px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #4C5BFF;
                border-radius: 7px;
                min-height: 30px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #6366F1;
            }
        """)
        
        dialog.exec_()
    
    def exportar_config(self):
        """Exportar configuración"""
        QMessageBox.information(self, "Exportar", "📤 Función de exportación en desarrollo")
    
    def aplicar_estilos_mejorados(self):
        """Aplicar estilos CSS mejorados con mejor visibilidad"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #0B1D4A, stop: 1 #1F2A56);
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            #tituloPrincipal {
                font-size: 28px;
                font-weight: bold;
                color: #FFFFFF;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #4C5BFF, stop: 1 #6366F1);
                padding: 20px;
                border-radius: 15px;
                border: 3px solid #FFFFFF;
                margin: 10px;
            }
            
            #subtitulo {
                font-size: 16px;
                color: #E2E8F0;
                background: #1E3058;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #4C5BFF;
                margin: 5px;
            }
            
            #tabsQA::pane {
                border: 3px solid #4C5BFF;
                border-radius: 20px;
                background: #141F3C;
                padding: 15px;
                margin-top: 10px;
            }
            
            #tabsQA::tab-bar {
                alignment: center;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #1E3058, stop: 1 #2D4A7B);
                color: #FFFFFF;
                padding: 18px 25px;
                margin: 3px;
                border-radius: 12px;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #4C5BFF;
                min-width: 120px;
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
            
            #tituloSeccion {
                font-size: 20px;
                font-weight: bold;
                color: #FFFFFF;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #1E3058, stop: 1 #2D3748);
                padding: 15px;
                border-radius: 12px;
                border: 2px solid #4C5BFF;
                margin: 10px 0;
            }
            
            #grupoHerramienta {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #1A2332, stop: 1 #2D3748);
                border: 2px solid #4C5BFF;
                border-radius: 15px;
                padding: 15px;
                margin: 8px;
            }
            
            #grupoHerramienta:hover {
                border: 2px solid #FFD700;
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #2A3441, stop: 1 #3D4A57);
            }
            
            #botonHerramienta {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #4C5BFF, stop: 1 #6366F1);
                color: #FFFFFF;
                border: 2px solid #FFFFFF;
                border-radius: 12px;
                padding: 15px 25px;
                font-size: 16px;
                font-weight: bold;
                margin: 5px;
            }
            
            #botonHerramienta:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #6366F1, stop: 1 #7C3AED);
                border: 2px solid #FFD700;
                color: #FFFFFF;
                transform: scale(1.02);
            }
            
            #botonHerramienta:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #3B4BCC, stop: 1 #5A47F3);
                color: #FFFFFF;
            }
            
            #descripcionHerramienta {
                color: #F1F5F9;
                font-size: 13px;
                line-height: 1.4;
                padding: 8px;
                background: #0F1419;
                border-radius: 8px;
                border: 1px solid #374151;
                margin: 5px 0;
            }
            
            #scrollArea {
                border: 2px solid #4C5BFF;
                border-radius: 15px;
                background: #141F3C;
            }
            
            #botonConfig, #botonHelp, #botonExport {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #1E3058, stop: 1 #2D3748);
                color: #FFFFFF;
                border: 2px solid #4C5BFF;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                padding: 15px 25px;
                min-width: 150px;
            }
            
            #botonConfig:hover, #botonHelp:hover, #botonExport:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #4C5BFF, stop: 1 #6366F1);
                border: 2px solid #FFD700;
                color: #FFFFFF;
            }
            
            #botonCerrar {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #DC2626, stop: 1 #EF4444);
                color: #FFFFFF;
                border: 2px solid #FFFFFF;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                padding: 15px 25px;
                min-width: 100px;
            }
            
            #botonCerrar:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #EF4444, stop: 1 #F87171);
                border: 2px solid #FFD700;
                color: #FFFFFF;
            }
            
            QScrollBar:vertical {
                background: #1B243A;
                width: 15px;
                border-radius: 7px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background: #4C5BFF;
                border-radius: 7px;
                min-height: 30px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #6366F1;
            }
        """)

# Test independiente
if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = PanelQAAvanzado()
    panel.show()
    sys.exit(app.exec_())
