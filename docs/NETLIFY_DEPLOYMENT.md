# 🚀 Despliegue con Netlify (Frontend Gratis)

## ⭐ Mejor Opción: Netlify (Frontend) + Railway (Backend)

### Por qué esta combinación es ideal:

✅ **Frontend GRATIS en Netlify**
- 100GB bandwidth/mes
- SSL automático
- CDN global (edge network)
- Deploy automático desde Git
- 300 build minutes/mes
- Forms y Functions incluidos

✅ **Backend en Railway** - $5/mes
- Deploy automático
- SSL incluido
- Variables de entorno seguras

**Costo Total: $5/mes** (solo el backend)

---

## 📋 Setup Paso a Paso (15 minutos)

### Paso 1: Deploy Frontend en Netlify (5 min)

#### 1.1 Crear cuenta en Netlify

1. Ve a [netlify.com](https://www.netlify.com)
2. Sign up con GitHub (recomendado)
3. Autoriza Netlify a acceder a tus repos

#### 1.2 Crear nuevo site

1. Click "Add new site" → "Import an existing project"
2. Selecciona GitHub
3. Busca y selecciona tu repositorio `jira-ai-agent`

#### 1.3 Configurar build

```yaml
# Netlify detecta automáticamente, pero verifica:

Base directory: jira-tracker
Build command: npm run build
Publish directory: jira-tracker/dist
```

#### 1.4 Variables de entorno

En "Site settings" → "Environment variables":

```bash
VITE_API_URL=https://tu-backend.railway.app
```

**Importante:** Déjalo temporal por ahora, lo actualizaremos cuando tengamos la URL de Railway.

#### 1.5 Deploy

1. Click "Deploy site"
2. Espera ~2 minutos
3. Tu app estará en: `https://random-name-123456.netlify.app`

---

### Paso 2: Deploy Backend en Railway (5 min)

#### 2.1 Crear cuenta en Railway

1. Ve a [railway.app](https://railway.app)
2. Sign up con GitHub
3. Autoriza Railway

#### 2.2 Crear proyecto

1. Click "New Project"
2. "Deploy from GitHub repo"
3. Selecciona `jira-ai-agent`

#### 2.3 Configurar servicio

Railway detecta automáticamente FastAPI. Configura:

**Service name:** `jira-backend`

**Variables de entorno:**
```bash
JIRA_BASE_URL=https://tu-empresa.atlassian.net
JIRA_EMAIL=tu-email@example.com
JIRA_API_TOKEN=tu_api_token
PORT=8000
```

**Start Command (en Settings):**
```bash
cd app && uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 2.4 Generar dominio

1. En Railway, ve a Settings
2. Click "Generate Domain"
3. Copia la URL: `https://jira-backend-production.up.railway.app`

---

### Paso 3: Conectar Frontend y Backend (5 min)

#### 3.1 Actualizar CORS en el backend

Edita `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Desarrollo
        "https://tu-sitio.netlify.app",  # ← Agregar tu dominio de Netlify
        "https://random-name-123456.netlify.app",  # Si usas el auto-generado
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit y push:
```bash
git add app/main.py
git commit -m "Add Netlify domain to CORS"
git push origin main
```

Railway auto-deploya en ~1 minuto.

#### 3.2 Actualizar variable en Netlify

1. Ve a Netlify Dashboard
2. Site settings → Environment variables
3. Edita `VITE_API_URL`:
   ```
   https://jira-backend-production.up.railway.app
   ```
4. Click "Save"
5. En Deploys, click "Trigger deploy" → "Deploy site"

---

### Paso 4: Configurar Dominio Custom (Opcional)

#### Opción A: Dominio Netlify custom

1. En Netlify: Domain settings → "Add custom domain"
2. Ingresa: `app.tudominio.com`
3. Netlify te da instrucciones de DNS
4. Agrega CNAME en tu DNS provider:
   ```
   app.tudominio.com → random-name-123456.netlify.app
   ```
5. SSL se genera automáticamente en 24 horas

#### Opción B: Dominio Railway custom

1. En Railway: Settings → "Add custom domain"
2. Ingresa: `api.tudominio.com`
3. Agrega CNAME en tu DNS:
   ```
   api.tudominio.com → jira-backend-production.up.railway.app
   ```

**Actualiza CORS y variables con los nuevos dominios.**

---

## 🎨 Configuración Avanzada de Netlify

### netlify.toml (Recomendado)

Crea `jira-tracker/netlify.toml`:

```toml
# Build configuration
[build]
  base = "jira-tracker"
  command = "npm run build"
  publish = "dist"

# Production context
[context.production.environment]
  VITE_API_URL = "https://jira-backend-production.up.railway.app"

# Deploy previews (ramas de PR)
[context.deploy-preview.environment]
  VITE_API_URL = "https://jira-backend-staging.up.railway.app"

# Branch deploys (staging)
[context.branch-deploy.environment]
  VITE_API_URL = "https://jira-backend-staging.up.railway.app"

# Redirects y rewrites para SPA
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

# Headers de seguridad
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "no-referrer-when-downgrade"

# Cache para assets estáticos
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

# No cache para index.html
[[headers]]
  for = "/index.html"
  [headers.values]
    Cache-Control = "no-cache, no-store, must-revalidate"
```

### Forms (Bonus - Gratis)

Netlify Forms permite capturar datos sin backend:

```html
<!-- En tu React component -->
<form name="contact" method="POST" data-netlify="true">
  <input type="hidden" name="form-name" value="contact" />
  <input type="email" name="email" />
  <textarea name="message"></textarea>
  <button type="submit">Enviar</button>
</form>
```

### Functions (Bonus - Gratis)

Netlify Functions te da 125k invocaciones/mes gratis:

```javascript
// netlify/functions/hello.js
exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: "Hello from Netlify!" })
  };
};
```

Accesible en: `https://tu-sitio.netlify.app/.netlify/functions/hello`

