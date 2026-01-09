# Ejemplos de Descripción de Tareas

## Ejemplo 1: Sin descripción personalizada

### Input:
```python
service.create_reel_workflow(
    project_key="KAN",
    title="Tips de fotografía en viajes",
    content_type="Carrusel",
    priority="High"
)
```

### Resultado en Jira:

**Título de la tarea:**
```
🎠 Carrusel IG | Tips de fotografía en viajes
```

**Descripción de la tarea:**
```
📹 PROYECTO: Carrusel - Tips de fotografía en viajes

🎯 WORKFLOW DE PRODUCCIÓN:
1. 🎬 Selección de tomas - Organización del material
2. ✂️ Edición - Montaje del video
3. 🎵 Diseño sonoro - Audio y música
4. 🎨 Color - Corrección y gradación de color
5. ✍️ Copy / Caption - Redacción de texto
6. 📤 Export - Exportación final

📊 SEGUIMIENTO:
- Cada fase tiene su propia subtarea
- Completa las subtareas en orden
- El proyecto estará listo cuando todas las subtareas estén completas

🤖 Creado automáticamente por Jira AI Agent
```

---

## Ejemplo 2: Con descripción personalizada

### Input:
```python
service.create_reel_workflow(
    project_key="KAN",
    title="Guía de restaurantes en Bogotá",
    content_type="Carrusel",
    priority="High",
    description="Serie de 10 imágenes mostrando los mejores restaurantes de la zona T con precios, menú estrella y tips para reservar. Incluir: Andrés Carne de Res, Harry Sasson, Leo, etc."
)
```

### Resultado en Jira:

**Título de la tarea:**
```
🎠 Carrusel IG | Guía de restaurantes en Bogotá
```

**Descripción de la tarea:**
```
📹 PROYECTO: Carrusel - Guía de restaurantes en Bogotá

📝 DESCRIPCIÓN:
Serie de 10 imágenes mostrando los mejores restaurantes de la zona T con precios, menú estrella y tips para reservar. Incluir: Andrés Carne de Res, Harry Sasson, Leo, etc.

🎯 WORKFLOW DE PRODUCCIÓN:
1. 🎬 Selección de tomas - Organización del material
2. ✂️ Edición - Montaje del video
3. 🎵 Diseño sonoro - Audio y música
4. 🎨 Color - Corrección y gradación de color
5. ✍️ Copy / Caption - Redacción de texto
6. 📤 Export - Exportación final

📊 SEGUIMIENTO:
- Cada fase tiene su propia subtarea
- Completa las subtareas en orden
- El proyecto estará listo cuando todas las subtareas estén completas

🤖 Creado automáticamente por Jira AI Agent
```

---

## Ejemplo 3: Usando el API con lenguaje natural

### Request:
```bash
curl -X POST "http://localhost:8000/api/v1/instagram" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Crear carrusel de 10 destinos imperdibles en Colombia, incluir costos aproximados y mejor época para visitar cada lugar",
    "project_key": "KAN"
  }'
```

### Resultado en Jira:

**Título de la tarea:**
```
🎠 Carrusel IG | 10 destinos imperdibles en Colombia, incluir costos aproximados y mejor época para visitar cada lugar
```

**Descripción de la tarea:**
```
📹 PROYECTO: Carrusel - 10 destinos imperdibles en Colombia, incluir costos aproximados y mejor época para visitar cada lugar

🎯 WORKFLOW DE PRODUCCIÓN:
1. 🎬 Selección de tomas - Organización del material
2. ✂️ Edición - Montaje del video
3. 🎵 Diseño sonoro - Audio y música
4. 🎨 Color - Corrección y gradación de color
5. ✍️ Copy / Caption - Redacción de texto
6. 📤 Export - Exportación final

📊 SEGUIMIENTO:
- Cada fase tiene su propia subtarea
- Completa las subtareas en orden
- El proyecto estará listo cuando todas las subtareas estén completas

🤖 Creado automáticamente por Jira AI Agent
```

---

## Resumen de la Estructura

La descripción de cada tarea principal ahora tiene una estructura clara y separada:

### 1. **PROYECTO** (siempre presente)
- Muestra el tipo de contenido y el título
- Formato: `📹 PROYECTO: {content_type} - {title}`

### 2. **DESCRIPCIÓN** (opcional)
- Solo aparece si se proporciona un `description` en la llamada
- Útil para agregar contexto adicional, requisitos específicos, etc.
- Formato: `📝 DESCRIPCIÓN:\n{custom_description}`

### 3. **WORKFLOW DE PRODUCCIÓN** (siempre presente)
- Lista las 6 fases del workflow
- Cada fase tiene su emoji identificador

### 4. **SEGUIMIENTO** (siempre presente)
- Instrucciones sobre cómo usar las subtareas
- Mensaje de creación automática

---

## Ventajas de esta Estructura

✅ **Claridad**: El título y la descripción están claramente separados
✅ **Consistencia**: Todas las tareas tienen el mismo formato
✅ **Flexibilidad**: La descripción personalizada es opcional
✅ **Organización**: Fácil de leer y entender el flujo de trabajo
✅ **Trazabilidad**: Se puede identificar fácilmente el tipo de contenido y el proyecto
