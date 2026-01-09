"""
Ejemplos de uso del endpoint de usuarios del proyecto

Este archivo muestra cómo usar el endpoint para obtener todos los usuarios
asignables a un proyecto específico de Jira.
"""

import requests
import json

# Configuración
API_BASE_URL = "http://localhost:8000"
PROJECT_KEY = "KAN"  # Cambia esto por tu clave de proyecto


def ejemplo_obtener_usuarios():
    """
    Ejemplo 1: Obtener todos los usuarios asignables del proyecto

    Endpoint: GET /api/v1/projects/{project_key}/users

    Response:
    {
        "success": true,
        "project_key": "KAN",
        "total_users": 5,
        "users": [
            {
                "account_id": "5b10ac8d82e05b22cc7d4ef5",
                "display_name": "Juan Pérez",
                "email": "juan@example.com",
                "active": true,
                "avatar_url": "https://avatar-management..."
            },
            ...
        ]
    }
    """

    print("=" * 70)
    print("EJEMPLO 1: Obtener usuarios del proyecto")
    print("=" * 70)

    url = f"{API_BASE_URL}/api/v1/projects/{PROJECT_KEY}/users"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            print(f"\n✓ SUCCESS: Se encontraron {data['total_users']} usuarios")
            print(f"  Proyecto: {data['project_key']}\n")

            print("Usuarios disponibles:")
            print("-" * 70)

            for user in data['users']:
                print(f"\n  👤 {user['display_name']}")
                print(f"     Account ID: {user['account_id']}")
                if user.get('email'):
                    print(f"     Email: {user['email']}")
                print(f"     Activo: {'Sí' if user['active'] else 'No'}")

            print("\n" + "=" * 70)

            return data['users']

        else:
            print(f"\n✗ ERROR {response.status_code}")
            print(f"  {response.text}")
            return None

    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: No se pudo conectar al servidor")
        print("  ¿Está el servidor corriendo en http://localhost:8000?")
        return None

    except Exception as e:
        print(f"\n✗ ERROR inesperado: {str(e)}")
        return None


def ejemplo_filtrar_usuarios_activos():
    """
    Ejemplo 2: Filtrar solo usuarios activos del lado del cliente

    El endpoint ya filtra usuarios activos, pero este ejemplo muestra
    cómo trabajar con los datos en el cliente.
    """

    print("\n" + "=" * 70)
    print("EJEMPLO 2: Filtrar usuarios activos")
    print("=" * 70)

    url = f"{API_BASE_URL}/api/v1/projects/{PROJECT_KEY}/users"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Filtrar usuarios activos (aunque el endpoint ya lo hace)
            active_users = [user for user in data['users'] if user['active']]

            print(f"\n✓ Total usuarios activos: {len(active_users)}")

            # Crear un diccionario para búsqueda rápida por nombre
            users_by_name = {user['display_name'].lower(): user for user in active_users}

            print("\nBúsqueda de usuarios:")
            search_name = "juan"  # Nombre a buscar

            matching_users = [
                user for name, user in users_by_name.items()
                if search_name.lower() in name
            ]

            if matching_users:
                print(f"\n  Usuarios que coinciden con '{search_name}':")
                for user in matching_users:
                    print(f"    - {user['display_name']} ({user['account_id']})")
            else:
                print(f"\n  No se encontraron usuarios con '{search_name}'")

            print("\n" + "=" * 70)

        else:
            print(f"\n✗ ERROR {response.status_code}")

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")