---

## 📊 Límites del Free Tier de Netlify

### Incluido GRATIS:

✅ **100GB bandwidth/mes**
- Suficiente para ~10,000 usuarios activos
- Assets estáticos cacheados en edge

✅ **300 build minutes/mes**
- ~100 deploys/mes
- Builds paralelos

✅ **Sitios ilimitados**
- Múltiples proyectos en la misma cuenta

✅ **1 usuario**
- Para colaboración necesitas Pro

✅ **SSL automático**
- Let's Encrypt incluido
- Renovación automática

✅ **Forms**
- 100 submissions/mes

✅ **Functions**
- 125k invocaciones/mes
- 100 horas runtime/mes

### Límites:

⚠️ **Build time**: 300 min/mes (suficiente para ~100 builds)
⚠️ **Concurrent builds**: 1 (Pro: 3)
⚠️ **Team members**: Solo tú (Pro: ilimitados)
⚠️ **Deploy previews**: Limitados a 1,000/mes

### Cuándo upgradar a Pro ($19/mes):

- Necesitas >100GB bandwidth
- Múltiples colaboradores
- >1 build concurrent
- Analytics avanzados
- Password protection
- A/B testing

---

## 🔐 Variables de Entorno Seguras

### En Netlify

Netlify soporta diferentes contextos:

```bash
# Production
VITE_API_URL=https://api.tudominio.com

# Deploy Preview (PRs)
VITE_API_URL=https://api-staging.tudominio.com

# Branch Deploy (staging)
VITE_API_URL=https://api-staging.tudominio.com
```

**Configurar:**
1. Site settings → Environment variables
2. Click "Add a variable"
3. Selecciona el scope:
   - All deploys
   - Production only
   - Deploy previews

### En Railway

```bash
JIRA_BASE_URL=https://tu-empresa.atlassian.net
JIRA_EMAIL=tu-email@example.com
JIRA_API_TOKEN=tu_api_token  # Marca como "sensitive"
```

---

## 🚀 Workflow de Desarrollo Completo

### Ramas y Deploys

```bash
# Rama principal (production)
main → Netlify production + Railway production

# Rama de staging
staging → Netlify branch deploy + Railway staging

# Pull Requests
feature/xyz → Netlify deploy preview
```

### Setup de Staging

#### 1. Crear servicio staging en Railway

```bash
# En Railway dashboard
New service → "jira-backend-staging"
Variables: mismas que production
Branch: staging
```

#### 2. Configurar en Netlify

```toml
# netlify.toml
[context."staging"]
  command = "npm run build"
  [context."staging".environment]
    VITE_API_URL = "https://jira-backend-staging.railway.app"
```

#### 3. Proteger rama main

```bash
# En GitHub: Settings → Branches → Add rule
Branch name pattern: main
✅ Require pull request reviews before merging
✅ Require status checks to pass before merging
   - Netlify build
```

---

## 📈 Monitoreo y Analytics

### Netlify Analytics (Gratis con limitaciones)

**Free tier incluye:**
- Pageviews totales
- Top pages
- Top sources
- No tracking cookies

**Pro tier ($9/mes adicional):**
- Data retention ilimitada
- Tráfico detallado
- Bandwidth usage

### Railway Metrics (Incluido)

**Dashboard incluye:**
- CPU usage
- Memory usage
- Network I/O
- Request count
- Response times

### Alternativas Gratis

**Google Analytics:**
```html
<!-- En jira-tracker/index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Plausible Analytics (privacy-friendly):**
```html
<script defer data-domain="tudominio.com" src="https://plausible.io/js/script.js"></script>
```

---

## 🔄 CI/CD Pipeline

### Netlify Build Process

```
1. GitHub Push/PR
   ↓
2. Netlify detecta cambio
   ↓
3. Clona repo
   ↓
4. Ejecuta: npm install
   ↓
5. Ejecuta: npm run build
   ↓
6. Publica dist/ a CDN
   ↓
7. Invalida cache
   ↓
