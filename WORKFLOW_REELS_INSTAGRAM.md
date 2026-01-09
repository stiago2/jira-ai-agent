# 📱 WORKFLOW PARA REELS E HISTORIAS DE INSTAGRAM

> Diseño de workflow específico para producción de contenido de Instagram usando Jira
>
> **Compatible con**: Proyecto existente jira-ai-agent
> **Proyecto Jira**: KAN (Instagram Reels)
> **Fecha**: 2026-01-08

---

## 🎯 OBJETIVO

Crear un sistema automatizado que convierta texto natural en workflows completos de producción de Reels/Historias, estructurados en Jira con Epics y Subtasks.

**Ejemplo de input**:
```
"Crear reel sobre viaje a Cartagena, grabar en playa, editar con música tropical,
duración 30 segundos, asignar grabación a Juan y edición a María"
```

**Resultado esperado en Jira**:
- 1 Epic: "🎬 [REEL] Viaje a Cartagena"
- 4 Subtasks: Preproducción, Grabación, Edición, Publicación

---

## 📊 ESTRUCTURA DEL WORKFLOW

### Jerarquía de Issues

```
Epic (Issue Type: Epic)
  └─ Nombre: 🎬 [REEL] {Título del contenido}
      ├─ Subtask 1: 📋 Preproducción: {Título}
      ├─ Subtask 2: 🎥 Grabación: {Título}
      ├─ Subtask 3: ✂️ Edición: {Título}
      └─ Subtask 4: 🚀 Publicación: {Título}
```

### Alternativa para Historias

```
Epic (Issue Type: Epic)
  └─ Nombre: 📸 [HISTORIA] {Título del contenido}
      ├─ Subtask 1: 📋 Planificación: {Título}
      ├─ Subtask 2: 📷 Captura: {Título}
      └─ Subtask 3: 🚀 Publicación: {Título}
```

---

## 🏗️ DISEÑO DETALLADO DE TAREAS

### 1️⃣ EPIC (Contenedor del Proyecto)

**Issue Type**: `Epic`

**Convención de Nombre**:
```
Patrón: {Emoji} [TIPO] {Título corto}

Ejemplos:
- 🎬 [REEL] Viaje a Cartagena
- 📸 [HISTORIA] Receta de arepas
- 🎬 [REEL] Tips de fotografía móvil
- 📸 [HISTORIA] Día en la oficina
```

**Campos Jira**:
| Campo | Valor | Ejemplo |
|-------|-------|---------|
| **summary** | `{Emoji} [TIPO] {Título}` | `🎬 [REEL] Viaje a Cartagena` |
| **issuetype** | `Epic` | Epic |
| **project** | `KAN` | KAN |
| **labels** | `["reel", "{ubicacion}", "{tema}"]` | `["reel", "cartagena", "viaje"]` |
| **duedate** | Fecha de publicación deseada | `2026-01-15` |
| **description** | Descripción completa en ADF | Ver formato abajo |

**Formato de Descripción (ADF)**:
```
📹 CONTENIDO: {Tipo de contenido}
🎯 OBJETIVO: {Qué se quiere lograr}
📍 UBICACIÓN: {Dónde se grabará}
⏱️ DURACIÓN: {30 segundos}
🎨 ESTILO: {Música, filtros, estética}
📝 NOTAS ADICIONALES: {Cualquier contexto extra}
```

**Labels recomendadas para Epic**:
- **Tipo de contenido**: `reel`, `historia`, `carrusel`
- **Categoría temática**: `viaje`, `comida`, `tutorial`, `detrás-de-escena`, `promocional`
- **Ubicación**: `cartagena`, `bogota`, `medellin`, `estudio`, `exterior`
- **Urgencia**: `urgente`, `planificado`

---

### 2️⃣ SUBTASKS (Fases del Workflow)

#### 📋 FASE 1: PREPRODUCCIÓN / PLANIFICACIÓN

**Issue Type**: `Subtask`
**Parent**: Epic ID

