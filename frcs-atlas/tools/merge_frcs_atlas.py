#!/usr/bin/env python3
"""
FRCS (CTh) & EBCTS 2026 Atlas — One-Command Local 54-Chapter Merger
Zero external dependencies (Python 3 standard library only).

Usage:
  1. Put this file in the folder containing your unzipped HTML files (or pass the folder path).
  2. Run:   python3 merge_frcs_atlas.py
     (or:   python3 merge_frcs_atlas.py /path/to/your/html/folder)
  3. Outputs:
     - FRCS-EBCTS-ISCP2026-Consolidated-54-Chapters.html  (if FRCS-Atlas-Consolidated.html is found)
     - FRCS-EBCTS-ISCP2026-Standalone-54-Chapters.html    (always built — clean offline searchable app)
"""

from __future__ import annotations  # allows "str | None" on Python 3.7-3.9

import re, sys
from pathlib import Path
from html import escape as H

MANIFEST = [
    ("s1", "1. Aortic root aneurysm and valve-sparing root replacement", "Aortic"),
    ("s2", "2. Ascending aortic aneurysm and bicuspid aortopathy", "Aortic"),
    ("s3", "3. Acute type A aortic dissection", "Aortic"),
    ("s4", "4. Arch aneurysm, arch replacement and cerebral protection", "Aortic"),
    ("s5", "5. Acute type B aortic dissection", "Aortic"),
    ("s6", "6. Intramural haematoma and penetrating aortic ulcer", "Aortic"),
    ("s7", "7. Descending thoracic aortic aneurysm and TEVAR", "Aortic"),
    ("s8", "8. Thoracoabdominal aortic aneurysm and spinal cord protection", "Aortic"),
    ("s9", "9. Chronic aortic dissection and residual false-lumen disease", "Aortic"),
    ("htad", "10. Heritable thoracic aortic disease and pregnancy", "Aortic"),
    ("endoleak", "11. Endoleak and late endovascular complications", "Aortic"),
    ("infection", "12. Aortic infection and infected vascular grafts", "Aortic"),
    ("btai", "13. Blunt thoracic aortic injury (BTAI)", "Aortic"),
    ("aortic_stenosis", "14. Aortic stenosis and lifetime management (SAVR vs TAVI)", "Adult Cardiac"),
    ("aortic_regurgitation", "15. Aortic regurgitation and aortic valve repair", "Adult Cardiac"),
    ("primary_mr", "16. Primary (degenerative) mitral regurgitation and mitral valve repair", "Adult Cardiac"),
    ("secondary_mr_ms", "17. Secondary mitral regurgitation and mitral stenosis", "Adult Cardiac"),
    ("tricuspid_valve", "18. Tricuspid regurgitation and right-sided valve surgery", "Adult Cardiac"),
    ("prosthetic_redo", "19. Prosthetic valve dysfunction, PPM, PVL and redo cardiac surgery", "Adult Cardiac"),
    ("endocarditis", "20. Infective endocarditis (native, prosthetic and aortic root abscess)", "Adult Cardiac"),
    ("cad_cabg", "21. Coronary artery disease and CABG", "Adult Cardiac"),
    ("mech_mi", "22. Mechanical complications of myocardial infarction", "Adult Cardiac"),
    ("cpb_pccs", "23. Cardiopulmonary bypass, myocardial protection and PCCS", "Adult Cardiac"),
    ("lvad_transplant", "24. Advanced heart failure, durable LVADs and heart transplantation", "Adult Cardiac"),
    ("cardiac_anatomy_phys", "25. Surgical cardiac anatomy, applied physiology and risk stratification", "Adult Cardiac"),
    ("af_arrhythmia", "26. Surgery for atrial fibrillation, LAA occlusion and pacemakers/ICDs", "Adult Cardiac"),
    ("pericardial_disease", "27. Pericardial disease (tamponade, constrictive pericarditis and effusions)", "Adult Cardiac"),
    ("tumours_hocm_lv", "28. Cardiac tumours, HOCM and LV aneurysms", "Adult Cardiac"),
    ("pe_cteph", "29. Acute massive pulmonary embolism and CTEPH (PEA/BPA)", "Adult Cardiac"),
    ("carotid_trauma", "30. Combined carotid/CABG, combined valve/CABG and cardiac trauma", "Adult Cardiac"),
    ("cardiac_icu_bojar", "31. Cardiac surgical critical care, perioperative pharmacology and complications", "Adult Cardiac"),
    ("thoracic_anatomy_pft", "32. Thoracic surgical anatomy, pulmonary physiology and preoperative fitness", "General Thoracic"),
    ("lung_cancer_staging", "33. Pulmonary nodules, IASLC 9th Edition TNM and mediastinal staging", "General Thoracic"),
    ("nsclc_surgery", "34. Early-stage and locally advanced NSCLC", "General Thoracic"),
    ("pneumonectomy_bpf_carcinoid", "35. Post-pneumonectomy complications, BPF, carcinoid and metastasectomy", "General Thoracic"),
    ("lvrs_infections_lungtx", "36. Emphysema (LVRS), ILD, infections/haemoptysis and lung transplantation", "General Thoracic"),
    ("pleural_bts2023", "37. Pneumothorax, pleural effusion, empyema and chylothorax (BTS 2023)", "General Thoracic"),
    ("mesothelioma", "38. Malignant pleural mesothelioma (MARS 2)", "General Thoracic"),
    ("chest_wall_diaphragm", "39. Chest wall deformities, tumours, TOS and diaphragm", "General Thoracic"),
    ("trachea_airway", "40. Tracheal stenosis, airway tumours and TEF", "General Thoracic"),
    ("mediastinum_thymoma", "41. Mediastinal masses, thymoma and myasthenia gravis", "General Thoracic"),
    ("oesophagus", "42. Oesophageal cancer, benign motility/GORD and perforation", "General Thoracic"),
    ("thoracic_trauma_ssrf", "43. Blunt and penetrating thoracic trauma, flail chest and SSRF", "General Thoracic"),
    ("embryology_duct", "44. Cardiac embryology, segmental analysis and duct-dependent emergencies", "Congenital"),
    ("palliative_shunts", "45. Palliative congenital procedures: mBTS, PA banding, Glenn and Fontan", "Congenital"),
    ("shunt_lesions", "46. Left-to-right shunt lesions: PDA, ASD/PAPVR, VSD and AVSD", "Congenital"),
    ("coarctation_iaa_rings", "47. Coarctation of the aorta, interrupted aortic arch and vascular rings", "Congenital"),
    ("tof_pavsd", "48. Tetralogy of Fallot and pulmonary atresia with VSD", "Congenital"),
    ("tga_aso", "49. Transposition of the great arteries and arterial switch operation", "Congenital"),
    ("tapvc_truncus", "50. TAPVC and truncus arteriosus", "Congenital"),
    ("hlhs_norwood", "51. HLHS, Norwood/Sano and single-ventricle palliation", "Congenital"),
    ("lvoto_ebstein_coronaries", "52. Congenital LVOTO (Ross/Konno), Ebstein and anomalous coronaries", "Congenital"),
    ("achd_picu", "53. Adult Congenital Heart Disease (2025 ACHD) and PICU", "Congenital"),
    ("iscp2026", "54. ISCP August 2026 Professional Practice: Genomics, Informatics, Outcomes & Sustainability", "ISCP 2026"),
]

