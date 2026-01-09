"""
Script para probar la creación de issues con assignee.
"""
import requests
import json

def test_create_issue():
    """Prueba crear un issue con assignee."""

    url = "http://localhost:8000/api/v1/tasks/create"

    # Ejemplo 1: Con assignee que puede no existir
    data = {
        "text": "Crear reel sobre viaje a Cartagena, alta prioridad, asignado a santiago",
        "project_key": "KAN"
    }

    print("=" * 80)
    print("PRUEBA DE CREACIÓN DE ISSUE CON ASSIGNEE")
    print("=" * 80)
    print()
    print("INPUT:")
    print(json.dumps(data, indent=2))
    print()

    try:
        response = requests.post(url, json=data)

        print("RESPONSE:")
        print(f"Status Code: {response.status_code}")
        print()

        result = response.json()
        print(json.dumps(result, indent=2))

        if response.status_code == 200:
            print()
            print("✅ Issue creado exitosamente!")
            print(f"   Key: {result['issue_key']}")
            print(f"   URL: {result['issue_url']}")
            print(f"   Assignee detectado: {result['parsed_data'].get('assignee', 'N/A')}")
        else:
            print()
            print("❌ Error al crear issue")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_create_issue()
