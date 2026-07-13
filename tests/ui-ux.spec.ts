import { expect, test, type Page, type TestInfo } from '@playwright/test';

const viewports = [
  { width: 320, height: 568, name: '320x568' },
  { width: 375, height: 667, name: '375x667' },
  { width: 390, height: 844, name: '390x844' },
  { width: 768, height: 1024, name: '768x1024' },
  { width: 1024, height: 768, name: '1024x768' },
  { width: 1366, height: 768, name: '1366x768' },
  { width: 1440, height: 900, name: '1440x900' },
];

const routes = [
  { label: 'Homepage', path: '/' },
  { label: 'Projects', path: '/projects.html' },
  { label: 'Display category', path: '/category/display-projects.html' },
  { label: 'Beginner project', path: '/projects/esp32-iot-weather-station.html' },
  { label: 'Safety project', path: '/projects/esp32-smart-energy-meter.html' },
  { label: 'Guides', path: '/guides.html' },
  { label: 'Guide detail', path: '/guides/what-is-esp32.html' },
  { label: 'Components', path: '/components.html' },
  { label: 'ESP32-CAM component', path: '/components/esp32-cam.html' },
  { label: 'HC-SR04 component', path: '/components/hc-sr04.html' },
  { label: 'Parents', path: '/parents.html' },
  { label: 'Teachers', path: '/teachers.html' },
  { label: 'Tools', path: '/tools.html' },
  { label: 'Learning resources', path: '/downloads.html' },
  { label: 'Contact', path: '/contact.html' },
  { label: 'About', path: '/about.html' },
  { label: 'Search', path: '/search.html' },
  { label: 'Human sitemap', path: '/sitemap.html' },
];

const mojibakePatterns = ['Ã‚', 'Ãƒ', 'Ã¢â‚¬', 'Ã°Å¸', 'Â', 'â€', 'ðŸ'];
const ignoredConsole = [/favicon/i, /googletagmanager/i, /google-analytics/i, /fonts\.googleapis/i, /fonts\.gstatic/i];

function isIgnored(message: string, url = '') {
  const haystack = `${message} ${url}`;
  return ignoredConsole.some((pattern) => pattern.test(haystack));
}

async function preparePage(page: Page, testInfo: TestInfo) {
  const consoleErrors: string[] = [];
  const pageErrors: string[] = [];
  const failedRequests: string[] = [];

  page.on('console', (msg) => {
    if (msg.type() !== 'error') return;
    const text = msg.text();
    if (!isIgnored(text, msg.location().url)) consoleErrors.push(text);
  });
  page.on('pageerror', (err) => pageErrors.push(err.message));
  page.on('requestfailed', (request) => {
    const url = request.url();
    if (!url.startsWith('http://127.0.0.1:4173')) return;
    failedRequests.push(`${request.method()} ${url} ${request.failure()?.errorText || ''}`.trim());
  });

  await page.addInitScript(() => {
    localStorage.setItem('cookie-consent', 'rejected');
  });

  await testInfo.attach('runtime-watchers', {
    body: 'Console, page error, and same-origin request failure watchers enabled.',
    contentType: 'text/plain',
  });

  return { consoleErrors, pageErrors, failedRequests };
}

async function gotoOk(page: Page, path: string) {
  const response = await page.goto(path, { waitUntil: 'networkidle' });
  expect(response, `No response for ${path}`).toBeTruthy();
  expect(response!.status(), `${path} should return successfully`).toBeLessThan(400);
}

async function visibleBoxCount(page: Page, selector: string) {
  return page.locator(selector).evaluateAll((els) =>
    els.filter((el) => {
      const style = getComputedStyle(el as HTMLElement);
      const rect = (el as HTMLElement).getBoundingClientRect();
      return style.visibility !== 'hidden' && style.display !== 'none' && rect.width > 0 && rect.height > 0;
    }).length
  );
}

