"""
Ejemplo de uso del cliente de Jira.

Este script demuestra cómo usar JiraClient para interactuar con Jira Cloud.
"""

import sys
import os

# Agregar el directorio raíz al path para importar el módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.clients.jira_client import JiraClient, JiraAPIError


def main():
    """
    Función principal de ejemplo.
    """
    print("=" * 60)
    print("  Prueba del Cliente de Jira")
    print("=" * 60)
    print()

    try:
        # Crear cliente (lee credenciales de .env o variables de entorno)
        print("1. Inicializando cliente de Jira...")
        client = JiraClient()
        print(f"   ✓ Cliente creado para: {client.base_url}")
        print()

        # Verificar conexión
        print("2. Verificando conexión...")
        if client.test_connection():
            print("   ✓ Conexión exitosa con Jira")
        else:
            print("   ✗ No se pudo conectar con Jira")
            return
        print()

        # Obtener información del usuario actual
        print("3. Obteniendo información del usuario...")
        user = client.get_current_user()
        print(f"   ✓ Usuario: {user.get('displayName', 'N/A')}")
        print(f"   ✓ Email: {user.get('emailAddress', 'N/A')}")
        print(f"   ✓ Account ID: {user.get('accountId', 'N/A')}")
        print()

        # Obtener información de un proyecto (cambia "PROJ" por tu proyecto)
        print("4. Obteniendo información del proyecto...")
        try:
            project_key = os.getenv("JIRA_DEFAULT_PROJECT", "PROJ")
            project = client.get_project(project_key)
            print(f"   ✓ Proyecto: {project.get('name', 'N/A')}")
            print(f"   ✓ Key: {project.get('key', 'N/A')}")
            print(f"   ✓ Type: {project.get('projectTypeKey', 'N/A')}")
        except JiraAPIError as e:
            print(f"   ✗ Error al obtener proyecto: {e}")
        print()

        # Crear un issue de prueba
        print("5. Creando issue de prueba...")
        issue = client.create_issue(
            project_key=project_key,
            summary="Issue de prueba desde Python - Test JiraClient",
            description=(
                "Este es un issue de prueba creado con el cliente de Jira.\n\n"
                "Características:\n"
                "- Creado con Python\n"
                "- Usa la REST API v3 de Jira\n"
                "- Soporta formato ADF para descripción"
            ),
            issue_type="Task",
            priority="Medium",
            labels=["python", "automation", "test"]
        )

        print(f"   ✓ Issue creado exitosamente!")
        print(f"   ✓ Key: {issue['key']}")
        print(f"   ✓ ID: {issue['id']}")
        print(f"   ✓ URL: {client.base_url}/browse/{issue['key']}")
        print()

        # Obtener el issue recién creado
        print("6. Verificando issue creado...")
        created_issue = client.get_issue(issue['key'])
        print(f"   ✓ Summary: {created_issue['fields']['summary']}")
        print(f"   ✓ Status: {created_issue['fields']['status']['name']}")
        print(f"   ✓ Priority: {created_issue['fields']['priority']['name']}")
        print()

        print("=" * 60)
        print("  ✓ Todas las pruebas completadas exitosamente")
        print("=" * 60)

    except ValueError as e:
        print(f"\n✗ Error de configuración: {e}")
        print("\nAsegúrate de configurar las variables de entorno:")
        print("  - JIRA_BASE_URL")
        print("  - JIRA_EMAIL")
        print("  - JIRA_API_TOKEN")
        print("\nO crea un archivo .env en la raíz del proyecto.")

    except JiraAPIError as e:
        print(f"\n✗ Error de Jira API: {e}")
        if e.status_code == 401:
            print("\nVerifica tus credenciales (email y API token)")
        elif e.status_code == 404:
            print("\nEl recurso no fue encontrado (verifica el project key)")
        elif e.status_code == 403:
            print("\nNo tienes permisos para realizar esta operación")

    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
