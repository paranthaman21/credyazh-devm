# Yazh Tour — Rollback Guide

## Option 1: Disable via feature flag (recommended, zero-risk)

Set the environment variable and restart the dev server:

```env
# client/.env
VITE_YAZH_TOUR_ENABLED=false
```

When `false`, `useYazhTour` returns immediately and nothing is rendered.
The app runs exactly as it did before the tour was added.

---

## Option 2: Remove the integration from App.jsx (surgical revert)

Three lines to undo:

```diff
# 1. Remove import (line 7 of App.jsx)
-import YazhTour from './yazh-tour/index.jsx';

# 2. Remove the mount (near bottom of App return)
-<YazhTour
-  currentView={view}
-  onNavigate={setView}
-  onOpenKalai={() => setShowKalaiModal(true)}
-/>

# 3. Remove data-tour="tour-kalai-btn" from the Kalai button (cosmetic only)
```

The `data-tour` attributes on `data-tour="tour-entry-panel"` etc. are inert
HTML attributes — they cause no harm if left behind.

---

## Option 3: Full removal

```powershell
Remove-Item -Recurse -Force "credyazh\client\src\yazh-tour"
Remove-Item -Recurse -Force "docs\yazh-tour"
```

Then revert the three App.jsx lines from Option 2.

---

## Verification after rollback

```powershell
npx vite build   # must exit 0
```

Run the dev server and confirm:
- Dashboard loads normally
- Voice entry works
- Customer ledger works
- Kalai modal opens
- No console errors mentioning 'yazh' or 'tour'
