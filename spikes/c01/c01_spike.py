#!/usr/bin/env python3
"""C-01 data spike — NormGraph.
Segments one Open Legal Data decision (markdown rendering of the case page) into
Tenor / Tatbestand / (Entscheidungs-)Gründe and builds a citation surface-form inventory.

THROWAWAY SPIKE CODE: heuristics only. Not the DD-003 trajectory schema, not the
C-02 citation parser. No architecture commitments (DD-001/002/005 are open).
Local pipeline note: via API/dump the content arrives as raw HTML (h2 section
headings); here we parse the markdown rendering — marker logic covers both styles.
"""
import json
import re
import sys
from collections import Counter

# ---------- text normalization ----------

MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")  # [text](#refs) -> text


def normalize(text: str) -> str:
    text = MD_LINK.sub(r"\1", text)
    text = text.replace("\u00a0", " ")
    return text


# ---------- segmentation ----------

SECTION_MARKERS = {
    "tenor": "tenor",
    "tatbestand": "tatbestand",
    "entscheidungsgründe": "entscheidungsgründe",
    "entscheidungsgruende": "entscheidungsgründe",
    "gründe": "gründe",
    "gruende": "gründe",
    "tatbestand und entscheidungsgründe": "tatbestand und entscheidungsgründe",
    "tatbestand und gründe": "tatbestand und gründe",
}

ROMAN = re.compile(r"^[IVX]{1,4}\.$")
ARABIC = re.compile(r"^\d{1,2}\.(\s|$)")
LETTER = re.compile(r"^[a-z][.)](\s|$)")
EMBEDDED = {"beschluss", "beschluß"}  # e.g. Streitwert-Beschluss embedded in the Tenor block


def marker_of(line: str):
    """Canonical section name if the line is a section marker, else None.
    Accepts markdown headings (## Tenor) and bare short lines (Tenor / TENOR / Tenor:)."""
    t = re.sub(r"^#{1,6}\s*", "", line.strip())
    t = t.rstrip(":").strip()
    if len(t) > 45:
        return None
    return SECTION_MARKERS.get(t.lower())


def segment(text: str):
    sections, anomalies = {"kopf": []}, []
    current = "kopf"
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            continue
        m = marker_of(line)
        if m:
            if m in sections:
                anomalies.append(f"duplicate marker '{m}'")
            current = m
            sections.setdefault(current, [])
            continue
        if line.lower().rstrip(":") in EMBEDDED:
            anomalies.append(f"embedded marker '{line}' inside section '{current}'")
        sections[current].append(line)
    return sections, anomalies


def substructure(blocks):
    return {
        "roman": sum(1 for b in blocks if ROMAN.match(b)),
        "arabic_numbered": sum(1 for b in blocks if ARABIC.match(b)),
        "letter_points": sum(1 for b in blocks if LETTER.match(b)),
    }


# ---------- norm citation extraction ----------

KNOWN_LAWS = (
    "BGB ZPO StGB StPO HGB GG EGBGB EGZPO VVG VAG UWG UrhG MarkenG PatG InsO "
    "GKG FamGKG RVG JVEG ZVG GBO WEG StVG StVO StVZO PflVG ProdHaftG AMG AGG "
    "TKG BDSG DSGVO GmbHG AktG ArbGG KSchG BUrlG TzBfG BetrVG TVG EFZG GewO "
    "BauGB VwGO VwVfG SGG FGO AO EStG UStG FamFG GVG BeurkG BNotO BRAO RDG "
    "EMRK GRCh AEUV EUV"
).split()
SLASH_LAWS = ["MB/KK", "MB/KT", "MB/PPV", "VOB/B", "VOB/A", "AVB"]  # AGB-type works cited statute-style
LAW_ALT = "|".join(map(re.escape, sorted(KNOWN_LAWS + SLASH_LAWS, key=len, reverse=True)))
GENERIC_LAW = r"[A-ZÄÖÜ][A-Za-zÄÖÜäöüß]{1,13}(?:G|O|VO|GB)"
LAW_TOKEN = rf"(?:{LAW_ALT}|{GENERIC_LAW})"

TOKEN = rf"""(?:
    §§?
  | Artikel | Art\.
  | \d{{1,4}}[a-z]{{0,2}}\b
  | [IVX]{{1,4}}\b
  | Abs\. | Absatz | Satz | S\. | Nr\. | Nummer | Hs\. | Halbsatz
  | Alt\. | Var\. | lit\. | Buchst\. | Rn\. | Rdnr\.
  | ff\. | f\.
  | a\.\s?F\. | n\.\s?F\.
  | analog | entsprechend
  | i\.\s?V\.\s?m\. | iVm | in\s+Verbindung\s+mit
  | und | bis | ,
  | """ + LAW_TOKEN + r"""
)"""
CHAIN = re.compile(r"(?:§§?|Artikel\b|Art\.)\s*(?:" + TOKEN + r"\s*)+", re.X)
TRAIL = re.compile(r"(?:\s|,|\bund\b|\bbis\b|i\.\s?V\.\s?m\.|iVm|in\s+Verbindung\s+mit)+$")

FEATURE_KEYS = (
    "plural_sign", "range_ff", "ivm", "analog", "old_new_version", "roman_abs",
    "abs_explicit", "satz", "nr", "rn", "enum_und", "implicit_code",
)


