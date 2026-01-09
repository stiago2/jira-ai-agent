# 🎯 MEJORAS AL PARSER - Detección Automática de Campos

> Actualización del parser para inferir automáticamente assignee, priority e issue type
>
> **Fecha**: 2026-01-08
> **Estado**: ✅ Completado y Probado

---

## 📊 RESUMEN DE CAMBIOS

El endpoint `/api/v1/tasks/create` ahora **infiere automáticamente** del texto:

| Campo | ¿Se detecta? | Ejemplo |
|-------|--------------|---------|
| **Assignee** (Persona) | ✅ Sí | "asignado a Juan" → `assignee: "Juan"` |
| **Priority** (Prioridad) | ✅ Sí | "alta prioridad" → `priority: "High"` |
| **Issue Type** (Tipo) | ✅ Sí | "bug crítico" → `issue_type: "Bug"` |
| **Labels** (Etiquetas) | ✅ Sí | "reel de viaje" → `labels: ["reel", "viaje"]` |

**NO se requieren cambios en la API pública**. El endpoint sigue siendo el mismo.

---

## 🔍 DETECCIÓN DE ASSIGNEE (PERSONA)

### Patrones Soportados

El parser detecta nombres de personas en estos formatos:

| Patrón | Ejemplo | Assignee Detectado |
|--------|---------|-------------------|
| `asignado a {Nombre}` | "asignado a Juan" | Juan |
| `asignar a {Nombre}` | "asignar a María" | María |
| `responsable {Nombre}` | "responsable Pedro" | Pedro |
| `a cargo de {Nombre}` | "a cargo de Ana" | Ana |
| `para {Nombre}` | "para Carlos" | Carlos |
| `por {Nombre}` | "por Luis" | Luis |
| `que lo haga {Nombre}` | "que lo haga Sofía" | Sofía |
| `@{Nombre}` | "@Juan" | Juan |

### Ejemplos Reales

```
INPUT: "Crear reel sobre viaje a Cartagena, asignado a Juan"
OUTPUT: assignee = "Juan"

INPUT: "Editar video responsable María, alta prioridad"
OUTPUT: assignee = "María"

INPUT: "Tutorial de fotografía a cargo de Pedro"
OUTPUT: assignee = "Pedro"

INPUT: "Reel de comida por Juan"
OUTPUT: assignee = "Juan"

INPUT: "Crear contenido @María importante"
OUTPUT: assignee = "María"
```

### Notas Importantes

⚠️ **El assignee debe ser un nombre con primera letra mayúscula** para ser detectado correctamente.

❌ NO funciona: "asignado a juan" (todo minúsculas)
✅ SÍ funciona: "asignado a Juan" (primera mayúscula)

⚠️ **Jira requiere Account ID, no nombres**

El parser extrae el nombre, pero para crear el issue en Jira necesitas el Account ID del usuario.

**Opciones**:
1. Mapear nombres a Account IDs en tu código
2. Buscar el usuario en Jira por nombre (ver sección "Búsqueda de Usuarios" abajo)
3. Dejar assignee como `null` y asignar manualmente en Jira

---

## ⚡ DETECCIÓN DE PRIORIDAD

### Palabras Clave Soportadas

| Prioridad Jira | Palabras Clave Detectadas |
|----------------|---------------------------|
| **Highest** | crítico, critical, urgente, urgent, inmediato, asap, bloqueante, blocker, emergencia, ahora mismo |
| **High** | alta, high, importante, important, pronto, prioritario, priority |
| **Medium** | media, medium, normal, regular, moderado (default) |
| **Low** | baja, low, menor, minor, cuando se pueda, no urgente |
| **Lowest** | muy baja, lowest, mínima, trivial, algún día, nice to have |

### Ejemplos

```
"Bug crítico en login" → priority = "Highest"
"Tarea importante para mañana" → priority = "High"
"Editar reel, prioridad media" → priority = "Medium"
"Documentar API, baja prioridad" → priority = "Low"
"Fix menor en UI, trivial" → priority = "Lowest"
"Crear tarea normal" → priority = "Medium" (default)
```

---

## 📝 DETECCIÓN DE ISSUE TYPE (WORK TYPE)

### Tipos Soportados

| Issue Type | Palabras Clave Detectadas |
|------------|---------------------------|
| **Bug** | bug, error, falla, fallo, problema, issue, arreglar, corregir, fix, solucionar, reparar, no funciona, roto, broken |
| **Story** | historia, story, user story, como usuario, necesito, quiero que, feature request, nueva funcionalidad |
| **Epic** | epic, épica, iniciativa, programa, proyecto grande, milestone, fase |
| **Task** | tarea, task, hacer, crear, implementar, agregar, desarrollar, actualizar, modificar, editar, configurar (default) |

