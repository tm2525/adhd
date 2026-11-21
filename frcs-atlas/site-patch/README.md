# Patch for tm2525/Claude-apps (FRCS site), 21 November 2026

This patch is for the `frcs/` site, which is built from `st4-src/`. It fills the gaps found when all 54 FRCS Atlas chapters were checked against the site. This session couldn't push to `Claude-apps`, so the change is delivered here as a patch.

It touches only `st4-src/`. It applies cleanly on top of `86e11a3`.

## Apply

```bash
cd Claude-apps
git am /path/to/0001-frcs-atlas-audit-fixes.patch   # or: git apply
pip install markdown beautifulsoup4 lxml            # if not installed
python3 st4-src/build.py                            # rebuilds st4/ and frcs/
git add -A && git commit --amend --no-edit          # include the rebuilt pages
git push
```

## What changes

**New section in the FRCS syllabus map:** professional practice. This is Atlas chapter 54, which the site lacked. It covers:
- NACSA/NLCA audit
- HQIP alert and alarm limits (2 SD and 3 SD; 99.8%)
- VLAD and CUSUM charts
- WHO checklist (Haynes 2009)
- the current status of Never Events
- PSIRF and the Regulation 20 Duty of Candour
- statistics for the viva (ARR, RRR, NNT, SnNout/SpPin, non-inferiority)
- genomics governance
- sustainability (desflurane from April 2024; net zero 2040 and 2045)

**Gap fills:**
- Echo cannot exclude type A dissection.
- Open repair of blunt aortic injury with left heart bypass.
- Aortic stenosis futility (Class III when survival beyond 1 year is unlikely).
- Bicaval against biatrial implantation.
- Why bronchopleural fistula is commoner after right pneumonectomy.
- The UCSD CTEPH classifications by name.
- Aspirin after a shunt, and the CLARINET result.
- Glenn and Fontan haemodynamic criteria; signs of a failing Fontan.
- Ebstein pre-excitation.

**Notes that reconcile figures the site gives more than one way:**
- DOACs: EACTS 2024 recommends stopping 48 to 96 h before surgery (I B); the 36 to 48 h figure is from the body text.
- Post-cardiotomy shock: under 4%, not 0.5 to 1.5%.
- ESC 2024 AF ablation levels (I A and IIa B).
- Trusler constants (20, 24 and 22 mm + 1 mm/kg).
- Subaortic stenosis: the threshold is a peak gradient of 50 mmHg or more.

Every added line says what it was checked against. Lines checked only from memory or a search extract say so.

**Not changed, because the site was already right:**
- the TR concomitant classes
- the adrenaline dose (100–300 µg, EACTS 2009)
- Trusler in the main tables
- the left main SYNTAX class
- the primary MR class
- the AR thresholds
- the ACHD classes
