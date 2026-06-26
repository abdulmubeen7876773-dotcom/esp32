# Release Checklist

Generated: 2026-06-26T17:20:38Z

Complete these checks before production deployment.

## Build

- [x] Static build passes (`py tools/build_all.py`)
- [x] No build errors
- [ ] Zero build warnings

## Content

- [ ] Mission guides pass content validation
- [x] At least one published mission
- [x] Reference guides available
- [x] Golden projects built

## Assets

- [ ] Wiring diagrams present for missions
- [ ] Component photos present
- [ ] Component pinouts documented
- [ ] Image validation warnings resolved

## Links & SEO

- [x] No broken internal links
- [x] No duplicate sitemap URLs
- [x] No orphan HTML pages
- [x] SEO score ≥ 90

## Documentation

- [x] Editorial and engineering docs present

## Accessibility

- [ ] Alt text coverage ≥ 80%

## Overall Readiness

- [ ] Overall readiness score ≥ 80 (39/100)

## Manual verification (human)

- [ ] Spot-check Mission 01 on mobile (375px width)
- [ ] Verify analytics ID in `content/site.yaml`
- [ ] Confirm DNS points to current static host
- [ ] Review staging vs production content parity

