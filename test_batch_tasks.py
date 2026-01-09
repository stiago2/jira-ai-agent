"""
Script para probar la creación de workflows de Instagram en batch.
"""
import requests
import json


def test_create_batch_instagram_workflows():
    """Prueba crear múltiples workflows de Instagram en batch."""

    url = "http://localhost:8000/api/v1/tasks/batch"

    # Ejemplo de batch: 3 contenidos de Instagram
    batch_request = {
        "project_key": "KAN",
        "tasks": [
            {"text": "Crear reel sobre viaje a Cartagena en la playa, alta prioridad, asignado a santiago"},
            {"text": "Historia de receta de arepas en el estudio, asignado a santiago"},
            {"text": "Reel de tips de fotografía, media prioridad, etiquetas: educativo, tips"},
        ]
    }

    print("=" * 80)
    print("PRUEBA: CREAR WORKFLOWS DE INSTAGRAM EN BATCH")
    print("=" * 80)
    print()
    print("REQUEST:")
    print(json.dumps(batch_request, indent=2, ensure_ascii=False))
    print()

    try:
        response = requests.post(url, json=batch_request)

        print("RESPONSE:")
        print(f"Status Code: {response.status_code}")
        print()

        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if response.status_code == 200:
            print()
            print("=" * 80)
            print("✅ RESUMEN DEL BATCH")
            print("=" * 80)
            print(f"Total workflows solicitados: {result['total_requested']}")
            print(f"Workflows creados exitosamente: {result['total_created']}")
            print(f"Workflows fallidos: {result['total_failed']}")
            print(f"Total tareas de Jira creadas: {result['total_tasks_created']}")
            print(f"Promedio: {result['total_tasks_created'] / result['total_requested']:.0f} tareas por workflow")
            print()

            print("RESULTADOS INDIVIDUALES:")
            print("-" * 80)
            for i, task_result in enumerate(result['results'], 1):
                print(f"\n{i}. {task_result['original_text']}")
                if task_result['success']:
                    print(f"   ✅ Workflow creado exitosamente")
                    print(f"   📦 Tipo: {task_result['content_type']}")
                    print(f"   🎯 Tarea Principal: {task_result['main_task_key']}")
                    print(f"   🔗 URL: {task_result['main_task_url']}")
                    print(f"   📊 Total tareas creadas: {task_result['total_tasks']}")
                    print(f"   📝 Subtareas ({len(task_result['subtasks'])}):")
                    for subtask in task_result['subtasks']:
                        print(f"      {subtask['emoji']} {subtask['key']}: {subtask['phase']}")
                else:
                    print(f"   ❌ Error: {task_result.get('error', 'Unknown error')}")

            print()
            print("=" * 80)
        else:
            print()
            print("❌ Error al crear batch de workflows")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_create_batch_instagram_workflows()
