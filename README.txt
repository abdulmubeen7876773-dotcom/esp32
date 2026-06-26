ESP32 Engine — Static-First Educational Platform (Phase 1)
==========================================================

ARCHITECTURE
  - All content: version-controlled YAML files in content/
  - Build step: Python scripts in tools/ (run locally or via GitHub Actions)
  - Runtime: 100% static HTML + client-side JS (no server, database, or auth)
  - Search:  search-index.json + search.js (browser-only)

NO BACKEND IN PHASE 1
  - No admin panel, API, database, or login
  - Edit content by changing files in content/ and rebuilding
  - See static.config.yaml and content/manifest.yaml for structure

QUICK START (edit content)
  1. Edit YAML in content/ (guides, components, projects, pages)
  2. Run:  py tools/build_all.py
  3. Push to main — GitHub Actions rebuilds automatically

CONTENT LOCATIONS
  content/site.yaml              Site settings
  content/home.yaml              Homepage text
  content/guides/*.yaml          Missions and reference guides
  content/components/*.yaml      Component encyclopedia
  content/projects/*.yaml        Project source data
  content/pages/*.yaml           Static pages (about, parents, etc.)

GENERATED FILES (do not edit by hand — rebuild instead)
  *.html, guides/**, components/**, projects/*.html
  search-index.json, projects.json, project-icons.js
  sitemap.xml, feed.xml

MAINTENANCE (owner away 10+ days)
  - Site keeps running on GitHub Pages with zero server upkeep
  - To publish changes: edit content/*.yaml, push to main
  - CI validates content and regenerates all pages
  - Only dependency: Python 3 + PyYAML (installed in CI automatically)

FUTURE PHASE 2 (backend optional)
  - content/backend in static.config.yaml can switch to api
  - Implement tools/content_api.py — templates in tools/ stay unchanged
  - Public interface: tools/content_store.py

DEPLOY
  - Push repo to GitHub, enable Pages on main branch / root
  - Domain: CNAME file points to esp32engine.com
