import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
import os
from datetime import datetime
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

class ChatBotGUI:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("🤖 ChatBot Assistant - Interfaz Visual")
        self.ventana.geometry("800x600")
        
        # Configurar modo tema (True = oscuro, False = claro)
        self.modo_oscuro = False
        
        self.ventana.configure(bg='#f0f0f0')
        
        # Configurar el icono y estilo
        self.configurar_estilo()
        
        # Inicializar el chatbot
        self.chatbot = ChatBot("ChatBot Assistant")
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Mensaje de bienvenida
        self.mostrar_mensaje_bot("¡Hola! Soy ChatBot Assistant. ¿En qué puedo ayudarte hoy? 😊")
        
        # Configurar evento de cierre
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
    
    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Definir temas
        self.temas = {
            'claro': {
                'fondo_principal': '#f8f9fa',
                'fondo_ventana': '#ffffff',
                'fondo_chat': '#ffffff',
                'fondo_entry': '#ffffff',
                'fondo_frame': '#f8f9fa',
                'texto_principal': '#212529',
                'texto_secundario': '#6c757d',
                'usuario': '#ffffff',
                'bot': '#ffffff',
                'texto_usuario': '#212529',
                'texto_bot': '#212529',
                'borde': '#dee2e6',
                'boton_bg': '#e9ecef',
                'boton_fg': '#495057',
                'tree_bg': '#ffffff',
                'tree_fg': '#212529',
                'tree_select': '#e3f2fd'
            },
            'oscuro': {
                'fondo_principal': '#121212',
                'fondo_ventana': '#1e1e1e',
                'fondo_chat': '#2d2d2d',
                'fondo_entry': '#404040',
                'fondo_frame': '#1e1e1e',
                'texto_principal': '#ffffff',
                'texto_secundario': '#b0b0b0',
                'usuario': '#2d2d2d',
                'bot': '#2d2d2d',
                'texto_usuario': '#ffffff',
                'texto_bot': '#ffffff',
                'borde': '#404040',
                'boton_bg': '#404040',
                'boton_fg': '#ffffff',
                'tree_bg': '#2d2d2d',
                'tree_fg': '#ffffff',
                'tree_select': '#404040'
            }
        }
        
        self.aplicar_tema()
    
    def aplicar_tema(self):
        """Aplica el tema actual a todos los componentes"""
        tema_actual = 'oscuro' if self.modo_oscuro else 'claro'
        colores = self.temas[tema_actual]
        
        # Configurar ventana principal
        self.ventana.configure(bg=colores['fondo_principal'])
        
        # Configurar estilos TTK
        self.style.configure('TFrame', 
                           background=colores['fondo_frame'],
                           bordercolor=colores['borde'])
        
        self.style.configure('TLabel', 
                           background=colores['fondo_frame'], 
                           foreground=colores['texto_principal'],
                           font=('Segoe UI', 9))
        
        self.style.configure('TButton', 
                           background=colores['boton_bg'], 
                           foreground=colores['boton_fg'],
                           borderwidth=1,
                           focuscolor='none',
                           font=('Segoe UI', 9))
        
        self.style.map('TButton',
                      background=[('active', colores['borde']),
                                ('pressed', colores['texto_secundario'])])
        
        self.style.configure('TLabelFrame', 
                           background=colores['fondo_frame'], 
                           foreground=colores['texto_principal'],
                           bordercolor=colores['borde'])
        
        self.style.configure('TLabelFrame.Label', 
                           background=colores['fondo_frame'], 
                           foreground=colores['texto_principal'],
                           font=('Segoe UI', 10, 'bold'))
        
        self.style.configure('TEntry',
                           fieldbackground=colores['fondo_entry'],
                           foreground=colores['texto_principal'],
                           bordercolor=colores['borde'],
                           lightcolor=colores['borde'],
                           darkcolor=colores['borde'],
                           font=('Segoe UI', 10))
        
        # Configurar Treeview
        self.style.configure('Treeview',
                           background=colores['tree_bg'],
                           foreground=colores['tree_fg'],
                           fieldbackground=colores['tree_bg'],
                           borderwidth=0,
                           font=('Segoe UI', 9))
        
        self.style.configure('Treeview.Heading',
                           background=colores['boton_bg'],
                           foreground=colores['texto_principal'],
                           font=('Segoe UI', 9, 'bold'))
        
        self.style.map('Treeview',
                      background=[('selected', colores['tree_select'])])
        
        # Guardar colores actuales para componentes personalizados
        self.colores = colores
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        # Frame principal
        frame_principal = ttk.Frame(self.ventana, padding="10")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar peso de filas y columnas
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.rowconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(
            frame_principal, 
            text="🤖 ChatBot Assistant", 
            font=('Segoe UI', 18, 'bold')
        )
        titulo.grid(row=0, column=0, pady=(0, 15))
        
        # Área de chat
        self.crear_area_chat(frame_principal)
        
        # Área de entrada
        self.crear_area_entrada(frame_principal)
        
        # Área de archivos adjuntos
        self.crear_area_adjuntos(frame_principal)
        
        # Botones adicionales
        self.crear_botones(frame_principal)
        
        # Status bar
        self.crear_status_bar(frame_principal)
    
    def crear_area_chat(self, parent):
        """Crea el área donde se muestran los mensajes"""
        # Frame para el chat
        frame_chat = ttk.LabelFrame(parent, text="💬 Conversación", padding="5")
        frame_chat.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        frame_chat.columnconfigure(0, weight=1)
        frame_chat.rowconfigure(0, weight=1)
        
        # Área de texto con scroll
        self.area_chat = scrolledtext.ScrolledText(
            frame_chat,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Segoe UI', 10),
            bg=self.colores['fondo_chat'],
            fg=self.colores['texto_principal'],
            relief=tk.FLAT,
            borderwidth=1,
            insertbackground=self.colores['texto_principal'],
            selectbackground=self.colores['borde']
        )
        self.area_chat.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.configurar_tags_chat()
    
    def configurar_tags_chat(self):
        """Configura los tags de colores para el chat"""
        # Configurar tags para estilos de mensajes
        self.area_chat.tag_configure(
            "usuario",
            foreground=self.colores['texto_usuario'],
            font=('Segoe UI', 10, 'bold'),
            lmargin1=10,
            lmargin2=10,
            rmargin=10,
            spacing1=2,
            spacing3=2,
            justify='left'
        )
        
        self.area_chat.tag_configure(
            "bot",
            foreground=self.colores['texto_bot'],
            font=('Segoe UI', 10),
            lmargin1=10,
            lmargin2=10,
            rmargin=10,
            spacing1=2,
            spacing3=2,
            justify='left'
        )
        
        self.area_chat.tag_configure(
            "timestamp", 
            foreground=self.colores['texto_secundario'], 
            font=('Segoe UI', 8),
            justify='left'
        )
    
    def crear_area_entrada(self, parent):
        """Crea el área donde el usuario escribe mensajes"""
        frame_entrada = ttk.Frame(parent)
        frame_entrada.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_entrada.columnconfigure(0, weight=1)
        
        # Entry para escribir mensajes
        self.entrada_texto = ttk.Entry(
            frame_entrada,
            font=('Segoe UI', 11),
            width=50
        )
        self.entrada_texto.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Botón adjuntar archivos
        self.boton_adjuntar = ttk.Button(
            frame_entrada,
            text="📎 Adjuntar",
            command=self.adjuntar_archivo
        )
        self.boton_adjuntar.grid(row=0, column=1, padx=(0, 10))
        
        # Botón enviar
        self.boton_enviar = ttk.Button(
            frame_entrada,
            text="📤 Enviar",
            command=self.enviar_mensaje,
            style='Accent.TButton'
        )
        self.boton_enviar.grid(row=0, column=2)
        
        # Bind Enter key
        self.entrada_texto.bind('<Return>', lambda event: self.enviar_mensaje())
        self.entrada_texto.focus()
    
    def crear_area_adjuntos(self, parent):
        """Crea el área para mostrar archivos adjuntos"""
        self.frame_adjuntos = ttk.LabelFrame(parent, text="📎 Archivos Adjuntos", padding="5")
        self.frame_adjuntos.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.frame_adjuntos.columnconfigure(0, weight=1)
        
        # Lista para mostrar archivos adjuntos
        self.lista_adjuntos = tk.Listbox(
            self.frame_adjuntos,
            height=3,
            font=('Segoe UI', 9),
            bg=self.colores['fondo_chat'],
            fg=self.colores['texto_principal'],
            selectbackground=self.colores['borde']
        )
        self.lista_adjuntos.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Frame para botones de adjuntos
        frame_botones_adj = ttk.Frame(self.frame_adjuntos)
        frame_botones_adj.grid(row=0, column=1, sticky=(tk.N))
        
        # Botón quitar archivo
        self.boton_quitar = ttk.Button(
            frame_botones_adj,
            text="🗑️ Quitar",
            command=self.quitar_archivo_adjunto
        )
        self.boton_quitar.pack(pady=(0, 5))
        
        # Botón limpiar todos
        self.boton_limpiar_adj = ttk.Button(
            frame_botones_adj,
            text="🧹 Limpiar",
            command=self.limpiar_adjuntos
        )
        self.boton_limpiar_adj.pack()
        
        # Lista para almacenar rutas de archivos
        self.archivos_adjuntos = []
        
        # Ocultar el frame inicialmente
        self.frame_adjuntos.grid_remove()
    
    def crear_botones(self, parent):
        """Crea botones adicionales"""
        frame_botones = ttk.Frame(parent)
        frame_botones.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botón limpiar chat
        boton_limpiar = ttk.Button(
            frame_botones,
            text="🗑️ Limpiar Chat",
            command=self.limpiar_chat
        )
        boton_limpiar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón ver historial
        boton_historial = ttk.Button(
            frame_botones,
            text="📂 Ver Historial",
            command=self.abrir_ventana_historial
        )
        boton_historial.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón guardar conversación
        boton_guardar = ttk.Button(
            frame_botones,
            text="💾 Guardar",
            command=self.guardar_conversacion_actual
        )
        boton_guardar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón ayuda
        boton_ayuda = ttk.Button(
            frame_botones,
            text="❓ Ayuda",
            command=self.mostrar_ayuda
        )
        boton_ayuda.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón cambiar tema
        self.boton_tema = ttk.Button(
            frame_botones,
            text="🌙 Modo Oscuro" if not self.modo_oscuro else "☀️ Modo Claro",
            command=self.cambiar_tema
        )
        self.boton_tema.pack(side=tk.LEFT, padx=(0, 10))
        
        # Indicador de estado IA
        self.label_ia = ttk.Label(
            frame_botones,
            text="✅ IA Conectada" if self.chatbot.usar_ia else "⚠️ Solo Local",
            foreground="green" if self.chatbot.usar_ia else "orange"
        )
        self.label_ia.pack(side=tk.RIGHT)
    
    def crear_status_bar(self, parent):
        """Crea la barra de estado"""
        self.status_var = tk.StringVar()
        self.status_var.set("Listo para conversar")
        
        status_bar = ttk.Label(
            parent,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=('Segoe UI', 9)
        )
        status_bar.grid(row=5, column=0, sticky=(tk.W, tk.E))
    
    def cambiar_tema(self):
        """Cambia entre modo claro y oscuro"""
        self.modo_oscuro = not self.modo_oscuro
        
        # Actualizar texto del botón
        self.boton_tema.configure(
            text="☀️ Modo Claro" if self.modo_oscuro else "🌙 Modo Oscuro"
        )
        
        # Aplicar nuevo tema
        self.aplicar_tema()
        
        # Actualizar área de chat
        self.area_chat.configure(
            bg=self.colores['fondo_chat'],
            fg=self.colores['texto_principal'],
            insertbackground=self.colores['texto_principal'],
            selectbackground=self.colores['borde']
        )
        
        # Reconfigurar tags
        self.configurar_tags_chat()
        
        # Actualizar colores del área de adjuntos
        self.actualizar_colores_adjuntos()
        
        # Actualizar status
        tema_nombre = "Oscuro" if self.modo_oscuro else "Claro"
        self.status_var.set(f"✨ Tema {tema_nombre} aplicado")
    
    def adjuntar_archivo(self):
        """Permite adjuntar archivos o imágenes"""
        tipos_archivo = [
            ("Todos los archivos soportados", "*.txt;*.pdf;*.docx;*.doc;*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.json;*.xml;*.csv"),
            ("Documentos de texto", "*.txt;*.pdf;*.docx;*.doc"),
            ("Imágenes", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
            ("Datos", "*.json;*.xml;*.csv"),
            ("Todos los archivos", "*.*")
        ]
        
        archivos = filedialog.askopenfilenames(
            title="Seleccionar archivos para adjuntar",
            filetypes=tipos_archivo
        )
        
        if archivos:
            for archivo in archivos:
                if archivo not in self.archivos_adjuntos:
                    self.archivos_adjuntos.append(archivo)
                    nombre_archivo = os.path.basename(archivo)
                    
                    # Determinar el tipo de archivo
                    extension = os.path.splitext(archivo)[1].lower()
                    if extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                        icono = "🖼️"
                    elif extension in ['.pdf']:
                        icono = "📄"
                    elif extension in ['.docx', '.doc']:
                        icono = "📝"
                    elif extension in ['.txt']:
                        icono = "📄"
                    elif extension in ['.json', '.xml']:
                        icono = "📋"
                    elif extension in ['.csv']:
                        icono = "📊"
                    else:
                        icono = "📎"
                    
                    self.lista_adjuntos.insert(tk.END, f"{icono} {nombre_archivo}")
            
            # Mostrar el área de adjuntos si hay archivos
            if self.archivos_adjuntos:
                self.frame_adjuntos.grid()
                self.actualizar_colores_adjuntos()
            
            self.status_var.set(f"📎 {len(self.archivos_adjuntos)} archivo(s) adjunto(s)")
    
    def quitar_archivo_adjunto(self):
        """Quita el archivo seleccionado de la lista"""
        seleccion = self.lista_adjuntos.curselection()
        if seleccion:
            indice = seleccion[0]
            self.lista_adjuntos.delete(indice)
            del self.archivos_adjuntos[indice]
            
            if not self.archivos_adjuntos:
                self.frame_adjuntos.grid_remove()
                self.status_var.set("Listo para conversar")
            else:
                self.status_var.set(f"📎 {len(self.archivos_adjuntos)} archivo(s) adjunto(s)")
    
    def limpiar_adjuntos(self):
        """Limpia todos los archivos adjuntos"""
        self.archivos_adjuntos.clear()
        self.lista_adjuntos.delete(0, tk.END)
        self.frame_adjuntos.grid_remove()
        self.status_var.set("Listo para conversar")
    
    def actualizar_colores_adjuntos(self):
        """Actualiza los colores del área de adjuntos según el tema"""
        if hasattr(self, 'lista_adjuntos'):
            self.lista_adjuntos.configure(
                bg=self.colores['fondo_chat'],
                fg=self.colores['texto_principal'],
                selectbackground=self.colores['borde']
            )
    
    def procesar_archivos_adjuntos(self):
        """Procesa los archivos adjuntos y extrae su contenido"""
        contenido_archivos = []
        
        for archivo in self.archivos_adjuntos:
            try:
                nombre = os.path.basename(archivo)
                extension = os.path.splitext(archivo)[1].lower()
                
                if extension == '.txt':
                    with open(archivo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                    contenido_archivos.append(f"📄 Archivo: {nombre}\nContenido:\n{contenido}\n{'='*50}\n")
                
                elif extension == '.docx':
                    if DOCX_DISPONIBLE:
                        try:
                            doc = Document(archivo)
                            contenido = ""
                            for paragraph in doc.paragraphs:
                                if paragraph.text.strip():
                                    contenido += paragraph.text + "\n"
                            
                            # También extraer texto de tablas si las hay
                            for table in doc.tables:
                                for row in table.rows:
                                    for cell in row.cells:
                                        if cell.text.strip():
                                            contenido += cell.text + " | "
                                    contenido += "\n"
                            
                            if contenido.strip():
                                contenido_archivos.append(f"📝 Documento Word: {nombre}\nContenido:\n{contenido}\n{'='*50}\n")
                            else:
                                contenido_archivos.append(f"📝 Documento Word: {nombre}\n[El documento parece estar vacío o no contiene texto extraíble]\n{'='*50}\n")
                        except Exception as e:
                            contenido_archivos.append(f"❌ Error al leer documento Word {nombre}: {str(e)}\n{'='*50}\n")
                    else:
                        contenido_archivos.append(f"📝 Documento Word: {nombre}\n[No se puede leer - librería python-docx no disponible]\n{'='*50}\n")
                
                elif extension == '.doc':
                    # Para archivos .doc (formato antiguo), sugerir conversión
                    contenido_archivos.append(f"📝 Documento Word (formato antiguo): {nombre}\n[Por favor, convierte el archivo a formato .docx para poder leerlo, o copia y pega el contenido directamente]\n{'='*50}\n")
                
                elif extension == '.pdf':
                    if PDF_DISPONIBLE:
                        try:
                            contenido = self.extraer_texto_pdf(archivo)
                            if contenido.strip():
                                contenido_archivos.append(f"📄 Archivo PDF: {nombre}\nContenido:\n{contenido}\n{'='*50}\n")
                            else:
                                contenido_archivos.append(f"📄 Archivo PDF: {nombre}\n[No se pudo extraer texto del PDF o está vacío]\n{'='*50}\n")
                        except Exception as e:
                            contenido_archivos.append(f"❌ Error al leer PDF {nombre}: {str(e)}\n{'='*50}\n")
                    else:
                        contenido_archivos.append(f"📄 Archivo PDF: {nombre}\n[No se puede leer - librería PyPDF2 no disponible]\n{'='*50}\n")
                
                elif extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                    # Para imágenes, solo indicamos que están adjuntas
                    contenido_archivos.append(f"🖼️ Imagen adjunta: {nombre}\n[La imagen ha sido adjuntada para análisis]\n{'='*50}\n")
                
                elif extension == '.json':
                    with open(archivo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                    contenido_archivos.append(f"📋 Archivo JSON: {nombre}\nContenido:\n{contenido}\n{'='*50}\n")
                
                elif extension == '.csv':
                    with open(archivo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                    contenido_archivos.append(f"📊 Archivo CSV: {nombre}\nContenido:\n{contenido}\n{'='*50}\n")
                
                else:
                    # Para otros tipos de archivo, intentar leer como texto
                    try:
                        with open(archivo, 'r', encoding='utf-8') as f:
                            contenido = f.read()
                        contenido_archivos.append(f"📎 Archivo: {nombre}\nContenido:\n{contenido}\n{'='*50}\n")
                    except:
                        contenido_archivos.append(f"📎 Archivo: {nombre}\n[Archivo binario - no se puede mostrar el contenido]\n{'='*50}\n")
                        
            except Exception as e:
                contenido_archivos.append(f"❌ Error al leer {nombre}: {str(e)}\n{'='*50}\n")
        
        return "\n".join(contenido_archivos)
    
    def extraer_texto_pdf(self, ruta_pdf):
        """Extrae texto de un archivo PDF"""
        if not PDF_DISPONIBLE or PyPDF2 is None:
            return "Error: Librería PyPDF2 no disponible"
        
        try:
            texto = ""
            with open(ruta_pdf, 'rb') as archivo:
                # Usar la sintaxis correcta según la versión de PyPDF2
                try:
                    # Intentar con PyPDF2 versión 3.x
                    lector = PyPDF2.PdfReader(archivo)
                    for pagina in lector.pages:
                        texto += pagina.extract_text() + "\n"
                except AttributeError:
                    # Fallback para versiones anteriores de PyPDF2
                    lector = PyPDF2.PdfFileReader(archivo)
                    for num_pagina in range(lector.numPages):
                        pagina = lector.getPage(num_pagina)
                        texto += pagina.extractText() + "\n"
            return texto
        except Exception as e:
            return f"Error al extraer texto del PDF: {str(e)}"
    
    def mostrar_mensaje(self, mensaje, tipo, timestamp=True):
        """Muestra un mensaje en el área de chat"""
        self.area_chat.configure(state=tk.NORMAL)
        
        if timestamp:
            tiempo = datetime.now().strftime("%H:%M:%S")
            self.area_chat.insert(tk.END, f"[{tiempo}] ", "timestamp")
        
        if tipo == "usuario":
            self.area_chat.insert(tk.END, f"Tú: {mensaje}\n", "usuario")
        else:
            self.area_chat.insert(tk.END, f"🤖 Bot: {mensaje}\n", "bot")
        
        self.area_chat.insert(tk.END, "\n")
        self.area_chat.configure(state=tk.DISABLED)
        self.area_chat.see(tk.END)
    
    def mostrar_mensaje_bot(self, mensaje):
        """Muestra un mensaje del bot"""
        self.mostrar_mensaje(mensaje, "bot")
    
    def mostrar_mensaje_usuario(self, mensaje):
        """Muestra un mensaje del usuario"""
        self.mostrar_mensaje(mensaje, "usuario")
    
    def enviar_mensaje(self):
        """Envía un mensaje al chatbot"""
        mensaje = self.entrada_texto.get().strip()
        
        # Verificar si hay mensaje o archivos adjuntos
        if not mensaje and not self.archivos_adjuntos:
            return
        
        # Si no hay mensaje pero sí archivos, crear mensaje automático
        if not mensaje and self.archivos_adjuntos:
            mensaje = "Por favor, analiza los archivos adjuntos."
        
        # Limpiar entrada
        self.entrada_texto.delete(0, tk.END)
        
        # Procesar archivos adjuntos si los hay
        contenido_adjuntos = ""
        if self.archivos_adjuntos:
            contenido_adjuntos = self.procesar_archivos_adjuntos()
            # Mostrar información de archivos adjuntos en el chat
            self.mostrar_mensaje_adjuntos()
        
        # Combinar mensaje con contenido de archivos
        mensaje_completo = mensaje
        if contenido_adjuntos:
            mensaje_completo += f"\n\n--- ARCHIVOS ADJUNTOS ---\n{contenido_adjuntos}"
        
        # Mostrar mensaje del usuario (solo el texto, no los archivos)
        self.mostrar_mensaje_usuario(mensaje)
        
        # Verificar si quiere salir
        if mensaje.lower() in ['salir', 'exit', 'quit']:
            self.cerrar_aplicacion()
            return
        
        # Deshabilitar botón mientras procesa
        self.boton_enviar.configure(state='disabled')
        self.boton_adjuntar.configure(state='disabled')
        self.status_var.set("🤔 Analizando archivos y generando respuesta...")
        
        # Procesar mensaje en hilo separado
        threading.Thread(
            target=self.procesar_mensaje_async,
            args=(mensaje_completo,),
            daemon=True
        ).start()
        
        # Limpiar archivos adjuntos después de enviar
        if self.archivos_adjuntos:
            self.limpiar_adjuntos()
    
    def mostrar_mensaje_adjuntos(self):
        """Muestra información sobre los archivos adjuntos en el chat"""
        if self.archivos_adjuntos:
            archivos_info = []
            for archivo in self.archivos_adjuntos:
                nombre = os.path.basename(archivo)
                extension = os.path.splitext(archivo)[1].lower()
                
                if extension in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                    icono = "🖼️"
                elif extension == '.pdf':
                    icono = "📄"
                elif extension in ['.docx', '.doc']:
                    icono = "📝"
                elif extension == '.txt':
                    icono = "📄"
                elif extension in ['.json', '.xml']:
                    icono = "📋"
                elif extension == '.csv':
                    icono = "📊"
                else:
                    icono = "📎"
                
                archivos_info.append(f"{icono} {nombre}")
            
            mensaje_adjuntos = f"📎 Archivos adjuntos: {', '.join(archivos_info)}"
            self.mostrar_mensaje(mensaje_adjuntos, "usuario", timestamp=False)
    
    def procesar_mensaje_async(self, mensaje):
        """Procesa el mensaje en un hilo separado"""
        try:
            respuesta = self.chatbot.procesar_mensaje(mensaje)
            
            # Actualizar UI en el hilo principal
            self.ventana.after(0, self.mostrar_respuesta, respuesta)
            
        except Exception as e:
            error_msg = f"Lo siento, ocurrió un error: {str(e)}"
            self.ventana.after(0, self.mostrar_respuesta, error_msg)
    
    def mostrar_respuesta(self, respuesta):
        """Muestra la respuesta del bot y reactiva controles"""
        self.mostrar_mensaje_bot(respuesta)
        self.boton_enviar.configure(state='normal')
        self.boton_adjuntar.configure(state='normal')
        self.status_var.set("Listo para conversar")
        self.entrada_texto.focus()
    
    def limpiar_chat(self):
        """Limpia el área de chat"""
        respuesta = messagebox.askyesno(
            "Limpiar Chat", 
            "¿Estás seguro de que quieres limpiar toda la conversación?"
        )
        if respuesta:
            self.area_chat.configure(state=tk.NORMAL)
            self.area_chat.delete(1.0, tk.END)
            self.area_chat.configure(state=tk.DISABLED)
            self.mostrar_mensaje_bot("Chat limpiado. ¡Empecemos de nuevo! 😊")
    
    def abrir_ventana_historial(self):
        """Abre la ventana del historial de conversaciones"""
        ventana_historial = tk.Toplevel(self.ventana)
        ventana_historial.title("📂 Historial de Conversaciones")
        ventana_historial.geometry("900x700")
        ventana_historial.configure(bg=self.colores['fondo_principal'])
        
        # Frame principal
        frame_principal = ttk.Frame(ventana_historial, padding="10")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            frame_principal, 
            text="📂 Historial de Conversaciones", 
            font=('Arial', 14, 'bold')
        )
        titulo.pack(pady=(0, 10))
        
        # Frame para lista y detalles
        frame_contenido = ttk.Frame(frame_principal)
        frame_contenido.pack(fill=tk.BOTH, expand=True)
        
        # Lista de sesiones (izquierda)
        frame_lista = ttk.LabelFrame(frame_contenido, text="📋 Sesiones", padding="5")
        frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Treeview para sesiones
        columnas = ('Fecha', 'Hora', 'Mensajes')
        tree_sesiones = ttk.Treeview(frame_lista, columns=columnas, show='headings', height=15)
        
        # Configurar columnas
        tree_sesiones.heading('Fecha', text='Fecha')
        tree_sesiones.heading('Hora', text='Hora')
        tree_sesiones.heading('Mensajes', text='Mensajes')
        
        tree_sesiones.column('Fecha', width=100)
        tree_sesiones.column('Hora', width=80)
        tree_sesiones.column('Mensajes', width=80)
        
        # Scrollbar para treeview
        scroll_tree = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=tree_sesiones.yview)
        tree_sesiones.configure(yscrollcommand=scroll_tree.set)
        
        tree_sesiones.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_tree.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Área de detalles (derecha)
        frame_detalles = ttk.LabelFrame(frame_contenido, text="💬 Conversación", padding="5")
        frame_detalles.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Área de texto para mostrar conversación
        area_conversacion = scrolledtext.ScrolledText(
            frame_detalles,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Segoe UI', 10),
            bg=self.colores['fondo_chat'],
            fg=self.colores['texto_principal'],
            insertbackground=self.colores['texto_principal']
        )
        area_conversacion.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para colores (adaptable a tema)
        area_conversacion.tag_configure("usuario", 
                                       foreground=self.colores['texto_usuario'], 
                                       font=('Segoe UI', 10, 'bold'),
                                       justify='left')
        area_conversacion.tag_configure("bot", 
                                       foreground=self.colores['texto_bot'], 
                                       font=('Segoe UI', 10),
                                       justify='left')
        area_conversacion.tag_configure("timestamp", 
                                       foreground=self.colores['texto_secundario'], 
                                       font=('Segoe UI', 8),
                                       justify='left')
        area_conversacion.tag_configure("ia_badge", 
                                       foreground=self.colores['texto_secundario'], 
                                       font=('Segoe UI', 8, 'italic'),
                                       justify='left')
        
        # Cargar sesiones
        self.cargar_sesiones_en_tree(tree_sesiones)
        
        # Evento de selección
        def on_select(event):
            selection = tree_sesiones.selection()
            if selection:
                item = tree_sesiones.item(selection[0])
                archivo = item['values'][3]  # Archivo guardado en valores ocultos
                self.mostrar_conversacion_en_area(archivo, area_conversacion)
        
        tree_sesiones.bind('<<TreeviewSelect>>', on_select)
        
        # Frame para botones
        frame_botones_hist = ttk.Frame(frame_principal)
        frame_botones_hist.pack(fill=tk.X, pady=(10, 0))
        
        # Botón actualizar
        btn_actualizar = ttk.Button(
            frame_botones_hist,
            text="🔄 Actualizar",
            command=lambda: self.cargar_sesiones_en_tree(tree_sesiones)
        )
        btn_actualizar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón exportar seleccionada
        btn_exportar_sel = ttk.Button(
            frame_botones_hist,
            text="💾 Exportar Seleccionada",
            command=lambda: self.exportar_sesion_seleccionada(tree_sesiones)
        )
        btn_exportar_sel.pack(side=tk.LEFT, padx=(0, 10))
        
        # Estadísticas
        stats = self.chatbot.obtener_estadisticas_historial()
        if stats:
            texto_stats = f"📊 Total: {stats['total_sesiones']} sesiones, {stats['total_conversaciones']} mensajes"
            label_stats = ttk.Label(frame_botones_hist, text=texto_stats)
            label_stats.pack(side=tk.RIGHT)
    
    def cargar_sesiones_en_tree(self, tree):
        """Carga las sesiones en el treeview"""
        # Limpiar tree
        for item in tree.get_children():
            tree.delete(item)
        
        # Cargar sesiones
        sesiones = self.chatbot.cargar_historial_sesiones()
        
        for sesion in sesiones:
            datos = sesion['datos']
            inicio = datetime.fromisoformat(datos['inicio'])
            fecha = inicio.strftime("%Y-%m-%d")
            hora = inicio.strftime("%H:%M:%S")
            mensajes = len(datos['conversaciones'])
            
            # Insertar en tree (guardamos el archivo en values[3] oculto)
            tree.insert('', tk.END, values=(fecha, hora, mensajes, sesion['archivo']))
    
    def mostrar_conversacion_en_area(self, archivo, area):
        """Muestra una conversación específica en el área de texto"""
        try:
            ruta_archivo = os.path.join(self.chatbot.directorio_historial, archivo)
            
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                sesion = json.load(f)
            
            area.configure(state=tk.NORMAL)
            area.delete(1.0, tk.END)
            
            # Información de la sesión
            inicio = datetime.fromisoformat(sesion['inicio'])
            area.insert(tk.END, f"📅 Sesión del {inicio.strftime('%Y-%m-%d %H:%M:%S')}\n", "timestamp")
            area.insert(tk.END, f"💬 Total de mensajes: {len(sesion['conversaciones'])}\n\n", "timestamp")
            
            # Mostrar conversaciones
            for i, conv in enumerate(sesion['conversaciones'], 1):
                timestamp = datetime.fromisoformat(conv['timestamp'])
                tiempo = timestamp.strftime("%H:%M:%S")
                
                # Badge de IA si fue respuesta de IA
                ia_badge = " [IA]" if conv.get('fue_ia', False) else " [Local]"
                
                area.insert(tk.END, f"[{tiempo}] ", "timestamp")
                area.insert(tk.END, f"Tú: {conv['usuario']}\n", "usuario")
                
                area.insert(tk.END, f"[{tiempo}] ", "timestamp")
                area.insert(tk.END, f"🤖 Bot{ia_badge}: {conv['bot']}\n\n", "bot")
            
            area.configure(state=tk.DISABLED)
            area.see(1.0)  # Ir al inicio
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la conversación: {e}")
    
    def exportar_sesion_seleccionada(self, tree):
        """Exporta la sesión seleccionada a un archivo de texto"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor selecciona una sesión para exportar.")
            return
        
        item = tree.item(selection[0])
        archivo = item['values'][3]
        
        try:
            ruta_archivo = os.path.join(self.chatbot.directorio_historial, archivo)
            
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                sesion = json.load(f)
            
            # Crear contenido de texto
            inicio = datetime.fromisoformat(sesion['inicio'])
            contenido = f"Conversación con ChatBot Assistant\n"
            contenido += f"Fecha: {inicio.strftime('%Y-%m-%d %H:%M:%S')}\n"
            contenido += f"Total de mensajes: {len(sesion['conversaciones'])}\n"
            contenido += "=" * 50 + "\n\n"
            
            for conv in sesion['conversaciones']:
                timestamp = datetime.fromisoformat(conv['timestamp'])
                tiempo = timestamp.strftime("%H:%M:%S")
                ia_badge = " [IA]" if conv.get('fue_ia', False) else " [Local]"
                
                contenido += f"[{tiempo}] Usuario: {conv['usuario']}\n"
                contenido += f"[{tiempo}] Bot{ia_badge}: {conv['bot']}\n\n"
            
            # Guardar archivo
            archivo_export = filedialog.asksaveasfilename(
                title="Guardar conversación",
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if archivo_export:
                with open(archivo_export, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                messagebox.showinfo("Éxito", "Conversación exportada exitosamente.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar la conversación: {e}")
    
    def guardar_conversacion_actual(self):
        """Guarda la conversación actual en el historial"""
        if len(self.chatbot.sesion_actual['conversaciones']) == 0:
            messagebox.showwarning("Advertencia", "No hay conversación actual para guardar.")
            return
        
        try:
            # Guardar la sesión actual en el historial
            archivo_guardado = self.chatbot.guardar_sesion_completa()
            
            if archivo_guardado:
                messagebox.showinfo(
                    "Éxito", 
                    f"Conversación guardada exitosamente en el historial.\n\nArchivo: {archivo_guardado}"
                )
                self.status_var.set("✅ Conversación guardada en historial")
            else:
                messagebox.showwarning("Advertencia", "No se pudo guardar la conversación.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la conversación: {e}")
    
    def exportar_conversacion_actual(self):
        """Exporta la conversación actual que se está viendo"""
        if len(self.chatbot.sesion_actual['conversaciones']) == 0:
            messagebox.showwarning("Advertencia", "No hay conversación actual para exportar.")
            return
        
        try:
            # Crear contenido de texto
            inicio = datetime.fromisoformat(self.chatbot.sesion_actual['inicio'])
            contenido = f"Conversación Actual con ChatBot Assistant\n"
            contenido += f"Fecha: {inicio.strftime('%Y-%m-%d %H:%M:%S')}\n"
            contenido += f"Total de mensajes: {len(self.chatbot.sesion_actual['conversaciones'])}\n"
            contenido += "=" * 50 + "\n\n"
            
            for conv in self.chatbot.sesion_actual['conversaciones']:
                timestamp = datetime.fromisoformat(conv['timestamp'])
                tiempo = timestamp.strftime("%H:%M:%S")
                ia_badge = " [IA]" if conv.get('fue_ia', False) else " [Local]"
                
                contenido += f"[{tiempo}] Usuario: {conv['usuario']}\n"
                contenido += f"[{tiempo}] Bot{ia_badge}: {conv['bot']}\n\n"
            
            # Guardar archivo
            archivo_export = filedialog.asksaveasfilename(
                title="Guardar conversación actual",
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if archivo_export:
                with open(archivo_export, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                messagebox.showinfo("Éxito", "Conversación actual exportada exitosamente.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar la conversación: {e}")
    
    def mostrar_ayuda(self):
        """Muestra información de ayuda"""
        ayuda_texto = """
🤖 ChatBot Assistant - Ayuda

• Escribe tu pregunta y presiona Enter o clic en 'Enviar'
• Puedo responder preguntas sobre cualquier tema
• Uso IA avanzada para darte respuestas inteligentes
• Escribe 'salir' para cerrar la aplicación

Funciones disponibles:
✨ Respuestas inteligentes con IA
💬 Conversación natural
🧠 Memoria de contexto
🔄 Respuestas de respaldo si falla la IA
📂 Historial completo de conversaciones
💾 Guardar conversaciones en historial
🌙/☀️ Modo oscuro y claro
🎨 Interfaz elegante y adaptable

📎 NUEVA FUNCIONALIDAD - Archivos Adjuntos:
• Adjunta documentos (.txt, .docx, .pdf)
• Adjunta imágenes (.png, .jpg, .jpeg, .gif, .bmp)
• Adjunta datos (.json, .xml, .csv)
• ✨ NUEVO: Lectura completa de archivos Word (.docx)
• Extracción automática de texto y tablas

🎯 SOLICITUDES ESPECÍFICAS:
• "Dame un resumen del documento" - Solo resumen
• "Genera casos de prueba" - Solo casos de prueba
• "Analiza el código" - Solo análisis de código
• "Revisa el documento" - Revisión general
• Sé específico en tu solicitud para mejores resultados

¡Pregúntame lo que quieras y adjunta archivos para análisis!
        """
        messagebox.showinfo("Ayuda - ChatBot Assistant", ayuda_texto)
    
    def cerrar_aplicacion(self):
        """Cierra la aplicación guardando la sesión"""
        try:
            # Guardar sesión actual si hay conversaciones
            if len(self.chatbot.sesion_actual['conversaciones']) > 0:
                archivo_guardado = self.chatbot.guardar_sesion_completa()
                if archivo_guardado:
                    print(f"✅ Sesión guardada en: {archivo_guardado}")
            
            self.ventana.quit()
        except Exception as e:
            print(f"Error al guardar sesión: {e}")
            self.ventana.quit()
    
    def ejecutar(self):
        """Inicia la aplicación"""
        try:
            self.ventana.mainloop()
        except KeyboardInterrupt:
            self.cerrar_aplicacion()

def main():
    """Función principal"""
    app = ChatBotGUI()
    app.ejecutar()

if __name__ == "__main__":
    main()
