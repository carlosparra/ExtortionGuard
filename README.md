# ExtortionGuard

## Descripción del Proyecto

ExtortionGuard es una iniciativa tecnológica de ciberseguridad enfocada en proteger a los usuarios de intentos de extorsión telefónica y digital. Su propósito principal es detectar, registrar y gestionar reportes de llamadas, mensajes SMS o WhatsApp sospechosos, construyendo un sistema de confianza que permita identificar números problemáticos y reducir riesgos de fraude o acoso.

## Características Principales

### Registro de Reportes

- Los usuarios pueden reportar números sospechosos mediante un endpoint (`POST /api/reports`)
- Cada reporte contiene metadatos como canal (call, sms, wa), teléfono y detalles del incidente
- Los reportes se almacenan con UUID como identificador único, asegurando trazabilidad y consistencia

### Consulta de Riesgo

- A través del endpoint (`GET /api/risk/lookup`), se consulta el "score" o etiqueta de riesgo de un número
- Este score se calcula considerando el historial de reportes y un algoritmo de validación basado en cantidad de confirmaciones y caducidad de los números

### Gestión de Apelaciones

- Los usuarios pueden apelar un reporte o solicitar re-evaluación si creen que un número fue marcado erróneamente (`POST /api/appeals`)
- Esto garantiza equilibrio entre seguridad y justicia, evitando falsos positivos

### Caducidad y Confirmación

- Los números sospechosos caducan con el tiempo, salvo que acumulen suficiente evidencia para ser considerados problemáticos
- Se define un algoritmo de consenso: cuando un número recibe n reportes consistentes, se confirma su clasificación como de alto riesgo

### Monitoreo de Salud del Sistema

- Endpoint de verificación (`GET /api/health/ready`) para asegurar que el servicio esté en funcionamiento y disponible

## Valor Agregado

### Prevención Proactiva
ExtortionGuard busca adelantarse a intentos de extorsión mediante la creación de una base de datos colaborativa y dinámica.

### Protección Comunitaria
Cada reporte contribuye a proteger no solo al usuario que lo envía, sino a toda la comunidad.

### Transparencia y Control
Al permitir apelaciones y caducidad, se evita estigmatizar de forma indefinida números que pudieran haber sido reportados por error.

## API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/reports` | Registrar un nuevo reporte de número sospechoso |
| GET | `/api/risk/lookup` | Consultar el score de riesgo de un número |
| POST | `/api/appeals` | Crear una apelación para un reporte |
| GET | `/api/health/ready` | Verificar el estado de salud del servicio |

## Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- PostgreSQL
- Docker (opcional)

### Instalación con Poetry

```bash
# Clonar el repositorio
git clone <repository-url>
cd ExtortionGuard

# Instalar dependencias
poetry install

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar migraciones
alembic upgrade head

# Iniciar el servidor
poetry run uvicorn app.api.main:app --reload
```

### Instalación con Docker

```bash
# Construir y ejecutar con Docker Compose
docker-compose up --build
```

## Uso

Una vez que el servicio esté ejecutándose, puedes acceder a:

- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/health/ready`

## Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o sugerencias sobre ExtortionGuard, por favor abre un issue en este repositorio.