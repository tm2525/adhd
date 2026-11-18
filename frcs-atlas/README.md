# FRCS Atlas — Cardiothoracic learning beta 0.1.0

Built: 18 November 2026. Independent educational prototype; not affiliated with or endorsed by JCIE, ISCP, FRCS colleges or any society or publisher.

## Open immediately
Open `index.html` in a modern browser. The main learning, question and revision features are self-contained. External publication links require internet access. Some browsers restrict local storage for file URLs; use a local server for reliable persistence.

## Run as a progressive web app
From the extracted folder:

```sh
python -m http.server 8000
```

Open http://localhost:8000/index.html and use the browser's Install / Add to Home Screen command where supported. A manifest and service worker are supplied. Installation support varies by browser. Production hosting requires HTTPS. GitHub Pages or another static host can serve these files; this bundle has NOT been deployed.

A service worker caches the application shell after its first successful load. External sources are not cached. Browser data clearing can remove offline assets and study progress. Offline use always displays a dated snapshot, not current surveillance.

## Included
- 49 provisional topic slots across five domains: 8 starter lessons, 41 planned chapters.
- 8 original SBA practice questions; 3 timed viva exercises.
- 35 source/directory links including AATS, STS, EACTS, ESTS, SCTS, NICE, JCIE/FRCS, ISCP, JAMA, Nature, Perfusion, NEJM, Lancet and specialist journals.
- Search, bookmarks, read markers, self-rated confidence, private notes.
- Answer feedback, local attempts and user-selected review scheduling.
- Local publication-review queue, JSON export and progress backup/restore.
- Responsive interface, dark theme, keyboard focus and a skip link.

## What the content status means
Source-checked seed means a limited starter synthesis checked against the cited source, NOT independent clinical peer review. Original trial abstract access is labelled where applicable. Planned chapters contain no released clinical recommendations. Provisional topic slots do not establish complete objective-level curriculum coverage. No official exam weighting or pass prediction is claimed.

No user PDFs have been bulk reproduced. Guideline directory links are not incorporated guidance. ESC explicitly states that software use of guideline content requires a formal licence; protected guideline tables and algorithms have not been included. STS also states restrictions on electronic republication. Obtain the appropriate permissions before expansion or distribution. Journal subscriptions or access rights are not included. No third-party images or society logos are bundled.

## Updating content
`content.json` is the editable dataset. The same data are embedded into index.html so the app also runs directly from a file. After editing content.json run:

```sh
python build_content.py
```

Then increment the release version and service-worker cache key for a public deployment. Test all dependent chapters, questions and references. JSON edits are an engineering operation, not clinical approval.

The editorial queue lives only in your browser and cannot publish or change the released lessons. Export it for the clinical editorial team. There is no server, account system, cloud sync, automatic PubMed/journal polling, subscription scraping, AI tutor or production CMS in this release.

## Editorial release gates
1. Complete objective-level mapping against the official August 2026 curriculum and current JCIE blueprint.
2. Author and clinically review each domain, including congenital, transplantation, critical care and emergency topics.
3. Verify original publication, population, endpoints, units, uncertainty and corrections.
4. Resolve publisher rights, licensing and permissions.
5. Document named reviewers, sign-off dates and dependent learning items.
6. Conduct clinical safety, accessibility, browser, installation and resident usability testing.
7. Separate education from clinical decision support; do not release patient-specific treatment advice without a separate governance assessment.

## Privacy
Progress, notes and editorial records use browser localStorage. They are not encrypted. Do not enter identifiable patient information or confidential material. Exported backups contain notes. No analytics or AI network calls are included; source links open external publisher sites.

## Testing
See TEST-REPORT.md for tests actually performed. Tests do not certify clinical correctness, completeness, accessibility compliance or cross-browser compatibility.

## Deployment handoff
This is a static app. Place index.html, manifest.webmanifest, icon.svg and sw.js at the same relative location on an HTTPS static host. Keep content.json, build_content.py and review artefacts in a maintained source repository. No paid API keys or package installation are required to run the frontend.