**Convención de Nombre**:
```
📋 Preproducción: {Título del Epic}
```

**Campos Jira**:
| Campo | Valor | Ejemplo |
|-------|-------|---------|
| **summary** | `📋 Preproducción: {Título}` | `📋 Preproducción: Viaje a Cartagena` |
| **issuetype** | `Subtask` | Subtask |
| **parent** | Epic key | `KAN-123` |
| **assignee** | Productor/Planner | Account ID |
| **labels** | `["preproduccion", "planificacion"]` | - |
| **priority** | Basado en urgencia | `High`, `Medium` |

**Descripción**:
```
✅ CHECKLIST DE PREPRODUCCIÓN:
- [ ] Definir concepto y mensaje clave
- [ ] Crear guion/storyline
- [ ] Identificar locaciones necesarias
- [ ] Listar props/elementos necesarios
- [ ] Planificar vestuario
- [ ] Coordinar horarios del equipo
- [ ] Solicitar permisos si es necesario

📝 ENTREGABLES:
- Guion aprobado
- Lista de recursos
- Cronograma de grabación
```

**Labels específicas**:
- `preproduccion`
- `planificacion`
- `concept-design`

---

#### 🎥 FASE 2: GRABACIÓN / CAPTURA

**Issue Type**: `Subtask`
**Parent**: Epic ID

**Convención de Nombre**:
```
Para Reels: 🎥 Grabación: {Título del Epic}
Para Historias: 📷 Captura: {Título del Epic}
```

**Campos Jira**:
| Campo | Valor | Ejemplo |
|-------|-------|---------|
| **summary** | `🎥 Grabación: {Título}` | `🎥 Grabación: Viaje a Cartagena` |
| **issuetype** | `Subtask` | Subtask |
| **parent** | Epic key | `KAN-123` |
| **assignee** | Camarógrafo/Creador | Account ID |
| **labels** | `["grabacion", "filming", "{ubicacion}"]` | `["grabacion", "filming", "playa"]` |
| **priority** | Alta si tiene deadline | `High` |
| **duedate** | Fecha límite de grabación | `2026-01-10` |

**Descripción**:
```
🎬 PLAN DE GRABACIÓN:
- [ ] Verificar equipo: Cámara, trípode, iluminación
- [ ] Confirmar locación y permisos
- [ ] Revisar condiciones climáticas (si aplica)
- [ ] Grabar tomas principales
- [ ] Grabar B-roll y tomas de apoyo
- [ ] Revisar material grabado en sitio

📋 SHOTS NECESARIOS:
- {Lista de tomas específicas}

⏱️ DURACIÓN ESTIMADA: {X horas}

📍 UBICACIÓN: {Dirección o lugar específico}
```

**Labels específicas**:
- `grabacion` / `filming`
- `video`
- Ubicación: `playa`, `estudio`, `ciudad`, `exterior`, `interior`
- `raw-footage`

---

#### ✂️ FASE 3: EDICIÓN

**Issue Type**: `Subtask`
**Parent**: Epic ID

**Convención de Nombre**:
```
✂️ Edición: {Título del Epic}
```

**Campos Jira**:
| Campo | Valor | Ejemplo |
|-------|-------|---------|
| **summary** | `✂️ Edición: {Título}` | `✂️ Edición: Viaje a Cartagena` |
| **issuetype** | `Subtask` | Subtask |
| **parent** | Epic key | `KAN-123` |
| **assignee** | Editor de video | Account ID |
| **labels** | `["edicion", "postproduccion", "video-editing"]` | - |
| **priority** | Alta si tiene deadline | `High` |
| **duedate** | Fecha límite de edición | `2026-01-12` |

