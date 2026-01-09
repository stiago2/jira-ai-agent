"""
Script para verificar los tipos de issue y campos disponibles en Jira.
"""
from dotenv import load_dotenv
from app.clients.jira_client import JiraClient
import json

# Cargar variables de entorno
load_dotenv()

def check_jira_capabilities():
    """Verifica qué tipos de issues y campos están disponibles."""
    try:
        client = JiraClient()
        project_key = "KAN"  # Tu proyecto

        print("=" * 70)
        print("VERIFICANDO CAPACIDADES DE JIRA")
        print("=" * 70)

        # 1. Tipos de issue disponibles
        print("\n1. TIPOS DE ISSUE DISPONIBLES:")
        print("-" * 70)
        try:
            issue_types = client._make_request("GET", f"/project/{project_key}")
            if "issueTypes" in issue_types:
                for it in issue_types["issueTypes"]:
                    print(f"  - {it['name']:<20} (ID: {it['id']}, Subtask: {it.get('subtask', False)})")
            else:
                print("  No se encontraron tipos de issue en la respuesta")
        except Exception as e:
            print(f"  Error: {e}")

        # 2. Campos disponibles para crear issues
        print("\n2. CAMPOS DISPONIBLES PARA CREAR ISSUES:")
        print("-" * 70)
        try:
            create_meta = client._make_request("GET", f"/issue/createmeta", params={
                "projectKeys": project_key,
                "expand": "projects.issuetypes.fields"
            })

            if "projects" in create_meta and len(create_meta["projects"]) > 0:
                project = create_meta["projects"][0]
                for issue_type in project["issuetypes"]:
                    print(f"\n  Tipo: {issue_type['name']}")
                    print(f"  Campos requeridos:")
                    for field_key, field_info in issue_type["fields"].items():
                        if field_info.get("required"):
                            print(f"    - {field_info['name']:<30} ({field_key})")

                    print(f"  Campos opcionales principales:")
                    optional_fields = ["assignee", "labels", "priority", "duedate", "components"]
                    for field_key, field_info in issue_type["fields"].items():
                        if not field_info.get("required") and (field_key in optional_fields or field_info["name"] in ["Assignee", "Labels", "Priority"]):
                            print(f"    - {field_info['name']:<30} ({field_key})")
        except Exception as e:
            print(f"  Error: {e}")

        # 3. Campos personalizados
        print("\n3. CAMPOS PERSONALIZADOS:")
        print("-" * 70)
        try:
            fields = client._make_request("GET", "/field")
            custom_fields = [f for f in fields if f["custom"]]
            if custom_fields:
                for field in custom_fields[:10]:  # Primeros 10
                    print(f"  - {field['name']:<40} ({field['id']})")
            else:
                print("  No hay campos personalizados")
        except Exception as e:
            print(f"  Error: {e}")

        # 4. Prioridades disponibles
        print("\n4. PRIORIDADES DISPONIBLES:")
        print("-" * 70)
        try:
            priorities = client._make_request("GET", "/priority")
            for priority in priorities:
                print(f"  - {priority['name']:<15} (ID: {priority['id']})")
        except Exception as e:
            print(f"  Error: {e}")

        print("\n" + "=" * 70)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}\n")

if __name__ == "__main__":
    check_jira_capabilities()
