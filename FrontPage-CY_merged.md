



CredYazh





From voice to ledger instantly.

Problem Statement & Solution Statement





Product rationale, user pain, proposed solution, impact hypotheses and validation plan Version 1.0 | 18 October 2026 | Product discovery / concept validation

Prepared for: founders, mentors, product managers, engineering leads and prospective pilot merchants.

POSITIONING

CredYazh is the voice-first ledger platform powered by Kalai AI, enabling businesses to manage accounts naturally in Tamil, Tanglish, and English.





###### Executive summary

India’s neighborhood merchants often operate with tight margins, repeated small transactions and informal customer credit. During busy hours, they may rely on memory, paper notebooks or time-consuming phone entry. When an item or repayment is not recorded accurately, a shop may struggle to collect what is owed, explain a balance, or reconcile the day’s sales. The problem is not that merchants cannot keep accounts; it is that existing bookkeeping workflows may interrupt the work that earns their income.

CredYazh proposes a voice-first, mobile-friendly digital ledger. A merchant speaks naturally; Kalai interprets the customer, items, quantities, amount and transaction intent; the system displays a reviewable entry and stores an auditable record only after required checks. The first market is kirana and grocery shops using an Android-first progressive web app (PWA), validated through a 5–20-shop pilot.





###### The human problem: effort is high, margin for error is small

A neighborhood merchant can spend long hours serving customers, weighing goods, managing cash and maintaining relationships. On some low-margin products, the gross profit per item may be only a few rupees. That makes unrecorded credit, payment confusion and disputed balances disproportionately painful. The shopkeeper may lose not only money, but also time, confidence and goodwill.

Illustrative scenario (not market-wide data): a merchant earns ₹3 gross profit on an item and forgets to record a ₹90 credit sale. Recovering that ₹90 is equivalent to the gross profit from 30 such items. This comparison illustrates exposure; it is not a calculation of net profit or an estimate of typical grocery margins.

A day in the shop

Morning: a regular customer takes milk and groceries on credit while other customers wait.

Afternoon: a family member purchases additional goods under the same household account.

Evening: the customer makes a partial payment; the owner is interrupted before updating the notebook.

Month end: merchant and customer remember different totals, and neither has a complete itemized history.



###### Formal problem statement (PS)

Small neighborhood merchants who extend informal credit need a fast, trustworthy way to record every sale, payment and adjustment while serving customers. Existing manual or typing-heavy processes can be interrupted by busy hands, language friction, repeated low-value transactions and unreliable connectivity. As a result, merchants may face missing entries, incorrect outstanding balances, avoidable disputes, delayed collections and administrative effort. The challenge is to capture transactions in the merchant’s natural language without sacrificing financial accuracy, transparency, privacy or control.

Short pitch-ready problem statement

Small merchants work hard to earn a few rupees on many everyday products, yet a forgotten credit entry or disputed payment can wipe out the benefit of multiple sales. Bookkeeping should protect their hard-earned income, not interrupt their business.





###### Who is affected?



###### Root causes and consequences



###### Why existing approaches may be insufficient

Paper notebooks are familiar, cheap and offline, but difficult to search, back up or share as itemized statements. Spreadsheet and conventional bookkeeping apps can provide stronger records, yet may demand typing, accounting vocabulary or too many taps during rush hours. Generic voice transcription can capture words but does not inherently validate financial intent, customer identity, totals or duplicate submissions. These are hypotheses to test with merchants; existing products vary and some may already address individual gaps.



###### Formal solution statement (SS)

CredYazh is a voice-first, multilingual ledger SaaS for neighborhood businesses. Powered by Kalai AI, it turns spoken Tamil, Tanglish and English into structured, reviewable business records. It captures itemized credit sales, payments and adjustments, resolves customer aliases, maintains chronological history, calculates balances deterministically and enables respectful statement sharing. Its goal is to reduce bookkeeping friction while making every financial entry traceable and correctable.

Short pitch-ready solution statement

CredYazh lets merchants keep serving customers while Kalai turns natural speech into accurate, itemized digital ledger entries—instantly ready for review, confirmation and later settlement.





###### Signature workflow: one bill, multiple items, one spoken total

Merchant says: “Kumar kanakkil arai kilo paruppu, oru litre paal — motham nootri arubathu roobai.” Meaning: Add half a kilogram of dal and one litre of milk to Kumar’s account, with a total bill of ₹160.

Non-negotiable rule: Kalai must not invent individual item prices or silently choose between customers with the same name. An explicitly spoken total can be recorded while per-item prices remain null. If the user also states line prices, the backend validates their sum against the total and flags any mismatch.





###### Proposed solution components

React Android-first PWA: large record control, Tamil/English UI, customer ledger, review and undo.

Node.js + Express: tenant authentication, customer matching, business rules, idempotent ledger writes, payments and statement links.

MongoDB: tenant-scoped customers, bills, line items, payments, reversals, aliases and audit history.

Python FastAPI + Gemini: audio understanding and structured command extraction; no unrestricted database writes.

Kalai assistant: contextual clarifications, balance queries, onboarding help and spoken confirmations.

WhatsApp sharing: merchant-reviewed messages and statements opened in native WhatsApp via deep link.





###### Differentiation and value proposition





###### Product scope and phased expansion

Release 1: Grocery / Kirana pilot

Target: 5–20 local shops. Essential flows: onboarding, customers and aliases, manual and voice entry, multi-item bills, partial payments, running balances, chronological statements, undo/reversal, tenant security and basic WhatsApp sharing. Offline manual queue and advanced reminder automation are phased based on testing.

Later domains

Bakeries and chemists use the standard ledger with category-specific controls. Dairies, newspapers and water suppliers add subscriptions, routes, exceptions and container returns. Hardware and building-material shops add project ledgers, delivery proofs and settlement allocation. These are planned expansions, not pilot commitments.





###### Why this matters: economic, operational and human impact

Economic: reduce avoidable leakage from missed credit entries and duplicate/incorrect charges.

Operational: shorten entry time and simplify end-of-day or month-end reconciliation.

Trust: give both merchant and customer a transparent itemized record.

Language inclusion: let merchants use the language and phrasing they already speak.

Dignity: make debt reminders factual, respectful and merchant-controlled rather than embarrassing.

Business continuity: retain usable records across device changes and provide export and backup paths. These benefits are intended outcomes, not established product results. They must be measured during the pilot.



###### Risks, constraints and safeguards



###### How to validate the problem before claiming product-market fit

Interview at least 5–8 grocery merchants, observe real checkout routines with consent, and run a 5–20-shop pilot. Seek disconfirming evidence: merchants who prefer paper, who already use effective apps, or whose losses arise mainly from customer nonpayment rather than recording errors.

Interview questions

How do you record a credit sale during the busiest 30 minutes of your day?

How often do you discover a missing, wrong or disputed entry? Can you recall a recent example?

How are partial payments and family purchases handled?

What languages and phrases do you naturally use while recording?

What would make you distrust an AI-generated ledger entry?

Would you use a press-to-talk PWA daily? What would stop you?

What is your current monthly cost in time, disputes or unrecovered amounts?



Pilot measurements and proposed targets

Do not claim a percentage reduction in losses until baseline and follow-up evidence exists. Any revenue, market-size or margin statistics used in a pitch should be independently sourced and dated.





###### Success criteria and decision gates

Problem validation: merchants independently describe missed or disputed credit as a meaningful pain, not merely a hypothetical one.

Usability validation: owners can complete core credit and repayment tasks without developer assistance.

AI validation: voice extraction meets agreed test thresholds on real Tamil/Tanglish recordings, with uncertain results safely escalated.

Reliability validation: balance reconciliation, reversals, tenant isolation and retry protection pass tests.

Commercial validation: merchants indicate willingness to keep using the product and to pay at a sustainable price.





###### Brand story and naming rationale

Cred stands for credit, trust and the everyday transactions that keep small businesses running. Yazh evokes Tamil heritage, expression and authenticity. Together, CredYazh connects traditional neighborhood trust with modern voice-powered bookkeeping. Kalai is the approachable AI assistant helping merchants work in their own language.

One-line pitch: “CredYazh is a voice-first ledger that turns conversations into business records.”



Alternative: “An AI ledger that understands Tamil, Tanglish, and English.”





###### Submission-ready PS and SS

Problem statement

Small neighborhood shop owners work long hours to earn modest margins on everyday products, yet credit sales are frequently recorded in notebooks, remembered until later, or entered manually while customers wait. A missed entry, incorrect amount or disputed repayment can consume the benefit of many small sales and weaken customer trust. Merchants need a faster, language-friendly way to keep reliable accounts without stopping the work that sustains their business.

Solution statement

CredYazh, powered by Kalai AI, is an Android-friendly voice-first ledger platform that converts natural Tamil, Tanglish and English speech into structured, itemized credit and payment records. It supports multiple products under one bill, customer aliases, partial payments, chronological history, safe corrections and clear statements. Merchant confirmation and backend financial validation protect accuracy, while a lightweight PWA keeps the workflow accessible to neighborhood shops.





###### Next actions

Confirm the problem statement with 5–8 real kirana merchants and document direct quotes with consent.

Gather 50–100 realistic voice command examples, including multi-item bills and ambiguous payments.

Define a baseline for recording time, missed entries, disputed balances and reconciliation effort.

Finalize pilot scope and acceptance criteria in the SRS; then create the System Architecture & Database Design.

Build a small Kalai audio-to-JSON proof of concept before connecting it to live financial writes.

Document status: Concept-stage PS–SS. Business impact and comparative claims are hypotheses pending field validation.



CredYazh





SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

From voice to ledger instantly.

Version 1.0 | 18 October 2026 | Status: Proposed for stakeholder review Prepared for: Product Owner, Engineering, UX, QA and Pilot Operations



###### Document control



###### Brand identity and positioning

