"""
Ejemplo de cómo crear un Carrusel usando el ReelWorkflowService.

Este archivo muestra diferentes formas de crear contenido de Instagram
incluyendo Reels, Historias y Carruseles.
"""

from app.clients.jira_client import JiraClient
from app.services.reel_workflow_service import ReelWorkflowService


def ejemplo_crear_carrusel():
    """Ejemplo 1: Crear un carrusel básico."""

    # 1. Inicializar cliente de Jira
    jira_client = JiraClient(
        base_url="https://tu-dominio.atlassian.net",
        email="tu-email@example.com",
        api_token="tu-api-token"
    )

    # 2. Inicializar servicio de workflow
    service = ReelWorkflowService(jira_client)

    # 3. Crear carrusel
    resultado = service.create_reel_workflow(
        project_key="KAN",
        title="Tips de fotografía en viajes",
        content_type="Carrusel",  # 🎠
        priority="Medium"
    )

    # 4. Resultado
    print(f"✅ Carrusel creado: {resultado['main_task']['key']}")
    print(f"🔗 URL: {resultado['main_task']['url']}")
    print(f"📊 Total de tareas: {resultado['total_tasks']}")
    print(f"\n📋 Subtareas creadas:")
    for subtask in resultado['subtasks']:
        print(f"  {subtask['emoji']} {subtask['phase']}: {subtask['key']}")


def ejemplo_carrusel_completo():
    """Ejemplo 2: Crear un carrusel con todas las opciones."""

    jira_client = JiraClient(
        base_url="https://tu-dominio.atlassian.net",
        email="tu-email@example.com",
        api_token="tu-api-token"
    )

    service = ReelWorkflowService(jira_client)

    # Buscar el account ID del usuario asignado
    assignee_id = jira_client.get_user_account_id("santiago", "KAN")

    resultado = service.create_reel_workflow(
        project_key="KAN",
        title="10 destinos imperdibles en Colombia",
        content_type="Carrusel",
        priority="High",
        labels=["viajes", "colombia", "turismo"],
        assignee=assignee_id,
        description="Serie de 10 imágenes mostrando los mejores destinos turísticos de Colombia con tips y recomendaciones."
    )

    print(f"✅ Carrusel creado: {resultado['main_task']['key']}")


def ejemplo_todos_los_tipos():
    """Ejemplo 3: Crear diferentes tipos de contenido."""

    jira_client = JiraClient(
        base_url="https://tu-dominio.atlassian.net",
        email="tu-email@example.com",
        api_token="tu-api-token"
    )

    service = ReelWorkflowService(jira_client)

    # Crear un Reel
    reel = service.create_reel_workflow(
        project_key="KAN",
        title="Tour por Cartagena",
        content_type="Reel",  # 🎬
        priority="High"
    )
    print(f"🎬 Reel creado: {reel['main_task']['key']}")

    # Crear una Historia
    historia = service.create_reel_workflow(
        project_key="KAN",
        title="Behind the scenes del viaje",
        content_type="Historia",  # 📸
        priority="Medium"
    )
    print(f"📸 Historia creada: {historia['main_task']['key']}")

    # Crear un Carrusel
    carrusel = service.create_reel_workflow(
        project_key="KAN",
        title="Guía de restaurantes en Bogotá",
        content_type="Carrusel",  # 🎠
        priority="Medium"
    )
    print(f"🎠 Carrusel creado: {carrusel['main_task']['key']}")


def ejemplo_usando_api():
    """Ejemplo 4: Crear un carrusel usando el API endpoint."""

    import requests

    url = "http://localhost:8000/api/v1/instagram"

    # Ejemplos de texto en lenguaje natural
    ejemplos = [
        "Crear carrusel de tips de viaje para Colombia",
        "Hacer un carrusel sobre los mejores hoteles en Medellín, alta prioridad",
        "Carrusel de recetas colombianas, asignado a santiago",
    ]

    for texto in ejemplos:
        response = requests.post(
            url,
            json={
                "text": texto,
                "project_key": "KAN"
            }
        )

        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ {resultado['content_type']} creado: {resultado['main_task_key']}")
            print(f"   Subtareas: {len(resultado['subtasks'])}")
        else:
            print(f"❌ Error: {response.text}")


