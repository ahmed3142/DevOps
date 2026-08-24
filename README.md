# Nimbus Notes

A deliberately tiny Next.js notes service, built as the **artefact repository (Deliverable 2)** for the Learnkey Institute assessment *"Design, Justify and Present a DevOps Delivery Strategy"* (Scenario B — a SaaS start-up outgrowing manual scripts). The application itself is trivial by design: the graded material is the delivery machinery around it — the version-control workflow, the CI pipeline, and the container/infrastructure artefacts described below.

## How this maps to the brief

| Brief requirement | Where to look |
| --- | --- |
| Sensible commit history, at least one branch, a merge, a tagged release | `git log --graph --oneline` — small conventional commits, `feature/*` branches merged with merge commits, annotated release tag `v1.0.0` |
| Working CI workflow that builds and runs tests | [.github/workflows/ci.yml](.github/workflows/ci.yml) |
| Container / infrastructure artefact with explanation | [Dockerfile](Dockerfile), [compose.yml](compose.yml), [infra/main.tf](infra/main.tf) — explanations below |

## Running it

```bash
npm ci            # install exact locked dependencies
npm run dev       # local development server on :3000
npm test          # unit tests (Vitest)
npm run lint      # ESLint
npm run build     # production build

docker compose up --build   # containerised production build on :3000
```

## API

| Route | Method | Behaviour |
| --- | --- | --- |
| `/api/health` | GET | Liveness probe: status, running version, uptime |
| `/api/notes` | GET | List notes (in-memory) |
| `/api/notes` | POST | Create a note — `{"text": "..."}`; 400 if `text` missing/blank |

## Artefact notes

**CI workflow (`.github/workflows/ci.yml`).** Every push and pull request runs the same gate: install from the lockfile, lint, unit tests, then a production build; a second job builds the container image from the same commit. This means broken code is caught in minutes on a disposable runner instead of during a manual deploy, and the image that ships is produced by the pipeline, not by whoever happens to have a working laptop. Image publishing to a registry is intentionally left as the next step of the delivery strategy rather than baked in here.

**Dockerfile.** A three-stage build: dependencies are installed from the lockfile only, the production bundle is compiled, and the final image contains nothing but the Next.js standalone server, running as an unprivileged user on a minimal Alpine base. The same image runs identically on a laptop, in CI, and in production — which is the direct fix for the "works on my machine / environments drift" problem in the scenario.

**Compose file (`compose.yml`).** Defines how the container runs as code: port mapping, restart policy, and a healthcheck that polls `/api/health`. The healthcheck is what turns "the container is running" into "the service is actually answering", and is the hook an orchestrator or deploy script uses to decide whether a new release is healthy or should be rolled back.

**Terraform snippet (`infra/main.tf`).** Illustrative only — it is not applied to any real cloud account. It shows how the production host would be captured as reviewable, versioned code instead of a hand-configured server: the instance size lives in one obvious place, environments are stamped from the same definition, and every resource carries `Owner`/`CostCentre`/`Environment` tags so the cloud bill can be attributed (the FinOps practice argued in the report).

## Releases

Releases are annotated tags (`v1.0.0`) on `main`. The health endpoint reports the running version, so any environment can be traced back to the exact tagged commit that produced it.
