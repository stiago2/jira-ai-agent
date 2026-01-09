# Guía de Despliegue - Jira AI Agent

## 📋 Tabla de Contenidos
- [Arquitectura Actual](#arquitectura-actual)
- [Opciones de Despliegue](#opciones-de-despliegue)
- [Opción Recomendada](#opción-recomendada)
- [Despliegues Alternativos](#despliegues-alternativos)
- [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
- [Checklist de Seguridad](#checklist-de-seguridad)
- [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)

---

## 🏗️ Arquitectura Actual

### Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    JIRA AI AGENT                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐        ┌──────────────────┐         │
│  │   FRONTEND       │        │    BACKEND       │         │
│  │                  │        │                  │         │
│  │  React/TypeScript│◄──────►│  FastAPI/Python  │         │
│  │  Vite            │  API   │  Uvicorn         │         │
│  │  Port: 5173      │        │  Port: 8000      │         │
│  └──────────────────┘        └──────────────────┘         │
│                                      │                      │
│                                      ▼                      │
│                              ┌──────────────┐              │
│                              │  Jira Cloud  │              │
│                              │  REST API    │              │
│                              └──────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### Stack Tecnológico

**Backend:**
- Python 3.9+
- FastAPI
- Uvicorn (ASGI server)
- Pydantic (validación)
- python-dotenv
- Dependencias: requests, etc.

**Frontend:**
- React 18+
- TypeScript
- Vite (build tool)
- React Router
- CSS modules

---

## 🚀 Opciones de Despliegue

### Comparativa Rápida

| Opción | Backend | Frontend | Costo | Complejidad | Escalabilidad |
|--------|---------|----------|-------|-------------|---------------|
| **Railway** | ✅ | ✅ | $5-20/mes | ⭐⭐ | ⭐⭐⭐ |
| **Render** | ✅ | ✅ | $7-25/mes | ⭐⭐ | ⭐⭐⭐ |
| **Vercel + Railway** | Railway | Vercel | $5-15/mes | ⭐⭐ | ⭐⭐⭐⭐ |
| **AWS (EC2)** | ✅ | ✅ | $10-50/mes | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **DigitalOcean** | ✅ | ✅ | $6-24/mes | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Docker Compose** | ✅ | ✅ | Variable | ⭐⭐⭐ | ⭐⭐⭐ |
| **Fly.io** | ✅ | ✅ | $0-15/mes | ⭐⭐ | ⭐⭐⭐⭐ |

---

## ⭐ Opción Recomendada: Railway

### Por qué Railway?

1. **Simplicidad**: Deploy directo desde GitHub
2. **Monorepo friendly**: Soporta múltiples servicios
3. **Variables de entorno**: Gestión fácil y segura
4. **Precio justo**: $5/mes por servicio
5. **Dominios custom**: Incluidos gratuitamente
6. **CI/CD automático**: Deploy en cada push
7. **Logs en tiempo real**: Debugging fácil

### Estructura del Proyecto para Railway

```
jira-ai-agent/
├── app/                    # Backend FastAPI
│   ├── __init__.py
│   ├── main.py
│   ├── requirements.txt    # Dependencias Python
│   └── ...
├── jira-tracker/          # Frontend React
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── ...
├── railway.json           # Configuración Railway (nuevo)
└── README.md
```

### Paso a Paso: Deploy en Railway

#### 1. Preparar el Backend

**Crear `requirements.txt` en la raíz:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
requests==2.31.0
```

**Crear `Procfile` (opcional, Railway lo detecta automáticamente):**
```
web: cd app && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Crear `railway.json` en la raíz:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd app && uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 2. Preparar el Frontend

**Actualizar `jira-tracker/vite.config.ts`:**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
  },
  preview: {
    port: 4173,
  },
  build: {
    outDir: 'dist',
  }
})
```

**Actualizar `jira-tracker/package.json`:**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "start": "vite preview --host 0.0.0.0 --port $PORT"
  }
}
```

#### 3. Deploy en Railway

**Opción A: Desde Dashboard (Recomendado)**

1. Ve a [railway.app](https://railway.app)
2. Crea cuenta con GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detectará automáticamente los servicios

**Configurar Backend:**
- Service name: `jira-backend`
- Root directory: `/`
- Start command: `cd app && uvicorn main:app --host 0.0.0.0 --port $PORT`
- Variables de entorno:
  ```
  JIRA_BASE_URL=https://tu-dominio.atlassian.net
  JIRA_EMAIL=tu-email@ejemplo.com
  JIRA_API_TOKEN=tu_api_token
  ```

**Configurar Frontend:**
- Service name: `jira-frontend`
- Root directory: `/jira-tracker`
- Build command: `npm install && npm run build`
- Start command: `npm run start`
- Variables de entorno:
  ```
  VITE_API_URL=https://jira-backend.railway.app
  ```

**Opción B: Usando Railway CLI**

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Crear servicios
railway service create backend
railway service create frontend

# Deploy backend
railway up --service backend

# Deploy frontend
railway up --service frontend
```

#### 4. Configurar Dominios

Railway proporciona dominios automáticos:
- Backend: `https://jira-backend-production.up.railway.app`
- Frontend: `https://jira-frontend-production.up.railway.app`

**Para dominio custom:**
1. Ve a Settings de cada servicio
2. Click "Generate Domain" o "Add Custom Domain"
3. Configura DNS:
   - Backend: `api.tudominio.com` → CNAME a Railway
   - Frontend: `app.tudominio.com` → CNAME a Railway

#### 5. CORS en el Backend

Actualizar `app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Desarrollo
        "https://jira-frontend-production.up.railway.app",  # Producción
        "https://app.tudominio.com"  # Custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔄 Despliegues Alternativos

### Opción 2: Vercel (Frontend) + Railway/Render (Backend)

**Ventajas:**
- Vercel es excelente para React/Next.js
- Deploy automático desde Git
- CDN global incluido
- SSL automático
- Serverless por defecto

**Despliegue:**

**Backend en Railway (igual que arriba)**

**Frontend en Vercel:**

1. Ve a [vercel.com](https://vercel.com)
2. Import proyecto desde GitHub
3. Configura:
   - Framework: Vite
   - Root Directory: `jira-tracker`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. Variables de entorno:
   ```
   VITE_API_URL=https://jira-backend-production.up.railway.app
   ```

5. Deploy automático en cada push

**Costo:**
- Vercel: $0 (Hobby) o $20/mes (Pro)
- Railway: $5/mes backend

---

### Opción 3: Render (Todo-en-uno)

**Ventajas:**
- Free tier disponible
- Fácil configuración
- Soporta monorepos
- PostgreSQL incluido si lo necesitas

**Despliegue:**

1. Ve a [render.com](https://render.com)
2. New → Web Service (para backend)
3. Conecta GitHub
4. Configuración backend:
   ```
   Name: jira-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: cd app && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

5. New → Static Site (para frontend)
6. Configuración frontend:
   ```
   Name: jira-frontend
   Build Command: cd jira-tracker && npm install && npm run build
   Publish Directory: jira-tracker/dist
   ```

**Costo:**
- Free tier: $0 (con limitaciones)
- Starter: $7/mes por servicio

---

### Opción 4: DigitalOcean App Platform

**Ventajas:**
- Infraestructura robusta
- Escalabilidad automática
- Bases de datos managed
- Buen precio/rendimiento

**Despliegue:**

1. Ve a [DigitalOcean App Platform](https://www.digitalocean.com/products/app-platform)
2. Create App → GitHub
3. Detecta automáticamente los componentes

**Backend:**
```yaml
name: jira-backend
source:
  repo: tu-usuario/jira-ai-agent
  branch: main
run_command: cd app && uvicorn main:app --host 0.0.0.0 --port $PORT
environment_variables:
  - key: JIRA_BASE_URL
    scope: RUN_TIME
  - key: JIRA_EMAIL
    scope: RUN_TIME
  - key: JIRA_API_TOKEN
    scope: RUN_TIME
    type: SECRET
```

**Frontend:**
```yaml
name: jira-frontend
source:
  repo: tu-usuario/jira-ai-agent
  branch: main
build_command: cd jira-tracker && npm install && npm run build
output_dir: jira-tracker/dist
```

**Costo:**
- Basic: $5/mes por componente
- Professional: $12/mes por componente

---

### Opción 5: AWS (Producción Enterprise)

**Para cuando necesites máximo control y escalabilidad.**

**Arquitectura AWS:**

```
┌─────────────────────────────────────────────────────┐
│                    AWS Cloud                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐        ┌─────────────┐           │
│  │   Route 53  │        │  CloudFront │           │
│  │    (DNS)    │        │    (CDN)    │           │
│  └──────┬──────┘        └──────┬──────┘           │
│         │                      │                   │
│         ▼                      ▼                   │
│  ┌─────────────┐        ┌─────────────┐           │
│  │     ALB     │        │     S3      │           │
│  │(Load Bal.)  │        │  (Static)   │           │
│  └──────┬──────┘        └─────────────┘           │
│         │                                          │
│         ▼                                          │
│  ┌─────────────┐                                  │
│  │   ECS/EC2   │                                  │
│  │  (Backend)  │                                  │
│  └─────────────┘                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Servicios necesarios:**

1. **S3 + CloudFront**: Frontend estático
2. **ECS (Fargate) o EC2**: Backend FastAPI
3. **Application Load Balancer**: Balanceo de carga
4. **Route 53**: DNS management
5. **Secrets Manager**: Variables de entorno seguras
6. **CloudWatch**: Logs y monitoring

**Costo estimado:**
- $20-100/mes (dependiendo del tráfico)

**Despliegue con CDK (recomendado):**

```bash
# Instalar AWS CDK
npm install -g aws-cdk

# Crear proyecto CDK
cdk init app --language typescript

# Deploy
cdk deploy
```

---

### Opción 6: Docker Compose (Self-hosted)

**Para desplegar en tu propio servidor.**

**Crear `docker-compose.yml` en la raíz:**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - JIRA_BASE_URL=${JIRA_BASE_URL}
      - JIRA_EMAIL=${JIRA_EMAIL}
      - JIRA_API_TOKEN=${JIRA_API_TOKEN}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./jira-tracker
      dockerfile: Dockerfile.frontend
      args:
        - VITE_API_URL=http://localhost:8000
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
      - frontend
    restart: unless-stopped
```

**Crear `Dockerfile.backend`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY app/ ./app/

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/health')"

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Crear `jira-tracker/Dockerfile.frontend`:**

```dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copiar package files
COPY package*.json ./
RUN npm ci

# Copiar código y build
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Production stage
FROM nginx:alpine

# Copiar build
COPY --from=build /app/dist /usr/share/nginx/html

# Configuración nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Crear `jira-tracker/nginx.conf`:**

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript
               application/x-javascript application/xml+rss
               application/javascript application/json;

    # SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Deploy:**

```bash
# Crear .env
cat > .env << EOF
JIRA_BASE_URL=https://tu-dominio.atlassian.net
JIRA_EMAIL=tu-email@ejemplo.com
JIRA_API_TOKEN=tu_api_token
EOF

# Build y start
docker-compose up -d

# Ver logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔐 Configuración de Variables de Entorno

### Variables Requeridas

**Backend:**
```bash
# Jira Configuration
JIRA_BASE_URL=https://tu-dominio.atlassian.net
JIRA_EMAIL=tu-email@ejemplo.com
JIRA_API_TOKEN=tu_api_token_aqui

# Optional
PORT=8000
ENVIRONMENT=production
LOG_LEVEL=info
```

**Frontend:**
```bash
# API Configuration
VITE_API_URL=https://api.tudominio.com

# Optional
VITE_APP_NAME=Jira AI Agent
VITE_ENVIRONMENT=production
```

### Cómo obtener Jira API Token

1. Ve a [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Dale un nombre descriptivo (ej: "Jira AI Agent Production")
4. Copia el token (solo se muestra una vez)
5. Guárdalo de forma segura

### Gestión Segura de Secrets

**Railway:**
- Usa el dashboard para agregar variables
- Marca tokens como "secret" para ofuscarlos

**Vercel:**
- Usa "Environment Variables" en Settings
- Marca como "Sensitive" los tokens

**AWS:**
- Usa AWS Secrets Manager
- Referencia con CDK/CloudFormation

**Docker:**
- Usa archivos `.env` (nunca commitear)
- O usa Docker Secrets en Swarm mode

---

## 🛡️ Checklist de Seguridad

### Antes del Deploy

- [ ] **API Tokens**: Nunca commitear en Git
- [ ] **CORS**: Configurar origins permitidos
- [ ] **HTTPS**: Forzar SSL/TLS
- [ ] **Rate Limiting**: Implementar en FastAPI
- [ ] **Input Validation**: Usar Pydantic correctamente
- [ ] **Secrets**: Usar variables de entorno
- [ ] **Dependencies**: Actualizar a versiones seguras
- [ ] **Error Messages**: No exponer información sensible

### Rate Limiting en FastAPI

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/tasks/create")
@limiter.limit("10/minute")
async def create_task(request: Request, ...):
    ...
```

### Headers de Seguridad

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Force HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["tudominio.com", "*.tudominio.com"]
)

# Security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

---

## 📊 Monitoreo y Mantenimiento

### Logs

**Railway/Render:**
- Logs integrados en el dashboard
- Retención: 7 días (free) - 30 días (paid)

**CloudWatch (AWS):**
```python
import logging
import watchtower

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

### Health Checks

Ya implementado en `app/main.py`:
```python
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
```

### Métricas

**Implementar métricas básicas:**

```python
from prometheus_fastapi_instrumentator import Instrumentator

# En main.py
Instrumentator().instrument(app).expose(app)

# Endpoint: /metrics
```

### Alertas

**Railway:**
- Configure notificaciones en Settings
- Email, Slack, Discord, Webhook

**AWS CloudWatch:**
- Crear alarmas para:
  - CPU > 80%
  - Memory > 80%
  - Error rate > 5%
  - Response time > 2s

---

## 💰 Comparativa de Costos (Mensual)

### Tráfico Bajo (< 10k requests/mes)

| Plataforma | Costo | Incluye |
|------------|-------|---------|
| **Railway** | $10 | Backend + Frontend, SSL, Dominios |
| **Render Free** | $0 | Limitado, sleep después de inactividad |
| **Vercel + Railway** | $5 | Railway backend, Vercel frontend free |
| **Fly.io** | $0-5 | 3 VMs gratis, luego $2/VM |

### Tráfico Medio (< 100k requests/mes)

| Plataforma | Costo | Incluye |
|------------|-------|---------|
| **Railway** | $20 | Mejor performance, más recursos |
| **Render** | $14 | Starter tier ambos servicios |
| **DigitalOcean** | $12 | App Platform básico |
| **AWS** | $25-50 | ECS Fargate + S3 + CloudFront |

### Tráfico Alto (> 1M requests/mes)

| Plataforma | Costo | Incluye |
|------------|-------|---------|
| **AWS** | $100-500 | Escalado automático, multi-región |
| **GCP** | $100-500 | Similar a AWS |
| **DigitalOcean** | $50-200 | Kubernetes cluster |

---

## 🎯 Recomendación Final

### Para Empezar (MVP/Testing)
**→ Railway (Backend + Frontend)**
- ✅ Más rápido de configurar
- ✅ $10/mes total
- ✅ Deploy en 10 minutos
- ✅ CI/CD automático

### Para Producción (Pequeña/Mediana empresa)
**→ Vercel (Frontend) + Railway (Backend)**
- ✅ Mejor performance frontend (CDN global)
- ✅ Backend estable en Railway
- ✅ $5-15/mes
- ✅ Escalabilidad automática

### Para Enterprise
**→ AWS (Todo)**
- ✅ Máximo control
- ✅ Escalabilidad ilimitada
- ✅ Múltiples regiones
- ✅ Cumplimiento regulatorio
- ⚠️ Requiere expertise DevOps

---

## 📚 Recursos Adicionales

- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 🚀 Next Steps

1. **Elige una plataforma** basado en tu presupuesto y necesidades
2. **Configura variables de entorno** de forma segura
3. **Realiza deploy de prueba** en ambiente staging
4. **Prueba funcionalidad** completa
5. **Configura monitoreo** y alertas
6. **Deploy a producción**
7. **Documenta el proceso** para tu equipo

---

**¿Necesitas ayuda específica con alguna plataforma? Házmelo saber y puedo crear guías más detalladas.**
