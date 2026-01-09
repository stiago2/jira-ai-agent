"""
Task Parser - Transforma texto natural a estructura de Jira.

Parser basado en reglas y heurísticas que extrae información de texto
en lenguaje natural para crear tareas de Jira.

Este módulo está diseñado para ser fácilmente reemplazado por un LLM
en el futuro, manteniendo la misma interfaz.
"""

import re
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class ParsedTask:
    """
    Resultado del parsing de una tarea.

    Attributes:
        summary: Título corto de la tarea
        description: Descripción detallada
        issue_type: Tipo de issue (Task, Bug, Story, Epic)
        priority: Prioridad (Highest, High, Medium, Low, Lowest)
        assignee: Nombre del asignado (opcional)
        labels: Lista de etiquetas extraídas
        confidence: Nivel de confianza del parsing (0.0-1.0)
    """
    summary: str
    description: str
    issue_type: str
    priority: str
    assignee: Optional[str] = None
    labels: List[str] = None
    confidence: float = 0.0

    def __post_init__(self):
        """Inicializar labels si es None."""
        if self.labels is None:
            self.labels = []

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el objeto a diccionario.

        Returns:
            Diccionario con los campos del task
        """
        return {
            "summary": self.summary,
            "description": self.description,
            "issue_type": self.issue_type,
            "priority": self.priority,
            "assignee": self.assignee,
            "labels": self.labels,
            "confidence": self.confidence
        }


class TaskParser:
    """
    Parser de tareas basado en reglas heurísticas.

    Extrae información estructurada de texto en lenguaje natural
    usando patrones, palabras clave y reglas simples.

    Diseñado para ser fácilmente reemplazado por un LLM manteniendo
    la misma interfaz pública.
    """

    # Palabras clave para tipos de issue
    ISSUE_TYPE_KEYWORDS = {
        "Bug": [
            "bug", "error", "falla", "fallo", "problema", "issue",
            "arreglar", "corregir", "fix", "solucionar", "reparar",
            "no funciona", "roto", "broken"
        ],
        "Story": [
            "historia", "story", "user story", "como usuario",
            "necesito", "quiero que", "feature request", "nueva funcionalidad"
        ],
        "Epic": [
            "epic", "épica", "iniciativa", "programa", "proyecto grande",
            "milestone", "fase"
        ],
        "Task": [
            "tarea", "task", "hacer", "crear", "implementar", "agregar",
            "desarrollar", "actualizar", "modificar", "editar", "configurar"
        ]
    }

    # Palabras clave para prioridades
    PRIORITY_KEYWORDS = {
        "Highest": [
            "crítico", "critical", "urgente", "urgent", "inmediato",
            "asap", "bloqueante", "blocker", "emergencia", "ahora mismo"
        ],
        "High": [
            "alta", "high", "importante", "important", "pronto",
            "prioritario", "priority"
        ],
        "Medium": [
            "media", "medium", "normal", "regular", "moderado"
        ],
        "Low": [
            "baja", "low", "menor", "minor", "cuando se pueda",
            "no urgente"
        ],
        "Lowest": [
            "muy baja", "lowest", "mínima", "trivial", "algún día",
            "nice to have"
        ]
    }

    # Patrones para extraer nombres de personas (orden importa!)
    ASSIGNEE_PATTERNS = [
        r"asignad[oa]\s+a\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",  # asignado a Juan
        r"asignad[oa]\s+para\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",  # asignado para Juan
        r"asign(?:ar|ado|ada)\s+a\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",  # asignar a Juan
        r"responsable:?\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",  # responsable Juan
        r"a\s+cargo\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",  # a cargo de Juan
        r"que\s+lo\s+haga\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",  # que lo haga Juan
        r"por\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)(?:\s*,|\s*$)",  # por Juan, ...
        r"para\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)(?:\s*,|\s*$)",  # para Juan, ...
        r"assign(?:ed)?\s+to\s+([A-Z][a-z]+)",  # assigned to John
        r"@([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",  # @Juan
    ]

    # Palabras de acción que indican el verbo principal
    ACTION_VERBS = [
        "crear", "hacer", "implementar", "agregar", "añadir", "desarrollar",
        "arreglar", "corregir", "fix", "solucionar", "reparar",
        "actualizar", "modificar", "editar", "cambiar",
        "eliminar", "borrar", "quitar", "remover",
        "configurar", "instalar", "desplegar", "deploy",
        "revisar", "review", "analizar", "investigar",
        "documentar", "escribir", "redactar"
    ]

    def __init__(self):
        """Inicializa el parser."""
        self.default_priority = "Medium"
        self.default_issue_type = "Task"

    def parse(self, text: str) -> ParsedTask:
        """
        Parsea texto natural y extrae información estructurada.

        Args:
            text: Texto en lenguaje natural describiendo la tarea

        Returns:
            ParsedTask con la información extraída

        Example:
            >>> parser = TaskParser()
            >>> result = parser.parse("Crea una tarea para editar el reel de Komodo, prioridad alta")
            >>> print(result.summary)
            "Editar el reel de Komodo"
        """
        if not text or not text.strip():
            raise ValueError("El texto no puede estar vacío")

        # Normalizar texto para la mayoría de extracciones
        text_normalized = self._normalize_text(text)

        # Extraer componentes
        issue_type = self._extract_issue_type(text_normalized)
        priority = self._extract_priority(text_normalized)
        assignee = self._extract_assignee(text)  # Usar texto original para mantener mayúsculas
        labels = self._extract_labels(text_normalized)
        summary = self._extract_summary(text_normalized, issue_type)
        description = self._generate_description(text, summary)

        # Calcular confianza del parsing
        confidence = self._calculate_confidence(
            text_normalized, issue_type, priority, summary
        )

        return ParsedTask(
            summary=summary,
            description=description,
            issue_type=issue_type,
            priority=priority,
            assignee=assignee,
            labels=labels,
            confidence=confidence
        )

    def _normalize_text(self, text: str) -> str:
        """
        Normaliza el texto para facilitar el parsing.

        Args:
            text: Texto original

        Returns:
            Texto normalizado (lowercase, sin espacios extra)
        """
        # Convertir a minúsculas
        text = text.lower()

        # Reemplazar múltiples espacios por uno solo
        text = re.sub(r'\s+', ' ', text)

        # Quitar espacios al inicio y final
        text = text.strip()

        return text

    def _extract_issue_type(self, text: str) -> str:
        """
        Extrae el tipo de issue del texto.

        Args:
            text: Texto normalizado

        Returns:
            Tipo de issue (Task, Bug, Story, Epic)
        """
        # Contador de coincidencias por tipo
        scores = {issue_type: 0 for issue_type in self.ISSUE_TYPE_KEYWORDS}

        # Buscar palabras clave
        for issue_type, keywords in self.ISSUE_TYPE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    # Peso mayor si la palabra está al inicio
                    if text.startswith(keyword):
                        scores[issue_type] += 2
                    else:
                        scores[issue_type] += 1

        # Retornar el tipo con mayor score
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)

        return self.default_issue_type

    def _extract_priority(self, text: str) -> str:
        """
        Extrae la prioridad del texto.

        Args:
            text: Texto normalizado

        Returns:
            Prioridad (Highest, High, Medium, Low, Lowest)
        """
        # Buscar palabras clave de prioridad
        for priority, keywords in self.PRIORITY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    return priority

        return self.default_priority

    def _extract_assignee(self, text: str) -> Optional[str]:
        """
        Extrae el nombre del asignado del texto.

        Args:
            text: Texto original (sin normalizar para preservar mayúsculas)

        Returns:
            Nombre del asignado o None si no se encuentra
        """
        # Intentar con cada patrón
        for pattern in self.ASSIGNEE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1)
                # Capitalizar solo la primera letra si todo está en minúsculas
                if name.islower():
                    return name.capitalize()
                return name

        return None

    def _extract_labels(self, text: str) -> List[str]:
        """
        Extrae etiquetas/labels del texto.

        Args:
            text: Texto normalizado

        Returns:
            Lista de etiquetas extraídas
        """
        labels = []

        # Etiquetas comunes basadas en palabras clave
        label_keywords = {
            # Tecnología
            "frontend": ["frontend", "ui", "interfaz", "diseño", "visual"],
            "backend": ["backend", "servidor", "api", "base de datos", "database"],
            "mobile": ["mobile", "móvil", "ios", "android", "app"],

            # Documentación y testing
            "documentation": ["documentación", "documentation", "docs", "readme"],
            "testing": ["testing", "test", "prueba", "qa"],

            # Seguridad y performance
            "security": ["seguridad", "security", "auth", "autenticación"],
            "performance": ["performance", "rendimiento", "optimización", "velocidad"],

            # Contenido de redes sociales
            "reel": ["reel", "reels"],
            "historia": ["historia", "story", "stories"],
            "video": ["video", "grabación", "filmación"],
            "edicion": ["edición", "editar", "editing", "montaje"],
            "publicacion": ["publicación", "publicar", "posting", "subir"],

            # Categorías de contenido
            "viaje": ["viaje", "travel", "turismo"],
            "comida": ["comida", "receta", "food", "cocina"],
            "tutorial": ["tutorial", "how-to", "guía", "paso a paso"],
            "promocional": ["promocional", "promo", "ads", "publicidad"],

            # Ubicaciones
            "cartagena": ["cartagena"],
            "bogota": ["bogotá", "bogota"],
            "medellin": ["medellín", "medellin"],
            "playa": ["playa", "beach"],
            "estudio": ["estudio", "studio"],

            # Urgencia
            "urgent": ["urgente", "urgent", "crítico", "critical", "asap"]
        }

        for label, keywords in label_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    labels.append(label)
                    break

        # Eliminar duplicados manteniendo orden
        seen = set()
        labels = [x for x in labels if not (x in seen or seen.add(x))]

        return labels[:5]  # Limitar a 5 labels máximo

    def _extract_summary(self, text: str, issue_type: str) -> str:
        """
        Extrae el summary/título de la tarea.

        Args:
            text: Texto normalizado
            issue_type: Tipo de issue detectado

        Returns:
            Summary extraído
        """
        # Remover frases comunes de inicio
        prefixes_to_remove = [
            r"^(crea|crear|hace|hacer|agrega|agregar|añade|añadir)\s+(una\s+)?(tarea|task|issue)\s+(para\s+)?",
            r"^(arregla|arreglar|fix|corrige|corregir)\s+(el|la|los|las)\s+",
            r"^(implementa|implementar|develop|desarrolla|desarrollar)\s+",
            r"^necesito\s+(que\s+)?",
            r"^quiero\s+(que\s+)?",
        ]

        summary = text
        for prefix in prefixes_to_remove:
            summary = re.sub(prefix, "", summary, flags=re.IGNORECASE)

        # Remover información de prioridad y asignación
        # Primero remover "[prioridad] [nivel]" (con o sin coma antes)
        summary = re.sub(r",?\s*(prioridad|priority)\s+(muy\s+)?(alta|high|media|medium|baja|low|crítica|critical|urgente|urgent|highest|lowest)\b", "", summary, flags=re.IGNORECASE)
        # Remover "[nivel] prioridad" (orden inverso, común en español coloquial)
        summary = re.sub(r",?\s*(muy\s+)?(alta|high|media|medium|baja|low|crítica|critical|urgente|urgent|highest|lowest)\s+(prioridad|priority)\b", "", summary, flags=re.IGNORECASE)

        # Remover asignación
        summary = re.sub(r",?\s*asignad[oa](\s+a|\s+para)\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", "", summary, flags=re.IGNORECASE)
        summary = re.sub(r",?\s*(para|por|responsable)\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?=\s*,|\s*$)", "", summary, flags=re.IGNORECASE)
        summary = re.sub(r",?\s*@[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", "", summary, flags=re.IGNORECASE)
        summary = re.sub(r",?\s*a\s+cargo\s+de\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", "", summary, flags=re.IGNORECASE)

        # Limpiar
        summary = summary.strip().strip(",").strip()

        # Si quedó muy corto, usar el texto original
        if len(summary) < 10:
            summary = text

        # Capitalizar primera letra
        if summary:
            summary = summary[0].upper() + summary[1:]

        # Limitar longitud (Jira tiene límite de 255 caracteres)
        if len(summary) > 255:
            summary = summary[:252] + "..."

        return summary

    def _generate_description(self, original_text: str, summary: str) -> str:
        """
        Genera una descripción basada en el texto original.

        Args:
            original_text: Texto original (sin normalizar)
            summary: Summary ya extraído

        Returns:
            Descripción formateada (limpia, sin metadata de prioridad/assignee)
        """
        # Limpiar metadata del texto original
        description = original_text

        # Remover información de prioridad (ambos órdenes)
        description = re.sub(r",?\s*(prioridad|priority)\s+(muy\s+)?(alta|high|media|medium|baja|low|crítica|critical|urgente|urgent|highest|lowest)\b", "", description, flags=re.IGNORECASE)
        description = re.sub(r",?\s*(muy\s+)?(alta|high|media|medium|baja|low|crítica|critical|urgente|urgent|highest|lowest)\s+(prioridad|priority)\b", "", description, flags=re.IGNORECASE)

        # Remover información de asignación
        description = re.sub(r",?\s*asignad[oa](\s+a|\s+para)\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", "", description, flags=re.IGNORECASE)
        description = re.sub(r",?\s*(para|por|responsable)\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?=\s*,|\s*$)", "", description, flags=re.IGNORECASE)
        description = re.sub(r",?\s*@[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", "", description, flags=re.IGNORECASE)
        description = re.sub(r",?\s*a\s+cargo\s+de\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", "", description, flags=re.IGNORECASE)

        # Limpiar espacios y comas extras
        description = description.strip().strip(",").strip()

        # Si quedó muy corto o vacío, usar el summary
        if len(description) < 10:
            description = summary

        # Si el texto es muy similar al summary, agregar contexto
        if description.lower().strip() == summary.lower().strip():
            return f"{description}\n\n(Tarea creada automáticamente desde texto natural)"

        return description

    def _calculate_confidence(
        self,
        text: str,
        issue_type: str,
        priority: str,
        summary: str
    ) -> float:
        """
        Calcula un score de confianza del parsing (0.0-1.0).

        Args:
            text: Texto normalizado
            issue_type: Tipo extraído
            priority: Prioridad extraída
            summary: Summary extraído

        Returns:
            Score de confianza entre 0.0 y 1.0
        """
        score = 0.5  # Base score

        # Aumentar si encontramos palabras clave de tipo
        if issue_type != self.default_issue_type:
            score += 0.2

        # Aumentar si encontramos palabras clave de prioridad
        if priority != self.default_priority:
            score += 0.15

        # Aumentar si el summary es razonable (no muy corto ni muy largo)
        if 10 <= len(summary) <= 100:
            score += 0.15

        # Disminuir si el texto es muy corto
        if len(text) < 20:
            score -= 0.2

        # Asegurar que está en el rango [0.0, 1.0]
        return max(0.0, min(1.0, score))


class LLMTaskParser:
    """
    Placeholder para parser basado en LLM.

    Esta clase define la interfaz que debe implementar un parser
    basado en LLM (OpenAI, Anthropic, etc.) para mantener compatibilidad.

    TODO: Implementar cuando se integre el LLM
    """

    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Inicializa el parser con LLM.

        Args:
            api_key: API key del proveedor de LLM
            model: Modelo a usar
        """
        self.api_key = api_key
        self.model = model

    def parse(self, text: str) -> ParsedTask:
        """
        Parsea texto usando LLM.

        Args:
            text: Texto en lenguaje natural

        Returns:
            ParsedTask con la información extraída

        Raises:
            NotImplementedError: Aún no implementado
        """
        raise NotImplementedError(
            "LLM parser no implementado aún. "
            "Usa TaskParser para parsing basado en reglas."
        )


