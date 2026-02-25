# Changelog

All notable changes to the meetaudreyevans.com site are documented here.

---

## [Unreleased]

---

## 2026-02-25

### Fixed — Portfolio app link 404 errors

**Problem:** Several app cards in the Portfolio section linked to GitHub Pages URLs that returned 404 errors. The root cause was that three repos (`Pawsitting`, `mindmappr`, `ai-benchmarking-tool`) are private repositories — GitHub Pages requires a paid plan to serve from private repos, so those URLs were dead on arrival. Additionally, `rvvel-affiliate-links-mcp` is also a private repo with no Pages deployment.

**Changes made to `client/src/components/sections/Portfolio.tsx`:**

| App | Old URL | New URL | Reason |
|---|---|---|---|
| PawSitting | `https://midnghtsapphire.github.io/Pawsitting/` (404) | `https://github.com/MIDNGHTSAPPHIRE/Pawsitting` | Private repo — no GitHub Pages |
| MindMappr | `https://midnghtsapphire.github.io/mindmappr/` (404) | `https://github.com/MIDNGHTSAPPHIRE/mindmappr` | Private repo — no GitHub Pages |
| AI Benchmarking Tool | `https://midnghtsapphire.github.io/ai-benchmarking-tool/` (404) | `https://github.com/MIDNGHTSAPPHIRE/ai-benchmarking-tool` | Private repo — no GitHub Pages; status updated to "In Development" |
| Affiliate Links | `https://github.com/MIDNGHTSAPPHIRE/rvvel-affiliate-links-mcp` (404 for public) | `https://github.com/MIDNGHTSAPPHIRE/rvvel-affiliate-links-mcp` | Private repo; link kept, status confirmed "In Development" |

**Confirmed working (no change needed):**
- TheAltText → `https://midnghtsapphire.github.io/thealttext/` ✓
- Universal Data Router → `https://midnghtsapphire.github.io/universal-data-router/` ✓
- Project Face → `https://midnghtsapphire.github.io/project-face/` ✓
- Revvel Email Organizer → `https://midnghtsapphire.github.io/revvel-email-organizer/` ✓

### Added — Visual divider above PawSitting card

Added a subtle `col-span-full` horizontal rule (`<hr>`) above the PawSitting card in the portfolio grid. The divider uses `rgba(169, 149, 128, 0.18)` — a warm, low-contrast tone consistent with the Earth & Canopy design system.

### Fixed — Apple Music link in Music section

**File:** `client/src/components/sections/Music.tsx`

The generic artist slug URL `https://music.apple.com/us/artist/audrey-evans` returned a 404 ("The page you're looking for can't be found"). Fixed to use the canonical URL with artist ID:

- **Before:** `https://music.apple.com/us/artist/audrey-evans`
- **After:** `https://music.apple.com/us/artist/audrey-evans/1825732282`

---
