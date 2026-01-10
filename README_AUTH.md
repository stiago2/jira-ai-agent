# 🔐 Sistema de Autenticación - Jira AI Agent

Sistema completo de autenticación JWT implementado para el backend de Jira AI Agent.

---

## ⚡ Quick Start

```bash
# 1. Configurar entorno
cp .env.example .env
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))" >> .env
python3 -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())" >> .env

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Inicializar base de datos
python -m app.core.init_db

# 4. Iniciar servidor
uvicorn app.main:app --reload

# 5. Probar en Swagger UI
open http://localhost:8000/docs
```

---

## 🎯 ¿Qué se Implementó?

### Sistema Completo de Autenticación

- ✅ **JWT Tokens** - Autenticación stateless con expiración automática
- ✅ **Base de Datos** - SQLAlchemy con soporte SQLite/PostgreSQL
- ✅ **Encriptación** - Credenciales de Jira encriptadas con Fernet
- ✅ **Endpoints Protegidos** - Todos los endpoints requieren autenticación
- ✅ **Credenciales por Usuario** - Cada usuario usa sus propias credenciales de Jira

### Beneficios

1. **Seguridad** 🔒
   - Contraseñas hasheadas con bcrypt
   - Tokens de Jira encriptados en base de datos
   - JWT con expiración automática (24h)
   - Validación en cada request

2. **Auditoría** 📊
   - Tareas en Jira aparecen con el usuario correcto
   - Logs de quién creó qué
   - Trazabilidad completa

3. **Control de Acceso** 👥
   - Usuarios solo ven sus proyectos de Jira
   - Permisos de Jira respetados por usuario
   - Aislamiento de credenciales

---

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| **[LOCAL_TESTING_GUIDE.md](docs/LOCAL_TESTING_GUIDE.md)** | Guía paso a paso para probar localmente |
| **[PROTECTED_ENDPOINTS_SUMMARY.md](docs/PROTECTED_ENDPOINTS_SUMMARY.md)** | Lista de todos los endpoints protegidos |
| **[AUTH_QUICK_START.md](docs/AUTH_QUICK_START.md)** | Guía rápida para desarrolladores |
| **[BACKEND_AUTH_SUMMARY.md](docs/BACKEND_AUTH_SUMMARY.md)** | Resumen de implementación del backend |
| **[AUTHENTICATION_ANALYSIS.md](docs/AUTHENTICATION_ANALYSIS.md)** | Análisis completo (32 páginas) |

---

## 🔑 Endpoints

### Públicos (No requieren autenticación)

```
POST /api/v1/auth/register   - Registrar usuario
POST /api/v1/auth/login      - Login (obtener token)
POST /api/v1/auth/logout     - Logout
GET  /api/v1/auth/health     - Health check
GET  /api/v1/health          - Health check general
GET  /docs                   - Documentación Swagger
```

### Protegidos (Requieren JWT token)

```
GET  /api/v1/auth/me                        - Info del usuario actual
GET  /api/v1/projects                       - Lista de proyectos
GET  /api/v1/projects/{key}/users          - Usuarios del proyecto
POST /api/v1/tasks/create                   - Crear tarea
POST /api/v1/tasks/batch                    - Crear múltiples tareas
POST /api/v1/content/instagram              - Crear contenido Instagram
```

---

## 🧪 Testing

### Opción 1: Swagger UI (Recomendado)

```bash
# Iniciar servidor
uvicorn app.main:app --reload

# Abrir en navegador
open http://localhost:8000/docs
```

### Opción 2: Script Automatizado

```bash
# Configurar credenciales
export JIRA_EMAIL="tu-email@company.com"
export JIRA_TOKEN="tu_token_jira"
export JIRA_URL="https://yourcompany.atlassian.net"

# Ejecutar tests
./test_auth_endpoints.sh
```

### Opción 3: cURL Manual

```bash
# 1. Registrar
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

# 2. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=testuser&password=TestPassword123!"

# 3. Usar token
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🗄️ Base de Datos

### Desarrollo (SQLite)
```bash
DATABASE_URL=sqlite:///./jira_agent.db
```

### Producción (PostgreSQL)

**Supabase (Recomendado - Gratis):**
```bash
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
```

**Neon:**
```bash
DATABASE_URL=postgresql://user:pass@host.region.neon.tech/dbname
```

---

## 🚀 Despliegue en Render

### 1. Backend (Ya desplegado)
URL: `https://jira-ai-agent.onrender.com`

### 2. Agregar Variables de Entorno

En el dashboard de Render, agregar:

```bash
# Seguridad (REQUERIDO)
JWT_SECRET_KEY=<genera-con-secrets.token_urlsafe>
ENCRYPTION_KEY=<genera-con-Fernet.generate_key>

# Base de Datos (REQUERIDO)
DATABASE_URL=postgresql://postgres:...@db.xxx.supabase.co:5432/postgres

# Configuración
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 3. Generar Claves

```bash
# JWT Secret
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Encryption Key
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 4. Inicializar BD en Producción

