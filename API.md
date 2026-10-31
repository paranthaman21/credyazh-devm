# CredYazh — API Integration & Interface Specification (API.md)

**Product:** CredYazh  
**Tagline:** *From voice to ledger instantly.*  
**System Role:** API Contracts, Internal Micro-Interfaces & External Integrations  
**Document Status:** Production API Blueprint (Derived from `FrontPage-CY_merged.md`, `ARCHITECTURE.md`, and `DATABASE.md`)  

---

## 1. Architectural Interface Topology

CredYazh enforces a strict boundary between public counter interactions, internal orchestration, and third-party cloud engines:

```mermaid
flowchart TD
    subgraph ClientZone ["Public Client Zone (Browser / Android PWA)"]
        UI["React 18 PWA"]
    end

    subgraph EdgeZone ["Protected API Gateway (Port 4000)"]
        EXPRESS["Express API Gateway"]
        AUTH["Tenant Guard (shopId)"]
        ZOD["Zod Validation & Math"]
        IDEM["Idempotency Filter"]
    end

    subgraph PrivateAIZone ["Private Internal Network (Port 8000)"]
        FASTAPI["FastAPI Extraction Gateway"]
        PYD["Pydantic v2 Schema Engine"]
        FALLBACK["Multi-Model Failover Cascade"]
    end

    subgraph ExternalZone ["External Third-Party Services"]
        GEMINI["Google Gemini API (HTTPS)"]
        WA["WhatsApp Client (wa.me) / Cloud API"]
    end

    subgraph DataZone ["Database Tier"]
        MONGO[("MongoDB Atlas")]
    end

    UI -->|HTTPS /api/* (Public REST)| EXPRESS
    EXPRESS --> AUTH
    AUTH --> ZOD
    ZOD --> IDEM
    IDEM --> MONGO
    EXPRESS -->|Private HTTP /draft/* (Internal Only)| FASTAPI
    FASTAPI --> PYD
    PYD --> FALLBACK
    FALLBACK -->|Secure HTTPS (REST / gRPC)| GEMINI
    UI -.->|Merchant Deep Link (wa.me)| WA
```

### Core Interface Rules:
1. **Zero Client Secrets:** The React PWA never possesses database credentials or Google Gemini API keys.
2. **AI Isolation:** The FastAPI AI Gateway has no MongoDB driver and cannot read or write to the database. It strictly performs in-memory natural language and audio parsing.
3. **Internal Network Boundary:** Port 8000 (FastAPI) is bound to `127.0.0.1` (or an internal VPC subnet). Only Port 4000 (Express) exposes public endpoints to the PWA.

---

## 2. Global Request & Response Conventions

### 2.1. Headers Contract

| Header Name | Requirement | Example | Description |
| :--- | :--- | :--- | :--- |
| `Content-Type` | Required for JSON | `application/json` | MIME type for structured payloads |
| `Idempotency-Key` | Mandatory on `POST /api/ledger` | `c4b79b8a-7d12-4f3b-9e8a-028a49c25e1a` | Client-generated UUIDv4 preventing double-commit |
| `Authorization` | Mandatory in Production | `Bearer eyJhbGciOi...` | Merchant JWT containing `shopId` and `role` |
| `Server-Timing` | Injected by Server | `total;dur=1438, ai;dur=1210, db;dur=12` | W3C performance metrics for telemetry |

### 2.2. Standard Error Response Envelope
All error responses adhere to the RFC 7807 problem details specification:
```json
{
  "error": "Human-readable explanation of failure",
  "code": "ERROR_ENUM_CODE",
  "details": {
    "field": "signedAmountPaise",
    "issue": "Expected integer paise, received float"
  },
  "requestId": "req_89f02a3b"
}
```

### 2.3. HTTP Status Code Taxonomy
- `200 OK`: Successful synchronous retrieval or idempotent duplicate return.
- `201 Created`: Immutable resource committed to MongoDB.
- `400 Bad Request`: Zod validation failure, float paise detected, or missing required headers.
- `401 Unauthorized`: Missing or invalid authentication token.
- `403 Forbidden`: Cross-tenant access violation.
- `404 Not Found`: Customer or transaction does not exist under current `shopId`.
- `409 Conflict`: Reversal of an already reversed entry, or `Idempotency-Key` payload mismatch.
- `502 Bad Gateway`: Internal FastAPI AI service unreachable or model extraction failed.
- `503 Service Unavailable`: Google Gemini upstream API authentication failure or global cloud outage.

