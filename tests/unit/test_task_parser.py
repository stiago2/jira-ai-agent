"""
Tests unitarios para TaskParser.
"""

import pytest
from app.parsers.task_parser import TaskParser, ParsedTask, create_parser


class TestTaskParser:
    """Tests para la clase TaskParser."""

    @pytest.fixture
    def parser(self):
        """Fixture que crea un parser."""
        return TaskParser()

    def test_parse_basic_task(self, parser):
        """Test parsing de tarea básica."""
        text = "Crear una tarea para editar el reel de Komodo"
        result = parser.parse(text)

        assert isinstance(result, ParsedTask)
        assert "reel" in result.summary.lower()
        assert result.issue_type == "Task"
        assert result.priority == "Medium"  # Default

    def test_parse_with_priority(self, parser):
        """Test parsing con prioridad especificada."""
        text = "Crear tarea urgente para el servidor"
        result = parser.parse(text)

        assert result.priority in ["Highest", "High"]

    def test_parse_with_assignee(self, parser):
        """Test parsing con asignado."""
        text = "Tarea para configurar BD asignada a Juan"
        result = parser.parse(text)

        assert result.assignee == "Juan"

    def test_parse_bug(self, parser):
        """Test detección de tipo Bug."""
        text = "Bug crítico en el login"
        result = parser.parse(text)

        assert result.issue_type == "Bug"
        assert result.priority in ["Highest", "High"]

    def test_parse_story(self, parser):
        """Test detección de User Story."""
        text = "Como usuario quiero exportar datos a CSV"
        result = parser.parse(text)

        assert result.issue_type == "Story"

    def test_parse_epic(self, parser):
        """Test detección de Epic."""
        text = "Epic para implementar el módulo de reportes"
        result = parser.parse(text)

        assert result.issue_type == "Epic"

    def test_extract_labels(self, parser):
        """Test extracción de labels."""
        text = "Implementar autenticación en el backend API con testing"
        result = parser.parse(text)

        assert "backend" in result.labels
        assert "security" in result.labels or "testing" in result.labels

    def test_summary_length_limit(self, parser):
        """Test que el summary respeta el límite de caracteres."""
        long_text = "Crear tarea " + "x" * 300
        result = parser.parse(long_text)

        assert len(result.summary) <= 255

    def test_empty_text_raises_error(self, parser):
        """Test que texto vacío lanza error."""
        with pytest.raises(ValueError):
            parser.parse("")

    def test_confidence_score_range(self, parser):
        """Test que confidence está en rango válido."""
        text = "Tarea con prioridad alta"
        result = parser.parse(text)

        assert 0.0 <= result.confidence <= 1.0

    def test_to_dict_conversion(self, parser):
        """Test conversión a diccionario."""
        text = "Bug en el sistema"
        result = parser.parse(text)
        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert "summary" in result_dict
        assert "issue_type" in result_dict
        assert "priority" in result_dict
        assert "assignee" in result_dict
        assert "labels" in result_dict
        assert "confidence" in result_dict

    def test_multiple_assignee_patterns(self, parser):
        """Test diferentes patrones de asignación."""
        texts = [
            "Tarea asignada a Pedro",
            "Tarea para María",
            "Tarea que lo haga Luis",
            "Tarea @Ana"
        ]

        for text in texts:
            result = parser.parse(text)
            assert result.assignee is not None

    def test_priority_keywords_spanish(self, parser):
        """Test palabras clave de prioridad en español."""
        priority_texts = {
            "Highest": "tarea crítica",
            "High": "tarea importante",
            "Low": "tarea menor"
        }

        for expected_priority, text in priority_texts.items():
            result = parser.parse(text)
            assert result.priority == expected_priority

    def test_video_label_detection(self, parser):
        """Test detección de label de video."""
        text = "Editar el reel de marketing"
        result = parser.parse(text)

        assert "video" in result.labels

    def test_normalize_text(self, parser):
        """Test normalización de texto."""
        text = "  CREAR   TAREA   CON   ESPACIOS  "
        result = parser.parse(text)

        # Debe parsear correctamente sin errores
        assert result.summary
        assert result.issue_type


class TestParsedTask:
    """Tests para la clase ParsedTask."""

    def test_parsed_task_creation(self):
        """Test creación de ParsedTask."""
        task = ParsedTask(
            summary="Test task",
            description="Description",
            issue_type="Task",
            priority="High",
            assignee="John",
            labels=["test"],
            confidence=0.8
        )

        assert task.summary == "Test task"
        assert task.issue_type == "Task"
        assert task.assignee == "John"

    def test_parsed_task_default_labels(self):
        """Test que labels se inicializa como lista vacía."""
        task = ParsedTask(
            summary="Test",
            description="Desc",
            issue_type="Task",
            priority="Medium"
        )

        assert task.labels == []

    def test_parsed_task_to_dict(self):
        """Test conversión de ParsedTask a dict."""
        task = ParsedTask(
            summary="Test",
            description="Desc",
            issue_type="Bug",
            priority="High",
            confidence=0.9
        )

        d = task.to_dict()

        assert d["summary"] == "Test"
        assert d["issue_type"] == "Bug"
        assert d["confidence"] == 0.9


class TestCreateParser:
    """Tests para la función create_parser."""

    def test_create_rule_based_parser(self):
        """Test crear parser basado en reglas."""
        parser = create_parser(use_llm=False)

        assert isinstance(parser, TaskParser)

    def test_create_llm_parser_raises_not_implemented(self):
        """Test que LLM parser lanza NotImplementedError."""
        parser = create_parser(use_llm=True, api_key="test", model="gpt-4")

        with pytest.raises(NotImplementedError):
            parser.parse("test")


class TestIntegration:
    """Tests de integración end-to-end."""

    def test_full_workflow(self):
        """Test flujo completo de parsing."""
        parser = create_parser()

        # Input real
        text = "Bug crítico: el sistema de pagos no funciona, asignar a Carlos urgentemente"

        # Parse
        result = parser.parse(text)

        # Verificar resultado
        assert result.issue_type == "Bug"
        assert result.priority in ["Highest", "High"]
        assert result.assignee == "Carlos"
        assert "pagos" in result.summary.lower() or "pagos" in result.description.lower()

    def test_real_world_examples(self):
        """Test con ejemplos del mundo real."""
        parser = create_parser()

        examples = [
            {
                "text": "Crea una tarea para editar el reel de Komodo, prioridad alta, asignada a Juan",
                "expected": {
                    "issue_type": "Task",
                    "priority": "High",
                    "assignee": "Juan"
                }
            },
            {
                "text": "Arreglar el bug en el login de mobile",
                "expected": {
                    "issue_type": "Bug",
                }
            },
            {
                "text": "Implementar API REST para usuarios",
                "expected": {
                    "issue_type": "Task",
                }
            }
        ]

        for example in examples:
            result = parser.parse(example["text"])

            for key, expected_value in example["expected"].items():
                actual_value = getattr(result, key)
                assert actual_value == expected_value, \
                    f"Failed for '{example['text']}': expected {key}={expected_value}, got {actual_value}"