async function runCoreChecks(page: Page, label: string, path: string, watchers: Awaited<ReturnType<typeof preparePage>>) {
  await expect(page.locator('header, .site-nav-sticky').first(), `${label}: header/nav should render`).toBeVisible();
  await expect(page.locator('footer').first(), `${label}: footer should render`).toBeVisible();
  await expect(page.locator('main').first(), `${label}: main content should render`).toBeVisible();

  const h1Count = await visibleBoxCount(page, 'h1');
  expect(h1Count, `${label}: should have exactly one visible H1`).toBe(1);

  await page.evaluate(async () => {
    const maxY = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    for (const y of [0, maxY * 0.33, maxY * 0.66, maxY]) {
      window.scrollTo(0, y);
      await new Promise((resolve) => window.setTimeout(resolve, 80));
    }
    window.scrollTo(0, 0);
  });
  await page.waitForLoadState('networkidle');

  const integrity = await page.evaluate((patterns) => {
    const doc = document.documentElement;
    const viewportWidth = doc.clientWidth;
    const all = [...document.querySelectorAll<HTMLElement>('body *')];
    const visible = all.filter((el) => {
      const style = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
    });
    const ids = [...document.querySelectorAll<HTMLElement>('[id]')].map((el) => el.id);
    const dupes = ids.filter((id, i) => ids.indexOf(id) !== i);
    const emptyLinks = [...document.querySelectorAll<HTMLAnchorElement>('a[href]')]
      .filter((a) => {
        const imgAlt = [...a.querySelectorAll<HTMLImageElement>('img')].map((img) => img.alt).join(' ').trim();
        return !a.textContent.trim() && !a.getAttribute('aria-label') && !a.getAttribute('title') && !imgAlt;
      })
      .map((a) => a.outerHTML.slice(0, 120));
    const emptyButtons = [...document.querySelectorAll<HTMLButtonElement>('button')]
      .filter((b) => !b.textContent.trim() && !b.getAttribute('aria-label') && !b.getAttribute('title'))
      .map((b) => b.outerHTML.slice(0, 120));
    const positiveTabIndex = [...document.querySelectorAll<HTMLElement>('[tabindex]')]
      .filter((el) => Number(el.getAttribute('tabindex')) > 0)
      .map((el) => el.outerHTML.slice(0, 120));
    const previouslyFocused = document.activeElement as HTMLElement | null;
    const focusableHidden = [...document.querySelectorAll<HTMLElement>('[hidden] a, [hidden] button, [hidden] input, [aria-hidden="true"] a, [aria-hidden="true"] button, [aria-hidden="true"] input, .filter-hidden, .page-hidden, .home-hidden')]
      .filter((el) => {
        el.focus();
        return document.activeElement === el;
      })
      .map((el) => el.outerHTML.slice(0, 120));
    previouslyFocused?.focus?.();
    const overflowElements = visible
      .filter((el) => {
        const rect = el.getBoundingClientRect();
        return rect.right > viewportWidth + 3 || rect.left < -3;
      })
      .filter((el) => {
        const rect = el.getBoundingClientRect();
        for (let parent = el.parentElement; parent; parent = parent.parentElement) {
          const parentStyle = getComputedStyle(parent);
          if (!['hidden', 'clip'].includes(parentStyle.overflowX)) continue;
          const parentRect = parent.getBoundingClientRect();
          if (rect.right > parentRect.right + 1 || rect.left < parentRect.left - 1) return false;
        }
        return true;
      })
      .filter((el) => {
        const scrollParent = el.closest<HTMLElement>('.nav-spotlight-scroll, .v2-trust-strip-inner, .wiring-table-wrap, .pin-table-wrap, .code-block, pre, .level-code, .component-toc');
        if (!scrollParent) return true;
        const style = getComputedStyle(scrollParent);
        return !(scrollParent.scrollWidth > scrollParent.clientWidth && ['auto', 'scroll'].includes(style.overflowX));
      })
      .filter((el) => !['SCRIPT', 'STYLE', 'LINK', 'META'].includes(el.tagName))
      .slice(0, 12)
      .map((el) => `${el.tagName}.${el.className} ${Math.round(el.getBoundingClientRect().left)}..${Math.round(el.getBoundingClientRect().right)}`);
    const collapsedCards = [...document.querySelectorAll<HTMLElement>('.card, .premium-card, .project-card, .tool-card')]
      .filter((el) => {
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return style.display !== 'none' && rect.width > 0 && rect.height < 24;
      })
      .map((el) => el.outerHTML.slice(0, 120));
    const anchorMisses = [...document.querySelectorAll<HTMLAnchorElement>('a[href^="#"]')]
      .map((a) => a.getAttribute('href') || '')
      .filter((href) => href.length > 1 && !document.getElementById(decodeURIComponent(href.slice(1))));
    const text = document.body.innerText || '';
    const mojibake = patterns.filter((pattern) => text.includes(pattern));
    return {
      scrollWidth: doc.scrollWidth,
      clientWidth: doc.clientWidth,
      dupes: [...new Set(dupes)],
      emptyLinks,
      emptyButtons,
      positiveTabIndex,
      focusableHidden,
      overflowElements,
      collapsedCards,
      anchorMisses,
      mojibake,
    };
  }, mojibakePatterns);

  expect(integrity.scrollWidth, `${label}: no page-level horizontal overflow`).toBeLessThanOrEqual(integrity.clientWidth + 3);
  expect(integrity.dupes, `${label}: duplicate element IDs`).toEqual([]);
  expect(integrity.emptyLinks, `${label}: empty links`).toEqual([]);
  expect(integrity.emptyButtons, `${label}: empty buttons`).toEqual([]);
  expect(integrity.positiveTabIndex, `${label}: positive tabindex`).toEqual([]);
  expect(integrity.focusableHidden, `${label}: hidden focusable elements`).toEqual([]);
  expect(integrity.overflowElements, `${label}: elements should stay within viewport on ${path}`).toEqual([]);
  expect(integrity.collapsedCards, `${label}: cards should not collapse`).toEqual([]);
  expect(integrity.anchorMisses, `${label}: internal anchors should target existing IDs`).toEqual([]);
  expect(integrity.mojibake, `${label}: visible text should be mojibake-free`).toEqual([]);

  const imageSources = await page.locator('img').evaluateAll((imgs) =>
    [...new Set(imgs
      .map((img) => (img as HTMLImageElement).currentSrc || (img as HTMLImageElement).src || '')
      .filter((src) => src.startsWith(location.origin))
      .map((src) => new URL(src).href))]
  );
  const brokenImages: string[] = [];
  for (const src of imageSources) {
    const response = await page.request.get(src);
    if (!response.ok()) brokenImages.push(new URL(src).pathname);
  }
  expect(brokenImages, `${label}: same-origin images should load`).toEqual([]);

  await page.keyboard.press('Tab');
  await expect(page.locator(':focus'), `${label}: keyboard focus should be visible`).toBeVisible();

  expect(watchers.consoleErrors, `${label}: no serious console errors`).toEqual([]);
  expect(watchers.pageErrors, `${label}: no uncaught JS errors`).toEqual([]);
  expect(watchers.failedRequests, `${label}: no failed same-origin requests`).toEqual([]);
}

