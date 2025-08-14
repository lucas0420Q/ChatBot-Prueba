"""
Panel de Opciones Avanzadas para QA
"""
import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QTabWidget, QWidget, QComboBox,
                           QCheckBox, QSlider, QLineEdit, QMessageBox, QFormLayout,
                           QGroupBox, QScrollArea, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Importar configuración de Notion y estilos
from notion_config_dialog import NotionConfigDialog
from notion_integration import NotionIntegration
from estilos_ui import obtener_estilos_panel_qa

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
        self.tabs.addTab(tab_docs, "📋 Test Cases & Docs")
        
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
        botones_layout.setSpacing(20)
        botones_layout.setContentsMargins(10, 10, 10, 10)
        
        btn_help = QPushButton("💡 Ayuda QA")
        btn_help.setObjectName("botonHelp")
        btn_help.setMinimumHeight(50)
        btn_help.clicked.connect(self.mostrar_ayuda)
        
        btn_notion = QPushButton("🔗 Configurar Notion")
        btn_notion.setObjectName("botonNotion")
        btn_notion.setMinimumHeight(50)
        btn_notion.clicked.connect(self.configurar_notion)
        
        btn_export = QPushButton("� Exportar Automáticamente a Notion")
        btn_export.setObjectName("botonExportNotion")
        btn_export.setMinimumHeight(50)
        btn_export.clicked.connect(self.exportar_a_notion)
        
        btn_generar_exportar = QPushButton("🚀 Generar y Exportar Casos")
        btn_generar_exportar.setObjectName("botonGenerarExportar")
        btn_generar_exportar.setMinimumHeight(50)
        btn_generar_exportar.clicked.connect(self.generar_y_exportar_casos)
        
        btn_cerrar = QPushButton("❌ Cerrar")
        btn_cerrar.setObjectName("botonCerrar")
        btn_cerrar.setMinimumHeight(50)
        btn_cerrar.clicked.connect(self.close)
        
        botones_layout.addWidget(btn_help)
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
            ("📖 Manual de Usuario", "Genera manual de usuario completo y profesional", self.generar_manual_usuario),
            ("✅ Casos de Prueba BDD", "Genera casos en formato Gherkin/Cucumber", self.generar_casos_bdd),
            ("� Casos de Prueba → Notion", "Genera casos formato estándar para documentar en Notion", self.generar_casos_notion),
            ("��🗂️ Casos de Prueba → Completos", "Genera casos en AMBOS formatos: Estándar + JSON", self.generar_casos_completos),
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
        prompt_qa = f"""🎯 **Senior QA Engineer con 10+ años de experiencia**

**SOLICITUD:** {comando}

**FORMATO DE RESPUESTA:**
# 📌 [TÍTULO DE LA RESPUESTA]

## 🎯 **Objetivo y Alcance**
[Descripción clara del propósito]

## 📋 **Contenido Principal**
[Casos de prueba, documentación o análisis según solicitud]

## ✅ **Recomendaciones QA**
[Mejores prácticas y consejos técnicos]

**INSTRUCCIONES:**
✅ Formato profesional con terminología QA apropiada
✅ Responder exactamente según el formato solicitado
✅ Si se piden múltiples formatos, incluir TODOS
✅ Separadores visuales: ═══════════════════════════════════════════════════════════
✅ Incluir mejores prácticas de la industria y ejemplos prácticos"""
        
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
    
    def generar_manual_usuario(self):
        self.enviar_comando("Actúa como experto en documentación técnica y genera un MANUAL DE USUARIO COMPLETO siguiendo la plantilla estándar. Incluye: 1) Estructura completa con índice, introducción, información general, guía de usuario, funcionalidades detalladas, casos de uso comunes, solución de problemas y anexos. 2) Para cada funcionalidad, describe el propósito, cuándo usar, pasos detallados paso a paso, consejos útiles y solución de problemas. 3) Lenguaje claro y accesible para usuarios finales. 4) Ejemplos prácticos y casos de uso reales. 5) Formato profesional con estructura jerárquica. Enfócate en CÓMO usar el sistema, no en validarlo.")
    
    def generar_casos_bdd(self):
        self.enviar_comando("Genera casos de prueba en formato BDD usando Gherkin (Given-When-Then), incluyendo escenarios, ejemplos y integración con Cucumber/SpecFlow.")
    
    def generar_casos_notion(self):
        self.enviar_comando("""Genera casos de prueba en formato específico para Notion con emojis y estructura detallada.

**FORMATO EXACTO REQUERIDO PARA CADA CASO:**

[ID del Caso de Prueba] [Título del Caso de Prueba]

📄 Descripción
[Escribe aquí la descripción detallada del caso de prueba, indicando el objetivo y qué se validará.]

📅 Fecha de creación
[Fecha actual: 12/08/2025]

🔢 Nº ID
[ID numérico: 1, 2, 3, etc.]

🗂 Módulo
[Nombre del módulo correspondiente]

✅ Paso la prueba
[SI / NO - inicialmente "Pendiente"]

🚨 Prioridad
[Alta / Media / Baja]

🔄 Status
[En curso / Pendiente / Completado - inicialmente "Pendiente"]

📌 Proyectos
[Nombre del proyecto]

🎯 Resultado esperado
[Describe el resultado esperado de la ejecución del caso de prueba, con criterios claros de aceptación.]

Comentarios
[Espacio para comentarios adicionales - inicialmente vacío o con notas relevantes]

Pasos a seguir:

[Primer paso del caso de prueba]

[Segundo paso del caso de prueba]

[Tercer paso, y así sucesivamente]

---

**INSTRUCCIONES ESPECÍFICAS:**
✅ Usa EXACTAMENTE el formato mostrado arriba con todos los emojis
✅ Numera los casos como CP-1, CP-2, CP-3, etc.
✅ Incluye fecha actual (12/08/2025)
✅ Varía las prioridades entre Alta, Media y Baja
✅ Status inicial siempre "Pendiente"
✅ Incluye módulos relevantes para el sistema
✅ Pasos detallados y específicos numerados
✅ Resultados esperados claros y medibles
✅ Genera mínimo 15-20 casos de prueba completos
✅ Separa cada caso con --- al final
✅ Formato optimizado para copiar y pegar en Notion

**IMPORTANTE:** Este formato está diseñado específicamente para ser copiado directamente a Notion manteniendo toda la estructura y emojis.""")
    
    def generar_casos_json(self):
        self.enviar_comando("""Genera casos de prueba en formato estándar detallado Y JSON estructurado.

**FORMATO ESTÁNDAR** (Primera parte):
Casos detallados con descripción, pasos y resultados esperados.

**FORMATO JSON** (Segunda parte):
```json
[{
  "proyecto_id": 1, "epic_id": 1, "titulo": "Título del caso",
  "descripcion": "Descripción detallada", "pasos": ["Paso 1", "Paso 2"],
  "resultado_esperado": "Resultado específico", "prioridad": "Alta/Media/Baja",
  "estado": "Pendiente", "asignado_a": "QA Engineer",
  "fecha_inicio": "12/08/2025", "fecha_fin": "13/08/2025",
  "tiempo_estimado": "4 horas", "categoria": "Funcional/UI/API/Performance/Security"
}]
```

**SEPARADORES:**
- Entre casos: ═══════════════════════════════════════════════════════════
- Entre formatos: ┌── 🔄 FORMATO ESTÁNDAR → JSON ──┐

**REQUISITOS:** Mínimo 15-20 casos, fechas DD/MM/YYYY, ambos formatos incluidos.""")
    
    def generar_casos_completos(self):
        """Función unificada que genera casos en AMBOS formatos: estándar Y JSON"""
        self.enviar_comando("""Genera casos de prueba completos en formato estándar detallado Y JSON estructurado.

**FORMATO ESTÁNDAR** (Primera parte):
Casos detallados con descripción, pasos y resultados esperados.

**FORMATO JSON** (Segunda parte):
```json
[{
  "proyecto_id": 1, "epic_id": 1, "titulo": "Título del caso",
  "descripcion": "Descripción detallada", "pasos": ["Paso 1", "Paso 2"],
  "resultado_esperado": "Resultado específico", "prioridad": "Alta/Media/Baja",
  "estado": "Pendiente", "asignado_a": "QA Engineer",
  "fecha_inicio": "12/08/2025", "fecha_fin": "13/08/2025",
  "tiempo_estimado": "4 horas", "categoria": "Funcional/UI/API/Performance/Security"
}]
```

**SEPARADORES:**
- Entre casos: ═══════════════════════════════════════════════════════════
- Entre formatos: ┌── 🔄 FORMATO ESTÁNDAR → JSON ──┐

**REQUISITOS:** Mínimo 15-20 casos, fechas DD/MM/YYYY, prioridades equilibradas, ambos formatos incluidos.""")
    
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
                <li><strong>📋 Test Cases & Docs:</strong> Documentación, casos de prueba y manuales</li>
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
            
            <h3 style='color: #DC2626;'>⭐ NUEVAS FUNCIONALIDADES:</h3>
            <ul style='color: #1F2937; line-height: 1.8; font-size: 15px;'>
                <li><strong>📖 Manual de Usuario:</strong> Genera manuales completos y profesionales</li>
                <li>Incluye estructura estándar con índice, funcionalidades y casos de uso</li>
                <li>Formato profesional adaptable a cualquier sistema o aplicación</li>
                <li>Lenguaje claro y accesible para usuarios finales</li>
                <li><strong>🔗 Integración con Notion:</strong> Conecta directamente con tu workspace</li>
                <li><strong>📝 Casos para Notion:</strong> Formato optimizado para documentación</li>
                <li><strong>🗂️ Casos JSON:</strong> Formato estructurado para gestión de proyectos</li>
            </ul>
            
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
    
    def configurar_notion(self):
        """Abrir configuración de Notion"""
        try:
            # Verificar que el archivo existe
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(script_dir, "notion_config_dialog.py")
            
            if not os.path.exists(config_file):
                QMessageBox.critical(self, "Error", f"Archivo de configuración no encontrado: {config_file}")
                return
            
            # Intentar importar y crear el diálogo
            from notion_config_dialog import NotionConfigDialog
            dialog = NotionConfigDialog(self)
            dialog.show()  # Usar show() en lugar de exec_() para mejor compatibilidad
            
        except ImportError as e:
            QMessageBox.warning(self, "Error de Importación", 
                              f"No se pudo cargar el módulo de configuración de Notion.\n\nError: {str(e)}\n\nAsegúrate de que el archivo 'notion_config_dialog.py' esté presente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Error al abrir configuración de Notion:\n\n{str(e)}\n\nTipo de error: {type(e).__name__}")
            
            # Debug info
            import traceback
            print(f"Error completo: {traceback.format_exc()}")
    
    def parsear_casos_notion(self, texto_casos):
        """
        Parsear casos de prueba del texto generado en formato Notion con emojis
        
        Args:
            texto_casos: Texto con casos de prueba en formato Notion
            
        Returns:
            Lista de diccionarios con casos de prueba
        """
        casos = []
        import re
        
        # Filtrar solo el contenido que contiene casos de prueba reales
        # Buscar secciones que contengan casos de prueba
        lineas = texto_casos.split('\n')
        texto_filtrado = []
        capturando_casos = False
        
        for linea in lineas:
            linea_clean = linea.strip()
            
            # Comenzar a capturar cuando encontremos un caso de prueba real
            if re.match(r'\[CP-\d+\]', linea_clean) or re.match(r'\[\w+-\d+\]', linea_clean):
                capturando_casos = True
            
            # Dejar de capturar si encontramos texto de instrucciones
            if capturando_casos and any(keyword in linea_clean.upper() for keyword in [
                'INSTRUCCIONES ESPECÍFICAS', 'FORMATO DE RESPUESTA', 'IMPORTANTE:',
                'REQUISITOS:', 'SEPARADORES:', 'TIPS:', 'EJEMPLOS:', 'NOTA:'
            ]):
                break
                
            if capturando_casos:
                texto_filtrado.append(linea)
        
        if not texto_filtrado:
            # Si no encontramos casos con el filtro, buscar directamente por patrones
            texto_para_parsear = texto_casos
        else:
            texto_para_parsear = '\n'.join(texto_filtrado)
        
        # Buscar patrones de casos de prueba que inicien con [CP-X] o similar
        patron_caso = r'\[(CP-\d+|[A-Z]+-\d+)\]\s*([^\n\[]+)'
        matches = list(re.finditer(patron_caso, texto_para_parsear))
        
        for i, match in enumerate(matches):
            try:
                inicio = match.start()
                # Determinar el final del caso actual
                if i + 1 < len(matches):
                    fin = matches[i + 1].start()
                else:
                    # Buscar el próximo separador ---
                    resto_texto = texto_para_parsear[inicio:]
                    separador_match = re.search(r'\n---\s*\n', resto_texto)
                    if separador_match:
                        fin = inicio + separador_match.start()
                    else:
                        fin = len(texto_para_parsear)
                
                bloque_caso = texto_para_parsear[inicio:fin]
                caso = {}
                
                # Extraer ID y título del patrón inicial
                caso['id'] = match.group(1).strip()
                caso['titulo'] = match.group(2).strip()
                
                # Validar que tenemos un caso real
                if not caso['titulo'] or 'instrucciones' in caso['titulo'].lower():
                    continue
                
                lineas_caso = bloque_caso.split('\n')
                pasos_list = []
                capturando_pasos = False
                
                i_linea = 0
                while i_linea < len(lineas_caso):
                    linea = lineas_caso[i_linea].strip()
                    if not linea:
                        i_linea += 1
                        continue
                    
                    # Extraer información usando emojis como delimitadores
                    if '📄 Descripción' in linea or 'Descripción' in linea:
                        # Buscar la siguiente línea con contenido
                        if i_linea + 1 < len(lineas_caso):
                            descripcion = lineas_caso[i_linea + 1].strip()
                            caso['descripcion'] = descripcion.replace('[', '').replace(']', '').strip()
                    
                    elif '📅 Fecha de creación' in linea or 'Fecha de creación' in linea:
                        if i_linea + 1 < len(lineas_caso):
                            fecha = lineas_caso[i_linea + 1].strip()
                            caso['fecha'] = fecha.replace('[', '').replace(']', '').strip()
                    
                    elif '🔢 Nº ID' in linea or 'Nº ID' in linea:
                        if i_linea + 1 < len(lineas_caso):
                            numero = lineas_caso[i_linea + 1].strip()
                            caso['numero_id'] = numero.replace('[', '').replace(']', '').strip()
                    
                    elif '🗂 Módulo' in linea or 'Módulo' in linea:
                        if i_linea + 1 < len(lineas_caso):
                            modulo = lineas_caso[i_linea + 1].strip()
                            caso['modulo'] = modulo.replace('[', '').replace(']', '').strip()
                    
                    elif '🚨 Prioridad' in linea or 'Prioridad' in linea:
                        if i_linea + 1 < len(lineas_caso):
                            prioridad = lineas_caso[i_linea + 1].strip()
                            caso['prioridad'] = prioridad.replace('[', '').replace(']', '').strip()
                    
                    elif '🔄 Status' in linea or 'Status' in linea:
                        if i_linea + 1 < len(lineas_caso):
                            status = lineas_caso[i_linea + 1].strip()
                            caso['estado'] = status.replace('[', '').replace(']', '').strip()
                    
                    elif '📌 Proyectos' in linea or 'Proyectos' in linea:
                        if i_linea + 1 < len(lineas_caso):
                            proyecto = lineas_caso[i_linea + 1].strip()
                            caso['proyecto'] = proyecto.replace('[', '').replace(']', '').strip()
                    
                    elif '🎯 Resultado esperado' in linea or 'Resultado esperado' in linea:
                        capturando_pasos = False
                        if i_linea + 1 < len(lineas_caso):
                            resultado = lineas_caso[i_linea + 1].strip()
                            caso['resultado_esperado'] = resultado.replace('[', '').replace(']', '').strip()
                    
                    elif 'Comentarios' in linea:
                        if i_linea + 1 < len(lineas_caso):
                            comentario = lineas_caso[i_linea + 1].strip()
                            caso['comentarios'] = comentario.replace('[', '').replace(']', '').strip()
                    
                    elif 'Pasos a seguir:' in linea:
                        capturando_pasos = True
                    
                    elif capturando_pasos and linea and not linea.startswith('---'):
                        # Capturar pasos que están en líneas individuales
                        paso_limpio = linea.replace('[', '').replace(']', '').strip()
                        if (paso_limpio and 
                            not paso_limpio.startswith('Resultado') and 
                            not paso_limpio.startswith('Comentarios') and
                            not any(keyword in paso_limpio.upper() for keyword in ['INSTRUCCIONES', 'IMPORTANTE', 'FORMATO'])):
                            pasos_list.append(paso_limpio)
                    
                    i_linea += 1
                
                # Asignar pasos si los hay
                if pasos_list:
                    caso['pasos'] = pasos_list
                
                # Valores por defecto si no se encontraron
                caso.setdefault('descripcion', 'Descripción del caso de prueba')
                caso.setdefault('fecha', '12/08/2025')
                caso.setdefault('modulo', 'General')
                caso.setdefault('prioridad', 'Media')
                caso.setdefault('estado', 'Pendiente')
                caso.setdefault('proyecto', 'Proyecto QA')
                caso.setdefault('resultado_esperado', 'Resultado esperado del caso')
                caso.setdefault('comentarios', 'Sin comentarios adicionales')
                caso.setdefault('pasos', ['Paso 1: Ejecutar acción', 'Paso 2: Verificar resultado'])
                
                # Solo agregar casos que tengan ID y título válidos
                if (caso.get('id') and caso.get('titulo') and 
                    not 'instrucciones' in caso['titulo'].lower() and
                    len(caso['titulo'].strip()) > 5):  # Título mínimo de 5 caracteres
                    casos.append(caso)
                    
            except Exception as e:
                # Si hay error parseando un caso específico, continuar con el siguiente
                print(f"Error parseando caso: {e}")
                continue
        
        return casos
    
    def enviar_casos_a_notion(self, casos):
        """
        Enviar casos de prueba a Notion usando formato con emojis
        
        Args:
            casos: Lista de casos de prueba parseados
            
        Returns:
            Resultado de la operación
        """
        try:
            from notion_integration import NotionConfigManager
            import webbrowser
            import urllib.parse
            
            config_manager = NotionConfigManager()
            database_id = config_manager.obtener_database_id()
            
            resultados = {
                "total": len(casos),
                "exitosos": 0,
                "fallidos": 0,
                "casos_formateados": []
            }
            
            # Formatear casos para Notion con emojis
            casos_formateados = []
            for i, caso in enumerate(casos, 1):
                caso_formateado = f"""[{caso.get('id', f'CP-{i:03d}')}] {caso.get('titulo', 'Sin título')}

� Descripción
{caso.get('descripcion', 'Sin descripción')}

� Fecha de creación
{caso.get('fecha', '12/08/2025')}

🔢 Nº ID
{caso.get('numero_id', str(i))}

�🗂 Módulo
{caso.get('modulo', 'General')}

✅ Paso la prueba
{caso.get('paso_prueba', 'Pendiente')}

🚨 Prioridad
{caso.get('prioridad', 'Media')}

🔄 Status
{caso.get('estado', 'Pendiente')}

� Proyectos
{caso.get('proyecto', 'Proyecto QA')}

🎯 Resultado esperado
{caso.get('resultado_esperado', 'Sin resultado definido')}

Comentarios
{caso.get('comentarios', 'Sin comentarios adicionales')}

Pasos a seguir:

{chr(10).join([paso for paso in caso.get('pasos', ['Sin pasos definidos'])])}

---

"""
                casos_formateados.append(caso_formateado)
                resultados["exitosos"] += 1
            
            # Crear contenido completo para copiar
            contenido_completo = f"""# 📋 Casos de Prueba - Exportación Automática
*Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}*

{chr(10).join(casos_formateados)}

💡 **Instrucciones para Notion:**
1. 📋 Este contenido ya está copiado en tu portapapeles
2. 🌐 Se abrirá Notion en tu navegador
3. ➕ Crea páginas nuevas en tu base de datos
4. 📝 Pega cada caso en una página separada
5. 🎨 Notion mantendrá automáticamente los emojis y formato

🔗 **ID de tu base de datos:** {database_id}

✨ **¡Listo para usar en Notion con vista de tablero!**
"""
            
            # Guardar en un archivo temporal para facilitar la copia
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(contenido_completo)
                archivo_temp = f.name
            
            # Copiar al portapapeles usando PyQt5
            from PyQt5.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(contenido_completo)
            
            # Abrir Notion en el navegador
            notion_url = f"https://notion.so/{database_id}"
            webbrowser.open(notion_url)
            
            # Limpiar archivo temporal después de un tiempo
            import threading
            def limpiar_temp():
                import time
                time.sleep(300)  # 5 minutos
                try:
                    os.unlink(archivo_temp)
                except:
                    pass
            
            threading.Thread(target=limpiar_temp, daemon=True).start()
            
            resultados["casos_formateados"] = casos_formateados
            resultados["archivo_temp"] = archivo_temp
            
            return {
                "status": "success",
                "message": f"✅ {resultados['exitosos']} casos preparados para Notion.\n\n📋 Casos copiados al portapapeles con formato completo.\n🌐 Notion se abrirá en tu navegador.\n🎨 Los emojis y formato se mantendrán automáticamente.\n\n💡 Simplemente pega en tu base de datos con vista de tablero.",
                "data": resultados
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error durante la preparación: {str(e)}"
            }
    def exportar_a_notion(self):
        """Exportar casos de prueba generados automáticamente a Notion"""
        try:
            from notion_integration import NotionConfigManager
            config_manager = NotionConfigManager()
            
            if not config_manager.esta_configurado():
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Configuración requerida")
                msg_box.setText("Primero debes configurar la base de datos de Notion.\n\nHaz clic en '🔗 Configurar Notion' para comenzar.")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                                  stop: 0 #0B1D4A, stop: 1 #1F2A56);
                        color: #FFFFFF;
                        font-family: 'Segoe UI', Arial, sans-serif;
                        font-size: 14px;
                        border: 2px solid #EF4444;
                        border-radius: 15px;
                    }
                    QMessageBox QLabel {
                        color: #FFFFFF;
                        font-size: 14px;
                        background: transparent;
                        padding: 20px;
                    }
                    QMessageBox QPushButton {
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                                  stop: 0 #EF4444, stop: 1 #DC2626);
                        color: white;
                        border: none;
                        border-radius: 8px;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 10px 20px;
                        min-width: 80px;
                        margin: 5px;
                    }
                    QMessageBox QPushButton:hover {
                        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                                  stop: 0 #F87171, stop: 1 #EF4444);
                    }
                """)
                msg_box.exec_()
                return
            
            # Obtener el texto del área de chat de múltiples maneras
            texto_completo = ""
            
            # Método 1: Buscar en diferentes posibles referencias del área de chat
            posibles_referencias = ['area_chat', 'chat_area', 'text_area', 'chat_display', 'respuesta_area']
            
            for ref in posibles_referencias:
                if hasattr(self.parent_window, ref):
                    widget = getattr(self.parent_window, ref)
                    if hasattr(widget, 'toPlainText'):
                        texto_completo = widget.toPlainText()
                        print(f"✅ Texto encontrado usando {ref}: {len(texto_completo)} caracteres")
                        break
                    elif hasattr(widget, 'text'):
                        texto_completo = widget.text()
                        print(f"✅ Texto encontrado usando {ref}.text(): {len(texto_completo)} caracteres")
                        break
            
            # Método 2: Si no encontramos texto, buscar en el portapapeles
            if not texto_completo.strip():
                try:
                    from PyQt5.QtWidgets import QApplication
                    clipboard = QApplication.clipboard()
                    texto_portapapeles = clipboard.text()
                    
                    if texto_portapapeles and any(patron in texto_portapapeles for patron in ['[CP-', '📄 Descripción', '🎯 Resultado esperado']):
                        texto_completo = texto_portapapeles
                        print(f"✅ Texto encontrado en portapapeles: {len(texto_completo)} caracteres")
                        
                        # Preguntar si quiere usar el contenido del portapapeles
                        confirmacion_clipboard = QMessageBox(self)
                        confirmacion_clipboard.setWindowTitle("Usar Portapapeles")
                        confirmacion_clipboard.setText(f"No se encontró texto en el chat, pero hay contenido en el portapapeles.\n\n¿Deseas usar el contenido del portapapeles para exportar?\n\n(Contiene {len(texto_portapapeles)} caracteres)")
                        confirmacion_clipboard.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                        confirmacion_clipboard.setDefaultButton(QMessageBox.Yes)
                        confirmacion_clipboard.setIcon(QMessageBox.Question)
                        
                        if confirmacion_clipboard.exec_() != QMessageBox.Yes:
                            return
                except Exception as e:
                    print(f"Error accediendo al portapapeles: {e}")
            
            # Método 3: Si aún no hay texto, ofrecer opción de generar casos de ejemplo
            if not texto_completo.strip():
                opcion_ejemplo = QMessageBox(self)
                opcion_ejemplo.setWindowTitle("Generar Casos de Ejemplo")
                opcion_ejemplo.setText("No se encontró texto con casos de prueba.\n\n¿Deseas generar casos de ejemplo para probar la exportación?\n\n(Se generarán 3 casos de prueba de ejemplo)")
                opcion_ejemplo.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                opcion_ejemplo.setDefaultButton(QMessageBox.Yes)  # Cambiar default a Yes
                opcion_ejemplo.setIcon(QMessageBox.Question)
                
                if opcion_ejemplo.exec_() == QMessageBox.Yes:
                    texto_completo = self.generar_casos_ejemplo()
                else:
                    self.mostrar_mensaje_info("📝 Genera Casos Primero", 
                        "Para exportar a Notion necesitas:\n\n1. Usar el botón '📝 Casos de Prueba → Notion' para generar casos\n2. Presionar ENTER para que el AI genere los casos\n3. Esperar a que aparezcan en el chat con formato [CP-001]\n4. Luego usar 'Exportar Automáticamente'\n\nO usar la opción de casos de ejemplo para probar.")
                    return
            
            # Buscar casos de prueba en el texto
            print(f"🔍 Analizando texto de {len(texto_completo)} caracteres...")
            casos_encontrados = self.parsear_casos_notion(texto_completo)
            print(f"📋 Casos encontrados: {len(casos_encontrados)}")
            
            if not casos_encontrados:
                # Mostrar información de debug más clara
                debug_info = f"📊 **Análisis del texto:**\n"
                debug_info += f"• Caracteres analizados: {len(texto_completo)}\n"
                debug_info += f"• Contiene '[CP-': {'✅ Sí' if '[CP-' in texto_completo else '❌ No'}\n"
                debug_info += f"• Contiene '📄 Descripción': {'✅ Sí' if '📄 Descripción' in texto_completo else '❌ No'}\n"
                debug_info += f"• Contiene casos válidos: ❌ No\n\n"
                debug_info += f"🔍 **Muestra del contenido:**\n{texto_completo[:300]}...\n\n"
                debug_info += f"💡 **Para generar casos:**\n"
                debug_info += f"1. Tab 'Test Cases & Docs' → 'Casos de Prueba → Notion'\n"
                debug_info += f"2. Presionar ENTER para generar\n"
                debug_info += f"3. Esperar casos con formato [CP-001]\n"
                debug_info += f"4. Luego exportar automáticamente"
                
                self.mostrar_mensaje_info("⚠️ No se encontraron casos de prueba", debug_info)
                return
            
            # Mostrar confirmación antes de exportar
            confirmacion = QMessageBox(self)
            confirmacion.setWindowTitle("Confirmar Exportación")
            confirmacion.setText(f"¿Deseas exportar {len(casos_encontrados)} casos de prueba a Notion?")
            confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirmacion.setDefaultButton(QMessageBox.Yes)
            confirmacion.setIcon(QMessageBox.Question)
            confirmacion.setStyleSheet("""
                QMessageBox {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                              stop: 0 #0B1D4A, stop: 1 #1F2A56);
                    color: #FFFFFF;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 14px;
                    border: 2px solid #4C5BFF;
                    border-radius: 15px;
                }
                QMessageBox QLabel {
                    color: #FFFFFF;
                    font-size: 14px;
                    background: transparent;
                    padding: 20px;
                }
                QMessageBox QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                              stop: 0 #4C5BFF, stop: 1 #6366F1);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px 20px;
                    min-width: 80px;
                    margin: 5px;
                }
                QMessageBox QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                              stop: 0 #6366F1, stop: 1 #7C3AED);
                }
            """)
            
            if confirmacion.exec_() == QMessageBox.Yes:
                # Exportar casos a Notion
                resultado = self.enviar_casos_a_notion(casos_encontrados)
                
                if resultado["status"] == "success":
                    self.mostrar_mensaje_exito("✅ Exportación Exitosa", resultado["message"])
                else:
                    self.mostrar_mensaje_error("❌ Error de Exportación", resultado["message"])
                    
        except ImportError:
            self.mostrar_mensaje_error("❌ Error", "Módulo de Notion no disponible")
        except Exception as e:
            self.mostrar_mensaje_error("❌ Error", f"Error inesperado: {str(e)}")
    
    def generar_y_exportar_casos(self):
        """Generar casos de prueba de ejemplo y exportarlos directamente a Notion"""
        try:
            from notion_integration import NotionConfigManager
            config_manager = NotionConfigManager()
            
            if not config_manager.esta_configurado():
                self.mostrar_mensaje_info("🔗 Configuración requerida", 
                    "Primero debes configurar la base de datos de Notion.\n\nHaz clic en '🔗 Configurar Notion' para comenzar.")
                return
            
            # Preguntar qué tipo de casos generar
            tipo_casos = QMessageBox(self)
            tipo_casos.setWindowTitle("Tipo de Casos de Prueba")
            tipo_casos.setText("¿Qué tipo de casos de prueba deseas generar y exportar?")
            
            btn_ejemplo = tipo_casos.addButton("📝 Casos de Ejemplo", QMessageBox.YesRole)
            btn_personalizados = tipo_casos.addButton("🎯 Casos Personalizados", QMessageBox.NoRole)
            btn_cancelar = tipo_casos.addButton("❌ Cancelar", QMessageBox.RejectRole)
            
            tipo_casos.exec_()
            clicked = tipo_casos.clickedButton()
            
            if clicked == btn_cancelar:
                return
            elif clicked == btn_ejemplo:
                # Usar casos de ejemplo predefinidos
                casos_texto = self.generar_casos_ejemplo()
                casos_encontrados = self.parsear_casos_notion(casos_texto)
                
                if casos_encontrados:
                    confirmacion = QMessageBox(self)
                    confirmacion.setWindowTitle("Confirmar Exportación")
                    confirmacion.setText(f"Se generaron {len(casos_encontrados)} casos de ejemplo.\n\n¿Deseas exportarlos a Notion?")
                    confirmacion.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    confirmacion.setDefaultButton(QMessageBox.Yes)
                    
                    if confirmacion.exec_() == QMessageBox.Yes:
                        resultado = self.enviar_casos_a_notion(casos_encontrados)
                        
                        if resultado["status"] == "success":
                            self.mostrar_mensaje_exito("✅ Exportación Exitosa", 
                                f"Se exportaron {len(casos_encontrados)} casos de ejemplo a Notion.\n\n{resultado['message']}")
                        else:
                            self.mostrar_mensaje_error("❌ Error de Exportación", resultado["message"])
                else:
                    self.mostrar_mensaje_error("❌ Error", "No se pudieron generar los casos de ejemplo")
                    
            elif clicked == btn_personalizados:
                # Generar prompt para casos personalizados
                prompt_personalizado = """🎯 **Senior QA Engineer con 10+ años de experiencia**