---

## 3. Public REST API Endpoints (Express Gateway — Port 4000)

### 3.1. Voice & Text Extraction (Gate 1)

#### `POST /api/draft/audio`
Translates spoken 16 kHz Mono PCM WAV audio (Tamil, Tanglish, or English) into an editable draft transaction.

- **Content-Type:** `multipart/form-data`
- **Payload:** Form field `audio` containing binary WAV blob ($\le 5\text{ MB}$).
- **Validation:** Multer verifies MIME type (`audio/wav`, `audio/wave`, `audio/x-wav`) and file size limit.
- **Response (`200 OK`):**
```json
{
  "kind": "credit",
  "customerName": "Kumar",
  "matchedCustomerId": "6627a1b0c9e123456789abcd",
  "candidateCustomers": [],
  "items": [
    { "name": "paruppu", "quantity": "0.5", "unit": "kg", "pricePaise": null },
    { "name": "paal", "quantity": "1", "unit": "litre", "pricePaise": null }
  ],
  "totalPaise": 16000,
  "operations": [],
  "transcript": "Kumar account-la arai kilo paruppu, oru litre paal, total 160 rupees",
  "confidence": "high",
  "warnings": [],
  "metrics": {
    "serverTotalMs": 1438,
    "aiCallMs": 1210,
    "dbLatencyMs": 12,
    "geminiLatencyMs": 1180
  }
}
```
- **Response Headers:**
  `Server-Timing: total;dur=1438, ai;dur=1210, db;dur=12, gemini;dur=1180`

#### `POST /api/draft/text`
Parses typed Tamil script, Tanglish, or English sentences.
- **Content-Type:** `application/json`
- **Request Body:**
```json
{
  "text": "Kumar 200 kuduthutu 70-ku arisi vaanginaan"
}
```
- **Response (`200 OK`):** Returns combined operation draft:
```json
{
  "kind": "combined",
  "customerName": "Kumar",
  "matchedCustomerId": "6627a1b0c9e123456789abcd",
  "operations": [
    {
      "kind": "payment",
      "totalPaise": 20000,
      "items": []
    },
    {
      "kind": "credit",
      "totalPaise": 7000,
      "items": [{ "name": "Rice", "quantity": "1", "unit": "unit", "pricePaise": null }]
    }
  ],
  "confidence": "high",
  "warnings": []
}
```

---

### 3.2. Customer Management

#### `GET /api/customers`
Retrieves the active customer directory with dynamically aggregated running balances.
- **Query Parameters:**
  - `archived` (optional, boolean): `false` (default) returns active customers; `true` returns archived.
  - `query` (optional, string): Search filter matching `name`, `phone`, or `aliases`.
  - `limit` (optional, integer): Pagination limit (default: `50`, max: `200`).
  - `skip` (optional, integer): Pagination offset (default: `0`).
- **Response (`200 OK`):**
```json
[
  {
    "_id": "6627a1b0c9e123456789abcd",
    "shopId": "demo-shop",
    "name": "Kumar",
    "phone": "9876543210",
    "aliases": ["Kumar tea shop", "Annachi"],
    "creditLimitPaise": 500000,
    "archived": false,
    "balancePaise": 37000,
    "createdAt": "2026-10-23T10:15:30.000Z"
  }
]
```

#### `POST /api/customers`
Enrolls a new customer under the current tenant.
- **Request Body:**
```json
{
  "name": "Murugan Provisions",
  "phone": "9123456780",
  "aliases": ["Murugan", "Muru"],
  "creditLimitPaise": 1000000
}
```
- **Validation:** `name` must be 1–100 characters; `phone` must be numeric 10-digits or E.164.
- **Response (`201 Created`):** Returns customer document with `balancePaise: 0`.

#### `PUT /api/customers/:id`
Updates customer profile attributes.
- **Response (`200 OK`):** Updated document with fresh balance.

