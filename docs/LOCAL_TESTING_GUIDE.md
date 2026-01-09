# 🧪 Guía de Testing Local - Sistema de Autenticación

Esta guía te ayudará a probar el sistema de autenticación completo en tu máquina local.

---

## 📋 Pre-requisitos

- [x] Python 3.9 o superior instalado
- [x] Credenciales de Jira (email, API token, URL)
- [x] `jq` instalado para pretty-print JSON (opcional pero recomendado)

```bash
# Instalar jq (opcional)
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq
```

---

## 🚀 Paso 1: Configurar Variables de Entorno

### 1.1 Copiar archivo de ejemplo

```bash
cp .env.example .env
```

### 1.2 Generar claves de seguridad

```bash
# Generar JWT_SECRET_KEY
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))" >> .env

# Generar ENCRYPTION_KEY
python3 -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())" >> .env
```

### 1.3 Editar .env con tus credenciales de Jira

Abre `.env` y configura estas variables (solo para testing local):

```bash
# Estas son tus credenciales personales para probar
JIRA_BASE_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=tu-email@company.com
JIRA_API_TOKEN=tu_token_de_jira

# Database (SQLite para local)
DATABASE_URL=sqlite:///./jira_agent.db
```

**Nota:** Estas credenciales en `.env` son solo para el health check del sistema. Los usuarios registrados usarán sus propias credenciales.

---

## 📦 Paso 2: Instalar Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

Dependencias principales que se instalarán:
- `fastapi` - Framework web
- `sqlalchemy` - ORM para base de datos
- `python-jose` - JWT tokens
- `passlib` - Hashing de contraseñas
- `cryptography` - Encriptación de tokens Jira

---

## 🗄️ Paso 3: Inicializar Base de Datos

```bash
python -m app.core.init_db
```

El script te pedirá:

```
¿Deseas crear un usuario administrador? (s/n): s

📝 Ingresa los datos del usuario administrador:

  Username: admin
  Email: admin@example.com
  Password: [tu password seguro]
  Confirmar password: [tu password seguro]

📝 Ingresa las credenciales de Jira:

  Jira Email: tu-email@company.com
  Jira API Token: [tu token de Jira]
  Jira Base URL: https://yourcompany.atlassian.net
```

Esto creará:
- ✅ Archivo `jira_agent.db` (base de datos SQLite)
- ✅ Tabla `users` con el esquema completo
- ✅ Usuario administrador inicial

---

## ▶️ Paso 4: Iniciar el Servidor

```bash
uvicorn app.main:app --reload
```

Deberías ver:

```
======================================================================
  JIRA AI AGENT - Starting...
======================================================================
✓ Variables de entorno configuradas correctamente

✓ Servidor iniciado
  - Health check: http://localhost:8000/api/v1/health
  - Docs: http://localhost:8000/docs
======================================================================
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **El servidor está corriendo en http://localhost:8000**

---

## 🧪 Paso 5: Probar con Swagger UI (Recomendado)

La forma más fácil de probar es usando la documentación interactiva:

### 5.1 Abrir Swagger UI

Abre en tu navegador: **http://localhost:8000/docs**

### 5.2 Probar Registro

1. Expande `POST /api/v1/auth/register`
2. Click en "Try it out"
3. Edita el JSON con tus datos:

```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "TestPassword123!",
  "jira_email": "tu-email@company.com",
  "jira_api_token": "ATATT3xFfGF0...",
  "jira_base_url": "https://yourcompany.atlassian.net"
}
```

4. Click "Execute"
5. Deberías ver respuesta **201 Created**

### 5.3 Probar Login

1. Expande `POST /api/v1/auth/login`
2. Click en "Try it out"
3. Ingresa:
   - `username`: testuser
   - `password`: TestPassword123!
4. Click "Execute"
5. Copia el `access_token` de la respuesta

### 5.4 Autorizar Requests

1. Scroll hasta arriba
2. Click en el botón **"Authorize"** 🔒
3. Pega el token en el campo `Value`
4. Click "Authorize"
5. Click "Close"

**¡Ahora todos los endpoints protegidos funcionarán!**

### 5.5 Probar Endpoints Protegidos

Ahora puedes probar cualquier endpoint:
- `GET /api/v1/projects` - Ver tus proyectos de Jira
- `GET /api/v1/projects/{project_key}/users` - Ver usuarios del proyecto
- `POST /api/v1/tasks/create` - Crear tarea
- `POST /api/v1/content/instagram` - Crear contenido de Instagram

---

## 🔧 Paso 6: Probar con cURL (Alternativa)

Si prefieres usar la terminal:

### 6.1 Registrar Usuario

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPassword123!",
    "jira_email": "tu-email@company.com",
    "jira_api_token": "ATATT3xFfGF0...",
    "jira_base_url": "https://yourcompany.atlassian.net"
  }'
```