Approved positioning statement: “CredYazh is the voice-first ledger platform powered by Kalai AI, enabling businesses to manage accounts naturally in Tamil, Tanglish, and English.”

One-line pitch: “CredYazh is a voice-first ledger that turns conversations into business records.” Alternative: “An AI ledger that understands Tamil, Tanglish, and English.”

Brand story

Small business owners should not have to stop working just to write accounts. Many think and speak in Tamil, Tanglish, or English, not accounting terms. CredYazh lets them manage business the way they naturally communicate: by speaking. Whether it is “Ravi-ku 500 kuduthen” or “Add ₹1000 credit for Kumar,” CredYazh listens, understands, and records automatically after appropriate validation.

Name rationale

“Cred” represents credit, trust, and the daily transactions that keep small businesses running. “Yazh” represents Tamil heritage, communication, and authenticity. Together, CredYazh expresses traditional trust meeting modern AI; as the Yazh enabled musical expression, CredYazh transforms bookkeeping through voice.

Kalai assistant role

Kalai is the branded AI assistant for onboarding, guided voice capture, clarification, explaining ledger balances, navigation, and drafting respectful reminders. Kalai must distinguish suggestions from completed financial operations, never fabricate amounts or identities, and never write directly to MongoDB. Merchant-visible confirmations must reflect committed backend results.



###### Product scope and release boundaries

Out of scope: money lending, payment processing, clinical diagnosis, autonomous debt collection, tax filing and direct WhatsApp sending without merchant authorization. The ledger is a recordkeeping tool, not a bank.



###### Stakeholders, personas and access



###### Core functional requirements

FR-001 | Tenant creation and isolation [P0]

Requirement: Every store receives immutable tenantId; all reads/writes and background jobs are tenant-scoped.

Acceptance: Tenant A cannot read, modify or infer Tenant B records via altered IDs, URLs, filters or exports.

FR-002 | Authentication and roles [P0]

Requirement: Secure merchant authentication; owner role; sessions and recovery. Staff roles extensible.

Acceptance: Unauthenticated requests are rejected; authorization checked per resource.

FR-003 | Store onboarding [P0]

Requirement: Capture store name, business type, preferred language, timezone Asia/Kolkata and currency INR.





Acceptance: Owner completes onboarding and can add first customer.

FR-004 | Customer directory [P0]

Requirement: Customer name, optional phone, aliases, notes, active status and unique customer ID per tenant.

Acceptance: Search by name/alias; duplicate name prompts selection, not auto-merge.

FR-005 | Voice capture [P0]

Requirement: Push-and-hold recording in PWA with recording indicator, retry and manual fallback. Acceptance: Permission denied and network failure show recoverable guidance; no silent capture.

FR-006 | Multilingual understanding [P0]

Requirement: Understand Tamil, English and code-mixed Tanglish with item names, quantities, totals and payment intent.

Acceptance: Representative test utterances produce validated structured drafts.

FR-007 | Multiple items, one total [P0]

Requirement: Parse multiple item names and quantities in one utterance with a single aggregate bill total; item prices optional.

Acceptance: Example Kumar utterance creates ONE bill, TWO item lines and total ₹160; no invented line prices.

FR-008 | Amounts and ambiguity [P0]

Requirement: Support spoken currency amounts, decimals, mixed language, and ambiguity clarification.

Acceptance: Low-confidence customer/amount/intent never posts automatically.

FR-009 | Chronological ledger [P0]

Requirement: Store immutable debit, payment, reversal and adjustment events with server timestamps and business date.

Acceptance: Multiple purchases append events; history never overwritten by current balance.

FR-010 | Payment recording [P0]

Requirement: Support full/partial customer payments, optional payment mode and notes.

Acceptance: ₹1500 owed minus ₹500 payment yields ₹1000 owed, without modifying prior purchases.

FR-011 | Balance calculation [P0]

Requirement: Customer balance derives from ledger events, with reconciled cached summaries permitted.

Acceptance: Balance remains consistent after payment, retry, reversal and export.

FR-012 | Confirmation and undo [P0]

Requirement: Show draft before posting when uncertain; after commit, announce result via TTS and offer 5-second Undo.





Acceptance: Undo produces compensating reversal; original event remains auditable.

FR-013 | Manual entry and editing [P0]

Requirement: Allow manual bill creation and correction through authorized reversal/replacement. Acceptance: Manual workflow works without microphone and maintains audit history.

FR-014 | Customer statements [P0]

Requirement: Generate date-filtered itemized statements, balances, payments and reversal labels. Acceptance: Statement reconciles to ledger, including bills with unpriced item lines.

FR-015 | WhatsApp handoff [P0]

Requirement: Generate encoded wa.me message with merchant-reviewed summary or secure statement link.

Acceptance: User taps Send in WhatsApp; platform does not claim automatic delivery.

FR-016 | Idempotency [P0]

Requirement: Client-generated idempotency key on every posting, with tenant-scoped uniqueness and safe retry.

Acceptance: Same key/request posted twice yields one financial event; changed payload with same key is rejected.

FR-017 | Kalai conversational help [P0]

Requirement: Explain actions, guide new merchants, ask clarifying questions, and read back committed transactions.

Acceptance: Kalai cannot claim success before backend commit and cannot execute unapproved ambiguous commands.

FR-018 | Search and dashboard [P0]

Requirement: Show outstanding balance, customer search, recent entries and collection summary. Acceptance: Amounts reconcile with transactions and filter to current tenant.

FR-019 | Offline draft queue [P1]

Requirement: Persist pending commands locally with retry, expiry and sync status; do not treat pending as posted.

Acceptance: Reconnect does not duplicate entries; failed items are visibly flagged.

FR-020 | Exports and audit [P1]

Requirement: CSV/PDF exports and actor/time/device audit events. Acceptance: Exports include selected date range and tenant only.

FR-021 | Debt reminders [P1]

Requirement: Identify overdue balances using configurable due dates and generate respectful bilingual draft messages.





Acceptance: Merchant reviews before opening WhatsApp; no shaming language or automatic harassment.

FR-022 | Subscriptions and SaaS billing [P1]

Requirement: Store plan, trial, limits and billing state without cross-tenant access.

Acceptance: Plan checks enforced server-side and do not hide/export-lock merchant-owned records.





###### Detailed voice-to-bill contract (critical)

Example: “குமார் கணக்கில் அரர கிலலா பருப்பு, ஒரு லிட்டர் பால்—மமாத்தம் நூற்றி அறுபF ரூபாய்.”

Interpretation: customer alias/name = Kumar; intent = ADD_CREDIT_BILL; line 1 = பருப்பு, quantity 0.5, unit kg; line 2 = பால், quantity 1, unit litre; total = INR 160.00; individual unit prices and line totals

= null (not inferred).

Suggested normalized payload:

{

"intent": "ADD_CREDIT_BILL",

"customerQuery": "Kumar", "items": [

{"name": "பருப்பு", "quantity": 0.5, "unit": "kg", "unitPrice": null, "lineTotal": null},

{"name": "பால்", "quantity": 1, "unit": "litre", "unitPrice": null, "lineTotal": null}

],

"billTotal": 160.00, "currency": "INR",

"priceAllocation": "UNSPECIFIED", "requiresConfirmation": false

}

Rules: (1) aggregate bill total is authoritative when explicitly spoken; (2) no fabricated line-item prices;

(3) if explicit line prices conflict with spoken total, ask whether discount, extra fee or correction applies; (4) if total is absent and item prices unavailable, request total rather than posting ₹0; (5) if customer alias is ambiguous, request identity selection; (6) itemized statement shows items and bill total, and labels unavailable per-item amounts.

Example test cases: “Kumar-ku milk 40 sugar 60” → two lines and total ₹100 when both line amounts are clear; “Kumar-ku milk and sugar total 100” → two lines with null prices and ₹100 total; “Ravi-ku 500 kuduthen” → ambiguous transfer direction, ask whether payment received, cash given or credit added.



###### Domain-specific requirements (future-compatible)







###### Domain workflow: exceptions-only delivery (R2)

Create route with ordered stops and effective-date subscriptions. Generate planned delivery batch. Worker records spoken exceptions (“Sequence 2 double pack, Sequence 3 skip”). Resolve stop number against active route and service date, preview exceptions, confirm actual completion, and post idempotent delivery events. Distinguish PLANNED, DELIVERED, SKIPPED and UNVERIFIED. Never automatically bill unverified stops merely because a route was started.



###### Non-functional requirements







###### Logical data model (developer handoff)

Use integer paise (minor currency units) for persisted money, not floating point. Use MongoDB sessions/transactions for atomic multi-document ledger posting when required. Enforce unique compound indexes on tenantId + idempotencyKey and relevant business keys. Avoid unbounded customer-embedded transaction arrays; store events in indexed collections.



###### API boundary and AI safety contract





Candidate routes: POST /v1/voice/parse; POST /v1/bills; GET /v1/customers; POST /v1/payments; POST /v1/ledger-events/{id}/reverse; GET /v1/customers/{id}/statement; GET /v1/dashboard; POST

/v1/kalai/chat. Exact schemas require API design review. Avoid storing raw audio indefinitely.





###### Quality assurance and acceptance scenarios



###### Pilot rollout and success metrics

Recruit 5–20 grocery shops; observe baseline notebook workflow, onboard merchants, run a 30-day pilot, collect feedback weekly and reconcile sample statements with merchant books. Proposed targets: 95% correct customer-and-amount extraction on representative recordings after clarification, zero duplicate postings in retry tests, onboarding under 10 minutes, typical clear command under 10 seconds. Track correction rate, time saved, weekly active shops and continued paper-book dependence.



###### Risks, assumptions and open decisions







###### Delivery handoff checklist

Product owner signs off R1/P0 scope and brand copy.

UX provides Tamil/English PWA flows, empty/error/loading states and Kalai clarification screens.

