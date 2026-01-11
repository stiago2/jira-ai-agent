"""
Subtask template model for user-defined workflow subtasks.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class SubtaskTemplate(Base):
    """
    Model for storing user-defined subtask templates.

    Each user can create custom subtask templates that will appear
    in the subtask selector when creating workflows.
    """
    __tablename__ = "subtask_templates"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Subtask details
    name = Column(String(100), nullable=False)
    emoji = Column(String(10), nullable=False, default="📋")
    description = Column(Text, nullable=True)

    # Labels for Jira (stored as comma-separated string)
    labels = Column(Text, nullable=True)  # e.g., "label1,label2,label3"

    # Order for display (lower numbers appear first)
    order = Column(Integer, nullable=False, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<SubtaskTemplate(id={self.id}, name='{self.name}', user_id={self.user_id})>"

    @property
    def labels_list(self) -> list[str]:
        """Convert comma-separated labels to list."""
        if not self.labels:
            return []
        return [label.strip() for label in self.labels.split(',') if label.strip()]

    @labels_list.setter
    def labels_list(self, value: list[str]):
        """Convert list to comma-separated labels."""
        self.labels = ','.join(value) if value else None
