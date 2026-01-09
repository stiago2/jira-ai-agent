# Task Parser

Parser que transforma texto en lenguaje natural a estructura de Jira.

## Características

- ✅ **Parsing basado en reglas** - Usa heurísticas y palabras clave
- ✅ **Detección de tipo de issue** - Task, Bug, Story, Epic
- ✅ **Extracción de prioridad** - Highest, High, Medium, Low, Lowest
- ✅ **Detección de asignado** - Múltiples patrones soportados
- ✅ **Extracción de labels** - Automática basada en contexto
- ✅ **Score de confianza** - Calcula qué tan seguro es el parsing
- ✅ **Preparado para LLM** - Interfaz compatible para futura integración

## Uso Básico

### Parsing Simple

```python
from app.parsers.task_parser import TaskParser

# Crear parser
parser = TaskParser()

# Parsear texto
text = "Crea una tarea para editar el reel de Komodo, prioridad alta, asignada a Juan"
result = parser.parse(text)

# Acceder a los campos
print(f"Summary: {result.summary}")
print(f"Type: {result.issue_type}")
print(f"Priority: {result.priority}")
print(f"Assignee: {result.assignee}")
print(f"Labels: {result.labels}")
print(f"Confidence: {result.confidence}")
```

### Usando Factory Pattern

```python
from app.parsers import create_parser

# Parser basado en reglas (default)
parser = create_parser(use_llm=False)

# Parser basado en LLM (futuro)
# parser = create_parser(use_llm=True, api_key="sk-...", model="gpt-4")

result = parser.parse("Bug crítico en el login")
```

### Convertir a Diccionario

```python
result = parser.parse("Implementar OAuth2")
data = result.to_dict()

# {
#     "summary": "Implementar OAuth2",
#     "description": "...",
#     "issue_type": "Task",
#     "priority": "Medium",
#     "assignee": None,
#     "labels": ["backend", "security"],
#     "confidence": 0.8
# }
```

## Ejemplos de Parsing

### 1. Tarea Básica

**Input:**
```
"Crear una tarea para editar el reel de Komodo"
```

**Output:**
```python
ParsedTask(
    summary="Editar el reel de komodo",
    issue_type="Task",
    priority="Medium",
    labels=["video"]
)
```

### 2. Bug con Prioridad

**Input:**
```
"Bug crítico: el login no funciona en mobile"
```

**Output:**
```python
ParsedTask(
    summary="Bug crítico: el login no funciona en mobile",
    issue_type="Bug",
    priority="Highest",
    labels=["mobile", "urgent"]
)
```

### 3. Tarea con Asignado

**Input:**
```
"Implementar API REST asignada a Pedro"
```

**Output:**
```python
ParsedTask(
    summary="Implementar api rest",
    issue_type="Task",
    priority="Medium",
    assignee="Pedro",
    labels=["backend"]
)
```

### 4. User Story

**Input:**
```
"Como usuario quiero exportar datos a CSV"
```

**Output:**
```python
ParsedTask(
    summary="Como usuario quiero exportar datos a csv",
    issue_type="Story",
    priority="Medium"
)
```

## Palabras Clave Soportadas

### Tipos de Issue

| Tipo | Palabras Clave |
|------|----------------|
| **Bug** | bug, error, falla, fallo, problema, arreglar, corregir, fix |
| **Story** | historia, story, user story, como usuario, feature request |
| **Epic** | epic, épica, iniciativa, programa |
| **Task** | tarea, task, hacer, crear, implementar, desarrollar |

### Prioridades

| Prioridad | Palabras Clave |
|-----------|----------------|
| **Highest** | crítico, critical, urgente, urgent, asap, bloqueante |
| **High** | alta, high, importante, important, prioritario |
| **Medium** | media, medium, normal, regular |
| **Low** | baja, low, menor, minor |
| **Lowest** | muy baja, lowest, trivial |

### Patrones de Asignación

- `asignada a [nombre]`
- `para [nombre]`
- `que lo haga [nombre]`
- `assign to [nombre]`
- `@[nombre]`

### Labels Automáticas

El parser detecta automáticamente labels basadas en contexto:

- **frontend** - ui, interfaz, diseño, visual
- **backend** - servidor, api, base de datos
- **mobile** - móvil, ios, android
- **documentation** - documentación, docs
- **testing** - test, prueba, qa
- **security** - seguridad, auth, autenticación
- **performance** - rendimiento, optimización
- **video** - video, reel, edición
- **urgent** - urgente, crítico

## Confidence Score

El parser calcula un score de confianza (0.0-1.0) basado en:

