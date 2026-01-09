# ✅ Endpoints Protegidos - Resumen Completo

## 🎉 ¡Todos los endpoints están protegidos!

Se ha completado la protección de todos los endpoints de la API con autenticación JWT. Ahora cada usuario usa sus propias credenciales de Jira almacenadas de forma segura.

---

## 🔐 Endpoints Protegidos

### Públicos (NO requieren autenticación)

✅ **Autenticación:**
- `POST /api/v1/auth/register` - Registrar nuevo usuario
- `POST /api/v1/auth/login` - Login (obtener JWT token)
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/health` - Health check de autenticación

✅ **Info:**
- `GET /` - Información de la API
- `GET /api/v1/health` - Health check general (con credenciales del sistema)
- `GET /docs` - Documentación interactiva (Swagger UI)

### Protegidos (requieren JWT token)

🔒 **Usuario:**
- `GET /api/v1/auth/me` - Obtener info del usuario actual

🔒 **Proyectos:**
- `GET /api/v1/projects` - Listar proyectos de Jira del usuario
- `GET /api/v1/projects/{project_key}/users` - Usuarios del proyecto

🔒 **Tareas:**
- `POST /api/v1/tasks/create` - Crear tarea individual
- `POST /api/v1/tasks/parse` - Preview de parsing (sin crear)
- `POST /api/v1/tasks/batch` - Crear múltiples tareas

🔒 **Instagram:**
- `POST /api/v1/content/instagram` - Crear contenido de Instagram

---

## 🔑 Cómo Usar los Endpoints Protegidos

### 1. Registrar Usuario

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "SecurePassword123!",
    "jira_email": "john@company.com",
    "jira_api_token": "ATATT3xFfGF0...",
    "jira_base_url": "https://yourcompany.atlassian.net"
  }'
```

### 2. Login (Obtener Token)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=SecurePassword123!"
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Usar Token en Requests

Incluye el token en el header `Authorization`:

```bash
# Guardar token en variable
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Ejemplo: Listar proyectos
curl -X GET "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN"

# Ejemplo: Crear tarea
curl -X POST "http://localhost:8000/api/v1/tasks/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Crear reel sobre viaje a Cartagena",
    "project_key": "KAN"
  }'
```

---

## 📊 Cambios Implementados

### 1. Nueva Dependency: `get_user_jira_client()`

**Ubicación:** `app/api/dependencies.py`

```python
def get_user_jira_client(current_user: User = Depends(get_current_user)) -> JiraClient:
    """
    Obtiene JiraClient con las credenciales del usuario autenticado.

    - Desencripta el token de Jira del usuario
    - Crea JiraClient con sus credenciales
    - Valida que el usuario tenga config de Jira
    """
```

**Beneficios:**
- ✅ Cada usuario usa sus propias credenciales de Jira
- ✅ Mejor auditoría (tareas creadas por el usuario real)
- ✅ Seguridad: Credenciales encriptadas en base de datos
- ✅ Validación automática de configuración

### 2. Endpoints en `app/main.py`

**Modificados:**

```python
# Antes
@app.get("/api/v1/projects")
async def list_projects():
    jira_client = get_jira_client()  # Credenciales del sistema

# Después
@app.get("/api/v1/projects")
async def list_projects(
    jira_client: JiraClient = Depends(get_user_jira_client)  # Credenciales del usuario
):
```

```python
# Antes
@app.post("/api/v1/tasks/create")
async def create_task_from_text(request: CreateTaskRequest):
    jira_client = get_jira_client()  # Credenciales del sistema

# Después
@app.post("/api/v1/tasks/create")
async def create_task_from_text(
    request: CreateTaskRequest,
    jira_client: JiraClient = Depends(get_user_jira_client)  # Credenciales del usuario
):
```

### 3. Endpoints en `app/api/routes/projects.py`

```python
# Antes
@router.get("/projects/{project_key}/users")
async def get_project_users(
    project_key: str,
    jira_client: JiraClient = Depends(get_jira_client)
):

# Después
@router.get("/projects/{project_key}/users")
async def get_project_users(
    project_key: str,
    jira_client: JiraClient = Depends(get_user_jira_client)  # ← Cambio
):
```