# Corrections found by auditing the chapters against the revision site and primary sources (21 Nov 2026).
# (chapter id, what the chapter says, what to use instead, how it was checked)
ERRATA = [
    ("af_arrhythmia", "Concomitant ablation at mitral surgery is Class I, C (ESC/EACTS 2024)",
     "Class I, level A; non-mitral cardiac surgery IIa B", "ESC 2024 AF guideline (class from ESC Essential Messages; level from a published summary); STS 2017 also I A"),
    ("tricuspid_valve", "Concomitant repair for mild-to-moderate secondary TR with a dilated annulus is IIa",
     "2025 ESC/EACTS: severe I B; moderate IIa B; mild with annulus >=40 mm or >21 mm/m2 IIb B", "2025 ESC/EACTS valve guideline, via published summaries"),
    ("palliative_shunts", "Trusler's rule for single ventricle: 24 mm + 1 mm/kg",
     "20 mm + 1 mm/kg non-mixing; 24 mm + 1 mm/kg mixing; 22 mm + 1 mm/kg single ventricle for Fontan", "StatPearls, Pulmonary Artery Banding"),
    ("lvoto_ebstein_coronaries", "Subaortic membrane: operate at peak/mean >=50/30 mmHg",
     "2025 ACC/AHA ACHD uses a peak gradient >=50 mmHg for subaortic stenosis (mean >=40 mmHg is for valvar AS)", "2025 ACC/AHA ACHD guideline text"),
    ("cardiac_icu_bojar", "Stop DOACs 36-48 h before surgery",
     "EACTS 2024 recommendation: 48-96 h before elective open-heart surgery by drug and renal function, no routine bridging (I B); 36-48 h is the body-text figure for normal renal function only", "2024 EACTS perioperative medication guideline, Table 7"),
    ("cardiac_icu_bojar", "Adrenaline in arrest after cardiac surgery: 50-100 mcg aliquots",
     "Routine 1 mg is avoided; EACTS (Dunning 2009) allows smaller 100-300 mcg boluses peri-arrest", "EACTS 2009 resuscitation guideline, via search extract"),
    ("cpb_pccs", "Post-cardiotomy cardiogenic shock incidence 0.5-1.5%",
     "Under 4% (2020 EACTS/ELSO/STS/AATS consensus; 2024 EACTS patient blood management guideline)", "consensus document, via search extract"),
    ("cpb_pccs", "Protamine 1 mg per 100 IU heparin",
     "2024 guideline: protamine-to-heparin ratio below 1.0 to avoid overdose (I B)", "revision site, checked against the guideline"),
    ("cad_cabg", "Left main PCI with SYNTAX >=33 is Class III (2024 ESC CCS)",
     "Class III B was the 2018 recommendation; the 2024 guideline replaced it (IIb B statement for high surgical risk)", "revision site, checked against the guideline"),
    ("primary_mr", "Early repair is recommended when any one of AF, sPAP >50 mmHg or LAVI >=60 mL/m2 is present",
     "Class I B only with at least three of the four markers; AF or PH alone IIa B; LA dilatation alone IIa B", "revision site, checked against the 2025 guideline"),
    ("aortic_regurgitation", "Earlier surgery at LVESDi >20-22 mm/m2 or LVEF <=55% (IIb/IIa)",
     "2025: IIb B at LVESDi >22 mm/m2, or LVESVi >45 mL/m2, or LVEF <=55%; >20 mm/m2 was the 2021 threshold", "revision site, checked against the guideline"),
    ("endoleak", "Treat type II/V endoleak with sac growth >=5 mm",
     "Sac growth >=10 mm (EACTS/STS and ESC 2024, IIa C)", "revision site, checked against the guidelines"),
    ("infection", "Early/late graft infection cut-off 4 months; 4-6 weeks IV antibiotics",
     "Early infection <=3 months (ACC/AHA); antibiotics at least 6 weeks", "revision site, checked against the guidelines"),
    ("shunt_lesions", "Close VSD at PVR <3-5 WU",
     "2025 ACC/AHA: Class 1 at PVR <=2 WU; 2a at >2 to <5 WU; 2b at 5-8 WU if it falls on PAH therapy", "revision site, checked against the 2025 ACHD guideline"),
    ("lvoto_ebstein_coronaries", "Class I EP study before Ebstein surgery; Class I surgery for AAOCA with high-risk anatomy",
     "EP study and ablation before tricuspid surgery is 2a; AAOCA: Class 1 if symptomatic or ischaemia, asymptomatic high-risk anatomy 2a", "revision site, checked against the 2025 ACHD guideline"),
    ("coarctation_iaa_rings", "Covered stent is first-line for adult coarctation",
     "Surgery or stent; stents carry more reintervention; individualise", "revision site, checked against the 2025 ACHD guideline"),
    ("achd_picu", "ACHD specialist care for non-cardiac surgery in IC-D, IIA-D, IIIA-D",
     "Post-procedure care IC-D, IIB-D, IIIA-D; anaesthesia IC-D, IIC-D, IIIA-D (IIA-D applies to cardiac procedures)", "revision site, checked against the 2025 ACHD guideline"),
    ("pe_cteph", "UCSD levels: II lobar/segmental, III distal segmental",
     "UCSD levels (Madani 2012): I main PA (IC complete occlusion), II lobar, III segmental, IV subsegmental", "published definitions"),
]

