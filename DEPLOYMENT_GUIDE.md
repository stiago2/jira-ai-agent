# Guía de Deployment - Jira AI Agent

Esta guía explica cómo desplegar tanto el backend (FastAPI) como el frontend (React) de la aplicación.

## Opciones de Deployment

Tienes 3 opciones principales para desplegar la aplicación:

1. **Railway (Recomendado para MVP/Producción)** - Más fácil y rápido
2. **Docker + VPS** - Para control total
3. **Servicios Separados** - Backend en Railway, Frontend en Vercel/Netlify

---

## Opción 1: Deployment en Railway (Recomendado)

Railway es perfecto para aplicaciones full-stack con base de datos.

### Preparación

1. Crea una cuenta en [Railway.app](https://railway.app)
2. Instala Railway CLI (opcional):
   ```bash
   npm install -g @railway/cli
   railway login
   ```

### A. Desplegar Backend

#### Desde la Web UI:

1. **Crear Nuevo Proyecto**
   - Ve a Railway Dashboard
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio

2. **Configurar Variables de Entorno**

   En el dashboard de Railway, ve a Variables y agrega:

   ```bash
   # Base de datos
   DATABASE_URL=postgresql://user:password@hostname:port/dbname

   # JWT
   SECRET_KEY=tu_secret_key_super_seguro_minimo_32_caracteres
   JWT_SECRET_KEY=otro_secret_key_diferente_para_jwt
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_MINUTES=10080

   # CORS (tu dominio de frontend)
   CORS_ORIGINS=https://tu-app.vercel.app,https://www.tu-dominio.com

   # Puerto (Railway lo asigna automáticamente)
   PORT=${{RAILWAY_PUBLIC_PORT}}
   ```

3. **Configurar Build y Start**

   Railway debería detectar automáticamente el `railway.json`, pero verifica:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Agregar PostgreSQL**
   - En el proyecto, click en "+ New"
   - Selecciona "Database" → "PostgreSQL"
   - Railway creará automáticamente `DATABASE_URL`

5. **Deploy**
   - Railway detectará cambios en git y desplegará automáticamente
   - Obtén la URL del backend: `https://tu-proyecto.railway.app`

#### Desde CLI:

```bash
cd /path/to/jira-ai-agent
railway init
railway up
railway variables set SECRET_KEY="tu_secret_key_aqui"
railway variables set JWT_SECRET_KEY="otro_secret_key"
# ... agregar más variables
```

### B. Desplegar Frontend

#### Opción 1: Vercel (Recomendado para React)

1. **Instalar Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Configurar Variables de Entorno**

   Crear archivo `jira-tracker/.env.production`:
   ```bash
   REACT_APP_API_URL=https://tu-backend.railway.app
   ```

3. **Deploy**
   ```bash
   cd jira-tracker
   vercel --prod
   ```

4. **Desde Vercel Web**
   - Ve a [vercel.com](https://vercel.com)
   - Importa tu repositorio
   - Root Directory: `jira-tracker`
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Environment Variables: `REACT_APP_API_URL`

#### Opción 2: Netlify

1. **Configurar `netlify.toml`** (ya deberías tener uno)

2. **Deploy**
   ```bash
   cd jira-tracker
   npm run build
   npx netlify deploy --prod --dir=build
   ```

3. **Variables de Entorno en Netlify**
   - Site settings → Environment variables
   - Agregar: `REACT_APP_API_URL=https://tu-backend.railway.app`

---

## Opción 2: Docker + VPS (DigitalOcean, AWS, etc.)

### Preparación

1. **Servidor con Docker instalado**
   - DigitalOcean Droplet ($5/mes)
   - AWS EC2
   - Contabo VPS

2. **Dominio configurado** (opcional pero recomendado)

### Pasos de Deployment

#### 1. En tu servidor VPS:

```bash
# Conectar al servidor
ssh user@tu-servidor.com

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/jira-ai-agent.git
cd jira-ai-agent
```

#### 3. Configurar variables de entorno:

```bash
cp .env.example .env
nano .env
```

Agregar:
```bash
# Database
DATABASE_URL=sqlite:///./jira_agent.db

# JWT
SECRET_KEY=tu_secret_key_super_seguro
JWT_SECRET_KEY=otro_secret_key_diferente
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=10080

# CORS
CORS_ORIGINS=http://localhost:3000,https://tu-dominio.com

# Port
PORT=8000
```

#### 4. Build y ejecutar con Docker Compose:

```bash
# Modo producción
docker-compose -f docker-compose.production.yml up -d --build

# Ver logs
docker-compose -f docker-compose.production.yml logs -f

# Ver status
docker-compose -f docker-compose.production.yml ps
```

#### 5. Configurar Nginx como proxy reverso:

```bash
sudo apt install nginx

# Crear configuración
sudo nano /etc/nginx/sites-available/jira-agent
```

Contenido:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/jira-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 6. Configurar SSL con Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

---

## Opción 3: Servicios Separados

### Backend → Railway/Render
### Frontend → Vercel/Netlify

Esta es la opción más común y escalable:

#### Backend en Railway:
- Sigue los pasos de "Opción 1 - A"
- URL resultante: `https://backend-xxx.railway.app`

#### Frontend en Vercel:
- Sigue los pasos de "Opción 1 - B"
- Configura `REACT_APP_API_URL` con la URL de Railway
- URL resultante: `https://tu-app.vercel.app`

---

## Configuración de Base de Datos

### SQLite (Desarrollo/Pruebas)
```bash
DATABASE_URL=sqlite:///./jira_agent.db
```

### PostgreSQL (Producción Recomendado)
```bash
DATABASE_URL=postgresql://user:password@hostname:port/dbname
```

### Migraciones

Si usas PostgreSQL, necesitas ejecutar las migraciones:

```bash
# En el servidor o localmente conectado a la DB
python -c "from app.core.database import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

---

## Verificación Post-Deployment

### Backend

```bash
# Health check
curl https://tu-backend.railway.app/api/v1/health

# Debería responder:
{
  "status": "healthy",
  "jira_connection": "ok",
  "parser": "rule-based"
}
```

### Frontend

1. Visita: `https://tu-app.vercel.app`
2. Intenta registrarte con un usuario
3. Crea un proyecto
4. Verifica que las subtareas se carguen correctamente

---

## Monitoreo y Logs

### Railway
- Dashboard → Tu proyecto → Deployments → Ver logs
- Métricas automáticas de CPU, memoria, etc.

### Docker
```bash
# Ver logs del backend
docker-compose -f docker-compose.production.yml logs -f backend

# Ver logs del frontend
docker-compose -f docker-compose.production.yml logs -f frontend

# Ver stats
docker stats
```

### Herramientas Recomendadas
- **Sentry** - Error tracking
- **LogTail** - Log management
- **UptimeRobot** - Monitoring uptime

---

## Troubleshooting

### Error: CORS

**Síntoma**: Errores de CORS en el navegador

**Solución**: Verifica que `CORS_ORIGINS` incluya tu dominio del frontend:
```bash
CORS_ORIGINS=https://tu-app.vercel.app,https://www.tu-dominio.com
```

### Error: Database connection

**Síntoma**: Error al conectar a la base de datos

**Solución**:
1. Verifica `DATABASE_URL`
2. Si usas PostgreSQL, asegúrate que la DB esté accesible
3. Para Railway, verifica que el servicio de PostgreSQL esté corriendo

### Error: JWT Authentication

**Síntoma**: Tokens inválidos o expirados

**Solución**:
1. Verifica `SECRET_KEY` y `JWT_SECRET_KEY`
2. No cambies las keys en producción (invalida todos los tokens)
3. Ajusta `JWT_EXPIRATION_MINUTES` si es necesario

### Frontend no se conecta al Backend

**Síntoma**: Requests fallan, errores de red

**Solución**:
1. Verifica `REACT_APP_API_URL` en frontend
2. Asegúrate que el backend esté corriendo
3. Verifica que no haya problemas de CORS
4. Revisa que las URLs no tengan `/` al final

---

## Costos Estimados

### Opción Gratuita (Hobby)
- **Railway**: $5/mes (500 horas gratis)
- **Vercel**: Gratis (Hobby plan)
- **Total**: ~$0-5/mes

### Opción Profesional
- **Railway Pro**: $20/mes
- **Vercel Pro**: $20/mes
- **PostgreSQL dedicado**: $7/mes
- **Total**: ~$47/mes

### Opción VPS
- **DigitalOcean Droplet**: $6-12/mes
- **Dominio**: $10-15/año
- **Total**: ~$6-13/mes

---

## Comandos Útiles

### Railway
```bash
railway login
railway link
railway up
railway logs
railway variables
railway status
```

### Docker
```bash
# Build
docker-compose -f docker-compose.production.yml build

# Up
docker-compose -f docker-compose.production.yml up -d

# Down
docker-compose -f docker-compose.production.yml down

# Logs
docker-compose -f docker-compose.production.yml logs -f

# Restart
docker-compose -f docker-compose.production.yml restart
```

### Vercel
```bash
vercel login
vercel --prod
vercel logs
vercel env pull
```

---

## Seguridad

### Checklist Pre-Producción

- [ ] Variables de entorno configuradas correctamente
- [ ] Secrets (JWT, API keys) son únicos y seguros (mínimo 32 caracteres)
- [ ] CORS configurado correctamente (solo dominios permitidos)
- [ ] HTTPS habilitado (SSL/TLS)
- [ ] Base de datos con backup automático
- [ ] Rate limiting habilitado
- [ ] Logs configurados
- [ ] Health checks funcionando
- [ ] No hay secretos en el código (git secrets)

---

## Próximos Pasos Recomendados

1. **Configurar CI/CD**
   - GitHub Actions para tests automáticos
   - Deploy automático en push a `main`

2. **Monitoreo**
   - Sentry para error tracking
   - Analytics para frontend

3. **Backups**
   - Backup automático de base de datos
   - Snapshots regulares

4. **Documentación**
   - API documentation con Swagger
   - User guide

5. **Performance**
   - CDN para assets estáticos
   - Caché con Redis
   - Database indexing

---

## Soporte

Si tienes problemas durante el deployment:

1. Revisa los logs del servicio
2. Verifica las variables de entorno
3. Consulta la documentación específica de cada plataforma:
   - [Railway Docs](https://docs.railway.app/)
   - [Vercel Docs](https://vercel.com/docs)
   - [Docker Docs](https://docs.docker.com/)
