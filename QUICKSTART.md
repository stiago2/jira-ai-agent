# Quick Start Guide

## 🚀 Inicio Rápido (5 minutos)

### Opción 1: Usando el script de setup (Recomendado)

```bash
# Desde el directorio del proyecto
./scripts/setup.sh
```

Esto hará:
1. ✓ Verificar Python 3.11
2. ✓ Crear entorno virtual
3. ✓ Instalar dependencias
4. ✓ Crear archivo .env

### Opción 2: Setup manual

```bash
# 1. Crear entorno virtual
python3.11 -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
```

## 📝 Configurar Credenciales de Jira

### 1. Obtener API Token de Jira

1. Ve a: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click en **"Create API token"**
3. Dale un nombre (ej: "jira-ai-agent")
4. **Copia el token** (solo se muestra una vez)

### 2. Editar archivo `.env`

```bash
nano .env  # o usa tu editor favorito
```

Configura estas variables:

```env
JIRA_BASE_URL=https://tu-empresa.atlassian.net
JIRA_EMAIL=tu-email@empresa.com
JIRA_API_TOKEN=tu_token_copiado_aqui
JIRA_DEFAULT_PROJECT=PROJ
```

**Importante:**
- Reemplaza `tu-empresa` con el nombre de tu workspace de Jira
- Usa el email de tu cuenta de Jira
- Pega el API token que copiaste

## ▶️ Ejecutar la Aplicación

### Opción 1: Usando uvicorn directamente

```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Ejecutar servidor
uvicorn app.main:app --reload
```

### Opción 2: Usando el script

```bash
./scripts/run_dev.sh
```

### Opción 3: Usando Docker

```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f api
```

## ✅ Verificar que Funciona

### 1. Abrir el navegador

Ve a: http://localhost:8000

Deberías ver:
```json
{
  "name": "Jira AI Agent",
  "version": "0.1.0",
  "status": "running"
}
```

### 2. Ver documentación de la API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Hacer una prueba con curl

```bash
# Health check
curl http://localhost:8000/api/v1/health
```

## 📚 Próximos Pasos

1. **Explorar la documentación**: http://localhost:8000/docs
2. **Leer la arquitectura**: [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)
3. **Ver el README completo**: [README.md](README.md)

## 🔧 Troubleshooting

### Error: "Python 3.11 not found"

**Solución:**
```bash
# macOS (usando Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11

# Verificar instalación
python3.11 --version
```

### Error: "Module not found"

**Solución:**
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Address already in use"

**Solución:**
```bash
# El puerto 8000 está ocupado, usar otro puerto
uvicorn app.main:app --reload --port 8001
```

### Error: "JIRA_BASE_URL is required"

**Solución:**
- Verifica que el archivo `.env` existe
- Verifica que las variables están configuradas correctamente
- Reinicia el servidor después de editar `.env`

## 🎯 Comandos Útiles

```bash
# Ver logs en desarrollo
tail -f logs/app.log

# Ejecutar tests
pytest

# Ver cobertura de tests
pytest --cov=app --cov-report=html

# Formatear código
black app/

# Verificar estilo
flake8 app/

# Type checking
mypy app/

# Detener Docker
docker-compose down

# Ver logs de Docker
docker-compose logs -f
```

## 📞 Ayuda

Si tienes problemas:

1. Revisa el archivo [README.md](README.md)
2. Revisa la documentación en [docs/](docs/)
3. Abre un issue en el repositorio