### Ejemplos

```
"Bug crítico en el login" → issue_type = "Bug"
"Como usuario quiero exportar datos" → issue_type = "Story"
"Epic para módulo de reportes" → issue_type = "Epic"
"Crear reel sobre viaje" → issue_type = "Task"
"Implementar OAuth2" → issue_type = "Task"
```

---

## 🏷️ DETECCIÓN DE LABELS (ETIQUETAS)

### Labels Soportadas

El parser detecta automáticamente labels de varias categorías:

#### Tecnología
- `frontend` → frontend, ui, interfaz, diseño, visual
- `backend` → backend, servidor, api, base de datos, database
- `mobile` → mobile, móvil, ios, android, app

#### Contenido de Redes Sociales
- `reel` → reel, reels
- `historia` → historia, story, stories
- `video` → video, grabación, filmación
- `edicion` → edición, editar, editing, montaje
- `publicacion` → publicación, publicar, posting, subir

#### Categorías de Contenido
- `viaje` → viaje, travel, turismo
- `comida` → comida, receta, food, cocina
- `tutorial` → tutorial, how-to, guía, paso a paso
- `promocional` → promocional, promo, ads, publicidad

#### Ubicaciones
- `cartagena` → cartagena
- `bogota` → bogotá, bogota
- `medellin` → medellín, medellin
- `playa` → playa, beach
- `estudio` → estudio, studio

#### Urgencia
- `urgent` → urgente, urgent, crítico, critical, asap

### Ejemplos

```
"Crear reel de viaje a Cartagena"
→ labels = ["reel", "viaje", "cartagena"]

"Editar video de comida en estudio"
→ labels = ["video", "edicion", "comida", "estudio"]

"Bug urgente en el backend"
→ labels = ["backend", "urgent"]
```

---

## 📡 USO DEL ENDPOINT

### Request

```bash
curl -X POST http://localhost:8000/api/v1/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Crear reel sobre viaje a Cartagena de 30 segundos, alta prioridad, asignado a Juan",
    "project_key": "KAN"
  }'
```

### Response

```json
{
  "success": true,
  "issue_key": "KAN-123",
  "issue_url": "https://sfg222.atlassian.net/browse/KAN-123",
  "parsed_data": {
    "summary": "Crear reel sobre viaje a cartagena de 30 segundos, alta prioridad",
    "description": "Crear reel sobre viaje a Cartagena de 30 segundos, alta prioridad, asignado a Juan",
    "issue_type": "Task",
    "priority": "High",
    "assignee": "Juan",
    "labels": ["reel", "viaje", "cartagena"],
    "confidence": 0.80
  },
  "confidence": 0.80
}
```

### Interpretación

- ✅ **issue_type**: `Task` (default, no había keyword específico)
- ✅ **priority**: `High` (detectó "alta prioridad")
- ✅ **assignee**: `Juan` (detectó "asignado a Juan")
- ✅ **labels**: `["reel", "viaje", "cartagena"]` (detectó keywords)
- ✅ **confidence**: `0.80` (score de confianza del parsing)

---

## 🔄 BÚSQUEDA DE USUARIOS EN JIRA

### Problema

Jira requiere el **Account ID** del usuario, no el nombre.

**Ejemplo**:
- ❌ `assignee: "Juan"` → NO funciona
- ✅ `assignee: "5b10a2844c20165700ede21g"` → SÍ funciona

### Solución: Buscar Usuario por Nombre

Agrega este método al `JiraClient`:

```python
def search_user_by_name(self, name: str) -> Optional[str]:
    """
    Busca un usuario en Jira por nombre y retorna su Account ID.

    Args:
        name: Nombre del usuario (ej: "Juan", "María")

    Returns:
        Account ID del usuario o None si no se encuentra
    """
    try:
        # Buscar usuarios
        response = self._make_request(
            "GET",
            "/user/search",
            params={"query": name}
        )

        # Si encontramos resultados
        if response and len(response) > 0:
            # Retornar el Account ID del primer match
            return response[0]["accountId"]

        return None

    except Exception as e:
        print(f"Error buscando usuario {name}: {e}")
        return None
```

### Uso en el Endpoint

Modifica el endpoint `create_task_from_text` en `main.py`:

```python
# Si hay assignee, buscar el Account ID
assignee_account_id = None
if parsed_task.assignee:
    assignee_account_id = jira_client.search_user_by_name(parsed_task.assignee)
    if not assignee_account_id:
        print(f"⚠️  Usuario '{parsed_task.assignee}' no encontrado en Jira")

# Crear issue con Account ID
jira_response = jira_client.create_issue(
    project_key=request.project_key,
    summary=parsed_task.summary,
    description=parsed_task.description,
    issue_type=parsed_task.issue_type,
    priority=parsed_task.priority,
    labels=parsed_task.labels,
    assignee=assignee_account_id  # Usar Account ID, no nombre
)
```