**SOLICITUD:** Genera casos de prueba en formato específico para Notion con emojis y estructura detallada.

**FORMATO EXACTO REQUERIDO PARA CADA CASO:**

[CP-001] [Título del Caso de Prueba]

📄 Descripción
[Escribe aquí la descripción detallada del caso de prueba, indicando el objetivo y qué se validará.]

📅 Fecha de creación
[Fecha actual: 12/08/2025]

🔢 Nº ID
[ID numérico: 1, 2, 3, etc.]

🗂 Módulo
[Nombre del módulo correspondiente]

✅ Paso la prueba
[SI / NO - inicialmente "Pendiente"]

🚨 Prioridad
[Alta / Media / Baja]

🔄 Status
[En curso / Pendiente / Completado - inicialmente "Pendiente"]

📌 Proyectos
[Nombre del proyecto]

🎯 Resultado esperado
[Describe el resultado esperado de la ejecución del caso de prueba, con criterios claros de aceptación.]

Comentarios
[Espacio para comentarios adicionales - inicialmente vacío o con notas relevantes]

Pasos a seguir:

[Primer paso del caso de prueba]

[Segundo paso del caso de prueba]

[Tercer paso, y así sucesivamente]

---

**INSTRUCCIONES ESPECÍFICAS:**
✅ Usa EXACTAMENTE el formato mostrado arriba con todos los emojis
✅ Numera los casos como CP-1, CP-2, CP-3, etc.
✅ Incluye fecha actual (12/08/2025)
✅ Varía las prioridades entre Alta, Media y Baja
✅ Status inicial siempre "Pendiente"
✅ Incluye módulos relevantes para el sistema
✅ Pasos detallados y específicos numerados
✅ Resultados esperados claros y medibles
✅ Genera mínimo 10-15 casos de prueba completos
✅ Separa cada caso con --- al final
✅ Formato optimizado para copiar y pegar en Notion

