import re
import random
import os
import json
from datetime import datetime, timedelta
import google.generativeai as genai

class ChatBot:
    def __init__(self, nombre="AsistentBot"):
        self.nombre = nombre
        self.usar_ia = True
        self.modelo_ia = None
        self.historial_conversacion = []
        self.sesion_actual = {
            'inicio': datetime.now().isoformat(),
            'conversaciones': []
        }
        
        # Configurar directorio de historial
        self.directorio_historial = os.path.join(os.path.dirname(__file__), 'historial')
        self.crear_directorio_historial()
        
        # Configurar Google AI
        self.configurar_ia()
        
        # Respuestas locales básicas (se usarán si la IA no está disponible)
        self.respuestas_locales = {
            # Saludos
            "hola|buenos dias|buenas tardes|buenas noches|saludos": [
                f"¡Hola! Soy {self.nombre}, ¿en qué puedo ayudarte?",
                f"¡Saludos! Soy {self.nombre}, ¿qué necesitas?",
                f"¡Hola! ¿Cómo estás? Soy {self.nombre}"
            ],
            
            # Presentación
            "quien eres|como te llamas|tu nombre": [
                f"Soy {self.nombre}, un chatbot creado para ayudarte.",
                f"Me llamo {self.nombre} y estoy aquí para asistirte.",
                f"Soy {self.nombre}, tu asistente virtual."
            ],
            
            # Estado/Cómo está
            "como estas|que tal|como te encuentras": [
                "¡Estoy muy bien, gracias por preguntar!",
                "¡Perfecto! Listo para ayudarte.",
                "¡Excelente! ¿Y tú cómo estás?"
            ],
            
            # Ayuda
            "ayuda|que puedes hacer|funciones": [
                "Puedo ayudarte con preguntas básicas, conversar contigo y responder sobre diversos temas.",
                "Estoy aquí para conversar y responder tus preguntas. ¡Pregúntame lo que quieras!",
                "Puedo responder preguntas, conversar y ayudarte con información básica."
            ],
            
            # Hora y fecha
            "que hora es|hora|tiempo": [
                "Lo siento, no tengo acceso a la hora actual en este momento.",
                "No puedo consultar la hora ahora mismo, pero puedes verificarla en tu dispositivo."
            ],
            
            # Despedidas
            "adios|chao|hasta luego|nos vemos|bye": [
                "¡Hasta luego! Fue un placer ayudarte.",
                "¡Adiós! Que tengas un excelente día.",
                "¡Nos vemos! Vuelve cuando necesites ayuda."
            ],
            
            # Agradecimientos
            "gracias|muchas gracias|te agradezco": [
                "¡De nada! Estoy aquí para ayudarte.",
                "¡Un placer ayudarte!",
                "¡Para eso estoy aquí!"
            ],
            
            # Información personal
            "como estas|tu edad|cuantos anos": [
                "Soy un programa de computadora, así que no tengo edad como los humanos.",
                "Soy software, ¡así que técnicamente nací cuando me programaron!"
            ],
            
            # Archivos y análisis
            "archivo|documento|imagen|analisis": [
                "Puedo ayudarte a analizar archivos y documentos. ¿Qué tipo de análisis necesitas?",
                "Estoy preparado para revisar documentos. ¿Quieres un resumen, análisis o algo específico?",
                "¿Necesitas que analice algún archivo? ¡Adjúntalo y dime qué quieres que haga!"
            ],
            
            # Casos de prueba específicos
            "casos de prueba|test cases|testing": [
                "¡Perfecto! Puedo generar casos de prueba detallados desde documentos.",
                "Especializado en casos de prueba. Adjunta tu documentación y te los genero.",
                "¿Tienes documentos de requisitos? Puedo crear casos de prueba desde ellos."
            ],
            
            # Manuales de usuario
            "manual de usuario|manual usuario|documentacion usuario|guia usuario": [
                "¡Excelente! Puedo generar manuales de usuario siguiendo estructuras específicas.",
                "Especializado en documentación de usuario. Adjunta tu información y genero el manual.",
                "¿Tienes información del sistema? Puedo crear un manual de usuario completo."
            ],
            
            # Resumen de documentos
            "resumen|resumir|resume": [
                "Puedo hacer resúmenes claros y concisos de tus documentos.",
                "¿Quieres que resuma algún documento? ¡Adjúntalo!",
                "Especializado en resumir documentos técnicos y de negocio."
            ]
        }
        
        # Respuestas por defecto cuando no entiende
        self.respuestas_default = [
            "Interesante... ¿puedes contarme más sobre eso?",
            "No estoy seguro de cómo responder a eso. ¿Podrías reformular la pregunta?",
            "Hmm, no tengo una respuesta específica para eso. ¿Hay algo más en lo que pueda ayudarte?",
            "Esa es una pregunta interesante. ¿Podrías ser más específico?",
            "Lo siento, no entiendo completamente. ¿Puedes explicar de otra manera?"
        ]
    
    def configurar_ia(self):
        """Configura la conexión con Google AI Studio"""
        try:
            # Cargar API key desde archivo .env
            api_key = self.cargar_api_key()
            if api_key:
                genai.configure(api_key=api_key)
                self.modelo_ia = genai.GenerativeModel('gemini-2.0-flash')
                print(f"✅ IA configurada correctamente - {self.nombre} con Gemini 2.0 Flash")
            else:
                self.usar_ia = False
                print("⚠️ No se pudo cargar la API key, usando respuestas locales")
        except Exception as e:
            self.usar_ia = False
            print(f"⚠️ Error configurando IA: {e}")
            print("Usando respuestas locales")
    
    def cargar_api_key(self):
        """Carga la API key desde el archivo .env"""
        try:
            env_path = os.path.join(os.path.dirname(__file__), '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('GOOGLE_API_KEY='):
                            return line.split('=', 1)[1].strip()
            return None
        except Exception as e:
            print(f"Error cargando API key: {e}")
            return None
    
    def es_respuesta_local(self, mensaje):
        """Verifica si el mensaje debe ser respondido localmente"""
        mensaje_limpio = mensaje.lower().strip()
        
        # Patrones que siempre se responden localmente
        patrones_locales = [
            r'\b(hola|hi|buenos dias|buenas tardes|buenas noches|saludos)\b',
            r'\b(adios|chao|hasta luego|nos vemos|bye)\b',
            r'\b(gracias|muchas gracias|te agradezco)\b',
            r'\b(quien eres|como te llamas|tu nombre)\b'
        ]
        
        for patron in patrones_locales:
            if re.search(patron, mensaje_limpio):
                return True
        return False
    
    def responder_localmente(self, mensaje):
        """Genera respuesta usando patrones locales"""
        mensaje_limpio = mensaje.lower().strip()
        
        # Buscar coincidencias en las respuestas predefinidas
        for patron, respuestas in self.respuestas_locales.items():
            if re.search(patron, mensaje_limpio):
                return random.choice(respuestas)
        
        # Si no encuentra coincidencia, usar respuesta por defecto
        return random.choice(self.respuestas_default)
    
    def obtener_plantilla_casos_prueba(self):
        """Retorna la plantilla estándar para casos de prueba"""
        return """
IMPORTANTE: Todos los casos de prueba deben seguir EXACTAMENTE esta estructura:

CP-[NÚMERO]: [Título del caso de prueba]
Descripción: [Descripción detallada de qué se va a validar]
Fecha de creación: [Fecha actual]
Nº ID: [Número incremental]
Módulo: [Nombre del módulo o sistema]
Prioridad: [Alta/Media/Baja]
Status: Por hacer
Resultado esperado: [Describir el comportamiento esperado del sistema]
Paso a paso de la prueba:
1. [Primer paso]
2. [Segundo paso]
3. [Tercer paso]
4. [Etc...]

Ejemplo de formato correcto:
CP-1: Verificar la adición del botón "Enviar" en el formulario
Descripción: Validar que el botón "Enviar" se muestra correctamente en la interfaz de carga y edición de la planilla de mantenimiento, junto a los botones "Cancelar" y "Guardar".
Fecha de creación: 8 de agosto de 2025
Nº ID: 1
Módulo: Mantenimiento de la sucursal (Formulario)
Prioridad: Alta
Status: Por hacer
Resultado esperado: El botón "Enviar" es visible en la esquina superior derecha de la pantalla, al lado de "Guardar". Al hacerle clic, el sistema debe procesar el envío de la planilla.
Paso a paso de la prueba:
1. Ingresar al módulo de Mantenimiento.
2. Hacer clic en "Agregar nuevo" o editar un mantenimiento existente con estado "Pendiente".
3. Observar la esquina superior derecha de la pantalla del formulario.
4. Verificar que los tres botones se muestran en el orden esperado: Cancelar, Guardar, Enviar.

IMPORTANTE: SIEMPRE usar esta estructura exacta para todos los casos de prueba.
        """
    
    def calcular_fechas_proyecto(self, fecha_inicio_str, horas_estimadas, horas_por_dia=8):
        """Calcula fechas de inicio y fin basado en horas estimadas"""
        try:
            # Convertir string a fecha
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            
            # Calcular días necesarios (redondeando hacia arriba)
            dias_necesarios = (horas_estimadas + horas_por_dia - 1) // horas_por_dia
            
            # Calcular fecha fin (excluyendo fines de semana)
            fecha_fin = fecha_inicio
            dias_agregados = 0
            
            while dias_agregados < dias_necesarios:
                # Si no es fin de semana (0=lunes, 6=domingo)
                if fecha_fin.weekday() < 5:  # 0-4 son lunes a viernes
                    dias_agregados += 1
                if dias_agregados < dias_necesarios:
                    fecha_fin += timedelta(days=1)
            
            return fecha_inicio.strftime("%Y-%m-%d"), fecha_fin.strftime("%Y-%m-%d")
        except Exception as e:
            print(f"Error calculando fechas: {e}")
            return fecha_inicio_str, fecha_inicio_str
    
    def obtener_plantilla_casos_prueba_json(self):
        """Retorna la plantilla JSON para casos de prueba como tareas de proyecto"""
        return """
IMPORTANTE: Los casos de prueba en formato JSON deben seguir EXACTAMENTE esta estructura:

```json
{
  "proyectos": [
    {
      "proyecto_id": 1,
      "nombre": "[Nombre del proyecto/módulo]",
      "descripcion": "[Descripción general del proyecto]",
      "fecha_inicio": "2025-08-04",
      "epicas": [
        {
          "epic_id": 1,
          "titulo": "[Título de la épica]",
          "descripcion": "[Descripción de la épica]",
          "tareas": [
            {
              "descripcion": "[Descripción detallada del caso de prueba - qué se va a validar]",
              "resumen": "[Resumen corto del caso de prueba - título conciso]",
              "inicio": "[YYYY-MM-DD]",
              "fin": "[YYYY-MM-DD]",
              "estado": "Pendiente",
              "horas_estimadas": [número de horas]
            }
          ]
        }
      ]
    }
  ]
}
```

REGLAS IMPORTANTES PARA EL FORMATO JSON:
- "proyecto_id" y "epic_id" siempre tienen valor 1
- "estado" siempre es "Pendiente"
- Las fechas se calculan automáticamente desde 04/08/2025
- Se trabajan 8 horas por día (excluyendo fines de semana)
- "horas_estimadas" debe ser realista para cada caso de prueba (típicamente entre 2-8 horas)
- "descripcion" debe ser detallada explicando qué se validará
- "resumen" debe ser un título corto y claro del caso

Ejemplo correcto:
```json
{
  "proyectos": [
    {
      "proyecto_id": 1,
      "nombre": "Testing del Sistema de Mantenimiento",
      "descripcion": "Casos de prueba para validar la funcionalidad completa del módulo de mantenimiento",
      "fecha_inicio": "2025-08-04",
      "epicas": [
        {
          "epic_id": 1,
          "titulo": "Validación de Formularios",
          "descripcion": "Testing de todos los formularios del sistema",
          "tareas": [
            {
              "descripcion": "Validar que el botón 'Enviar' se muestra correctamente en la interfaz de carga y edición de la planilla de mantenimiento, junto a los botones 'Cancelar' y 'Guardar'. Verificar posición, funcionalidad y comportamiento esperado.",
              "resumen": "Verificar botón Enviar en formulario",
              "inicio": "2025-08-04",
              "fin": "2025-08-04",
              "estado": "Pendiente",
              "horas_estimadas": 4
            }
          ]
        }
      ]
    }
  ]
}
```
        """
    
    def generar_casos_dual_formato(self, contenido, casos_originales, proyecto_nombre="Sistema de Testing"):
        """Genera los casos en formato JSON basado en los casos originales ya creados"""
        try:
            fecha_inicio = "2025-08-04"
            fecha_actual = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            
            # Estructurar el JSON
            proyecto_json = {
                "proyectos": [
                    {
                        "proyecto_id": 1,
                        "nombre": proyecto_nombre,
                        "descripcion": f"Casos de prueba para validar la funcionalidad completa del {proyecto_nombre}",
                        "fecha_inicio": fecha_inicio,
                        "epicas": [
                            {
                                "epic_id": 1,
                                "titulo": "Validación Funcional Completa",
                                "descripcion": "Testing de todas las funcionalidades del sistema",
                                "tareas": []
                            }
                        ]
                    }
                ]
            }
            
            # Extraer casos de prueba del formato original
            lineas = casos_originales.split('\n')
            caso_actual = {}
            
            for linea in lineas:
                linea = linea.strip()
                
                if linea.startswith('CP-'):
                    # Nuevo caso de prueba
                    if caso_actual and 'titulo' in caso_actual:
                        # Agregar el caso anterior al JSON
                        self._agregar_caso_a_json(proyecto_json, caso_actual, fecha_actual)
                        fecha_actual += timedelta(days=1)
                        # Saltar fines de semana
                        while fecha_actual.weekday() > 4:  # 5=sábado, 6=domingo
                            fecha_actual += timedelta(days=1)
                    
                    # Iniciar nuevo caso
                    caso_actual = {
                        'titulo': linea.split(':', 1)[1].strip() if ':' in linea else linea
                    }
                
                elif linea.startswith('Descripción:'):
                    caso_actual['descripcion'] = linea.split(':', 1)[1].strip()
                
                elif linea.startswith('Módulo:'):
                    caso_actual['modulo'] = linea.split(':', 1)[1].strip()
                
                elif linea.startswith('Prioridad:'):
                    prioridad = linea.split(':', 1)[1].strip().lower()
                    # Asignar horas según prioridad
                    if prioridad == 'alta':
                        caso_actual['horas'] = 6
                    elif prioridad == 'media':
                        caso_actual['horas'] = 4
                    else:
                        caso_actual['horas'] = 2
            
            # Agregar el último caso
            if caso_actual and 'titulo' in caso_actual:
                self._agregar_caso_a_json(proyecto_json, caso_actual, fecha_actual)
            
            return json.dumps(proyecto_json, indent=2, ensure_ascii=False)
            
        except Exception as e:
            print(f"Error generando JSON: {e}")
            return self._generar_json_ejemplo()
    
    def _agregar_caso_a_json(self, proyecto_json, caso, fecha_inicio):
        """Método auxiliar para agregar un caso al JSON"""
        try:
            horas = caso.get('horas', 4)
            fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%d")
            
            # Calcular fecha fin
            fecha_fin = fecha_inicio
            if horas > 8:
                dias_extra = (horas - 8) // 8
                fecha_fin += timedelta(days=dias_extra)
                # Saltar fines de semana
                while fecha_fin.weekday() > 4:
                    fecha_fin += timedelta(days=1)
            
            fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")
            
            tarea = {
                "descripcion": caso.get('descripcion', caso.get('titulo', 'Caso de prueba')),
                "resumen": caso.get('titulo', 'Caso de prueba'),
                "inicio": fecha_inicio_str,
                "fin": fecha_fin_str,
                "estado": "Pendiente",
                "horas_estimadas": horas
            }
            
            proyecto_json["proyectos"][0]["epicas"][0]["tareas"].append(tarea)
            
        except Exception as e:
            print(f"Error agregando caso al JSON: {e}")
    
    def _generar_json_ejemplo(self):
        """Genera un JSON de ejemplo en caso de error"""
        ejemplo = {
            "proyectos": [
                {
                    "proyecto_id": 1,
                    "nombre": "Sistema de Testing",
                    "descripcion": "Casos de prueba para validar la funcionalidad del sistema",
                    "fecha_inicio": "2025-08-04",
                    "epicas": [
                        {
                            "epic_id": 1,
                            "titulo": "Validación Funcional",
                            "descripcion": "Testing de funcionalidades principales",
                            "tareas": [
                                {
                                    "descripcion": "Validar funcionalidad principal del sistema",
                                    "resumen": "Caso de prueba principal",
                                    "inicio": "2025-08-04",
                                    "fin": "2025-08-04",
                                    "estado": "Pendiente",
                                    "horas_estimadas": 4
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        return json.dumps(ejemplo, indent=2, ensure_ascii=False)
    
    def obtener_plantillas_qa_avanzadas(self):
        """Retorna plantillas especializadas para QA profesional"""
        return {
            'casos_api': """
PLANTILLA PARA CASOS DE PRUEBA DE API:

API-[NÚMERO]: [Nombre del endpoint] - [Método HTTP]
Endpoint: [URL del endpoint]
Método: [GET/POST/PUT/DELETE]
Descripción: [Qué valida este caso]
Precondiciones: [Estado requerido antes de la prueba]

Headers requeridos:
- Content-Type: application/json
- Authorization: Bearer [token]

Payload de entrada:
```json
{
  "campo1": "valor",
  "campo2": 123
}
```

Validaciones:
- Código de respuesta esperado: [200/201/400/etc]
- Estructura de respuesta
- Validación de campos obligatorios
- Validación de tipos de datos
- Manejo de errores

Casos de prueba:
1. Caso positivo con datos válidos
2. Caso negativo con datos inválidos
3. Caso de borde con valores límite
4. Caso de autenticación fallida
5. Caso de autorización insuficiente
            """,
            
            'casos_seguridad': """
PLANTILLA PARA CASOS DE TESTING DE SEGURIDAD:

SEC-[NÚMERO]: [Tipo de vulnerabilidad] - [Componente]
Categoría: [OWASP Top 10 / ISO 27001]
Severidad: [Crítica/Alta/Media/Baja]
Tipo de ataque: [Injection/XSS/CSRF/etc]

Escenario de ataque:
[Descripción del vector de ataque]

Pasos para reproducir:
1. [Configuración inicial]
2. [Preparación del ataque]
3. [Ejecución del ataque]
4. [Verificación del resultado]

Resultado esperado:
- El sistema debe rechazar el ataque
- Debe registrar el intento en logs
- No debe exponer información sensible

Criterios de aceptación:
- No hay exposición de datos
- Autenticación/autorización funciona
- Logs de seguridad generados
            """,
            
            'casos_performance': """
PLANTILLA PARA CASOS DE TESTING DE PERFORMANCE:

PERF-[NÚMERO]: [Tipo de prueba] - [Componente]
Objetivo: [Tiempo de respuesta/Throughput/Carga]
Herramienta: [JMeter/LoadRunner/Artillery]

Configuración de carga:
- Usuarios concurrentes: [número]
- Duración: [tiempo]
- Ramp-up: [tiempo de incremento]

Métricas a medir:
- Tiempo de respuesta promedio
- Percentil 95
- Throughput (requests/segundo)
- CPU y memoria del sistema
- Errores por segundo

Criterios de aceptación:
- Tiempo respuesta < [X] segundos
- Throughput > [X] req/seg
- Tasa de error < [X]%
- CPU < 80% y Memoria < 85%
            """,
            
            'checklist_deploy': """
CHECKLIST PRE-DEPLOY - QA SIGN-OFF:

🔍 TESTING FUNCIONAL
☐ Casos de prueba críticos ejecutados y aprobados
☐ Regression testing completado
☐ Integración con APIs externas validada
☐ Flujos de usuario end-to-end verificados
☐ Validación de datos y formularios

🔒 TESTING DE SEGURIDAD  
☐ Autenticación y autorización validadas
☐ Validación de inputs contra inyecciones
☐ Manejo seguro de sesiones
☐ Encriptación de datos sensibles
☐ Validación de permisos por rol

⚡ TESTING DE PERFORMANCE
☐ Tiempos de respuesta dentro de SLA
☐ Testing de carga bajo condiciones normales
☐ Testing de stress en picos de uso
☐ Optimización de queries de base de datos
☐ Caching funcionando correctamente

🖥️ TESTING DE UI/UX
☐ Responsive design en diferentes dispositivos
☐ Cross-browser compatibility
☐ Accesibilidad (WCAG guidelines)
☐ Usabilidad validada con usuarios
☐ Loading states y error messages

📊 TESTING DE DATOS
☐ Migración de datos validada
☐ Backup y recovery procedures
☐ Integridad referencial verificada
☐ Validación de reportes y analytics

🔧 CONFIGURACIÓN Y AMBIENTE
☐ Variables de ambiente configuradas
☐ Logs y monitoreo funcionando
☐ SSL/TLS certificados válidos
☐ CDN y assets optimizados
☐ Health checks implementados

📋 DOCUMENTACIÓN
☐ Release notes actualizadas
☐ Manual de usuario actualizado
☐ Documentación técnica completa
☐ Runbook de troubleshooting
☐ Plan de rollback definido

✅ APROBACIONES
☐ Product Owner approval
☐ Technical Lead approval  
☐ QA Manager sign-off
☐ Security team approval
☐ DevOps team ready

🚀 READY FOR DEPLOYMENT
            """
        }
    
    def generar_contexto_qa_especializado(self, tipo_contexto="general"):
        """Genera contextos especializados para diferentes tipos de QA"""
        contextos = {
            'qa_manual': """
Como QA Manual Senior especializado en:
• Diseño de casos de prueba exhaustivos y detallados
• Testing exploratorio y descubrimiento de defectos críticos  
• Validación de UX/UI y flujos de usuario end-to-end
• Documentación detallada de defectos con pasos para reproducir
• Testing de regresión y validación de fixes
• Coordinación con desarrollo para resolution de issues
• Testing de aceptación y validación de criterios de negocio

Enfoque: Calidad desde la perspectiva del usuario final
            """,
            
            'qa_automatizado': """
Como QA Automation Engineer especializado en:
• Desarrollo de frameworks de automatización escalables
• Scripts de testing con Selenium, Playwright, Cypress
• API testing automatizado con Postman, RestAssured
• Integración con pipelines CI/CD (Jenkins, GitLab, Azure)
• Testing de performance automatizado con JMeter, k6
• Reporting automático y dashboards de métricas
• Mantenimiento y optimización de test suites

Enfoque: Eficiencia y cobertura automatizada
            """,
            
            'qa_api': """
Como API Testing Specialist especializado en:
• Diseño de test suites para REST/GraphQL APIs
• Validación de contratos de API y schemas
• Testing de autenticación y autorización
• Performance testing de endpoints bajo carga
• Testing de integración entre microservicios
• Validación de handling de errores y edge cases
• Security testing específico para APIs

Enfoque: Calidad y confiabilidad de servicios
            """,
            
            'qa_security': """
Como Security Testing Expert especializado en:
• Evaluación de vulnerabilidades OWASP Top 10
• Penetration testing y ethical hacking
• Testing de autenticación, autorización y sesiones
• Validación de inputs y protección contra inyecciones
• Testing de configuraciones de seguridad
• Evaluación de cifrado y manejo de datos sensibles
• Compliance con estándares (ISO 27001, SOC 2)

Enfoque: Seguridad y protección de datos
            """,
            
            'qa_performance': """
Como Performance Testing Specialist especializado en:
• Load testing y stress testing con herramientas especializadas
• Análisis de bottlenecks y optimización de performance
• Testing de escalabilidad y capacity planning
• Monitoring y profiling de aplicaciones
• Testing de bases de datos bajo carga
• Evaluación de CDN y caching strategies
• SLA validation y performance benchmarking

Enfoque: Performance y escalabilidad
            """,
            
            'qa_mobile': """
Como Mobile QA Engineer especializado en:
• Testing en múltiples dispositivos y OS versions
• Automatización mobile con Appium, Espresso, XCUITest
• Testing de conectividad y scenarios offline
• Performance testing específico para mobile
• Testing de push notifications y deep linking
• App store compliance y submission testing
• Battery usage y memory leak testing

Enfoque: Experiencia móvil optimizada
            """
        }
        
        return contextos.get(tipo_contexto, contextos['qa_manual'])
    
    def obtener_templates_documentacion_qa(self):
        """Templates especializados para documentación QA"""
        return {
            'plan_pruebas': """
# PLAN DE PRUEBAS
## [Nombre del Proyecto] - Versión [X.X.X]

### 1. INFORMACIÓN GENERAL
- **Proyecto:** [Nombre]
- **Versión:** [X.X.X]
- **Fecha:** [DD/MM/YYYY]
- **QA Lead:** [Nombre]
- **Stakeholders:** [Lista]

### 2. OBJETIVOS Y ALCANCE
**Objetivos:**
- Validar funcionalidades críticas según AC
- Asegurar calidad y estabilidad del release
- Verificar compliance con estándares

**Incluye:**
- Testing funcional de nuevas features
- Regression testing de funcionalidades existentes
- Testing de integración con sistemas externos
- Performance testing bajo carga normal

**Excluye:**
- Testing de compatibilidad con browsers legacy
- Testing manual de funcionalidades automatizadas

### 3. ESTRATEGIA DE TESTING
**Tipos de Testing:**
- **Funcional:** Validación de requirements y AC
- **Regresión:** Automated smoke tests + manual spot checking
- **Integración:** APIs y flujos end-to-end
- **Performance:** Load testing de endpoints críticos
- **Security:** OWASP Top 10 validation

**Criterios de Entrada:**
- Development completo y unit tests passing
- Build deployed en ambiente de QA
- Test data preparada y configurada

**Criterios de Salida:**
- 100% casos críticos ejecutados y passed
- 0 defectos críticos o high priority open
- Performance tests dentro de SLA
- Sign-off de stakeholders

### 4. RECURSOS Y TIMELINE
**Team:**
- QA Lead: [Nombre] - Planning y coordination
- QA Engineers: [Nombres] - Execution
- Automation Engineer: [Nombre] - Scripts y CI/CD

**Timeline:**
- Planning: [fechas]
- Execution: [fechas]  
- Regression: [fechas]
- Sign-off: [fecha]

### 5. ENVIRONMENTS Y HERRAMIENTAS
**Ambientes:**
- DEV: Para smoke testing y early validation
- QA: Para testing completo y automation
- STAGING: Para final validation y UAT

**Herramientas:**
- Test Management: [Jira/TestRail/Azure DevOps]
- Automation: [Selenium/Playwright/Postman]
- Performance: [JMeter/LoadRunner]
- Bug Tracking: [Jira/Azure DevOps]

### 6. RIESGOS Y MITIGACIONES
**Riesgos Identificados:**
- Timeline ajustado para testing completo
  - *Mitigación:* Priorizar casos críticos, parallel execution
- Dependencia de APIs externas inestables
  - *Mitigación:* Mock services, fallback scenarios
- Limited access to production-like data
  - *Mitigación:* Data masking, synthetic data generation

### 7. COMUNICACIÓN Y REPORTING
**Daily Standups:** 9:00 AM con dev team
**Status Reports:** Daily a stakeholders
**Escalation Path:** QA Lead → Dev Lead → Project Manager
**Final Report:** Comprehensive summary con metrics y recommendations
            """,
            
            'estrategia_pruebas': """
# ESTRATEGIA DE PRUEBAS
## [Proyecto] - [Año]

### 1. VISIÓN Y OBJETIVOS
**Visión de Calidad:**
Asegurar que el software cumple con los estándares de calidad, 
performance y seguridad esperados por usuarios y stakeholders.

**Objetivos Estratégicos:**
- Detectar defectos temprano en el ciclo de desarrollo
- Asegurar compliance con requirements de negocio
- Minimizar riesgos de producción
- Optimizar ROI del esfuerzo de testing

### 2. ENFOQUE METODOLÓGICO
**Metodología:** [Agile/Waterfall/DevOps]
**Testing Approach:** [Risk-based/Requirements-based]
**Automation Strategy:** [Pyramid/Diamond/Trophy]

**Principios:**
- Shift-left testing approach
- Risk-based test prioritization  
- Continuous testing integration
- Test automation optimization

### 3. NIVELES DE TESTING
**Unit Testing (Desarrollo)**
- Responsable: Development team
- Cobertura objetivo: 80%+
- Herramientas: [Jest/JUnit/xUnit]

**Integration Testing (QA + Dev)**
- API testing automatizado
- Database integration validation
- Third-party services integration

**System Testing (QA)**
- End-to-end functional testing
- Business workflow validation
- Cross-browser/platform testing

**Acceptance Testing (Business + QA)**  
- User acceptance scenarios
- Business rule validation
- Sign-off criteria verification

### 4. TIPOS DE TESTING ESPECIALIZADOS
**Performance Testing:**
- Load testing para usage normal
- Stress testing para picos de tráfico
- Herramientas: JMeter, k6, LoadRunner

**Security Testing:**
- OWASP Top 10 validation
- Authentication/Authorization testing
- Data protection compliance

**Accessibility Testing:**
- WCAG 2.1 compliance
- Screen reader compatibility
- Keyboard navigation validation

**Mobile Testing:**
- Multiple device/OS combinations
- Native app performance
- Offline functionality

### 5. AUTOMATIZACIÓN
**Automation Pyramid:**
- 70% Unit tests (fast, isolated)
- 20% Integration tests (API, services)
- 10% E2E tests (critical user journeys)

**Herramientas:**
- UI: Selenium, Playwright, Cypress
- API: Postman, RestAssured, Pact
- Mobile: Appium, Espresso, XCUITest
- Performance: JMeter, k6, Artillery

**CI/CD Integration:**
- Automated test execution en pipelines
- Quality gates basados en test results
- Parallel execution para faster feedback

### 6. GESTIÓN DE DEFECTOS
**Clasificación:**
- **Crítico:** Bloquea funcionalidad core, security issues
- **Alto:** Funcionalidad importante afectada
- **Medio:** Minor functionality issues  
- **Bajo:** Cosmetic, nice-to-have fixes

**Workflow:**
New → Assigned → In Progress → Fixed → Verified → Closed

**SLA:**
- Crítico: 24 horas
- Alto: 72 horas  
- Medio: 1 semana
- Bajo: Next release cycle

### 7. MÉTRICAS Y KPIs
**Quality Metrics:**
- Defect density (defects/KLOC)
- Test coverage percentage
- Test execution progress
- Defect escape rate to production

**Efficiency Metrics:**  
- Test automation coverage
- Time to execute full regression
- Mean time to detect defects
- Cost per defect found

**Delivery Metrics:**
- Release frequency
- Lead time for changes
- Deployment frequency
- Mean time to recovery

### 8. ROLES Y RESPONSABILIDADES
**QA Manager:**
- Strategy definition y oversight
- Resource allocation y planning
- Stakeholder communication

**QA Lead:**
- Test planning y coordination
- Technical guidance y mentoring
- Quality gate decisions

**QA Engineers:**
- Test case design y execution
- Defect investigation y reporting
- Test automation development

**Automation Engineers:**
- Framework development y maintenance
- CI/CD pipeline integration
- Performance testing execution
            """
        }
    
    def generar_casos_desde_api_schema(self, schema_json):
        """Genera casos de prueba específicos para APIs desde schema JSON"""
        return f"""
Basándome en el schema JSON proporcionado, aquí están los casos de prueba para API:

{self.obtener_plantillas_qa_avanzadas()['casos_api']}

CASOS ESPECÍFICOS GENERADOS:
[Análisis del schema y generación de casos automática]
        """
    
    def generar_sesion_exploratoria_avanzada(self):
        """Genera una sesión de testing exploratorio estructurada"""
        return """
# SESIÓN DE TESTING EXPLORATORIO ESTRUCTURADA

## CHARTER DE LA SESIÓN
**Objetivo:** Explorar [área/funcionalidad] para descubrir issues relacionados con [usabilidad/performance/seguridad]
**Duración:** 90 minutos
**Tester:** [Nombre]
**Build:** [Versión]

## ESTRATEGIA DE EXPLORACIÓN
**Técnicas a usar:**
- Boundary value analysis
- Error guessing
- Negative testing scenarios
- User journey simulation
- Data variation testing

## ÁREAS DE ENFOQUE
1. **Happy Path Variations**
   - Diferentes combinaciones de inputs válidos
   - Secuencias alternativas de pasos
   - Timing variations

2. **Edge Cases y Boundaries**
   - Valores límite en campos numéricos
   - Strings muy largos o vacíos
   - Caracteres especiales y Unicode

3. **Error Scenarios**
   - Conectividad intermitente
   - Session timeouts
   - Permisos insuficientes
   - Recursos no disponibles

4. **Usability Heuristics**
   - Navigation intuitiveness
   - Error message clarity
   - Loading time perception
   - Mobile responsiveness

## NOTAS DE EXPLORACIÓN
**[Timestamp] - [Observación]**
- 10:15 - Botón submit queda disabled después de error de validación
- 10:23 - Modal no se puede cerrar con ESC key
- 10:31 - Loading spinner no aparece en operaciones lentas

## BUGS ENCONTRADOS
**BUG-001:** [Título descriptivo]
- **Severidad:** Alta
- **Pasos:** [1, 2, 3...]
- **Resultado:** [Comportamiento actual]
- **Esperado:** [Comportamiento correcto]

## PREGUNTAS SURGIDAS
- ¿Qué pasa si el usuario tiene múltiples sesiones abiertas?
- ¿El sistema maneja correctamente cambios de timezone?
- ¿Hay validación del lado servidor para todos los inputs?

## FOLLOW-UP ACTIONS
- [ ] Crear bug reports para issues encontrados
- [ ] Proponer casos de prueba para scenarios interesantes
- [ ] Investigar más a fondo [área específica]
- [ ] Coordinar con UX team sobre findings de usabilidad
        """
    
    def obtener_plantilla_manual_usuario(self):
        """Retorna la plantilla estándar para manuales de usuario"""
        return """
IMPORTANTE: Todos los manuales de usuario deben seguir EXACTAMENTE esta estructura:

ESTRUCTURA PRINCIPAL DEL MANUAL:
====================================

# Manual de Usuario 
## [NOMBRE DEL SISTEMA]

[LOGO O IMAGEN SI CORRESPONDE]

## ÍNDICE
1. **Introducción**
   1.1. Objetivo del Manual
   1.2. Alcance del Sistema
   1.3. Audiencia Objetivo
2. **Información General**
   2.1. Descripción del Sistema
   2.2. Requisitos del Sistema
   2.3. Acceso al Sistema
3. **Guía de Usuario**
   3.1. Primer Acceso
   3.2. Navegación General
   3.3. Interfaz Principal
4. **Funcionalidades del Sistema**
   4.1. [Módulo 1]
   4.2. [Módulo 2]
   4.3. [Módulo 3]
   [... continuar con todos los módulos]
5. **Casos de Uso Comunes**
   5.1. Tareas Diarias
   5.2. Tareas Periódicas
   5.3. Tareas Administrativas
6. **Solución de Problemas**
   6.1. Problemas Comunes
   6.2. Códigos de Error
   6.3. Contacto de Soporte
7. **Anexos**
   7.1. Glosario
   7.2. Referencias
   7.3. Notas de Versión

====================================
FORMATO PARA CADA MÓDULO:
====================================

## [Número]. [Nombre del Módulo]

### Descripción General
[Explicación clara y detallada de qué hace el módulo, cuál es su propósito principal y cómo beneficia al usuario]

### Objetivos del Módulo
- [Objetivo 1]: [Descripción del beneficio]
- [Objetivo 2]: [Descripción del beneficio]
- [Objetivo 3]: [Descripción del beneficio]

### Funcionalidades Principales
• **[Funcionalidad 1]**: [Descripción breve y clara]
• **[Funcionalidad 2]**: [Descripción breve y clara]
• **[Funcionalidad 3]**: [Descripción breve y clara]

### Cómo Acceder al Módulo
1. [Paso detallado 1 - desde dónde empezar]
2. [Paso detallado 2 - qué buscar o dónde hacer clic]
3. [Paso detallado 3 - confirmación de acceso]

---

### [Nombre de la Funcionalidad Específica]

**Propósito:** [Para qué sirve esta funcionalidad específica]

**Cuándo usar:** [En qué situaciones es útil esta función]

**Pasos detallados:**

1. **[Acción inicial]**: [Explicación detallada del primer paso, incluyendo dónde hacer clic, qué buscar en pantalla]
   
2. **[Navegación]**: [Descripción de la pantalla que aparece, elementos importantes a considerar]
   
3. **[Completar información]**: [Qué campos completar, cuáles son obligatorios, formato esperado]
   
4. **[Validación]**: [Cómo verificar que la información esté correcta antes de continuar]
   
5. **[Confirmación]**: [Cómo guardar o confirmar la acción, qué botón usar]
   
6. **[Verificación final]**: [Qué verá el usuario como confirmación de que la acción fue exitosa]

**Consejos útiles:**
- [Tip 1]: [Consejo práctico para mejorar la experiencia]
- [Tip 2]: [Advertencia importante o buena práctica]
- [Tip 3]: [Atajo o funcionalidad adicional útil]

**Solución de problemas:**
- **Si [problema común]**: [Solución paso a paso]
- **Si [otro problema]**: [Otra solución]

---

====================================
EJEMPLO DE FORMATO CORRECTO:
====================================

## 3. Módulo de Gestión de Entidades

### Descripción General
El módulo de Gestión de Entidades permite administrar toda la información relacionada con las empresas, organizaciones y personas que son clientes o proveedores del sistema. Este módulo centraliza los datos de contacto, información legal, direcciones y permite mantener un registro histórico de todas las interacciones. Es fundamental para la gestión de relaciones comerciales y el seguimiento de clientes.

### Objetivos del Módulo
- **Centralización de datos**: Mantener toda la información de entidades en un solo lugar
- **Trazabilidad**: Registro histórico de cambios y actualizaciones
- **Eficiencia**: Acceso rápido a información relevante de clientes y proveedores
- **Calidad de datos**: Validaciones que aseguran información completa y correcta

### Funcionalidades Principales
• **Crear nueva entidad**: Registro de nuevas empresas o personas en el sistema
• **Editar entidad existente**: Modificación de datos de entidades ya registradas
• **Consultar información**: Visualización detallada de todos los datos de la entidad
• **Buscar y filtrar**: Localización rápida de entidades usando diferentes criterios
• **Gestionar contactos**: Administración de múltiples contactos por entidad
• **Historial de cambios**: Registro de todas las modificaciones realizadas

### Cómo Acceder al Módulo
1. Desde la pantalla principal del sistema, localice el menú lateral izquierdo
2. Busque y haga clic en "Gestión de Entidades" o el ícono 🏢
3. El sistema cargará la pantalla principal del módulo con la lista de entidades

---

### Crear una Nueva Entidad

**Propósito:** Registrar una nueva empresa, organización o persona en el sistema para futuras transacciones comerciales.

**Cuándo usar:** Cuando necesite registrar un nuevo cliente, proveedor o cualquier entidad con la que la empresa vaya a tener relaciones comerciales.

**Pasos detallados:**

1. **Acceder al formulario**: Desde la pantalla principal del módulo de entidades, localice el botón "Nueva Entidad" en la parte superior derecha y haga clic en él.

2. **Seleccionar tipo de entidad**: En la pantalla que aparece, elija si va a registrar una "Empresa" o "Persona Natural" marcando la opción correspondiente.

3. **Completar información básica**: Llene los siguientes campos obligatorios (marcados con asterisco rojo):
   - **Nombre/Razón Social**: Nombre completo de la empresa o persona
   - **Número de identificación**: RUC para empresas, Cédula para personas
   - **Tipo de entidad**: Cliente, Proveedor, o Ambos

4. **Agregar información de contacto**: Complete los datos de contacto:
   - **Dirección principal**: Dirección física completa
   - **Teléfono principal**: Número de contacto preferido
   - **Email principal**: Correo electrónico de contacto

5. **Información adicional (opcional)**: Si lo desea, puede completar:
   - Dirección secundaria
   - Teléfonos adicionales
   - Emails alternativos
   - Página web
   - Observaciones especiales

6. **Validar y guardar**: Revise toda la información ingresada, asegúrese de que no haya errores y haga clic en "Guardar Entidad".

7. **Confirmación**: El sistema mostrará un mensaje verde "Entidad creada exitosamente" y la nueva entidad aparecerá automáticamente en la lista principal.

**Consejos útiles:**
- **Verificación de duplicados**: El sistema verificará automáticamente si ya existe una entidad con el mismo número de identificación
- **Campos obligatorios**: Los campos marcados con asterisco (*) son obligatorios y deben completarse
- **Formato de identificación**: Para RUC usar formato 20-XXXXXXXX-X, para cédula 0-XXXX-XXXX

**Solución de problemas:**
- **Si aparece "Número de identificación ya existe"**: Verifique si la entidad ya está registrada usando la función de búsqueda
- **Si no se puede guardar**: Revise que todos los campos obligatorios estén completos y en el formato correcto
- **Si hay error de formato**: Verifique que el email tenga formato válido (usuario@dominio.com) y el teléfono solo contenga números

---

IMPORTANTE PARA EL MANUAL: 
- El manual debe ser **descriptivo y educativo**, guiando al usuario paso a paso
- **NO incluir** "Resultado esperado" ni elementos típicos de casos de prueba
- Enfocarse en **CÓMO usar el sistema**, no en validar si funciona
- Usar lenguaje claro y accesible para usuarios finales
- Incluir **consejos prácticos** y **solución de problemas comunes**
- Proporcionar **contexto** sobre cuándo y por qué usar cada funcionalidad
        """
    
    def responder_con_ia(self, mensaje):
        """Genera respuesta usando Google AI"""
        try:
            # Detectar si hay archivos adjuntos en el mensaje
            tiene_archivos = "--- ARCHIVOS ADJUNTOS ---" in mensaje
            
            # Detectar si el usuario solicita un rol específico
            rol_solicitado = self.detectar_rol_solicitado(mensaje)
            
            # Detectar funcionalidades QA específicas
            contexto_qa = self.detectar_contexto_qa_especializado(mensaje)
            
            if tiene_archivos:
                # Extraer solo la pregunta del usuario (sin el contenido de archivos)
                pregunta_usuario = mensaje.split("--- ARCHIVOS ADJUNTOS ---")[0].strip()
                if not pregunta_usuario:
                    pregunta_usuario = "Analiza este archivo"
                
                # Para mensajes con archivos, usar un prompt especializado pero específico
                # Detectar si se solicitan casos de prueba
                solicita_casos_prueba = any(palabra in pregunta_usuario.lower() for palabra in 
                                          ['casos de prueba', 'test cases', 'casos prueba', 'generar casos', 'crear casos'])
                
                # Detectar si se solicita manual de usuario
                solicita_manual_usuario = any(palabra in pregunta_usuario.lower() for palabra in 
                                            ['manual de usuario', 'manual usuario', 'documentacion usuario', 'guia usuario', 
                                             'documentation user', 'user manual', 'guia de usuario', 'manual del usuario'])
                
                if rol_solicitado or contexto_qa:
                    # Agregar plantillas según lo solicitado
                    plantilla_casos = self.obtener_plantilla_casos_prueba() if solicita_casos_prueba else ""
                    plantilla_casos_json = self.obtener_plantilla_casos_prueba_json() if solicita_casos_prueba else ""
                    plantilla_manual = self.obtener_plantilla_manual_usuario() if solicita_manual_usuario else ""
                    plantillas_qa = self.obtener_plantillas_qa_avanzadas() if contexto_qa else {}
                    contexto_especializado = self.generar_contexto_qa_especializado(contexto_qa) if contexto_qa else ""
                    
                    rol_final = rol_solicitado or f"QA Specialist - {contexto_qa}"
                    
                    prompt = f"""Eres {self.nombre}, actuando como {rol_final}.

{self.obtener_contexto_rol(rol_solicitado) if rol_solicitado else contexto_especializado}

IMPORTANTE: Mantén tu rol de {rol_final} y responde ÚNICAMENTE lo que el usuario solicita.

{plantilla_casos}
{plantilla_casos_json}
{plantilla_manual}

El usuario solicita: "{pregunta_usuario}"

{"INSTRUCCIÓN ESPECIAL PARA CASOS DE PRUEBA: Si el usuario solicita casos de prueba, debes generar AMBOS formatos: el formato original estándar Y el formato JSON. Presenta primero el formato original completo, luego una separación clara, y después el formato JSON completo." if solicita_casos_prueba else ""}

Basándote en tu experiencia como {rol_final} y en su solicitud específica:

Historial reciente:
{self.obtener_historial_reciente()}

Contenido del archivo y solicitud:
{mensaje}

Responde como {rol_final} específicamente a lo solicitado:"""
                else:
                    # Agregar plantillas según lo solicitado
                    plantilla_casos = self.obtener_plantilla_casos_prueba() if solicita_casos_prueba else ""
                    plantilla_casos_json = self.obtener_plantilla_casos_prueba_json() if solicita_casos_prueba else ""
                    plantilla_manual = self.obtener_plantilla_manual_usuario() if solicita_manual_usuario else ""
                    
                    prompt = f"""Eres {self.nombre}, un chatbot especializado en análisis de documentos y QA profesional.

IMPORTANTE: Responde ÚNICAMENTE lo que el usuario solicita. No agregues información extra no solicitada.

{plantilla_casos}
{plantilla_casos_json}
{plantilla_manual}

El usuario solicita: "{pregunta_usuario}"

{"INSTRUCCIÓN ESPECIAL PARA CASOS DE PRUEBA: Si el usuario solicita casos de prueba, debes generar AMBOS formatos: el formato original estándar Y el formato JSON. Presenta primero el formato original completo, luego una separación clara, y después el formato JSON completo." if solicita_casos_prueba else ""}

Basándote en su solicitud específica, puedes:
- Si pide un RESUMEN: Proporciona solo un resumen claro y conciso
- Si pide CASOS DE PRUEBA: Genera casos de prueba detallados siguiendo AMBAS plantillas (original y JSON)
- Si pide MANUAL DE USUARIO: Genera documentación siguiendo la estructura específica
- Si pide ANÁLISIS: Analiza el contenido según su solicitud
- Si pide REVISIÓN DE CÓDIGO: Revisa y sugiere mejoras
- Si no especifica: Pregunta qué tipo de análisis necesita

Historial reciente:
{self.obtener_historial_reciente()}

Contenido del archivo y solicitud:
{mensaje}

Responde específicamente a lo solicitado por el usuario:"""
            else:
                # Prompt normal para conversación regular
                # Detectar si se solicitan casos de prueba
                solicita_casos_prueba = any(palabra in mensaje.lower() for palabra in 
                                          ['casos de prueba', 'test cases', 'casos prueba', 'generar casos', 'crear casos'])
                
                # Detectar si se solicita manual de usuario
                solicita_manual_usuario = any(palabra in mensaje.lower() for palabra in 
                                            ['manual de usuario', 'manual usuario', 'documentacion usuario', 'guia usuario', 
                                             'documentation user', 'user manual', 'guia de usuario', 'manual del usuario'])
                
                if rol_solicitado or contexto_qa:
                    # Agregar plantillas según lo solicitado
                    plantilla_casos = self.obtener_plantilla_casos_prueba() if solicita_casos_prueba else ""
                    plantilla_casos_json = self.obtener_plantilla_casos_prueba_json() if solicita_casos_prueba else ""
                    plantilla_manual = self.obtener_plantilla_manual_usuario() if solicita_manual_usuario else ""
                    plantillas_qa = self.obtener_plantillas_qa_avanzadas() if contexto_qa else {}
                    contexto_especializado = self.generar_contexto_qa_especializado(contexto_qa) if contexto_qa else ""
                    
                    rol_final = rol_solicitado or f"QA Specialist - {contexto_qa}"
                    
                    # Agregar plantillas QA específicas si aplica
                    plantillas_texto = ""
                    if plantillas_qa:
                        plantillas_texto = "\n".join([f"=== {k.upper()} ===\n{v}" for k, v in plantillas_qa.items()])
                    
                    prompt = f"""Eres {self.nombre}, actuando como {rol_final}.

{self.obtener_contexto_rol(rol_solicitado) if rol_solicitado else contexto_especializado}

{plantilla_casos}
{plantilla_casos_json}
{plantilla_manual}
{plantillas_texto}

{"INSTRUCCIÓN ESPECIAL PARA CASOS DE PRUEBA: Si el usuario solicita casos de prueba, debes generar AMBOS formatos: el formato original estándar Y el formato JSON. Presenta primero el formato original completo, luego una separación clara, y después el formato JSON completo." if solicita_casos_prueba else ""}

Mantén tu rol y personalidad como {rol_final} durante toda la conversación.

Historial reciente de la conversación:
{self.obtener_historial_reciente()}

Usuario: {mensaje}

Responde como {rol_final} de manera profesional y experta:"""
                else:
                    # Agregar plantillas según lo solicitado
                    plantilla_casos = self.obtener_plantilla_casos_prueba() if solicita_casos_prueba else ""
                    plantilla_casos_json = self.obtener_plantilla_casos_prueba_json() if solicita_casos_prueba else ""
                    plantilla_manual = self.obtener_plantilla_manual_usuario() if solicita_manual_usuario else ""
                    
                    # Detectar si es una pregunta simple o técnica
                    preguntas_simples = ['como estas', 'que tal', 'hola', 'hi', 'buenos dias', 'buenas tardes', 
                                        'buenas noches', 'como te encuentras', 'que haces', 'adios', 'chao',
                                        'hasta luego', 'gracias', 'muchas gracias', 'de nada', 'ok', 'vale']
                    
                    es_pregunta_simple = any(palabra in mensaje.lower() for palabra in preguntas_simples)
                    
                    if es_pregunta_simple:
                        prompt = f"""Eres {self.nombre}, un chatbot amigable especializado en QA y testing.
                        
Responde de manera BREVE, NATURAL y AMIGABLE. NO uses formato estructurado para saludos o preguntas simples.

Usuario: {mensaje}

Responde de forma corta y conversacional (máximo 2-3 líneas):"""
                    else:
                        prompt = f"""Eres {self.nombre}, un chatbot especializado en QA y testing. 
                        
IMPORTANTE: Para consultas técnicas o complejas, responde en formato estructurado:

# 📌 [TÍTULO PRINCIPAL]
Breve introducción (máximo 2-3 líneas).

## 1️⃣ **Objetivo**
Descripción del propósito.

## 2️⃣ **Alcance**
Qué incluye y excluye.

## 3️⃣ **Estructura Detallada**
- **Punto 1**: Descripción
- **Punto 2**: Descripción

## 4️⃣ **Recomendaciones**
Consejos prácticos.

## 5️⃣ **Conclusión**
Resumen breve.

⚠️ Usa **negrita** para términos clave.
                        
{plantilla_casos}
{plantilla_casos_json}
{plantilla_manual}

{"INSTRUCCIÓN ESPECIAL PARA CASOS DE PRUEBA: Si el usuario solicita casos de prueba, debes generar AMBOS formatos: el formato original estándar Y el formato JSON. Presenta primero el formato original completo, luego una separación clara, y después el formato JSON completo." if solicita_casos_prueba else ""}
                        
Historial reciente:
{self.obtener_historial_reciente()}
                        
Usuario: {mensaje}
                        
Responde siguiendo el formato estructurado para esta consulta técnica:"""
            
            response = self.modelo_ia.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error con IA: {e}")
            return self.responder_localmente(mensaje)
    
    def detectar_contexto_qa_especializado(self, mensaje):
        """Detecta contextos QA especializados en el mensaje"""
        mensaje_lower = mensaje.lower()
        
        # Patrones para diferentes especializaciones QA
        contextos_qa = {
            "qa_api": [
                "endpoint", "api testing", "rest api", "json schema", "postman",
                "test api", "api cases", "swagger", "openapi", "microservices"
            ],
            "qa_security": [
                "security testing", "owasp", "vulnerabilities", "penetration test",
                "authentication", "authorization", "sql injection", "xss", "csrf"
            ],
            "qa_performance": [
                "performance testing", "load testing", "stress testing", "jmeter",
                "performance cases", "response time", "throughput", "scalability"
            ],
            "qa_mobile": [
                "mobile testing", "app testing", "android testing", "ios testing",
                "mobile automation", "appium", "device testing"
            ],
            "qa_automatizado": [
                "test automation", "selenium", "playwright", "cypress", "automation scripts",
                "automated testing", "test framework", "ci/cd testing"
            ],
            "qa_manual": [
                "manual testing", "exploratory testing", "user acceptance testing",
                "uat", "manual test cases", "regression testing"
            ]
        }
        
        for contexto, patrones in contextos_qa.items():
            for patron in patrones:
                if patron in mensaje_lower:
                    return contexto
        
        # Si menciona QA en general pero no específico
        if any(palabra in mensaje_lower for palabra in ["qa", "quality assurance", "testing", "test cases"]):
            return "qa_manual"  # Default a manual QA
        
        return None
    
    def detectar_rol_solicitado(self, mensaje):
        """Detecta si el usuario solicita un rol específico"""
        mensaje_lower = mensaje.lower()
        
        # Patrones para diferentes roles profesionales
        roles = {
            "experto en QA y casos de prueba": [
                "actua como experto en qa", "actua como ingeniero qa", "actua como tester",
                "actua como experto en testing", "actua como experto en casos de prueba",
                "comportate como qa", "comportate como tester", "eres un experto qa",
                "eres un ingeniero qa", "experto en quality assurance"
            ],
            "arquitecto de software": [
                "actua como arquitecto", "actua como arquitecto de software",
                "comportate como arquitecto", "eres un arquitecto de software"
            ],
            "analista de negocio": [
                "actua como analista", "actua como analista de negocio",
                "comportate como analista", "eres un analista de negocio"
            ],
            "desarrollador senior": [
                "actua como desarrollador", "actua como programador senior",
                "comportate como desarrollador", "eres un desarrollador senior"
            ],
            "consultor técnico": [
                "actua como consultor", "actua como consultor tecnico",
                "comportate como consultor", "eres un consultor técnico"
            ]
        }
        
        for rol, patrones in roles.items():
            for patron in patrones:
                if patron in mensaje_lower:
                    return rol
        
        return None
    
    def obtener_contexto_rol(self, rol):
        """Obtiene el contexto y características de un rol específico"""
        contextos_roles = {
            "experto en QA y casos de prueba": """
Como experto en QA y casos de prueba con más de 10 años de experiencia, tienes:

• Especialización en metodologías de testing (manual y automatizado)
• Experiencia en diseño de casos de prueba exhaustivos
• Conocimiento profundo de ISTQB, Agile Testing, y mejores prácticas
• Habilidad para identificar escenarios de borde y casos críticos
• Experiencia en documentación de defectos y seguimiento
• Conocimiento en herramientas como Jira, TestRail, Selenium, etc.
• Enfoque en calidad, cobertura de pruebas y análisis de riesgos

Tu objetivo es asegurar la máxima calidad del software mediante pruebas rigurosas.
            """,
            
            "arquitecto de software": """
Como arquitecto de software senior con amplia experiencia, tienes:

• Diseño de arquitecturas escalables y mantenibles
• Conocimiento profundo de patrones de diseño y arquitectura
• Experiencia en tecnologías cloud y microservicios
• Habilidad para evaluar y recomendar tecnologías
• Enfoque en performance, seguridad y escalabilidad
• Experiencia en documentación técnica y diagramas de arquitectura

Tu objetivo es diseñar soluciones técnicas robustas y eficientes.
            """,
            
            "analista de negocio": """
Como analista de negocio experimentado, tienes:

• Habilidad para entender procesos de negocio complejos
• Experiencia en levantamiento y análisis de requisitos
• Conocimiento en modelado de procesos y documentación
• Habilidad para traducir necesidades de negocio a requerimientos técnicos
• Experiencia en stakeholder management
• Enfoque en optimización de procesos y ROI

Tu objetivo es maximizar el valor de negocio de las soluciones.
            """,
            
            "desarrollador senior": """
Como desarrollador senior con amplia experiencia, tienes:

• Dominio de múltiples lenguajes y frameworks
• Experiencia en código limpio y mejores prácticas
• Conocimiento profundo de algoritmos y estructuras de datos
• Habilidad para revisar código y mentorear juniors
• Experiencia en debugging y optimización
• Enfoque en mantenibilidad y performance

Tu objetivo es escribir código de alta calidad y eficiente.
            """,
            
            "consultor técnico": """
Como consultor técnico experimentado, tienes:

• Amplio conocimiento en múltiples tecnologías y metodologías
• Habilidad para analizar problemas complejos y proponer soluciones
• Experiencia en diferentes industrias y proyectos
• Enfoque en mejores prácticas y estándares de la industria
• Habilidad para comunicar conceptos técnicos a diferentes audiencias
• Experiencia en auditorías técnicas y recomendaciones estratégicas

Tu objetivo es proporcionar guidance experto y soluciones optimizadas.
            """
        }
        
        return contextos_roles.get(rol, "Actúa como un profesional experto en tu área.")
    
    def obtener_historial_reciente(self):
        """Obtiene las últimas 3 interacciones para contexto"""
        if len(self.historial_conversacion) == 0:
            return "Esta es la primera interacción."
        
        historial = ""
        for interaccion in self.historial_conversacion[-3:]:
            historial += f"Usuario: {interaccion['usuario']}\n{self.nombre}: {interaccion['bot']}\n"
        return historial if historial else "Esta es la primera interacción."
    
    def crear_directorio_historial(self):
        """Crea el directorio para guardar el historial si no existe"""
        try:
            if not os.path.exists(self.directorio_historial):
                os.makedirs(self.directorio_historial)
        except Exception as e:
            print(f"Error creando directorio de historial: {e}")
    
    def guardar_conversacion(self, mensaje_usuario, respuesta_bot):
        """Guarda una conversación individual en la sesión actual"""
        conversacion = {
            'timestamp': datetime.now().isoformat(),
            'usuario': mensaje_usuario,
            'bot': respuesta_bot,
            'fue_ia': self.usar_ia and not self.es_respuesta_local(mensaje_usuario)
        }
        
        self.sesion_actual['conversaciones'].append(conversacion)
    
    def guardar_sesion_completa(self):
        """Guarda toda la sesión actual en un archivo JSON"""
        try:
            # Preparar datos de la sesión
            self.sesion_actual['fin'] = datetime.now().isoformat()
            self.sesion_actual['total_mensajes'] = len(self.sesion_actual['conversaciones'])
            
            # Crear nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"conversacion_{timestamp}.json"
            ruta_archivo = os.path.join(self.directorio_historial, nombre_archivo)
            
            # Guardar archivo
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.sesion_actual, f, ensure_ascii=False, indent=2)
            
            return ruta_archivo
        except Exception as e:
            print(f"Error guardando sesión: {e}")
            return None
    
    def cargar_historial_sesiones(self):
        """Carga todas las sesiones guardadas"""
        try:
            sesiones = []
            if os.path.exists(self.directorio_historial):
                for archivo in os.listdir(self.directorio_historial):
                    if archivo.endswith('.json'):
                        ruta_archivo = os.path.join(self.directorio_historial, archivo)
                        with open(ruta_archivo, 'r', encoding='utf-8') as f:
                            sesion = json.load(f)
                            sesiones.append({
                                'archivo': archivo,
                                'datos': sesion
                            })
            
            # Ordenar por fecha (más reciente primero)
            sesiones.sort(key=lambda x: x['datos']['inicio'], reverse=True)
            return sesiones
        except Exception as e:
            print(f"Error cargando historial: {e}")
            return []
    
    def obtener_estadisticas_historial(self):
        """Obtiene estadísticas del historial completo"""
        try:
            sesiones = self.cargar_historial_sesiones()
            total_sesiones = len(sesiones)
            total_conversaciones = sum(len(s['datos']['conversaciones']) for s in sesiones)
            
            if sesiones:
                primera_sesion = min(s['datos']['inicio'] for s in sesiones)
                ultima_sesion = max(s['datos']['inicio'] for s in sesiones)
            else:
                primera_sesion = None
                ultima_sesion = None
            
            return {
                'total_sesiones': total_sesiones,
                'total_conversaciones': total_conversaciones,
                'primera_sesion': primera_sesion,
                'ultima_sesion': ultima_sesion
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return None
    
    def procesar_mensaje(self, mensaje):
        """Procesa el mensaje del usuario y devuelve una respuesta"""
        mensaje_limpio = mensaje.lower().strip()
        
        # Verificar si hay archivos adjuntos
        tiene_archivos = "--- ARCHIVOS ADJUNTOS ---" in mensaje
        
        # Verificar si debe responder localmente (pero no si hay archivos)
        if (self.es_respuesta_local(mensaje) and not tiene_archivos) or not self.usar_ia:
            if tiene_archivos and not self.usar_ia:
                respuesta = self.generar_respuesta_archivo_local(mensaje)
            else:
                respuesta = self.responder_localmente(mensaje)
        else:
            respuesta = self.responder_con_ia(mensaje)
        
        # Agregar al historial (solo la parte del mensaje del usuario, no los archivos completos)
        mensaje_para_historial = mensaje.split("--- ARCHIVOS ADJUNTOS ---")[0].strip()
        if not mensaje_para_historial:
            mensaje_para_historial = "Análisis de archivos adjuntos"
        
        self.historial_conversacion.append({
            'usuario': mensaje_para_historial,
            'bot': respuesta
        })
        
        # Guardar conversación individual
        self.guardar_conversacion(mensaje_para_historial, respuesta)
        
        # Mantener solo las últimas 10 interacciones en memoria
        if len(self.historial_conversacion) > 10:
            self.historial_conversacion = self.historial_conversacion[-10:]
        
        return respuesta
    
    def analizar_contenido_archivo(self, contenido_archivo, tipo_analisis="general"):
        """Analiza el contenido de un archivo y genera respuestas específicas"""
        respuestas_analisis = {
            "casos_prueba": [
                "Basándome en el documento, aquí están los casos de prueba sugeridos:",
                "He analizado el contenido y generado estos casos de prueba:",
                "Según la documentación proporcionada, estos son los casos de prueba recomendados:"
            ],
            "analisis_codigo": [
                "He revisado el código y encontré los siguientes puntos:",
                "Análisis del código completado. Observaciones:",
                "Revisión de código finalizada. Sugerencias:"
            ],
            "analisis_documento": [
                "He analizado el documento y aquí está mi evaluación:",
                "Resumen del análisis del documento:",
                "Análisis completado. Puntos clave encontrados:"
            ]
        }
        
        if tipo_analisis in respuestas_analisis:
            return random.choice(respuestas_analisis[tipo_analisis])
        else:
            return "He analizado el contenido del archivo adjunto:"
    
    def detectar_tipo_contenido(self, contenido):
        """Detecta el tipo de contenido para dar respuestas más específicas"""
        contenido_lower = contenido.lower()
        
        # Detectar si es documentación de requisitos/casos de uso
        if any(palabra in contenido_lower for palabra in 
               ['requisito', 'caso de uso', 'funcionalidad', 'especificación', 'requirement']):
            return "requisitos"
        
        # Detectar si es código
        elif any(palabra in contenido_lower for palabra in 
                ['def ', 'class ', 'function', 'import', 'if __name__', 'public class']):
            return "codigo"
        
        # Detectar si son datos/configuración
        elif any(palabra in contenido_lower for palabra in 
                ['json', 'xml', 'csv', 'data', 'config']):
            return "datos"
        
        # Detectar si es documentación técnica
        elif any(palabra in contenido_lower for palabra in 
                ['manual', 'documentación', 'guía', 'tutorial', 'procedimiento']):
            return "documentacion"
        
        else:
            return "general"
    
    def generar_respuesta_archivo_local(self, mensaje):
        """Genera respuesta local cuando hay archivos adjuntos pero no hay IA"""
        if "--- ARCHIVOS ADJUNTOS ---" in mensaje:
            return ("He recibido tus archivos adjuntos. Aunque no tengo acceso a IA en este momento, "
                   "puedo ver que has adjuntado documentos. Para un análisis completo y generación de casos de prueba, "
                   "sería necesario tener la conexión de IA activa. ¿Hay algo específico sobre los archivos que te gustaría discutir?")
        else:
            return self.responder_localmente(mensaje)
    
    def agregar_respuesta(self, patron, respuestas):
        """Permite agregar nuevas respuestas locales al chatbot"""
        if isinstance(respuestas, str):
            respuestas = [respuestas]
        self.respuestas_locales[patron] = respuestas
    
    def iniciar_conversacion(self):
        """Inicia la conversación con el usuario"""
        print(f"🤖 ¡Hola! Soy {self.nombre}, tu chatbot personal.")
        if self.usar_ia:
            print("✨ Tengo capacidades de IA avanzadas para ayudarte mejor.")
        print("💬 Escribe 'salir' para terminar la conversación.")
        print("-" * 60)
        
        while True:
            try:
                # Obtener input del usuario
                mensaje_usuario = input("Tú: ").strip()
                
                # Verificar si quiere salir
                if mensaje_usuario.lower() in ['salir', 'exit', 'quit']:
                    print(f"{self.nombre}: ¡Hasta luego! Que tengas un buen día.")
                    break
                
                # Verificar que no esté vacío
                if not mensaje_usuario:
                    print(f"{self.nombre}: Por favor, escribe algo para que pueda ayudarte.")
                    continue
                
                # Procesar y responder
                respuesta = self.procesar_mensaje(mensaje_usuario)
                print(f"{self.nombre}: {respuesta}")
                
            except KeyboardInterrupt:
                print(f"\n{self.nombre}: ¡Hasta luego!")
                break
            except Exception as e:
                print(f"{self.nombre}: Lo siento, ocurrió un error. ¿Puedes intentar de nuevo?")

def main():
    """Función principal para ejecutar el chatbot"""
    # Crear una instancia del chatbot
    mi_chatbot = ChatBot("Asistente Virtual")
    
    # Agregar algunas respuestas personalizadas (opcional)
    mi_chatbot.agregar_respuesta(
        "python|programacion|codigo", 
        [
            "¡Me encanta Python! Es un lenguaje muy versátil.",
            "Python es excelente para principiantes y expertos.",
            "La programación es fascinante, ¿en qué proyecto estás trabajando?"
        ]
    )
    
    mi_chatbot.agregar_respuesta(
        "clima|temperatura|lluvia|sol", 
        [
            "No tengo acceso a información del clima en tiempo real.",
            "Te recomiendo consultar una app del clima para información actualizada.",
            "¿Hace buen día donde estás?"
        ]
    )
    
    mi_chatbot.agregar_respuesta(
        "casos de prueba|testing|qa|quality assurance", 
        [
            "¡Excelente! Puedo ayudarte a generar casos de prueba detallados.",
            "Los casos de prueba son fundamentales para la calidad del software.",
            "¿Tienes algún documento de requisitos que quieras que analice para generar casos de prueba?"
        ]
    )
    
    # Iniciar la conversación
    mi_chatbot.iniciar_conversacion()

if __name__ == "__main__":
    main()