def analyze(chain: str, before: str):
    c = re.sub(r"\s+", " ", chain).strip()
    laws_in = re.findall(r"\b(?:" + LAW_ALT + r")\b|\b" + GENERIC_LAW + r"\b", c)
    m_before = re.search(r"(?:" + LAW_ALT + r"|" + GENERIC_LAW + r")(?:\s+[IVX]{1,4})?\s*$", before)
    return {
        "raw": c,
        "n_markers": len(re.findall(r"§{1,2}|Artikel\b|Art\.", c)),
        "plural_sign": "§§" in c,
        "range_ff": bool(re.search(r"\bff?\.", c)),
        "ivm": bool(re.search(r"i\.\s?V\.\s?m\.|iVm|in\s+Verbindung\s+mit", c)),
        "analog": bool(re.search(r"\b(analog|entsprechend)\b", c)),
        "old_new_version": bool(re.search(r"\b[an]\.\s?F\.", c)),
        "roman_abs": bool(re.search(r"§§?\s*\d{1,4}[a-z]?\s+[IVX]{1,4}\b", c)),
        "abs_explicit": bool(re.search(r"\bAbs\.|\bAbsatz\b", c)),
        "satz": bool(re.search(r"\bS\.\s*\d|\bSatz\b", c)),
        "nr": bool(re.search(r"\bNr\.|\bNummer\b", c)),
        "rn": bool(re.search(r"\bRn\.|\bRdnr\.", c)),
        "enum_und": bool(re.search(r"\bund\b|,", c)),
        "laws_in_chain": laws_in,
        "law_before_marker": m_before.group(0).strip() if m_before else None,
        "implicit_code": not laws_in and not m_before,
    }


def extract(sections):
    out = []
    for sec, blocks in sections.items():
        text = " \n".join(blocks)
        for m in CHAIN.finditer(text):
            chain = TRAIL.sub("", m.group(0)).strip()
            before = text[max(0, m.start() - 24):m.start()]
            rec = analyze(chain, before)
            rec["section"] = sec
            out.append(rec)
    return out


# ---------- case-law / journal / anaphora references ----------

AZ = re.compile(r"\b(?:\d{1,2}|[IVX]{1,4})\s?[A-Z][A-Za-z]{0,2}\s?\d{1,5}/\d{2}\b")
JOURNAL = re.compile(r"\b(?:NJW-RR|NJW|NJOZ|MDR|VersR|BGHZ|BGHSt|WM|ZIP|NZM)\s+\d{4},\s*\d+")
AAO = re.compile(r"a\.\s?a\.\s?O\.")
COURT_CITE = re.compile(r"\b(?:BGH|BVerfG|BAG|BSG|BVerwG|BFH|OLG|LG|AG|EuGH)\b")


# ---------- main ----------

def main(md_path, meta_path, out_path):
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)
    with open(md_path, encoding="utf-8") as f:
        text = normalize(f.read())

    sections, anomalies = segment(text)
    sec_stats = {}
    for name, blocks in sections.items():
        joined = " ".join(blocks)
        sec_stats[name] = {"blocks": len(blocks), "chars": len(joined),
                           "words": len(joined.split()), **substructure(blocks)}

    cits = extract(sections)
    inv = Counter()
    for c in cits:
        for k in FEATURE_KEYS:
            if c[k]:
                inv[k] += 1
        if c["law_before_marker"]:
            inv["law_before_marker(commentary_order)"] += 1

    law_pairs = Counter()
    for c in cits:
        law = (c["laws_in_chain"][-1] if c["laws_in_chain"] else c["law_before_marker"]) or "IMPLIZIT"
        num = re.search(r"\d{1,4}[a-z]?", c["raw"])
        law_pairs[f"{law} § {num.group(0) if num else '?'}"] += 1

    per_section = Counter(c["section"] for c in cits)
    full = " \n".join(" \n".join(b) for b in sections.values())
    report = {
        "meta": meta, "anomalies": anomalies, "sections": sec_stats,
        "norm_citations": cits,
        "inventory_feature_counts": dict(inv),
        "norm_law_pairs": dict(law_pairs),
        "citations_per_section": dict(per_section),
        "case_refs": {"aktenzeichen": AZ.findall(full), "journal": JOURNAL.findall(full),
                      "a_a_O": len(AAO.findall(full)),
                      "court_mentions": dict(Counter(COURT_CITE.findall(full)))},
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    print(f"== C-01 spike — {meta['court']} {meta['file_number']} ({meta['type']}, {meta['date']}) ==")
    print("\n-- sections --")
    for n, s in sec_stats.items():
        print(f"  {n:12s} blocks={s['blocks']:3d} words={s['words']:5d} "
              f"roman={s['roman']} num={s['arabic_numbered']} lett={s['letter_points']}")
    for a in anomalies:
        print("  ! " + a)
    print("\n-- norm citations (chain | section | features) --")
    for c in cits:
        flags = [k for k in FEATURE_KEYS if c[k]]
        lb = f" [law-before: {c['law_before_marker']}]" if c["law_before_marker"] else ""
        print(f"  [{c['section'][:5]:5s}] {c['raw']}{lb}  {'|'.join(flags)}")
    print("\n-- feature inventory --")
    for k, v in sorted(inv.items()):
        print(f"  {k:36s} {v}")
    print("\n-- law/§ pairs --")
    for k, v in sorted(law_pairs.items()):
        print(f"  {k:24s} {v}")
    print("\n-- citations per section --", dict(per_section))
    cr = report["case_refs"]
    print(f"\n-- case refs -- Az={cr['aktenzeichen']}")
    print(f"   journals={cr['journal']} | a.a.O. x{cr['a_a_O']} | courts={cr['court_mentions']}")
    print("\n-- OLD's own norm refs (comparison) --", meta["old_extracted_refs"]["norms"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
