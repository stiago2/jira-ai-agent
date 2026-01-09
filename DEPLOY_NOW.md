# 🚀 DEPLOY AHORA

## 🎯 Elige tu Opción

### Opción A: 100% GRATIS (Netlify + Render Free) ⭐
- **Costo: $0/mes**
- **Setup: 20 minutos**
- ⚠️ Backend duerme después de 15min (primera carga lenta)
- ✅ Solución: Keep-alive con UptimeRobot
- [Ver guía completa →](#opción-a-100-gratis-netlify--render-free)

### Opción B: $5/mes (Netlify + Railway) ⭐⭐⭐
- **Costo: $5/mes**
- **Setup: 15 minutos**
- ✅ Sin sleep, siempre rápido
- ✅ Mejor performance
- [Ver guía completa →](#opción-b-5mes-netlify--railway)

---

## 🆓 Opción A: 100% GRATIS (Netlify + Render Free)

### ✅ Por qué elegir esta opción:
- **Completamente GRATIS** para siempre
- **Frontend en Netlify** (100GB bandwidth, SSL, CDN)
- **Backend en Render Free** (512MB RAM, SSL)
- **Keep-alive con UptimeRobot** (evita sleep)
- **Costo total: $0/mes**

### ⚠️ Limitación:
- Backend duerme después de 15 min inactividad
- Primera request toma 30-60 segundos
- Después funciona normal

### 📋 Setup 100% Gratis (20 minutos)

#### Parte 1: Frontend en Netlify (5 min)

1. Ve a [netlify.com](https://www.netlify.com)
2. "Sign up" con GitHub
3. "Add new site" → "Import existing project"
4. Selecciona repo `jira-ai-agent`
5. Config:
   ```
   Base directory: jira-tracker
   Build command: npm run build
   Publish directory: jira-tracker/dist
   ```
6. Variable de entorno (temporal):
   ```
   VITE_API_URL=http://localhost:8000
   ```
7. Deploy → Copia URL

#### Parte 2: Backend en Render Free (10 min)

1. Ve a [render.com](https://render.com)
2. "Get Started for Free" → Sign up con GitHub
3. "New" → "Web Service"
4. Connect repo `jira-ai-agent`
5. Config:
   ```
   Name: jira-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: cd app && uvicorn main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free ← IMPORTANTE
   ```
6. Variables de entorno:
   ```
   JIRA_BASE_URL=https://tu-empresa.atlassian.net
   JIRA_EMAIL=tu-email@example.com
   JIRA_API_TOKEN=tu_token
   ```
7. "Create Web Service"
8. Espera 3-5 min → Copia URL

#### Parte 3: Keep-Alive con UptimeRobot (3 min)

1. Ve a [uptimerobot.com](https://uptimerobot.com)
2. Sign up (gratis, sin tarjeta)
3. "Add New Monitor"
4. Config:
   ```
   Monitor Type: HTTP(s)
   Friendly Name: Jira Backend
   URL: https://tu-backend.onrender.com/api/v1/health
   Monitoring Interval: 5 minutes
   ```
5. "Create Monitor" ✅

**Esto mantiene tu backend despierto 24/7**

#### Parte 4: Conectar (2 min)

1. Actualizar CORS en `app/main.py`:
   ```python
   allow_origins=[
       "http://localhost:5173",
       "https://tu-app.netlify.app",  # Tu URL de Netlify
   ]
   ```
2. Push cambios → Render auto-redeploya
3. Actualizar Netlify variable:
   ```
   VITE_API_URL=https://tu-backend.onrender.com
   ```
4. Trigger deploy en Netlify

**✅ ¡App 100% gratis en producción!**

---

## 💰 Opción B: $5/mes (Netlify + Railway)

### ✅ Por qué elegir esta opción:
- **Frontend GRATIS** en Netlify
- **Backend $5/mes** en Railway
- **Sin sleep** - siempre rápido ⚡
- **Mejor performance**
- **Setup en 15 minutos**
- **Costo total: $5/mes**

---

## 📋 Checklist Rápido

### Antes de empezar:
- [ ] Cuenta GitHub con el repo
- [ ] Credenciales de Jira listas:
  - `JIRA_BASE_URL` (ej: https://tu-empresa.atlassian.net)
  - `JIRA_EMAIL` (tu email)
  - `JIRA_API_TOKEN` ([obtener aquí](https://id.atlassian.com/manage-profile/security/api-tokens))

---

## 🎯 Parte 1: Backend en Railway (5 minutos)

### Paso 1: Crear cuenta
1. Ve a [railway.app](https://railway.app)
2. "Login" con GitHub
3. Autoriza Railway

### Paso 2: Deploy
1. "New Project" → "Deploy from GitHub repo"
2. Selecciona `jira-ai-agent`
3. Railway auto-detecta FastAPI ✅

### Paso 3: Configurar variables
En el dashboard de Railway, agrega estas variables:

```bash
JIRA_BASE_URL=https://tu-empresa.atlassian.net
JIRA_EMAIL=tu-email@example.com
JIRA_API_TOKEN=tu_token_aqui
PORT=8000
```

### Paso 4: Configurar start command
Settings → Start Command:
```bash
cd app && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Paso 5: Generar dominio
1. Settings → "Generate Domain"
2. **COPIA LA URL** (ej: `https://jira-backend-production.up.railway.app`)
3. La necesitarás en el siguiente paso ⬇️

---

## 🎨 Parte 2: Frontend en Netlify (5 minutos)

### Paso 1: Crear cuenta
1. Ve a [netlify.com](https://www.netlify.com)
2. "Sign up" con GitHub
3. Autoriza Netlify

### Paso 2: Import site
1. "Add new site" → "Import an existing project"
2. GitHub → Selecciona `jira-ai-agent`

### Paso 3: Configurar build
Netlify auto-detecta, pero verifica:

```yaml
Base directory: jira-tracker
Build command: npm run build
Publish directory: jira-tracker/dist
```

### Paso 4: Variable de entorno
Antes de deploy, agrega:

```bash
VITE_API_URL=https://jira-backend-production.up.railway.app
```
*(Pega la URL que copiaste de Railway)*

### Paso 5: Deploy
1. Click "Deploy site"
2. Espera ~2 minutos ⏱️
3. **COPIA LA URL** de Netlify (ej: `https://random-name-123456.netlify.app`)

---

## 🔗 Parte 3: Conectar ambos (5 minutos)

### Paso 1: Actualizar CORS
Edita `app/main.py` localmente:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://random-name-123456.netlify.app",  # ← TU URL DE NETLIFY
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Paso 2: Push cambios
```bash
git add app/main.py
git commit -m "Add Netlify CORS"
git push origin main
```

Railway auto-deploya en ~1 minuto ✅

### Paso 3: Re-deploy Netlify (si es necesario)
Si la URL de Railway cambió:
1. Site settings → Environment variables
2. Actualiza `VITE_API_URL`
3. Deploys → "Trigger deploy"

---

## ✅ Verificación (2 minutos)

### 1. Backend funcionando
Abre en navegador:
```
https://jira-backend-production.up.railway.app/api/v1/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "jira_connection": "ok",
  "jira_user": "Tu Nombre"
}
```

### 2. Frontend funcionando
Abre tu URL de Netlify:
```
https://random-name-123456.netlify.app
```

Deberías ver la app cargada ✅

### 3. Integración completa
1. En la app, ve a la página principal
2. Deberías ver la lista de proyectos de Jira
3. Crea una tarea de prueba
4. Verifica que aparece en Jira ✅

---

## 🎉 ¡Listo! Tu app está en producción

### URLs finales:
- **Frontend**: `https://random-name-123456.netlify.app`
- **Backend**: `https://jira-backend-production.up.railway.app`
- **Costo**: $5/mes (solo Railway, Netlify gratis)

---

## 🎨 Bonus: Dominio Custom (Opcional)

### Si tienes un dominio:

**Para el frontend:**
1. Netlify: Domain settings → "Add custom domain"
2. Configura DNS:
   ```
   app.tudominio.com → CNAME → random-name-123456.netlify.app
   ```
3. SSL automático en 24h

**Para el backend:**
1. Railway: Settings → "Add custom domain"
2. Configura DNS:
   ```
   api.tudominio.com → CNAME → jira-backend-production.up.railway.app
   ```
3. SSL automático

**Actualiza CORS y variables con los nuevos dominios.**

---

## 🐛 ¿Problemas?

### Error: "CORS blocked"
**Fix:** Asegúrate de agregar el dominio exacto de Netlify a `allow_origins`

### Error: "Network Error"
**Fix:** Verifica que `VITE_API_URL` apunta a la URL correcta de Railway

### Error: "401 Unauthorized"
**Fix:** Verifica credenciales de Jira en Railway

### Build falla
**Fix:**
- Netlify: Verifica que `jira-tracker` sea el base directory
- Railway: Verifica que `requirements.txt` existe en la raíz

---

## 📚 Documentación Completa

Para más detalles, revisa:
- [Guía completa de Netlify](./docs/NETLIFY_DEPLOYMENT.md)
- [Guía de despliegue general](./docs/DEPLOYMENT_GUIDE.md)
- [Comparativa de costos](./docs/COST_COMPARISON.md)

---

## 🚀 Próximos Pasos

1. ✅ **Configurar dominio custom** (opcional pero recomendado)
2. ✅ **Agregar Google Analytics** para tracking
3. ✅ **Configurar alertas** en Railway/Netlify
4. ✅ **Crear branch staging** para desarrollo
5. ✅ **Invitar a tu equipo** a usar la app

---

## 💰 Costo Total

```
Mes 1-6:  $5/mes  ($30 total)
Mes 7-12: $8/mes  ($48 total después)
Año 1:    $84 total

Netlify: GRATIS ✅
Railway: $5/mes ✅
```

**Comparado con:**
- AWS: $900+/año ❌
- DigitalOcean: $144/año
- Render: $168/año
- VPS + DevOps time: $1,058+/año ❌

---

**¿Todo funcionando? 🎉 ¡Felicidades! Tu Jira AI Agent está en producción.**

**¿Problemas?** Abre un issue en GitHub o revisa la documentación completa.