#### `DELETE /api/customers/:id`
Enforces the **Settle-Before-Delete Rule**. Soft-deletes a customer by setting `archived: true`.
- **Validation:** If dynamically aggregated `balancePaise !== 0`, the deletion is rejected.
- **Error Response (`400 Bad Request`):**
```json
{
  "error": "Cannot delete customer with active balance of Rs 370.00. Please settle the balance first.",
  "code": "CUSTOMER_BALANCE_NON_ZERO",
  "details": { "currentBalancePaise": 37000 }
}
```
- **Success Response (`200 OK`):** `{"ok": true, "archived": true, "id": "6627a1b0c9e123456789abcd"}`

#### `PUT /api/customers/:id/restore`
Restores an archived customer to the active directory.
- **Response (`200 OK`):** `{"_id": "...", "archived": false, "balancePaise": 0}`

---

### 3.3. Ledger Event Operations (Gate 2)

#### `POST /api/ledger`
Commits merchant-confirmed transactions to the append-only ledger.
- **Mandatory Header:** `Idempotency-Key: <UUIDv4>`
- **Request Body (Single Operation):**
```json
{
  "kind": "credit",
  "customerId": "6627a1b0c9e123456789abcd",
  "totalPaise": 16000,
  "items": [
    { "name": "paruppu", "quantity": "0.5", "unit": "kg", "pricePaise": null },
    { "name": "paal", "quantity": "1", "unit": "litre", "pricePaise": null }
  ],
  "source": "voice",
  "transcript": "Kumar account-la arai kilo paruppu, oru litre paal, total 160 rupees"
}
```

- **Request Body (Combined Batch Operation):**
```json
{
  "kind": "combined",
  "customerId": "6627a1b0c9e123456789abcd",
  "operations": [
    { "kind": "payment", "totalPaise": 20000, "items": [] },
    { "kind": "credit", "totalPaise": 7000, "items": [{ "name": "Rice", "quantity": "1", "unit": "unit" }] }
  ],
  "source": "voice",
  "transcript": "Kumar 200 kuduthutu 70-ku arisi vaanginaan"
}
```

- **Response (`201 Created` — First Submission):**
```json
{
  "events": [
    {
      "_id": "6627b2c0c9e9876543210001",
      "shopId": "demo-shop",
      "customerId": "6627a1b0c9e123456789abcd",
      "type": "PAYMENT",
      "signedAmountPaise": -20000,
      "groupId": "c4b79b8a-7d12-4f3b-9e8a-028a49c25e1a",
      "batchIndex": 0,
      "idempotencyKey": "c4b79b8a-7d12-4f3b-9e8a-028a49c25e1a:payment:0",
      "createdAt": "2026-10-23T11:00:00.000Z"
    },
    {
      "_id": "6627b2c0c9e9876543210002",
      "shopId": "demo-shop",
      "customerId": "6627a1b0c9e123456789abcd",
      "type": "CREDIT",
      "signedAmountPaise": 7000,
      "groupId": "c4b79b8a-7d12-4f3b-9e8a-028a49c25e1a",
      "batchIndex": 1,
      "idempotencyKey": "c4b79b8a-7d12-4f3b-9e8a-028a49c25e1a:credit:1",
      "createdAt": "2026-10-23T11:00:00.001Z"
    }
  ],
  "duplicate": false
}
```

- **Response (`200 OK` — Idempotent Retry):**
  If the merchant retries or double taps with the same `Idempotency-Key`:
```json
{
  "events": [ /* Existing committed documents */ ],
  "duplicate": true
}
```

#### `POST /api/ledger/:id/reverse`
Executes an auditable financial reversal.
- **Request Body:**
```json
{
  "reason": "Customer corrected purchase quantity on counter"
}
```
- **Validation & Guard Rails:**
  1. If `original.type === 'REVERSAL'`, rejects with `HTTP 409 Conflict: a reversal cannot be reversed`.
  2. If `reversesEventId` unique index conflicts, rejects with `HTTP 409 Conflict: this entry is already reversed`.
- **Response (`201 Created`):**
```json
{
  "event": {
    "_id": "6627c3d0c9e1112223334445",
    "shopId": "demo-shop",
    "customerId": "6627a1b0c9e123456789abcd",
    "type": "REVERSAL",
    "signedAmountPaise": -16000,
    "reversesEventId": "6627b2c0c9e9876543210001",
    "reason": "Customer corrected purchase quantity on counter",
    "createdAt": "2026-10-23T11:05:00.000Z"
  }
}
```

