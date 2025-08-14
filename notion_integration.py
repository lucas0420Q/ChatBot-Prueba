"""
Integración con Notion para casos de prueba
"""
import requests
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class NotionIntegration:
    """Clase para integrar casos de prueba con Notion"""
    
    def __init__(self, token: str = None, database_id: str = None):
        """
        Inicializar integración con Notion
        
        Args:
            token: Token de integración de Notion
            database_id: ID de la base de datos de casos de prueba
        """
        self.token = token
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}" if token else "",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
    def verificar_conexion(self) -> Dict[str, Any]:
        """
        Verificar conexión con Notion
        
        Returns:
            Diccionario con el resultado de la verificación
        """
        if not self.token:
            return {
                "status": "error",
                "message": "Token de Notion no configurado"
            }
            
        try:
            response = requests.get(
                f"{self.base_url}/users/me",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Conexión exitosa con Notion",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Error de conexión: {response.status_code}",
                    "details": response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Error de conexión: {str(e)}"
            }
    
    def crear_caso_prueba(self, caso: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un caso de prueba en Notion
        
        Args:
            caso: Diccionario con los datos del caso de prueba
            
        Returns:
            Resultado de la operación
        """
        if not self.database_id:
            return {
                "status": "error",
                "message": "Database ID de Notion no configurado"
            }
            
        # Estructura de página para Notion
        page_data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Título": {
                    "title": [
                        {
                            "text": {
                                "content": caso.get("titulo", "Caso de prueba sin título")
                            }
                        }
                    ]
                },
                "ID": {
                    "rich_text": [
                        {
                            "text": {
                                "content": caso.get("id", "CP-000")
                            }
                        }
                    ]
                },
                "Objetivo": {
                    "rich_text": [
                        {
                            "text": {
                                "content": caso.get("objetivo", "")
                            }
                        }
                    ]
                },
                "Prioridad": {
                    "select": {
                        "name": caso.get("prioridad", "Media")
                    }
                },
                "Estado": {
                    "select": {
                        "name": caso.get("estado", "Pendiente")
                    }
                },
                "Categoría": {
                    "select": {
                        "name": caso.get("categoria", "Funcional")
                    }
                },
                "Fecha de creación": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            },
            "children": self._crear_contenido_caso(caso)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/pages",
                headers=self.headers,
                json=page_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Caso de prueba creado en Notion",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Error al crear caso: {response.status_code}",
                    "details": response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Error de red: {str(e)}"
            }
    
    def _crear_contenido_caso(self, caso: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Crear el contenido del bloque para el caso de prueba
        
        Args:
            caso: Datos del caso de prueba
            
        Returns:
            Lista de bloques para el contenido
        """
        contenido = []
        
        # Prerrequisitos
        if caso.get("prerrequisitos"):
            contenido.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📋 Prerrequisitos"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": caso["prerrequisitos"]}}]
                    }
                }
            ])
        
        # Pasos de ejecución
        if caso.get("pasos"):
            contenido.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🔧 Pasos de ejecución"}}]
                }
            })
            
            for i, paso in enumerate(caso["pasos"], 1):
                contenido.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": paso}}]
                    }
                })
        
        # Resultado esperado
        if caso.get("resultado_esperado"):
            contenido.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "✅ Resultado esperado"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": caso["resultado_esperado"]}}]
                    }
                }
            ])
        
        # Datos de prueba
        if caso.get("datos_prueba"):
            contenido.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📊 Datos de prueba"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": caso["datos_prueba"]}}]
                    }
                }
            ])
        
        # Criterios de aceptación
        if caso.get("criterios_aceptacion"):
            contenido.extend([
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "🎯 Criterios de aceptación"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": caso["criterios_aceptacion"]}}]
                    }
                }
            ])
        
        return contenido
    
    def crear_multiples_casos(self, casos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Crear múltiples casos de prueba en Notion
        
        Args:
            casos: Lista de casos de prueba
            
        Returns:
            Resultado de la operación con estadísticas
        """
        resultados = {
            "total": len(casos),
            "exitosos": 0,
            "fallidos": 0,
            "errores": []
        }
        
        for i, caso in enumerate(casos, 1):
            resultado = self.crear_caso_prueba(caso)
            
            if resultado["status"] == "success":
                resultados["exitosos"] += 1
            else:
                resultados["fallidos"] += 1
                resultados["errores"].append({
                    "caso": i,
                    "titulo": caso.get("titulo", f"Caso {i}"),
                    "error": resultado["message"]
                })
        
        return resultados
    
    def obtener_casos_prueba(self, filtros: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Obtener casos de prueba de la base de datos de Notion
        
        Args:
            filtros: Filtros opcionales para la consulta
            
        Returns:
            Lista de casos de prueba
        """
        if not self.database_id:
            return {
                "status": "error",
                "message": "Database ID de Notion no configurado"
            }
        
        query_data = {
            "page_size": 100
        }
        
        if filtros:
            query_data["filter"] = filtros
        
        try:
            response = requests.post(
                f"{self.base_url}/databases/{self.database_id}/query",
                headers=self.headers,
                json=query_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Casos obtenidos exitosamente",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Error al obtener casos: {response.status_code}",
                    "details": response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Error de red: {str(e)}"
            }
    
    def generar_template_caso(self) -> Dict[str, Any]:
        """
        Generar un template de caso de prueba
        
        Returns:
            Template de caso de prueba
        """
        return {
            "id": "CP-001",
            "titulo": "Verificar login con credenciales válidas",
            "objetivo": "Validar que el usuario pueda autenticarse correctamente",
            "prerrequisitos": "Usuario registrado en el sistema",
            "pasos": [
                "Navegar a la página de login",
                "Introducir email válido",
                "Introducir contraseña válida",
                "Hacer clic en 'Iniciar Sesión'"
            ],
            "resultado_esperado": "El usuario es redirigido al dashboard principal",
            "datos_prueba": "Email: test@ejemplo.com, Password: Test123!",
            "criterios_aceptacion": "Login exitoso y redirección correcta",
            "prioridad": "Alta",
            "estado": "Pendiente",
            "categoria": "Funcional"
        }

class NotionConfigManager:
    """Gestor de configuración para Notion"""
    
    def __init__(self, config_file: str = "notion_config.json"):
        self.config_file = config_file
        self.config = self.cargar_configuracion()
    
    def cargar_configuracion(self) -> Dict[str, str]:
        """Cargar configuración desde archivo"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "database_id": "",
                "workspace_name": "",
                "configurado": False
            }
        except json.JSONDecodeError:
            return {
                "database_id": "",
                "workspace_name": "",
                "configurado": False
            }
    
    def guardar_configuracion(self, token: str, database_id: str) -> bool:
        """Guardar configuración en archivo"""
        try:
            # Solo guardamos database_id ahora, token no es necesario
            nueva_config = {
                "database_id": database_id,
                "workspace_name": "",
                "configurado": True
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(nueva_config, f, indent=2, ensure_ascii=False)
            self.config = nueva_config
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    def obtener_token(self) -> str:
        """Obtener token de configuración"""
        return self.config.get("token", "")
    
    def obtener_database_id(self) -> str:
        """Obtener database ID de configuración"""
        return self.config.get("database_id", "")
    
    def configurar_notion(self, token: str, database_id: str, workspace_name: str = "") -> bool:
        """
        Configurar credenciales de Notion
        
        Args:
            token: Token de integración
            database_id: ID de la base de datos
            workspace_name: Nombre del workspace (opcional)
            
        Returns:
            True si se guardó correctamente
        """
        nueva_config = {
            "token": token,
            "database_id": database_id,
            "workspace_name": workspace_name
        }
        
        return self.guardar_configuracion(nueva_config)
    
    def esta_configurado(self) -> bool:
        """Verificar si Notion está configurado"""
        return bool(self.config.get("database_id") and self.config.get("configurado"))
    
    def limpiar_configuracion(self) -> bool:
        """
        Limpiar completamente la configuración de Notion
        
        Returns:
            True si se limpió correctamente
        """
        try:
            import os
            
            # Resetear configuración en memoria
            self.config = {
                "database_id": "",
                "workspace_name": "",
                "configurado": False
            }
            
            # Eliminar archivo de configuración si existe
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
                
            return True
        except Exception as e:
            print(f"Error al limpiar configuración: {e}")
            return False