**Descripción**:
```
🎨 TAREAS DE EDICIÓN:
- [ ] Importar footage a software de edición
- [ ] Seleccionar mejores tomas
- [ ] Crear corte inicial (rough cut)
- [ ] Agregar música/audio
- [ ] Aplicar transiciones y efectos
- [ ] Agregar texto/subtítulos si aplica
- [ ] Corrección de color
- [ ] Exportar en formato correcto (1080x1920, vertical)
- [ ] Revisión final

🎵 MÚSICA: {Nombre de la pista o link}

📐 FORMATO FINAL:
- Resolución: 1080x1920 (9:16 vertical)
- Duración: {30 segundos}
- Formato: MP4, H.264

✅ APROBACIÓN: {Quién debe aprobar}
```

**Labels específicas**:
- `edicion` / `editing`
- `postproduccion`
- `video-editing`
- `color-grading`
- `sound-design`

---

#### 🚀 FASE 4: PUBLICACIÓN

**Issue Type**: `Subtask`
**Parent**: Epic ID

**Convención de Nombre**:
```
🚀 Publicación: {Título del Epic}
```

**Campos Jira**:
| Campo | Valor | Ejemplo |
|-------|-------|---------|
| **summary** | `🚀 Publicación: {Título}` | `🚀 Publicación: Viaje a Cartagena` |
| **issuetype** | `Subtask` | Subtask |
| **parent** | Epic key | `KAN-123` |
| **assignee** | Community Manager | Account ID |
| **labels** | `["publicacion", "social-media", "instagram"]` | - |
| **priority** | Highest si es time-sensitive | `Highest` |
| **duedate** | Fecha/hora de publicación | `2026-01-15` |

**Descripción**:
```
📱 TAREAS DE PUBLICACIÓN:
- [ ] Redactar caption/descripción
- [ ] Seleccionar hashtags relevantes
- [ ] Programar fecha y hora óptima
- [ ] Subir a Instagram
- [ ] Verificar que se publicó correctamente
- [ ] Monitorear primeras interacciones
- [ ] Responder comentarios iniciales

✍️ CAPTION:
{Texto para la publicación}

#️⃣ HASHTAGS:
{Lista de hashtags}

🕐 FECHA Y HORA:
{Fecha y hora específica de publicación}

📊 MÉTRICAS A MONITOREAR:
- Views en primeras 24h
- Engagement rate
- Saves/Shares
```

**Labels específicas**:
- `publicacion` / `publishing`
- `social-media`
- `instagram`
- `scheduled` (si está programado)
- `live` (cuando está publicado)

---

## 🏷️ SISTEMA DE LABELS COMPLETO

### Labels por Categoría

#### 1. **Tipo de Contenido** (Obligatorio - 1 por Epic)
```
reel           → Video corto (hasta 90 segundos)
historia       → Instagram Story (24 horas)
carrusel       → Múltiples imágenes/videos
post           → Imagen estática tradicional
```

#### 2. **Fase del Workflow** (1 por Subtask)
```
preproduccion   → Fase de planificación
grabacion       → Fase de captura de contenido
edicion         → Fase de postproducción
publicacion     → Fase de publicación
```

#### 3. **Categoría Temática** (1-2 por Epic)
```
viaje           → Contenido de viajes
comida          → Recetas, restaurantes
tutorial        → Educativo, how-to
detras-escena   → Behind the scenes
promocional     → Contenido comercial
colaboracion    → Con otras cuentas
evento          → Cobertura de eventos
lifestyle       → Día a día, personal
```

#### 4. **Ubicación** (Opcional - 0-1 por Epic)
```
cartagena       → Grabado en Cartagena
bogota          → Grabado en Bogotá
medellin        → Grabado en Medellín
estudio         → Grabado en estudio
exterior        → Locación exterior
interior        → Locación interior
```

#### 5. **Prioridad/Estado** (Opcional)
```
urgente         → Requiere atención inmediata
planificado     → Parte del calendario editorial
trending        → Relacionado con trending topic
evergreen       → Contenido atemporal
```

#### 6. **Aspectos Técnicos** (Opcional - para Subtasks)
```
vertical        → Formato 9:16
horizontal      → Formato 16:9
cuadrado        → Formato 1:1
4k              → Resolución 4K
drone           → Requiere drone
time-lapse      → Técnica de time-lapse
slow-motion     → Cámara lenta
```