#### `GET /api/customers/:id/ledger`
Fetches complete chronological customer ledger statements.
- **Response (`200 OK`):**
```json
{
  "customer": { "_id": "...", "name": "Kumar" },
  "balancePaise": 37000,
  "totalCreditPaise": 57000,
  "totalPaymentPaise": 20000,
  "events": [
    {
      "_id": "...",
      "type": "CREDIT",
      "signedAmountPaise": 16000,
      "items": [{ "name": "paruppu", "quantity": "0.5", "unit": "kg" }],
      "isReversed": false,
      "createdAt": "2026-10-23T11:00:00.000Z"
    }
  ]
}
```

---

### 3.4. WhatsApp Statement Generation

#### `POST /api/customers/:id/whatsapp-message`
Generates a respectful, culturally aligned bilingual statement formatted for WhatsApp.
- **Request Body:**
```json
{
  "language": "tamil"
}
```
- **Enum for `language`:** `english` | `tamil` | `tanglish`
- **Response (`200 OK`):**
```json
{
  "message": "வணக்கம் Kumar, Demo Kirana Shop-லிருந்து உங்கள் கணக்கு விவரம்:\n\nதற்போதைய நிலுவைத் தொகை: ₹370.00\nமொத்த வரவு: ₹570.00 | செலுத்தியது: ₹200.00\n\nசமீபத்திய பரிவர்த்தனைகள்:\n- 23 Oct: Dal 0.5kg, Milk 1L (Credit) ₹160.00\n- 23 Oct: Cash Payment (Payment) ₹200.00\n\nஏதேனும் சந்தேகம் இருப்பின் எங்களை தொடர்பு கொள்ளவும். நன்றி!",
  "language": "tamil",
  "phone": "9876543210",
  "whatsappUrl": "https://wa.me/919876543210?text=%E0%AE%B5%E0%AE%A3%E0%AE%95%E0%AF%8D%E0%AE%95%E0%AE%AE%E0%AF%8D..."
}
```

---

## 4. Internal API Endpoints (FastAPI AI Gateway — Port 8000)

These endpoints are strictly internal to the server tier.

### 4.1. `POST /draft/audio`
- **Input:** Multipart WAV file stream.
- **Internal Action:** Dispatches audio byte parts to `client.models.generate_content` using `response_schema=Draft`.
- **Response:** Pydantic validated `DraftResponse` including timing metrics.

### 4.2. `POST /draft/text`
- **Input:** `{"text": "string"}`.
- **Internal Action:** Dispatches text string to Gemini extraction pipeline.

### 4.3. `GET /health`
- **Response (`200 OK`):**
```json
{
  "ok": true,
  "primary_model": "gemini-3.5-flash-lite",
  "configured_models": [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash"
  ],
  "total_models": 4
}
```

---

## 5. External Service Integrations & Webhooks

### 5.1. Google Gemini API Integration

```
FastAPI Gateway ──> HTTPS POST https://generativelanguage.googleapis.com/v1beta/models/...
```
- **SDK:** `google-genai` Python SDK v1.0+.
- **Authentication:** Injected via server environment variable `GEMINI_API_KEY`.
- **System Instruction:** Embedded system prompt enforcing Tamil/Tanglish normalization, null price preservation, and Pydantic schema typing.
- **Deterministic Parameter:** `temperature: 0.0`.
- **Failover Policy:**
  ```
  gemini-3.5-flash-lite ──(on 503/fail)──> gemini-3.5-flash ──(on fail)──> gemini-3.7-flash ──> gemini-3.8-flash
  ```

### 5.2. WhatsApp Integration

#### Phase 1: MVP Client-Side Deep Linking (`wa.me`)
To preserve merchant control and avoid unsolicited messaging penalties:
- The backend generates a pre-formatted message text.
- The PWA constructs an intent deep link:
  ```
  https://wa.me/91{customerPhone}?text={encodeURIComponent(message)}
  ```
- The merchant reviews the text on their screen and taps "Open in WhatsApp", explicitly sending it via their native WhatsApp application.

