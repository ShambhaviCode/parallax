
# PARALLAX
### Incident intelligence for systems that cannot afford guesswork.

PARALLAX is a demo-ready incident command product for distributed software teams. It turns a noisy service incident into a structured investigation: service impact, evidence-backed competing hypotheses, a controlled experiment, a recovery proposal, and an explicit human decision.

<img width="1917" height="897" alt="image" src="https://github.com/user-attachments/assets/41f429b1-61d2-4e72-9a11-9390de1cca11" />

## Product experience

- **Public product site** with a guided explanation and a live demo entry point.
- **Incident command center** with system health, incident impact, service topology and investigation progress.
- **Evidence ledger** that shows supporting and contradicting signals for competing hypotheses.
- **Counterfactual experiment** with a reproducible before/after comparison.
- **Human decision gate** for approving or rejecting a recovery proposal.
- **Incident report** export in Markdown and JSON.
- **Audit trail** for investigation and operator decisions.
- **Switch workflow template** for a watcher and investigator agent collaborating in a shared room.




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
=======
# parallax
AI powered incident intelligence platform using Switch-connected agents to detect incidents, investigate root causes, analyze evidence, and support human in the loop decisions.
