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

En produccion, el frontend toma la URL del backend desde `frontend/.env.production`:

```text
VITE_API_BASE_URL=https://passguard-8j7p.onrender.com
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

El deploy de GitHub Pages queda en `.github/workflows/pages.yml`.

Antes de usarlo:

1. En GitHub, ir a `Settings` -> `Pages`
2. En `Source`, elegir `GitHub Actions`
3. Hacer push a `main`

La URL final del sitio quedara con el formato:

```text
https://enzog.github.io/PassGuard/
```

## Docker

Para levantar el proyecto completo con contenedores:

```powershell
docker compose up --build
```

Servicios:

- frontend: `http://localhost:8080`
- backend API: `http://localhost:8000`

El frontend se sirve con `nginx` y proxyea `/health` y `/password` al contenedor `backend`.

## CORS del backend

El backend permite por defecto estos origenes:

- `http://localhost:5173`
- `http://127.0.0.1:5173`
- `https://enzog.github.io`

Si queres cambiarlo en Render, defini la variable de entorno `CORS_ORIGINS` con origenes separados por comas.

## SonarCloud

La configuracion del analisis queda en `sonar-project.properties`.

### Integracion con GitHub Actions

El workflow queda en `.github/workflows/sonarqube.yml`.

Antes de usarlo, hay que configurar en GitHub:

1. Hacer el repositorio publico o verificar que entre en el free tier de SonarCloud.
2. Crear la organizacion/proyecto en SonarCloud.
3. Reemplazar `sonar.organization=REPLACE_WITH_SONARCLOUD_ORG` en `sonar-project.properties`.
4. Si SonarCloud genera un `projectKey` distinto, actualizar tambien `sonar.projectKey`.
5. Crear el secret del repositorio `SONAR_TOKEN`.

Con SonarCloud no hace falta definir `SONAR_HOST_URL` en GitHub Actions.

### SonarQube local opcional

Si queres mantener un servidor local para demo:

```powershell
docker compose --profile quality up -d
```

Servicios extra del perfil `quality`:

- SonarQube: `http://localhost:9000`
- PostgreSQL interno para SonarQube