test.describe('responsive page integrity matrix', () => {
  for (const viewport of viewports) {
    for (const route of routes) {
      test(`${route.label} renders cleanly at ${viewport.name}`, async ({ page }, testInfo) => {
        await page.setViewportSize({ width: viewport.width, height: viewport.height });
        const watchers = await preparePage(page, testInfo);
        await gotoOk(page, route.path);
        await runCoreChecks(page, `${route.label} ${viewport.name}`, route.path, watchers);
      });
    }
  }
});

test('mobile navigation opens, exposes links, and closes after selection', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  const watchers = await preparePage(page, testInfo);
  await gotoOk(page, '/');
  const toggle = page.locator('.nav-toggle');
  await expect(toggle).toBeVisible();
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  await toggle.click();
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('.top-nav')).toHaveClass(/is-open/);
  await expect(page.locator('.top-nav a[href="/projects.html"]')).toBeVisible();
  await page.keyboard.press('Tab');
  await expect(page.locator(':focus')).toBeVisible();
  await page.locator('.top-nav a[href="/projects.html"]').click();
  await expect(toggle).toHaveAttribute('aria-expanded', 'false');
  expect(watchers.consoleErrors).toEqual([]);
  expect(watchers.pageErrors).toEqual([]);
});

test('mobile navigation opens from keyboard activation', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 320, height: 568 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/');
  const toggle = page.locator('.nav-toggle');
  await toggle.focus();
  await page.keyboard.press('Enter');
  await expect(toggle).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('.top-nav')).toHaveClass(/is-open/);
});

