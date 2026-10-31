# CredYazh — Team Setup Guide

> **One command to run the entire project.** This guide gets any teammate from zero to a fully running CredYazh on their laptop in under 10 minutes.

---

## Prerequisites

Install these once on your laptop (all free):

| Tool | Version | Download |
|---|---|---|
| **Docker Desktop** | Latest | https://www.docker.com/products/docker-desktop |
| **Git** | Any | https://git-scm.com |

> You do **not** need Node.js, Python, npm, pip, or any language runtime installed locally. Docker handles everything.

---

## First-Time Setup (5 steps)

### Step 1 — Clone the repository

```bash
git clone <your-team-repo-url>
cd credyazh-prototype
```

---

### Step 2 — Create the AI service `.env`

```bash
cp credyazh/ai-service/.env.example credyazh/ai-service/.env
```

Open `credyazh/ai-service/.env` and fill in:

```ini
# Required — get this from the team lead or Google AI Studio
GEMINI_API_KEY=your_key_here

# Everything else is pre-configured with safe defaults — do not change unless told to
GEMINI_MODELS=gemini-3.5-flash-lite,gemini-3.5-flash
AI_SHARED_DEADLINE_MS=35000
GEMINI_REQUEST_TIMEOUT_MS=12000
GEMINI_MIN_ATTEMPT_BUDGET_MS=10000
GEMINI_RATE_LIMIT_BACKOFF_MS=250
GEMINI_MAX_OUTPUT_TOKENS=1024
ENABLE_LOCAL_EXTRACTOR=true
AI_FAILOVER_ENABLED=false
```

---

### Step 3 — Create the server `.env`

```bash
cp credyazh/server/.env.example credyazh/server/.env
```

Open `credyazh/server/.env` and fill in:

```ini
PORT=4000

# Required — get this from the team lead (MongoDB Atlas connection string)
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/credyazh?retryWrites=true&w=majority

# Leave exactly as-is for Docker (ai-service is the container name)
AI_SERVICE_URL=http://ai-service:8000
AI_CLIENT_TIMEOUT_MS=40000
```

> **Important:** `AI_SERVICE_URL` must stay as `http://ai-service:8000` when running with Docker. Do **not** change it to `localhost`.

---

### Step 4 — Build & start everything

From the project root (where `compose.yaml` lives):

```bash
docker compose up --build
```

This will:
1. Build the Python AI service image
2. Build the Node.js Express server image
3. Build the React PWA and serve it via Nginx
4. Start all three containers and wire them together

> First build takes **3–5 minutes** (downloading images and installing packages).  
> Subsequent starts (no code changes) take **< 15 seconds**.

---

### Step 5 — Open the app

```
http://localhost
```

That's it. 🎉

---

## Daily Workflow

### Start the project
```bash
docker compose up
```

### Start in background (detached)
```bash
docker compose up -d
```

### Stop everything
```bash
docker compose down
```

### Rebuild after code changes
```bash
docker compose up --build
```

### View live logs
```bash
# All services
docker compose logs -f

# One service only
docker compose logs -f ai-service
docker compose logs -f server
docker compose logs -f client
```

### Open a shell inside a container (for debugging)
```bash
docker compose exec ai-service bash
docker compose exec server sh
```

---

## Service Map

| Service | Container Name | Internal URL | Exposed Port |
|---|---|---|---|
| React PWA | `credyazh-client` | — | **http://localhost** (port 80) |
| Express API | `credyazh-server` | `http://server:4000` | http://localhost:4000 |
| FastAPI AI | `credyazh-ai` | `http://ai-service:8000` | http://localhost:8000 |

```
Your Browser
     │
     ▼  http://localhost
┌─────────────────────────┐
│  Nginx (credyazh-client)│
│  serves React PWA       │
│                         │
│  /api/* → proxy         │
└────────────┬────────────┘
             │
             ▼  http://server:4000
┌─────────────────────────┐
│  Express (credyazh-     │
│  server)                │
│  REST API, DB, Zod      │
└────────────┬────────────┘
             │
             ▼  http://ai-service:8000
┌─────────────────────────┐
│  FastAPI (credyazh-ai)  │
│  Gemini extraction      │
│  Local regex fast-path  │
└─────────────────────────┘
             │
             ▼  HTTPS (internet)
        Google Gemini API
```

---

## Checking Service Health

Each service has a health check built in:

```bash
# AI service
curl http://localhost:8000/health

# Express server
curl http://localhost:4000/api/customers

# Check all container statuses
docker compose ps
```

A healthy output looks like:
```
NAME                 STATUS          PORTS
credyazh-ai          Up (healthy)    0.0.0.0:8000->8000/tcp
credyazh-server      Up (healthy)    0.0.0.0:4000->4000/tcp
credyazh-client      Up              0.0.0.0:80->80/tcp
```

---

## Troubleshooting

### Port 80 already in use
Another app is using port 80. Either stop it or change the client port in `compose.yaml`:
```yaml
ports:
  - "3000:80"   # access at http://localhost:3000 instead
```

### `GEMINI_API_KEY` missing error
The AI service `.env` file is missing or the key is empty. Re-check Step 2.

### MongoDB connection failed
- Make sure your `MONGODB_URI` in `server/.env` is correct
- Check that your IP is whitelisted in MongoDB Atlas → Network Access

### Container exits immediately
Run with logs to see the error:
```bash
docker compose up --build --no-deps ai-service
docker compose up --build --no-deps server
```

### Code change not reflected
Run `docker compose up --build` to rebuild the changed service.

### Starting fresh (nuclear reset)
```bash
docker compose down --volumes --rmi all
docker compose up --build
```

---

## For Local Development (Without Docker)

If you want to run services directly (faster reload during active development):

```bash
# Terminal 1 — AI service
cd credyazh/ai-service
python -m venv .venv
.venv/Scripts/activate        # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — Express server
# Edit server/.env: change AI_SERVICE_URL=http://localhost:8000
cd credyazh/server
npm install
npm run dev

# Terminal 3 — React client
cd credyazh/client
npm install
npm run dev
# Open http://localhost:5173
```

> When running locally (not Docker), change `AI_SERVICE_URL` in `server/.env` to `http://localhost:8000`.

---

## File Reference

```
credyazh-prototype/
├── compose.yaml                      ← Run this file with Docker Compose
├── credyazh/
│   ├── ai-service/
│   │   ├── Dockerfile                ← Python FastAPI image definition
│   │   ├── .env.example              ← Copy → .env and fill GEMINI_API_KEY
│   │   └── .env                      ← Your local secrets (git-ignored)
│   ├── server/
│   │   ├── Dockerfile                ← Node.js Express image definition
│   │   ├── .env.example              ← Copy → .env and fill MONGODB_URI
│   │   └── .env                      ← Your local secrets (git-ignored)
│   └── client/
│       ├── Dockerfile                ← React build + Nginx image definition
│       └── nginx.conf                ← Nginx proxy config (/api → server)
└── TEAM_SETUP.md                     ← This file
```

---

> **Need help?** Ping the team lead or check the `ARCHITECTURE.md` for how all the pieces fit together.