# Factory function para facilitar el cambio entre parsers
def create_parser(use_llm: bool = False, **kwargs) -> TaskParser:
    """
    Factory para crear el parser apropiado.

    Args:
        use_llm: Si True, usa LLM parser. Si False, usa rule-based parser
        **kwargs: Argumentos adicionales para el parser (api_key, model, etc.)

    Returns:
        Instancia del parser

    Example:
        >>> # Parser basado en reglas (default)
        >>> parser = create_parser()
        >>>
        >>> # Parser basado en LLM (futuro)
        >>> parser = create_parser(use_llm=True, api_key="sk-...", model="gpt-4")
    """
    if use_llm:
        return LLMTaskParser(**kwargs)
    return TaskParser()


# Ejemplo de uso
if __name__ == "__main__":
    """
    Ejemplos de uso del parser.
    """

    # Crear parser
    parser = TaskParser()

    # Ejemplos de parsing
    examples = [
        "Crea una tarea para editar el reel de Komodo, prioridad alta, asignada a Juan",
        "Bug urgente: el login no funciona en mobile",
        "Implementar autenticación con OAuth2 para el backend",
        "Arreglar el error en el formulario de registro",
        "Documentar la API REST, baja prioridad",
        "Como usuario quiero poder exportar mis datos a CSV"
    ]

    print("=" * 70)
    print("  EJEMPLOS DE PARSING DE TAREAS")
    print("=" * 70)
    print()

    for i, text in enumerate(examples, 1):
        print(f"{i}. Input: {text}")
        print("-" * 70)

        try:
            result = parser.parse(text)

            print(f"   Summary:     {result.summary}")
            print(f"   Type:        {result.issue_type}")
            print(f"   Priority:    {result.priority}")
            print(f"   Assignee:    {result.assignee or 'N/A'}")
            print(f"   Labels:      {', '.join(result.labels) if result.labels else 'N/A'}")
            print(f"   Confidence:  {result.confidence:.2f}")

        except Exception as e:
            print(f"   Error: {e}")

        print()