### Ejemplo de Etiquetado Completo

**Epic**:
```
Labels: ["reel", "viaje", "cartagena", "planificado"]
```

**Subtask - Grabación**:
```
Labels: ["grabacion", "playa", "vertical", "drone"]
```

**Subtask - Edición**:
```
Labels: ["edicion", "color-grading", "sound-design"]
```

**Subtask - Publicación**:
```
Labels: ["publicacion", "instagram", "scheduled"]
```

---

## 📋 CAMPOS DE JIRA UTILIZADOS

### Campos Estándar de Jira Cloud

| Campo Jira | Tipo | Uso en Workflow | Obligatorio | Ejemplo |
|------------|------|-----------------|-------------|---------|
| **summary** | Text (255 chars) | Título del issue | ✅ Sí | `🎬 [REEL] Viaje a Cartagena` |
| **issuetype** | Enum | Epic o Subtask | ✅ Sí | `Epic` |
| **project** | Object | Proyecto KAN | ✅ Sí | `{"key": "KAN"}` |
| **parent** | Object | Link a Epic (solo subtasks) | ✅ En Subtasks | `{"key": "KAN-123"}` |
| **description** | ADF Object | Descripción detallada | ❌ No | Ver formatos arriba |
| **assignee** | Object | Responsable de la tarea | ❌ No | `{"id": "account-id"}` |
| **labels** | Array[String] | Categorización | ❌ No | `["reel", "viaje"]` |
| **priority** | Object | Urgencia de la tarea | ❌ No | `{"name": "High"}` |
| **duedate** | Date (YYYY-MM-DD) | Deadline | ❌ No | `2026-01-15` |
| **reporter** | Object | Quién creó el issue | ✅ Auto | Sistema |

### Campos Personalizados Disponibles (Opcionales)

| Campo Custom | Custom Field ID | Uso Posible | Tipo |
|--------------|----------------|-------------|------|
| **Start date** | customfield_10015 | Fecha de inicio de grabación | Date |
| **Team** | customfield_10001 | Equipo asignado | Select |
| **Flagged** | customfield_10021 | Marcar issues urgentes | Flag |

**Nota**: El proyecto usa campos estándar principalmente. Los campos custom son opcionales.

---

## 🎨 CONVENCIONES DE NOMBRES

### Formato de Summary por Issue Type

#### Epic
```
Patrón: {Emoji} [TIPO_CONTENIDO] {Título Descriptivo}

Emojis:
  🎬 → REEL
  📸 → HISTORIA
  🖼️ → CARRUSEL
  📝 → POST

Ejemplos:
  ✅ 🎬 [REEL] Viaje a Cartagena
  ✅ 📸 [HISTORIA] Receta de arepas
  ✅ 🎬 [REEL] Tips de fotografía móvil
  ✅ 🖼️ [CARRUSEL] Outfit de la semana

  ❌ Crear reel de viaje             (Sin formato)
  ❌ [REEL] cartagena                (Sin emoji, título vago)
  ❌ 🎬 Reel sobre viaje             (Sin [TIPO])
```

#### Subtasks
```
Patrón: {Emoji_Fase} {Nombre_Fase}: {Título del Epic (sin prefijo)}

Emojis por Fase:
  📋 → Preproducción/Planificación
  🎥 → Grabación (Reels)
  📷 → Captura (Historias)
  ✂️ → Edición
  🚀 → Publicación

Ejemplos:
  Epic:     🎬 [REEL] Viaje a Cartagena
  Subtask1: 📋 Preproducción: Viaje a Cartagena
  Subtask2: 🎥 Grabación: Viaje a Cartagena
  Subtask3: ✂️ Edición: Viaje a Cartagena
  Subtask4: 🚀 Publicación: Viaje a Cartagena

  Epic:     📸 [HISTORIA] Receta de arepas
  Subtask1: 📋 Planificación: Receta de arepas
  Subtask2: 📷 Captura: Receta de arepas
  Subtask3: 🚀 Publicación: Receta de arepas
```

