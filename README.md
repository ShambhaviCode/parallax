
# PARALLAX



<img width="1917" height="898" alt="Screenshot 2026-11-07 201231" src="https://github.com/user-attachments/assets/7b2d91c9-0435-4ae3-ba9c-88babca990a5" />


<img width="1697" height="871" alt="Screenshot 2026-11-07 201557" src="https://github.com/user-attachments/assets/44ae55dc-81c2-4770-ad17-a3bd43cff254" />


<img width="1686" height="892" alt="Screenshot 2026-11-07 201657" src="https://github.com/user-attachments/assets/fd187ad1-6654-4818-b406-293cabf1dbf3" />

<img width="1911" height="916" alt="Screenshot 2026-11-07 202032" src="https://github.com/user-attachments/assets/7198e697-4c4c-465f-b1fd-5ed9d8a34c6c" />

<img width="1890" height="891" alt="Screenshot 2026-11-07 202142" src="https://github.com/user-attachments/assets/08ddaa9e-1716-4784-bc62-e43b4bd9f786" />




## Demo

Live Application:https://parallax-delta-one.vercel.app/



### See the Signal. Prove the Cause.

**AI-powered incident intelligence through collaborative multi-agent investigation.**

PARALLAX is an AI-powered incident intelligence platform designed to help engineering teams move beyond traditional monitoring and understand the actual causes behind production incidents.

Instead of simply notifying teams when something goes wrong, PARALLAX aims to investigate why it happened by combining system telemetry, service dependencies, evidence analysis, and specialized AI agents.

Built around a human-in-the-loop philosophy, PARALLAX brings incident detection, investigation, recommendations, and decision tracking into one unified command center.

---

## The Problem

Imagine being an engineer during a production incident.

Latency is increasing. Services are failing. Error rates are rising. Multiple dashboards are showing different signals, and everyone is trying to identify the root cause.

The problem isn't always a lack of data. It's the difficulty of connecting that data into a clear explanation.

Traditional monitoring systems are good at telling teams that something is wrong. PARALLAX explores how AI agents can help teams understand why.

## Our Solution

PARALLAX introduces a collaborative multi-agent incident investigation workflow powered by **Switch**.

Instead of relying on one general-purpose AI agent, we designed two specialized agents with distinct responsibilities.

### Meet the Agents

#### 1. `parallax-watch` | Incident Observer

Responsible for identifying suspicious system behavior and initiating incident handoffs.

- Detects potential incidents from available signals.
- Identifies relevant incident context.
- Prepares structured incident handoffs.
- Sends investigation requests to the specialist agent through the shared Switch room.

#### 2. `parallax-investigator` | Evidence Investigator

Responsible for deeper incident analysis.

- Receives incident handoffs.
- Retrieves relevant evidence.
- Examines service dependencies and system signals.
- Evaluates competing root-cause hypotheses.
- Challenges assumptions instead of blindly accepting the first explanation.
- Prepares structured investigation reports and recommendations.

### How the Agents Collaborate

```text
       SYSTEM TELEMETRY
              |
              v
      +----------------+
      | parallax-watch |
      | Incident Agent |
      +----------------+
              |
              | Structured Handoff
              v
      +----------------+
      |  SWITCH ROOM   |
      | Communication  |
      +----------------+
              |
              v
 +------------------------+
 | parallax-investigator  |
 |  Investigation Agent   |
 +------------------------+
              |
              v
      +----------------+
      | Evidence-Based |
      | Investigation  |
      +----------------+
              |
              v
      +----------------+
      | Human Operator |
      +----------------+
          /       \
      APPROVE    REJECT
          \       /
              |
              v
      +----------------+
      | PARALLAX Audit |
      | & Decision Log |
      +----------------+
```

Switch acts as the communication layer connecting the specialized agent sessions.

**The core principle: One agent detects. Another investigates. A human decides.**

---

## Features

### 1. Incident Intelligence Command Center

A unified interface for monitoring incidents, understanding system behavior, and reviewing investigation progress.

### 2. Service Topology

Visualize service relationships and dependencies to understand how failures in one component may affect others.

### 3. Telemetry Insights

Bring relevant system signals into the investigation process, including latency, errors, service health, and SLO-related information.