**IMPORTANTE:** Este formato está diseñado específicamente para ser copiado directamente a Notion manteniendo toda la estructura y emojis."""
                
                if self.parent_window and hasattr(self.parent_window, 'entrada_texto'):
                    self.close()
                    self.parent_window.entrada_texto.setPlainText(prompt_personalizado)
                    self.parent_window.entrada_texto.setFocus()
                    
                    self.mostrar_mensaje_info("📝 Prompt Cargado", 
                        "Se ha cargado el prompt para generar casos personalizados.\n\n1. Presiona ENTER para generar los casos\n2. Espera a que aparezcan en el chat\n3. Luego usa 'Exportar Automáticamente a Notion'")
                else:
                    self.mostrar_mensaje_error("❌ Error", "No se pudo acceder al campo de texto")
                    
        except ImportError:
            self.mostrar_mensaje_error("❌ Error", "Módulo de Notion no disponible")
        except Exception as e:
            self.mostrar_mensaje_error("❌ Error", f"Error inesperado: {str(e)}")
    
    def generar_casos_ejemplo(self):
        """Generar casos de prueba de ejemplo para testing"""
        casos_ejemplo = """[CP-001] Validación de login con credenciales válidas

📄 Descripción
Verificar que un usuario pueda iniciar sesión correctamente con credenciales válidas en el sistema

