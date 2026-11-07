# Test and verification checklist

## Backend
```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

Expected: six workflow tests pass.

## Frontend
```powershell
cd frontend
npm install
npm run build
```

## Manual acceptance
- [ ] Landing page opens and all nav anchors work.
- [ ] Launch command center opens the application.
- [ ] Dashboard loads from API.
- [ ] Service nodes show status and latency on click.
- [ ] Investigation button returns success and refreshes audit events.
- [ ] Scenario controls change service health.
- [ ] Counterfactual experiment displays before/after metrics.
- [ ] Approve and reject require a note and persist the decision.
- [ ] Markdown and JSON report downloads work.
- [ ] Reset restores the seeded demo.
- [ ] Mobile layout works at 390px width.
- [ ] Switch room template is validated in the installed Switch Console.
- [ ] Both Switch agent sessions are running and complete a real handoff.