Backend team finalizes schema, indexes, tenant guards, monetary event rules and API contracts.

AI team delivers JSON schema, language test corpus, uncertainty flags and evaluation report.

QA maps AT-01 to AT-12 to automated/manual tests and adds tenant security regression tests.

DevOps sets up secrets, environments, logging, backups, monitoring and deployment.

Pilot lead recruits stores and documents consent, onboarding and support process.

Approval status: Draft / pending product owner, engineering lead and pilot merchant validation. This SRS is a developer handoff baseline, not evidence that all requirements have been validated.

Revision v1.1 • 18 October 2026 • Supersedes v1.0 for developer planning.

Requirements FR-001–FR-022 are retained; new requirements start at FR-023 to avoid identifier collisions.



###### Change control and requirements baseline (v1.1)

Document status: Proposed engineering baseline for review; not a signed-off production

specification. Product: CredYazh. AI assistant: Kalai. Tagline: “From voice to ledger instantly.” Initial target: Kirana/grocery merchants; Android-first progressive web app; pilot of 5–20 shops. Future domains remain in scope for architecture, not first-release implementation.

Priority legend: P0 = pilot launch blocker; P1 = commercial expansion; P2 = later optional enhancement. Release legend: R1 = grocery pilot, R1.1 = post-pilot, R2 = domain expansion. A requirement marked P0/R1 must have automated or manual acceptance evidence before launch.



###### Additional functional requirements — grocery pilot

FR-023 | Multi-item bill with explicit item prices [P0 / R1]

Requirement: Recognize two or more products, quantities, units, line prices and one bill total in a single utterance.

Business rules: Validate sum of line totals plus applicable adjustments equals stated total; do not silently overwrite a mismatch.

Acceptance: Given “Kumar milk ₹40, sugar ₹60, total ₹100”, create one bill with two item lines and

₹100 total. Given total ₹110, show mismatch and request confirmation/correction.

FR-024 | Credit, repayment, advance and refund intent separation [P0 / R1] Requirement: Distinguish a sale on credit, customer repayment, cash advanced by merchant, customer prepayment and merchant refund.

Business rules: Ambiguous “Ravi-ku ₹500 kuduthen” must not post automatically; show clarification.

Cash advances/loans are disabled by default pending product/legal scope decision.

Acceptance: “Ravi ₹500 thiruppi kuduthan” creates a repayment credit against receivable, not another sale; ambiguous statements remain drafts.

FR-025 | Customer and amount ambiguity resolution [P0 / R1]

Requirement: Resolve nicknames only against current tenant; confirm collisions and uncertain amounts.

Business rules: Never infer a unique customer from two equally plausible matches; AI confidence alone is insufficient to approve a financial posting.

Acceptance: If two Kumars match, show both identifiers and do not commit until merchant selects one.

FR-026 | Reversal, correction and five-second undo [P0 / R1]

Requirement: Permit merchant to reverse a just-posted bill and correct an erroneous customer, quantity or amount.

Business rules: Never delete a posted financial event; append a reversal and replacement where appropriate, link to original event, retain actor/time/reason. Undo expires visually after five seconds but correction remains available with authorization.

Acceptance: Undo once creates one linked reversal; retry does not create a second reversal; audit shows before/after.

FR-027 | Paper ledger opening balances [P0 / R1]

Requirement: Import each customer’s initial outstanding credit or advance with effective date and source.

Business rules: Opening balance is an auditable event, not an untraceable overwrite; merchant must confirm sign and amount.

Acceptance: Customer with ₹750 previous debt begins at ₹750 without fabricated purchase items.



FR-028 | Household and alternate purchaser identities [P1 / R1.1]

Requirement: Allow authorized household members to purchase against a shared account with attribution.

Business rules: Do not merge separate customer accounts automatically based on family name or address.

Acceptance: Wife and child can be tagged as purchasers on one household account, while statement names actual purchaser when captured.

FR-029 | Catalog, local aliases, units and historical pricing [P1 / R1.1]

Requirement: Support store-specific product catalog, Tamil/Tanglish aliases, weight/volume/each units and optional price suggestions.

Business rules: Prices derived from catalog must be labeled as calculated and confirmed if not spoken; price snapshots persist in posted bills.

Acceptance: 500 g resolves to 0.5 kg; changing price tomorrow does not alter yesterday’s bill.

FR-030 | Discounts, returns and mixed settlement [P1 / R1.1]

Requirement: Support bill-level discounts, item returns, cash+credit split and customer deposits.

Business rules: Refunds and returns reference source bill when possible; deposits are not treated as revenue or debt repayment without explicit application.

Acceptance: ₹250 bill with ₹100 paid produces ₹150 receivable; ₹20 discount on ₹180 yields ₹160 total.

FR-031 | Customer payment allocation and disputes [P1 / R1.1]

Requirement: Allow payments against general outstanding balance or selected bills; flag and resolve disputed lines.

Business rules: Document allocation policy (oldest-first default or manual); disputed items remain traceable and cannot be silently erased.

Acceptance: ₹500 payment against ₹1500 due results ₹1000 due; statement displays allocation and dispute status.

FR-032 | Daily collections reconciliation [P1 / R1.1]

Requirement: Show daily cash, UPI and other recorded receipts with discrepancies and close-of-day notes.

Business rules: Ledger records are not bank settlement proof; merchant confirms actual cash and payment receipt.

Acceptance: Daily report separates cash sales, credit sales, collections and refunds.

FR-033 | Reliable offline drafts and synchronization [P1 / R1.1]

Requirement: Permit offline manual draft capture and safe later synchronization; optionally queue raw audio locally with explicit consent.

Business rules: AI processing requires network unless on-device recognition is implemented; use client-generated idempotency keys and conflict handling.





Acceptance: Network retry posts each confirmed transaction at most once; unprocessed offline audio is visibly pending, not labeled saved.

FR-034 | Credit limits and overdue flags [P1 / R1.1]

Requirement: Configure optional per-customer credit limit, due date and warning. Business rules: Limits warn by default; blocking credit requires owner configuration.

Acceptance: Owner sees warning when new sale crosses limit; ledger remains accurate if authorized override occurs.

FR-035 | Multi-branch and staff policy [P1 / R1.1]

Requirement: Support staff roles and optionally multiple branches under one merchant organization.

Business rules: Branch-level vs organization-wide customer balance and permissions must be explicitly configured before enabling multi-branch.

Acceptance: Staff member cannot access unrelated tenant or unauthorized branch data.

FR-036 | Statement delivery and customer dispute intake [P1 / R1.1]

Requirement: Create itemized PDF/CSV statements and share via merchant-controlled WhatsApp link.

Business rules: Signed statement URLs expire; do not send messages automatically in R1; preserve sharing audit without claiming WhatsApp delivery confirmation.

Acceptance: Statement contains date, item lines, bills, payments, adjustments, opening and closing balance.



###### Kalai AI functional and safety requirements

AI-001 | Conversation-aware clarification [P0 / R1]

Requirement: Kalai asks which customer, amount, unit or intent is intended when unresolved; never auto-posts ambiguous commands.

Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.

AI-002 | Multilingual contextual commands [P0 / R1]

Requirement: Kalai handles Tamil script, spoken Tamil, English and Tanglish code-switching with store-local product aliases.

Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.



AI-003 | Voice corrections and queries [P1 / R1.1]

Requirement: Kalai can interpret “not 150, 115”, “Kumar balance evlo?” and history queries, but backend verifies authorization and applies changes.

Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.

AI-004 | Merchant onboarding assistant [P1 / R1.1]

Requirement: Kalai guides adding customers, aliases, opening balances and recording first bill without making unauthorized financial changes.

Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.

AI-005 | Noise and uncertainty handling [P0 / R1]

Requirement: Kalai signals low-confidence or incomplete recordings and requests repeat or manual review; no invented values.

Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.

AI-006 | Typed command schema [P0 / R1]

Requirement: AI service returns validated JSON with intent, raw transcript, extracted entities, missing fields, uncertainties, provenance and request ID.

Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.

AI-007 | Tenant-scoped context [P0 / R1]

Requirement: AI receives only minimal authorized customer candidates; tenant filtering occurs before and after inference.

Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.

AI-008 | Read-only queries and controlled mutations [P0 / R1]

Requirement: Balance/history answers are computed by backend; AI output never directly writes MongoDB.





Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.

AI-009 | Voice confirmation [P0 / R1]

Requirement: On successful commit, Kalai may speak customer and amount; spoken response must reflect committed server result.

Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.

AI-010 | Model evaluation and fallback [P1 / R1.1]

Requirement: Version prompts/models; benchmark with consented local audio and fall back to manual entry on AI failure.

Business rules: Model output is untrusted and must pass deterministic authorization, schema, amount and idempotency checks.

Acceptance: Test representative positive, negative and ambiguous utterances; no unsafe financial writes.



###### Voice bill contract — required examples

Scenario A (explicit aggregate total, no line prices): “குமார் கணக்கில் அரர கிலலா பருப்பு, ஒரு லிட்டர் பால்—மமாத்தம் நூற்றி அறுபF ரூபாய்.” Customer spoken alias Kumar; items: dal 0.5 kg and milk 1 litre; stated bill total INR 160. Each line price = null, price_source = unspecified. Bill total =

160. The merchant reviews and confirms one bill, not two separate charges. Missing per-line prices are never invented or evenly split.

Scenario B (line prices): “Kumar milk forty rupees, sugar sixty rupees, total hundred.” Extract ₹40 and

₹60; verify arithmetic total ₹100 before posting.

Scenario C (mixed settlement): “Ravi bill 250, cash 100, balance account-la podu.” One ₹250 sale and linked ₹100 payment; outstanding increase ₹150. Confirm payment method.

Scenario D (quantity missing): “Suresh-ku thirty rupees sugar.” Store item and ₹30 value; quantity null unless spoken or explicitly confirmed from merchant-approved catalog.