📅 Fecha de creación
12/08/2025

🔢 Nº ID
1

🗂 Módulo
Autenticación

🚨 Prioridad
Alta

🔄 Status
Pendiente

📌 Proyectos
Sistema de Login

🎯 Resultado esperado
El usuario debe poder acceder al sistema y ser redirigido al dashboard principal con su sesión activa

Comentarios
Caso crítico para funcionalidad básica del sistema

Pasos a seguir:

Abrir la página de login en el navegador
Ingresar usuario válido en el campo correspondiente
Ingresar contraseña válida en el campo de password
Hacer clic en el botón "Iniciar Sesión"
Verificar redirección al dashboard principal
Confirmar que el nombre de usuario aparece en la interfaz

---

[CP-002] Validación de login con credenciales inválidas

📄 Descripción
Verificar que el sistema rechace credenciales incorrectas y muestre mensajes de error apropiados

📅 Fecha de creación
12/08/2025

🔢 Nº ID
2

🗂 Módulo
Autenticación

🚨 Prioridad
Alta

🔄 Status
Pendiente

📌 Proyectos
Sistema de Login

🎯 Resultado esperado
El sistema debe mostrar mensaje de error claro y no permitir el acceso al sistema

Comentarios
Validar seguridad del sistema contra accesos no autorizados