test('homepage recommendation controls update content accessibly', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1366, height: 768 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/');
  await expect(page.locator('#learning-adventure')).toBeVisible();

  for (const audience of ['student', 'parent', 'teacher', 'maker']) {
    const button = page.locator(`[data-audience="${audience}"]`);
    await button.click();
    await expect(button).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('#home-recommendations')).toBeVisible();
    await expect(page.locator('#home-recommendations a')).toHaveCount(3);
  }

  for (const goal of ['first-esp32-project', 'sensors-and-data', 'smart-home-and-iot', 'robotics-and-motion', 'cameras-and-computer-vision', 'ai-and-advanced-builds']) {
    const button = page.locator(`[data-goal="${goal}"]`);
    await button.click();
    await expect(button).toHaveAttribute('aria-pressed', 'true');
    await expect(page.locator('#home-recommendations a')).toHaveCount(3);
  }

  const hiddenFocusable = await page.locator('[hidden] a, [hidden] button, [aria-hidden="true"] a, [aria-hidden="true"] button').evaluateAll((els) =>
    els.filter((el) => {
      const previouslyFocused = document.activeElement as HTMLElement | null;
      (el as HTMLElement).focus();
      const focused = document.activeElement === el;
      previouslyFocused?.focus?.();
      return focused;
    }).length
  );
  expect(hiddenFocusable).toBe(0);
});

test('project listing filters public projects accurately', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/projects.html');
  await expect(page.locator('.project-card')).toHaveCount(49);
  await expect(page.locator('body')).not.toContainText('ESP32 TinyML Sound Classifier');
  await expect(page.locator('.breadcrumb')).toContainText(/Home\s*Projects/);
  await expect(page.locator('body')).not.toContainText('3 Levels Each');
  await expect(page.locator('body')).not.toContainText('Beginner, Intermediate, and Advanced stages');

  await page.locator('#diff').selectOption('Advanced');
  await expect(page.locator('#count')).toContainText(/projects found/);
  let badVisible = await page.locator('.project-card:not(.filter-hidden)').evaluateAll((cards) =>
    cards.filter((card) => !(card as HTMLElement).dataset.levels?.includes('Advanced')).length
  );
  expect(badVisible).toBe(0);

  await page.locator('#cat').selectOption('ESP32-CAM');
  badVisible = await page.locator('.project-card:not(.filter-hidden)').evaluateAll((cards) =>
    cards.filter((card) => (card as HTMLElement).dataset.category !== 'ESP32-CAM').length
  );
  expect(badVisible).toBe(0);

  await page.locator('#q').fill('zzzz-no-project');
  await expect(page.locator('#projects-no-results')).toBeVisible();
  const focusableHidden = await page.locator('.project-card.filter-hidden').evaluateAll((cards) =>
    cards.filter((card) => (card as HTMLElement).tabIndex >= 0).length
  );
  expect(focusableHidden).toBe(0);

  await page.locator('#q').fill('');
  await page.locator('#cat').selectOption('');
  await page.locator('#diff').selectOption('');
  const loadMore = page.locator('#projects-load-more');
  if (await loadMore.isVisible()) {
    await loadMore.click();
    await expect(page.locator('.project-card.page-hidden')).toHaveCount(0);
  }
});