Scenario E (ambiguous intent): “Ravi-ku 500 kuduthen.” No automatic debit/credit. Ask whether cash loan, refund or other transfer; disable unsupported actions.

Proposed API command example (not final schema):



{

"intent": "ADD_CREDIT_BILL",

"customer_spoken_name": "Kumar", "items": [

{"name": "dal", "quantity": 0.5, "unit": "kg", "line_total": null},

{"name": "milk", "quantity": 1, "unit": "litre", "line_total": null}





],

"bill_total": 160, "currency": "INR",

"price_source": "spoken_bill_total_only", "requires_confirmation": true

}



Data integrity: persist bill header, child item lines, currency in integer paise, server-generated transaction ID, tenant ID, customer ID, timestamps, status, actor ID, source utterance reference, and idempotency key. A single bill total must affect receivables exactly once; item lines are descriptive when line amounts are null.



###### Additional domain requirements — future releases

Kirana and grocery (R1)

Household tabs, weights and loose quantities, colloquial aliases, repeat purchases, returns, partial settlement, opening balances.

Chemist / pharmacy (R2)

Medicine names and quantities, repeat prescriptions, restricted access to health-related details, batch/expiry references only where needed; no clinical advice.

Bakery (R2)

Small rapid purchases, weekly family tabs, advance cake orders, cancellations and deposits.

Milk distribution (R2)

Route sequence, recurring packs, skip/extra exceptions, holiday pause, verified route completion and daily batch idempotency.

Newspaper distribution (R2)

Publication-specific subscriptions, weekday/weekend pricing, route reassignment, pauses and monthly billing.

Water can suppliers (R2)

Full/empty can inventory, deposits, damages, customer container liability and separate financial balances.

Hardware/electrical (R2)

Contractor/project association, negotiated rates, partial returns, project statements and staged settlements.

Building materials (R2)

Site, truck, challan, receiver acknowledgment, freight and staged delivery/settlement records.

Route-specific safety: “default delivery” represents a planned batch, not proof of actual delivery. Finalize only after route completion/exception confirmation; skipped and unknown houses remain distinguishable. One route-day batch ID prevents duplicate posting.



###### Security, privacy and SaaS operational requirements

SEC-001 | Tenant isolation [P0 / R1]

Requirement: All queries and mutations require authenticated tenant context; compound tenant indexes and adversarial cross-tenant tests.

Business rules: Implementation must have documented owner and test coverage. Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.

SEC-002 | Authorization [P0 / R1]

Requirement: Owner/cashier/worker/accountant roles; least privilege; session revocation. Business rules: Implementation must have documented owner and test coverage.

Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.

SEC-003 | Data protection [P0 / R1]

Requirement: TLS, encryption at rest, secrets management, signed expiring statements, audio retention limits.

Business rules: Implementation must have documented owner and test coverage. Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.

SEC-004 | Privacy and consent [P0 / R1]

Requirement: Clear notice for contacts/audio, opt-in contact import, retention/deletion/export processes; legal review of Indian DPDP requirements.

Business rules: Implementation must have documented owner and test coverage. Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.

SEC-005 | Auditability [P0 / R1]

Requirement: Record who posted, corrected, reversed, exported and shared; redact sensitive data in logs.

Business rules: Implementation must have documented owner and test coverage. Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.

OPS-001 | Reliability [P0 / R1]

Requirement: Idempotent posting, transaction atomicity, backup/restore tests, error alerts and monitoring.

Business rules: Implementation must have documented owner and test coverage. Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.

OPS-002 | Pilot observability [P0 / R1]

Requirement: Track speech parsing success, clarification frequency, corrections, latency, duplicate attempts and cost per transaction.

Business rules: Implementation must have documented owner and test coverage.





Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.

OPS-003 | SaaS plans [P1 / R1.1]

Requirement: Trials, merchant billing, usage quotas, plan changes and suspension rules. Business rules: Implementation must have documented owner and test coverage.

Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.

OPS-004 | Support [P1 / R1.1]

Requirement: Merchant help, issue tickets, consented diagnostic access, account recovery and escalation.

Business rules: Implementation must have documented owner and test coverage. Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.

OPS-005 | Deployment [P0 / R1]

Requirement: Separate dev/staging/prod, environment-scoped secrets, CI checks and rollback procedure.

Business rules: Implementation must have documented owner and test coverage. Acceptance: QA verifies authorized success and unauthorized denial/failure recovery.



###### Non-functional targets and pilot acceptance matrix



###### Developer handoff, decisions and recommended sequence

Required deliverables before implementation: signed-off user journeys; low-fidelity mobile screens; API/OpenAPI contracts; tenant-scoped ERD; state machine for draft/confirmed/reversed transactions;





permission matrix; financial sign conventions; Kalai JSON schema; labeled evaluation dataset; acceptance test cases; pilot privacy notice and retention policy.

Recommended build sequence: (1) observe 5–8 kirana merchants and validate utterances/edge cases;

(2) confirm R1 scope and unresolved policy decisions; (3) design ledger invariants and tenant-scoped MongoDB models; (4) implement auth/customers/manual bills/payments/reversals; (5) implement Gemini audio parser with structured schema and offline-safe confirmation; (6) build Android PWA; (7) security and failure testing; (8) staged rollout to 2 shops then 5–20 shops with measurement.

Open decisions requiring product owner approval: family accounts; cash advance/loan support; auto-price suggestions; statement retention; staff roles; opening balance verification; partial payment allocation; offline audio retention; branch structure; GST invoice scope; pricing/subscription strategy; consent and contact import behavior.

Out of R1 scope: real money transfer or lending, fully automatic WhatsApp sending, always-on microphone, autonomous financial posting without merchant review, pharmacy clinical features, delivery route batch billing and contractor project billing.



## CredYazh





System Architecture & Database Design (SA&DD)

Version 1.0 | Architecture baseline | 18 October 2026

Product definition: CredYazh is a multilingual voice-ledger Progressive Web App for small merchants. Kalai is an optional in-app AI assistant within CredYazh; the platform is not described as “powered by Kalai AI” and makes no “first voice-ledger” claim.









###### Executive architecture decision

Use a modular monolith for the ledger backend, not microservices for every feature. Deploy React PWA, Node/Express business API, MongoDB Atlas, and one separately deployable Python/FastAPI AI adapter. All financial writes pass through Express; neither Gemini nor Kalai writes directly to MongoDB.









###### Scope and boundaries

MVP R1 in scope

Single merchant organization with one store; owner and optional employee roles.

Customers, aliases, opening balances, item catalog (optional), sales on credit, collections, returns/reversals, balances and statements.

Manual entry always available; voice entry via explicit review-and-confirm step.



Tamil, Tanglish and English voice commands; explicit unsupported/ambiguous response handling.

Audit history, idempotency, tenant isolation, export, simple WhatsApp share links.

Android Chrome installable PWA; offline manual drafts, clearly labeled as pending sync.



Deferred from R1

Automatic route delivery, subscriptions and container deposits (later mode).

Contractor projects, challans and multi-branch consolidated accounts (later mode).

Autonomous AI posting, voice-only financial confirmation, payment processing or lending.

Advanced GST invoicing, full inventory, automated WhatsApp Business messaging, continuous live assistant.



Non-goals

CredYazh does not hold customer funds, extend regulated loans, or guarantee accounting/tax compliance. It records merchant-provided business transactions and should be reviewed against applicable law before commercialization.





###### Logical system context

Merchant Android PWA

| HTTPS + authenticated session v

Express Business API ---> MongoDB Atlas (tenant-scoped collections)

|	|

|	+--> statement generator / export / audit / observability

|

+-- short-lived signed audio request --> FastAPI AI Adapter --> Gemini

<----- structured proposed command + warnings -----

|

+--> validate / resolve customer / preview --> merchant confirms

+--> atomic ledger posting + idempotency --> response + balance

Trust boundary: AI output is untrusted proposal data. Tenant identity is derived from the authenticated server session, never accepted from model output or a client-supplied tenantId.





###### Core modules and ownership



###### Tenancy, authorization and identity

Every business-owned document carries tenantId (ObjectId) and createdAt; storeId is reserved for future multi-branch use.

Authenticate each request; server resolves active tenant from user membership and selected organization.

Repository layer requires TenantContext for all reads and writes; no unrestricted model.find() in application routes.

Compound indexes begin with tenantId; unique constraints are scoped by tenant.

Role baseline: OWNER manages staff, exports and reversals; STAFF may create drafts and post within configurable limits; VIEWER reads authorized records only.

Separate support/operator access; support must not automatically read private ledger content.

Test cross-tenant IDOR and forged tenantId on every resource endpoint.





###### Data model — proposed collections



Financial data types

Store INR in integer paise (amountMinor), never floating-point rupees. Quantities may use decimal128 or fixed decimal strings with explicit unit.

Every bill line includes item name snapshot, quantity, unit, unitPriceMinor nullable, lineAmountMinor nullable and provenance (spoken/catalog/manual).

Bill total may be known while individual line prices are null; the system must not allocate the total arbitrarily.

Preserve historical item descriptions and prices even when the product catalog changes.

Amounts and currency are server-validated; negative amounts are represented through typed ledger events, not free-form signed inputs.

Financial event taxonomy







Invariant: customer outstanding = sum of authorized ledger event effects in paise. A cached balance is a projection and must be reconstructable from events. Payments exceeding outstanding create credit/advance only when explicitly allowed by merchant rules.





###### Posting workflow and consistency

POST /command-drafts (manual or AI proposal)

Resolve customer; reject ambiguity; calculate deterministic totals

Display customer, items, total, payment split, effect on balance

Merchant taps Confirm -> POST /bills with Idempotency-Key

Server verifies tenant/role, draft freshness, payload hash

MongoDB transaction: bill + ledger event(s) + audit + key result

Return committed receipt; update projections asynchronously or in transaction

On retry, return same result; on conflicting key payload, return 409

