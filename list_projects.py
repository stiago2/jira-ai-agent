"""
Script para listar los proyectos disponibles en tu instancia de Jira.
"""
from dotenv import load_dotenv
from app.clients.jira_client import JiraClient

# Cargar variables de entorno
load_dotenv()

def list_projects():
    """Lista todos los proyectos disponibles en Jira."""
    try:
        # Crear cliente de Jira
        client = JiraClient()

        print("=" * 70)
        print("Conectando a Jira...")
        print(f"URL: {client.base_url}")
        print(f"Usuario: {client.email}")
        print("=" * 70)

        # Obtener usuario actual para verificar conexión
        user = client.get_current_user()
        print(f"\n✓ Conectado como: {user.get('displayName', 'Unknown')}\n")

        # Listar proyectos
        print("Obteniendo proyectos disponibles...\n")
        projects = client._make_request("GET", "/project")

        if not projects:
            print("⚠️  No se encontraron proyectos.")
            print("   Verifica que tengas permisos para ver proyectos en Jira.")
            return

        print(f"Proyectos encontrados: {len(projects)}\n")
        print("=" * 70)
        print(f"{'KEY':<10} {'NOMBRE':<30} {'TIPO':<15}")
        print("=" * 70)

        for project in projects:
            key = project.get('key', 'N/A')
            name = project.get('name', 'N/A')
            project_type = project.get('projectTypeKey', 'N/A')

            # Truncar nombre si es muy largo
            if len(name) > 27:
                name = name[:27] + "..."

            print(f"{key:<10} {name:<30} {project_type:<15}")

        print("=" * 70)
        print("\n💡 Usa uno de los KEYs de arriba como 'project_key' en tus requests.")
        print("   Ejemplo: PROJ, DEV, TEST, etc.\n")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")
        print("Verifica que:")
        print("  1. El archivo .env tiene las credenciales correctas")
        print("  2. El API token es válido")
        print("  3. Tienes acceso a Jira Cloud\n")

if __name__ == "__main__":
    list_projects()