#### Phase 2: Meta WhatsApp Cloud API & Webhooks
For automated customer payment confirmations and monthly statement links:
- **Webhook Endpoint:** `POST /api/webhooks/whatsapp`
- **Verification Endpoint:** `GET /api/webhooks/whatsapp`
  Validates `hub.mode === 'subscribe'` and checks `hub.verify_token === process.env.WA_WEBHOOK_VERIFY_TOKEN`.
- **HMAC Signature Verification:**
  Every incoming webhook payload is validated against the `X-Hub-Signature-256` header:
  $$\text{Hash} = \text{HMAC-SHA256}(\text{app\_secret}, \text{rawRequestBody})$$
  Requests failing signature comparison return `HTTP 403 Forbidden` immediately.

---

## 6. Rate Limiting & DoS Protection

Enforced via `express-rate-limit` middleware on Express API:

| Endpoint Group | Rate Limit Window | Max Requests | Key Policy |
| :--- | :--- | :--- | :--- |
| **Audio Drafting (`/api/draft/audio`)** | 1 Minute | 30 req / min | Tenant + IP address |
| **Text Drafting (`/api/draft/text`)** | 1 Minute | 60 req / min | Tenant + IP address |
| **Ledger Commits (`/api/ledger`)** | 1 Minute | 120 req / min | Tenant `shopId` |
| **Public Directory (`/api/customers`)** | 1 Minute | 300 req / min | Tenant + IP address |

### Cloud LLM Throttling Protection
- **Exponential Backoff:** If Gemini returns `HTTP 429 (ResourceExhausted)`, the failover cascade waits $200\text{ ms} \times 2^{\text{attempt}}$ with random jitter before attempting the secondary fallback model.

---

## 7. Required Environment Variables

### 7.1. Express Server (`credyazh/server/.env`)
```ini
# Server Network Configuration
PORT=4000
NODE_ENV=production
CORS_ORIGIN=https://credyazh.app

# Database Connection
MONGO_URI=mongodb+srv://<db_user>:<db_pass>@cluster0.mongodb.net/credyazh?retryWrites=true&w=majority

# Internal AI Microservice Route
AI_SERVICE_URL=http://127.0.0.1:8000

# Store Metadata & Tenant Boundary
SHOP_ID=demo-shop
SHOP_NAME=Demo Kirana Store

# Production Authentication Secret
JWT_SECRET=super_secret_signing_key_min_64_chars
```

### 7.2. FastAPI AI Service (`credyazh/ai-service/.env`)
```ini
# Internal Microservice Port
PORT=8000
HOST=127.0.0.1

# Google GenAI Authentication
GEMINI_API_KEY=AIzaSyD-YourOfficialGoogleGeminiKeyHere

# Configured Fallback Cascade
GEMINI_MODELS=gemini-3.5-flash-lite,gemini-3.5-flash,gemini-3.7-flash,gemini-3.8-flash
```

### 7.3. Client PWA (`credyazh/client/.env`)
```ini
# Vite API Target (Proxied in Development, Absolute in Production)
VITE_API_URL=/api
VITE_APP_TITLE=CredYazh
```

---

## 8. Data Privacy & Fault-Tolerant Failure Handling

| Failure Scenario | Technical Behavior | Recovery Path |
| :--- | :--- | :--- |
| **Microphone Background Noise** | Gemini returns `confidence: "low"` or unresolvable total. | Express Gate 1 flags warning: *"Audio unclear. Please verify total amount."* Draft displays editable fields. |
| **Complete Internet Loss** | PWA fetch catches `TypeError: Failed to fetch`. | UI displays non-blocking toast: *"Network offline. Counter service operating in manual mode."* |
| **Gemini API Outage (All 4 Models Fail)** | FastAPI returns `HTTP 502 Bad Gateway`. | Express informs client gracefully: *"AI draft currently unavailable. Please enter bill manually."* Manual ledger commits remain 100% operational. |
| **Duplicate Counter Tap / Network Stutter** | Client fires identical `POST /api/ledger` twice. | MongoDB compound unique index catches error `11000`. Express returns existing receipt with `{ duplicate: true }` and **zero balance mutation**. |
| **Audio In-Memory Cleanup** | Audio chunks processed by Multer. | Chunks live purely as Node Buffers; garbage-collected immediately after HTTP proxy completion. |
