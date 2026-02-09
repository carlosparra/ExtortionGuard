# 🛡️ ExtortionGuard

**Protección colaborativa contra la extorsión telefónica y digital**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)

## 📖 Descripción

ExtortionGuard es una plataforma de ciberseguridad que protege a los usuarios contra intentos de extorsión telefónica y digital. A través de un sistema de reportes colaborativo, construye una base de datos de confianza para identificar números y URLs problemáticas, reduciendo el riesgo de fraudes y acoso.

## ✨ Características Principales

### 📞 Registro de Reportes
- Reporte de números sospechosos por llamadas, SMS o WhatsApp
- Identificadores únicos (UUID) para trazabilidad completa
- Metadatos detallados del incidente

### 📊 Evaluación de Riesgo
- Consulta de scores de riesgo basados en historial de reportes
- Algoritmo de validación con confirmaciones y caducidad
- Evaluación inteligente de patrones de comportamiento

### 🔗 Verificación de URLs
- Detección de enlaces maliciosos y phishing
- Múltiples versiones de verificación (v1, v2)
- Análisis de reputación de dominios

### ⚖️ Sistema de Apelaciones
- Proceso justo para revisar reportes erróneos
- Prevención de falsos positivos
- Transparencia en las decisiones

### 🏥 Monitoreo de Salud
- Health checks integrados para alta disponibilidad
- Métricas de rendimiento del sistema
- Logging y trazabilidad de requests

## 🚀 Instalación y Configuración

### 📋 Requisitos Previos
- **Python 3.13+**
- **PostgreSQL 16+**
- **Redis 7+**
- **Poetry** (recomendado) o pip
- **Docker** (opcional)

### 🐍 Instalación con Poetry

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/ExtortionGuard.git
cd ExtortionGuard

# Instalar dependencias
poetry install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar migraciones de base de datos
poetry run alembic upgrade head

# Iniciar servidor de desarrollo
poetry run uvicorn app.main:app --reload
```

### 🐳 Instalación con Docker

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Solo la base de datos para desarrollo local
docker-compose up postgres redis
```

### ⚙️ Variables de Entorno

Crea un archivo `.env` con las siguientes variables:

```env
# Base de datos
DATABASE_URL=postgresql://extuser:extpass@localhost:5433/extortion

# Redis
REDIS_URL=redis://localhost:6379

# Configuración de la aplicación
APP_NAME=ExtortionGuard
API_PREFIX=/api
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Configuración de seguridad
SECRET_KEY=tu-secret-key-super-seguro
```

## 🔧 Comandos de Desarrollo

El proyecto incluye un `Makefile` con comandos útiles:

```bash
# Servidor de desarrollo
make dev

# Ejecutar tests
make test

# Linting y formato de código
make lint
make fmt

# Migraciones de base de datos
make migrate-up
make migrate-rev
```

## 📡 API Endpoints

### 🔍 Documentación Interactiva
Una vez ejecutando el servidor, accede a:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 📋 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/reports` | Registrar reporte de número sospechoso |
| `GET` | `/api/risk/lookup` | Consultar score de riesgo de un número |
| `POST` | `/api/appeals` | Crear apelación para un reporte |
| `POST` | `/api/urlcheck/check` | Verificar URL maliciosa (v1) |
| `POST` | `/api/urlcheck/check/v2` | Verificar URL maliciosa (v2) |
| `GET` | `/api/health/ready` | Health check del servicio |
| `GET` | `/health` | Health check simple |

### 📝 Ejemplos de Uso

**Reportar número sospechoso:**
```bash
curl -X POST "http://localhost:8000/api/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+52123456789",
    "country": "MX",
    "channel": "call",
    "description": "Intento de extorsión"
  }'
```

**Consultar riesgo de número:**
```bash
curl "http://localhost:8000/api/risk/lookup?phone=+52123456789&country=MX"
```

**Verificar URL:**
```bash
curl -X POST "http://localhost:8000/api/urlcheck/check" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://ejemplo-sospechoso.com"}'
```

## 🏗️ Arquitectura del Proyecto

```
app/
├── api/                 # Capa de API (FastAPI)
│   ├── routes/         # Definición de endpoints
│   └── deps.py         # Dependencias compartidas
├── core/               # Configuración central
│   ├── config.py       # Settings de la aplicación
│   ├── logging.py      # Configuración de logs
│   └── security.py     # Utilidades de seguridad
├── db/                 # Capa de base de datos
│   ├── models.py       # Modelos SQLAlchemy
│   └── session.py      # Sesiones de DB
├── middleware/         # Middlewares personalizados
├── schemas/            # Schemas Pydantic (request/response)
├── services/           # Lógica de negocio
├── utils/              # Utilidades compartidas
└── tests/              # Tests automatizados
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
poetry run pytest

# Con cobertura
poetry run pytest --cov=app --cov-report=term-missing

# Test específico
poetry run pytest app/tests/test_reports.py -v
```

## 📊 Tecnologías Utilizadas

- **Backend**: FastAPI, Python 3.13
- **Base de Datos**: PostgreSQL con SQLAlchemy ORM
- **Cache**: Redis
- **Validación**: Pydantic
- **Migraciones**: Alembic
- **Testing**: Pytest
- **Linting**: Ruff
- **Containerización**: Docker & Docker Compose

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor sigue estos pasos:

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. **Commit** tus cambios (`git commit -m 'Agrega nueva característica'`)
4. **Push** a la rama (`git push origin feature/nueva-caracteristica`)
5. **Abre** un Pull Request

### 📝 Convenciones de Código
- Sigue PEP 8 para Python
- Usa `ruff` para linting y formato
- Incluye tests para nuevas funcionalidades
- Documenta APIs con docstrings

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

¿Tienes preguntas o necesitas ayuda?

- 📫 **Issues**: [GitHub Issues](https://github.com/tu-usuario/ExtortionGuard/issues)
- 📧 **Email**: team@extortionguard.com
- 📚 **Wiki**: Consulta nuestra [documentación](https://github.com/tu-usuario/ExtortionGuard/wiki)

---

**🛡️ Protegiendo comunidades, un reporte a la vez.**