- ✅ Presencia de palabras clave de tipo (+0.2)
- ✅ Presencia de palabras clave de prioridad (+0.15)
- ✅ Longitud razonable del summary (+0.15)
- ❌ Texto muy corto (-0.2)

**Interpretación:**
- **0.8-1.0**: Alta confianza - parsing muy confiable
- **0.6-0.8**: Buena confianza - parsing probablemente correcto
- **0.4-0.6**: Confianza media - revisar el resultado
- **0.0-0.4**: Baja confianza - texto ambiguo o muy corto

## Limitaciones Actuales

⚠️ El parser basado en reglas tiene limitaciones:

1. **Contexto limitado** - No entiende contexto complejo
2. **Idioma mixto** - Funciona mejor con español o inglés consistente
3. **Nombres ambiguos** - Puede confundir verbos con nombres de personas
4. **Sinónimos** - Lista fija de palabras clave

## Migración a LLM

El código está preparado para integrar un LLM:

```python
class LLMTaskParser:
    """Parser basado en LLM (OpenAI, Anthropic, etc.)"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model

    def parse(self, text: str) -> ParsedTask:
        """
        Parsea usando LLM con prompt engineering.

        TODO: Implementar llamada al LLM
        """
        # Prompt para el LLM
        prompt = f"""
        Extrae información estructurada del siguiente texto para crear un issue de Jira:

        Texto: {text}

        Extrae:
        - summary (título corto)
        - description (descripción)
        - issue_type (Task, Bug, Story, Epic)
        - priority (Highest, High, Medium, Low, Lowest)
        - assignee (si se menciona)
        - labels (etiquetas relevantes)

        Retorna en formato JSON.
        """

        # TODO: Llamar al LLM
        # response = llm.complete(prompt)
        # return ParsedTask(**response)

        raise NotImplementedError()
```

Para usar LLM en el futuro:

```python
# Implementar el parser con LLM
parser = create_parser(
    use_llm=True,
    api_key="sk-...",
    model="gpt-4"
)

result = parser.parse("texto complejo que requiere IA")
```

## Testing

```bash
# Ejecutar ejemplo
python examples/test_task_parser.py

# Ejecutar tests unitarios
pytest tests/unit/test_task_parser.py -v

# Con cobertura
pytest tests/unit/test_task_parser.py --cov=app.parsers
```

## API Reference

### `TaskParser`

```python
class TaskParser:
    def parse(self, text: str) -> ParsedTask:
        """
        Parsea texto en lenguaje natural.

        Args:
            text: Texto a parsear

        Returns:
            ParsedTask con campos extraídos

        Raises:
            ValueError: Si el texto está vacío
        """
```

### `ParsedTask`

```python
@dataclass
class ParsedTask:
    summary: str                    # Título (max 255 chars)
    description: str                # Descripción completa
    issue_type: str                 # Task, Bug, Story, Epic
    priority: str                   # Highest, High, Medium, Low, Lowest
    assignee: Optional[str] = None  # Nombre del asignado
    labels: List[str] = []          # Lista de etiquetas
    confidence: float = 0.0         # Score 0.0-1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
```

### `create_parser()`

```python
def create_parser(
    use_llm: bool = False,
    **kwargs
) -> Union[TaskParser, LLMTaskParser]:
    """
    Factory para crear el parser apropiado.

    Args:
        use_llm: Si True, usa LLM. Si False, usa reglas.
        **kwargs: Argumentos para el parser (api_key, model, etc.)

    Returns:
        Instancia del parser
    """
```

## Roadmap

### ✅ Implementado
- Parser basado en reglas
- Detección de tipos y prioridades
- Extracción de asignado
- Labels automáticas
- Score de confianza
- Tests unitarios

### 🚧 En Progreso
- Mejorar detección de nombres propios
- Soporte para más idiomas
- Manejo de fechas (due dates)

### 📋 Por Hacer
- Integración con OpenAI GPT-4
- Integración con Anthropic Claude
- Soporte para campos custom de Jira
- Detección de dependencias entre tareas
- Extracción de story points
- API REST para el parser

## Contribuir

Para agregar más palabras clave o mejorar el parsing:

1. Editar `ISSUE_TYPE_KEYWORDS` o `PRIORITY_KEYWORDS`
2. Agregar patrones en `ASSIGNEE_PATTERNS`
3. Extender `label_keywords` en `_extract_labels()`
4. Agregar tests en `tests/unit/test_task_parser.py`

## Referencias

- [Jira Issue Types](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/)
- [Jira Priorities](https://support.atlassian.com/jira-cloud-administration/docs/configure-priority/)
- [Natural Language Processing](https://en.wikipedia.org/wiki/Natural_language_processing)
