# Próximos Pasos para Deployment

## Estado Actual ✅

Tu aplicación está lista para ser desplegada. Todos los archivos de configuración y scripts han sido creados:

- ✅ `DEPLOYMENT_GUIDE.md` - Guía completa de deployment
- ✅ `deploy_railway.sh` - Script para desplegar backend
- ✅ `jira-tracker/deploy_vercel.sh` - Script para desplegar frontend
- ✅ `.env.production.example` - Template de variables de entorno
- ✅ `railway.json` - Configuración de Railway

## Pasos Rápidos para Deployment

### Opción Recomendada: Railway (Backend) + Vercel (Frontend)

#### 1. Desplegar Backend en Railway

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Ejecutar script de deployment
./deploy_railway.sh
```

El script te guiará para:
- Login en Railway
- Crear proyecto
- Configurar variables de entorno
- Desplegar automáticamente

**Variables de entorno que necesitas configurar en Railway:**
- `DATABASE_URL` (Railway lo crea automáticamente si agregas PostgreSQL)
- `SECRET_KEY` (mínimo 32 caracteres aleatorios)
- `JWT_SECRET_KEY` (diferente de SECRET_KEY)
- `JWT_ALGORITHM=HS256`
- `JWT_EXPIRATION_MINUTES=10080`
- `CORS_ORIGINS` (tu dominio de frontend, ejemplo: https://tu-app.vercel.app)
- `PORT=${{RAILWAY_PUBLIC_PORT}}` (Railway lo configura automáticamente)

#### 2. Agregar PostgreSQL en Railway

En el dashboard de Railway:
1. Click en "+ New"
2. Selecciona "Database" → "PostgreSQL"
3. Railway creará automáticamente la variable `DATABASE_URL`

#### 3. Desplegar Frontend en Vercel

```bash
# Instalar Vercel CLI
npm install -g vercel

# Crear archivo de variables de entorno
cd jira-tracker
cp .env.production.example .env.production

# Editar .env.production con la URL de tu backend
nano .env.production
# Cambiar: REACT_APP_API_URL=https://tu-backend.railway.app

# Ejecutar script de deployment
./deploy_vercel.sh
```

#### 4. Verificar Deployment

**Backend:**
```bash
curl https://tu-backend.railway.app/api/v1/health
```

Debería responder:
```json
{
  "status": "healthy",
  "jira_connection": "ok",
  "parser": "rule-based"
}
```

**Frontend:**
- Visita: `https://tu-app.vercel.app`
- Intenta registrarte
- Crea un proyecto
- Verifica que todo funcione correctamente

## Configuración Importante de CORS

Una vez tengas ambas URLs (backend y frontend), asegúrate de:

1. **En Railway** - Actualizar variable `CORS_ORIGINS`:
```bash
railway variables set CORS_ORIGINS="https://tu-app.vercel.app,https://www.tu-dominio.com"
```

2. **En Vercel** - Verificar que `REACT_APP_API_URL` apunte al backend correcto

## Alternativa: Deployment Manual desde Dashboard

### Railway (Backend)

1. Ve a [railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Conecta tu repositorio
4. Agrega PostgreSQL: "+ New" → "Database" → "PostgreSQL"
5. Configura variables de entorno en el dashboard
6. Railway desplegará automáticamente

### Vercel (Frontend)

1. Ve a [vercel.com](https://vercel.com)
2. "Import Project"
3. Conecta tu repositorio
4. Root Directory: `jira-tracker`
5. Build Command: `npm run build`
6. Output Directory: `build`
7. Environment Variables: `REACT_APP_API_URL=https://tu-backend.railway.app`
8. Deploy

## Troubleshooting Común

### Error: CORS
Si ves errores de CORS en el navegador:
- Verifica que `CORS_ORIGINS` en Railway incluya tu dominio de frontend
- No incluyas `/` al final de las URLs

### Error: Base de datos
Si el backend no puede conectar a la DB:
- Verifica que PostgreSQL esté corriendo en Railway
- Verifica que `DATABASE_URL` esté configurada correctamente

### Frontend no conecta al Backend
- Verifica `REACT_APP_API_URL` en Vercel
- Asegúrate que no tenga `/` al final
- Verifica que el backend esté respondiendo

## Recursos Útiles

- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- **Guía completa**: Ver `DEPLOYMENT_GUIDE.md` para más opciones

## Costos Estimados

### Plan Gratuito/Hobby
- Railway: $5/mes (500 horas gratis iniciales)
- Vercel: Gratis (Hobby plan)
- **Total**: ~$0-5/mes

## Soporte

Si tienes problemas:
1. Revisa los logs en Railway/Vercel dashboard
2. Consulta `DEPLOYMENT_GUIDE.md`
3. Verifica las variables de entorno

---

**¡Tu aplicación está lista para producción!** 🚀
