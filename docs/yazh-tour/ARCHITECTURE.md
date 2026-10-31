# Yazh Tour — Architecture & State Flow

## State Machine (`useYazhTour`)

```
idle
 │
 └─(first visit, 900ms delay)──► offer
                                    │
                         ┌──────────┴──────────┐
                   onStart()             onSkip()
                         │                     │
                      running               done ──► HelpLauncher
                         │
                    stepIndex 0..6
                    (nextStep / prevStep)
                         │
                  stepIndex === 6 + nextStep()
                         │
                       done ──► markComplete() → localStorage
```

## Component Tree

```
App.jsx
└── YazhTour (index.jsx)
    ├── [phase=offer]   → YazhWelcome
    ├── [phase=running]
    │   ├── [step=welcome] → YazhWelcome (tourMode)
    │   └── [step=2..7]   → YazhTooltip
    │                          └── [step=reliability] → TechnicalInsights (inline)
    └── [phase=done]    → YazhHelpLauncher
```

## Navigation Integration

`YazhTour` receives `currentView` and `onNavigate` as props from `App`.
When a step requires a different view, `onNavigate(targetView)` is called — the same
callback used by the bottom nav. No routing library is involved; the app uses
view state (`'home' | 'customers' | 'entry'`).

Kalai is opened by calling `onOpenKalai()` (maps to `setShowKalaiModal(true)`).

## Spotlight

Each step with a `targetDataAttr` value applies `.yazh-spotlight-active` to:
```js
document.querySelector(`[data-tour="${step.targetDataAttr}"]`)
```

Affected elements:
| data-tour            | Element                      |
|----------------------|------------------------------|
| `tour-kalai-btn`     | "Ask Kalai AI" header button |
| `tour-voice-btn`     | "Record Voice Note" mic btn  |
| `tour-entry-panel`   | New Entry section card       |
| `tour-customer-list` | Customer directory wrapper   |

The class is removed on cleanup (React `useEffect` return).

## localStorage

Key: `credyazh_yazh_tour_v1`
Value: `'v1'` (written on skip or finish)
Absence → `isFirstVisit = true` → offer phase triggered automatically.