def ejemplo_crear_tarea_con_asignacion(account_id: str):
    """
    Ejemplo 3: Crear una tarea y asignarla a un usuario específico

    Este ejemplo muestra el flujo completo:
    1. Obtener usuarios del proyecto
    2. Seleccionar un usuario por nombre
    3. Crear una tarea asignada a ese usuario

    Args:
        account_id: El account_id del usuario a asignar
    """

    print("\n" + "=" * 70)
    print("EJEMPLO 3: Crear tarea con asignación")
    print("=" * 70)

    # Datos de la tarea
    task_data = {
        "text": f"Crear Reel de producto nuevo, prioridad alta, asignado a {account_id}",
        "project_key": PROJECT_KEY
    }

    url = f"{API_BASE_URL}/api/v1/tasks/create"

    try:
        response = requests.post(
            url,
            json=task_data,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()

            print(f"\n✓ Tarea creada exitosamente")
            print(f"  Issue Key: {data['issue_key']}")
            print(f"  URL: {data['issue_url']}")
            print(f"  Asignado a: {account_id}")
            print("\n" + "=" * 70)

        else:
            print(f"\n✗ ERROR {response.status_code}")
            print(f"  {response.text}")

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")


def ejemplo_flujo_completo():
    """
    Ejemplo 4: Flujo completo de obtener usuarios y crear tarea asignada

    Este es el flujo típico en una aplicación:
    1. Usuario selecciona un proyecto
    2. La app carga los usuarios disponibles
    3. Usuario crea una tarea y selecciona un asignado
    4. La tarea se crea con el assignee
    """

    print("\n" + "=" * 70)
    print("EJEMPLO 4: Flujo completo")
    print("=" * 70)

    # Paso 1: Obtener usuarios
    print("\n📋 Paso 1: Obtener usuarios del proyecto...")
    users = ejemplo_obtener_usuarios()

    if not users or len(users) == 0:
        print("No hay usuarios disponibles para asignar")
        return

    # Paso 2: Seleccionar un usuario (simulado)
    print("\n👤 Paso 2: Seleccionar usuario...")
    selected_user = users[0]  # En una app real, el usuario elige
    print(f"  Usuario seleccionado: {selected_user['display_name']}")
    print(f"  Account ID: {selected_user['account_id']}")

    # Paso 3: Crear tarea asignada
    print("\n📝 Paso 3: Crear tarea con asignación...")
    ejemplo_crear_tarea_con_asignacion(selected_user['account_id'])


def ejemplo_manejo_errores():
    """
    Ejemplo 5: Manejo de errores comunes
    """

    print("\n" + "=" * 70)
    print("EJEMPLO 5: Manejo de errores")
    print("=" * 70)

    # Error: Proyecto no válido
    print("\n🔍 Probando con proyecto inválido...")
    url = f"{API_BASE_URL}/api/v1/projects/INVALID/users"

    try:
        response = requests.get(url)

        if response.status_code == 404:
            print("✓ Error manejado correctamente: Proyecto no encontrado")
        elif response.status_code == 401:
            print("✗ Error de autenticación con Jira")
        else:
            print(f"✗ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"✗ Error de conexión: {str(e)}")

    print("\n" + "=" * 70)


# ============================================================================
# Uso en React/TypeScript (ejemplo de código frontend)
# ============================================================================

REACT_EXAMPLE = """
// ============================================================================
// EJEMPLO DE USO EN REACT
// ============================================================================

import React, { useState } from 'react';
import { UserSelector } from '../components/UserSelector';
import { ApiService } from '../services/api.service';

export const TaskCreator: React.FC = () => {
  const [projectKey] = useState('KAN');
  const [taskText, setTaskText] = useState('');
  const [selectedUserId, setSelectedUserId] = useState<string | undefined>();

  const handleCreateTask = async () => {
    try {
      // Si hay un usuario seleccionado, incluirlo en el texto
      let text = taskText;
      if (selectedUserId) {
        text += ` asignado a ${selectedUserId}`;
      }

      const result = await ApiService.createTask({
        text: text,
        project_key: projectKey,
      });

      console.log('Tarea creada:', result);
    } catch (error) {
      console.error('Error al crear tarea:', error);
    }
  };

  return (
    <div>
      <h2>Crear Tarea</h2>

      <textarea
        value={taskText}
        onChange={(e) => setTaskText(e.target.value)}
        placeholder="Describe la tarea..."
      />

      {/* Selector de usuarios */}
      <UserSelector
        projectKey={projectKey}
        selectedUserId={selectedUserId}
        onUserSelect={setSelectedUserId}
        label="Asignar a"
        placeholder="Sin asignar"
        allowUnassigned={true}
      />

      <button onClick={handleCreateTask}>
        Crear Tarea
      </button>
    </div>
  );
};
"""


# ============================================================================
# Ejecutar ejemplos
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "EJEMPLOS DE ENDPOINT DE USUARIOS" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")

    # Menú de opciones
    print("\nSelecciona un ejemplo para ejecutar:")
    print("  1. Obtener usuarios del proyecto")
    print("  2. Filtrar usuarios activos")
    print("  3. Crear tarea con asignación")
    print("  4. Flujo completo (recomendado)")
    print("  5. Manejo de errores")
    print("  6. Ver ejemplo de código React")
    print("  0. Salir")

    try:
        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            ejemplo_obtener_usuarios()
        elif opcion == "2":
            ejemplo_filtrar_usuarios_activos()
        elif opcion == "3":
            users = ejemplo_obtener_usuarios()
            if users and len(users) > 0:
                print(f"\nUsando el primer usuario: {users[0]['display_name']}")
                ejemplo_crear_tarea_con_asignacion(users[0]['account_id'])
        elif opcion == "4":
            ejemplo_flujo_completo()
        elif opcion == "5":
            ejemplo_manejo_errores()
        elif opcion == "6":
            print(REACT_EXAMPLE)
        elif opcion == "0":
            print("\n¡Hasta luego!")
        else:
            print("\nOpción no válida")

    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
    except Exception as e:
        print(f"\nError: {str(e)}")
