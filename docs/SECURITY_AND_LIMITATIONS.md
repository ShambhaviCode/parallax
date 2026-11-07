# Security and limitations

This is a hackathon demo, not a production deployment.

- Do not expose the API publicly without authentication, authorization, rate limits and TLS.
- CORS is configurable, but CORS is not authentication.
- SQLite is suitable for local demo persistence, not multi-user production scale.
- The demo uses simulated telemetry and deterministic investigation logic.
- The counterfactual experiment is a model, not a live infrastructure test.
- Recovery proposals are advisory. The API only records human decisions.
- Never place Switch credentials or provider API keys in source control.
- Give agents least-privilege access and use separate working directories.
- Verify current Switch protocol details against official docs; do not copy guessed endpoints from unofficial examples.