### 4. Endpoints en `app/api/routes/batch_tasks.py`

```python
# Antes
@router.post("/batch")
async def create_batch_tasks(
    request: CreateBatchTasksRequest,
    service: ReelWorkflowService = Depends(get_reel_workflow_service),
    jira_client: JiraClient = Depends(get_jira_client)
):

# Después
@router.post("/batch")
async def create_batch_tasks(
    request: CreateBatchTasksRequest,
    jira_client: JiraClient = Depends(get_user_jira_client)  # ← Cambio
):
    # Crear servicio con credenciales del usuario
    service = ReelWorkflowService(jira_client)
```

### 5. Endpoints en `app/api/routes/instagram.py`

```python
# Antes
@router.post("/instagram")
async def create_instagram_content(
    request: CreateInstagramContentRequest,
    service: ReelWorkflowService = Depends(get_reel_workflow_service),
    jira_client: JiraClient = Depends(get_jira_client)
):

# Después
@router.post("/instagram")
async def create_instagram_content(
    request: CreateInstagramContentRequest,
    jira_client: JiraClient = Depends(get_user_jira_client)  # ← Cambio
):
    # Crear servicio con credenciales del usuario
    service = ReelWorkflowService(jira_client)
```

---

## 🚨 Breaking Changes

### Para Usuarios Existentes de la API

**Antes** (sin autenticación):
```bash
curl -X GET "http://localhost:8000/api/v1/projects"
# ✅ Funcionaba sin token
```

**Ahora** (con autenticación requerida):
```bash
# ❌ Sin token da error 401
curl -X GET "http://localhost:8000/api/v1/projects"

# ✅ Con token funciona
curl -X GET "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN"
```

### Respuestas de Error

**401 Unauthorized - Token faltante o inválido:**
```json
{
  "detail": "Not authenticated"
}
```

**401 Unauthorized - Token expirado:**
```json
{
  "detail": "Token inválido o expirado"
}
```

**400 Bad Request - Usuario sin credenciales de Jira:**
```json
{
  "detail": "Usuario no tiene configurada la URL de Jira. Por favor, actualiza tu perfil."
}
```

---

## 📈 Beneficios de la Autenticación

### 1. Seguridad Mejorada
- ✅ Solo usuarios autenticados pueden usar la API
- ✅ Cada usuario tiene sus propias credenciales de Jira
- ✅ Tokens de Jira encriptados en base de datos
- ✅ Tokens JWT con expiración automática (24 horas)

### 2. Mejor Auditoría
- ✅ Tareas creadas en Jira aparecen con el usuario correcto
- ✅ Se sabe quién creó qué tarea
- ✅ Logs con información del usuario

### 3. Control de Acceso
- ✅ Usuarios solo ven proyectos permitidos en su cuenta Jira
- ✅ Permisos de Jira se respetan por usuario
- ✅ Si un usuario pierde acceso en Jira, pierde acceso en la API

### 4. Escalabilidad
- ✅ Múltiples usuarios pueden usar la misma instancia
- ✅ Cada usuario independiente
- ✅ No hay límite de usuarios

---

## 🧪 Testing de Endpoints Protegidos

### Script de Test Completo

