#!/bin/bash

# ============================================================================
# Script de Testing de Autenticación - Jira AI Agent
# ============================================================================
# Este script prueba todos los endpoints de autenticación y protegidos
# ============================================================================

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables de configuración
API_URL="${API_URL:-http://localhost:8000}"
USERNAME="testuser_$(date +%s)"  # Username único para cada ejecución
PASSWORD="TestPassword123!"
EMAIL="test_$(date +%s)@example.com"

# Credenciales de Jira (configura las tuyas aquí)
JIRA_EMAIL="${JIRA_EMAIL:-your-jira-email@company.com}"
JIRA_TOKEN="${JIRA_TOKEN:-your-jira-api-token}"
JIRA_URL="${JIRA_URL:-https://yourcompany.atlassian.net}"
PROJECT_KEY="${PROJECT_KEY:-KAN}"

echo -e "${GREEN}============================================================================${NC}"
echo -e "${GREEN}  JIRA AI AGENT - Testing de Autenticación${NC}"
echo -e "${GREEN}============================================================================${NC}"
echo ""
echo "API URL: $API_URL"
echo "Username: $USERNAME"
echo "Email: $EMAIL"
echo ""

# Función para hacer requests con pretty print
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local auth_header=$4

    echo -e "${YELLOW}→ $method $endpoint${NC}"

    if [ -n "$auth_header" ]; then
        if [ -n "$data" ]; then
            response=$(curl -s -w "\n%{http_code}" -X "$method" "$API_URL$endpoint" \
                -H "Authorization: Bearer $auth_header" \
                -H "Content-Type: application/json" \
                -d "$data")
        else
            response=$(curl -s -w "\n%{http_code}" -X "$method" "$API_URL$endpoint" \
                -H "Authorization: Bearer $auth_header")
        fi
    else
        if [ -n "$data" ]; then
            response=$(curl -s -w "\n%{http_code}" -X "$method" "$API_URL$endpoint" \
                -H "Content-Type: application/json" \
                -d "$data")
        else
            response=$(curl -s -w "\n%{http_code}" -X "$method" "$API_URL$endpoint")
        fi
    fi

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ HTTP $http_code${NC}"
    else
        echo -e "${RED}✗ HTTP $http_code${NC}"
    fi

    echo "$body" | jq '.' 2>/dev/null || echo "$body"
    echo ""

    # Retornar el body para uso posterior
    echo "$body"
}

# ============================================================================
# 1. Health Check (Público)
# ============================================================================
echo -e "${GREEN}1. Health Check (público)${NC}"
echo "---"
make_request "GET" "/api/v1/health" "" "" > /dev/null

# ============================================================================
# 2. Auth Health Check (Público)
# ============================================================================
echo -e "${GREEN}2. Auth Health Check (público)${NC}"
echo "---"
make_request "GET" "/api/v1/auth/health" "" "" > /dev/null

# ============================================================================
# 3. Registrar Usuario
# ============================================================================
echo -e "${GREEN}3. Registrar nuevo usuario${NC}"
echo "---"
register_data=$(cat <<EOF
{
    "email": "$EMAIL",
    "username": "$USERNAME",
    "password": "$PASSWORD",
    "jira_email": "$JIRA_EMAIL",
    "jira_api_token": "$JIRA_TOKEN",
    "jira_base_url": "$JIRA_URL"
}
EOF
)

register_response=$(make_request "POST" "/api/v1/auth/register" "$register_data" "")

# ============================================================================
# 4. Login
# ============================================================================
echo -e "${GREEN}4. Login${NC}"
echo "---"
login_response=$(curl -s -X POST "$API_URL/api/v1/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$USERNAME&password=$PASSWORD")

echo "$login_response" | jq '.'

