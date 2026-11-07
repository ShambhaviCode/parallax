# PARALLAX
### Incident intelligence for systems that cannot afford guesswork.

PARALLAX is a demo-ready incident command product for distributed software teams. It turns a noisy service incident into a structured investigation: service impact, evidence-backed competing hypotheses, a controlled experiment, a recovery proposal, and an explicit human decision.

> **Demo honesty:** This repository ships with a deterministic simulated environment. The incident data, telemetry and experiment outcomes are simulated. The app does not execute production changes. Switch collaboration is supplied as a template and integration guide; it must be connected to a running Switch installation and live agent sessions before it can be claimed as operational.

## Product experience

- **Public product site** with a guided explanation and a live demo entry point.
- **Incident command center** with system health, incident impact, service topology and investigation progress.
- **Evidence ledger** that shows supporting and contradicting signals for competing hypotheses.
- **Counterfactual experiment** with a reproducible before/after comparison.
- **Human decision gate** for approving or rejecting a recovery proposal.
- **Incident report** export in Markdown and JSON.
- **Audit trail** for investigation and operator decisions.
- **Switch workflow template** for a watcher and investigator agent collaborating in a shared room.

## Quick start on Windows

### Option A: Docker Desktop
1. Install and start Docker Desktop.
2. Extract this repository.
3. Open PowerShell in the extracted `PARALLAX` folder.
4. Run:

```powershell
docker compose up --build
```

5. Open:
   - Product site and app: http://localhost:5173
   - API docs: http://localhost:8100/docs
   - API health: http://localhost:8100/api/health

Stop with `Ctrl+C`, then `docker compose down`.

### Option B: Run without Docker
Requirements: Python 3.11+ and Node.js 20.19+ (or Node.js 22+).

PowerShell terminal 1:
```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8100
```

PowerShell terminal 2:
```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## 90-second demo script
1. Open the product site and click **Open live command center**.
2. Show the active `INC-2048` incident and the affected service path.
3. Open the hypotheses. Explain why connection-pool exhaustion is the leading explanation, and point out the counter-signal rather than hiding it.
4. Run **Counterfactual test**. Show the controlled comparison and how the leading hypothesis changes.
5. Open the recovery proposal. Approve it with a decision note. Explain that this records a human decision only; it does not deploy a change.
6. Export the incident report.

## API surface
- `GET /api/health`
- `GET /api/overview`
- `GET /api/services`
- `GET /api/incidents`
- `GET /api/incidents/{incident_id}`
- `POST /api/incidents/{incident_id}/investigate`
- `POST /api/incidents/{incident_id}/experiment`
- `POST /api/incidents/{incident_id}/decision`
- `GET /api/incidents/{incident_id}/report?format=markdown|json`
- `GET /api/audit`
- `POST /api/demo/scenario`
- `POST /api/demo/reset`

## Switch: intended workflow
See [`switch/README.md`](switch/README.md) and [`switch/parallax.template.yaml`](switch/parallax.template.yaml). The template follows the public example shape published for the Flip the Switch hackathon. Switch is central to the intended team workflow: the watcher posts a detected incident, the investigator owns the evidence review, and a human operator reviews the recovery proposal in the same room.

**Important:** the template is not proof of a live Switch integration. Follow the current official Switch quickstart and agent protocol, validate the template in Switch Console, run both agent sessions, and capture the actual room interaction for the demo.

## Engineering
- Backend: Fastapi, SQLite, Pydantic.
- Frontend: React, TypeScript, Vite, Lucide.
- Tests: Pytest API and workflow tests.
- Persistence: SQLite file at `backend/parallax.db` (created at runtime).
- No external LLM key is required for the deterministic demo.

## Known boundaries
- Telemetry is simulated, not collected from production services.
- The experiment is a deterministic model of the incident, not a live database test.
- No production infrastructure is modified.
- Switch setup requires a separate Switch server, a supported provider/runtime, registered agents and active sessions.
- Run a production security review before exposing this demo to a public network.