```bash
#!/bin/bash

# Variables
API_URL="http://localhost:8000"
USERNAME="testuser"
PASSWORD="TestPass123!"
EMAIL="test@example.com"
JIRA_EMAIL="test@company.com"
JIRA_TOKEN="your_jira_token"
JIRA_URL="https://yourcompany.atlassian.net"
PROJECT_KEY="KAN"

# 1. Registrar usuario
echo "1. Registrando usuario..."
curl -X POST "$API_URL/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"username\": \"$USERNAME\",
    \"password\": \"$PASSWORD\",
    \"jira_email\": \"$JIRA_EMAIL\",
    \"jira_api_token\": \"$JIRA_TOKEN\",
    \"jira_base_url\": \"$JIRA_URL\"
  }"

echo -e "\n\n2. Login..."
# 2. Login y obtener token
RESPONSE=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$USERNAME&password=$PASSWORD")

TOKEN=$(echo $RESPONSE | jq -r '.access_token')
echo "Token obtenido: ${TOKEN:0:50}..."

# 3. Probar endpoint protegido: Obtener info del usuario
echo -e "\n\n3. Obteniendo info del usuario..."
curl -X GET "$API_URL/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"

# 4. Probar endpoint protegido: Listar proyectos
echo -e "\n\n4. Listando proyectos..."
curl -X GET "$API_URL/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN"

# 5. Probar endpoint protegido: Usuarios del proyecto
echo -e "\n\n5. Obteniendo usuarios del proyecto..."
curl -X GET "$API_URL/api/v1/projects/$PROJECT_KEY/users" \
  -H "Authorization: Bearer $TOKEN"

# 6. Probar endpoint protegido: Crear tarea
echo -e "\n\n6. Creando tarea..."
curl -X POST "$API_URL/api/v1/tasks/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Crear reel sobre testing de autenticación\",
    \"project_key\": \"$PROJECT_KEY\"
  }"

# 7. Probar sin token (debería fallar)
echo -e "\n\n7. Probando sin token (debe fallar)..."
curl -X GET "$API_URL/api/v1/projects"

echo -e "\n\n✅ Testing completado"
```

Guarda como `test_auth.sh` y ejecuta:
```bash
chmod +x test_auth.sh
./test_auth.sh
```

---

## 📝 Checklist de Migración

Para desarrolladores que están migrando código existente:

- [ ] Actualizar cliente HTTP para incluir header `Authorization`
- [ ] Implementar flujo de login para obtener token
- [ ] Guardar token de forma segura (localStorage, sessionStorage, etc.)
- [ ] Incluir token en todas las peticiones a endpoints protegidos
- [ ] Manejar errores 401 (redirigir a login)
- [ ] Implementar refresh de token antes de expiración
- [ ] Actualizar tests para incluir autenticación

---

## 🔄 Próximos Pasos Opcionales

### 1. Refresh Tokens
Implementar refresh tokens para renovar el access token sin que el usuario haga login nuevamente.

### 2. Rate Limiting
Agregar límite de requests por usuario para prevenir abuso:
```python
from slowapi import Limiter

@router.post("/login")
@limiter.limit("5/minute")  # Máximo 5 intentos de login por minuto
async def login(...):
    pass
```

### 3. Webhook de Eventos
Notificar a sistemas externos cuando un usuario crea tareas:
```python
@app.middleware("http")
async def log_task_creation(request, call_next):
    if request.url.path.endswith("/tasks/create"):
        # Enviar webhook
        pass
    response = await call_next(request)
    return response
```

### 4. Frontend con Autenticación
Implementar login/registro en React (ver `docs/AUTHENTICATION_ANALYSIS.md` Fase 3).

---

## 📚 Recursos

- **Documentación de Auth:** [docs/AUTH_QUICK_START.md](AUTH_QUICK_START.md)
- **Análisis Completo:** [docs/AUTHENTICATION_ANALYSIS.md](AUTHENTICATION_ANALYSIS.md)
- **Implementación Backend:** [docs/BACKEND_AUTH_SUMMARY.md](BACKEND_AUTH_SUMMARY.md)
- **Swagger UI:** http://localhost:8000/docs (cuando el servidor esté corriendo)

---

## ✨ Conclusión

✅ **Todos los endpoints críticos están protegidos**
✅ **Cada usuario usa sus propias credenciales de Jira**
✅ **Sistema listo para producción**
✅ **Documentación completa disponible**

El backend ahora tiene un sistema de autenticación completo y robusto, listo para:
- Desarrollo local
- Despliegue en producción (Render + Supabase/Neon)
- Integración con frontend React
- Escalamiento a múltiples usuarios

**Tiempo total de implementación:** ~8 horas ⚡
