# 🆓 Opciones GRATUITAS para el Backend

## 🎯 TL;DR - Mejor Opción 100% Gratis

```
┌────────────────────────────────────────────────────────┐
│  OPCIÓN COMPLETAMENTE GRATIS:                         │
│  → Netlify (Frontend) + Render Free (Backend)         │
│     Costo: $0/mes | Setup: 20 min                     │
│     ⚠️ Limitación: Backend duerme después de 15 min   │
└────────────────────────────────────────────────────────┘
```

---

## 📊 Comparativa de Opciones Gratuitas

| Plataforma | Costo | RAM | Sleep | Build Time | Mejor Para |
|------------|-------|-----|-------|------------|------------|
| **Render Free** | $0 | 512MB | ⚠️ 15min | Ilimitado | MVP testing |
| **Fly.io** | $0 | 256MB | ❌ No | Limitado | Producción ligera |
| **Railway Trial** | $0 | Flexible | ❌ No | Limitado | 30 días prueba |
| **Koyeb** | $0 | 512MB | ⚠️ Sí | Limitado | Testing |
| **Cyclic** | $0 | 256MB | ⚠️ Sí | Limitado | Serverless |
| **Deta Space** | $0 | 128MB | ❌ No | Limitado | Micro-apps |

---

## 🏆 Opción #1: Render (Free Tier) - MÁS FÁCIL

### ✅ Ventajas
- **Completamente gratis** para siempre
- **512MB RAM** (suficiente para FastAPI)
- **SSL automático**
- **Deploy desde Git** automático
- **Logs incluidos**
- **No requiere tarjeta de crédito**

### ⚠️ Limitación Principal
- **El servicio duerme después de 15 minutos de inactividad**
- Primera request después de dormir toma 30-60 segundos en despertar
- Funciona bien para demos y testing

### 📋 Setup (10 minutos)