### Reglas de Nomenclatura

1. **Capitalización**:
   - Primera letra de cada palabra principal en mayúscula
   - Preposiciones en minúscula (de, a, en)
   - Ejemplo: `Tips de Fotografía Móvil` ✅

2. **Longitud**:
   - Epic: 30-60 caracteres
   - Subtask: 40-80 caracteres
   - Máximo permitido: 255 caracteres

3. **Claridad**:
   - Debe entenderse sin contexto adicional
   - Evitar abreviaciones ambiguas
   - Ser específico pero conciso

4. **Consistencia**:
   - Usar siempre el mismo emoji para el mismo tipo
   - Mantener el formato [TIPO] en Epics
   - Repetir el título del Epic en todas las subtasks

---

## 🔄 FLUJO DE ESTADOS (Status Workflow)

### Estados de Jira por Defecto

Aunque Jira tiene estados configurables, estos son los estados típicos:

```
Epic:
  TODO → IN PROGRESS → DONE

Subtask:
  TODO → IN PROGRESS → DONE
```

### Transiciones Recomendadas

```
Epic creado (TODO)
  ↓
Primera Subtask comienza (Epic → IN PROGRESS)
  ↓
Subtasks se completan secuencialmente
  ↓
Última Subtask completada (Epic → DONE)
```

**Regla**: El Epic se marca DONE solo cuando todas sus Subtasks están DONE.

---

## 📊 EJEMPLO COMPLETO DE WORKFLOW

### Input de Usuario
```
"Crear reel sobre viaje a Cartagena de 30 segundos,
 grabar en las playas, editar con música tropical,
 publicar el viernes próximo, alta prioridad"
```

### Resultado en Jira

#### Epic Creado
```json
{
  "fields": {
    "project": {"key": "KAN"},
    "issuetype": {"name": "Epic"},
    "summary": "🎬 [REEL] Viaje a Cartagena",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [{
            "type": "text",
            "text": "📹 CONTENIDO: Reel vertical de 30 segundos"
          }]
        },
        {
          "type": "paragraph",
          "content": [{
            "type": "text",
            "text": "🎯 OBJETIVO: Mostrar la belleza de las playas de Cartagena"
          }]
        },
        {
          "type": "paragraph",
          "content": [{
            "type": "text",
            "text": "📍 UBICACIÓN: Playas de Cartagena"
          }]
        },
        {
          "type": "paragraph",
          "content": [{
            "type": "text",
            "text": "⏱️ DURACIÓN: 30 segundos"
          }]
        },
        {
          "type": "paragraph",
          "content": [{
            "type": "text",
            "text": "🎨 ESTILO: Música tropical, colores vibrantes"
          }]
        }
      ]
    },
    "labels": ["reel", "viaje", "cartagena", "playa"],
    "duedate": "2026-01-15"
  }
}
```
**Issue Key**: `KAN-50`

#### Subtask 1: Preproducción
```json
{
  "fields": {
    "project": {"key": "KAN"},
    "issuetype": {"name": "Subtask"},
    "parent": {"key": "KAN-50"},
    "summary": "📋 Preproducción: Viaje a Cartagena",
    "description": {...},
    "labels": ["preproduccion", "planificacion"],
    "assignee": null,
    "priority": {"name": "High"}
  }
}
```
**Issue Key**: `KAN-51`

#### Subtask 2: Grabación
```json
{
  "fields": {
    "project": {"key": "KAN"},
    "issuetype": {"name": "Subtask"},
    "parent": {"key": "KAN-50"},
    "summary": "🎥 Grabación: Viaje a Cartagena",
    "description": {...},
    "labels": ["grabacion", "playa", "exterior"],
    "assignee": null,
    "priority": {"name": "High"},
    "duedate": "2026-01-12"
  }
}
```
**Issue Key**: `KAN-52`

