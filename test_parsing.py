"""
Script para probar el parsing mejorado con ejemplos reales.
"""
from app.parsers.task_parser import TaskParser

def test_parser():
    """Prueba el parser con diferentes textos."""
    parser = TaskParser()

    examples = [
        # Ejemplo básico
        "Crear reel sobre viaje a Cartagena, alta prioridad, asignado a Juan",

        # Con más detalles
        "Grabar reel de 30 segundos en la playa de Cartagena, editar con música tropical, asignar edición a María",

        # Historia simple
        "Historia sobre receta de arepas, publicar mañana, urgente",

        # Tutorial
        "Tutorial de fotografía móvil, 5 tips rápidos, para Pedro, prioridad media",

        # Bug
        "Bug crítico en el login, arreglar asap, responsable Juan",

        # Sin asignación
        "Editar reel de Komodo, alta prioridad",

        # Con @
        "Crear contenido promocional para Instagram @María, importante",

        # Diferentes formas de asignación
        "Reel de comida por Juan, baja prioridad",
        "Video tutorial a cargo de Pedro",
        "Historia de viaje responsable María, urgente",
    ]

    print("=" * 80)
    print("PRUEBAS DE PARSING MEJORADO")
    print("=" * 80)
    print()

    for i, text in enumerate(examples, 1):
        print(f"{i}. INPUT:")
        print(f"   {text}")
        print()

        try:
            result = parser.parse(text)

            print(f"   RESULTADO:")
            print(f"   ├─ Summary:      {result.summary}")
            print(f"   ├─ Issue Type:   {result.issue_type}")
            print(f"   ├─ Priority:     {result.priority}")
            print(f"   ├─ Assignee:     {result.assignee or 'Sin asignar'}")
            print(f"   ├─ Labels:       {', '.join(result.labels) if result.labels else 'Sin labels'}")
            print(f"   └─ Confidence:   {result.confidence:.2f}")

        except Exception as e:
            print(f"   ERROR: {e}")

        print()
        print("-" * 80)
        print()

if __name__ == "__main__":
    test_parser()