FALLBACK_CH54 = """<article id="new-iscp2026">
<h2>Chapter 54: ISCP August 2026 Professional Practice: Genomics, Clinical Informatics, Surgical Outcomes (CiP 7), Statistics and Sustainability</h2>
<p><small>ISCP Version 2 (August 2026) Professional Practice · Full-length educational draft · independent clinical review pending</small></p>
<section><h3>1. Genomics in Cardiothoracic Surgery (ISCP August 2026 Section 3.5.1)</h3>
<p>Integrate genomic testing across four domains: HTAD panels (FBN1, TGFBR1/2, SMAD3, COL3A1, ACTA2) governing prophylactic aortic thresholds and family screening; NSCLC molecular profiling (EGFR/ADAURA, ALK/ALINA, PD-L1/CheckMate 816) governing targeted adjuvant therapy vs chemo-immunotherapy; cardiomyopathy panels (MYH7/MYBPC3); and congenital genetics (22q11.2 DiGeorge—irradiated blood products &amp; calcium, 7q11.23 Williams, Trisomy 21, Turner 45,X). Obtain documented consent under the NHS Genomic Medicine Service and never operate solely on a VUS.</p></section>
<section><h3>2. Clinical Informatics, Surgical Outcomes (CiP 7) and Governance</h3>
<p>UK cardiac outcomes are submitted to NICOR/NACSA and thoracic outcomes to NLCA/SCTS using Risk-Adjusted Mortality Rate (RAMR via EuroSCORE II / Thoracoscore). Monitor performance with funnel plots (95% 2 SD alert; 99.8% 3 SD alarm) and real-time VLAD/CUSUM charts. Uphold WHO Surgical Safety Checklists, Never Event reporting (wrong-site surgery/drain, retained swab), PSIRF root-cause analysis, and statutory Duty of Candour (prompt, honest apology and written explanation after moderate/severe harm—not an admission of legal liability).</p></section>
<section><h3>3. Research Statistics and Sustainability</h3>
<p>Master ARR, RRR, NNT (1/ARR), Hazard Ratios, SnNout/SpPin, and non-inferiority trials (always verify BOTH intention-to-treat and per-protocol analyses so crossovers do not falsely suggest non-inferiority). Under ISCP August 2026 Sustainability (Section 3.5.1), eliminate desflurane/N2O in favour of TIVA/low-flow sevoflurane, rationalise single-use packs, and adopt safe ERAS/virtual pathways without compromising sterility or patient safety.</p></section>
</article>"""