#### Subtask 3: Edición
```json
{
  "fields": {
    "project": {"key": "KAN"},
    "issuetype": {"name": "Subtask"},
    "parent": {"key": "KAN-50"},
    "summary": "✂️ Edición: Viaje a Cartagena",
    "description": {...},
    "labels": ["edicion", "video-editing", "sound-design"],
    "assignee": null,
    "priority": {"name": "High"},
    "duedate": "2026-01-14"
  }
}
```
**Issue Key**: `KAN-53`

#### Subtask 4: Publicación
```json
{
  "fields": {
    "project": {"key": "KAN"},
    "issuetype": {"name": "Subtask"},
    "parent": {"key": "KAN-50"},
    "summary": "🚀 Publicación: Viaje a Cartagena",
    "description": {...},
    "labels": ["publicacion", "instagram", "scheduled"],
    "assignee": null,
    "priority": {"name": "Highest"},
    "duedate": "2026-01-15"
  }
}
```
**Issue Key**: `KAN-54`

### Vista en Jira

```
KAN-50  🎬 [REEL] Viaje a Cartagena                [Epic] [TODO]
  ├─ KAN-51  📋 Preproducción: Viaje a Cartagena   [Subtask] [TODO]
  ├─ KAN-52  🎥 Grabación: Viaje a Cartagena       [Subtask] [TODO]
  ├─ KAN-53  ✂️ Edición: Viaje a Cartagena         [Subtask] [TODO]
  └─ KAN-54  🚀 Publicación: Viaje a Cartagena     [Subtask] [TODO]
```

---

## 🔌 INTEGRACIÓN CON API EXISTENTE

### Endpoint Nuevo Propuesto

```
POST /api/v1/reels/workflow/create
```

**Request Body**:
```json
{
  "text": "Crear reel sobre viaje a Cartagena...",
  "project_key": "KAN",
  "content_type": "reel",  // opcional: "reel", "historia", "carrusel"
  "due_date": "2026-01-15",  // opcional
  "assignees": {  // opcional
    "grabacion": "Juan",
    "edicion": "María"
  }
}
```

**Response**:
```json
{
  "success": true,
  "epic": {
    "key": "KAN-50",
    "summary": "🎬 [REEL] Viaje a Cartagena",
    "url": "https://sfg222.atlassian.net/browse/KAN-50"
  },
  "subtasks": [
    {
      "key": "KAN-51",
      "summary": "📋 Preproducción: Viaje a Cartagena",
      "phase": "preproduccion",
      "url": "https://sfg222.atlassian.net/browse/KAN-51"
    },
    {
      "key": "KAN-52",
      "summary": "🎥 Grabación: Viaje a Cartagena",
      "phase": "grabacion",
      "url": "https://sfg222.atlassian.net/browse/KAN-52"
    },
    {
      "key": "KAN-53",
      "summary": "✂️ Edición: Viaje a Cartagena",
      "phase": "edicion",
      "url": "https://sfg222.atlassian.net/browse/KAN-53"
    },
    {
      "key": "KAN-54",
      "summary": "🚀 Publicación: Viaje a Cartagena",
      "phase": "publicacion",
      "url": "https://sfg222.atlassian.net/browse/KAN-54"
    }
  ],
  "total_tasks": 5,
  "parsed_data": {
    "content_type": "reel",
    "title": "Viaje a Cartagena",
    "location": "cartagena",
    "duration": "30 segundos",
    "style": "música tropical",
    "priority": "high",
    "labels": ["reel", "viaje", "cartagena", "playa"]
  }
}
```

### Endpoint de Preview

```
POST /api/v1/reels/workflow/preview
```

Mismo request que `/create` pero NO crea los issues, solo retorna cómo quedarían.

---

## 📝 VARIANTES DEL WORKFLOW

### Variante 1: Reel Completo (4 Subtasks)
```
Epic
  ├─ Preproducción
  ├─ Grabación
  ├─ Edición
  └─ Publicación
```
**Uso**: Proyectos que requieren planificación completa

