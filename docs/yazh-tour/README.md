# Yazh Guided Tour — Feature Overview

## What is Yazh?

**Yazh** is a friendly animated mascot guide that introduces first-time visitors — especially DEXATHON Round 2 judges — to the real CredYazh prototype through an interactive seven-step tour.

Yazh is **not** Kalai, **not** the Gemini extraction engine, and **not** a video. It is a lightweight React overlay that navigates through the existing app's actual screens.

---

## Feature Flag

```
VITE_YAZH_TOUR_ENABLED=true   # enable (default)
VITE_YAZH_TOUR_ENABLED=false  # completely disable — no code runs
```

Set in `client/.env` (for local dev) or the deployment environment.

---

## File Structure

```
client/src/yazh-tour/
├── index.jsx                    ← Top-level orchestrator (mount once in App.jsx)
├── components/
│   ├── YazhMascot.jsx           ← Reusable mascot image with emoji fallback
│   ├── YazhWelcome.jsx          ← First-visit welcome card & step 1 intro
│   ├── YazhTooltip.jsx          ← Bottom-sheet tour tooltip (steps 2–7)
│   ├── YazhSpotlight.jsx        ← SVG-mask overlay with polling & resize tracking
│   ├── YazhTapIndicator.jsx      ← Animated hand tap & ripple pointer demonstration
│   ├── YazhTechnicalInsights.jsx← Step 6 architecture card with failover flow
│   └── YazhHelpLauncher.jsx     ← Floating replay button (after tour done)
├── hooks/
│   └── useYazhTour.js           ← State machine: idle → offer → running → done
├── config/
│   ├── tourSteps.js             ← 7 step definitions
│   └── yazhAssets.js            ← PNG asset registry with fallback
└── styles/
    └── yazhTour.css             ← All tour animations, spotlight, and tap styles
```

---

## Safety Guarantees

The Yazh tour **NEVER**:
- Calls `api.*` endpoints
- Triggers Gemini or Groq extraction
- Saves, modifies, or deletes any ledger data
- Changes customer balances
- Triggers WhatsApp messages
- Modifies Kalai's behavior
- Writes to MongoDB

The only side effects are:
- `localStorage.setItem('credyazh_yazh_tour_v1', 'v1')` on completion/skip
- `setView()` call to navigate app views
- CSS class `yazh-spotlight-active` applied briefly to DOM elements

---

## Replay

Users can replay by clicking the floating **Tour Guide** launcher that appears after the tour ends.
Programmatically: `localStorage.removeItem('credyazh_yazh_tour_v1')` then reload.

---

## Skills Used

- **Web application development guidelines** (from system prompt): React 18, Vite, vanilla CSS
- **Mobile-first responsive design** principles: safe-area-inset, clamp(), bottom-sheet pattern
- **AAS rules**: Small, testable changes; preserve existing architecture conventions
