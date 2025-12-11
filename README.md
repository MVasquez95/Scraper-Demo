# AWS Job Scraper (Indeed → PostgreSQL)

Este proyecto implementa un **scraper serverless** que obtiene puestos laborales desde Indeed y los almacena en una base de datos **PostgreSQL (Amazon RDS)** usando **AWS Lambda**.

El objetivo es tener un scraper profesional, modular, fácil de desplegar y listo para integrarse con dashboards o APIs en el futuro.

---

## Arquitectura del Proyecto

EventBridge (cron)
↓
Lambda Scraper (Python)
↓
PostgreSQL (Amazon RDS)
↓
API Gateway
↓
Lambda API Handler
↓
Frontend Dashboard (React)

## Estructura del Proyecto
- `scraper_project/`
    - `lambda_scraper/`
        - `handler.py` → Entry point de AWS Lambda
        - `scraper.py` → Scraping logic (Indeed)
        - `db.py` → Conexión e inserción en PostgreSQL
        - `utils.py` → Utilidades futuras
        - `requirements.txt` → Dependencias para instalar en CloudShell

No incluye credenciales ni variables de entorno.

---

## Dependencias principale

El scraper usa:

- `requests` — para obtener HTML
- `selectolax` — parser rápido basado en C
- `psycopg2-binary` — para conectarse a PostgreSQL

Estas librerías se instalan directamente en CloudShell porque Lambda requiere binarios para Linux.

---

## Cómo desplegar en AWS Lambda

### 1. Clonar el repositorio en AWS CloudShell

```bash
git clone <TU_REPO_URL>
cd scraper_project/lambda_scraper
```

### 2. Instalar dependencias dentro de la carpeta (Linux-compatible)

```bash
pip install -r requirements.txt --target .
```

### 3. Crear el ZIP para Lambda

```bash
zip -r lambda.zip .
```

### 4. Subir a AWS Lambda
En la consola de AWS:
- Ir a tu Lambda
- Cargar archivo ZIP
- Guardar y testear

## Variables de entorno requeridas (en AWS Lambda)

| Variable     | Descripción                |
|--------------|----------------------------|
| DB_HOST      | Host de PostgreSQL RDS     |
| DB_PORT      | Puerto (generalmente 5432) |
| DB_NAME      | Nombre de la base          |
| DB_USER      | Usuario                    |
| DB_PASSWORD  | Contraseña                 |

## Tabla `jobs`
```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    summary TEXT,
    url TEXT,
    scraped_at TIMESTAMP
);
```

## Licencia
MIT License.