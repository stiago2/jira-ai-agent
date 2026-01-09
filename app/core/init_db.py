"""
Database initialization script.

Run this script to:
1. Create all database tables
2. Optionally create a default admin user
"""
import sys
import os
from getpass import getpass

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.core.database import engine, SessionLocal, init_db
from app.core.security import get_password_hash
from app.core.encryption import encrypt_token
from app.models.user import User


def create_admin_user(
    username: str,
    email: str,
    password: str,
    jira_email: str,
    jira_api_token: str,
    jira_base_url: str
):
    """
    Create an admin user.

    Args:
        username: Admin username
        email: Admin email
        password: Admin password
        jira_email: Jira account email
        jira_api_token: Jira API token
        jira_base_url: Jira instance URL
    """
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            print(f"⚠️  Usuario '{username}' ya existe en la base de datos")
            return

        # Create admin user
        admin_user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            jira_email=jira_email,
            jira_api_token=encrypt_token(jira_api_token),
            jira_base_url=jira_base_url.rstrip("/"),
            is_active=True,
            is_superuser=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"✓ Usuario admin '{username}' creado exitosamente")
        print(f"  - Email: {email}")
        print(f"  - ID: {admin_user.id}")

    except Exception as e:
        print(f"❌ Error al crear usuario admin: {str(e)}")
        db.rollback()
    finally:
        db.close()


def main():
    """Main function to initialize database."""
    print("=" * 70)
    print("  JIRA AI AGENT - Inicialización de Base de Datos")
    print("=" * 70)
    print()

    # Create tables
    print("📦 Creando tablas de base de datos...")
    try:
        init_db()
        print("✓ Tablas creadas exitosamente")
    except Exception as e:
        print(f"❌ Error al crear tablas: {str(e)}")
        return

    print()

    # Ask if user wants to create admin user
    create_admin = input("¿Deseas crear un usuario administrador? (s/n): ").lower().strip()

    if create_admin in ['s', 'si', 'y', 'yes']:
        print()
        print("📝 Ingresa los datos del usuario administrador:")
        print()

        username = input("  Username: ").strip()
        email = input("  Email: ").strip()
        password = getpass("  Password: ")
        password_confirm = getpass("  Confirmar password: ")

        if password != password_confirm:
            print("❌ Las contraseñas no coinciden")
            return

        print()
        print("📝 Ingresa las credenciales de Jira:")
        print()

        jira_email = input("  Jira Email: ").strip()
        jira_api_token = getpass("  Jira API Token: ")
        jira_base_url = input("  Jira Base URL (ej: https://company.atlassian.net): ").strip()

        print()
        print("🔨 Creando usuario administrador...")
        create_admin_user(
            username=username,
            email=email,
            password=password,
            jira_email=jira_email,
            jira_api_token=jira_api_token,
            jira_base_url=jira_base_url
        )

    print()
    print("=" * 70)
    print("  ✓ Inicialización completada")
    print("=" * 70)


if __name__ == "__main__":
    main()
