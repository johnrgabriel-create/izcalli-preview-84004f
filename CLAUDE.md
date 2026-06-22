# Izcalli Website Redesign — Project Context

Rebuild of **izcalli.org** for SRS client **Izcalli** (Chicano/Indigenous
cultural-healing nonprofit, San Diego). Client-separation rule applies: Izcalli
only, never mix with MJ / WAME / other SRS clients.

## Goal
- Replace the end-of-life WordPress site (HostGator, ~2019 Genesis theme) with a
  polished, credible site.
- **#1 objective: funder credibility** (strong About/approach + Programs + impact).
- **Bilingual EN/ES** with a language toggle.
- Build a **static prototype first** as the design+content blueprint, regardless
  of final hosting.

## Phase plan
- **Phase 0 — Content map** (IN PROGRESS): extract real copy from Izcalli's own
  documents, draft `content-map.md`, get John's red-line approval BEFORE design.
- **Phase 1 — Static prototype**: bilingual, ~7 pages, earth-tone design.
- **Phase 2 — Hosting decision**: static-free (Cloudflare Pages/Netlify) vs. light
  git CMS (Decap/Pages CMS). Open; driven by who edits and how often.

## Sitemap (proposed, ~30 WP pages → 7)
Home · About / Our Approach · Programs · Annual Men's Gathering · Get Involved ·
Donate · Contact

## Source material
- Canonical doc library = Google Drive **"Izcalli Folder with John Gabriel"**
  (synced locally at `~/Library/CloudStorage/GoogleDrive-johnrgabriel@gmail.com/My Drive/`).
- Extracted text from key narratives in `_source_text/` (board/staff, DWP
  narrative, 2026 program plan, SD Foundation MH, Irvine nomination, US Bank,
  website edits, existing izcalli-history.html).
- **Photo assets**: `~/Desktop/Izcalli Photos/_MASTER_unique/` — 184 images + 9
  videos, deduped from Drive + Photos album + iMessage + WhatsApp (Macedonio).

## Design language (from comparable orgs + existing history page)
Warm earth tones (maroon #6B2D1A, tan #C4844A, cream #F7F3ED), tasteful
Indigenous motifs, real ceremony/gathering photography carries the site, program
cards, prominent Donate, bilingual, strong "our approach" story for funders.

## Build commands
- **Site:** `python3 build_site.py` (single source of truth, 9 pages; never hand-edit generated HTML).
- **Cutover runbook docx:** `NODE_PATH="$(npm root -g)" node build-cutover-runbook-docx.js`
  — `docx` is installed GLOBALLY, not in this folder (no local node_modules), so
  the `NODE_PATH` prefix is required or it fails with "Cannot find module 'docx'".

## Standing constraints
- John is non-technical. Maintenance question (who edits, how often) still open.
- Don't rush to build: content/design approved first, then polished artifacts.
- Cite sources / flag confidence on facts and numbers (some impact figures are
  dated and need a current-year refresh from John).
