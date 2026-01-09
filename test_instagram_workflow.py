"""
Script para probar la creación de contenido de Instagram.
"""
import requests
import json


def test_create_instagram_content():
    """Prueba crear un workflow completo de Instagram (Reel/Historia)."""

    url = "http://localhost:8000/api/v1/content/instagram"

    # Ejemplos de prueba
    ejemplos = [
        {
            "nombre": "Reel de viaje",
            "data": {
                "text": "Crear reel sobre viaje a Cartagena en la playa, alta prioridad, asignado a santiago",
                "project_key": "KAN"
            }
        },
        {
            "nombre": "Historia de comida",
            "data": {
                "text": "Historia de receta de arepas en el estudio, asignado a santiago",
                "project_key": "KAN"
            }
        }
    ]

    for i, ejemplo in enumerate(ejemplos, 1):
        print("=" * 80)
        print(f"PRUEBA {i}: {ejemplo['nombre'].upper()}")
        print("=" * 80)
        print()
        print("INPUT:")
        print(json.dumps(ejemplo['data'], indent=2))
        print()

        try:
            response = requests.post(url, json=ejemplo['data'])

            print("RESPONSE:")
            print(f"Status Code: {response.status_code}")
            print()

            result = response.json()
            print(json.dumps(result, indent=2))

            if response.status_code == 200:
                print()
                print("✅ Workflow creado exitosamente!")
                print(f"   Tarea Principal: {result['main_task_key']}")
                print(f"   URL: {result['main_task_url']}")
                print(f"   Tipo: {result['content_type']}")
                print(f"   Total Tareas: {result['total_tasks']}")
                print()
                print("📋 Subtareas creadas:")
                for subtask in result['subtasks']:
                    print(f"   {subtask['emoji']} {subtask['key']}: {subtask['phase']}")
                    print(f"      URL: {subtask['url']}")
            else:
                print()
                print("❌ Error al crear workflow")

        except Exception as e:
            print(f"❌ Error: {e}")

        print()
        if i < len(ejemplos):
            input("Presiona Enter para continuar con el siguiente ejemplo...")
            print()


if __name__ == "__main__":
    test_create_instagram_content()
