"""
Project and user management endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional

from app.clients.jira_client import JiraClient, JiraAPIError
from app.api.dependencies import get_user_jira_client


router = APIRouter(tags=["Projects"])


# ============================================================================
# Pydantic Models
# ============================================================================

class JiraUser(BaseModel):
    """Información de un usuario de Jira."""

    account_id: str = Field(..., description="ID único de la cuenta", example="5f8a1b2c3d4e5f6g7h8i9j0k")
    display_name: str = Field(..., description="Nombre para mostrar", example="Santiago Florez")
    email: Optional[str] = Field(None, description="Email del usuario", example="santiago@example.com")
    active: bool = Field(default=True, description="Si el usuario está activo")
    avatar_url: Optional[str] = Field(None, description="URL del avatar")


class GetProjectUsersResponse(BaseModel):
    """Response con la lista de usuarios asignables al proyecto."""

    success: bool = Field(default=True)
    project_key: str = Field(..., description="Clave del proyecto", example="KAN")
    total_users: int = Field(..., description="Total de usuarios encontrados")
    users: List[JiraUser] = Field(..., description="Lista de usuarios asignables")


# ============================================================================
# Endpoints
# ============================================================================

@router.get("/projects/{project_key}/users", response_model=GetProjectUsersResponse)
async def get_project_users(
    project_key: str,
    jira_client: JiraClient = Depends(get_user_jira_client)
):
    """
    Obtiene todos los usuarios asignables a un proyecto específico.

    Requiere autenticación con JWT token.

    Este endpoint es útil para mostrar dropdowns de usuarios en la UI,
    permitiendo asignar tareas a personas específicas del equipo.

    Args:
        project_key: Clave del proyecto de Jira (ej: "KAN")
        jira_client: Cliente de Jira con credenciales del usuario (inyectado)

    Returns:
        GetProjectUsersResponse con lista de usuarios

    Raises:
        HTTPException 404: Proyecto no encontrado
        HTTPException 401: Error de autenticación con Jira
        HTTPException 500: Error interno del servidor

    Example:
        GET /api/v1/projects/KAN/users

        Response:
        {
            "success": true,
            "project_key": "KAN",
            "total_users": 3,
            "users": [
                {
                    "account_id": "5f8a1b2c3d4e5f6g7h8i9j0k",
                    "display_name": "Santiago Florez",
                    "email": "santiago@example.com",
                    "active": true,
                    "avatar_url": "https://..."
                }
            ]
        }
    """
    try:
        # Buscar usuarios asignables al proyecto usando la API de Jira
        # Endpoint: /rest/api/3/user/assignable/search
        response = jira_client._make_request(
            method="GET",
            endpoint="/user/assignable/search",
            params={
                "project": project_key,
                "maxResults": 1000  # Máximo permitido por Jira
            }
        )

        # Parsear usuarios
        users = []
        for user_data in response:
            # Verificar que el usuario esté activo
            if user_data.get("active", True):
                users.append(JiraUser(
                    account_id=user_data["accountId"],
                    display_name=user_data.get("displayName", "Unknown"),
                    email=user_data.get("emailAddress"),
                    active=user_data.get("active", True),
                    avatar_url=user_data.get("avatarUrls", {}).get("48x48")
                ))

        # Ordenar por nombre para mejor UX
        users.sort(key=lambda u: u.display_name.lower())

        return GetProjectUsersResponse(
            success=True,
            project_key=project_key,
            total_users=len(users),
            users=users
        )

    except JiraAPIError as e:
        if e.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proyecto '{project_key}' no encontrado"
            )
        elif e.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Error de autenticación con Jira: {str(e)}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener usuarios: {str(e)}"
            )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )
