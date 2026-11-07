# Switch workflow

PARALLAX's intended Switch workflow is not a notification-only integration:

1. `parallax-watch` runs as a separate agent session and detects/posts an incident handoff.
2. `parallax-investigator` receives the handoff, retrieves evidence, challenges hypotheses and prepares a report.
3. The human operator reviews the recommendation and records approve/reject.
4. The report and decision remain available in the PARALLAX application.

## Setup
1. Install Switch Console and Docker using the official Switch quickstart.
2. Confirm the local Switch server is healthy.
3. Create a room from `parallax.template.yaml` using the current Console/template workflow.
4. Replace `{provider}` and `{bridge}` using the values supported by your installed Switch version.
5. Register both agents and invite them to the shared room.
6. Start a live session for each agent. Room membership alone does not mean an agent is running.
7. Give each agent access only to the PARALLAX demo API and the intended working directory.
8. Test the handoff with the seeded incident and capture the real room transcript.

## Protocol caution
The hackathon page describes Switch as an agent protocol with server-sent events inbound and HTTP outbound. The exact endpoints, headers, registration credentials and environment variables are version-specific. This repo intentionally does not invent those details or include a fake Switch client. Use the official docs and the version of Switch Console you actually run.

## Evidence to include in the submission
- Screenshot of the shared room with both agents present.
- Screenshot showing both agent sessions running.
- A watcher incident handoff addressed to the investigator.
- Investigator's evidence-backed response.
- Human approval/rejection recorded in the room and PARALLAX.
- Short clip showing the full task, not just agent chat.