8. Deploy completo (~2 min)
```

### Railway Build Process

```
1. GitHub Push
   ↓
2. Railway detecta cambio
   ↓
3. Clona repo
   ↓
4. Ejecuta: pip install -r requirements.txt
   ↓
5. Inicia: uvicorn app.main:app
   ↓
6. Health check
   ↓
7. Switch traffic
   ↓
8. Deploy completo (~3 min)
```

---

## 🐛 Troubleshooting

### Error: "Build failed"

**Netlify:**
```bash
# Ver logs completos en Netlify dashboard
# Errores comunes:

# 1. Node version incorrecta
# Fix: Agregar .nvmrc
echo "18" > jira-tracker/.nvmrc

# 2. Build command incorrecto
# Fix en netlify.toml:
[build]
  command = "cd jira-tracker && npm ci && npm run build"

# 3. Variables de entorno faltantes
# Fix: Agregar en Site settings → Environment variables
```

**Railway:**
```bash
# Ver logs en Railway dashboard

# 1. Requirements.txt no encontrado
# Fix: Asegurar que está en la raíz

# 2. Puerto incorrecto
# Fix: Usar $PORT en uvicorn
uvicorn app.main:app --host 0.0.0.0 --port $PORT

# 3. Python version incorrecta
# Fix: Crear runtime.txt
echo "python-3.11" > runtime.txt
```

### Error: CORS

**Síntomas:**
```
Access to fetch at 'https://backend.railway.app' from origin
'https://tu-app.netlify.app' has been blocked by CORS policy
```

**Fix:**
```python
# app/main.py
allow_origins=[
    "http://localhost:5173",
    "https://tu-app.netlify.app",  # ← Agregar dominio exacto
    "https://*.netlify.app",  # O usar wildcard para branch deploys
]
```

### Error: Netlify no encuentra archivos

**Fix: Crear _redirects:**
```bash
# jira-tracker/public/_redirects
/*    /index.html   200
```

O usar `netlify.toml` (recomendado).

---

## 💰 Comparativa de Costos

### Netlify (Frontend) + Railway (Backend)

```
Mes 1-6:
├── Netlify:      $0/mes (free tier)
├── Railway:      $5/mes (backend)
└── Total:        $5/mes

Mes 7-12 (si creces):
├── Netlify:      $0/mes (aún en free tier)
├── Railway:      $10/mes (más recursos)
└── Total:        $10/mes

Año 1 total: $60-120
```

### Comparado con otras opciones:

| Opción | Costo Año 1 | Frontend | Backend |
|--------|-------------|----------|---------|
| **Netlify + Railway** | **$60** | ✅ Gratis | $5/mes |
| Vercel + Railway | $60 | ✅ Gratis | $5/mes |
| Railway solo | $120 | $5/mes | $5/mes |
| Render | $168 | $7/mes | $7/mes |
| AWS | $900+ | $10/mes | $65/mes |

---

## ✅ Checklist de Deploy

### Pre-Deploy
- [ ] Credenciales de Jira listas
- [ ] Repositorio en GitHub
- [ ] .env.example actualizado
- [ ] CORS configurado para localhost

### Netlify Setup
- [ ] Cuenta creada
- [ ] Site importado desde GitHub
- [ ] Build settings configurados
- [ ] VITE_API_URL configurada
- [ ] Deploy exitoso
- [ ] SSL activo

### Railway Setup
- [ ] Cuenta creada
- [ ] Servicio creado desde GitHub
- [ ] Variables de entorno configuradas
- [ ] Start command correcto
- [ ] Dominio generado
- [ ] Health check passing

### Post-Deploy
- [ ] CORS actualizado con dominio de Netlify
- [ ] Frontend puede listar proyectos
- [ ] Se pueden crear tareas de prueba
- [ ] SSL funcionando en ambos
- [ ] Dominios custom configurados (opcional)
- [ ] Analytics configurado (opcional)

---

## 🎯 Comandos Útiles

### Netlify CLI (Opcional)

```bash
# Instalar
npm install -g netlify-cli

# Login
netlify login

# Deploy desde local
netlify deploy

# Deploy a producción
netlify deploy --prod

# Ver logs
netlify logs

# Abrir dashboard
netlify open
```

### Railway CLI

```bash
# Instalar
npm install -g @railway/cli

# Login
railway login

# Ver logs
railway logs

# Ver variables
railway variables

# Deploy
railway up
```

---

## 📚 Recursos Adicionales

- [Netlify Docs](https://docs.netlify.com/)
- [Railway Docs](https://docs.railway.app/)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🚀 Next Steps

1. **Deploy ahora** siguiendo esta guía (15 min)
2. **Prueba la aplicación** end-to-end
3. **Configura dominio custom** (opcional)
4. **Agrega analytics** para tracking
5. **Configura staging** para desarrollo
6. **Invita a tu equipo** a probar

---

**¿Listo para deploy? Comienza con el Paso 1: Deploy Frontend en Netlify** ⬆️