test('site search returns public, escaped, useful results', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/search.html');
  const input = page.locator('#search-page-input');
  const results = page.locator('#search-page-results');

  for (const query of ['ESP32 Low-Voltage Energy Meter Demo', 'energy meter', 'Blink an LED with ESP32', 'HC-SR04', '  esp32 cam  ']) {
    await input.fill(query);
    await expect(results.locator('a').first()).toBeVisible();
  }

  await input.fill('ESP32 TINYML SOUND CLASSIFIER');
  await expect(results).toContainText('No results found');
  await expect(results).not.toContainText('TinyML Sound Classifier');

  await input.fill('<img src=x onerror=alert(1)>');
  await expect(results).toContainText('No results found');
  await expect(page.locator('#search-page-results img')).toHaveCount(0);

  await input.fill('DHT22');
  await input.press('Enter');
  await page.waitForURL(/search\.html\?q=DHT22/);
});

test('global search overlay opens and closes without trapping page state', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/');
  await page.locator('#search-open').click();
  await expect(page.locator('#search-overlay')).toBeVisible();
  await expect(page.locator('#global-search')).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.locator('#search-overlay')).toBeHidden();
});

test('tools calculators handle input ranges without NaN or Infinity', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/tools.html');
  const inputs = page.locator('[data-tool]');
  const count = await inputs.count();
  expect(count).toBeGreaterThan(0);

  for (const value of ['', '12', '3.14', '0', '-5', '999999', ' abc ']) {
    for (let i = 0; i < count; i += 1) {
      const input = inputs.nth(i);
      await input.evaluate((el, nextValue) => {
        (el as HTMLInputElement).value = nextValue;
        el.dispatchEvent(new Event('input', { bubbles: true }));
      }, value);
    }
    const outputs = await page.locator('[data-tool-output]').allTextContents();
    expect(outputs.join(' '), `calculator outputs for ${value}`).not.toMatch(/\bNaN\b|Infinity/);
  }

  await expect(page.locator('[data-tool-output="adc"]')).toContainText(/ADC|volts|about|≈|ESP32/i);
  await expect(page.locator('button', { hasText: /reset/i })).toHaveCount(0);
});

test('theme toggle persists and keeps content readable', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 768, height: 1024 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/tools.html');
  const toggle = page.locator('#theme-toggle');
  await expect(toggle).toBeVisible();
  await toggle.click();
  const theme = await page.locator('html').getAttribute('data-theme');
  expect(['dark', 'light']).toContain(theme);
  await page.reload({ waitUntil: 'networkidle' });
  await expect(page.locator('html')).toHaveAttribute('data-theme', theme!);
  await page.keyboard.press('Tab');
  await expect(page.locator(':focus')).toBeVisible();
});

