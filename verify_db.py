"""
Script to verify database tables exist and create them if needed.
"""
from app.core.database import engine, Base
from app.models import SubtaskTemplate, User

def verify_database():
    """Verify and create database tables if needed."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables verified and created successfully")

        # Print all table names
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\n📋 Available tables: {', '.join(tables)}")

        # Check subtask_templates table specifically
        if 'subtask_templates' in tables:
            columns = [col['name'] for col in inspector.get_columns('subtask_templates')]
            print(f"\n✨ subtask_templates columns: {', '.join(columns)}")
        else:
            print("\n⚠️ subtask_templates table not found")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_database()