def extract_element_by_id(html: str, tag: str, elem_id: str) -> str | None:
    """Balanced-tag extractor for <tag ... id="elem_id" ...>...</tag>."""
    pat = re.compile(rf'<{tag}\b[^>]*\bid=["\']{re.escape(elem_id)}["\'][^>]*>', re.I)
    m = pat.search(html)
    if not m:
        return None
    start = m.start()
    pos = m.end()
    depth = 1
    token = re.compile(rf'<(/?){tag}\b[^>]*>', re.I)
    for t in token.finditer(html, pos):
        if t.group(1) == '/':
            depth -= 1
            if depth == 0:
                return html[start:t.end()]
        else:
            if not t.group(0).rstrip().endswith('/>'):
                depth += 1
    return None


ID_RE = re.compile(r'(\sid=)(["\'])([^"\']+)\2')
HREF_RE = re.compile(r'(\shref=)(["\'])#([^"\']+)\2')
IDREF_RE = re.compile(r'(\s(?:for|aria-controls|aria-labelledby|aria-describedby)=)(["\'])([^"\']+)\2')


def ids_in(fragment: str) -> set:
    return {m.group(3) for m in ID_RE.finditer(fragment)}


def scope_ids(fragment: str, prefix: str, ref_prefix: str | None = None, ref_ids: set | None = None) -> str:
    """Prefix every id and in-page link so fragments from different files cannot collide.

    Links that point at an id outside this fragment but inside the source file's
    reference list (ref_ids) are rewritten to the reference block's prefix, so
    citation links like href="#ref3" keep working after the merge.
    """
    own = ids_in(fragment)
    ref_ids = ref_ids or set()

    def target(i: str) -> str:
        if i not in own and i in ref_ids and ref_prefix:
            return ref_prefix + i
        return prefix + i

    fragment = ID_RE.sub(lambda m: f'{m.group(1)}{m.group(2)}{prefix}{m.group(3)}{m.group(2)}', fragment)
    fragment = HREF_RE.sub(lambda m: f'{m.group(1)}{m.group(2)}#{target(m.group(3))}{m.group(2)}', fragment)
    fragment = IDREF_RE.sub(lambda m: m.group(1) + m.group(2) + " ".join(target(x) for x in m.group(3).split()) + m.group(2), fragment)
    return fragment