#### Paso 1: Crear cuenta
1. Ve a [render.com](https://render.com)
2. Sign up con GitHub (gratis, sin tarjeta)

#### Paso 2: Crear Web Service
1. Dashboard → "New" → "Web Service"
2. Connect tu repo `jira-ai-agent`
3. Configuración:

```yaml
Name: jira-backend
Environment: Python 3
Region: Oregon (US West)
Branch: main
Build Command: pip install -r requirements.txt
Start Command: cd app && uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Paso 3: Variables de entorno
```bash
JIRA_BASE_URL=https://tu-empresa.atlassian.net
JIRA_EMAIL=tu-email@example.com
JIRA_API_TOKEN=tu_token
PORT=10000
```

#### Paso 4: Seleccionar plan
- Selecciona **"Free"** ✅
- Click "Create Web Service"

#### Paso 5: Copiar URL
- Espera ~3 minutos
- Copia la URL: `https://jira-backend.onrender.com`

### 🔧 Solución al "Sleep" (Opcional)

**Opción A: Cron job para mantener despierto**

Usar un servicio externo que haga ping cada 10 minutos:

1. **UptimeRobot** (gratis):
   - Crea cuenta en [uptimerobot.com](https://uptimerobot.com)
   - Add Monitor → HTTP(s)
   - URL: `https://jira-backend.onrender.com/api/v1/health`
   - Interval: 5 minutes
   - ✅ Tu backend nunca duerme

2. **Cron-job.org** (gratis):
   - Crea cuenta en [cron-job.org](https://cron-job.org)
   - Create cronjob
   - URL: `https://jira-backend.onrender.com/api/v1/health`
   - Every: 10 minutes

**Opción B: Aceptar el sleep**
- Bueno para demos y testing
- Primera carga lenta, luego normal
- Gratis para siempre

---

## 🥈 Opción #2: Fly.io - MEJOR RENDIMIENTO GRATIS

### ✅ Ventajas
- **Completamente gratis** hasta 3 VMs
- **NO duerme** ✅ (siempre activo)
- **160GB bandwidth/mes** incluido
- **Global edge network**
- **SSL automático**
- **Mejor rendimiento** que Render free

### ⚠️ Limitaciones
- **256MB RAM por VM** (suficiente pero ajustado)
- **3GB persistent storage** máximo
- Requiere tarjeta de crédito (pero no cobra si no pasas el límite)
- Setup más técnico (Docker)

### 📋 Setup (20 minutos)

#### Paso 1: Instalar Fly CLI
```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

#### Paso 2: Login
```bash
flyctl auth signup  # O login si ya tienes cuenta
```

#### Paso 3: Crear app
```bash
cd /path/to/jira-ai-agent

# Crear configuración
flyctl launch --no-deploy

# Responde:
# App name: jira-backend
# Region: Miami (closest to you)
# Setup PostgreSQL: No
# Setup Redis: No
```

Esto crea `fly.toml`:
```toml
app = "jira-backend"
primary_region = "mia"

[build]
  dockerfile = "Dockerfile.backend"

[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [services.concurrency]
    hard_limit = 25
    soft_limit = 20

[[vm]]
  memory = '256mb'
  cpu_kind = 'shared'
  cpus = 1
```

#### Paso 4: Configurar secrets
```bash
flyctl secrets set \
  JIRA_BASE_URL=https://tu-empresa.atlassian.net \
  JIRA_EMAIL=tu-email@example.com \
  JIRA_API_TOKEN=tu_token
```

#### Paso 5: Deploy
```bash
flyctl deploy
```

Tu app estará en: `https://jira-backend.fly.dev`

### 💡 Optimizar para 256MB RAM

Edita `Dockerfile.backend` para usar menos memoria:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Solo instalar lo necesario
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8080

# Usar solo 1 worker
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
```

---

## 🥉 Opción #3: Railway Trial - MEJOR PARA TESTING

### ✅ Ventajas
- **$5 de crédito gratis** al registrarte
- **Sin tarjeta de crédito** requerida
- **No duerme**
- **Mejor DX** (developer experience)
- Misma experiencia que la versión paga

### ⚠️ Limitaciones
- Solo dura hasta que gastes los $5 (aprox 1 mes)
- Después necesitas upgrade a $5/mes
- Límite de $5/mes en free tier

### 📋 Setup
Ver [DEPLOY_NOW.md](../DEPLOY_NOW.md) - mismos pasos, usar trial.

---

## 💎 Opción #4: Koyeb - ALTERNATIVA EUROPEA

### ✅ Ventajas
- **Free tier disponible**
- **512MB RAM**
- **100GB bandwidth**
- Regiones en Europa
- Deploy desde Git

### ⚠️ Limitaciones
- Duerme después de inactividad
- Menos conocido, menor community

### 📋 Setup (15 minutos)

1. Ve a [koyeb.com](https://www.koyeb.com)
2. Sign up con GitHub
3. New Service → Git
4. Selecciona repo
5. Configuración:
   ```
   Build type: Dockerfile
   Dockerfile: Dockerfile.backend
   Port: 8000
   Instance: Nano (Free)
   ```
6. Variables de entorno (mismas que antes)
7. Deploy

---

## 🚀 Opción #5: Deta Space - MICRO BACKEND

### ✅ Ventajas
- **Completamente gratis**
- **No duerme**
- Fácil de usar
- Python support nativo

### ⚠️ Limitaciones
- **128MB RAM** (muy limitado)
- Solo para apps muy ligeras
- No ideal para FastAPI completo

### 📋 Setup
```bash
# Instalar Deta CLI
curl -fsSL https://get.deta.dev/cli.sh | sh

# Login
deta login

# Deploy
cd app
deta new --python
```

---

## 🔄 Opción #6: Cyclic.sh - SERVERLESS

### ✅ Ventajas
- **Gratis para siempre**
- Serverless (escala automático)
- Deploy desde GitHub

### ⚠️ Limitaciones
- **Principalmente para Node.js**
- Python support limitado
- Cold starts

---

## 📊 Comparación Detallada

### Performance Real

```
Render Free (con sleep):
├── First request:     30-60 segundos ⚠️
├── After wake:        200-500ms ✅
└── Concurrent users:  10-20 ✅

Fly.io Free:
├── First request:     200-300ms ✅
├── Normal:            100-200ms ✅
└── Concurrent users:  5-10 ⚠️ (256MB limit)

Railway Trial:
├── First request:     200-300ms ✅
├── Normal:            100-200ms ✅
└── Concurrent users:  20-50 ✅
```

### Límites de Requests

```
Render Free:
└── Unlimited requests (pero duerme)

Fly.io Free:
└── 160GB bandwidth/mes
   ≈ 1.6M requests (100KB response)

Railway Trial:
└── Hasta agotar $5
   ≈ 1 mes de uso normal
```

---

## 🎯 Recomendación por Caso de Uso

### Para Demo/Presentación (1-7 días)
```
🥇 MEJOR: Render Free + UptimeRobot
   Razón: Gratis, fácil, mantén despierto con ping
   Setup: 15 minutos
```

### Para MVP/Testing (1-3 meses)
```
🥇 MEJOR: Fly.io Free
   Razón: No duerme, mejor performance, gratis real
   Setup: 20 minutos
```

### Para Producción Real
```
🥇 MEJOR: Railway $5/mes
   Razón: Vale la pena, sin limitaciones, profesional
   Setup: 10 minutos
```

### Si NUNCA quieres pagar
```
🥇 MEJOR: Render Free + UptimeRobot para mantener vivo
   Razón: Único que es gratis para siempre sin trucos
   Limitación: Sleep inicial, pero resoluble
```

---

## 🔧 Setup Combo Recomendado: 100% Gratis

### Frontend: Netlify (Gratis)
### Backend: Render Free (Gratis)
### Keep-alive: UptimeRobot (Gratis)

### Total: $0/mes ✅

### Pasos Completos:

#### 1. Deploy Frontend en Netlify (5 min)
```bash
1. netlify.com → Sign up con GitHub
2. Import repo → jira-tracker
3. Build settings automáticos
4. Deploy
```

#### 2. Deploy Backend en Render (10 min)
```bash
1. render.com → Sign up con GitHub
2. New Web Service → Import repo
3. Configuración:
   - Build: pip install -r requirements.txt
   - Start: cd app && uvicorn main:app --host 0.0.0.0 --port $PORT
   - Plan: Free
4. Variables de entorno (Jira)
5. Deploy
```

#### 3. Keep Backend Awake (5 min)
```bash
1. uptimerobot.com → Create free account
2. Add Monitor:
   - Type: HTTP(s)
   - URL: https://tu-backend.onrender.com/api/v1/health
   - Interval: 5 minutes
3. Save
```

#### 4. Conectar Frontend y Backend (5 min)
```bash
1. Netlify → Environment variables
   VITE_API_URL=https://tu-backend.onrender.com

2. Redeploy Netlify

3. Actualizar CORS en app/main.py
   allow_origins=["https://tu-frontend.netlify.app"]

4. Push a GitHub (auto-redeploy)
```

### ✅ Resultado: App 100% funcional, 100% gratis, 24/7

---

## ⚡ Performance Tips para Free Tier

### Optimizar FastAPI para 512MB RAM

```python
# app/main.py

# 1. Limitar workers
# En Render, usa solo 1 worker (por defecto)

# 2. Agregar cache simple
from functools import lru_cache

@lru_cache(maxsize=100)
def get_project_info(project_key: str):
    # Cache de requests frecuentes
    pass

# 3. Rate limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/tasks/create")
@limiter.limit("10/minute")
async def create_task(...):
    pass
```

### Reducir tiempo de wake-up en Render

```python
# app/main.py

@app.on_event("startup")
async def startup_event():
    """Pre-calentar conexiones"""
    # Hacer una request dummy a Jira
    try:
        jira_client = get_jira_client()
        jira_client.get_current_user()
    except:
        pass
```

---

## 💰 Comparación: Free vs Paid

### Render Free vs Railway $5/mes

```
Render Free:
├── Costo: $0/mes ✅
├── Sleep: Sí ⚠️
├── RAM: 512MB ✅
├── Build: Ilimitado ✅
└── Support: Community

Railway $5/mes:
├── Costo: $5/mes
├── Sleep: No ✅
├── RAM: 8GB ✅
├── Build: Ilimitado ✅
└── Support: Email

¿Vale la pena pagar $5/mes?
SÍ si:
- Necesitas respuesta instant
- >50 usuarios concurrentes
- App en producción real

NO si:
- Solo testing/demo
- Puedes esperar 30s primera carga
- <20 usuarios
```

---

## 🎓 Migración Path

### Empezar Gratis → Escalar Pagado

```
Mes 1-2: Render Free
├── Testing y validación
├── Primeros usuarios
└── Costo: $0

Mes 3-4: Railway Trial
├── Más usuarios
├── Mejor performance
└── Costo: $0 (trial)

Mes 5+: Railway Paid
├── Producción real
├── Sin limitaciones
└── Costo: $5/mes

Total costo año 1: $40 (8 meses × $5)
vs Empezar directo en Railway: $60
Ahorro: $20 + validaste el producto gratis
```

---

## ✅ Checklist Setup Gratis

- [ ] Cuenta GitHub creada
- [ ] Repo subido a GitHub
- [ ] Cuenta Netlify (frontend)
- [ ] Cuenta Render (backend)
- [ ] Cuenta UptimeRobot (keep-alive)
- [ ] Variables de entorno configuradas
- [ ] CORS actualizado
- [ ] Keep-alive configurado
- [ ] Testing end-to-end
- [ ] Documentar URLs para el equipo

---

## 🚨 Advertencias Importantes

### Render Free Sleep
- ⚠️ Usuarios pueden experimentar 30-60s de espera si la app durmió
- ✅ Solución: UptimeRobot mantiene vivo
- ✅ Alternativa: Mostrar mensaje "Despertando backend..."

### Fly.io 256MB RAM
- ⚠️ Puede quedarse sin memoria con muchos requests concurrentes
- ✅ Solución: Optimizar código, limitar concurrencia
- ✅ Alternativa: Usar 512MB ($3.20/mes)

### Railway Trial
- ⚠️ Solo dura ~30 días
- ✅ Plan: Usar trial para testing, luego decidir si pagar
- ✅ Alternativa: Combinar con Render después

---

## 📚 Recursos

- [Render Free Tier Docs](https://render.com/docs/free)
- [Fly.io Free Tier](https://fly.io/docs/about/pricing/)
- [Railway Pricing](https://railway.app/pricing)
- [UptimeRobot](https://uptimerobot.com/)
- [Netlify Free Tier](https://www.netlify.com/pricing/)

---

## 🎯 Decisión Final

### Para Jira AI Agent:

```
🏆 RECOMENDACIÓN GRATIS:

Frontend: Netlify (Gratis forever)
Backend: Render Free (Gratis forever)
Keep-alive: UptimeRobot (Gratis forever)

Total: $0/mes
Setup: 20 minutos
Limitación: ~30s primera carga después de sleep

✅ Perfecto para:
- MVP / Testing
- Demos a clientes
- Validación de producto
- <100 usuarios
- Budget = $0

⚠️ Migrar a Railway ($5/mes) cuando:
- Necesites respuesta instantánea
- >50 usuarios regulares
- Producción real
- Puedas invertir $5/mes
```

---

**¿Prefieres 100% gratis o invertir $5/mes para mejor experiencia?**

- **$0/mes**: Lee [Setup combo gratis](#setup-combo-recomendado-100-gratis) arriba ⬆️
- **$5/mes**: Lee [DEPLOY_NOW.md](../DEPLOY_NOW.md) para Railway

¡Ambas opciones son excelentes! 🚀