### Variante 2: Historia Simple (3 Subtasks)
```
Epic
  ├─ Planificación
  ├─ Captura
  └─ Publicación
```
**Uso**: Contenido más espontáneo, menos producción

### Variante 3: Carrusel (3 Subtasks)
```
Epic
  ├─ Diseño
  ├─ Creación de contenido
  └─ Publicación
```
**Uso**: Carruseles informativos o educativos

### Variante 4: Reel Express (2 Subtasks)
```
Epic
  ├─ Grabación y Edición
  └─ Publicación
```
**Uso**: Contenido trending, reacción rápida

---

## 🎯 REGLAS DE ASIGNACIÓN AUTOMÁTICA

### Basado en Fase

| Fase | Rol Sugerido | Criterio |
|------|--------------|----------|
| Preproducción | Productor/Creador | Quien inició el Epic |
| Grabación | Camarógrafo/Creador | Especificado en texto o default |
| Edición | Editor | Especificado en texto o default |
| Publicación | Community Manager | Especificado en texto o default |

### Detección de Asignación en Texto

Patrones regex:
```python
ASSIGN_PATTERNS = {
    "grabacion": [
        r"grabar[alo]? (?:por|con|a) (\w+)",
        r"filmado por (\w+)",
    ],
    "edicion": [
        r"editar (?:por|con|a) (\w+)",
        r"edición a cargo de (\w+)",
    ],
    "publicacion": [
        r"publicar[alo]? (\w+)",
        r"subir[alo]? (\w+)",
    ]
}
```

---

## 📊 MÉTRICAS Y REPORTES

### Métricas por Epic

- **Tiempo total**: Suma de tiempo de todas las subtasks
- **Progreso**: % de subtasks completadas
- **Fecha estimada de finalización**: Due date de última subtask
- **Bloqueos**: Subtasks en estado bloqueado

### Reportes Útiles

1. **Pipeline de Contenido**
   - Filtro: `type = Epic AND labels = reel`
   - Agrupado por: Estado
   - Muestra: Qué reels están en qué fase

2. **Carga de Trabajo por Persona**
   - Filtro: `assignee = currentUser() AND status != Done`
   - Agrupado por: Epic padre
   - Muestra: Qué tareas tiene cada persona

3. **Calendario Editorial**
   - Filtro: `type = Epic AND labels IN (reel, historia)`
   - Vista: Calendario por due date
   - Muestra: Cuándo se publicará cada contenido

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Modelos y Parser
- [ ] Crear `app/models/reel.py` con modelos de datos
- [ ] Crear `app/parsers/reel_parser.py` extendiendo TaskParser
- [ ] Agregar detección de tipo de contenido (reel, historia)
- [ ] Agregar extracción de duración, ubicación, estilo
- [ ] Tests unitarios para ReelParser

### Fase 2: Servicio de Workflow
- [ ] Crear `app/services/reel_workflow_service.py`
- [ ] Implementar `create_reel_workflow()` que cree Epic + Subtasks
- [ ] Implementar lógica de asignación automática
- [ ] Implementar generación de descripciones en ADF
- [ ] Tests de integración con JiraClient mock

### Fase 3: API Endpoints
- [ ] Crear `app/api/routes/reels.py`
- [ ] Endpoint POST `/api/v1/reels/workflow/create`
- [ ] Endpoint POST `/api/v1/reels/workflow/preview`
- [ ] Endpoint GET `/api/v1/reels/workflow/{epic_key}`
- [ ] Validación con Pydantic
- [ ] Documentación en Swagger

### Fase 4: Configuración
- [ ] Agregar variables de configuración en `config.py`
- [ ] Actualizar `.env.example` con nuevas variables
- [ ] Documentar variables en README

### Fase 5: Testing y Docs
- [ ] Tests end-to-end con Jira real
- [ ] Actualizar README con ejemplos de Reels
- [ ] Crear guía de usuario para el workflow
- [ ] Ejemplos de uso en `examples/`

---

## 📚 RECURSOS Y REFERENCIAS

### Jira API
- [REST API v3 - Create Issue](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post)
- [Atlassian Document Format (ADF)](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)

