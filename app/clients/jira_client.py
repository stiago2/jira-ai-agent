"""
Jira REST API Client.

Cliente para interactuar con Jira Cloud usando la REST API v3.
Soporta autenticación con email + API token y operaciones básicas de issues.
"""

import os
import base64
from typing import Dict, Any, List, Optional
import requests
from requests.exceptions import RequestException, Timeout, HTTPError


class JiraClient:
    """
    Cliente para Jira Cloud REST API v3.

    Autenticación usando Basic Auth con email y API token.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        email: Optional[str] = None,
        api_token: Optional[str] = None
    ):
        """
        Inicializa el cliente de Jira.

        Args:
            base_url: URL base de Jira (ej: https://company.atlassian.net)
            email: Email del usuario de Jira
            api_token: API token de Jira

        Si no se proporcionan, se leen desde variables de entorno:
            - JIRA_BASE_URL
            - JIRA_EMAIL
            - JIRA_API_TOKEN
        """
        # Leer desde variables de entorno si no se proporcionan
        self.base_url = (base_url or os.getenv("JIRA_BASE_URL", "")).rstrip("/")
        self.email = email or os.getenv("JIRA_EMAIL", "")
        self.api_token = api_token or os.getenv("JIRA_API_TOKEN", "")

        # Validar configuración requerida
        if not self.base_url:
            raise ValueError("JIRA_BASE_URL es requerido")
        if not self.email:
            raise ValueError("JIRA_EMAIL es requerido")
        if not self.api_token:
            raise ValueError("JIRA_API_TOKEN es requerido")

        # Crear headers de autenticación
        self.headers = self._create_auth_headers()

        # URL base de la API REST
        self.api_url = f"{self.base_url}/rest/api/3"

    def _create_auth_headers(self) -> Dict[str, str]:
        """
        Crea los headers de autenticación Basic Auth.

        Returns:
            Diccionario con headers de autenticación
        """
        # Codificar credenciales en Base64
        credentials = f"{self.email}:{self.api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Realiza una petición HTTP a la API de Jira.

        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint de la API (ej: /issue)
            data: Datos JSON para el body (opcional)
            params: Parámetros query string (opcional)
            timeout: Timeout en segundos (default: 30)

        Returns:
            Response JSON como diccionario

        Raises:
            JiraAPIError: Si la petición falla
        """
        url = f"{self.api_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
                timeout=timeout
            )

            # Lanzar excepción para códigos de error HTTP
            response.raise_for_status()

            # Retornar JSON si hay contenido
            if response.text:
                return response.json()
            return {}

        except Timeout:
            raise JiraAPIError(
                f"Timeout al conectar con Jira: {url}",
                status_code=None
            )
        except HTTPError as e:
            # Intentar extraer mensaje de error de Jira
            error_message = self._extract_error_message(e.response)
            raise JiraAPIError(
                f"Error HTTP {e.response.status_code}: {error_message}",
                status_code=e.response.status_code,
                response=e.response.json() if e.response.text else {}
            )
        except RequestException as e:
            raise JiraAPIError(f"Error de conexión con Jira: {str(e)}")

    def _extract_error_message(self, response: requests.Response) -> str:
        """
        Extrae el mensaje de error de una respuesta de Jira.

        Args:
            response: Response object de requests

        Returns:
            Mensaje de error legible
        """
        try:
            error_data = response.json()
            # Jira puede retornar errores en diferentes formatos
            if "errorMessages" in error_data and error_data["errorMessages"]:
                return "; ".join(error_data["errorMessages"])
            elif "errors" in error_data:
                return str(error_data["errors"])
            elif "message" in error_data:
                return error_data["message"]
        except Exception:
            pass

        return response.text or "Error desconocido"

    def create_issue(
        self,
        project_key: str,
        summary: str,
        description: Optional[str] = None,
        issue_type: str = "Task",
        priority: str = "Medium",
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crea un nuevo issue en Jira.

        Args:
            project_key: Clave del proyecto (ej: "PROJ")
            summary: Resumen del issue (máx 255 caracteres)
            description: Descripción detallada (opcional)
            issue_type: Tipo de issue (Task, Bug, Story, Epic) - default: Task
            priority: Prioridad (Highest, High, Medium, Low, Lowest) - default: Medium
            labels: Lista de etiquetas (opcional)
            assignee: Account ID del asignado (opcional)

        Returns:
            Diccionario con información del issue creado:
            {
                "id": "10001",
                "key": "PROJ-123",
                "self": "https://company.atlassian.net/rest/api/3/issue/10001"
            }

        Raises:
            JiraAPIError: Si falla la creación del issue
            ValueError: Si los parámetros son inválidos
        """
        # Validar parámetros requeridos
        if not project_key:
            raise ValueError("project_key es requerido")
        if not summary:
            raise ValueError("summary es requerido")
        if len(summary) > 255:
            raise ValueError("summary no puede exceder 255 caracteres")

        # Construir payload del issue
        fields = {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "issuetype": {
                "name": issue_type
            },
            "priority": {
                "name": priority
            }
        }

        # Agregar descripción si se proporciona
        if description:
            # Jira Cloud usa Atlassian Document Format (ADF) para descripciones
            fields["description"] = self._create_adf_content(description)

        # Agregar labels si se proporcionan
        if labels:
            fields["labels"] = labels

        # Agregar asignado si se proporciona
        if assignee:
            fields["assignee"] = {"id": assignee}

        # Crear el payload completo
        payload = {"fields": fields}

        # Hacer la petición POST
        response = self._make_request(
            method="POST",
            endpoint="/issue",
            data=payload
        )

        return response

    def _create_adf_content(self, text: str) -> Dict[str, Any]:
        """
        Convierte texto plano a formato ADF (Atlassian Document Format).

        Args:
            text: Texto plano

        Returns:
            Contenido en formato ADF
        """
        # Dividir por párrafos (doble salto de línea)
        paragraphs = text.split("\n\n")

        content = []
        for paragraph in paragraphs:
            if paragraph.strip():
                content.append({
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": paragraph.strip()
                        }
                    ]
                })

        return {
            "type": "doc",
            "version": 1,
            "content": content if content else [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        }

    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """
        Obtiene información de un issue por su key.

        Args:
            issue_key: Key del issue (ej: "PROJ-123")

        Returns:
            Diccionario con información completa del issue

        Raises:
            JiraAPIError: Si el issue no existe o hay error
        """
        return self._make_request(
            method="GET",
            endpoint=f"/issue/{issue_key}"
        )

    def get_project(self, project_key: str) -> Dict[str, Any]:
        """
        Obtiene información de un proyecto.

        Args:
            project_key: Clave del proyecto (ej: "PROJ")

        Returns:
            Diccionario con información del proyecto

        Raises:
            JiraAPIError: Si el proyecto no existe o hay error
        """
        return self._make_request(
            method="GET",
            endpoint=f"/project/{project_key}"
        )

    def search_user(self, query: str, project_key: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Busca usuarios en Jira por nombre o email.

        Args:
            query: Nombre o email del usuario a buscar
            project_key: Clave del proyecto para filtrar usuarios (opcional)

        Returns:
            Lista de usuarios que coinciden con la búsqueda

        Raises:
            JiraAPIError: Si hay error en la búsqueda
        """
        params = {"query": query}
        if project_key:
            params["project"] = project_key

        return self._make_request(
            method="GET",
            endpoint="/user/search",
            params=params
        )

    def get_user_account_id(self, name: str, project_key: Optional[str] = None) -> Optional[str]:
        """
        Obtiene el Account ID de un usuario por su nombre.

        Args:
            name: Nombre del usuario (ej: "Juan", "María")
            project_key: Clave del proyecto para filtrar búsqueda (opcional)

        Returns:
            Account ID del usuario o None si no se encuentra

        Example:
            >>> client.get_user_account_id("Juan", "KAN")
            "5b10a2844c20165700ede21g"
        """
        try:
            users = self.search_user(name, project_key)

            if users and len(users) > 0:
                # Retornar el Account ID del primer match
                return users[0].get("accountId")

            return None

        except JiraAPIError:
            # Si hay error en la búsqueda, retornar None
            return None

    def get_current_user(self) -> Dict[str, Any]:
        """
        Obtiene información del usuario autenticado.

        Returns:
            Diccionario con información del usuario

        Raises:
            JiraAPIError: Si hay error de autenticación
        """
        return self._make_request(
            method="GET",
            endpoint="/myself"
        )

    def test_connection(self) -> bool:
        """
        Verifica si la conexión con Jira es exitosa.

        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            self.get_current_user()
            return True
        except JiraAPIError:
            return False


class JiraAPIError(Exception):
    """
    Excepción personalizada para errores de la API de Jira.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None
    ):
        """
        Inicializa la excepción.

        Args:
            message: Mensaje de error
            status_code: Código de estado HTTP (opcional)
            response: Response JSON de Jira (opcional)
        """
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Representación en string del error."""
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


# Ejemplo de uso
if __name__ == "__main__":
    """
    Ejemplo de uso del cliente de Jira.

    Asegúrate de configurar las variables de entorno:
    export JIRA_BASE_URL="https://tu-empresa.atlassian.net"
    export JIRA_EMAIL="tu-email@empresa.com"
    export JIRA_API_TOKEN="tu-api-token"
    """

    try:
        # Crear cliente
        client = JiraClient()

        # Verificar conexión
        print("Verificando conexión con Jira...")
        if client.test_connection():
            print("✓ Conexión exitosa")

            # Obtener usuario actual
            user = client.get_current_user()
            print(f"✓ Usuario: {user.get('displayName')}")

            # Crear un issue de ejemplo
            print("\nCreando issue de prueba...")
            issue = client.create_issue(
                project_key="PROJ",
                summary="Issue de prueba creado desde Python",
                description="Esta es una descripción de prueba.\n\nCon múltiples párrafos.",
                issue_type="Task",
                priority="Medium",
                labels=["python", "api-test"]
            )

            print(f"✓ Issue creado: {issue['key']}")
            print(f"  URL: {issue['self']}")

        else:
            print("✗ Error al conectar con Jira")

    except ValueError as e:
        print(f"✗ Error de configuración: {e}")
    except JiraAPIError as e:
        print(f"✗ Error de Jira API: {e}")
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