### 6.2 Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=TestPassword123!"
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 6.3 Guardar Token

```bash
# Guardar token en variable
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 6.4 Probar Endpoint Protegido

```bash
# Listar proyectos
curl -X GET "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🤖 Paso 7: Usar Script de Testing Automatizado

Hemos creado un script que prueba todos los endpoints automáticamente:

### 7.1 Configurar Variables

```bash
# Exportar tus credenciales de Jira
export JIRA_EMAIL="tu-email@company.com"
export JIRA_TOKEN="ATATT3xFfGF0..."
export JIRA_URL="https://yourcompany.atlassian.net"
export PROJECT_KEY="KAN"  # O el key de tu proyecto
```

### 7.2 Ejecutar Script

```bash
./test_auth_endpoints.sh
```

El script probará:
1. ✅ Health checks
2. ✅ Registro de usuario
3. ✅ Login
4. ✅ Obtener info del usuario
5. ✅ Request sin token (debe fallar)
6. ✅ Listar proyectos
7. ✅ Usuarios del proyecto
8. ✅ Crear tarea individual
9. ✅ Crear contenido Instagram
10. ✅ Batch de tareas
11. ✅ Logout

---

## ✅ Verificación

### Verificar que todo funciona:

1. **Base de datos creada:**
   ```bash
   ls -lh jira_agent.db
   # Debería mostrar el archivo
   ```

2. **Usuario registrado:**
   ```bash
   sqlite3 jira_agent.db "SELECT id, username, email, is_active FROM users;"
   # Debería mostrar tu usuario
   ```

3. **Health check:**
   ```bash
   curl http://localhost:8000/api/v1/health
   # Debería retornar: {"status":"healthy","jira_connection":"ok"...}
   ```

4. **Documentación:**
   Abre http://localhost:8000/docs y verifica que ves todos los endpoints

---

## 🐛 Troubleshooting

### Error: "Import 'sqlalchemy' could not be resolved"

```bash
pip install sqlalchemy alembic
```

### Error: "Invalid ENCRYPTION_KEY"

Genera una nueva:
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Agrégala al `.env`:
```
ENCRYPTION_KEY=nueva_key_generada_aqui
```

### Error: "Token inválido o expirado"

El token expira después de 24 horas. Haz login nuevamente:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=testuser&password=TestPassword123!"
```

### Error: "Usuario no tiene configurado el token de Jira"

Verifica que registraste el usuario con todas las credenciales de Jira:
- `jira_email`
- `jira_api_token`
- `jira_base_url`

### Server no inicia

```bash
# Verificar que el puerto 8000 no esté en uso
lsof -ti:8000

# Si está en uso, matar el proceso
kill -9 $(lsof -ti:8000)

# O usa otro puerto
uvicorn app.main:app --reload --port 8001
```

### Base de datos corrupta

```bash
# Eliminar y recrear
rm jira_agent.db
python -m app.core.init_db
```

---

## 📊 Verificar Tareas en Jira

Después de crear tareas con la API, verifica en Jira:

1. Abre tu instancia de Jira
2. Ve al proyecto que usaste (ej: KAN)
3. Verifica que las tareas aparezcan con tu nombre como creador

---

## 🎯 Próximos Pasos

Una vez que todo funcione localmente:

1. **✅ Local testing completado**
2. **→ Desplegar a producción** (Render + Supabase)
3. **→ Implementar frontend** (React con auth)
4. **→ Agregar features adicionales** (refresh tokens, etc.)

---

## 📚 Recursos Adicionales

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Guía de Auth:** [AUTH_QUICK_START.md](AUTH_QUICK_START.md)
- **Endpoints Protegidos:** [PROTECTED_ENDPOINTS_SUMMARY.md](PROTECTED_ENDPOINTS_SUMMARY.md)
- **Análisis Completo:** [AUTHENTICATION_ANALYSIS.md](AUTHENTICATION_ANALYSIS.md)

---

¡Feliz testing! 🚀