MongoDB multi-document transactions require a suitable replica-set deployment. Keep transaction scope short. If any step fails, the client sees “not confirmed” until status is fetched; never infer posting from a timeout.

Example — one total, two items

Input: “Kumar account-la ara kilo paruppu, oru litre paal, total 160.” Draft: intent=ADD_CREDIT; customer=Kumar; lines=[Dal 0.5 kg,

Milk 1 litre]; each unitPriceMinor=null; totalMinor=16000 Preview: Kumar | 2 items | Total Rs 160 | Add to credit Rs 160 After confirmation: 1 bill + 1 CREDIT_SALE event (+16000 paise)

If there are two customers named Kumar, stop at disambiguation. If the user says “Kumar paid 100”, create a CUSTOMER_PAYMENT proposal, not a sale.





###### AI and voice pipeline

PWA records audio only after clear user action and microphone permission; show recording status and allow cancel.

Upload over HTTPS with strict size, duration, MIME validation; delete raw audio according to approved retention policy.

FastAPI sends audio to the chosen model with a versioned schema, language hints and instructions to abstain rather than guess.

Validate AI JSON against a strict schema. Unsupported intent, uncertain amount, conflicting total, unknown units or low-confidence identity becomes clarification.

Do not trust a model-generated confidence number as calibrated probability; benchmark per-field extraction on real recordings.

The merchant sees an editable transaction preview before posting. Kalai can explain and navigate, but its tools operate through the same authorization-controlled APIs.

Store prompt/model/schema version and anonymized evaluation metrics; avoid storing sensitive transcripts by default.



Versioned proposed command schema

{

"schemaVersion": "1.0", "intent": "ADD_CREDIT",





"customerSpokenName": "Kumar", "items": [

{"name":"Dal","quantity":"0.5","unit":"kg","unitPriceMinor":null},

{"name":"Milk","quantity":"1","unit":"litre","unitPriceMinor":null}

],

"totalMinor":16000, "currency":"INR", "warnings":[], "needsClarification":false

}

Kalai assistant separation

Kalai is an in-app assistant, not a separate ledger owner or the product engine. Its supported tools (find customer, explain balance, prepare draft, open statement) use backend policy checks. AI can propose but never finalize financial postings autonomously in R1.





###### REST API contract — initial outline

Standard response envelope: {data, error:{code,message,details}, requestId}. Define pagination, error codes, API versioning, request-size limits and OpenAPI contracts before implementation. 401 = unauthenticated, 403 = unauthorized, 404 for inaccessible resources, 409 for idempotency conflict.





###### Offline and sync strategy

Use service worker for application shell and IndexedDB for pending manual drafts; do not store long-lived access tokens or sensitive audio in plaintext browser storage.

A queued record must display PENDING, SYNCING, CONFIRMED or NEEDS_REVIEW. Never show pending as posted credit.

Generate stable clientRequestId/idempotency key at draft creation; retries reuse it.

Sync on connectivity restoration and explicit user action; reconcile via server receipt and transaction lookup.

Voice AI processing is online-only for R1; show manual entry fallback when offline.

Conflicts: customer deleted/merged, catalog changed, stale draft or authorization revoked -> stop and request review.

Define offline retention and device loss policy; evaluate encryption and shared-device threats during pilot.





###### Security, privacy and reliability







Pilot service targets (proposed, not guarantees)

Availability objective: 99.5% monthly for pilot, subject to provider constraints.

Typical short voice command: aim for <=5 s p95 on specified networks; measure before committing.

No duplicated committed financial events under retry/failure tests.

Daily backup and periodic restore drills; choose explicit RPO/RTO before production launch.

Collect AI field-level precision and abstention metrics on consented noisy Tamil/Tanglish/English audio.





###### Deployment topology and environments

Production: CDN/static PWA -> HTTPS API -> Express app -> Atlas

|

+-> private FastAPI adapter -> Gemini

+-> managed object storage (exports/audio if approved) Staging: separate app, credentials, DB, model keys and test customers

Development: local mock AI, seeded data and test tenant fixtures

Use separate dev/staging/prod secrets, domains, databases and service accounts.

Set request IDs and correlation IDs across PWA, Express and FastAPI.

Protect AI service from public direct posting; network restrictions and service authentication.

Centralize metrics for latency, AI cost, error rates, queued sync, balance drift and failed transactions.

Use migration scripts and feature flags for future domain modes.





###### Extensibility for eight merchant domains

Implement domain-specific modules behind explicit capabilities rather than adding dozens of nullable fields to core ledger events. Planned route delivery is never considered delivered until confirmed. Chemist data requires extra sensitive-data controls.



###### Architecture decision records (ADRs)



###### Test and acceptance matrix



###### Phased implementation plan







###### Open questions requiring product sign-off

Can one customer account represent a household? Who can make purchases on it?

Are customer advances and negative balances allowed by default?

How should an unallocated payment be applied to bills?

Can staff reverse transactions or only owners? What threshold requires owner approval?

What customer identity fields are mandatory? Is phone number optional?

What is the policy for store branches, customer merging and deleted customers?

What data may be sent to the AI provider and for how long may audio/transcripts be retained?

What are the exact offline storage and shared-device requirements?

Are price catalogs optional or mandatory in the pilot?

What constitutes an accepted voice command accuracy target by language?





###### Developer handoff checklist

Approve ADRs and outstanding business rules; freeze R1 scope.

Write OpenAPI 3.1 specification and request/response JSON schemas.

Produce MongoDB collection schemas, indexes and tenant-safe repository interfaces.

Implement balance invariants, ledger event state machine and idempotency contract.

Prepare test fixtures: multiple tenants, duplicate names, ambiguous commands, refunds and partial payments.

Build clickable PWA wireframes and user-confirmation states.

Benchmark Gemini with consented merchant recordings before model/vendor commitment.

Create threat model, data retention plan, backup/restore runbook and pilot observability dashboard.

Document note: This is a proposed engineering baseline rather than an assertion of deployed functionality. Performance targets, compliance decisions and architecture assumptions require validation. Brand language intentionally avoids

“powered by Kalai AI” and “first voice-ledger.”



# Risk Register & Mitigation Plan



CredYazh | Voice-ledger SaaS for small merchants

Kalai is an AI assistant within the CredYazh PWA—not the product’s powering brand. This document never claims CredYazh is the first voice-ledger.

Version 1.0 • 19 October 2026 • Status: Proposed controls for team review





###### Executive decision

No risk has a universally perfect solution. The best practical solution is a layered control: prevent the failure where possible, detect it quickly, recover without silently altering financial history, and prove effectiveness with tests. The residual risk must be accepted by an accountable owner before pilot launch.



###### Product context and scope

Pilot: Android-first React PWA for kirana/grocery merchants, with Node.js/Express, MongoDB/Mongoose and optional Python FastAPI + Gemini voice interpretation. Manual ledger operation is the system of record; AI proposes drafts, never writes financial records directly. Pilot target: 5–20 shops, subject to merchant validation.

Financial design rule: one confirmed bill may contain multiple items with only a spoken aggregate total. Missing line prices remain unknown, not invented. Payments, reversals and opening balances are separately typed and audited.



###### Risk scoring and ownership

Priority labels are qualitative planning assessments, not measured incident probabilities. Critical: potential financial integrity, authorization or recovery failure; High: serious adoption, availability, cost or privacy impact; Medium: bounded workflow or usability impact. Residual risk ratings below are forecasts to validate during tests.





###### Risk register at a glance











###### Detailed prevention, detection, recovery and acceptance criteria

R01 — AI amount misinterpretation

Severity: Critical | Domain: Voice/AI | Proposed owner: AI lead | Phase: P0 | Residual risk: High Failure scenario: ₹150 is understood as ₹1,500.

Best-practical prevention: Strict typed JSON; plausibility rules; merchant preview; second confirmation for abnormal amounts.

Detection and monitoring: Track corrected amounts, outlier alerts, sampled audio-to-draft reviews with consent.

Recovery and response: Do not commit uncertain drafts; merchant edits or re-records; reverse wrong posted event with reason.

Acceptance test / evidence: 100–200 multilingual samples; test 150/1500, decimals, lakh, noisy audio; zero unconfirmed postings.

R02 — Wrong customer match

Severity: Critical | Domain: Identity | Proposed owner: Backend lead | Phase: P0 | Residual risk: Medium Failure scenario: Two customers share the name Kumar.

Best-practical prevention: Tenant-scoped matching; aliases; distinguish by phone/area; never auto-select ambiguous names.

Detection and monitoring: Multiple-candidate flags; unmatched-name metrics; merchant feedback.

Recovery and response: Block save until selected; reverse misapplied charge and reissue to correct customer. Acceptance test / evidence: Same-name fixture; verify selection required and cross-tenant match impossible.

R03 — Duplicate transactions

Severity: Critical | Domain: Ledger | Proposed owner: Backend lead | Phase: P0 | Residual risk: Low Failure scenario: Double-tap or retry posts the same bill twice.

Best-practical prevention: Server idempotency key per intent; unique compound index; atomic write; disable repeat UI.

Detection and monitoring: Duplicate-key metrics and repeated-payload anomaly alerts.

Recovery and response: Return original receipt for retry; reversal workflow for distinct accidental duplicates. Acceptance test / evidence: Simulate 50 parallel retries, timeouts, app reload; exactly one committed bill.

R04 — Debit/credit intent confusion

Severity: Critical | Domain: Ledger/AI | Proposed owner: Product + AI | Phase: P0 | Residual risk: Medium Failure scenario: “Ravi gave ₹500” has unclear financial direction.

Best-practical prevention: Typed transaction intents; explicit clarification for ambiguous speech; confirmation shows effect on balance.



Detection and monitoring: Intent corrections and unusual balance-direction monitoring. Recovery and response: Cancel draft or post compensating adjustment with audit trail.