# Extraer token
TOKEN=$(echo "$login_response" | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo -e "${RED}✗ Error: No se pudo obtener el token${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Token obtenido: ${TOKEN:0:50}...${NC}"
echo ""

# ============================================================================
# 5. Obtener Info del Usuario (Protegido)
# ============================================================================
echo -e "${GREEN}5. Obtener info del usuario actual (protegido)${NC}"
echo "---"
make_request "GET" "/api/v1/auth/me" "" "$TOKEN" > /dev/null

# ============================================================================
# 6. Probar endpoint sin token (debe fallar)
# ============================================================================
echo -e "${GREEN}6. Probar endpoint protegido SIN token (debe fallar con 401)${NC}"
echo "---"
make_request "GET" "/api/v1/projects" "" "" > /dev/null

# ============================================================================
# 7. Listar Proyectos (Protegido)
# ============================================================================
echo -e "${GREEN}7. Listar proyectos de Jira (protegido)${NC}"
echo "---"
projects_response=$(make_request "GET" "/api/v1/projects" "" "$TOKEN")

# Extraer primer project_key si existe
FIRST_PROJECT=$(echo "$projects_response" | jq -r '.projects[0].key' 2>/dev/null)

if [ "$FIRST_PROJECT" != "null" ] && [ -n "$FIRST_PROJECT" ]; then
    PROJECT_KEY="$FIRST_PROJECT"
    echo -e "${GREEN}✓ Usando proyecto: $PROJECT_KEY${NC}"
    echo ""
fi

# ============================================================================
# 8. Obtener Usuarios del Proyecto (Protegido)
# ============================================================================
echo -e "${GREEN}8. Obtener usuarios del proyecto (protegido)${NC}"
echo "---"
make_request "GET" "/api/v1/projects/$PROJECT_KEY/users" "" "$TOKEN" > /dev/null

# ============================================================================
# 9. Crear Tarea Individual (Protegido)
# ============================================================================
echo -e "${GREEN}9. Crear tarea individual (protegido)${NC}"
echo "---"
task_data=$(cat <<EOF
{
    "text": "Crear reel sobre testing de autenticación en el backend",
    "project_key": "$PROJECT_KEY"
}
EOF
)

make_request "POST" "/api/v1/tasks/create" "$task_data" "$TOKEN" > /dev/null

# ============================================================================
# 10. Crear Contenido de Instagram (Protegido)
# ============================================================================
echo -e "${GREEN}10. Crear contenido de Instagram (protegido)${NC}"
echo "---"
instagram_data=$(cat <<EOF
{
    "text": "Crear reel sobre las nuevas features de autenticación",
    "description": "Video mostrando cómo funciona el login y JWT en la API",
    "project_key": "$PROJECT_KEY"
}
EOF
)

make_request "POST" "/api/v1/content/instagram" "$instagram_data" "$TOKEN" > /dev/null

# ============================================================================
# 11. Crear Batch de Tareas (Protegido)
# ============================================================================
echo -e "${GREEN}11. Crear batch de tareas (protegido)${NC}"
echo "---"
batch_data=$(cat <<EOF
{
    "project_key": "$PROJECT_KEY",
    "tasks": [
        {
            "text": "Crear reel sobre beaches de Cartagena"
        },
        {
            "text": "Crear carrusel de tips de viaje"
        }
    ]
}
EOF
)

make_request "POST" "/api/v1/tasks/batch" "$batch_data" "$TOKEN" > /dev/null

# ============================================================================
# 12. Logout
# ============================================================================
echo -e "${GREEN}12. Logout${NC}"
echo "---"
make_request "POST" "/api/v1/auth/logout" "" "$TOKEN" > /dev/null

# ============================================================================
# Resumen Final
# ============================================================================
echo -e "${GREEN}============================================================================${NC}"
echo -e "${GREEN}  ✅ Testing Completado${NC}"
echo -e "${GREEN}============================================================================${NC}"
echo ""
echo "Usuario creado: $USERNAME"
echo "Email: $EMAIL"
echo "Token generado: ${TOKEN:0:50}..."
echo ""
echo -e "${YELLOW}Nota: El token expira en 24 horas (configurable con ACCESS_TOKEN_EXPIRE_MINUTES)${NC}"
echo ""
echo -e "${GREEN}Próximos pasos:${NC}"
echo "1. Verifica las tareas creadas en Jira: $JIRA_URL"
echo "2. Puedes usar el token para hacer más requests"
echo "3. Prueba la documentación interactiva: $API_URL/docs"
echo ""
