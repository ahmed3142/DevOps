# Nimbus Notes

A small Next.js notes service. It is the artefact repository for the Learnkey Institute DevOps assessment (Scenario B) — the application is deliberately trivial, and the point of the repository is the delivery tooling around it.

## Stack

Next.js 16 (App Router, TypeScript) · Vitest · Docker · GitHub Actions

## Commands

```bash
npm ci            # install from the lockfile
npm run dev       # development server on :3000
npm test          # unit tests
npm run lint      # ESLint
npm run build     # production build

docker compose up --build   # containerised build on :3000
```

## API

| Route | Method | Behaviour |
| --- | --- | --- |
| `/api/health` | GET | Status, running version, uptime |
| `/api/notes` | GET | List notes |
| `/api/notes` | POST | Create a note — `{"text": "..."}`; 400 if `text` is missing or blank |

Notes are held in memory and reset when the process restarts.

## Layout

| Path | Contents |
| --- | --- |
| `app/api/health/route.ts` | Health endpoint; reports the version from `package.json` |
| `app/api/notes/route.ts` | Notes list and create routes |
| `lib/notes.ts` | In-memory store |
| `tests/` | Vitest unit tests for the store and both routes |
| `.github/workflows/ci.yml` | CI pipeline |
| `Dockerfile`, `.dockerignore` | Three-stage container build |
| `compose.yml` | Local run with a health check |
| `infra/main.tf` | Terraform snippet — illustrative only, not applied to any account |

## CI

`.github/workflows/ci.yml` runs on every push and pull request:

1. `build-test` — install from the lockfile, lint, unit tests, production build
2. `docker-image` — builds the container image from the same commit (build only, no registry push)

## Releases

Releases are annotated tags on `main` (`v1.0.0`). `/api/health` returns the running version, so a deployed environment can be traced back to the commit that produced it.

```bash
git log --graph --oneline --all
git tag -n1
```
