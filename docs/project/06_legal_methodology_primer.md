# 06 · Legal-methodology primer — Gutachtenstil, Prüfungsschemata, Anspruchsaufbau

Status: standing reference doc · Lane: ARCH/PAPER (domain background) · Established 2026-06-24
during DD-002, at the user's request, to ground the node/edge model in primary legal-methodology
sources rather than Claude's paraphrase. Lives at `docs/project/06_legal_methodology_primer.md`;
reaches the claude.ai mirror via the connector (inside `docs/project/`).

## 0. Why this file exists
DD-001 (node model) and DD-002 (edge taxonomy) both rest on one structural claim:
**Prüfungsschemata are Tatbestandsmerkmal trees with typed transitions between Einzelnormen.**
The project lead comes from the AI/Tech side, so this file collects the authoritative and
free-to-read sources on how Gutachten and Prüfungsschemata actually work, so design calls are
made against primary doctrine, not a model's summary. It is **not** the DSR method canon
(that is `01_literature_map.md`) and **not** the domain corpus proper (legal-NLP / legal-KG /
LJP literature, still to be built per the `00` brief). It is the **methodology-of-Fallbearbeitung
seed** of that domain review — when the domain corpus is built (Webster & Watson concept matrix;
search documented per vom Brocke et al. 2009), these entries fold into it as the
"computational model of legal reasoning / German legal method" concept column.

## 1. The doctrinal vocabulary our model encodes
The semantic axis of the DD-002 edge taxonomy is standard Zivilrechtsdogmatik. Reading targets,
mapped to our design objects:

