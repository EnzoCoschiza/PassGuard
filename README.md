# PassGuard CI

Proyecto academico para demostrar un flujo de calidad e integracion continua alrededor de una aplicacion web simple de analisis de contrasenas.

## Estructura

- `app/`: backend FastAPI
- `tests/`: tests del backend
- `frontend/`: frontend React + Vite
- `docs/`: especificaciones funcionales

## Backend con uv y entorno virtual

El entorno virtual local esperado es `.venv`.

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv sync --dev
uv run uvicorn app.main:app --reload
```

Comandos utiles:

```powershell
uv run pytest
uv run ruff check .
```

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Comandos utiles:

```powershell
npm run test
npm run lint
npm run build
```

## Pipeline local minimo

El flujo local recomendado antes de integrar CI remota es:

1. `uv run ruff check .`
2. `uv run pytest`
3. `cd frontend && npm run lint`
4. `cd frontend && npm run test`
5. `cd frontend && npm run build`

## GitHub Actions

El workflow de CI queda en `.github/workflows/ci.yml`.

Que hace en cada `push` a `main` o `master` y en cada `pull_request`:

1. Backend:
   - instala Python 3.11
   - instala `uv`
   - ejecuta `uv sync --dev`
   - corre `uv run ruff check .`
   - corre `uv run pytest`
2. Frontend:
   - instala Node 20
   - ejecuta `npm ci`
   - corre `npm run lint`
   - corre `npm run test`
   - corre `npm run build`

## Docker

Para levantar el proyecto completo con contenedores:

```powershell
docker compose up --build
```

Servicios:

- frontend: `http://localhost:8080`
- backend API: `http://localhost:8000`

El frontend se sirve con `nginx` y proxyea `/health` y `/password` al contenedor `backend`.