Acceptance test / evidence: Test gave/received/advance/refund in Tamil, Tanglish, English; no uncertain auto-posts.

R05 — Lost records or wrong balances

Severity: Critical | Domain: Data integrity | Proposed owner: Backend lead | Phase: P0 | Residual risk: Medium

Failure scenario: Partial write creates a bill without corresponding ledger event.

Best-practical prevention: Append-only journal; MongoDB atomic transactions for related writes; decimal-safe integer paise; reconciliation.

Detection and monitoring: Daily journal-to-balance checks, invariant alerts, backup verification.

Recovery and response: Stop affected writes, restore from tested backup/PITR where supported, replay valid events and reconcile.

Acceptance test / evidence: Crash between writes; restore drill; recomputed balances equal expected values.

R06 — Cross-tenant data exposure

Severity: Critical | Domain: Security | Proposed owner: Security/backend | Phase: P0 | Residual risk: Medium Failure scenario: Store A sees Store B customer balances.

Best-practical prevention: Server-derived tenant context; scoped repository methods; RBAC; compound tenant indexes; deny-by-default.

Detection and monitoring: Authorization-denied logs; automated tenant isolation suite; security monitoring. Recovery and response: Revoke access, contain incident, investigate logs, notify as required, rotate credentials. Acceptance test / evidence: All CRUD/query/export routes tested with two tenants; zero cross-tenant results.

R07 — Internet and offline failures

Severity: Critical | Domain: Availability | Proposed owner: Frontend lead | Phase: P0/P1 | Residual risk: Medium

Failure scenario: Merchant loses network while saving.

Best-practical prevention: Manual offline queue with local IDs, explicit pending state, idempotent sync; AI requires internet in MVP.

Detection and monitoring: Queue-age, failed-sync, and conflict metrics; persistent pending indicator.

Recovery and response: Retry safely, surface conflicts, permit merchant correction; never mark pending as confirmed.

Acceptance test / evidence: Airplane mode, reconnect, double sync, stale token, device restart; no duplicates.

R08 — Disputes and unauthorized changes

Severity: Critical | Domain: Governance | Proposed owner: Product/backend | Phase: P0 | Residual risk: Medium

Failure scenario: Employee removes a legitimate debt after a dispute.

Best-practical prevention: Append-only reversal/adjustment, actor/time/reason; permissions; owner approval for sensitive changes.

Detection and monitoring: Audit reports; large reversal alerts; dispute status tracking.



Recovery and response: Freeze disputed item where appropriate; investigate evidence; authorized adjustment with history.

Acceptance test / evidence: Employee cannot silently edit history; full trace of every correction.

R09 — Noisy shop audio

Severity: High | Domain: Voice UX | Proposed owner: AI lead | Phase: P0 | Residual risk: Medium Failure scenario: Fan/traffic causes incorrect extraction.

Best-practical prevention: Noise-tolerant capture, push-to-talk, confidence gating, quick rerecord and manual fallback.

Detection and monitoring: Error rate by noise category and rerecord frequency. Recovery and response: Prompt rerecord or manual entry; no auto-save.

Acceptance test / evidence: Record in shop-like noise; compare field-level error rates.

R10 — Dialect and code-switch errors

Severity: High | Domain: Voice UX | Proposed owner: AI lead | Phase: P0 | Residual risk: Medium Failure scenario: Tamil dialect or Tanglish changes meaning.

Best-practical prevention: Diverse consented evaluation set, vocabulary aliases, field-level evaluation, clarifying questions.

Detection and monitoring: Track errors by language and expression, not only overall accuracy. Recovery and response: Offer text edit/manual entry; expand regression corpus.

Acceptance test / evidence: Test dialects, mixed scripts, colloquial money expressions.

R11 — Voice latency

Severity: High | Domain: Performance | Proposed owner: AI/backend | Phase: P1 | Residual risk: Medium Failure scenario: Slow response interrupts busy checkout.

Best-practical prevention: Bound audio length; async progress; model benchmarking; timeout/fallback; avoid needless model calls.

Detection and monitoring: P50/P95 end-to-end latency, timeout rate. Recovery and response: Offer manual entry, safe retry without duplicate.

Acceptance test / evidence: Load-test on budget Android and mobile network; verify defined P95 target.

R12 — AI operating cost

Severity: High | Domain: Economics | Proposed owner: Founder/ops | Phase: P0 | Residual risk: Medium Failure scenario: API expense exceeds subscription income.

Best-practical prevention: Meter tokens/audio and retries; quotas, rate limits, pricing experiments, budget alerts. Detection and monitoring: Cost per confirmed transaction and per tenant; margin dashboard.

Recovery and response: Disable optional AI on budget breach; retain manual ledger; revise quotas/pricing. Acceptance test / evidence: Simulate 10/100/500 shops and failed calls; enforce spend ceiling.

R13 — Low merchant adoption

Severity: High | Domain: Product market | Proposed owner: Founder/product | Phase: P0 | Residual risk: High Failure scenario: Merchants stick to notebooks.



Best-practical prevention: Merchant interviews, 3-minute onboarding, import opening balances, manual + voice modes, assisted pilot.

Detection and monitoring: Weekly active shops, retained users, completed transactions, interviews. Recovery and response: Simplify workflows, reduce steps, change target segment if evidence demands. Acceptance test / evidence: 5–8 interviews, 5–20 shop pilot; observe task completion and repeat usage.

R14 — Low-end Android performance

Severity: High | Domain: Frontend | Proposed owner: Frontend lead | Phase: P0 | Residual risk: Medium Failure scenario: PWA freezes on entry-level phones.

Best-practical prevention: Small bundles, lazy loading, efficient lists, low-memory testing, accessibility. Detection and monitoring: Crash logs, interaction timing, device-class metrics.

Recovery and response: Graceful reload and persisted drafts; fallback UI. Acceptance test / evidence: Test low-RAM Android, slow 4G, storage pressure.

R15 — Privacy and personal data misuse

Severity: High | Domain: Privacy | Proposed owner: Security/product | Phase: P0 | Residual risk: Medium Failure scenario: Customer phone and ledger details leak.

Best-practical prevention: Minimize collection; role permissions; encryption; retention policy; privacy notices; vendor review.

Detection and monitoring: Access audit, security scans, abnormal export alerts.

Recovery and response: Contain breach, rotate secrets, assess notification duties and remediate. Acceptance test / evidence: Verify restricted exports, deleted audio per policy, no secrets in logs.

R16 — Competitive differentiation

Severity: High | Domain: Strategy | Proposed owner: Founder | Phase: P1 | Residual risk: High Failure scenario: Existing ledger products already satisfy needs.

Best-practical prevention: Benchmark alternatives; focus on validated Tamil/Tanglish workflow and reliability; measure time saved.

Detection and monitoring: Merchant preference tests, conversion and churn reasons. Recovery and response: Reposition niche, simplify pricing or product scope.

Acceptance test / evidence: Blind usability comparison on representative merchant tasks.

R17 — Incorrect product aliases

Severity: Medium | Domain: Catalog | Proposed owner: Product/backend | Phase: P1 | Residual risk: Medium Failure scenario: Paruppu resolves to wrong dal variant.

Best-practical prevention: Tenant-specific aliases; disambiguation for conflicting catalog matches; editable preview.

Detection and monitoring: Correction and alias-collision logs.

Recovery and response: Correct item through auditable adjustment and update alias mapping. Acceptance test / evidence: Same alias mapped to multiple SKUs; require choice.



R18 — Unit and quantity confusion

Severity: Medium | Domain: Catalog/AI | Proposed owner: AI/backend | Phase: P0 | Residual risk: Low Failure scenario: 500 g becomes 500 kg.

Best-practical prevention: Canonical units, range checks, explicit spoken-vs-inferred fields, confirmation. Detection and monitoring: Outlier quantities and unit correction rate.

Recovery and response: Block implausible draft; merchant corrects.

Acceptance test / evidence: Test grams/kg, ml/litre, loose quantities, ₹-worth items.

R19 — Shared device/session misuse

Severity: Medium | Domain: Security | Proposed owner: Security/frontend | Phase: P1 | Residual risk: Medium

Failure scenario: Employee uses owner’s unlocked session.

Best-practical prevention: Per-user roles, short idle timeout, optional device PIN, owner reauth for sensitive operations.

Detection and monitoring: Login/session history, anomalous changes. Recovery and response: Revoke sessions and credentials, audit changes. Acceptance test / evidence: Role tests and stolen-device scenario.

R20 — Opening balance migration errors

Severity: Medium | Domain: Onboarding | Proposed owner: Product/backend | Phase: P0 | Residual risk: Medium

Failure scenario: Notebook balance copied incorrectly.

Best-practical prevention: Separate opening-balance event; source date; merchant confirmation; optional evidence photo with consent.

Detection and monitoring: Reconciliation report and early disputes. Recovery and response: Audited correction entry, never silent overwrite.

Acceptance test / evidence: Migration sample with disputed and negative balances.

R21 — Feature overload

Severity: Medium | Domain: UX/scope | Proposed owner: Product lead | Phase: P0 | Residual risk: Low Failure scenario: Grocery owner sees delivery and contractor features.

Best-practical prevention: Kirana-only pilot UI; modular feature flags; progressive disclosure. Detection and monitoring: Drop-off and task-time analytics.

Recovery and response: Hide low-value modules, redesign navigation.

Acceptance test / evidence: First-time merchant completes common tasks without guidance.

R22 — WhatsApp reminder misunderstandings

Severity: Medium | Domain: Messaging | Proposed owner: Frontend/product | Phase: P1 | Residual risk: Low Failure scenario: Merchant thinks message was sent automatically.

Best-practical prevention: Explicit share-to-WhatsApp deep link; show “prepared” vs “sent” accurately; no delivery claims.



Detection and monitoring: User feedback and support issues.

