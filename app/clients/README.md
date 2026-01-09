# Jira Client

Cliente Python para interactuar con Jira Cloud REST API v3.

## Características

- ✅ Autenticación con email + API token (Basic Auth)
- ✅ Lectura de credenciales desde variables de entorno
- ✅ Creación de issues con múltiples campos
- ✅ Soporte para formato ADF (Atlassian Document Format)
- ✅ Manejo de errores HTTP detallado
- ✅ Métodos para obtener proyectos, issues y usuario actual
- ✅ Validación de conexión
- ✅ Código limpio y bien comentado

## Instalación

```bash
pip install requests
```

## Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
JIRA_BASE_URL=https://tu-empresa.atlassian.net
JIRA_EMAIL=tu-email@empresa.com
JIRA_API_TOKEN=tu_api_token_aqui
```

### Obtener API Token

1. Ve a: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click en "Create API token"
3. Dale un nombre y copia el token

## Uso Básico

### Crear el Cliente

```python
from app.clients.jira_client import JiraClient, JiraAPIError

# Opción 1: Leer desde variables de entorno
client = JiraClient()

# Opción 2: Pasar credenciales directamente
client = JiraClient(
    base_url="https://tu-empresa.atlassian.net",
    email="tu-email@empresa.com",
    api_token="tu-api-token"
)
```

### Verificar Conexión

```python
if client.test_connection():
    print("✓ Conexión exitosa")
else:
    print("✗ Error de conexión")
```

### Crear un Issue

```python
try:
    issue = client.create_issue(
        project_key="PROJ",
        summary="Implementar nueva funcionalidad",
        description="Descripción detallada del issue",
        issue_type="Task",           # Task, Bug, Story, Epic
        priority="High",              # Highest, High, Medium, Low, Lowest
        labels=["backend", "api"]    # Opcional
    )

    print(f"Issue creado: {issue['key']}")
    print(f"URL: {client.base_url}/browse/{issue['key']}")

except JiraAPIError as e:
    print(f"Error: {e}")
```

### Obtener Información de un Issue

```python
issue = client.get_issue("PROJ-123")
print(f"Summary: {issue['fields']['summary']}")
print(f"Status: {issue['fields']['status']['name']}")
```

### Obtener Información de un Proyecto

```python
project = client.get_project("PROJ")
print(f"Nombre: {project['name']}")
print(f"Key: {project['key']}")
```

### Obtener Usuario Actual

```python
user = client.get_current_user()
print(f"Usuario: {user['displayName']}")
print(f"Email: {user['emailAddress']}")
```

## Campos Soportados para Crear Issues

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `project_key` | `str` | ✅ | Clave del proyecto (ej: "PROJ") |
| `summary` | `str` | ✅ | Título del issue (máx 255 chars) |
| `description` | `str` | ❌ | Descripción en formato ADF |
| `issue_type` | `str` | ❌ | Task, Bug, Story, Epic (default: Task) |
| `priority` | `str` | ❌ | Highest, High, Medium, Low, Lowest (default: Medium) |
| `labels` | `List[str]` | ❌ | Lista de etiquetas |
| `assignee` | `str` | ❌ | Account ID del asignado |

## Manejo de Errores

El cliente lanza `JiraAPIError` para todos los errores de la API:

```python
try:
    issue = client.create_issue(...)
except JiraAPIError as e:
    print(f"Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Response: {e.response}")
```

### Códigos de Error Comunes

- **401**: Credenciales inválidas
- **403**: Sin permisos
- **404**: Recurso no encontrado
- **400**: Datos inválidos

## Ejemplo Completo

```python
from app.clients.jira_client import JiraClient, JiraAPIError

def main():
    try:
        # Crear cliente
        client = JiraClient()

        # Verificar conexión
        if not client.test_connection():
            print("No se pudo conectar con Jira")
            return

        # Obtener usuario actual
        user = client.get_current_user()
        print(f"Conectado como: {user['displayName']}")

        # Crear issue
        issue = client.create_issue(
            project_key="PROJ",
            summary="Nuevo issue desde Python",
            description="Descripción detallada",
            issue_type="Task",
            priority="Medium",
            labels=["python", "automation"]
        )

        print(f"✓ Issue creado: {issue['key']}")

    except ValueError as e:
        print(f"Error de configuración: {e}")
    except JiraAPIError as e:
        print(f"Error de Jira: {e}")

if __name__ == "__main__":
    main()
```

## Script de Prueba

Ejecuta el script de ejemplo:

```bash
python examples/test_jira_client.py
```

## Formato ADF (Atlassian Document Format)

El cliente convierte automáticamente texto plano a formato ADF para las descripciones:

```python
# Texto con múltiples párrafos
description = """
Este es el primer párrafo.

Este es el segundo párrafo.
"""

# Se convierte automáticamente a:
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Este es el primer párrafo."}]
    },
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Este es el segundo párrafo."}]
    }
  ]
}
```

## Notas Importantes

1. **API Token vs Password**: Usa API token, no tu contraseña de Jira
2. **Base URL**: Debe ser la URL completa sin trailing slash
3. **Project Key**: Debe existir y tener los permisos correctos
4. **Issue Types**: Deben existir en tu proyecto Jira
5. **Timeout**: Por defecto 30 segundos, configurable

## Limitaciones

- Solo soporta Jira Cloud (no Jira Server/Data Center)
- Solo crea issues básicos (no soporta todos los campos custom)
- No soporta attachments
- No soporta transiciones de workflow

## Extensión

Para agregar más funcionalidades, extiende la clase:

```python
class ExtendedJiraClient(JiraClient):
    def update_issue(self, issue_key: str, fields: dict):
        return self._make_request(
            method="PUT",
            endpoint=f"/issue/{issue_key}",
            data={"fields": fields}
        )
```

## Referencias

- [Jira Cloud REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
- [API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