def is_consolidated_base(html: str) -> bool:
    return (
        bool(re.search(r'<title>[^<]*FRCS Atlas[^<]*Consolidated reconstruction', html, re.I))
        and len(re.findall(r'<article\b[^>]*\bid="s\d+"', html)) > 0
        and 'id="data"' in html
        and 'id="history"' in html
    )


def scan_folder(root: Path):
    base_file = None
    base_html = None
    chapters = {}
    chapter_ref = {}   # chapter id -> key of the reference list from the same source file
    refs = []
    seen_ref_keys = set()
    short_src = {}
    short_ids = []

    html_files = sorted(
        p for p in root.rglob("*.html")
        if "__MACOSX" not in p.parts and not p.name.startswith("._")
    )
    print(f"Scanning {len(html_files)} HTML file(s) in: {root.resolve()}")

    for p in html_files:
        if p.name.startswith("FRCS-EBCTS-ISCP2026-"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  [skip] {p.name}: {e}")
            continue

        if is_consolidated_base(text):
            if base_file is None or ("2" not in p.name and "2" in base_file.name):
                base_file, base_html = p, text
            continue

        title_m = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
        title = title_m.group(1) if title_m else ""

        def grab(cid, tag, eid, rkey=None):
            if cid not in chapters:
                el = extract_element_by_id(text, tag, eid)
                if el:
                    chapters[cid] = el
                    if rkey:
                        chapter_ref[cid] = rkey

        def grab_ref(rkey, *candidates):
            """candidates: (tag, id) pairs; the first one present is used."""
            if rkey in seen_ref_keys:
                return
            for tag, eid in candidates:
                el = extract_element_by_id(text, tag, eid)
                if el:
                    seen_ref_keys.add(rkey)
                    refs.append((rkey, el))
                    return

        if 'id="new-root"' in text and "valve-sparing" in text.lower():
            grab("s1", "article", "new-root")
        if re.search(r'Aortic Dissection Chapters', title, re.I):
            grab("s3", "article", "chapter1", "dis")
            grab("s5", "article", "chapter2", "dis")
            grab_ref("dis", ("section", "references"), ("aside", "references"))
        if re.search(r'Ascending aorta and arch', title, re.I):
            grab("s2", "article", "chapter1", "arch")
            grab("s4", "article", "chapter2", "arch")
            grab_ref("arch", ("section", "references"), ("aside", "references"))
        if re.search(r'Descending and thoracoabdominal aorta', title, re.I):
            grab("s7", "article", "c1", "distal")
            grab("s8", "article", "c2", "distal")
            grab_ref("distal", ("section", "references"), ("aside", "references"))
        if re.search(r'Main app aortic update', title, re.I):
            grab("s6", "article", "new-s6")
            grab("s9", "article", "new-s9")
        if re.search(r'14 Chapters Total', title, re.I):
            for k in ["htad", "endoleak", "infection", "btai", "aortic_stenosis"]:
                grab(k, "article", f"new-{k}", "m14")
            grab_ref("m14", ("aside", "new-references"))
        if re.search(r'24 Chapters Total', title, re.I):
            for k in ["aortic_regurgitation", "primary_mr", "secondary_mr_ms", "tricuspid_valve", "prosthetic_redo", "endocarditis", "cad_cabg", "mech_mi", "cpb_pccs", "lvad_transplant"]:
                grab(k, "article", f"new-{k}", "m24")
            grab_ref("m24", ("aside", "ac-references"))
        if re.search(r'31 Chapters Total', title, re.I):
            for k in ["cardiac_anatomy_phys", "af_arrhythmia", "pericardial_disease", "tumours_hocm_lv", "pe_cteph", "carotid_trauma", "cardiac_icu_bojar"]:
                grab(k, "article", f"new-{k}", "m31")
            grab_ref("m31", ("aside", "ac2-references"))
        if re.search(r'All 53 Chapters Complete', title, re.I):
            for k in ["thoracic_anatomy_pft", "lung_cancer_staging", "nsclc_surgery", "pneumonectomy_bpf_carcinoid", "lvrs_infections_lungtx", "pleural_bts2023", "mesothelioma", "chest_wall_diaphragm", "trachea_airway", "mediastinum_thymoma", "oesophagus", "thoracic_trauma_ssrf", "embryology_duct", "palliative_shunts", "shunt_lesions", "coarctation_iaa_rings", "tof_pavsd", "tga_aso", "tapvc_truncus", "hlhs_norwood", "lvoto_ebstein_coronaries", "achd_picu"]:
                grab(k, "article", f"new-{k}", "m53")
            grab_ref("m53", ("aside", "tc-references"))
        if re.search(r'Chapter 54', title, re.I):
            grab("iscp2026", "article", "new-iscp2026", "m54")
            grab_ref("m54", ("aside", "ch54-refs"))
        if re.search(r'Aortic and Thoracic evidence build', title, re.I):
            # Short-form versions; used for chapters 6 and 9 only if no full-length file supplied them.
            short_src[("s6", "c6")] = text
            short_src[("s9", "c22")] = text

    for (cid, eid), text in short_src.items():
        if cid not in chapters:
            el = extract_element_by_id(text, "article", eid)
            if el:
                note = ('<p class="short-note"><small>Short-form version (from the "Aortic and Thoracic '
                        'evidence build" file) — no full-length chapter was found for this topic.</small></p>')
                el = re.sub(r'<a\s+href="#index">[^<]*</a>', '', el)  # back-link to a page that is not merged
                chapters[cid] = re.sub(r'(<article\b[^>]*>)', r'\1' + note, el, count=1)
                short_ids.append(cid)
                print(f"  [info] Chapter {cid}: using short-form version (no full-length source found).")

    if "iscp2026" not in chapters:
        chapters["iscp2026"] = FALLBACK_CH54
        short_ids.append("iscp2026")
        print("  [info] Included built-in Chapter 54 (ISCP August 2026 Professional Practice).")

    return base_file, base_html, chapters, chapter_ref, refs, short_ids


def scope_chapter(cid: str, html: str, prefix: str, ref_prefix_fmt: str, chapter_ref: dict, refs: list) -> str:
    rkey = chapter_ref.get(cid)
    ref_el = next((el for k, el in refs if k == rkey), None)
    if ref_el is None:
        return scope_ids(html, prefix)
    return scope_ids(html, prefix, ref_prefix_fmt.format(rkey), ids_in(ref_el))


def errata_html(chapters: dict, link_prefix: str) -> str:
    titles = {cid: t for cid, t, _ in MANIFEST}
    rows = []
    for cid, says, use, checked in ERRATA:
        if cid not in chapters:
            continue
        rows.append(f'<tr><td><a href="#{link_prefix}{cid}">{H(titles[cid].split(". ", 1)[0])}</a></td>'
                    f'<td>{H(says)}</td><td><strong>{H(use)}</strong></td><td><small>{H(checked)}</small></td></tr>')
    return ('<section id="atlas-errata"><h2>Corrections to these chapters (checked 21 November 2026)</h2>'
            '<p>Where a chapter below disagrees with the current guideline, use the right-hand column. '
            'The chapters are educational drafts and are not otherwise altered.</p>'
            '<div style="overflow-x:auto"><table><thead><tr><th>Ch</th><th>Chapter says</th><th>Use instead</th><th>Checked against</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div></section>')


def write_standalone(out_path: Path, chapters: dict, chapter_ref: dict, refs: list):
    css = (
        "body{margin:0;font:16.5px/1.65 system-ui;color:#173845;background:#eef5f6;display:grid;grid-template-columns:300px 1fr;min-height:100vh}"
        "aside.nav{background:#143a4b;color:#fff;padding:16px;overflow-y:auto;position:sticky;top:0;height:100vh;box-sizing:border-box}"
        "aside.nav input,aside.nav select{width:100%;padding:7px;margin:5px 0;border-radius:6px;border:0;box-sizing:border-box}"
        "aside.nav a{display:block;color:#c3f4ea;text-decoration:none;font-size:.86em;padding:4px 6px;border-radius:5px}"
        "aside.nav a:hover{background:#1f5268}"
        "main{padding:22px;max-width:940px}"
        "article,section,aside.refs{background:#fff;padding:22px;border-radius:12px;margin:0 0 18px}"
        "figure,details{background:#e3f3f0;padding:10px;border-radius:8px}summary{cursor:pointer;font-weight:600}"
        ".flow span{display:inline-block;padding:5px 9px;background:#d6ece8;border-radius:6px;margin:3px}"
        "table{width:100%;border-collapse:collapse}th,td{border:1px solid #c6dcdd;padding:7px}"
        "@media(max-width:850px){body{grid-template-columns:1fr}aside.nav{position:static;height:auto}}"
    )
    toc_links, body_parts = [], []
    for cid, title, dom in MANIFEST:
        if cid not in chapters:
            continue
        scoped = scope_chapter(cid, chapters[cid], f"ch-{cid}-", "ref-{}-", chapter_ref, refs)
        body_parts.append(f'<div class="chap-wrap" id="chap-{cid}" data-domain="{H(dom)}">{scoped}</div>')
        toc_links.append(f'<a href="#chap-{cid}" data-domain="{H(dom)}">{H(title)}</a>')
    ref_parts = [f'<div class="refs">{scope_ids(el, f"ref-{k}-")}</div>' for k, el in refs]
    search_js = (
        'const q=document.querySelector("#q"),dom=document.querySelector("#dom"),'
        'wraps=[...document.querySelectorAll(".chap-wrap")],links=[...document.querySelectorAll("#toc a")];'
        'function filt(){const t=q.value.trim().toLowerCase(),d=dom.value;'
        'wraps.forEach((w,i)=>{const ok=(!d||w.dataset.domain===d)&&(!t||w.textContent.toLowerCase().includes(t));'
        'w.style.display=ok?"":"none";if(links[i])links[i].style.display=ok?"":"none";})}'
        'q.oninput=filt;dom.onchange=filt;'
    )
    html = (
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>FRCS (CTh) &amp; EBCTS 2026 — Complete Standalone Textbook ({len(chapters)} Chapters)</title>'
        f'<style>{css}</style></head><body>'
        f'<aside class="nav"><h2 style="margin-top:0;font-size:1.15em">FRCS / EBCTS Atlas</h2>'
        f'<p style="font-size:.85em;opacity:.85">{len(chapters)} of 54 chapters packaged</p>'
        f'<input id="q" placeholder="Search all chapters…">'
        f'<select id="dom"><option value="">All Domains</option><option>Aortic</option><option>Adult Cardiac</option><option>General Thoracic</option><option>Congenital</option><option>ISCP 2026</option></select>'
        f'<div id="toc">{"".join(toc_links)}</div></aside>'
        f'<main><section><h1>FRCS (CTh) &amp; EBCTS 2026 Complete Textbook</h1>'
        f'<p>Offline single-file HTML edition containing <strong>{len(chapters)} of 54</strong> full chapters. Independent clinical review pending; not an institutional protocol.</p></section>'
        f'{errata_html(chapters, "chap-")}'
        f'{"".join(body_parts)}{"".join(ref_parts)}</main>'
        f'<script>{search_js}</script></body></html>'
    )
    out_path.write_text(html, encoding="utf-8")


def write_consolidated(out_path: Path, base_html: str, chapters: dict, chapter_ref: dict, refs: list):
    styles = (
        "<style>"
        "[data-atlas-import]{margin-top:24px;border-top:2px solid #9ec9c5;padding-top:14px}"
        "[data-atlas-import] figure,[data-atlas-import] details{background:#e3f3f0;padding:10px;border-radius:8px}"
        "[data-atlas-import] .flow span{display:inline-block;padding:5px 9px;background:#d6ece8;border-radius:6px;margin:3px}"
        "</style>"
    )
    base_count = len(re.findall(r'<article\b[^>]*\bid="s\d+"', base_html))
    toc_items = []
    blocks = []
    for cid, title, _ in MANIFEST:
        if cid in chapters:
            toc_items.append(f'<li><a href="#atlas-py-{cid}">{H(title)}</a></li>')
            scoped = scope_chapter(cid, chapters[cid], f"py-{cid}-", "pyref-{}-", chapter_ref, refs)
            blocks.append(f'<div id="atlas-py-{cid}" data-atlas-import="{cid}">{scoped}</div>')
        else:
            toc_items.append(f'<li>{H(title)} — not found in folder</li>')
    ref_blocks = [f'<div data-atlas-refs="{k}">{scope_ids(el, f"pyref-{k}-")}</div>' for k, el in refs]
    banner = (
        f'<section id="atlas-py-master-index" style="background:#fff;padding:20px;margin:16px auto;max-width:1000px;border-radius:12px">'
        f'<h2>FRCS (CTh) &amp; EBCTS 2026 Complete Atlas ({len(chapters)} of 54 chapters merged)</h2>'
        f'<p>All {base_count} original study sections, source library, gallery, revision tools and scripts are preserved verbatim below.</p>'
        f'<ol>{"".join(toc_items)}</ol>{errata_html(chapters, "atlas-py-")}</section>'
    )
    extra_section = (
        f'<section id="atlas-py-expanded-chapters" style="background:#fff;padding:22px;margin:16px auto;max-width:1000px;border-radius:12px">'
        f'<h2>Expanded Full-Length Textbook Chapters ({len(chapters)} Chapters)</h2>'
        f'{"".join(blocks)}{"".join(ref_blocks)}</section>'
    )
    merged = base_html.replace("</head>", styles + "\n</head>", 1)
    merged = merged.replace("<main", banner + "\n<main", 1)
    merged = merged.replace("</main>", "\n" + extra_section + "\n</main>", 1)

    # Verify original 71 sections and data script remain intact
    assert len(re.findall(r'<article\b[^>]*\bid="s\d+"', merged)) == base_count, "Integrity error: original article count changed!"
    assert 'id="data"' in merged and 'id="history"' in merged, "Integrity error: core app data/history missing!"
    out_path.write_text(merged, encoding="utf-8")


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    base_file, base_html, chapters, chapter_ref, refs, short_ids = scan_folder(root)
    missing = [title for cid, title, _ in MANIFEST if cid not in chapters]

    print(f"\nPackaged {len(chapters)} / 54 chapters "
          f"({len(chapters) - len(short_ids)} full-length, {len(short_ids)} short-form or built-in: {', '.join(short_ids) or 'none'}).")
    if missing:
        print("Missing chapters (add their HTML file to this folder and re-run if needed):")
        for m in missing:
            print("  -", m)

    standalone_out = root / "FRCS-EBCTS-ISCP2026-Standalone-54-Chapters.html"
    write_standalone(standalone_out, chapters, chapter_ref, refs)
    print(f"\n[OK] Wrote standalone app:   {standalone_out.name} ({standalone_out.stat().st_size:,} bytes)")

    if len(chapters) < 54:
        print(f"[Note] Output file names say '54-Chapters' but only {len(chapters)} were packaged (see list above).")
    if base_html:
        cons_out = root / "FRCS-EBCTS-ISCP2026-Consolidated-54-Chapters.html"
        write_consolidated(cons_out, base_html, chapters, chapter_ref, refs)
        print(f"[OK] Wrote consolidated app: {cons_out.name} ({cons_out.stat().st_size:,} bytes)")
        print(f"     Base file preserved verbatim: {base_file.name}")
    else:
        print("[Note] FRCS-Atlas-Consolidated.html not found in this folder — only standalone app was written.")


if __name__ == "__main__":
    main()
