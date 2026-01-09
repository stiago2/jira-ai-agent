# Sistema de Autenticación - Guía Rápida

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Generar claves de seguridad
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))" >> .env
python -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())" >> .env
```

### 3. Inicializar Base de Datos

```bash
# Crear tablas y usuario admin
python -m app.core.init_db
```

Esto te pedirá:
- Username y password para el admin
- Credenciales de Jira (email, API token, base URL)

### 4. Iniciar el Servidor

```bash
uvicorn app.main:app --reload
```

### 5. Probar la Autenticación

Abre http://localhost:8000/docs para ver la documentación interactiva.

---

## 📖 Uso de la API

### Registrar un Usuario

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

**Respuesta:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "jira_email": "john@company.com",
  "jira_base_url": "https://yourcompany.atlassian.net",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-01-09T20:00:00Z",
  "last_login": null
}
```

### Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=SecurePassword123!"
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Obtener Info del Usuario Actual

```bash
# Guardar el token en una variable
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "jira_email": "john@company.com",
  "jira_base_url": "https://yourcompany.atlassian.net",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-01-09T20:00:00Z",
  "last_login": "2026-01-09T20:05:00Z"
}
```

### Usar Endpoints Protegidos

Una vez que tengas el token, inclúyelo en el header `Authorization` de todas las peticiones:

```bash
# Ejemplo: Obtener proyectos (requiere autenticación cuando esté protegido)
curl -X GET "http://localhost:8000/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔐 Seguridad

### Variables de Entorno Críticas

Estas variables **DEBEN** configurarse en producción:

```bash
# REQUERIDO: Genera con secrets.token_urlsafe(32)
JWT_SECRET_KEY=your-secret-key-CHANGE-THIS

# REQUERIDO: Genera con Fernet.generate_key()
ENCRYPTION_KEY=your-encryption-key-CHANGE-THIS

# REQUERIDO: URL de base de datos en producción
DATABASE_URL=postgresql://user:pass@host/db
```

### Generar Claves de Forma Segura

```python
# JWT Secret Key
import secrets
print(secrets.token_urlsafe(32))
# Ejemplo: 'XAhHF7_QfGlm8TnTiUk9j3YZ0w5rK8bN1qW2eR3tY4u'

# Encryption Key
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
# Ejemplo: 'kZ8v3X9mN4pQ2wR7tY1uI5oP0aS6dF3gH8jK4lM9nB2='
```

### Configurar en Render

En el dashboard de Render, agrega estas variables de entorno:

```
JWT_SECRET_KEY=<genera-uno-aleatorio>
ENCRYPTION_KEY=<genera-uno-aleatorio>
DATABASE_URL=<tu-url-de-postgresql>
```

---

## 🗄️ Base de Datos

### SQLite (Desarrollo)

Por defecto usa SQLite, perfecto para desarrollo:

```bash
DATABASE_URL=sqlite:///./jira_agent.db
```

El archivo `jira_agent.db` se creará en el directorio raíz.

### PostgreSQL (Producción)

#### Opción 1: Supabase (Recomendado - Gratis)

1. Crea cuenta en [supabase.com](https://supabase.com)
2. Crea un proyecto
3. Copia la `DATABASE_URL` de Project Settings → Database
4. Formato: `postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres`

#### Opción 2: Neon PostgreSQL (Gratis)

1. Crea cuenta en [neon.tech](https://neon.tech)
2. Crea un proyecto
3. Copia la connection string
4. Formato: `postgresql://user:pass@host.region.neon.tech/dbname`

#### Opción 3: Render PostgreSQL (Gratis 90 días)

1. En Render dashboard, crea un PostgreSQL database
2. Copia la `Internal Database URL`
3. Agrega como variable de entorno `DATABASE_URL`

### Migraciones

Para cambios futuros en el modelo, usa Alembic:

```bash
# Inicializar Alembic (solo una vez)
alembic init alembic

# Crear migración
alembic revision --autogenerate -m "Add new field"

# Aplicar migraciones
alembic upgrade head
```

---

## 🧪 Testing

### Probar Registro y Login

```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPass123!",
    "jira_email": "test@company.com",
    "jira_api_token": "test_token",
    "jira_base_url": "https://test.atlassian.net"
  }'

# 2. Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=TestPass123!"

# 3. Copiar el access_token de la respuesta

# 4. Probar endpoint protegido
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <TU_TOKEN_AQUI>"
```

### Health Check de Autenticación

```bash
curl http://localhost:8000/api/v1/auth/health
```

Respuesta esperada:
```json
{
  "service": "authentication",
  "status": "healthy"
}
```

---

## 🔧 Troubleshooting

### Error: "Token inválido o expirado"

- Verifica que el token esté en el header: `Authorization: Bearer <token>`
- El token expira después de 24 horas (configurable con `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Haz login nuevamente para obtener un nuevo token

### Error: "Email ya registrado"

- El email debe ser único
- Usa otro email o elimina el usuario existente de la base de datos

### Error: "Import 'sqlalchemy.orm' could not be resolved"

- Asegúrate de haber instalado las dependencias:
```bash
pip install sqlalchemy alembic
```

### Error: "Invalid ENCRYPTION_KEY"

- Genera una nueva encryption key:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```
- Agrégala al archivo `.env`

### Error: "No se pueden crear tablas"

- Verifica que `DATABASE_URL` esté configurado correctamente
- Para SQLite, verifica permisos de escritura en el directorio
- Para PostgreSQL, verifica la conexión y credenciales

---

## 📚 Próximos Pasos

Ahora que tienes autenticación funcionando:

1. **Proteger endpoints existentes** - Agrega `Depends(get_current_user)` a los endpoints que requieran auth
2. **Frontend** - Implementa login/registro en React
3. **Refresh tokens** - Para mayor seguridad
4. **Roles y permisos** - Control de acceso más granular
5. **OAuth** - Login con Google/Microsoft

Consulta [AUTH_IMPLEMENTATION_ANALYSIS.md](./AUTHENTICATION_ANALYSIS.md) para más detalles sobre la implementación completa.