Recovery and response: Reopen share flow; allow copy/share alternative. Acceptance test / evidence: Cancel WhatsApp share; app must not mark delivered.

R23 — Account takeover and credential theft

Severity: High | Domain: Security | Proposed owner: Security/backend | Phase: P0 | Residual risk: Medium Failure scenario: Attacker signs in as merchant owner.

Best-practical prevention: Strong authentication, secure sessions, rate limiting, MFA for admins, credential hygiene.

Detection and monitoring: Suspicious sign-in and token-reuse alerts.

Recovery and response: Revoke sessions, rotate secrets, investigate and restore account. Acceptance test / evidence: Brute-force, stolen-token and session-expiry tests.

R24 — AI provider outage or quota exhaustion

Severity: High | Domain: Availability | Proposed owner: AI/ops | Phase: P0 | Residual risk: Medium Failure scenario: Gemini unavailable during shop hours.

Best-practical prevention: AI circuit breaker, timeouts, usage headroom, clear manual-entry fallback. Detection and monitoring: Provider error/timeout and quota alerts.

Recovery and response: Switch to manual entry; queue only safe user-approved drafts; retry later. Acceptance test / evidence: Force 429/500/timeouts; ledger remains operational.

R25 — Backup failure or unrecoverable incident

Severity: Critical | Domain: Resilience | Proposed owner: Backend/ops | Phase: P0 | Residual risk: Medium Failure scenario: Database corruption and unusable backup.

Best-practical prevention: Automated backups, retention, restore drills, documented RPO/RTO and access separation.

Detection and monitoring: Backup job alerts and restore verification.

Recovery and response: Restore known-good snapshot, reconcile journal, communicate incident. Acceptance test / evidence: Quarterly full restore drill; prove RPO/RTO objectives.

R26 — Prompt injection / unsafe AI actions

Severity: High | Domain: AI security | Proposed owner: AI/backend | Phase: P0 | Residual risk: Medium Failure scenario: Audio asks AI to ignore rules or reveal other shop data.

Best-practical prevention: Treat model output as untrusted; schema validation; allowlisted intents; backend authorization; no direct DB tool.

Detection and monitoring: Rejected intents, anomalous query logs and adversarial test results. Recovery and response: Reject request, record incident, restrict compromised flows.

Acceptance test / evidence: Adversarial audio/text tests; AI cannot bypass tenant or confirmation checks.

R27 — Cash mismatch and payment reconciliation

Severity: High | Domain: Financial ops | Proposed owner: Product/backend | Phase: P1 | Residual risk: Medium



Failure scenario: Recorded payments differ from cash drawer.

Best-practical prevention: Payment methods, shift/day close report, optional allocation to invoices, no implied bank settlement.

Detection and monitoring: Daily totals and unexplained variance reports.

Recovery and response: Investigate and enter authorized adjustment, preserve original receipt. Acceptance test / evidence: Mixed cash/UPI/partial payment scenarios; totals reconcile.

R28 — Compliance and tax overclaim

Severity: High | Domain: Legal/business | Proposed owner: Founder/legal | Phase: P1 | Residual risk: Medium Failure scenario: Product is presented as compliant tax software without validation.

Best-practical prevention: Define bookkeeping scope; jurisdiction-specific legal review; tax fields only when verified; no lending/payment processing claims.

Detection and monitoring: Release checklist and legal review triggers.

Recovery and response: Correct claims, pause affected feature, update documentation. Acceptance test / evidence: Review marketing, invoices, retention, vendor contracts before launch.



###### Risk dependency map

Voice capture → AI interpretation → typed JSON proposal → server validation → merchant confirmation → idempotent journal write → statement/balance projection. R01/R09/R10/R18/R26 affect proposal quality; R02/R04 affect identity and direction; R03/R05/R08/R25 affect journal integrity; R06/R15/R19/R23 affect access; R07/R11/R24 affect availability. Controls must be applied at each boundary, not only at the model.



###### Financial invariants (non-negotiable)

A transaction is posted only after authenticated merchant confirmation (unless a separately approved future workflow explicitly changes this).

One idempotency key within its tenant/operation scope maps to at most one committed financial effect.

All money is represented as integer paise or another exact decimal representation, never floating-point arithmetic.

A customer balance equals the sum of authorized, posted ledger effects; derived caches can be rebuilt.

Reversals and adjustments reference the original event and retain actor, timestamp and reason.

Unspecified item prices/quantities are never fabricated; aggregate totals are not silently split.

No query, export, report, AI tool or background job bypasses tenant authorization.

Offline queued actions are visibly pending until the server confirms them.





Worked example: ₹160 multi-item credit bill

Spoken: “Kumar account-la half kilo dal, one litre milk, total one hundred sixty rupees.” Proposed JSON (draft, not yet persisted):

{ "intent": "ADD_CREDIT", "customer_spoken_name": "Kumar", "items": [{"name":"Dal","quantity":0.5,"unit":"kg","price":null},{"name":"Milk","quantity":1,"unit":"litre","price":null}],  "total_amount":160, "currency":"INR" }



Step 1: AI produces schema-validated draft. Step 2: Backend resolves tenant-specific Kumar or asks merchant to choose. Step 3: UI previews both items and total ₹160, clearly marking unspecified line prices. Step 4: Merchant confirms. Step 5: Express validates authorization and idempotency; MongoDB atomically writes bill and append-only journal event. Step 6: Balance projection updates and a receipt is shown. A repeated request returns the original result.



###### Risk-to-test coverage and pilot release gates



###### Incident response playbook

Identify: classify financial-integrity, security/privacy, availability or usability incident; record tenant and affected transaction IDs.

Contain: pause unsafe financial writes or AI flow while keeping safe manual access where feasible; revoke compromised credentials.

Preserve: keep immutable journal, request IDs, redacted logs and evidence; do not overwrite disputed records.

Recover: restore service, replay/reconcile posted events, reverse or adjust incorrect records with approvals.

Communicate: notify affected merchants and authorities when applicable; do not promise timelines without verification.

Learn: root-cause review, regression test, owner and due date; update risk score and release gate.





###### Pilot monitoring dashboard







###### Cost stress test — illustrative only

Example: 100 shops × 100 voice commands/day × 30 days × ₹0.12/command = ₹36,000 monthly AI expense. At

₹299/shop/month, revenue is ₹29,900 before hosting, support and taxes. This is a scenario, NOT verified Gemini pricing. Measure real token/audio consumption and failed-call rates before setting plans.



###### First 30-day mitigation plan



###### Open decisions requiring sign-off

Who may reverse a bill, and above what amount is owner re-authentication mandatory?

Are household accounts shared by default or explicitly linked by merchant choice?

How will payments be allocated: general account balance, oldest bill first, or merchant-selected invoice?

What are the opening-balance evidence and dispute rules?

What offline actions are allowed in MVP, and how long may pending actions remain?

What audio retention period and consent wording will be used?

What RPO/RTO, monthly AI spend cap and transaction amount warning thresholds are acceptable?

Which 5–20 pilot merchants agree to participate, and how will feedback be collected?





###### Governance and document control

Review weekly during development and daily during the first pilot week. Assign one named owner per risk; attach test results, dates, severity changes and accepted residual risk. Update this document whenever an incident, feature change or external dependency changes exposure.

Disclaimer: Engineering planning document, not legal or financial compliance certification. Privacy, GST/tax, contractual and regulatory obligations require qualified review before relevant production features are offered.



### CredYazh





Kalai AI Assistant — RAG Integration & Frontend Experience Design

Product design and architecture companion | Version 1.0 | 19 October 2026

Positioning: CredYazh is a multilingual voice-ledger PWA. Kalai is an AI assistant inside CredYazh—not a separate product and not the engine responsible for financial persistence.



###### Executive summary

CredYazh manages merchant credit, payments, balances and statements. The optional Kalai assistant helps users understand the app, ask authorized questions, and prepare voice-based transaction drafts. RAG is appropriate for knowledge-based help, but is not required for voice-to-JSON extraction or database balance calculations.



###### RAG versus the core voice-ledger workflow

###### Why this distinction matters

RAG retrieves relevant passages from unstructured knowledge and grounds a model response. A structured database lookup is more accurate for exact balances and should not be replaced with approximate vector search.



###### Frontend experience: CredYazh home

Concept wireframe for Android-first PWA. This is a design proposal, not an implemented screen.





Primary navigation: Home, Customers, Kalai, Profile. A prominent microphone entry can initiate voice transaction capture. Manual entry must always remain accessible.



###### Frontend experience: Kalai assistant

Kalai is reached through the app navigation or an optional contextual assistant entry point. It supports typed and spoken questions, presents grounded help, and routes balance questions to authorized APIs.





###### Required UI states



###### Simple system architecture

CredYazh React PWA → Express API gateway (auth, tenant scope, validation)

Express → MongoDB: customers, bills, payments, append-only ledger events



Express → Kalai AI service (FastAPI): intent routing and structured proposals

Kalai → Gemini: speech understanding / answer generation

Kalai → knowledge retriever: approved FAQ, product guides, troubleshooting content

Kalai → Express tools: approved read-only balance/history endpoints

Financial write: draft → backend validation → merchant confirmation → atomic commit





###### Voice transaction lifecycle

Example: “Kumar account-la half kilo dal, one litre milk, total 160 rupees.”

1. Merchant records audio. 2. PWA sends request with authenticated session. 3. AI service extracts intent and a JSON proposal. 4. Express validates fields and resolves customer identity. 5. Merchant reviews and confirms. 6. Express commits bill and ledger event with idempotency protection. 7. UI refreshes the balance.

###### Illustrative JSON draft — not a database write

{

"intent": "ADD_CREDIT", "customer_spoken_name": "Kumar", "items": [

{"name": "Dal", "quantity": 0.5, "unit": "kg", "price": null},

{"name": "Milk", "quantity": 1, "unit": "litre", "price": null}

],

"total_amount": 160, "currency": "INR"

}

