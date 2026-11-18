# Peak Window

An ADHD day planner that schedules everything around your stimulant pharmacokinetics instead of the clock.

Single-file app — no build step, no dependencies to install. React + Tailwind via CDN, JSX compiled in-browser by Babel standalone. All data stays on your device in `localStorage`.

## Features

- **Effect curve** — models long-acting lisdexamfetamine (onset ~1.5–2h, peak ~4h, tail to ~12h) plus an optional prescribed short-acting afternoon booster, drawn as a live SVG with a "now" marker.
- **Auto-built schedule** keyed off dose time, with three day types: Study, Clinical/theatre, Recovery/post-call.
- **Fuel timing** woven in — eat-by-the-clock meals and snacks placed to protect concentration through appetite suppression and the comedown.
- **Top 3 + task list** — tasks tagged 🧠 Deep or 🍃 Light; the "Right now" card surfaces only the tasks that fit the current block on the curve.
- **Focus check-ins & insights** — 1-tap 1–5 ratings build your *actual* focus curve vs the textbook model, with SOS presses overlaid.
- **Focus SOS** — curve-stage-aware advice, a 5-step reset protocol, and a one-card-at-a-time tactic dealer.
- **Focus gym** — trainable attention exercises with built-in timers.
- **Snack Patrol** — boredom-vs-hunger triage, craving-matched low-calorie snacks, daily kcal budget.
- **50/10 pomodoro** with chimes at phase ends and block transitions (toggleable).

## Run locally

Open `index.html` in a browser. That's it.

## Deploy on GitHub Pages

1. Create a new repository and push these files.
2. Repo **Settings → Pages → Source**: deploy from branch, `main`, `/ (root)`.
3. Your app is live at `https://<username>.github.io/<repo>/`.

## Install on iPhone (basic)

Open the GitHub Pages URL in Safari → Share → **Add to Home Screen**. For a full PWA (offline support, real notifications), add a manifest + service worker — the app is structured to make that straightforward.

## Data & privacy

Everything (settings, daily logs, task list, focus history) lives in your browser's `localStorage` under `pw:*` keys. Nothing leaves your device. Clearing site data resets the app.

## Disclaimer

Planning aid only — not medical advice. Medication doses and timing belong to you and your prescriber; the app deliberately models a single daily long-acting dose (plus an optional booster **only if prescribed**) and warns when timing would threaten sleep.

## Also in this repo: FRCS Atlas

[`frcs-atlas/`](frcs-atlas/) is a separate installable app: an independent FRCS cardiothoracic learning beta (lessons, SBA questions, timed vivas, source directory). See [`frcs-atlas/README.md`](frcs-atlas/README.md).