### 4. Counterfactual Lab

Explore alternative scenarios and examine how proposed changes could affect system behavior.

### 5. Specialist Perspectives

Organize investigation perspectives such as signal analysis, trace analysis, and causal reasoning.

### 6. Evidence-Based Reports

Generate structured investigation reports containing findings, supporting evidence, competing hypotheses, and recommendations.

### 7. Human-in-the-Loop Decisions

Operators review recommendations and explicitly approve or reject proposed actions.

### 8. Audit Trail

Keep investigation reports and recorded decisions accessible in the PARALLAX application.

---

## Technology Stack

The project is organized around a modern web frontend, a Python backend, and a multi-agent communication workflow.

| Component | Technology |
|---|---|
| Frontend | React |
| Build Tool | Vite |
| Backend | Python / FastAPI |
| Agent Communication | Switch |
| Agent Architecture | Specialized multi-agent workflow |
| Deployment | Vercel (frontend) |
| Backend Hosting | To be configured |

Additional libraries and services are documented in their respective project dependency files.

---

## Project Structure

```text
PARALLAX/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── requirements.txt
│   └── ...
│
├── docker-compose.yml
├── parallax.template.yaml
├── README.md
└── ...
```

The exact contents may vary depending on the current project version.

---

## Getting Started

### Prerequisites

Make sure you have:

- Git
- Node.js and npm
- Python 3
- Docker and Docker Compose
- Switch Console installed and configured for the intended workflow

### 1. Clone the Repository

```bash
git clone https://github.com/ShambhaviCode/parallax.git
cd parallax
```

### 2. Set Up the Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

### 3. Set Up the Backend

Open a separate terminal:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend using the actual FastAPI application module and configuration in your project.

For example, if the application object is named `app` in `main.py`:

```bash
uvicorn main:app --reload
```

### 4. Run with Docker

If Docker Compose is configured for your environment:

```bash
docker compose up --build
```

To stop the containers:

```bash
docker compose down
```

---

## Switch Integration

PARALLAX is designed around Switch's multi-agent communication model.

The intended workflow consists of:

1. Installing Switch Console using the official quickstart.
2. Confirming that the local Switch server is healthy.
3. Creating a shared room using `parallax.template.yaml` and the supported Console/template workflow.
4. Configuring the provider and bridge values supported by the installed Switch version.
5. Registering `parallax-watch` and `parallax-investigator`.
6. Inviting both agents to the shared room.
7. Starting a live session for each agent.
8. Giving each agent access only to the required PARALLAX API and working directory.
9. Testing the incident handoff and reviewing the actual room transcript.

**Important:** Room membership does not automatically mean an agent session is running.

Switch protocol endpoints, authentication headers, registration credentials, and environment variables are version-specific. Follow the official documentation for the installed Switch version rather than assuming endpoints or credentials.

---

## Human-in-the-Loop Philosophy

We believe AI should support engineering decisions, not silently make them.

PARALLAX keeps the human operator involved at the most important stage.

The investigator prepares evidence and recommendations. The operator reviews the findings and decides whether to approve or reject the proposed action.

This creates a workflow focused on:

- Transparency
- Accountability
- Evidence-backed decisions
- Traceability
- Human control

---


## What Makes PARALLAX Different?

Most monitoring tools focus on detecting and displaying problems.

PARALLAX explores a different approach: connecting incident detection with collaborative investigation.

Rather than treating AI as a single assistant, we use specialized agents with distinct responsibilities and a structured handoff between them.

Our objective is to make incident investigation more understandable, organized, and accountable.

---

## Future Scope

We envision extending PARALLAX with:

- More specialized investigation agents.
- Deeper observability integrations.
- Improved distributed tracing analysis.
- Automated evidence correlation.
- Richer investigation timelines.
- More advanced counterfactual analysis.
- Expanded agent collaboration workflows.
- Stronger incident reporting and decision analytics.

---

## Built With Switch

PARALLAX explores how collaborative AI agents can work together to address real engineering challenges.

We believe the future of AI-powered engineering is not necessarily one agent doing everything. It is specialized agents collaborating, challenging assumptions, and helping humans make better decisions.

**See the signal. Prove the cause.**

---

## Author

**Shambhavi**



---

