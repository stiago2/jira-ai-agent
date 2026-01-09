"""
Reel Workflow Service - Crea workflows completos para producción de Reels, Historias y Carruseles.

Este servicio orquesta la creación de una tarea principal y sus subtareas asociadas
siguiendo el flujo de producción de contenido para Instagram.
"""

from typing import Dict, Any, List, Optional
from app.clients.jira_client import JiraClient, JiraAPIError


class ReelWorkflowService:
    """
    Servicio para crear workflows completos de producción de Reels/Historias/Carruseles.

    A partir de una intención de contenido parseada, crea:
    - 1 tarea principal (Task/Epic)
    - 6 subtareas siguiendo el flujo de producción
    """

    # Definición de las fases del workflow
    WORKFLOW_PHASES = [
        {
            "id": "seleccion",
            "name": "Selección de tomas",
            "emoji": "🎬",
            "description": (
                "📹 SELECCIÓN DE MATERIAL:\n"
                "- [ ] Revisar todo el material grabado\n"
                "- [ ] Seleccionar mejores tomas principales\n"
                "- [ ] Identificar B-roll útil\n"
                "- [ ] Organizar material por secuencia\n"
                "- [ ] Crear carpeta de trabajo con selects\n\n"
                "✅ ENTREGABLE: Material seleccionado y organizado"
            ),
            "labels": ["seleccion", "footage", "produccion"]
        },
        {
            "id": "edicion",
            "name": "Edición",
            "emoji": "✂️",
            "description": (
                "🎬 EDICIÓN DE VIDEO:\n"
                "- [ ] Importar footage a software de edición\n"
                "- [ ] Crear rough cut inicial\n"
                "- [ ] Ajustar timing y ritmo\n"
                "- [ ] Aplicar transiciones\n"
                "- [ ] Agregar efectos visuales si aplica\n"
                "- [ ] Crear fine cut final\n\n"
                "✅ ENTREGABLE: Video editado (fine cut)"
            ),
            "labels": ["edicion", "video-editing", "postproduccion"]
        },
        {
            "id": "audio",
            "name": "Diseño sonoro",
            "emoji": "🎵",
            "description": (
                "🔊 AUDIO Y MÚSICA:\n"
                "- [ ] Seleccionar música de fondo\n"
                "- [ ] Ajustar niveles de audio\n"
                "- [ ] Agregar efectos de sonido si aplica\n"
                "- [ ] Sincronizar audio con video\n"
                "- [ ] Masterización final de audio\n\n"
                "✅ ENTREGABLE: Audio finalizado y mezclado"
            ),
            "labels": ["audio", "sound-design", "postproduccion"]
        },
        {
            "id": "color",
            "name": "Color",
            "emoji": "🎨",
            "description": (
                "🌈 CORRECCIÓN DE COLOR:\n"
                "- [ ] Balance de blancos\n"
                "- [ ] Ajustar exposición y contraste\n"
                "- [ ] Aplicar LUT o preset de color\n"
                "- [ ] Corrección de color por shot\n"
                "- [ ] Ajustes finales de gradación\n\n"
                "✅ ENTREGABLE: Color grading finalizado"
            ),
            "labels": ["color", "color-grading", "postproduccion"]
        },
        {
            "id": "copy",
            "name": "Copy / Caption",
            "emoji": "✍️",
            "description": (
                "📝 COPY Y CAPTION:\n"
                "- [ ] Redactar caption principal\n"
                "- [ ] Crear hook/gancho inicial\n"
                "- [ ] Agregar call-to-action\n"
                "- [ ] Seleccionar hashtags relevantes (3-5)\n"
                "- [ ] Revisar ortografía y gramática\n\n"
                "✅ ENTREGABLE: Caption final aprobado"
            ),
            "labels": ["copy", "caption", "contenido"]
        },
        {
            "id": "export",
            "name": "Export",
            "emoji": "📤",
            "description": (
                "💾 EXPORTACIÓN Y ENTREGA:\n"
                "- [ ] Exportar en formato correcto (1080x1920, 9:16)\n"
                "- [ ] Verificar calidad de exportación\n"
                "- [ ] Comprimir si es necesario\n"
                "- [ ] Subir a plataforma de almacenamiento\n"
                "- [ ] Marcar como listo para publicación\n\n"
                "📐 ESPECIFICACIONES:\n"
                "- Resolución: 1080x1920 (vertical)\n"
                "- Formato: MP4, H.264\n"
                "- Duración: 15-90 segundos\n\n"
                "✅ ENTREGABLE: Archivo final listo para publicar"
            ),
            "labels": ["export", "final", "delivery"]
        }
    ]

    def __init__(self, jira_client: JiraClient):
        """
        Inicializa el servicio de workflow.

        Args:
            jira_client: Instancia del cliente de Jira
        """
        self.jira_client = jira_client

    def create_reel_workflow(
        self,
        project_key: str,
        title: str,
        content_type: str = "Reel",
        priority: str = "Medium",
        labels: Optional[List[str]] = None,
        assignee: Optional[str] = None,
        description: Optional[str] = None,
        subtask_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Crea un workflow completo para producción de Reel/Historia/Carrusel.

        Args:
            project_key: Clave del proyecto de Jira (ej: "KAN")
            title: Título del contenido (ej: "Viaje a Cartagena")
            content_type: Tipo de contenido ("Reel", "Historia" o "Carrusel")
            priority: Prioridad heredada (Highest, High, Medium, Low, Lowest)
            labels: Labels adicionales a agregar
            assignee: Account ID del asignado (opcional)
            description: Descripción adicional (opcional)

        Returns:
            Diccionario con información del workflow creado:
            {
                "success": True,
                "main_task": {...},
                "subtasks": [...],
                "total_tasks": 8
            }

        Raises:
            JiraAPIError: Si falla la creación de algún issue

        Example:
            >>> service = ReelWorkflowService(jira_client)
            >>> result = service.create_reel_workflow(
            ...     project_key="KAN",
            ...     title="Viaje a Cartagena",
            ...     content_type="Reel",
            ...     priority="High",
            ...     labels=["viaje", "cartagena"]
            ... )
            >>> print(result["main_task"]["key"])
            "KAN-123"
        """
        # Preparar labels
        workflow_labels = labels or []

        # Agregar label del tipo de contenido
        content_label = content_type.lower()
        if content_label not in workflow_labels:
            workflow_labels.append(content_label)

        # Determinar emoji según tipo de contenido
        content_lower = content_type.lower()
        if content_lower == "reel":
            emoji = "🎬"
        elif content_lower == "carrusel":
            emoji = "🎠"
        else:  # Historia
            emoji = "📸"

        # 1. Crear tarea principal
        main_task_summary = self._format_main_task_title(emoji, content_type, title)
        main_task_description = self._generate_main_task_description(
            content_type=content_type,
            title=title,
            custom_description=description
        )

        try:
            main_task = self.jira_client.create_issue(
                project_key=project_key,
                summary=main_task_summary,
                description=main_task_description,
                issue_type="Task",  # Usar Task como contenedor
                priority=priority,
                labels=workflow_labels,
                assignee=assignee
            )

            main_task_key = main_task["key"]

            # 2. Determinar qué subtareas crear
            # Si se especifican subtask_ids, filtrar; sino crear todas
            phases_to_create = self.WORKFLOW_PHASES
            if subtask_ids:
                phases_to_create = [
                    phase for phase in self.WORKFLOW_PHASES
                    if phase["id"] in subtask_ids
                ]

            # 3. Crear subtareas para cada fase seleccionada
            subtasks = []
            for phase in phases_to_create:
                subtask_summary = self._format_subtask_title(
                    phase['emoji'],
                    phase['name'],
                    title
                )

                # Heredar labels de la tarea principal + labels específicos de la fase
                subtask_labels = workflow_labels.copy()
                subtask_labels.extend(phase["labels"])

                subtask = self._create_subtask(
                    project_key=project_key,
                    parent_key=main_task_key,
                    summary=subtask_summary,
                    description=phase["description"],
                    priority=priority,
                    labels=subtask_labels,
                    assignee=assignee
                )

                subtasks.append({
                    "key": subtask["key"],
                    "summary": subtask_summary,
                    "phase": phase["name"],
                    "emoji": phase["emoji"],
                    "url": f"{self.jira_client.base_url}/browse/{subtask['key']}"
                })

            # 4. Construir respuesta
            return {
                "success": True,
                "main_task": {
                    "key": main_task_key,
                    "summary": main_task_summary,
                    "url": f"{self.jira_client.base_url}/browse/{main_task_key}",
                    "type": content_type,
                    "priority": priority,
                    "labels": workflow_labels
                },
                "subtasks": subtasks,
                "total_tasks": 1 + len(subtasks)
            }

        except JiraAPIError as e:
            raise JiraAPIError(
                f"Error al crear workflow: {str(e)}",
                status_code=e.status_code
            )

    def _create_subtask(
        self,
        project_key: str,
        parent_key: str,
        summary: str,
        description: str,
        priority: str,
        labels: List[str],
        assignee: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crea una subtarea vinculada a una tarea principal.

        Args:
            project_key: Clave del proyecto
            parent_key: Key de la tarea padre
            summary: Título de la subtarea
            description: Descripción de la subtarea
            priority: Prioridad
            labels: Labels
            assignee: Account ID del asignado

        Returns:
            Respuesta de Jira con el issue creado
        """
        # Construir payload con parent
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": self.jira_client._create_adf_content(description),
                "issuetype": {"name": "Subtask"},
                "parent": {"key": parent_key},
                "labels": labels
            }
        }

        # Agregar assignee si se proporciona
        if assignee:
            payload["fields"]["assignee"] = {"id": assignee}

        # Nota: Las subtasks en este proyecto no tienen campo priority
        # Si tu proyecto sí lo soporta, descomenta la siguiente línea:
        # payload["fields"]["priority"] = {"name": priority}

        response = self.jira_client._make_request(
            method="POST",
            endpoint="/issue",
            data=payload
        )

        return response

    def _generate_main_task_description(
        self,
        content_type: str,
        title: str,
        custom_description: Optional[str] = None
    ) -> str:
        """
        Genera la descripción para la tarea principal.

        Args:
            content_type: Tipo de contenido (Reel, Historia, Carrusel)
            title: Título del contenido
            custom_description: Descripción personalizada adicional

        Returns:
            Descripción formateada en texto plano (se convertirá a ADF)
        """
        # Sección del título del proyecto
        base_description = f"📹 PROYECTO: {content_type} - {title}\n\n"

        # Sección de descripción personalizada (opcional)
        if custom_description:
            base_description += f"📝 DESCRIPCIÓN:\n{custom_description}\n\n"

        # Sección del workflow
        base_description += (
            "🎯 WORKFLOW DE PRODUCCIÓN:\n"
            "1. 🎬 Selección de tomas - Organización del material\n"
            "2. ✂️ Edición - Montaje del video\n"
            "3. 🎵 Diseño sonoro - Audio y música\n"
            "4. 🎨 Color - Corrección y gradación de color\n"
            "5. ✍️ Copy / Caption - Redacción de texto\n"
            "6. 📤 Export - Exportación final\n\n"
            "📊 SEGUIMIENTO:\n"
            "- Cada fase tiene su propia subtarea\n"
            "- Completa las subtareas en orden\n"
            "- El proyecto estará listo cuando todas las subtareas estén completas\n\n"
            "🤖 Creado automáticamente por Jira AI Agent"
        )

        return base_description

    def _format_main_task_title(self, emoji: str, content_type: str, title: str) -> str:
        """
        Formatea el título de la tarea principal.

        Args:
            emoji: Emoji del tipo de contenido
            content_type: Tipo de contenido (Reel/Historia/Carrusel)
            title: Título descriptivo

        Returns:
            Título formateado para Jira

        Example:
            >>> _format_main_task_title("🎬", "Reel", "Editar reel Komodo")
            "🎬 Reel IG | Editar reel Komodo"
        """
        # Limpiar el título si ya contiene el tipo de contenido
        title_clean = title
        for prefix in ["crear reel", "crear historia", "crear carrusel", "reel", "historia", "carrusel", "editar reel", "editar historia", "editar carrusel"]:
            if title_clean.lower().startswith(prefix):
                title_clean = title_clean[len(prefix):].strip()

        # Capitalizar primera letra
        if title_clean:
            title_clean = title_clean[0].upper() + title_clean[1:]

        return f"{emoji} {content_type} IG | {title_clean}"

    def _format_subtask_title(self, emoji: str, phase_name: str, title: str) -> str:
        """
        Formatea el título de una subtarea.

        Args:
            emoji: Emoji de la fase
            phase_name: Nombre de la fase
            title: Título del contenido

        Returns:
            Título formateado para subtarea

        Example:
            >>> _format_subtask_title("✂️", "Edición", "Komodo Dragons")
            "✂️ Edición – Komodo Dragons"
        """
        # Limpiar el título si ya contiene el tipo de contenido
        title_clean = title
        for prefix in ["crear reel", "crear historia", "crear carrusel", "reel", "historia", "carrusel", "editar reel", "editar historia", "editar carrusel"]:
            if title_clean.lower().startswith(prefix):
                title_clean = title_clean[len(prefix):].strip()

        # Capitalizar primera letra
        if title_clean:
            title_clean = title_clean[0].upper() + title_clean[1:]

        return f"{emoji} {phase_name} – {title_clean}"

    def get_workflow_status(self, main_task_key: str) -> Dict[str, Any]:
        """
        Obtiene el estado de un workflow y sus subtareas.

        Args:
            main_task_key: Key de la tarea principal (ej: "KAN-123")

        Returns:
            Diccionario con el estado del workflow

        Example:
            >>> service.get_workflow_status("KAN-123")
            {
                "main_task": {...},
                "subtasks": [...],
                "progress": {
                    "total": 6,
                    "completed": 3,
                    "percentage": 50.0
                }
            }
        """
        try:
            # Obtener tarea principal
            main_task = self.jira_client.get_issue(main_task_key)

            # Obtener subtareas
            subtasks_data = main_task.get("fields", {}).get("subtasks", [])

            subtasks = []
            completed = 0

            for subtask_data in subtasks_data:
                status = subtask_data.get("fields", {}).get("status", {}).get("name", "Unknown")
                is_done = status.lower() in ["done", "completed", "closed"]

                if is_done:
                    completed += 1

                subtasks.append({
                    "key": subtask_data.get("key"),
                    "summary": subtask_data.get("fields", {}).get("summary", ""),
                    "status": status,
                    "is_done": is_done
                })

            total = len(subtasks)
            percentage = (completed / total * 100) if total > 0 else 0

            return {
                "main_task": {
                    "key": main_task_key,
                    "summary": main_task.get("fields", {}).get("summary", ""),
                    "status": main_task.get("fields", {}).get("status", {}).get("name", "Unknown")
                },
                "subtasks": subtasks,
                "progress": {
                    "total": total,
                    "completed": completed,
                    "in_progress": total - completed,
                    "percentage": round(percentage, 2)
                }
            }

        except JiraAPIError as e:
            raise JiraAPIError(
                f"Error al obtener estado del workflow: {str(e)}",
                status_code=e.status_code
            )
