# Deployment en Render (Plan Gratuito)

Guía paso a paso para desplegar el backend y frontend en Render.

## 📋 Requisitos Previos

- Cuenta en [Render](https://render.com) (gratis)
- Repositorio en GitHub/GitLab
- Cuenta en Vercel para el frontend (o también puedes usar Render)

---

## 🚀 Parte 1: Desplegar Backend en Render

### Opción A: Desde el Dashboard (Recomendado)

#### 1. Crear Web Service

1. Ve a [render.com](https://render.com) y haz login
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub/GitLab
4. Selecciona el repositorio `jira-ai-agent`

#### 2. Configurar el Web Service

En la página de configuración:

**Basic Settings:**
- **Name**: `jira-ai-agent-backend` (o el nombre que prefieras)
- **Region**: Oregon (US West) - más cercano y rápido
- **Branch**: `main`
- **Root Directory**: dejar vacío (es la raíz del proyecto)
- **Environment**: `Python 3`
- **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

**Advanced Settings:**
- **Plan**: `Free`
- **Auto-Deploy**: `Yes` (se despliega automáticamente con cada push)

#### 3. Configurar Variables de Entorno

En la sección **Environment Variables**, agrega:

```bash
# Python Version
PYTHON_VERSION=3.11.0

# JWT Settings (puedes generar valores aleatorios)
SECRET_KEY=tu_secret_key_super_seguro_minimo_32_caracteres_aqui
JWT_SECRET_KEY=otro_secret_key_diferente_para_jwt_minimo_32_caracteres
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=10080

# CORS - IMPORTANTE: Actualizar después con la URL de tu frontend
CORS_ORIGINS=http://localhost:3000

# Database - Lo configuraremos en el siguiente paso
# DATABASE_URL se agregará automáticamente cuando creemos la DB
```

**Para generar SECRET_KEY y JWT_SECRET_KEY seguros:**
```bash
# En tu terminal local, ejecuta:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Copia el resultado para SECRET_KEY

python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Copia el resultado para JWT_SECRET_KEY (diferente al anterior)
```

#### 4. Crear PostgreSQL Database

1. En el Dashboard de Render, click en **"New +"** → **"PostgreSQL"**
2. Configuración:
   - **Name**: `jira-ai-agent-db`
   - **Database**: `jira_agent`
   - **User**: `jira_agent_user` (se genera automáticamente)
   - **Region**: Oregon (US West) - **MISMO que el backend**
   - **Plan**: `Free`

3. Click en **"Create Database"**

4. Espera a que la base de datos esté lista (aparecerá como "Available")

#### 5. Conectar Database al Backend

1. Ve al servicio web que creaste (`jira-ai-agent-backend`)
2. Click en **"Environment"** en el menú izquierdo
3. Agrega nueva variable de entorno:
   - **Key**: `DATABASE_URL`
   - **Value**: Click en el selector y escoge tu database `jira-ai-agent-db` → selecciona `Internal Database URL`

Render conectará automáticamente tu backend con la base de datos.

#### 6. Deploy

1. Click en **"Create Web Service"** o **"Manual Deploy"** si ya lo creaste
2. Render comenzará a construir y desplegar tu aplicación
3. Espera 5-10 minutos (el plan gratuito es más lento)
4. Una vez completado, verás el estado como **"Live"**

#### 7. Obtener URL del Backend

Tu backend estará disponible en:
```
https://jira-ai-agent-backend.onrender.com
```
(Render te mostrará la URL exacta en el dashboard)

#### 8. Verificar que Funcione

```bash
# Desde tu terminal:
curl https://jira-ai-agent-backend.onrender.com/api/v1/health

# Debería responder:
{
  "status": "healthy",
  "jira_connection": "ok",
  "parser": "rule-based"
}
```

---

## 🎨 Parte 2: Desplegar Frontend en Vercel

### 1. Preparar Variables de Entorno

Crea el archivo de producción:

```bash
cd jira-tracker
cp .env.production.example .env.production
```

Edita `.env.production`:
```bash
REACT_APP_API_URL=https://jira-ai-agent-backend.onrender.com
```

**IMPORTANTE**: No incluyas `/` al final de la URL.

### 2. Deploy en Vercel

#### Opción A: Desde el CLI (Rápido)

```bash
# Instalar Vercel CLI si no lo tienes
npm install -g vercel

# Desde el directorio jira-tracker
cd jira-tracker

# Login en Vercel
vercel login

# Deploy
vercel --prod
```

Durante el proceso, Vercel te preguntará:
- **Set up and deploy**: Yes
- **Which scope**: Tu cuenta personal
- **Link to existing project**: No
- **Project name**: `jira-ai-agent` (o el que prefieras)
- **In which directory is your code located**: `./`
- **Override settings**: No (usa las por defecto)

#### Opción B: Desde el Dashboard

1. Ve a [vercel.com](https://vercel.com)
2. Click en **"Add New"** → **"Project"**
3. Importa tu repositorio de GitHub
4. Configuración:
   - **Root Directory**: `jira-tracker`
   - **Framework Preset**: Create React App
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

5. **Environment Variables**:
   - Key: `REACT_APP_API_URL`
   - Value: `https://jira-ai-agent-backend.onrender.com`

6. Click en **"Deploy"**

### 3. Obtener URL del Frontend

Tu frontend estará en:
```
https://jira-ai-agent.vercel.app
```
(Vercel te mostrará la URL exacta)

---

## 🔗 Parte 3: Conectar Backend y Frontend

### 1. Actualizar CORS en Backend

1. Ve al dashboard de Render
2. Selecciona tu backend web service
3. Ve a **"Environment"**
4. Edita la variable `CORS_ORIGINS`:
   ```
   https://jira-ai-agent.vercel.app
   ```

5. Guarda los cambios
6. Render redesplegará automáticamente el backend

### 2. Verificar Conexión

1. Visita tu frontend: `https://jira-ai-agent.vercel.app`
2. Intenta registrarte con un nuevo usuario
3. Crea un proyecto
4. Verifica que todo funcione correctamente

---

## ⚠️ Limitaciones del Plan Gratuito de Render

### Backend (Web Service Free)

- ⏰ **Suspensión por inactividad**: Se suspende después de 15 minutos sin requests
- 🐌 **Arranque lento**: Tarda ~30-60 segundos en despertar (cold start)
- 💾 **750 horas/mes**: Suficiente para desarrollo/demo
- 📊 **512 MB RAM**: Adecuado para este proyecto
- 🔄 **Build time**: 10-15 minutos

### Base de Datos PostgreSQL Free

- 💾 **1 GB de almacenamiento**
- 🔄 **90 días de retención**: La DB expira después de 90 días (deberás recrearla)
- ⚡ **Conexiones limitadas**: 100 conexiones concurrentes

### Soluciones para Cold Start

**Opción 1: Ping Service (Recomendado)**
Usa un servicio gratuito como [UptimeRobot](https://uptimerobot.com) para hacer ping a tu backend cada 5-10 minutos:

1. Crea cuenta en UptimeRobot
2. Agrega monitor HTTP(S)
3. URL: `https://jira-ai-agent-backend.onrender.com/api/v1/health`
4. Interval: 5 minutos
5. Esto mantiene tu servicio activo

**Opción 2: Cron Job desde Vercel**
Puedes configurar una función serverless en Vercel que haga ping al backend periódicamente.

---

## 🔧 Troubleshooting

### Backend no responde

**Síntoma**: Error 503 o timeout

**Solución**:
1. Espera 60 segundos (cold start)
2. Revisa los logs en Render Dashboard → Tu servicio → Logs
3. Verifica que el build haya sido exitoso

### Error de CORS

**Síntoma**: En el navegador ves errores como "CORS policy blocked"

**Solución**:
1. Verifica `CORS_ORIGINS` en Render incluya la URL exacta del frontend
2. No incluyas `/` al final
3. Espera a que Render redesplegue (2-3 minutos)

### Database Connection Error

**Síntoma**: Error 500, logs muestran "database connection failed"

**Solución**:
1. Verifica que la database esté en estado "Available"
2. Verifica que `DATABASE_URL` esté configurada correctamente
3. Revisa que database y backend estén en la misma región

### Frontend no conecta al Backend

**Síntoma**: Requests fallan, no se puede registrar/login

**Solución**:
1. Verifica `REACT_APP_API_URL` en Vercel (Settings → Environment Variables)
2. Asegúrate que no tenga `/` al final
3. Verifica que el backend esté respondiendo:
   ```bash
   curl https://tu-backend.onrender.com/api/v1/health
   ```
4. Redeploy en Vercel si cambiaste variables de entorno

### Build Failed

**Backend:**
- Revisa que `requirements.txt` exista
- Verifica la versión de Python (3.11.0)
- Revisa los logs en Render

**Frontend:**
- Verifica que todas las dependencias estén en `package.json`
- Revisa que el directorio raíz sea `jira-tracker`
- Verifica los logs en Vercel

---

## 📊 Monitoreo

### Backend (Render)

1. Ve a tu servicio en Render Dashboard
2. **Logs**: Ver logs en tiempo real
3. **Metrics**: CPU, memoria, requests
4. **Events**: Historial de deploys

### Frontend (Vercel)

1. Ve a tu proyecto en Vercel Dashboard
2. **Analytics**: Pageviews, visitors (requiere upgrade)
3. **Logs**: Function logs
4. **Deployments**: Historial de deploys

---

## 🔐 Seguridad

### Checklist Pre-Producción

- [ ] `SECRET_KEY` y `JWT_SECRET_KEY` son únicos y seguros (mínimo 32 caracteres)
- [ ] `CORS_ORIGINS` solo incluye dominios permitidos
- [ ] Variables de entorno no están en el código (git secrets)
- [ ] HTTPS habilitado (Render y Vercel lo incluyen por defecto)
- [ ] Database tiene backups configurados (limitado en free tier)

---

## 💰 Costos

### Plan Actual: 100% Gratuito

- **Render Backend**: Gratis (con limitaciones)
- **Render PostgreSQL**: Gratis (90 días)
- **Vercel Frontend**: Gratis (Hobby plan)
- **Total**: $0/mes

### Upgrade Recomendado (Producción)

- **Render Starter**: $7/mes (sin suspensión, más rápido)
- **Render PostgreSQL**: $7/mes (persistente)
- **Vercel Pro**: $20/mes (analytics, más features)
- **Total**: ~$14-34/mes

---

## 📚 Recursos Útiles

- [Render Docs](https://render.com/docs)
- [Render Free Tier](https://render.com/docs/free)
- [Vercel Docs](https://vercel.com/docs)
- [PostgreSQL Best Practices](https://render.com/docs/databases)

---

## 🎯 Próximos Pasos Recomendados

1. **Configurar UptimeRobot** para mantener el backend activo
2. **Configurar custom domain** (opcional)
3. **Agregar Sentry** para error tracking
4. **Configurar backups** de la base de datos
5. **Agregar CI/CD** con GitHub Actions

---

## ✅ Deployment Completado

¡Tu aplicación está en producción! 🚀

**URLs:**
- Backend: `https://jira-ai-agent-backend.onrender.com`
- Frontend: `https://jira-ai-agent.vercel.app`

**Notas Importantes:**
- El backend puede tardar ~60 segundos en responder la primera vez (cold start)
- Configura UptimeRobot para mantenerlo activo
- La base de datos expira en 90 días en el plan gratuito
