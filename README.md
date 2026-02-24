# 🛡️ ExtortionGuard

**Collaborative protection against phone and digital extortion**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)

## 📖 Description

ExtortionGuard is a cybersecurity platform that protects users against phone and digital extortion attempts. Through a collaborative reporting system, it builds a trust database to identify problematic numbers and URLs, reducing the risk of fraud and harassment.

## ✨ Key Features

### 📞 Report Registration
- Report suspicious numbers from calls, SMS or WhatsApp
- Unique identifiers (UUID) for complete traceability
- Detailed incident metadata

### 📊 Risk Assessment
- Query risk scores based on report history
- Validation algorithm with confirmations and expiration
- Intelligent evaluation of behavior patterns

### 🔗 URL Verification
- Detection of malicious links and phishing
- Multiple verification versions (v1, v2)
- Domain reputation analysis

### ⚖️ Appeals System
- Fair process to review erroneous reports
- Prevention of false positives
- Transparency in decisions

### 🏥 Health Monitoring
- Integrated health checks for high availability
- System performance metrics
- Request logging and traceability

## 🚀 Installation and Configuration

### 📋 Prerequisites
- **Python 3.13+**
- **PostgreSQL 16+**
- **Redis 7+**
- **Poetry** (recommended) or pip
- **Docker** (optional)

### 🐍 Installation with Poetry

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

# Start development server
poetry run uvicorn app.main:app --reload
```

### 🐳 Installation with Docker

```bash
# Build and run all services
docker-compose up --build

# Only database for local development
docker-compose up postgres redis
```

### ⚙️ Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://extuser:extpass@localhost:5433/extortion

# Redis
REDIS_URL=redis://localhost:6379

# Application configuration
APP_NAME=ExtortionGuard
API_PREFIX=/api
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Security configuration
SECRET_KEY=your-super-secure-secret-key
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

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/reports` | Register suspicious number report |
| `GET` | `/api/risk/lookup` | Query risk score for a number |
| `POST` | `/api/appeals` | Create appeal for a report |
| `POST` | `/api/urlcheck/check` | Check malicious URL (v1) |
| `POST` | `/api/urlcheck/check/v2` | Check malicious URL (v2) |
| `GET` | `/api/health/ready` | Service health check |
| `GET` | `/health` | Simple health check |

### 📝 Usage Examples

**Report suspicious number:**
```bash
curl -X POST "http://localhost:8000/api/reports" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+52123456789",
    "country": "MX",
    "channel": "call",
    "description": "Extortion attempt"
  }'
```

**Query number risk:**
```bash
curl "http://localhost:8000/api/risk/lookup?phone=+52123456789&country=MX"
```

**Verify URL:**
```bash
curl -X POST "http://localhost:8000/api/urlcheck/check" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-example.com"}'
```

## 🏗️ Project Architecture

```
app/
├── api/                 # API Layer (FastAPI)
│   ├── routes/         # Endpoint definitions
│   └── deps.py         # Shared dependencies
├── core/               # Core configuration
│   ├── config.py       # Application settings
│   ├── logging.py      # Logging configuration
│   └── security.py     # Security utilities
├── db/                 # Database layer
│   ├── models.py       # SQLAlchemy models
│   └── session.py      # DB sessions
├── middleware/         # Custom middlewares
├── schemas/            # Pydantic schemas (request/response)
├── services/           # Business logic
├── utils/              # Shared utilities
└── tests/              # Automated tests
```

## 🧪 Testing

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=app --cov-report=term-missing

# Specific test
poetry run pytest app/tests/test_reports.py -v
```

## 📊 Technologies Used

- **Backend**: FastAPI, Python 3.13
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Validation**: Pydantic
- **Migrations**: Alembic
- **Testing**: Pytest
- **Linting**: Ruff
- **Containerization**: Docker & Docker Compose

## 🤝 Contributing

Contributions are welcome. Please follow these steps:

1. **Fork** the project
2. **Create** a feature branch (`git checkout -b feature/new-feature`)
3. **Commit** your changes (`git commit -m 'Add new feature'`)
4. **Push** to the branch (`git push origin feature/new-feature`)
5. **Open** a Pull Request

### 📝 Code Conventions
- Follow PEP 8 for Python
- Use `ruff` for linting and formatting
- Include tests for new functionalities
- Document APIs with docstrings

## 📄 License

This project is under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🆘 Support

Do you have questions or need help?

- 📫 **Issues**: [GitHub Issues](https://github.com/your-user/ExtortionGuard/issues)
- 📧 **Email**: team@extortionguard.com
- 📚 **Wiki**: Check our [documentation](https://github.com/your-user/ExtortionGuard/wiki)

---

**🛡️ Protecting communities, one report at a time.**