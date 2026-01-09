# Análisis: Implementación de Sistema de Login

## 📋 Índice
1. [Contexto Actual](#contexto-actual)
2. [Opciones de Autenticación](#opciones-de-autenticación)
3. [Arquitectura Recomendada](#arquitectura-recomendada)
4. [Implementación Detallada](#implementación-detallada)
5. [Estimación de Esfuerzo](#estimación-de-esfuerzo)
6. [Consideraciones de Seguridad](#consideraciones-de-seguridad)

---

## 🔍 Contexto Actual

### Estado Actual de la Aplicación

**Backend (FastAPI):**
- Sin autenticación
- Todos los endpoints son públicos
- Usa credenciales de Jira hardcodeadas (variables de entorno)
- No hay concepto de "usuarios" en la aplicación

**Frontend (React):**
- Sin sistema de login
- Acceso directo a todos los proyectos
- No hay sesiones ni tokens

**Problema:**
- Cualquiera con la URL puede usar la aplicación
- No hay control de acceso
- No hay auditoría de quién crea qué tareas

---

## 🎯 Opciones de Autenticación

### Opción 1: JWT (JSON Web Tokens) - ⭐⭐⭐ RECOMENDADA

**Ventajas:**
- ✅ Stateless (no requiere almacenar sesiones en servidor)
- ✅ Funciona perfecto con arquitectura REST
- ✅ Fácil de implementar con FastAPI
- ✅ Tokens pueden expirar automáticamente
- ✅ Funciona bien en ambientes distribuidos (Render Free)
- ✅ No requiere base de datos para sesiones

**Desventajas:**
- ⚠️ No se pueden revocar tokens antes de expiración (sin lista negra)
- ⚠️ Token más grande que session ID

**Ideal para:** Tu caso de uso actual (aplicación pequeña, despliegue gratuito)

---

### Opción 2: OAuth 2.0 con Google/Microsoft

**Ventajas:**
- ✅ Los usuarios usan sus cuentas existentes
- ✅ No manejas contraseñas
- ✅ Más seguro (delegas autenticación)
- ✅ Mejor experiencia de usuario

**Desventajas:**
- ⚠️ Requiere registro de aplicación en Google/Microsoft
- ⚠️ Más complejo de implementar
- ⚠️ Dependes de servicios externos

**Ideal para:** Empresas que ya usan Google Workspace o Microsoft 365

---

### Opción 3: Sesiones con Cookies

**Ventajas:**
- ✅ Fácil de entender
- ✅ Se pueden revocar inmediatamente

**Desventajas:**
- ⚠️ Requiere base de datos o Redis para almacenar sesiones
- ⚠️ Problemas con CORS y cookies cross-domain
- ⚠️ No funciona bien con múltiples instancias del backend
- ⚠️ Render Free tiene disco efímero

**Ideal para:** Aplicaciones monolíticas en un solo servidor

---

### Opción 4: API Keys

**Ventajas:**
- ✅ Muy simple de implementar
- ✅ Perfecto para integraciones M2M (machine-to-machine)

**Desventajas:**
- ⚠️ No identifica usuarios individuales
- ⚠️ Si se filtra la key, todos los usuarios están comprometidos
- ⚠️ No hay experiencia de login tradicional

**Ideal para:** APIs internas o integraciones automatizadas

---

## 🏗️ Arquitectura Recomendada: JWT + Base de Datos

### Stack Tecnológico

```
Frontend (React)
    ↓
JWT Token (localStorage/sessionStorage)
    ↓
Backend (FastAPI + JWT)
    ↓
Base de Datos (SQLite/PostgreSQL)
    ↓
Jira API (credenciales del usuario autenticado)
```

### Por qué JWT + Base de Datos

1. **JWT para autenticación** - Stateless, perfecto para Render Free
2. **Base de datos para usuarios** - Almacenar credenciales y configuración
3. **Sin Redis** - Evita costos adicionales
4. **Cada usuario usa sus propias credenciales de Jira** - Más seguro y auditable

---

## 🛠️ Implementación Detallada

### Fase 1: Base de Datos y Modelos de Usuario

#### 1.1 Agregar Dependencias al Backend

```txt
# requirements.txt (agregar)
sqlalchemy==2.0.23
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
alembic==1.13.1  # Para migraciones
```

#### 1.2 Modelo de Usuario

```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Credenciales de Jira del usuario
    jira_email = Column(String, nullable=True)
    jira_api_token = Column(String, nullable=True)  # Encriptado
    jira_base_url = Column(String, nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
```

#### 1.3 Base de Datos

**Opción A: SQLite (Simple, para empezar)**
```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./jira_agent.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Opción B: PostgreSQL (Producción)**
```python
# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/jira_agent"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Base de datos en Render:**
- Render ofrece PostgreSQL gratuito (90 días, luego se borra)
- Alternativa: Supabase PostgreSQL (gratis permanente, 500MB)
- Alternativa: Neon PostgreSQL (gratis, 512MB)

---

### Fase 2: Sistema de Autenticación Backend

#### 2.1 Utilidades de Seguridad

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# Configuración
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que la contraseña coincida con el hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera hash de contraseña."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verifica y decodifica JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

#### 2.2 Dependencias de Autenticación

```python
# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.database import SessionLocal
from app.models.user import User

security = HTTPBearer()

def get_db():
    """Dependency para obtener sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtiene el usuario actual desde el token JWT.
    Se usa como dependency en endpoints protegidos.
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    return user
```

#### 2.3 Endpoints de Autenticación

```python
# app/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr

from app.api.dependencies import get_db, get_current_user
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.models.user import User

router = APIRouter()

# ============================================================================
# Pydantic Models
# ============================================================================

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    jira_email: EmailStr
    jira_api_token: str
    jira_base_url: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    jira_email: str
    jira_base_url: str
    created_at: datetime

    class Config:
        from_attributes = True

# ============================================================================
# Endpoints
# ============================================================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario.
    """
    # Verificar que el email no exista
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado"
        )

    # Verificar que el username no exista
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username ya existe"
        )

    # TODO: Encriptar jira_api_token antes de guardar

    # Crear usuario
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        jira_email=user_data.jira_email,
        jira_api_token=user_data.jira_api_token,  # TODO: Encriptar
        jira_base_url=user_data.jira_base_url,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login con username y password.
    Retorna JWT token.
    """
    # Buscar usuario por username
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    # Actualizar last_login
    user.last_login = datetime.utcnow()
    db.commit()

    # Crear token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Obtiene información del usuario actual.
    """
    return current_user

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout (en JWT es cliente-side, solo elimina token del frontend).
    """
    return {"message": "Logout exitoso"}
```

#### 2.4 Proteger Endpoints Existentes

```python
# app/main.py (modificar)
from app.api.dependencies import get_current_user
from app.models.user import User

# Agregar dependency a endpoints protegidos
@app.post("/api/v1/tasks/create", response_model=CreateTaskResponse)
async def create_task_from_text(
    request: CreateTaskRequest,
    current_user: User = Depends(get_current_user)  # ← AGREGAR
):
    """
    Ahora requiere autenticación.
    Usa las credenciales de Jira del usuario autenticado.
    """
    # Crear JiraClient con credenciales del usuario
    jira_client = JiraClient(
        base_url=current_user.jira_base_url,
        email=current_user.jira_email,
        api_token=current_user.jira_api_token  # TODO: Desencriptar
    )

    # ... resto del código
```

---

### Fase 3: Frontend con Autenticación

#### 3.1 Context API para Autenticación

```typescript
// jira-tracker/src/contexts/AuthContext.tsx
import React, { createContext, useState, useContext, useEffect } from 'react';
import { ApiService } from '../services/api.service';

interface User {
  id: number;
  email: string;
  username: string;
  jira_email: string;
  jira_base_url: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Al cargar, verificar si hay token guardado
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      // Obtener información del usuario
      ApiService.getCurrentUser(storedToken)
        .then(user => setUser(user))
        .catch(() => {
          // Token inválido
          localStorage.removeItem('token');
          setToken(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (username: string, password: string) => {
    const response = await ApiService.login(username, password);
    setToken(response.access_token);
    localStorage.setItem('token', response.access_token);

    // Obtener info del usuario
    const userInfo = await ApiService.getCurrentUser(response.access_token);
    setUser(userInfo);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        logout,
        isAuthenticated: !!token,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

#### 3.2 Componente de Login

```typescript
// jira-tracker/src/pages/LoginPage.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './LoginPage.css';

export const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(username, password);
      navigate('/');
    } catch (err: any) {
      setError(err.message || 'Error al iniciar sesión');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <h1>Jira AI Agent</h1>
        <h2>Iniciar Sesión</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Usuario</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Cargando...' : 'Iniciar Sesión'}
          </button>
        </form>

        <p className="register-link">
          ¿No tienes cuenta? <a href="/register">Regístrate aquí</a>
        </p>
      </div>
    </div>
  );
};
```

#### 3.3 Rutas Protegidas

```typescript
// jira-tracker/src/components/ProtectedRoute.tsx
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { LoadingSpinner } from './LoadingSpinner';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};
```

#### 3.4 Actualizar App.tsx

```typescript
// jira-tracker/src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { HomePage } from './pages/HomePage';
import { ProjectWorkspace } from './pages/ProjectWorkspace';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route
            path="/"
            element={
              <ProtectedRoute>
                <HomePage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/project/:projectKey"
            element={
              <ProtectedRoute>
                <ProjectWorkspace />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
```

#### 3.5 Actualizar API Service con Token

```typescript
// jira-tracker/src/services/api.service.ts
const getAuthHeaders = (): HeadersInit => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
  };
};

export class ApiService {
  static async getProjects(): Promise<JiraProject[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/projects`, {
      headers: getAuthHeaders(),
    });
    // ... rest
  }

  // Agregar métodos de auth
  static async login(username: string, password: string) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<{ access_token: string; token_type: string }>(response);
  }

  static async getCurrentUser(token: string): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse<User>(response);
  }
}
```

---

## ⏱️ Estimación de Esfuerzo

### Fase 1: Backend Base de Datos (6-8 horas)
- ✅ Configurar SQLAlchemy/PostgreSQL: 1-2 horas
- ✅ Crear modelos de usuario: 1 hora
- ✅ Migraciones con Alembic: 1-2 horas
- ✅ Testing de base de datos: 1 hora
- ✅ Desplegar base de datos en Render/Supabase: 2 horas

### Fase 2: Backend Autenticación (8-10 horas)
- ✅ Implementar JWT utilities: 2 horas
- ✅ Endpoints de auth (login, register, me): 3-4 horas
- ✅ Proteger endpoints existentes: 2 horas
- ✅ Modificar JiraClient para usar credenciales por usuario: 2 horas
- ✅ Testing de endpoints: 1-2 horas

### Fase 3: Frontend Autenticación (6-8 horas)
- ✅ Context API de autenticación: 2 horas
- ✅ Página de login: 1-2 horas
- ✅ Página de registro: 1-2 horas
- ✅ Rutas protegidas: 1 hora
- ✅ Actualizar API service con tokens: 1 hora
- ✅ Testing y debugging: 1-2 horas

### Fase 4: Seguridad y Refinamiento (4-6 horas)
- ✅ Encriptar tokens de Jira en base de datos: 2 horas
- ✅ Refresh tokens (opcional): 2 horas
- ✅ Manejo de errores y edge cases: 1-2 horas
- ✅ Rate limiting en endpoints de auth: 1 hora

### **TOTAL: 24-32 horas** (3-4 días de trabajo)

---

## 🔒 Consideraciones de Seguridad

### 1. Almacenamiento de Contraseñas
```python
# ✅ CORRECTO: Usar bcrypt
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash(password)

# ❌ INCORRECTO: Nunca guardar en texto plano
password = "mypassword123"  # NO HACER ESTO
```

### 2. JWT Secret Key
```python
# ✅ CORRECTO: Variable de entorno fuerte
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Generado con secrets.token_urlsafe(32)

# ❌ INCORRECTO: Secret key hardcodeado
SECRET_KEY = "mysecret"  # NO HACER ESTO
```

**Generar secret key seguro:**
```python
import secrets
print(secrets.token_urlsafe(32))
# Ejemplo: 'XAhHF7_QfGlm8TnTiUk9j3YZ0w5rK8bN1qW2eR3tY4u'
```

### 3. Encriptar Tokens de Jira
```python
# app/core/encryption.py
from cryptography.fernet import Fernet
import os
import base64

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")  # 32 bytes base64
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_token(token: str) -> str:
    """Encripta un token."""
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    """Desencripta un token."""
    return fernet.decrypt(encrypted_token.encode()).decode()
```

**Generar encryption key:**
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### 4. HTTPS Obligatorio
- ✅ Render proporciona HTTPS automáticamente
- ✅ Nunca enviar tokens por HTTP
- ✅ Usar `secure` cookies en producción

### 5. CORS Restrictivo
```python
# ✅ Solo permitir frontend específico
allow_origins=["https://jira-tracker-l5m9.onrender.com"]

# ❌ NUNCA hacer esto en producción
allow_origins=["*"]
```

### 6. Rate Limiting en Login
```python
# Prevenir ataques de fuerza bruta
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")  # Máximo 5 intentos por minuto
async def login(...):
    pass
```

### 7. Token Expiration
```python
# ✅ Tokens deben expirar
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

# Para mayor seguridad:
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora
# + implementar refresh tokens
```

### 8. Validación de Input
```python
# ✅ Usar Pydantic para validación
class UserRegister(BaseModel):
    email: EmailStr  # Valida formato de email
    username: str = Field(min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    password: str = Field(min_length=8)
```

### 9. SQL Injection Protection
```python
# ✅ CORRECTO: Usar SQLAlchemy ORM
user = db.query(User).filter(User.email == email).first()

# ❌ INCORRECTO: SQL raw queries
db.execute(f"SELECT * FROM users WHERE email = '{email}'")  # VULNERABLE
```

### 10. Variables de Entorno en Render
```bash
# Backend service en Render
JWT_SECRET_KEY=XAhHF7_QfGlm8TnTiUk9j3YZ0w5rK8bN1qW2eR3tY4u
ENCRYPTION_KEY=kZ8v3X9mN4pQ2wR7tY1uI5oP0aS6dF3gH8jK4lM9nB2
DATABASE_URL=postgresql://user:pass@host/db
```

---

## 📦 Opciones de Base de Datos Gratuitas

### Opción 1: Render PostgreSQL (Gratis 90 días)
- ✅ 1GB storage
- ✅ Fácil integración con Render backend
- ⚠️ Se borra después de 90 días inactiva
- ⚠️ Requiere backup manual

### Opción 2: Supabase PostgreSQL ⭐ RECOMENDADA
- ✅ 500MB storage permanente
- ✅ 2GB bandwidth
- ✅ Backup automático
- ✅ Dashboard para administración
- ✅ 100% compatible con PostgreSQL

**Setup:**
1. Crear cuenta en [supabase.com](https://supabase.com)
2. Crear nuevo proyecto
3. Copiar `DATABASE_URL` de Project Settings
4. Agregar a variables de entorno en Render

### Opción 3: Neon PostgreSQL
- ✅ 512MB storage permanente
- ✅ Serverless (escala a 0)
- ✅ Rápido
- ✅ Gratuito para siempre

### Opción 4: SQLite (Desarrollo local)
- ✅ Cero configuración
- ✅ Perfecto para desarrollo
- ⚠️ NO usar en producción con Render (disco efímero)

---

## 🎯 Recomendación Final

### Stack Recomendado:
```
Frontend:
  React + TypeScript
  Context API para auth
  localStorage para token

Backend:
  FastAPI + JWT
  SQLAlchemy ORM
  Bcrypt para passwords
  Fernet para encriptar tokens de Jira

Base de Datos:
  Supabase PostgreSQL (gratis permanente)

Hosting:
  Render (backend + frontend gratis)
```

### Orden de Implementación:
1. ✅ **Semana 1:** Backend - Base de datos + Modelos
2. ✅ **Semana 2:** Backend - Sistema de autenticación JWT
3. ✅ **Semana 3:** Frontend - Login + Registro + Context
4. ✅ **Semana 4:** Seguridad + Testing + Deploy

### Características Opcionales (Post-MVP):
- 🔄 Refresh tokens para seguridad mejorada
- 👥 Roles y permisos (admin, user)
- 🔔 Recuperación de contraseña por email
- 📊 Auditoría de acciones (logs de quién creó qué)
- 🌐 OAuth con Google/Microsoft
- 📱 2FA (Two-Factor Authentication)

---

## 📚 Recursos Adicionales

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - Debugging de tokens
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [React Auth Best Practices](https://blog.logrocket.com/complete-guide-authentication-with-react-router-v6/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## ❓ Preguntas Frecuentes

### ¿Es seguro guardar el token en localStorage?
- ✅ Sí, para la mayoría de aplicaciones
- ⚠️ Vulnerable a XSS (Cross-Site Scripting)
- Alternativa: httpOnly cookies (más seguro pero más complejo)

### ¿Necesito HTTPS?
- ✅ SÍ, absolutamente
- Render lo proporciona gratis automáticamente

### ¿Cuánto cuesta implementar esto?
- Backend + Frontend en Render: **$0/mes**
- Base de datos en Supabase: **$0/mes**
- **TOTAL: $0/mes** para empezar

### ¿Puedo usar Google Login en vez de crear cuentas?
- Sí, pero es más complejo
- Requiere OAuth 2.0 implementation
- Agrega ~8-10 horas al proyecto

### ¿Los usuarios pueden compartir sus credenciales de Jira?
- Cada usuario usa sus propias credenciales
- Más seguro y auditable
- Las credenciales se encriptan en la base de datos

---

¿Quieres que implemente alguna de estas fases? Puedo empezar por donde prefieras.
