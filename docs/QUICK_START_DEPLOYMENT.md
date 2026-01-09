# 🚀 Quick Start - Despliegue en 10 Minutos

## Railway (Recomendado para empezar)

### Prerrequisitos
- Cuenta en [Railway.app](https://railway.app)
- Repositorio en GitHub
- Credenciales de Jira (API Token)

### Pasos

#### 1. Preparar el Repositorio (1 min)

```bash
# Asegúrate de tener todos los archivos listos
git add .
git commit -m "Preparar para deploy"
git push origin main
```

#### 2. Crear Proyecto en Railway (2 min)

1. Ve a [railway.app/new](https://railway.app/new)
2. Click "Deploy from GitHub repo"
3. Autoriza Railway a acceder a tu GitHub
4. Selecciona el repositorio `jira-ai-agent`

#### 3. Configurar Backend (3 min)

Railway creará automáticamente un servicio. Configúralo:

**Variables de entorno:**
```
JIRA_BASE_URL=https://tu-empresa.atlassian.net
JIRA_EMAIL=tu-email@example.com
JIRA_API_TOKEN=tu_api_token_aqui
PORT=8000
```

**Settings:**
- Service Name: `jira-backend`
- Start Command: `cd app && uvicorn main:app --host 0.0.0.0 --port $PORT`
- Auto-deploy: ✅ Enabled

#### 4. Configurar Frontend (2 min)

Crear un segundo servicio:

1. Click "New" → "Empty Service"
2. Conecta el mismo repositorio
3. Root Directory: `jira-tracker`

**Variables de entorno:**
```
VITE_API_URL=https://jira-backend-production.up.railway.app
```

**Settings:**
- Service Name: `jira-frontend`
- Build Command: `npm install && npm run build`
- Start Command: `npm run start`
- Auto-deploy: ✅ Enabled

#### 5. Generar Dominios (1 min)

Para cada servicio:
1. Click en Settings
2. Click "Generate Domain"
3. Copia la URL generada

Actualiza `VITE_API_URL` en el frontend con la URL del backend.

#### 6. Verificar Deploy (1 min)

**Backend:**
```bash
curl https://jira-backend-production.up.railway.app/api/v1/health
```

**Frontend:**
Abre en el navegador: `https://jira-frontend-production.up.railway.app`

---

## Docker Compose (Autohospedado)

### Prerrequisitos
- Docker y Docker Compose instalados
- Servidor con puerto 80/443 disponible

### Pasos

#### 1. Clonar y Configurar (2 min)

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/jira-ai-agent.git
cd jira-ai-agent

# Configurar variables de entorno
cp .env.example .env
nano .env  # Editar con tus credenciales
```

#### 2. Build y Deploy (5 min)

```bash
# Build de las imágenes
docker-compose -f docker-compose.production.yml build

# Iniciar servicios
docker-compose -f docker-compose.production.yml up -d

# Ver logs
docker-compose -f docker-compose.production.yml logs -f
```

#### 3. Verificar (1 min)

```bash
# Health check backend
curl http://localhost:8000/api/v1/health

# Health check frontend
curl http://localhost/health
```

#### 4. Acceder

- Frontend: http://localhost
- Backend API: http://localhost:8000

---

## Vercel (Solo Frontend)

### Prerrequisitos
- Cuenta en [Vercel](https://vercel.com)
- Backend desplegado en Railway/Render

### Pasos

#### 1. Deploy desde Vercel (3 min)

1. Ve a [vercel.com/new](https://vercel.com/new)
2. Import tu repositorio de GitHub
3. Configurar:
   - Framework Preset: `Vite`
   - Root Directory: `jira-tracker`
   - Build Command: `npm run build`
   - Output Directory: `dist`

#### 2. Variables de Entorno (1 min)

```
VITE_API_URL=https://tu-backend.railway.app
```

#### 3. Deploy (1 min)

Click "Deploy" y espera ~2 minutos.

Tu app estará en: `https://tu-proyecto.vercel.app`

---

## Checklist Post-Deploy

### Funcionalidad
- [ ] Backend responde en `/api/v1/health`
- [ ] Frontend carga correctamente
- [ ] Puedes listar proyectos de Jira
- [ ] Puedes crear una tarea de prueba
- [ ] Puedes listar usuarios del proyecto

### Seguridad
- [ ] HTTPS habilitado
- [ ] Variables de entorno configuradas
- [ ] API Token no expuesto en logs
- [ ] CORS configurado correctamente
- [ ] Headers de seguridad activos

### Performance
- [ ] Tiempo de respuesta < 2s
- [ ] Assets estáticos con caché
- [ ] Gzip habilitado
- [ ] Build optimizado (production)

### Monitoreo
- [ ] Logs accesibles
- [ ] Health checks funcionando
- [ ] Alertas configuradas (opcional)
- [ ] Métricas básicas (opcional)

---

## Solución de Problemas Comunes

### Backend no conecta con Jira

**Error:** `401 Unauthorized`

**Solución:**
1. Verifica `JIRA_BASE_URL` (sin / al final)
2. Verifica `JIRA_EMAIL` es correcto
3. Genera nuevo API Token si es necesario
4. Verifica que el token tenga permisos

### Frontend no ve el Backend

**Error:** `Network Error` o `CORS Error`

**Solución:**
1. Verifica `VITE_API_URL` apunta al backend correcto
2. Revisa configuración de CORS en `app/main.py`
3. Agrega el origen del frontend a `allow_origins`

### Build falla

**Error:** `npm ERR!` o `pip install failed`

**Solución:**
1. Elimina `node_modules` y `package-lock.json`
2. Ejecuta `npm install` de nuevo
3. Para Python, verifica `requirements.txt`
4. Limpia caché: `pip cache purge`

### Deploy lento

**Solución:**
1. Optimiza build de Vite (chunking)
2. Usa caché de dependencias
3. Reduce tamaño de imágenes Docker
4. Considera multi-stage builds

---

## Comandos Útiles

### Railway CLI

```bash
# Ver logs en tiempo real
railway logs

# Ver variables de entorno
railway variables

# Deploy manual
railway up

# Conectar a terminal del servicio
railway shell
```

### Docker

```bash
# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart servicio
docker-compose restart backend

# Rebuild
docker-compose build --no-cache backend

# Limpiar todo
docker-compose down -v
```

### Git

```bash
# Deploy a producción
git push origin main

# Revertir deploy
git revert HEAD
git push origin main
```

---

## Próximos Pasos

1. **Configurar dominio custom**
   - Compra un dominio
   - Configura DNS (CNAME)
   - Habilita SSL

2. **Agregar monitoreo**
   - Sentry para errores
   - Google Analytics
   - Uptime monitoring

3. **Optimizar performance**
   - CDN para assets
   - Redis para caché
   - Database si crece

4. **Agregar CI/CD**
   - Tests automáticos
   - Lint en pre-commit
   - Deploy staging primero

5. **Documentar API**
   - Swagger/OpenAPI habilitado
   - Ejemplos de uso
   - Postman collection

---

## Recursos

- [Documentación completa](./DEPLOYMENT_GUIDE.md)
- [Railway Docs](https://docs.railway.app/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vite Deployment](https://vitejs.dev/guide/static-deploy.html)

---

**¿Problemas? Revisa los logs primero:**
```bash
# Railway
railway logs

# Docker
docker-compose logs

# Local
tail -f app/logs/app.log
```
