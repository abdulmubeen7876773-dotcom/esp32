# Staging Deployment Report

Generated: 2026-06-26

Repository: `abdulmubeen7876773-dotcom/esp32`  
Production: [https://esp32engine.com](https://esp32engine.com)  
Staging: [https://stg.esp32engine.com](https://stg.esp32engine.com)

---

## Executive summary

**Root cause:** `stg.esp32engine.com` DNS still points to a **legacy AWS host** (`16.192.62.20`), not GitHub Pages. That host serves a **pre-mission static snapshot** (“Premium ESP32” site). The repository `main` and `staging` branches already contain the current mission-based build.

**Fix applied in repo:** CI now pushes built artifacts to **both** `main` and `staging`, uploads a deploy artifact, deploys **production** and **staging** via GitHub Pages Actions, and runs `tools/check_staging_dns.py` on every build.

**Manual step still required:** Update DNS (and one-time GitHub Pages settings) so staging traffic reaches GitHub Pages instead of AWS.

---

## Current deployment architecture

| Layer | Production | Staging |
|-------|------------|---------|
| **Public URL** | `https://esp32engine.com` | `https://stg.esp32engine.com` |
| **DNS (verified 2026-06-26)** | A → `185.199.108.153` … `185.199.111.153` (GitHub Pages) | A → `16.192.62.20` (legacy AWS) |
| **Git branch** | `main` | `staging` (force-synced from `main` after each CI build) |
| **Root CNAME file** | `esp32engine.com` | Same file on branch today; staging deploy artifact uses `stg.esp32engine.com` |
| **Build** | `py tools/build_all.py` in `.github/workflows/build-site.yml` | Same build output as production |
| **Intended host** | GitHub Pages | GitHub Pages (staging environment) |
| **Legacy host** | — | AWS (still receiving live traffic via DNS) |

### CI workflow (after this fix)

`.github/workflows/build-site.yml`:

1. Build static site on push to `main`
2. Auto-commit generated HTML/JSON/JS/reports
3. **Push `main`** and **force-sync `staging`**
4. Upload `static-site` artifact
5. **Deploy production** → GitHub Pages environment `github-pages`
6. **Deploy staging** → GitHub Pages environment `staging` (artifact CNAME = `stg.esp32engine.com`)
7. Run `tools/check_staging_dns.py` (warns if DNS still on AWS)

### AWS Amplify

`amplify.yml` exists at repo root for historical AWS Amplify builds:

```yaml
build: python3 tools/build_all.py
artifacts: /
```

**Why Amplify still matters:** `stg.esp32engine.com` resolves to `16.192.62.20`, which is consistent with an **old Amplify (or EC2) deployment**, not the current GitHub repository output.

**Recommendation:**

1. **Migrate staging fully to GitHub Pages** (recommended) — update DNS below, then disable or delete the legacy Amplify app connected to `stg.esp32engine.com` to avoid confusion and stale deploys.
2. Do **not** remove `amplify.yml` until Amplify is decommissioned (harmless if unused).

Production should **remain on GitHub Pages** — do not point `esp32engine.com` at Amplify.

---

## Root cause analysis

| Check | Result |
|-------|--------|
| Latest `origin/main` SHA | `63a38d15` — *Create visual asset pipeline* (local also has `4c19e35c` pending push) |
| Latest `origin/staging` SHA | `63a38d15` — matches `main` |
| Production homepage title | `ESP32 Engine — Build Amazing Things with ESP32` ✅ current build |
| Staging homepage title | `ESP32 Engine – Premium ESP32 tutorials…` ❌ old build |
| Production DNS | GitHub Pages (`185.199.x.x`) ✅ |
| Staging DNS | `16.192.62.20` ❌ legacy AWS |
| Staging branch content | Matches production (mission-based `index.html`) ✅ |
| Broken repo sync | **Not the issue** — branches are aligned |

**Conclusion:** Staging is stale because **DNS sends users to the wrong host**, not because Git branches are behind.

---

## Fix applied (repository)

| Change | Purpose |
|--------|---------|
| `.github/workflows/build-site.yml` | Push built `main`, sync `staging`, dual GitHub Pages deploy jobs |
| `tools/check_staging_dns.py` | Detect legacy AWS IP and old staging content in CI |
| `docs/reports/STAGING_DEPLOYMENT_REPORT.md` | This report |

No templates, CSS, or content YAML were modified.

---

## Remaining manual steps

### 1. GitHub repository settings (one-time)

1. Open **Settings → Pages**
2. Set **Source** to **GitHub Actions** (required for `deploy-pages` jobs)
3. Under **Environments**, ensure:
   - `github-pages` → custom domain **`esp32engine.com`**
   - `staging` → custom domain **`stg.esp32engine.com`** (create environment if missing)
4. Enable **Enforce HTTPS** for both domains after DNS propagates

### 2. DNS for staging (required)

At your DNS provider for `esp32engine.com`:

| Action | Record | Value |
|--------|--------|-------|
| **Delete** | `A` record for `stg` → `16.192.62.20` | Remove legacy AWS target |
| **Add** | `CNAME` for `stg` | `abdulmubeen7876773-dotcom.github.io` |

Do **not** change production records (`esp32engine.com` A/ALIAS → `185.199.x.x` or GitHub Pages targets).

### 3. Decommission legacy AWS / Amplify (recommended)

1. AWS Amplify Console → locate app serving `stg.esp32engine.com`
2. Disable auto-deploy or delete the app
3. Confirm `stg.esp32engine.com` no longer resolves to `16.192.62.20`

---

## Verification checklist

After DNS and GitHub settings are updated:

- [ ] `nslookup stg.esp32engine.com` returns `185.199.x.x` (GitHub Pages), **not** `16.192.62.20`
- [ ] `https://stg.esp32engine.com` title contains **Build Amazing Things with ESP32**
- [ ] `https://stg.esp32engine.com` does **not** contain **Premium ESP32 Learning Platform**
- [ ] `git rev-parse origin/staging` equals latest `origin/main` after CI run
- [ ] GitHub Actions **Build and Deploy Static Site** workflow: `deploy-production` and `deploy-staging` succeed
- [ ] `py tools/check_staging_dns.py` exits 0 (no errors)
- [ ] Production `https://esp32engine.com` unchanged and still on mission-based homepage

### Commands

```bash
nslookup stg.esp32engine.com
nslookup esp32engine.com
git fetch origin
git rev-parse origin/main origin/staging
py tools/check_staging_dns.py
```

---

## SHA reference (at time of report)

| Location | SHA | Notes |
|----------|-----|-------|
| `origin/main` | `63a38d15` | Current remote main |
| `origin/staging` | `63a38d15` | Synced with main |
| Local `main` (pre-push) | `4c19e35c` | Blink LED wiring SVG — included in deployment fix push |
| **Served by stg.esp32engine.com** | Unknown (old AWS snapshot) | Not tied to current git SHAs |
| **Served by esp32engine.com** | GitHub Pages from `main` | Current mission build ✅ |

---

## Related files

- `.github/workflows/build-site.yml` — build + deploy
- `CNAME` — production custom domain (`esp32engine.com`)
- `amplify.yml` — legacy Amplify build spec (safe to ignore after DNS migration)
- `docs/engineering/DEVELOPER_ARCHITECTURE.md` — architecture notes
- `tools/check_staging_dns.py` — automated DNS/content probe

Run `py tools/check_staging_dns.py` after DNS changes to confirm staging is fixed.
