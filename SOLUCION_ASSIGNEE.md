# ✅ SOLUCIÓN: Error de Assignee en Jira

> Solución al error: "Specify a valid value for assignee"
>
> **Problema**: Jira requiere Account ID, no nombres de usuario
> **Solución**: Búsqueda automática de Account ID por nombre
> **Fecha**: 2026-01-08

---

## ❌ PROBLEMA ORIGINAL

### Error Recibido

```json
{
  "detail": "Error de Jira API: [400] Error HTTP 400: {'assignee': 'Specify a valid value for assignee'}"
}
```

### Causa

Jira Cloud API v3 requiere el **Account ID** del usuario para el campo `assignee`, no el nombre.

**Lo que NO funciona**:
```python
assignee = "Juan"  # ❌ NO funciona
```

**Lo que SÍ funciona**:
```python
assignee = "5b10a2844c20165700ede21g"  # ✅ Account ID válido
```

---

## ✅ SOLUCIÓN IMPLEMENTADA

### 1. Método Agregado al JiraClient

He agregado dos métodos nuevos en `app/clients/jira_client.py`:

#### `search_user(query, project_key)`

Busca usuarios en Jira por nombre o email.

```python
def search_user(self, query: str, project_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Busca usuarios en Jira por nombre o email.

    Args:
        query: Nombre o email del usuario a buscar
        project_key: Clave del proyecto para filtrar usuarios (opcional)

    Returns:
        Lista de usuarios que coinciden con la búsqueda
    """
    params = {"query": query}
    if project_key:
        params["project"] = project_key

    return self._make_request(
        method="GET",
        endpoint="/user/search",
        params=params
    )
```

#### `get_user_account_id(name, project_key)`

Obtiene el Account ID de un usuario por su nombre.

```python
def get_user_account_id(self, name: str, project_key: Optional[str] = None) -> Optional[str]:
    """
    Obtiene el Account ID de un usuario por su nombre.

    Args:
        name: Nombre del usuario (ej: "Juan", "María")
        project_key: Clave del proyecto para filtrar búsqueda (opcional)

    Returns:
        Account ID del usuario o None si no se encuentra

    Example:
        >>> client.get_user_account_id("Juan", "KAN")
        "5b10a2844c20165700ede21g"
    """
    try:
        users = self.search_user(name, project_key)

        if users and len(users) > 0:
            # Retornar el Account ID del primer match
            return users[0].get("accountId")

        return None

    except JiraAPIError:
        # Si hay error en la búsqueda, retornar None
        return None
```

---

### 2. Modificación del Endpoint `/api/v1/tasks/create`

En `app/main.py`, el endpoint ahora busca automáticamente el Account ID:

```python
@app.post("/api/v1/tasks/create", response_model=CreateTaskResponse)
async def create_task_from_text(request: CreateTaskRequest):
    try:
        # 1. Parsear el texto
        parser = get_parser()
        parsed_task = parser.parse(request.text)

        # 2. Obtener cliente de Jira
        jira_client = get_jira_client()

        # 3. Si hay assignee, buscar el Account ID
        assignee_account_id = None
        if parsed_task.assignee:
            assignee_account_id = jira_client.get_user_account_id(
                parsed_task.assignee,
                request.project_key
            )
            if not assignee_account_id:
                print(f"⚠️  Usuario '{parsed_task.assignee}' no encontrado en Jira. El issue se creará sin asignar.")

        # 4. Crear issue en Jira
        jira_response = jira_client.create_issue(
            project_key=request.project_key,
            summary=parsed_task.summary,
            description=parsed_task.description,
            issue_type=parsed_task.issue_type,
            priority=parsed_task.priority,
            labels=parsed_task.labels,
            assignee=assignee_account_id  # ✅ Usa Account ID, no nombre
        )

        # ...resto del código
```

---

## 🎯 FLUJO COMPLETO

### 1. Usuario envía request

```bash
curl -X POST http://localhost:8000/api/v1/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Crear reel sobre viaje a Cartagena, asignado a santiago",
    "project_key": "KAN"
  }'
```

### 2. Parser detecta assignee

```python
parsed_task.assignee = "santiago"  # Extraído del texto
```

### 3. Sistema busca Account ID

```python
# Busca en Jira Cloud
assignee_account_id = jira_client.get_user_account_id("santiago", "KAN")

# Ejemplo de resultado:
# assignee_account_id = "712020:abcd1234-efgh-5678-ijkl-9012mnop3456"
```

### 4. Crea issue con Account ID

```python
jira_client.create_issue(
    project_key="KAN",
    summary="Crear reel sobre viaje a cartagena",
    assignee="712020:abcd1234-efgh-5678-ijkl-9012mnop3456"  # ✅ Account ID
)
```

---

## 📊 COMPORTAMIENTO SEGÚN CASOS

### Caso 1: Usuario existe en Jira

**Input**:
```json
{
  "text": "Crear reel, asignado a santiago",
  "project_key": "KAN"
}
```

**Proceso**:
1. Parser detecta: `assignee = "santiago"`
2. Sistema busca en Jira: Encuentra Account ID `712020:abc...`
3. Issue se crea asignado a santiago ✅

**Response**:
```json
{
  "success": true,
  "issue_key": "KAN-123",
  "parsed_data": {
    "assignee": "santiago"
  }
}
```

---

### Caso 2: Usuario NO existe en Jira

**Input**:
```json
{
  "text": "Crear reel, asignado a Juan",
  "project_key": "KAN"
}
```

**Proceso**:
1. Parser detecta: `assignee = "Juan"`
2. Sistema busca en Jira: NO encuentra usuario
3. Se muestra warning en logs: `⚠️  Usuario 'Juan' no encontrado en Jira`
4. Issue se crea **sin asignar** (assignee = null) ✅