def ejemplo_batch_mixto():
    """Ejemplo 5: Crear múltiples contenidos en batch (Reels, Historias y Carruseles)."""

    import requests

    url = "http://localhost:8000/api/v1/batch"

    # Crear múltiples contenidos de diferentes tipos
    response = requests.post(
        url,
        json={
            "tasks": [
                {"text": "Crear reel sobre tour en Cartagena, alta prioridad"},
                {"text": "Carrusel de 10 tips de fotografía de viaje"},
                {"text": "Historia behind the scenes del viaje"},
                {"text": "Carrusel de mejores restaurantes en Bogotá"},
                {"text": "Reel de receta de bandeja paisa, asignado a santiago"}
            ],
            "project_key": "KAN"
        }
    )

    if response.status_code == 200:
        resultado = response.json()
        print(f"\n📊 RESUMEN DEL BATCH:")
        print(f"  Total solicitado: {resultado['total_requested']}")
        print(f"  Creados exitosamente: {resultado['total_created']}")
        print(f"  Fallidos: {resultado['total_failed']}")
        print(f"  Total de tareas de Jira creadas: {resultado['total_tasks_created']}")

        print(f"\n📋 DETALLE:")
        for idx, task_result in enumerate(resultado['results'], 1):
            if task_result['success']:
                print(f"  {idx}. ✅ {task_result['content_type']} - {task_result['main_task_key']}")
                print(f"      Original: {task_result['original_text']}")
            else:
                print(f"  {idx}. ❌ Error: {task_result['error']}")
                print(f"      Original: {task_result['original_text']}")
    else:
        print(f"❌ Error en batch: {response.text}")


# Estructura del resultado que obtienes:
"""
{
    "success": True,
    "main_task": {
        "key": "KAN-123",
        "summary": "🎠 Carrusel IG | Tips de fotografía en viajes",
        "url": "https://tu-dominio.atlassian.net/browse/KAN-123",
        "type": "Carrusel",
        "priority": "Medium",
        "labels": ["carrusel"]
    },
    "subtasks": [
        {
            "key": "KAN-124",
            "summary": "🎬 Selección de tomas – Tips de fotografía en viajes",
            "phase": "Selección de tomas",
            "emoji": "🎬",
            "url": "https://tu-dominio.atlassian.net/browse/KAN-124"
        },
        {
            "key": "KAN-125",
            "summary": "✂️ Edición – Tips de fotografía en viajes",
            "phase": "Edición",
            "emoji": "✂️",
            "url": "https://tu-dominio.atlassian.net/browse/KAN-125"
        },
        {
            "key": "KAN-126",
            "summary": "🎵 Diseño sonoro – Tips de fotografía en viajes",
            "phase": "Diseño sonoro",
            "emoji": "🎵",
            "url": "https://tu-dominio.atlassian.net/browse/KAN-126"
        },
        {
            "key": "KAN-127",
            "summary": "🎨 Color – Tips de fotografía en viajes",
            "phase": "Color",
            "emoji": "🎨",
            "url": "https://tu-dominio.atlassian.net/browse/KAN-127"
        },
        {
            "key": "KAN-128",
            "summary": "✍️ Copy / Caption – Tips de fotografía en viajes",
            "phase": "Copy / Caption",
            "emoji": "✍️",
            "url": "https://tu-dominio.atlassian.net/browse/KAN-128"
        },
        {
            "key": "KAN-129",
            "summary": "📤 Export – Tips de fotografía en viajes",
            "phase": "Export",
            "emoji": "📤",
            "url": "https://tu-dominio.atlassian.net/browse/KAN-129"
        }
    ],
    "total_tasks": 7
}
"""


if __name__ == "__main__":
    print("=== Ejemplos de creación de Carruseles ===\n")

    # Descomenta el ejemplo que quieras ejecutar:
    # ejemplo_crear_carrusel()
    # ejemplo_carrusel_completo()
    # ejemplo_todos_los_tipos()
    # ejemplo_usando_api()
    # ejemplo_batch_mixto()