---

## 📊 EJEMPLOS COMPLETOS

### Ejemplo 1: Reel Simple

**Input**:
```json
{
  "text": "Crear reel de viaje a Cartagena, alta prioridad",
  "project_key": "KAN"
}
```

**Parsing**:
- summary: "Crear reel de viaje a cartagena, alta prioridad"
- issue_type: "Task"
- priority: "High" ← detectado "alta prioridad"
- assignee: null ← no especificado
- labels: ["reel", "viaje", "cartagena"] ← detectados automáticamente

---

### Ejemplo 2: Bug Urgente con Asignación

**Input**:
```json
{
  "text": "Bug crítico en el login mobile, asap, responsable Juan",
  "project_key": "KAN"
}
```

**Parsing**:
- summary: "Bug crítico en el login mobile, asap, responsable juan"
- issue_type: "Bug" ← detectado "bug"
- priority: "Highest" ← detectado "crítico" y "asap"
- assignee: "Juan" ← detectado "responsable Juan"
- labels: ["mobile", "urgent"] ← detectados automáticamente

---

### Ejemplo 3: Historia con Múltiples Labels

**Input**:
```json
{
  "text": "Historia de receta de arepas en Bogotá, publicar mañana, para María",
  "project_key": "KAN"
}
```

**Parsing**:
- summary: "Historia de receta de arepas en bogotá, publicar mañana, para maría"
- issue_type: "Story" ← detectado "historia"
- priority: "Medium" ← default (no especificado)
- assignee: "María" ← detectado "para María"
- labels: ["historia", "comida", "publicacion", "bogota"] ← detectados automáticamente

---

## 🎯 SCORE DE CONFIANZA

El parser calcula un score de confianza (0.0 a 1.0) basado en:

| Factor | Puntos |
|--------|--------|
| Base | 0.5 |
| Issue type detectado (≠ default) | +0.2 |
| Priority detectada (≠ default) | +0.15 |
| Summary tiene 10-100 caracteres | +0.15 |
| Texto muy corto (< 20 chars) | -0.2 |

**Ejemplos**:

```
"Bug crítico, alta prioridad"
→ confidence = 0.5 + 0.2 (Bug) + 0.15 (High) + 0.15 (summary ok) = 1.00

"Crear tarea"
→ confidence = 0.5 + 0.0 (Task default) + 0.0 (Medium default) - 0.2 (corto) = 0.30

"Reel de viaje a Cartagena, importante"
→ confidence = 0.5 + 0.0 (Task) + 0.15 (High) + 0.15 (summary ok) = 0.80
```

---

## 🧪 PRUEBAS

Ejecuta el script de pruebas:

```bash
python3 test_parsing.py
```

Esto probará 10 ejemplos diferentes y mostrará los resultados.

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN COMPLETADA

- [x] Mejorar patrones de detección de assignee
- [x] Agregar soporte para nombres con acentos (á, é, í, ó, ú, ñ)
- [x] Detectar assignee en texto original (preservar mayúsculas)
- [x] Ampliar keywords de labels para contenido de redes sociales
- [x] Agregar labels de ubicaciones (Cartagena, Bogotá, etc.)
- [x] Detectar múltiples formas de asignación (por, para, responsable, @)
- [x] Probar con ejemplos reales
- [x] Documentar todos los patrones soportados

---

## 🔮 PRÓXIMOS PASOS (OPCIONAL)

### 1. Mapeo de Nombres a Account IDs

Crear un diccionario en la configuración:

```python
# En .env o config
USER_MAPPING = {
    "Juan": "5b10a2844c20165700ede21g",
    "María": "5c20b3955d30275800fef32h",
    "Pedro": "5d30c4066e40385900gfg43i"
}
```

### 2. Cache de Búsquedas de Usuarios

Guardar en Redis o en memoria las búsquedas de Account ID para no consultar cada vez.

### 3. Validación de Assignee

Verificar que el usuario existe antes de crear el issue.

---

## 📞 SOPORTE

Si encuentras problemas con la detección de campos:

1. Verifica que los nombres tengan primera letra mayúscula
2. Usa palabras clave explícitas (prioridad, asignado, responsable)
3. Revisa los ejemplos en este documento
4. Ejecuta `test_parsing.py` para ver qué se está detectando

---

**Última actualización**: 2026-01-08
**Versión del parser**: 1.1.0
