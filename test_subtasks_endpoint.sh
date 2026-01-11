#!/bin/bash

# Script de prueba para verificar que el sistema de subtareas funciona correctamente

BASE_URL="http://localhost:8000/api/v1"

echo "🧪 Testing Subtasks Endpoints"
echo "================================"
echo ""

# 1. Primero necesitamos autenticarnos
echo "1️⃣ Login with existing user..."
TEST_USERNAME="subtask_test_$(date +%s)"
TEST_PASSWORD="testpass123"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$TEST_USERNAME&password=$TEST_PASSWORD")

echo "$LOGIN_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$LOGIN_RESPONSE"
echo ""

# Extraer el token
TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "❌ Login failed. Creating new user..."

  # Crear un nuevo usuario
  REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
    -H "Content-Type: application/json" \
    -d "{
      \"username\": \"$TEST_USERNAME\",
      \"email\": \"$TEST_USERNAME@example.com\",
      \"password\": \"$TEST_PASSWORD\"
    }")

  echo "$REGISTER_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$REGISTER_RESPONSE"
  echo ""

  # Ahora hacer login con el usuario recién creado
  echo "🔑 Logging in with new user..."
  LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$TEST_USERNAME&password=$TEST_PASSWORD")

  echo "$LOGIN_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$LOGIN_RESPONSE"
  TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
fi

if [ -z "$TOKEN" ]; then
  echo "❌ Failed to get authentication token"
  exit 1
fi

echo "✅ Authentication successful! Token: ${TOKEN:0:20}..."
echo ""

# 2. Obtener subtareas (debería auto-inicializar con defaults)
echo "2️⃣ Getting user subtasks (should auto-initialize)..."
GET_RESPONSE=$(curl -s -X GET "$BASE_URL/subtasks" \
  -H "Authorization: Bearer $TOKEN")

echo "$GET_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$GET_RESPONSE"
echo ""

# 3. Crear una nueva subtarea
echo "3️⃣ Creating a new custom subtask..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/subtasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Testing",
    "emoji": "🧪",
    "description": "Quality assurance and testing",
    "labels": ["testing", "qa", "quality"]
  }')

echo "$CREATE_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$CREATE_RESPONSE"
SUBTASK_ID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)
echo ""

# 4. Actualizar la subtarea
if [ ! -z "$SUBTASK_ID" ]; then
  echo "4️⃣ Updating the subtask (ID: $SUBTASK_ID)..."
  UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/subtasks/$SUBTASK_ID" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "description": "Updated: Comprehensive testing and QA",
      "labels": ["testing", "qa", "quality", "automation"]
    }')

  echo "$UPDATE_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$UPDATE_RESPONSE"
  echo ""
fi

# 5. Listar todas las subtareas nuevamente
echo "5️⃣ Listing all subtasks again..."
LIST_RESPONSE=$(curl -s -X GET "$BASE_URL/subtasks" \
  -H "Authorization: Bearer $TOKEN")

echo "$LIST_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$LIST_RESPONSE"
echo ""

# 6. Intentar eliminar la subtarea (opcional, solo si queremos limpiar)
if [ ! -z "$SUBTASK_ID" ]; then
  echo "6️⃣ Deleting the test subtask (ID: $SUBTASK_ID)..."
  DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/subtasks/$SUBTASK_ID" \
    -H "Authorization: Bearer $TOKEN" \
    -w "\nHTTP Status: %{http_code}")

  echo "$DELETE_RESPONSE"
  echo ""
fi

echo "✅ All tests completed!"
