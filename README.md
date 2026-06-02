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