Pasos a seguir:

Abrir la página de login en el navegador
Ingresar usuario inválido o inexistente
Ingresar contraseña incorrecta
Hacer clic en el botón "Iniciar Sesión"
Verificar que aparece mensaje de error
Confirmar que no se permite el acceso al sistema

---

[CP-003] Validación de registro de nuevo usuario

📄 Descripción
Verificar que el proceso de registro de nuevos usuarios funciona correctamente con datos válidos

📅 Fecha de creación
12/08/2025

🔢 Nº ID
3

🗂 Módulo
Registro de Usuarios

🚨 Prioridad
Media

🔄 Status
Pendiente

📌 Proyectos
Sistema de Registro

🎯 Resultado esperado
El nuevo usuario debe ser registrado exitosamente y recibir confirmación del registro

Comentarios
Flujo esencial para crecimiento de la base de usuarios

Pasos a seguir:

Acceder a la página de registro
Completar todos los campos obligatorios
Ingresar email válido y único
Crear contraseña que cumpla los requisitos
Aceptar términos y condiciones
Hacer clic en "Registrarse"
Verificar mensaje de confirmación
Confirmar que se envía email de verificación

---"""
        return casos_ejemplo
    
    def mostrar_mensaje_info(self, titulo, mensaje):
        """Mostrar mensaje informativo con estilos"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet("""
            QMessageBox {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #0B1D4A, stop: 1 #1F2A56);
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                border: 2px solid #17a2b8;
                border-radius: 15px;
            }
            QMessageBox QLabel {
                color: #FFFFFF;
                font-size: 14px;
                background: transparent;
                padding: 20px;
                min-width: 400px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #17a2b8, stop: 1 #138496);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                min-width: 80px;
                margin: 5px;
            }
        """)
        msg_box.exec_()
    
    def mostrar_mensaje_exito(self, titulo, mensaje):
        """Mostrar mensaje de éxito con estilos"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStyleSheet("""
            QMessageBox {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #0B1D4A, stop: 1 #1F2A56);
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                border: 2px solid #28a745;
                border-radius: 15px;
            }
            QMessageBox QLabel {
                color: #FFFFFF;
                font-size: 14px;
                background: transparent;
                padding: 20px;
                min-width: 400px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #28a745, stop: 1 #1e7e34);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                min-width: 80px;
                margin: 5px;
            }
        """)
        msg_box.exec_()
    
    def mostrar_mensaje_error(self, titulo, mensaje):
        """Mostrar mensaje de error con estilos"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setStyleSheet("""
            QMessageBox {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #0B1D4A, stop: 1 #1F2A56);
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                border: 2px solid #dc3545;
                border-radius: 15px;
            }
            QMessageBox QLabel {
                color: #FFFFFF;
                font-size: 14px;
                background: transparent;
                padding: 20px;
                min-width: 400px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #dc3545, stop: 1 #c82333);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                min-width: 80px;
                margin: 5px;
            }
        """)
        msg_box.exec_()
    
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
            
            #botonConfig, #botonHelp {
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
            
            #botonConfig:hover, #botonHelp:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #4C5BFF, stop: 1 #6366F1);
                border: 2px solid #FFD700;
                color: #FFFFFF;
            }
            
            #botonNotion {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #7C3AED, stop: 1 #A855F7);
                color: #FFFFFF;
                border: 2px solid #FFFFFF;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                padding: 15px 25px;
                min-width: 180px;
            }
            
            #botonNotion:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #A855F7, stop: 1 #C084FC);
                border: 2px solid #FFD700;
                color: #FFFFFF;
            }
            
            #botonExportNotion {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #059669, stop: 1 #10B981);
                color: #FFFFFF;
                border: 2px solid #FFFFFF;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                padding: 15px 25px;
                min-width: 180px;
            }
            
            #botonExportNotion:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #10B981, stop: 1 #34D399);
                border: 2px solid #FFD700;
                color: #FFFFFF;
            }
            
            #botonGenerarExportar {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #7C3AED, stop: 1 #A855F7);
                color: #FFFFFF;
                border: 2px solid #FFFFFF;
                border-radius: 15px;
                font-size: 14px;
                font-weight: bold;
                padding: 15px 25px;
                min-width: 200px;
            }
            
            #botonGenerarExportar:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                          stop: 0 #A855F7, stop: 1 #C084FC);
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
