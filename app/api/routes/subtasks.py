"""
API routes for managing user subtask templates.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.user import User
from app.models.subtask import SubtaskTemplate
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/subtasks", tags=["subtasks"])


# Pydantic models
class SubtaskCreate(BaseModel):
    """Request model for creating a subtask template."""
    name: str = Field(..., min_length=1, max_length=100, description="Subtask name")
    emoji: str = Field("📋", min_length=1, max_length=10, description="Emoji icon")
    description: str | None = Field(None, max_length=500, description="Subtask description")
    labels: List[str] = Field(default_factory=list, description="Jira labels")


class SubtaskUpdate(BaseModel):
    """Request model for updating a subtask template."""
    name: str | None = Field(None, min_length=1, max_length=100)
    emoji: str | None = Field(None, min_length=1, max_length=10)
    description: str | None = Field(None, max_length=500)
    labels: List[str] | None = None


class SubtaskReorder(BaseModel):
    """Request model for reordering subtasks."""
    subtask_ids: List[int] = Field(..., description="Ordered list of subtask IDs")


class SubtaskResponse(BaseModel):
    """Response model for subtask template."""
    id: int
    name: str
    emoji: str
    description: str | None
    labels: List[str]
    order: int
    created_at: str
    updated_at: str | None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, subtask: SubtaskTemplate):
        """Convert ORM model to response model."""
        return cls(
            id=subtask.id,
            name=subtask.name,
            emoji=subtask.emoji,
            description=subtask.description,
            labels=subtask.labels_list,
            order=subtask.order,
            created_at=subtask.created_at.isoformat() if subtask.created_at else "",
            updated_at=subtask.updated_at.isoformat() if subtask.updated_at else None,
        )


# Default subtasks for new users
DEFAULT_SUBTASKS_DATA = [
    {
        "name": "Selección de tomas",
        "emoji": "🎬",
        "description": "Organización del material",
        "labels": ["seleccion", "footage", "produccion"],
        "order": 0
    },
    {
        "name": "Edición",
        "emoji": "✂️",
        "description": "Montaje del video",
        "labels": ["edicion", "video-editing", "postproduccion"],
        "order": 1
    },
    {
        "name": "Diseño sonoro",
        "emoji": "🎵",
        "description": "Audio y música",
        "labels": ["audio", "sound-design", "postproduccion"],
        "order": 2
    },
    {
        "name": "Color",
        "emoji": "🎨",
        "description": "Corrección y gradación de color",
        "labels": ["color", "color-grading", "postproduccion"],
        "order": 3
    },
    {
        "name": "Copy / Caption",
        "emoji": "✍️",
        "description": "Redacción de texto",
        "labels": ["copy", "caption", "contenido"],
        "order": 4
    },
    {
        "name": "Export",
        "emoji": "📤",
        "description": "Exportación final",
        "labels": ["export", "final", "delivery"],
        "order": 5
    }
]


def initialize_default_subtasks(user_id: int, db: Session) -> List[SubtaskTemplate]:
    """Create default subtasks for a new user."""
    subtasks = []
    for data in DEFAULT_SUBTASKS_DATA:
        subtask = SubtaskTemplate(
            user_id=user_id,
            name=data["name"],
            emoji=data["emoji"],
            description=data["description"],
            labels=",".join(data["labels"]),
            order=data["order"]
        )
        db.add(subtask)
        subtasks.append(subtask)

    db.commit()
    for subtask in subtasks:
        db.refresh(subtask)

    return subtasks


@router.get("", response_model=List[SubtaskResponse])
async def get_subtasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all subtask templates for the current user.

    If the user has no subtasks yet, initialize them with defaults.
    """
    subtasks = db.query(SubtaskTemplate).filter(
        SubtaskTemplate.user_id == current_user.id
    ).order_by(SubtaskTemplate.order).all()

    # Initialize default subtasks if user has none
    if not subtasks:
        subtasks = initialize_default_subtasks(current_user.id, db)

    return [SubtaskResponse.from_orm(st) for st in subtasks]


@router.post("", response_model=SubtaskResponse, status_code=status.HTTP_201_CREATED)
async def create_subtask(
    subtask_data: SubtaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new subtask template for the current user."""
    # Get max order to append to end
    max_order = db.query(SubtaskTemplate).filter(
        SubtaskTemplate.user_id == current_user.id
    ).count()

    subtask = SubtaskTemplate(
        user_id=current_user.id,
        name=subtask_data.name,
        emoji=subtask_data.emoji,
        description=subtask_data.description,
        labels=",".join(subtask_data.labels) if subtask_data.labels else None,
        order=max_order
    )

    db.add(subtask)
    db.commit()
    db.refresh(subtask)

    return SubtaskResponse.from_orm(subtask)


@router.put("/{subtask_id}", response_model=SubtaskResponse)
async def update_subtask(
    subtask_id: int,
    subtask_data: SubtaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a subtask template."""
    subtask = db.query(SubtaskTemplate).filter(
        SubtaskTemplate.id == subtask_id,
        SubtaskTemplate.user_id == current_user.id
    ).first()

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found"
        )

    # Update fields if provided
    if subtask_data.name is not None:
        subtask.name = subtask_data.name
    if subtask_data.emoji is not None:
        subtask.emoji = subtask_data.emoji
    if subtask_data.description is not None:
        subtask.description = subtask_data.description
    if subtask_data.labels is not None:
        subtask.labels = ",".join(subtask_data.labels) if subtask_data.labels else None

    db.commit()
    db.refresh(subtask)

    return SubtaskResponse.from_orm(subtask)


@router.delete("/{subtask_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subtask(
    subtask_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a subtask template."""
    subtask = db.query(SubtaskTemplate).filter(
        SubtaskTemplate.id == subtask_id,
        SubtaskTemplate.user_id == current_user.id
    ).first()

    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subtask not found"
        )

    # Check if user has at least 2 subtasks before deleting
    count = db.query(SubtaskTemplate).filter(
        SubtaskTemplate.user_id == current_user.id
    ).count()

    if count <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the last subtask. You must have at least one subtask."
        )

    db.delete(subtask)
    db.commit()


@router.post("/reorder", response_model=List[SubtaskResponse])
async def reorder_subtasks(
    reorder_data: SubtaskReorder,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reorder subtasks by providing ordered list of IDs."""
    # Verify all subtasks belong to user
    subtasks = db.query(SubtaskTemplate).filter(
        SubtaskTemplate.id.in_(reorder_data.subtask_ids),
        SubtaskTemplate.user_id == current_user.id
    ).all()

    if len(subtasks) != len(reorder_data.subtask_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subtask IDs provided"
        )

    # Update order
    subtask_map = {st.id: st for st in subtasks}
    for idx, subtask_id in enumerate(reorder_data.subtask_ids):
        subtask_map[subtask_id].order = idx

    db.commit()

    # Refresh and return ordered list
    for subtask in subtasks:
        db.refresh(subtask)

    sorted_subtasks = sorted(subtasks, key=lambda x: x.order)
    return [SubtaskResponse.from_orm(st) for st in sorted_subtasks]
