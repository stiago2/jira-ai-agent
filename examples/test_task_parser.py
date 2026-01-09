"""
Ejemplo de uso del Task Parser.

Demuestra cómo usar el parser para transformar texto natural
en estructura de Jira.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.parsers.task_parser import TaskParser, create_parser


def print_separator(char="=", length=70):
    """Imprime una línea separadora."""
    print(char * length)


def print_result(result):
    """Imprime el resultado del parsing formateado."""
    print(f"   ✓ Summary:     {result.summary}")
    print(f"   ✓ Type:        {result.issue_type}")
    print(f"   ✓ Priority:    {result.priority}")
    print(f"   ✓ Assignee:    {result.assignee or 'N/A'}")
    print(f"   ✓ Labels:      {', '.join(result.labels) if result.labels else 'N/A'}")
    print(f"   ✓ Description: {result.description[:50]}...")
    print(f"   ✓ Confidence:  {result.confidence:.2%}")


def main():
    """Función principal de demostración."""
    print_separator()
    print("  TASK PARSER - Ejemplos de Uso")
    print_separator()
    print()

    # Crear parser
    parser = create_parser(use_llm=False)

    # Casos de prueba
    test_cases = [
        {
            "name": "Tarea con edición de video",
            "text": "Crea una tarea para editar el reel de Komodo, prioridad alta, asignada a Juan"
        },
        {
            "name": "Bug urgente",
            "text": "Bug crítico: el login no funciona en mobile, asignar a María"
        },
        {
            "name": "Feature backend",
            "text": "Implementar autenticación con OAuth2 para el backend API"
        },
        {
            "name": "Fix simple",
            "text": "Arreglar el error en el formulario de registro"
        },
        {
            "name": "Documentación",
            "text": "Documentar la API REST, baja prioridad"
        },
        {
            "name": "User Story",
            "text": "Como usuario quiero poder exportar mis datos a CSV para analizarlos offline"
        },
        {
            "name": "Tarea urgente",
            "text": "Configurar el servidor de producción ASAP, prioridad crítica"
        },
        {
            "name": "Performance",
            "text": "Optimizar las queries del dashboard para mejorar el rendimiento"
        }
    ]

    # Procesar cada caso
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['name']}")
        print(f"   Input: \"{test_case['text']}\"")
        print()

        try:
            result = parser.parse(test_case['text'])
            print_result(result)

        except Exception as e:
            print(f"   ✗ Error: {e}")

        print()

    # Ejemplo de conversión a dict
    print_separator("-")
    print("  Ejemplo de conversión a diccionario")
    print_separator("-")
    print()

    text = "Bug urgente en el sistema de pagos, asignar a Pedro"
    result = parser.parse(text)

    print(f"Input: \"{text}\"")
    print()
    print("Diccionario resultante:")
    print()

    result_dict = result.to_dict()
    for key, value in result_dict.items():
        print(f"   {key:12s}: {value}")

    print()

    # Ejemplo de validación de confianza
    print_separator("-")
    print("  Análisis de Confianza")
    print_separator("-")
    print()

    confidence_examples = [
        ("Texto muy descriptivo con prioridad alta y tipo bug", 0.8),
        ("Hacer algo", 0.5),
        ("x", 0.3)
    ]

    for text, expected_min in confidence_examples:
        result = parser.parse(text)
        status = "✓" if result.confidence >= expected_min else "✗"
        print(f"{status} \"{text}\"")
        print(f"   Confidence: {result.confidence:.2%}")
        print()

    print_separator()
    print("  ✓ Todos los ejemplos procesados")
    print_separator()


if __name__ == "__main__":
    main()