- **Three-level Anspruchsprüfung — entstanden / nicht erloschen / durchsetzbar.** The skeleton of
  every Anspruchsaufbau. Our *Einwendung*/*Einrede* edges hang off exactly these levels.
- **Einwendung vs. Einrede.**
  - *Einwendung* = rechtshindernd (claim never arose, e.g. Anfechtung, Formmangel) or
    rechtsvernichtend (claim extinguished, e.g. Erfüllung, Rücktritt). Examined *von Amts wegen*.
  - *Einrede* = rechtshemmend (claim exists but is blocked), only examined if *geltend gemacht*;
    peremptorisch (dauerhaft, e.g. Verjährung § 214) vs. dilatorisch (vorübergehend, e.g. § 320).
  - → our edge types **Einwendung** (negates) and **Einrede** (blocks-on-raising, streitig-
    conditional → couples to DD-007 Subsumtions-Gate). The "only if raised" property is why an
    *Einrede* edge cannot be traversed unconditionally.
- **Anspruchskonkurrenz & Prüfungsreihenfolge.** Claims are examined in a fixed order
  (vertraglich → quasivertraglich → dinglich → deliktisch → bereicherungsrechtlich), because some
  claims bar others (Sperrwirkung des EBV §§ 987 ff. over Delikt/Bereicherung). → our **Anspruchs-
  konkurrenz** edge: a lateral relation governing ordering/Sperrwirkung, not a defeater.
- **Rechtsgrundverweisung vs. Rechtsfolgenverweisung.** A statutory *Verweisung* either pulls in
  the referenced Tatbestand (must be re-prüft → traverse into its Merkmale) or only borrows the
  Rechtsfolge (no Tatbestand re-examination). → the traversal-relevant sub-flag on our
  **Verweisung** edge.
- **Konkretisierung / Legaldefinition.** A Merkmal is defined by another norm (Legaldefinition,
  e.g. »Sache« → § 90 BGB) or by case-law/doctrine (e.g. »medizinische Notwendigkeit«/
  »Erforderlichkeit« → BGH-Vertretbarkeitsmaßstab, the C-01 ratio). → candidate sixth edge type
  **Konkretisierung**; Legaldefinition-half is Einzelnorm-targeted (v1-populatable), doctrine-half
  needs the option-D doctrine nodes DD-001 deferred (coupled to DD-004, open).

## 2. Tier 1 — authoritative, citable anchors (verify against course PDFs before first cite)
1. **Leenen, *Anspruchsaufbau und Gesetz: Wie die Methodik der Fallbearbeitung hilft, das Gesetz
   leichter zu verstehen*, Jura 2011, S. 723–729.** THE article for our core thesis: the structure
   of Fallbearbeitung mirrors the structure of the statute. Load-bearing for DD-001/DD-002.
   (De Gruyter / Jura journal — paywalled; reachable via a university library, e.g. Osnabrück.)
2. **Leenen/Häublein, *BGB Allgemeiner Teil: Rechtsgeschäftslehre*, 3. Aufl. 2021, de Gruyter.**
   Lehrbuch built around Anspruchsaufbau; presents multiple Aufbaumethoden with explicit pros/cons.
   Good for seeing Merkmal-tree structure done rigorously. (Note: the widely-reviewed 2011 edition
   was solo-Leenen; current is Leenen/Häublein.)
3. **Medicus/Petersen, *Bürgerliches Recht — Eine nach Anspruchsgrundlagen geordnete Darstellung
   zur Examensvorbereitung*, 30. Aufl. 2025, Vahlen (ISBN 978-3-8006-7715-3).** The
   Anspruchsgrundlagen-ordered reference; its table of contents *is* a Prüfungsreihenfolge /
   Anspruchskonkurrenz graph (vertraglich → quasivertraglich → dinglich → deliktisch). Directly
   relevant to the **Anspruchskonkurrenz** edge type and to seeding the law-layer's top-level
   ordering. (Paywalled; Vahlen eLibrary via uni.)
4. **Bitter/Rauhut, *Grundzüge zivilrechtlicher Methodik — Schlüssel zu einer gelungenen
   Fallbearbeitung*, JuS 2009.** Compact methodology intro; on the Osnabrück "Methoden der
   Rechtswissenschaft" reading list. Good first read. (JuS / Beck — library access.)

## 3. Tier 2 — open-access university materials (free, read now, structurally explicit)
5. **Bezzenberger (Uni Potsdam), "Allgemeine Lehrmaterialien zum BGB."** Large free collection:
   Subsumtionstechnik & Gutachtenstil basics, "Grundschema für die Prüfung von Ansprüchen,"
   "Prüfungsreihenfolge nach Anspruchsarten," and dozens of per-Anspruch Schemata (§ 985, § 823,
   § 812, GoA, …). Near-ideal worked examples of Merkmal trees with transitions.
   → https://www.uni-potsdam.de/de/ls-bezzenberger/lehre/allgemeine-lehrmaterialien-zum-bgb
6. **Wandtke (HU Berlin), "Aufbauschemata und Übersichten zum BGB" (PDF).** Free PDF; shows the
   full Anspruchsprüfung skeleton (entstanden → übergegangen → erloschen [rechtsvernichtende
   Einwendungen] → durchsetzbar [Leistungsverweigerungsrechte]) and the §-433-Vertrag → §§ 145 ff.-
   Einigung structure — i.e. exactly the Merkmal-mediated transition DD-001 uses as its worked
   example. → http://wandtke.rewi.hu-berlin.de/doc/Skript_BGB_1.pdf
7. **opinioiuris.de — Prüfungsschemata / Zivilrecht.** Free, structured schema collection,
   explicitly built on the Medicus/Petersen systematization. A reasonable look at what a
   machine-readable schema seed would resemble. → https://opinioiuris.de/schema/ (BGB-AT entry:
   /schema/3860)

## 4. Tier 3 — orientation (free, for getting the shape fast)
8. **Passau, "Einführung in den Gutachtenstil" (uni script PDF).** Free; covers Gutachtenstil
   mechanics and cites the Leenen Jura-2011 article. Good bridge from "four-step Obersatz–
   Definition–Subsumtion–Ergebnis" to the Anspruchsaufbau.
   → https://ilias.uni-passau.de/ (search "Einführung in den Gutachtenstil")
9. **recht-vertieft.de / WikiJur — "Prüfungsreihenfolge."** Free; clean statement of the
   rechtshindernd/rechtsvernichtend/rechtshemmend Einwendung-vs-Einrede taxonomy that our edge
   types 3/4 encode. → https://www.recht-vertieft.de/wikijur/zr/bgb-at/grundlagen/pruefungsreihenfolge/
10. **juriverse / lecturio / jurahilfe Prüfungsreihenfolge explainers.** Free orientation on
    Anspruchskonkurrenz ordering and Sperrwirkung; commercial tutorial quality — use for intuition,
    not for citing.

## 5. Suggested reading order (AI-side reader)
1. A Tier-3 Gutachtenstil explainer (#8/#9) → the four-step mechanics + the three-level skeleton.
2. Bezzenberger #5 "Grundschema" + "Prüfungsreihenfolge nach Anspruchsarten" → the tree shape.
3. Wandtke #6 → the full Einwendung/Einrede/durchsetzbar levels + the §433→§§145 ff. transition.
4. Leenen Jura-2011 #1 → the thesis that statute structure ≙ Fallbearbeitung structure (our core).
5. Medicus/Petersen #3 ToC → Anspruchskonkurrenz / Prüfungsreihenfolge as the law-layer's spine.
Everything else on demand.

## 6. How this feeds the project
- **DD-001/DD-002:** these sources are the **Evidence/sources** backing the structural claims
  (Merkmal-mediated transitions, Verweisung sub-types, Einwendung/Einrede/Anspruchskonkurrenz as
  distinct relation semantics). Cite Leenen (2011) + a schema source for any such claim, alongside
  the C-01 spike (which corroborates with one case, n=1 — not the load-bearing evidence).
- **DD-004 (scope slice, open):** Medicus/Petersen's ordering and the per-area Schemata help score
  candidate slices (Kaufrecht vs. Delikt) on schema density and Anspruchskonkurrenz cleanliness.
- **PAPER / domain corpus:** this file is the seed of the "German legal method / computational
  legal reasoning" concept column of the Webster & Watson matrix; its search will be documented
  per vom Brocke et al. (2009) when the domain review is built.
- **Bibliography:** Tier-1 entries are candidates for `paper/bib/references.bib` — but per the
  PAPER-lane rule, every entry stays an UNVERIFIED SEED until checked against the actual source.

## Changelog
- 2026-06-24 · Created during DD-002 (ARCH) at the user's request; editions verified
  (Medicus/Petersen 30. Aufl. 2025; Leenen/Häublein 3. Aufl. 2021). DD-002 paused at the
  "what an edge connects = type-dependent geometry" decision, pending the user's reading.