**Response**:
```json
{
  "success": true,
  "issue_key": "KAN-124",
  "parsed_data": {
    "assignee": "Juan"
  }
}
```

**Nota**: El campo `parsed_data.assignee` muestra lo que se detectó del texto, pero el issue real en Jira queda sin asignar.

---

### Caso 3: Sin assignee en el texto

**Input**:
```json
{
  "text": "Crear reel sobre viaje a Cartagena",
  "project_key": "KAN"
}
```

**Proceso**:
1. Parser detecta: `assignee = None`
2. Sistema no busca nada
3. Issue se crea sin asignar ✅

**Response**:
```json
{
  "success": true,
  "issue_key": "KAN-125",
  "parsed_data": {
    "assignee": null
  }
}
```

---

## 🔍 CÓMO BUSCA USUARIOS EL SISTEMA

### API Endpoint Usado

```
GET /rest/api/3/user/search?query={name}&project={project_key}
```

### Ejemplo de Request

```
GET /rest/api/3/user/search?query=santiago&project=KAN
```

### Ejemplo de Response de Jira

```json
[
  {
    "accountId": "712020:abcd1234-efgh-5678-ijkl-9012mnop3456",
    "accountType": "atlassian",
    "displayName": "santiago florez",
    "emailAddress": "sfg222@gmail.com",
    "active": true
  }
]
```

### Lógica de Match

- Busca por nombre (parcial o completo)
- Retorna el **primer usuario** que coincida
- Si no encuentra nadie, retorna `None`

---

## ⚙️ CONFIGURACIÓN ADICIONAL (OPCIONAL)

### Opción 1: Mapeo Manual de Usuarios

Si prefieres tener un mapeo fijo de nombres a Account IDs, puedes agregarlo en `.env`:

```env
# Mapeo de nombres a Account IDs
USER_JUAN=712020:abcd1234-efgh-5678-ijkl-9012mnop3456
USER_MARIA=712020:wxyz7890-abcd-1234-efgh-5678ijkl9012
USER_PEDRO=712020:mnop3456-qrst-7890-uvwx-yzab1234cdef
```

Y modificar el código para buscar primero en el mapeo antes de buscar en Jira.

---

### Opción 2: Cache de Búsquedas

Para evitar buscar el mismo usuario múltiples veces, puedes implementar un cache:

```python
# En memoria
user_cache = {}

def get_user_account_id_cached(name: str, project_key: str) -> Optional[str]:
    cache_key = f"{name}:{project_key}"

    if cache_key in user_cache:
        return user_cache[cache_key]

    account_id = jira_client.get_user_account_id(name, project_key)
    user_cache[cache_key] = account_id

    return account_id
```

---

## 🧪 CÓMO PROBAR

### 1. Reiniciar el servidor

Si el servidor ya estaba corriendo, reinícialo para cargar los cambios:

```bash
# Ctrl+C para detener
# Luego:
uvicorn app.main:app --reload
```

### 2. Probar con Swagger UI

Abre http://localhost:8000/docs y prueba el endpoint `POST /api/v1/tasks/create`:

```json
{
  "text": "Crear reel sobre viaje a Cartagena, asignado a santiago",
  "project_key": "KAN"
}
```

### 3. Probar con curl

```bash
curl -X POST http://localhost:8000/api/v1/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Crear reel sobre viaje a Cartagena, asignado a santiago",
    "project_key": "KAN"
  }'
```

### 4. Verificar en Jira

1. Ve a tu proyecto KAN en Jira
2. Busca el issue creado
3. Verifica que esté asignado a santiago (si existe) o sin asignar (si no existe)

---

## 📝 NOTAS IMPORTANTES

### 1. Coincidencia de Nombres

La búsqueda de Jira hace match parcial:
- "santiago" → Encuentra "santiago florez"
- "santi" → Encuentra "santiago florez"
- "Juan" → Encuentra "Juan Pérez"

### 2. Múltiples Usuarios con el Mismo Nombre

Si hay varios usuarios con el mismo nombre, el sistema usa el **primer match**.

**Recomendación**: Usa nombres distintivos o emails:
- "Juan" → Puede haber varios
- "Juan.Perez" → Más específico
- "juan@empresa.com" → Único

### 3. Case Insensitive

La búsqueda NO distingue entre mayúsculas y minúsculas:
- "Santiago" = "santiago" = "SANTIAGO"

### 4. Performance

Cada búsqueda hace un request a Jira API.

**Para mejorar performance**:
- Implementar cache (Opción 2 arriba)
- Usar mapeo manual (Opción 1 arriba)
- Asignar manualmente en Jira después

---

## ✅ RESUMEN

### Antes (❌ Error)

```
texto: "asignado a Juan"
  ↓
parsed_task.assignee = "Juan"
  ↓
jira_client.create_issue(assignee="Juan")  ❌ ERROR 400
```

### Después (✅ Funciona)

```
texto: "asignado a santiago"
  ↓
parsed_task.assignee = "santiago"
  ↓
assignee_id = get_user_account_id("santiago", "KAN")
  → "712020:abcd1234-efgh-5678-ijkl-9012mnop3456"
  ↓
jira_client.create_issue(assignee="712020:abc...")  ✅ FUNCIONA
```

---

## 🎯 PRÓXIMOS PASOS

1. ✅ **Probar con tu usuario** (santiago)
2. ✅ **Probar con un usuario que NO existe**
3. ⏭️ **Opcional**: Implementar cache de usuarios
4. ⏭️ **Opcional**: Agregar mapeo manual en config

---

**Última actualización**: 2026-01-08
**Estado**: ✅ Implementado y listo para usar