Individual prices are unknown and must remain null. The backend never infers or invents missing financial values.



###### RAG architecture for Kalai knowledge support

Knowledge sources → document ingestion → cleaning/chunking → embeddings → vector index → tenant-appropriate retrieval → Gemini grounded answer → source links in UI.

###### Recommended initial content

Product FAQ; onboarding steps; correction/reversal instructions; supported voice phrases; error explanations; role permissions and privacy guidance.

###### Retrieval safeguards

Use only approved, versioned product documents; apply permissions to retrieved content; prevent prompt injection from retrieved text; log retrieval quality without exposing sensitive customer information. Cite help article title/version in answers.



###### API boundary examples



The AI service must not accept direct database credentials or arbitrary SQL/MongoDB queries generated by a model.



###### Privacy, safety and reliability

Never allow cross-tenant data access; derive tenant identity from verified auth context.

Do not auto-save AI-extracted financial values without explicit merchant confirmation.

Use idempotency keys and immutable adjustment/reversal events.

Provide an offline manual-entry path; cloud AI may be unavailable offline.

Define audio retention/deletion and disclose third-party processing.

Enforce rate limits, logging redaction, API key isolation and cost ceilings.

Benchmark Tamil, Tanglish, English, noise, latency and financial extraction accuracy.





###### MVP versus later releases



###### Suggested implementation order

Finalize screen wireframes and component states.

Build tenant-safe ledger and read-only query APIs.

Build Kalai chat panel with scripted FAQ and secure balance tool.

Integrate voice-to-JSON and confirmation preview.

Pilot with real merchant phrases and collect usability feedback.

Add RAG only after help content and retrieval evaluations justify it.





###### Acceptance checklist for teammates

Kalai is visibly an in-app assistant, not a separate app.

Every balance shown is sourced from authorized backend calculation.



Voice drafts never write directly to the database.

Unspecified individual prices remain null.

RAG answers use product documentation; no hallucinated financial records.

App remains useful when AI is slow or unavailable.

Document status: proposed frontend and technical design for review; not a claim that these features have been implemented.



### CredYazh

FINPS Analysis





Feasibility • Impact • Novelty • Presentation • Scalability

Project understanding and hackathon evaluation guide | Version 1.0 | October 2026

Theme: FinTech & EdTech (FinTech). Product: CredYazh, a multilingual voice-ledger PWA for small merchants. Kalai is an AI assistant inside CredYazh; it is not a separate product or the sole engine of the ledger.



###### At a glance: the five FINPS questions



###### FEASIBILITY — Can CredYazh actually work?

Technical feasibility

The MVP uses established technology: React/Vite PWA for Android-first screens; Express for authentication and financial rules; MongoDB/Mongoose for tenant-scoped records; FastAPI and Gemini for interpreting speech into proposed JSON. The architecture is technically achievable, but speech accuracy and transaction safety must be proven in realistic shops.







Operational and financial feasibility

Start with one shop category: kirana/grocery. Avoid launching all eight domains simultaneously.

Use manual entry as a fallback whenever voice AI is unavailable or uncertain.

Measure API cost per confirmed transaction, not just cost per model call.

Pilot with 5–20 consenting shops after passing financial and privacy release checks.

Do not assume merchants will pay until willingness-to-pay interviews and pilot usage support it.

MVP scope and realistic boundaries

Must have: Customer profiles, opening balances, manual credit/payment, itemized bill, preview/confirm voice entry, transaction history, statements, basic tenant roles, audit events and correction flow.

Can wait: RAG help retrieval, route-delivery automation, construction project ledgers, advanced analytics and fully automated reminders.

Feasibility verdict: Conditionally feasible. The biggest uncertainty is not whether the app can be coded; it is whether merchants can use it quickly and reliably in noisy real conditions.



###### IMPACT — Why would this matter?

Problem being addressed

Many small merchants work on narrow margins on individual goods. A forgotten credit sale, incorrect repayment entry or disputed balance may wipe out the benefit of multiple small transactions. This is a plausible pain point, not a universal or measured claim; the team must validate its frequency and severity.

Before and after scenario



Illustrative merchant story

A shopkeeper sells items with only ₹1–₹5 gross profit on some products. One missed ₹100 credit record could be meaningful. These figures illustrate the stakes; they are not verified average merchant margins or loss estimates.



How to measure actual impact





###### NOVELTY — What is meaningfully different?

CredYazh should not claim to be the first voice ledger. Its proposed differentiation is an integrated merchant workflow optimized for multilingual spoken transactions and financial correctness.





Novelty is not the same as inventing a new algorithm

The innovation can be a better end-to-end experience, especially for a specific underserved workflow. Judges may ask how CredYazh compares with existing ledger apps; prepare an evidence-based comparison instead of claiming competitors lack voice features.



###### PRESENTATION — How should we explain it?

One-line pitch

CredYazh is a multilingual voice-ledger PWA that helps small merchants record credit sales and payments naturally, while keeping their financial records reviewable and reliable.



A 90-second demonstration script



Recommended presentation sequence

Problem and real merchant quote (with consent)

Why the current workflow is painful

CredYazh solution and app screens

Live voice-to-JSON-to-ledger demonstration

Risk controls and trust safeguards

Feasibility, impact metrics and roadmap

Likely judge questions





###### SCALABILITY — Can it grow responsibly?

Scale in three stages





System scaling strategy

Shared MongoDB collections with mandatory tenantId filters and compound indexes initially.

Stateless Express instances behind a load balancer as traffic grows.

Separate asynchronous work such as report generation from transaction posting.

Use idempotency keys, transactional writes and append-only financial events.

Track AI cost, retries, latency and success per merchant; enforce fair-use limits.

Maintain backups, restore drills, observability and incident response.

Scaling constraints

Scaling users is not just adding servers. Support requests, merchant onboarding, local language coverage, privacy obligations, device performance and AI processing bills may become the limiting factors. Pricing and customer acquisition assumptions remain unvalidated.



###### FINPS scorecard — evidence, not marketing

The following is a qualitative planning assessment only. It is not a validated numerical rating or a forecast of hackathon scores.









###### Four-week validation plan





###### Final verdict and team responsibilities

CredYazh is a promising FinTech project because it targets a concrete merchant workflow and has a clear,

demonstrable technical solution. Its strongest case is not “AI can do anything”; it is “merchants can record and verify accounts with less friction, without sacrificing financial correctness.”

Product lead: Merchant interviews, scope, positioning and presentation. Frontend lead: Mobile PWA, accessibility, recording and confirmation UI. Backend lead: Ledger invariants, auth, tenant isolation and APIs.

AI lead: Audio evaluation, structured JSON extraction and Kalai help.

QA/security lead: Risk register, regression tests, backups and privacy checks.

Decision gate: proceed to pilot only after transaction integrity, merchant confirmation, tenant isolation, recovery and consent requirements have been tested.



₹₹

## CredYazh — See the entire app in 10 minutes

A multilingual voice ledger for small merchants. Kalai is an assistant inside the CredYazh PWA.







#### !	THE PAIN

A busy shopkeeper sells low-margin items. Credit is forgotten, delayed, or written incorrectly. Customers may dispute balances.









#### THE PRODUCT

CredYazh records customer credit, payments, and itemized bills through a simple mobile interface and voice workflow.









#### THE RESULT

The shopkeeper reviews the bill, confirms it, and sees an updated customer balance and shareable statement.













Key rule: AI never directly posts money to the ledger. The merchant confirms; the backend validates and saves.

CredYazh | Teammate visual walkthrough | Concept v1.0	01



##### Product mind map





Everything a teammate needs to know at a glance











Customers

Names, aliases, opening dues



















Merchant setup

Shop, staff, settings

Voice ledger

Tamil • Tanglish • English









#### CREDYAZH

Merchant-facing PWA











Money records

Bills, credit, payments

Statements

Balances, history, share

















Kalai assistant

Help, questions, voice actions















CredYazh | Teammate visual walkthrough | Concept v1.0	02



##### Merchant journey: from first launch to daily use

An app flow, not a developer-only architecture









CredYazh | Teammate visual walkthrough | Concept v1.0	03



##### UI screen flow: what the merchant taps





Illustrative screen map; final labels and layouts will be validated with shopkeepers

















CredYazh | Teammate visual walkthrough | Concept v1.0	04



One voice command → one itemized bill





Illustrative merchant speech: “Kumar account-la half kilo dal, one litre milk, total 160 rupees.”









CredYazh | Teammate visual walkthrough | Concept v1.0	05



##### What the AI-generated JSON looks like





An AI proposal is not a saved transaction. JSON becomes trusted only after checks and merchant confirmation.





































































CredYazh | Teammate visual walkthrough | Concept v1.0	06



##### Where the data travels





Simplified system architecture — boundaries and responsibilities

















CredYazh | Teammate visual walkthrough | Concept v1.0	07



##### How the ledger stores money





Never store “balance” as an unexplained number that can be overwritten.



















CredYazh | Teammate visual walkthrough | Concept v1.0	08



##### Three common branches and what happens





Examples show why the app must not silently guess













CredYazh | Teammate visual walkthrough | Concept v1.0	09



##### Kalai vs CredYazh: clear responsibilities





Kalai is the AI assistant inside CredYazh — not the product itself.







Example: Kalai suggests “Add ₹160 credit for Kumar.” CredYazh validates and records it only after confirmation.













CredYazh | Teammate visual walkthrough | Concept v1.0	10



##### MVP demo story: what to show a teammate





Follow this exact journey in a prototype; the screens may initially use mock data.











































































































CredYazh | Teammate visual walkthrough | Concept v1.0	11



##### Boundaries, assumptions, and next decisions





This is an onboarding visualization, not a replacement for the detailed SRS or SA&DD.













CredYazh | Teammate visual walkthrough | Concept v1.0	12