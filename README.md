# Nuclera Protein Screening

A small full-stack application for creating and reviewing protein screening
experiments. An experiment contains a name and exactly 20 amino-acid sequences,
entered manually or uploaded as a FASTA file.

The repository contains:

- A React, TypeScript, Vite, and Tailwind CSS frontend.
- A FastAPI backend with validation and an in-memory experiment store.
- Pytest backend tests and Playwright browser tests.
- Docker images and an Nginx reverse proxy for a single-host deployment.
- Labelled test inputs in [`sample/`](sample/README.md).

## Project scope

The application currently supports:

- Creating an experiment from 20 manually entered sequences separated by new
  lines, commas, or a mixture of both.
- Creating an experiment from a UTF-8 FASTA file up to 32 KiB (32,768 bytes).
- Validating sequence count, length, characters, common regions, and variable
  regions.
- Listing experiments with limit/offset pagination.
- API health checks and interactive OpenAPI documentation.

The sequence rules are:

- Exactly 20 sequences per experiment.
- Experiment names contain 1-100 characters after surrounding whitespace is removed.
- Each sequence contains 12-100 letters and is stored in uppercase.
- All sequences share at least five residues at the beginning and end.
- The region between the longest common prefix and suffix contains 2-9
  residues.
- FASTA headers contain 1-100 characters.

## Assumptions and current limitations

- The accepted amino-acid alphabet is uppercase `A`-`Z`, matching the
  [IUPAC code table referenced by the exercise](https://www.dnastar.com/SeqMan_Pro_Help/index.html#!Documents/iupaccodesforaminoacids.htm).
  This includes ambiguous, unknown, and uncommon codes such as `B`, `J`, `O`,
  `U`, `X`, and `Z`, rather than only the 20 canonical residues.
- Manual and FASTA input may use uppercase or lowercase letters. The backend
  normalizes all sequences to uppercase before validation and storage.
- FASTA headers identify records structurally but are not saved with an
  experiment.
- FASTA records must use `>` headers. Legacy lines beginning with `;` are not
  treated as headers or comments and are rejected.
- Experiments are stored only in the backend process memory. Restarting the
  backend or containers deletes all created experiments.
- The deployment assumes one backend instance. There is no shared database,
  authentication, authorization, audit trail, or user separation.
- The provided Docker configuration is suitable for evaluation or a controlled
  single-host environment. Public production use still requires HTTPS, access
  control, persistent storage, backups, observability, and an appropriate
  secrets/configuration strategy.

## Prerequisites

For local development:

- Python 3.13 or later.
- [uv](https://docs.astral.sh/uv/).
- Node.js 22 or later and npm.

For the containerized deployment:

- Docker with Docker Compose.

## Development setup

Install dependencies:

```powershell
npm run setup
```

This uses `uv` to create or select the backend environment automatically; no
manual virtual-environment activation is required.

Start the backend from the repository root:

```powershell
npm run dev:backend
```

Start the frontend in a second terminal:

```powershell
npm run dev:frontend
```

Open:

- Application: <http://localhost:5173>
- API documentation: <http://localhost:3000/docs>
- Health check: <http://localhost:3000/api/v1/health>

Vite proxies `/api` requests to `http://127.0.0.1:3000` by default. To use a
different backend, copy `frontend/.env.example` to `frontend/.env.local` and
change `VITE_API_PROXY_TARGET`. `VITE_API_BASE_URL` and `VITE_API_DOCS_URL` can
be used when the API is hosted on another origin.

## Tests and checks

Run the backend test suite from the repository root:

```powershell
npm run test:backend
```

Run frontend linting and a production build:

```powershell
npm run lint:frontend
npm run build:frontend
```

Install Playwright browsers once, then run the browser tests:

```powershell
npm run install:playwright
npm run test:frontend
```

The Playwright configuration starts the frontend automatically, but the backend
must already be running on port 3000.

## Containerized production deployment

Build and start both services from the repository root:

```powershell
npm run build:compose
```

The application is served at <http://localhost>, with Nginx forwarding `/api`,
`/docs`, and `/openapi.json` to the backend. Port 80 must be available on the
host.

Useful Docker Compose commands:

```powershell
npm run compose:ps
npm run compose:logs
npm run compose:down
```

For a public deployment, place the stack behind HTTPS or extend the Nginx
configuration with TLS, and address the persistence and security limitations
listed above before accepting real data.

## With more time

The next improvements would focus on production resilience and traceability:

### Backend

- Add persistent database storage so experiments survive restarts and can be
  shared safely across multiple backend instances.
- Define a backup and recovery strategy for the persistent store, including
  encrypted scheduled backups once database storage is implemented.
- Apply rate limits to write and upload endpoints to reduce accidental or
  abusive API usage.
- Record an audit trail for experiment creation, validation failures, and other
  important operations.
- Add idempotency keys to experiment creation before automatically retrying
  failed write requests, preventing duplicate experiments.

### Frontend

- Centralize manual-input parsing and normalization. Delimiters and surrounding
  whitespace can be normalized, while unexpected quotes or punctuation should
  produce a clear validation error.
- Use TanStack Query if the experiment-list workflow grows, providing managed
  caching, request deduplication, invalidation, and safe retries for reads.
- Preserve an unsent form draft locally after network failures and let the user
  retry explicitly.
- Improve loading, offline, and recovery states and expand accessibility and
  end-to-end coverage around failure scenarios.
- Make the experiment sequence list collapsible, allowing users to expand individual experiments to view their 20 amino acid sequences while keeping the experiment list compact and easier to navigate as it grows.
## Root commands

All project workflows can be run from the repository root:

| Command | Purpose |
| --- | --- |
| `npm run setup` | Install locked backend and frontend dependencies |
| `npm run setup:backend` | Install backend dependencies with `uv` |
| `npm run setup:frontend` | Install frontend dependencies with `npm ci` |
| `npm run dev:backend` | Start FastAPI with automatic reload on port 3000 |
| `npm run dev:frontend` | Start the Vite development server |
| `npm run build:frontend` | Type-check and build the production frontend |
| `npm run preview:frontend` | Preview the built frontend locally |
| `npm run lint:frontend` | Run frontend lint checks |
| `npm run test:backend` | Run the backend Pytest suite |
| `npm run install:playwright` | Install Playwright browser binaries |
| `npm run test:frontend` | Run the Playwright browser tests |
| `npm run build:compose` | Build and start the containerized application |
| `npm run compose:ps` | Show container status |
| `npm run compose:logs` | Follow container logs |
| `npm run compose:down` | Stop and remove the application containers |

## AI assistance

OpenAI Codex was used to support implementation, testing, code review, and documentation. All AI-assisted changes were reviewed and verified by the author.

## API overview

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Check backend health |
| `POST` | `/api/v1/experiments` | Create an experiment from JSON |
| `POST` | `/api/v1/experiments/upload` | Create an experiment from multipart FASTA input |
| `GET` | `/api/v1/experiments` | List experiments with `limit` and `offset` |

A valid manual input example is available at
[`sample/manual/valid/uppercase_newline.txt`](sample/manual/valid/uppercase_newline.txt).
All manual and FASTA success and failure cases are documented in
[`sample/README.md`](sample/README.md).

## Repository layout

```text
backend/   FastAPI application and backend tests
docker/    Dockerfiles, Compose configuration, and Nginx configuration
frontend/  React application and Playwright tests
sample/    Labelled manual and FASTA test inputs
```