### Instagram Best Practices
- Duración ideal Reels: 7-30 segundos
- Formato: 1080x1920 (9:16 vertical)
- Hashtags: 3-5 relevantes
- Mejor horario: 9am, 12pm, 3pm, 6pm, 9pm

### Herramientas Recomendadas
- Edición: CapCut, Adobe Premiere Rush, InShot
- Planificación: Later, Planoly, Buffer
- Analytics: Instagram Insights, Metricool

---

## 🎓 EJEMPLOS DE USO

### Ejemplo 1: Reel de Viaje
```
Input:
"Crear reel de 30 segundos sobre playas de Cartagena,
grabar atardecer en playa blanca, editar con música reggaeton,
publicar el sábado"

Output en Jira:
Epic: 🎬 [REEL] Playas de Cartagena
  ├─ 📋 Preproducción: Playas de Cartagena
  ├─ 🎥 Grabación: Playas de Cartagena (due: 2 días antes)
  ├─ ✂️ Edición: Playas de Cartagena (due: 1 día antes)
  └─ 🚀 Publicación: Playas de Cartagena (due: sábado)

Labels: ["reel", "viaje", "cartagena", "playa", "atardecer"]
```

### Ejemplo 2: Historia de Comida
```
Input:
"Historia sobre receta de arepas, grabar en cocina,
mostrar paso a paso, publicar mañana"

Output en Jira:
Epic: 📸 [HISTORIA] Receta de arepas
  ├─ 📋 Planificación: Receta de arepas
  ├─ 📷 Captura: Receta de arepas (due: hoy)
  └─ 🚀 Publicación: Receta de arepas (due: mañana)

Labels: ["historia", "comida", "receta", "tutorial"]
```

### Ejemplo 3: Reel Tutorial
```
Input:
"Reel tutorial de fotografía móvil, 5 tips rápidos,
grabar en estudio, alta prioridad, asignar edición a María"

Output en Jira:
Epic: 🎬 [REEL] Tips de fotografía móvil
  ├─ 📋 Preproducción: Tips de fotografía móvil
  ├─ 🎥 Grabación: Tips de fotografía móvil (labels: estudio, interior)
  ├─ ✂️ Edición: Tips de fotografía móvil (assignee: María)
  └─ 🚀 Publicación: Tips de fotografía móvil

Labels: ["reel", "tutorial", "fotografia", "educativo"]
Priority: High
```

---

## 🔍 PREGUNTAS FRECUENTES

### ¿Puedo modificar el workflow después de creado?
Sí, puedes:
- Agregar/eliminar subtasks manualmente en Jira
- Cambiar assignees, fechas, prioridades
- Agregar labels adicionales
- Modificar descripciones

### ¿Qué pasa si no especifico todos los detalles?
El sistema usa valores por defecto:
- Tipo: Reel (si no se especifica)
- Duración: 30 segundos
- Prioridad: Medium
- Sin assignees

### ¿Puedo crear solo algunas fases?
Sí, mediante configuración:
```python
REEL_PHASES = ["grabacion", "edicion", "publicacion"]  # Sin preproducción
```

### ¿El sistema detecta ubicaciones automáticamente?
Sí, tiene un diccionario de ubicaciones comunes en Colombia:
- Cartagena, Bogotá, Medellín, Cali, Santa Marta, etc.

### ¿Cómo manejo revisiones y aprobaciones?
Puedes:
1. Agregar una subtask adicional "Aprobación" entre Edición y Publicación
2. Usar comentarios en la subtask de Edición
3. Usar estados custom de Jira (En Revisión, Aprobado)

---

## 📞 SOPORTE Y CONTRIBUCIONES

Para reportar bugs o sugerir mejoras al workflow:
- Crear issue en el repositorio
- Tag: `enhancement`, `workflow`, `reels`

---

**Última actualización**: 2026-01-08
**Versión del workflow**: 1.0
**Compatible con**: jira-ai-agent v0.1.0
