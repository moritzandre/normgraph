# 04_specs / C-01 — Data spike: Open Legal Data → segmentation → citation inventory

Status: **done** · Date: 2026-06-11 · Lane: CODE · Feeds: DD-001 (evidence), DD-002/003/004/010 (context), C-03 (spec seeds)

## What was done
Pulled one current civil decision from Open Legal Data (OLD), segmented it into sections, and extracted a norm-citation surface-form inventory with throwaway stdlib-Python heuristics. No architecture commitments made (DD-001/002/005 open); segmentation labels here are heuristics, not the DD-003 trajectory schema.

Sample: **LG Nürnberg-Fürth, 8 O 4860/25, Endurteil v. 21.05.2026** (OLD case id 521203, slug `lg-nurnberg-furth-2026-05-21-8-o-486025`) — PKV-Fall, Erstattung „Abnehmspritze" (§ 192 VVG, MB/KK), Klage abgewiesen. Convenience sample; outside the DD-004 candidate slices, chosen for format study.

## Findings
- **F1 — Source is alive and near-live.** OLD ingests current decisions (front page showed May-2026 items; sampled judgment published 21.05., online within ~3 weeks). Access paths: per-case JSON API (`/api/cases/{id}/`), filterable web UI (Gerichtsbarkeit, Instanz, Datum), bulk dumps at `static.openlegaldata.io/dumps/de/` **plus a separate pre-extracted citations/references dump** (`…/dumps/de/refs/`).
- **F2 — Access constraints.** `robots.txt` disallows `/api/` for crawlers, so assistant-side fetching in claude.ai sessions can only use the public case pages; the claude.ai code container has no network egress at all. Consequence: corpus work (API/dumps) runs in the local pipeline; sessions operate on hand-carried samples. The API itself is open for direct clients (curl/SDK, no auth for reads).
- **F3 — Section markers vary by court/portal.** This Bavarian LG judgment uses Tenor / Tatbestand / **„Gründe"** — not „Entscheidungsgründe". Anomalies found: an embedded **Streitwert-Beschluss inside the Tenor block**, and anonymization placeholders („…", „...") in names/dates. Internal Gliederung of Gründe is typographically recoverable: roman (I., II.), arabic (1.–3.), letters (a., b.) — three levels in a 1,300-word judgment. § 313a-ZPO judgments (no Tatbestand) not observed (n=1) but remain a known case.
- **F4 — Citation inventory** (7 norm chains, all in Gründe):

| Phänomen | Beispiel (verbatim) | n | Note → DD-001.5 / C-03 |
|---|---|---|---|
| Volle Normzitate mit Abs. | § 192 Abs. 1 VVG · § 91 Abs. 1 ZPO | 3 | baseline form |
| Satz-Enumeration in einem Zitat | § 709 S. 1 und 2 ZPO | 1 | one citation, two Sätze |
| AGB/Musterbedingungen statute-style | § 1 Abs. 2 S. 1 MB/KK | 3 | non-statute „norm" — node type question |
| Kommentar-Reihenfolge (Gesetz vor §) | VVG § 192 Rn. 23 · MB/KK § 1 Rn. 94 | 2 | literature context, Rn.-suffix |
| Anaphorische Literaturreferenz | a.a.O. | 3 | needs resolution if literature modeled |
| Aktenzeichen (case refs) | IV ZR 278/01 · 8 U 935/14 | 4 | edge-provenance material (DD-002) |
| Zeitschriftenfundstellen | NJW 2003, 1596 · NJOZ 2016, 626 | 4 | multi-page variant exists (3074, 3075) |
| **Not observed (n=1, expected per DD-001):** ff.-Ranges, i.V.m., analog, a.F./n.F., römische Absätze (§ 433 II 1), §§-Plural, implizite Gesetzesangabe | — | 0 | LG wrote full-form throughout; BGH style differs → stratify C-03 dev set by court level |

- **F5 — OLD's own reference extraction is useful but incomplete.** OLD links per case only statutes resolvable in its law DB (here: VVG § 192, ZPO § 91, ZPO § 709 — all three also found by our extractor). It **missed** the MB/KK clause citations, both commentary-order citations, and the NJOZ Fundstelle. OLD also exposes a case-to-case citation network („Zitiert von"). Consequence: refs dump = weak supervision / cross-check signal, not a replacement for C-03.
- **F6 — Norm citations cluster by function.** All norms sit in Gründe; within it, material norms in part I. (Begründetheit), procedural Nebenentscheidungen (§ 91, § 709 ZPO) in part II. Tenor and Tatbestand cite nothing here. → Trajectory extraction (DD-003) should split the Begründetheits-Pfad from Nebenentscheidungen; the roman top-level Gliederung is a cheap split signal.
- **F7 — New canonicalization targets** beyond DD-001's list: AGB-type works cited statute-style (MB/KK, AVB — function as quasi-Anspruchsgrundlagen in PKV; touches DD-001 option D: non-statute nodes), commentary-order `GESETZ § N Rn. M`, anaphora `a.a.O.`, multi-page Fundstellen.

## Implications (observations, no decisions)
- **DD-001:** inventory delivered (partial — full-form-biased, n=1); adds sub-question: are Musterbedingungen/AVB clauses nodes? → option-D discussion.
- **DD-002:** OLD's „Zitiert von" network = candidate provenance source for learned edges.
- **DD-003:** Gliederungs-Marker (I./1./a.) as station anchors; Nebenentscheidungen filter.
- **DD-004:** insurance-law cases drag contract terms (AVB) into the norm layer — mild argument for statute-dense slices (Kaufrecht/Delikt).
- **DD-010:** decision body from OLD public page, § 5 UrhG unproblematic; OLD's added platform data (refs, network) has its own licensing — verify on OLD imprint/licensing page before bulk reuse.
- **C-03 seeds:** token-vocabulary chain matcher (anchor `§/§§/Art.` + bounded token grammar + trailing-connector strip) found 7/7 chains incl. all forms OLD missed; known gaps per F4; free eval harness: compare against OLD refs dump per case.

## Limitations
n=1; processed the markdown rendering of the case page (local pipeline gets raw HTML `content` with `h2` headings via API/dump — adapt marker logic, drop hand-transcription step entirely); regex is spike-grade, not the C-03 parser.

## Artifacts (session outputs, kept locally)
`c01_spike.py` (segmentation + inventory, stdlib), `sample_case_521203.md` (decision body, verbatim capture), `sample_case_521203.meta.json` (provenance + OLD's own refs as comparison target), `c01_output.json` (full machine-readable report).

## Changelog
- 2026-06-11 · C-01 executed in-session (claude.ai container, offline; ingress via assistant web fetch).
- 2026-06-12 · Next CODE items renumbered: **C-02 — repo bootstrap** (local repository scaffold + CLAUDE.md contract + Claude Code handoff prompt; executed via Claude Code in the user's IDE, since claude.ai sessions have no access to the local filesystem). **C-03 — citation parser** (proper grammar + tests + OLD-refs comparison harness), after DD-001 fixes canonicalization targets.