```bash
# Conectar a Render shell
# O ejecutar localmente con DATABASE_URL de producción
python -m app.core.init_db
```

---

## 📖 Uso del Sistema

### Flujo de Autenticación

```mermaid
sequenceDiagram
    User->>Frontend: Ingresa credenciales
    Frontend->>Backend: POST /auth/login
    Backend->>Database: Verificar usuario
    Database-->>Backend: Usuario válido
    Backend->>Backend: Generar JWT
    Backend-->>Frontend: Token JWT
    Frontend->>Backend: GET /projects (+ token)
    Backend->>Backend: Validar token
    Backend->>Backend: Desencriptar creds Jira
    Backend->>Jira API: Request con creds del usuario
    Jira API-->>Backend: Proyectos
    Backend-->>Frontend: Proyectos
```

### Arquitectura

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│              (React + Auth Context)              │
└────────────────────┬────────────────────────────┘
                     │ JWT Token
                     ▼
┌─────────────────────────────────────────────────┐
│                Backend (FastAPI)                 │
│  ┌───────────────────────────────────────────┐  │
│  │  get_current_user()                       │  │
│  │    ↓                                      │  │
│  │  verify_token()                           │  │
│  │    ↓                                      │  │
│  │  get_user_jira_client()                   │  │
│  │    ↓                                      │  │
│  │  decrypt_token()                          │  │
│  └───────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────┘
                     │ Credenciales del Usuario
                     ▼
┌─────────────────────────────────────────────────┐
│                  Jira API                        │
└─────────────────────────────────────────────────┘
```

---

## 🔒 Seguridad

### Almacenamiento Seguro

| Dato | Almacenamiento | Método |
|------|----------------|--------|
| Contraseña | Base de datos | Bcrypt hash (nunca reversible) |
| Token Jira | Base de datos | Fernet encryption (reversible) |
| JWT Secret | Variable de entorno | Secret seguro (32 bytes) |
| Encryption Key | Variable de entorno | Fernet key (32 bytes) |

### Best Practices Implementadas

- ✅ Nunca loguear contraseñas o tokens
- ✅ HTTPS obligatorio en producción (Render)
- ✅ CORS restrictivo (solo frontend permitido)
- ✅ Tokens con expiración automática
- ✅ Validación de input con Pydantic
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Credenciales encriptadas en reposo

---

## 🐛 Troubleshooting

### Token inválido o expirado
**Solución:** Hacer login nuevamente para obtener nuevo token

### Usuario sin credenciales de Jira
**Solución:** Verificar que el registro incluyó `jira_email`, `jira_api_token`, `jira_base_url`

### Error de base de datos
**Solución:**
```bash
rm jira_agent.db
python -m app.core.init_db
```

### Import errors
**Solución:**
```bash
pip install -r requirements.txt
```

---

## 📊 Estadísticas del Proyecto

- **Archivos creados:** 17
- **Líneas de código:** ~2,500
- **Endpoints protegidos:** 6
- **Documentación:** 5 guías completas
- **Tests:** Script automatizado incluido
- **Tiempo de implementación:** ~8 horas

---

## 🎯 Próximos Pasos

### Opcionales (Mejoras Futuras)

1. **Refresh Tokens** - Renovar tokens sin re-login
2. **OAuth 2.0** - Login con Google/Microsoft
3. **Rate Limiting** - Prevenir abuso de endpoints
4. **2FA** - Autenticación de dos factores
5. **Password Reset** - Recuperación por email
6. **Roles y Permisos** - Control de acceso granular

### Frontend (Próxima Fase)

Ver guía completa en `docs/AUTHENTICATION_ANALYSIS.md` - Fase 3

---

## 💡 Contribuir

Para agregar nuevos endpoints protegidos:

```python
from app.api.dependencies import get_user_jira_client
from app.clients.jira_client import JiraClient

@router.get("/mi-endpoint")
async def mi_endpoint(
    jira_client: JiraClient = Depends(get_user_jira_client)  # ← Agregar esto
):
    # Ahora jira_client tiene las credenciales del usuario autenticado
    return jira_client.hacer_algo()
```

---

## 📞 Soporte

- **Issues:** [GitHub Issues](https://github.com/stiago2/jira-ai-agent/issues)
- **Documentación:** `docs/` directory
- **Swagger UI:** http://localhost:8000/docs (local)
- **Producción:** https://jira-ai-agent.onrender.com/docs

---

## ✨ Créditos

Desarrollado con ❤️ usando:
- FastAPI
- SQLAlchemy
- JWT (python-jose)
- Bcrypt (passlib)
- Fernet (cryptography)

---

**Estado:** ✅ Producción Ready
**Versión:** 0.2.0
**Última actualización:** Enero 2026
