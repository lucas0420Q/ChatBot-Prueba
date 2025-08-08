import re
import random
import os
import json
from datetime import datetime
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
    
    def responder_con_ia(self, mensaje):
        """Genera respuesta usando Google AI"""
        try:
            # Detectar si hay archivos adjuntos en el mensaje
            tiene_archivos = "--- ARCHIVOS ADJUNTOS ---" in mensaje
            
            if tiene_archivos:
                # Extraer solo la pregunta del usuario (sin el contenido de archivos)
                pregunta_usuario = mensaje.split("--- ARCHIVOS ADJUNTOS ---")[0].strip()
                if not pregunta_usuario:
                    pregunta_usuario = "Analiza este archivo"
                
                # Para mensajes con archivos, usar un prompt especializado pero específico
                prompt = f"""Eres {self.nombre}, un chatbot especializado en análisis de documentos y archivos.

IMPORTANTE: Responde ÚNICAMENTE lo que el usuario solicita. No agregues información extra no solicitada.

El usuario solicita: "{pregunta_usuario}"

Basándote en su solicitud específica, puedes:
- Si pide un RESUMEN: Proporciona solo un resumen claro y conciso
- Si pide CASOS DE PRUEBA: Genera casos de prueba detallados
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
                prompt = f"""Eres {self.nombre}, un chatbot amigable y útil. 
                Responde de manera natural, conversacional y en español.
                
                Historial reciente de la conversación:
                {self.obtener_historial_reciente()}
                
                Usuario: {mensaje}
                
                Responde de manera útil y amigable:"""
            
            response = self.modelo_ia.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error con IA: {e}")
            return self.responder_localmente(mensaje)
    
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
    mi_chatbot = ChatBot("ChatBot Assistant")
    
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