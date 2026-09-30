# AI Moderator

AI Moderator is a backend service for accepting user-generated content and running it through a moderation workflow. It provides a FastAPI REST API, persists submitted content, and queues moderation work through Celery. The project also contains text, image, and video moderation modules, security and rate-limiting utilities, database migrations, and automated tests.

> **Project status:** The repository is a backend project in active development. Some components and deployment notes are aspirational or incomplete; see [Known limitations](#known-limitations) before using it in production.

## Contents

- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Run locally](#run-locally)
- [Configuration](#configuration)
- [API](#api)
- [Run tests](#run-tests)
- [Repository layout](#repository-layout)
- [Deployment](#deployment)
- [Known limitations](#known-limitations)
- [Security and privacy](#security-and-privacy)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Content intake API:** submit text or references to image/video content for moderation.
- **Asynchronous processing:** moderation requests are stored and queued through Celery, with Redis configured as the broker/result backend.
- **Moderation modules:** the codebase includes text toxicity, multilingual toxicity/language detection, image NSFW analysis, and video-frame extraction modules.
- **Persistence:** SQLAlchemy models with Alembic migration scaffolding.
- **API protection:** API-key dependency and request rate limiting are applied to the moderation endpoint.
- **Operational endpoints:** root and health-check routes, structured application logging, and Prometheus instrumentation.
- **Tests and load testing:** pytest test suite and a Locust load-test script.

The public moderation endpoint currently accepts content and returns its database ID and initial status. A successful submission means it was accepted for processing; it is not itself a moderation verdict.

## Architecture

```text
Client
  |
  | POST /api/v1/moderation/analyse (X-API-KEY)
  v
FastAPI backend -----> PostgreSQL (content records)
  |
  +------------------> Redis/Celery (background moderation tasks)
                              |
                              v
                       Moderation worker
```

The backend is under `backend/`. `backend/app/main.py` registers the moderation API and WebSocket router, and serves `/` and `/health`. The AI modules and worker code are under `backend/app/ai/` and `backend/app/workers/` respectively.

## Requirements

- Python 3.11 (the backend Dockerfile uses Python 3.11)
- PostgreSQL for normal API operation
- Redis for background task processing
- Git

PyTorch and Transformers may download model weights at runtime depending on the selected model implementation; allow for additional disk space, memory, and startup time when enabling those paths.

## Run locally

The following example is for PowerShell from the repository root. Start a PostgreSQL database and Redis instance first, then configure the environment variables described below.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in `backend/` with values for the required settings. For local development, `DATABASE_URL` should point to an existing PostgreSQL database and `REDIS_URL` to a reachable Redis instance. For example:

```dotenv
APP_NAME=AI Moderator
ENV=development
DATABASE_URL=postgresql://postgres:your-local-password@localhost:5432/ai_moderator
SECRET_KEY=replace-with-a-long-random-value
ALGORITHM=HS256
REDIS_URL=redis://localhost:6379/0
API_KEY_HEADER=X-API-KEY
```

Do not commit real credentials. The settings loader reads `.env` from the current working directory, so start the application from `backend/`:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Verify the process with:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

The health route reports API/process health only; it does not verify PostgreSQL, Redis, or worker availability.

To process queued jobs, open another PowerShell window, activate the same virtual environment, change to `backend/`, and start a Celery worker:

```powershell
celery -A app.core.celery.celery_app worker --loglevel=info
```

## Configuration

The settings class requires these environment variables; only `APP_NAME` and `DELETE_AFTER_DAYS` have defaults in the current implementation.

| Variable            | Purpose                                                                        |
| ------------------- | ------------------------------------------------------------------------------ |
| `APP_NAME`          | Service name; defaults to `AI Moderator`.                                      |
| `ENV`               | Environment label returned by the health endpoint.                             |
| `DATABASE_URL`      | SQLAlchemy database connection URL.                                            |
| `SECRET_KEY`        | Secret setting intended for security-related use. Use a strong, private value. |
| `ALGORITHM`         | Algorithm setting for token/security functionality.                            |
| `REDIS_URL`         | Redis connection URL used by Celery.                                           |
| `API_KEY_HEADER`    | Configured API-key header name.                                                |
| `DELETE_AFTER_DAYS` | Retention setting; defaults to `90`.                                           |

Although `API_KEY_HEADER` is configurable, the current API-key dependency uses the literal header `X-API-KEY`. The API-key values are also currently defined in code; see [Known limitations](#known-limitations).

## API

### Submit content

`POST /api/v1/moderation/analyse` accepts JSON with `external_id`, `content_type`, and `source_app`. `text` and `image_url` are optional fields.

```powershell
$body = @{
  external_id = "comment-123"
  text = "Example user-submitted text"
  content_type = "comment"
  source_app = "my-community"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/moderation/analyse `
  -Headers @{ "X-API-KEY" = "test-key-123" } `
  -ContentType "application/json" `
  -Body $body
```

The response contains the generated `id` and current `status` (initially `pending`). The endpoint is limited to 30 requests per minute per client. The included API keys are development placeholders, not credentials for a deployed service.

### Other endpoints

| Method    | Path             | Description                                       |
| --------- | ---------------- | ------------------------------------------------- |
| `GET`     | `/`              | Basic service status and configured service name. |
| `GET`     | `/health`        | Basic API health and environment label.           |
| `GET`     | `/metrics`       | Prometheus metrics exposed by the instrumentator. |
| WebSocket | `/ws/moderation` | WebSocket connection endpoint.                    |

FastAPI's generated OpenAPI UI is available at `/docs`; the schema is available at `/openapi.json`.

## Run tests

From the repository root, install backend requirements, configure the required environment variables, then run:

```powershell
cd backend
pytest tests/ -v
```

To request a coverage report:

```powershell
pytest tests/ -v --cov=app --cov-report=term-missing
```

The tests use SQLite and mock the Celery task path, so they do not require a running Redis service. The application settings are still loaded during test import and must be configured in the test environment.

## Repository layout

```text
backend/
  app/
    ai/              Moderation models, pipelines, and vision utilities
    api/v1/          FastAPI routes
    core/            Settings, database, security, logging, and Celery setup
    models/          SQLAlchemy models
    schemas/         Request and response schemas
    services/        Moderation and supporting services
    workers/         Background tasks
  tests/             API, security, health, and decision-engine tests
alembic/              Database migration configuration and revisions
docker-compose.yml    Container orchestration configuration
```

## Deployment

The repository includes a backend Dockerfile and reference deployment documents: [deployment architecture](DEPLOYMENT_ARCHITECTURE.md), [pre-deployment checklist](PRE_DEPLOYMENT_CHECKLIST.md), and [production readiness report](PRODUCTION_READINESS_REPORT.md). Treat those documents as planning/reference material and verify their commands and manifests against the current code before deploying.

The current `docker-compose.yml` defines both `backend` and `frontend` services, but this repository does not contain a `frontend/` directory. As written, the Compose configuration cannot build the frontend service. See [Known limitations](#known-limitations).

## Known limitations

- The checked-in Compose file references a `frontend/` build context that is not present.
- `alembic/env.py` imports `app.core.content`, which is not present in the repository; migration commands may fail until that import is corrected.
- The API-key validator contains hard-coded sample keys (`test-key-123` and `admin-key-456`). Replace this with secure key storage and rotation before any public deployment.
- The moderation endpoint's rate limit is fixed at 30 requests per minute, and CORS origins are currently hard-coded to localhost values.
- The `/health` response checks only that the API handler can respond; it is not a dependency/readiness check.
- Model modules and integration points are at varying levels of implementation. Verify that the desired moderation paths run end-to-end before relying on their results.
- The README and deployment reference files should not be interpreted as a production security or performance guarantee.

## Security and privacy

This service is designed to process potentially sensitive user content. Before operating it with real data:

- Replace development API keys and ensure secrets are supplied outside version control.
- Use HTTPS, restrict CORS to trusted origins, and add a real key-management and rotation process.
- Decide how long content and derived moderation data may be retained; validate that retention and deletion jobs are implemented and enabled.
- Avoid logging submitted content, credentials, or personally identifiable information.
- Review access controls, dependency versions, and data-processing obligations for your deployment.

## Contributing

Contributions are welcome. Keep changes focused, add or update tests for behavioral changes, and document configuration or API changes. Before opening a pull request, run the relevant tests with `pytest tests/ -v` from `backend/`.

## License

No license file is currently included in this repository. Until a license is added, assume that all rights are reserved and check with the repository owner before reusing or redistributing the code.