test('academy color tokens render readable light and dark surfaces', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1366, height: 768 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/');

  const auditColors = async () =>
    page.evaluate(() => {
      function parseRgb(value: string) {
        const match = value.match(/rgba?\(([^)]+)\)/);
        if (!match) return null;
        const channels = match[1].split(/[\s,\/]+/).filter(Boolean).slice(0, 3).map(Number);
        return channels.length === 3 && channels.every((channel) => Number.isFinite(channel)) ? channels : null;
      }
      function linear(channel: number) {
        const normalized = channel / 255;
        return normalized <= 0.03928 ? normalized / 12.92 : Math.pow((normalized + 0.055) / 1.055, 2.4);
      }
      function contrast(foreground: number[], background: number[]) {
        const f = 0.2126 * linear(foreground[0]) + 0.7152 * linear(foreground[1]) + 0.0722 * linear(foreground[2]);
        const b = 0.2126 * linear(background[0]) + 0.7152 * linear(background[1]) + 0.0722 * linear(background[2]);
        return (Math.max(f, b) + 0.05) / (Math.min(f, b) + 0.05);
      }
      const root = getComputedStyle(document.documentElement);
      const body = getComputedStyle(document.body);
      const header = getComputedStyle(document.querySelector('.site-nav-sticky') as HTMLElement);
      const button = getComputedStyle(document.querySelector('.btn-primary, .v2-btn-hero') as HTMLElement);
      const text = parseRgb(body.color);
      const pageBg = parseRgb(body.backgroundColor);
      const buttonText = parseRgb(button.color);
      const buttonBg = parseRgb(button.backgroundColor);
      return {
        theme: document.documentElement.getAttribute('data-theme'),
        surfacePage: root.getPropertyValue('--surface-page').trim(),
        surfaceCard: root.getPropertyValue('--surface-card').trim(),
        actionPrimary: root.getPropertyValue('--action-primary').trim(),
        focusRing: root.getPropertyValue('--focus-ring').trim(),
        bodyContrast: text && pageBg ? contrast(text, pageBg) : 0,
        buttonContrast: buttonText && buttonBg ? contrast(buttonText, buttonBg) : 0,
        headerBackground: header.backgroundColor,
      };
    });

  const light = await auditColors();
  expect(light.surfacePage).toBeTruthy();
  expect(light.surfaceCard).toBeTruthy();
  expect(light.actionPrimary).toBeTruthy();
  expect(light.focusRing).toBeTruthy();
  expect(light.bodyContrast).toBeGreaterThanOrEqual(4.5);
  expect(light.buttonContrast).toBeGreaterThanOrEqual(4.5);
  expect(light.headerBackground).not.toBe('rgba(0, 0, 0, 0)');

  await page.locator('#theme-toggle').click();
  const dark = await auditColors();
  expect(dark.theme).toBe('dark');
  expect(dark.surfacePage).not.toBe(light.surfacePage);
  expect(dark.bodyContrast).toBeGreaterThanOrEqual(4.5);
  expect(dark.buttonContrast).toBeGreaterThanOrEqual(4.5);
  expect(dark.headerBackground).not.toBe('rgba(0, 0, 0, 0)');
});

test('dark mode keeps representative cards and headings readable', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1366, height: 768 });
  await preparePage(page, testInfo);
  await page.addInitScript(() => localStorage.setItem('theme', 'light'));

  for (const path of ['/learning.html', '/projects.html', '/guides/blink-led-esp32.html', '/components.html', '/teachers.html', '/tools.html', '/about.html']) {
    await gotoOk(page, path);
    await page.locator('#theme-toggle').click();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await page.waitForFunction(() => {
      function parseRgb(value: string) {
        const match = value.match(/rgba?\(([^)]+)\)/);
        if (!match) return null;
        return match[1].split(/[\s,\/]+/).filter(Boolean).slice(0, 3).map(Number);
      }
      function isWhite(value: string) {
        const channels = parseRgb(value);
        return !!channels && channels.every((channel) => channel >= 245);
      }
      const selectors = '.premium-card, .tool-card, .path-card, .project-card-item, .guide-index-card, .component-card, .mission-section, .resource-card, .premium-stats div';
      return [...document.querySelectorAll<HTMLElement>(selectors)].every((el) => {
        const style = getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        return rect.width <= 0 || rect.height <= 0 || !isWhite(style.backgroundColor);
      });
    });
    const audit = await page.evaluate(() => {
      function parseRgb(value: string) {
        const match = value.match(/rgba?\(([^)]+)\)/);
        if (!match) return null;
        return match[1].split(/[\s,\/]+/).filter(Boolean).slice(0, 3).map(Number);
      }
      function isWhite(value: string) {
        const channels = parseRgb(value);
        return !!channels && channels.every((channel) => channel >= 245);
      }
      const selectors = '.premium-card, .tool-card, .path-card, .project-card-item, .guide-index-card, .component-card, .mission-section, .resource-card, .premium-stats div';
      const whiteCards = [...document.querySelectorAll<HTMLElement>(selectors)]
        .filter((el) => {
          const style = getComputedStyle(el);
          const rect = el.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0 && isWhite(style.backgroundColor);
        })
        .map((el) => `${el.tagName}.${el.className}`.slice(0, 120));
      const invisibleHeadings = [...document.querySelectorAll<HTMLElement>('h1, h2, h3')]
        .filter((el) => {
          const style = getComputedStyle(el);
          const bg = getComputedStyle(el.closest<HTMLElement>('.premium-card, .tool-card, .path-card, .project-card-item, .guide-index-card, .component-card, .mission-section, .resource-card, .premium-page-hero, body') || document.body).backgroundColor;
          return style.color === bg;
        })
        .map((el) => el.textContent?.trim().slice(0, 80));
      return { whiteCards, invisibleHeadings };
    });
    expect(audit.whiteCards, `${path}: no unintended white cards in dark mode`).toEqual([]);
    expect(audit.invisibleHeadings, `${path}: headings remain visible in dark mode`).toEqual([]);
  }
});

test('sticky header leaves headings and anchor targets visible', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/learning.html');
  const headingTop = await page.locator('h1').evaluate((h1) => (h1 as HTMLElement).getBoundingClientRect().top);
  expect(headingTop, 'initial heading should not sit under sticky bars').toBeGreaterThanOrEqual(-4);

  await page.goto('/learning.html#advanced', { waitUntil: 'networkidle' });
  const result = await page.evaluate(() => {
    const root = getComputedStyle(document.documentElement);
    const safeTop = parseFloat(root.getPropertyValue('--sticky-safe-top')) || 120;
    const target = document.querySelector('#advanced') as HTMLElement;
    return {
      safeTop,
      targetTop: target.getBoundingClientRect().top,
    };
  });
  expect(result.targetTop, 'anchor target should remain below sticky bars').toBeGreaterThanOrEqual(result.safeTop - 8);
});

test('public counts and section headings stay consistent', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/about.html');
  await expect(page.locator('.premium-stats')).toContainText('49');
  await expect(page.locator('.premium-stats')).toContainText('8');
  await expect(page.locator('.premium-stats')).toContainText('16');
  await expect(page.locator('body')).not.toContainText('7Core components');
  await expect(page.locator('body')).not.toContainText('7 Core components');

  await gotoOk(page, '/learning.html');
  await expect(page.locator('#builder')).toContainText('49 projects');
  await expect(page.locator('#explorer')).toContainText('8 components');
  await expect(page.locator('#beginner')).toContainText('16 missions');
  await expect(page.locator('body')).not.toContainText('50 projects');

  await gotoOk(page, '/guides/blink-led-esp32.html');
  const visibleText = await page.locator('body').innerText();
  expect(visibleText).not.toMatch(/PARTSComponents|ENGEngineering|CODECode|GPIOGPIO|SAFETYSafety|WIRINGWiring/);
});

test('reduced motion and constrained zoom-like viewport remain usable', async ({ page }, testInfo) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.setViewportSize({ width: 320, height: 568 });
  await preparePage(page, testInfo);
  await gotoOk(page, '/projects.html');
  await page.locator('body').evaluate((body) => {
    body.style.fontSize = '200%';
  });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(3);
  await expect(page.locator('.nav-toggle')).toBeVisible();
  await page.locator('.nav-toggle').click();
  await expect(page.locator('.top-nav')).toHaveClass(/is-open/);
});
