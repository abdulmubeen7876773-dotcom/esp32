import { test, expect } from '@playwright/test';
import fs from 'node:fs/promises';
import path from 'node:path';

const slugs = ['max7219-led-matrix', 'analog-joystick', 'reed-switch', 'sg90-micro-servo', 'through-hole-resistors', 'tactile-push-button'];

test.beforeEach(async ({ page }) => {
  // Local layout/navigation checks only; no analytics or YouTube playback requests.
  await page.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.hostname !== '127.0.0.1') return route.fulfill({ status: 200, body: '' });
    // Fulfil local generated files directly: Chromium loopback can be blocked by the Windows sandbox.
    const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '') || 'index.html';
    const target = path.resolve(process.cwd(), relative);
    if (!target.startsWith(process.cwd() + path.sep)) return route.fulfill({ status: 403, body: '' });
    const types: Record<string, string> = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2' };
    try { return route.fulfill({ status: 200, body: await fs.readFile(target), contentType: types[path.extname(target)] || 'application/octet-stream' }); }
    catch { return route.fulfill({ status: 404, body: '' }); }
  });
});

for (const width of [320, 768, 1440]) {
  for (const theme of ['light', 'dark']) {
    for (const slug of slugs) {
      test(`${slug}: ${width}px ${theme}, images, code and keyboard navigation`, async ({ page }) => {
        const errors: string[] = [];
        page.on('pageerror', e => errors.push(e.message));
        await page.setViewportSize({ width, height: 900 });
        const response = await page.goto(`/components/${slug}.html`);
        expect(response?.status()).toBe(200);
        const reject = page.getByRole('button', { name: 'Reject optional', exact: true });
        if (await reject.isVisible()) await reject.click();
        await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
        await expect(page.locator('h1')).toHaveCount(1);
        await expect(page.locator('#setup')).toContainText('ESP32-WROOM-32');
        await expect(page.locator('#setup')).toContainText('3.3.2');
        await expect(page.locator('#setup')).toContainText('Not compiled');
        const hero = page.locator('.component-hero-photo img');
        await expect(hero).toHaveAttribute('width', '1408');
        await expect(hero).toHaveAttribute('height', '768');
        await expect(hero).toHaveAttribute('alt', /illustration/);
        await expect.poll(() => hero.evaluate((img: HTMLImageElement) => img.naturalWidth)).toBe(1408);
        expect(await hero.evaluate((img: HTMLImageElement) => img.naturalHeight)).toBe(768);
        const images = page.locator('.article-concise img');
        for (const img of await images.all()) {
          await img.scrollIntoViewIfNeeded();
          await expect.poll(() => img.evaluate((el: HTMLImageElement) => el.complete && el.naturalWidth > 0)).toBe(true);
          await expect(img).toHaveAttribute('alt', /\S/);
        }
        await page.locator('.article-contents > summary').click();
        const nav = page.getByRole('navigation', { name: 'On this page', exact: true });
        for (const link of await nav.getByRole('link').all()) {
          await expect(page.locator((await link.getAttribute('href'))!)).toHaveCount(1);
        }
        const codeLink = nav.getByRole('link', { name: 'Wiring and matching Arduino code' });
        await codeLink.focus();
        await page.keyboard.press('Enter');
        await expect(page.locator('#code-heading')).toBeFocused();
        await page.keyboard.press('Tab');
        await expect(page.locator('#code .btn-copy').first()).toBeFocused();
        await page.keyboard.press('Tab');
        await expect(page.locator('#code pre')).toBeFocused();
        await expect(page.locator('#code pre')).toContainText('void setup()');
        await expect(page.locator('#code pre')).toContainText('void loop()');
        const table = page.locator('.article-concise .wiring-table-wrap').first();
        await table.focus();
        await expect(table).toBeFocused();
        await expect(table).toHaveAttribute('role', 'region');
        const diagramLink = page.getByRole('link', { name: 'Open wiring diagram at full size (new tab)' });
        await expect(diagramLink).toHaveAttribute('href', `/assets/visuals/components/wiring/${slug}-wiring.svg`);
        await diagramLink.focus();
        await expect(diagramLink).toBeFocused();
        const faq = page.locator('.component-faq .faq-q');
        await faq.first().focus();
        await page.keyboard.press('Enter');
        await expect(faq.first()).toHaveAttribute('aria-expanded', 'true');
        await faq.nth(1).focus();
        await page.keyboard.press('Enter');
        await expect(faq.first()).toHaveAttribute('aria-expanded', 'false');
        await expect(faq.nth(1)).toHaveAttribute('aria-expanded', 'true');
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
        expect(errors).toEqual([]);
        if (process.env.COMPONENT_QA_DIR && width !== 768) {
          await page.locator('h1').scrollIntoViewIfNeeded();
          await page.screenshot({ path: path.join(process.env.COMPONENT_QA_DIR, `${slug}-${width}-${theme}.png`) });
          await page.locator('#wiring').scrollIntoViewIfNeeded();
          await page.screenshot({ path: path.join(process.env.COMPONENT_QA_DIR, `${slug}-wiring-${width}-${theme}.png`) });
        }
      });
    }
  }
}

test('Component listing exposes 18 entries and the first six and next four approved pages, with usable keyboard search', async ({ page }) => {
  await page.goto('/components.html');
  await expect(page.locator('#component-grid .component-card')).toHaveCount(18);
  for (const slug of [...slugs, 'discrete-leds', 'rgb-led', 'passive-buzzer', 'l298n-motor-driver']) await expect(page.locator(`#component-grid .component-card[href="/components/${slug}.html"]`)).toHaveCount(1);
  const search = page.locator('#component-search');
  await search.focus();
  await page.keyboard.type('SG90');
  await expect(page.locator('#component-count')).toHaveText('1 component');
  const card = page.locator('.component-card[href="/components/sg90-micro-servo.html"]');
  await card.focus();
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/sg90-micro-servo\.html$/);
});

test('Dependent count pages and search contain the expanded catalog, with no DHT11 image entry', async ({ page }) => {
  await page.goto('/learning.html');
  await expect(page.locator('#explorer')).toContainText('18 components');
  await page.goto('/about.html');
  await expect(page.locator('.premium-stats').first()).toContainText('18');
  const search = JSON.parse(await fs.readFile(path.join(process.cwd(), 'search-index.json'), 'utf8'));
  const components = search.filter((item: { type: string }) => item.type === 'Component');
  expect(components).toHaveLength(18);
  for (const slug of slugs) expect(components.filter((item: { slug: string }) => item.slug === slug)).toHaveLength(1);
  expect(components.some((item: { slug: string }) => item.slug === 'dht11')).toBe(false);
});

for (const width of [320, 1440]) {
  for (const theme of ['light', 'dark']) {
    test(`Existing components retain images and layout: ${width}px ${theme}`, async ({ page }) => {
      await page.setViewportSize({ width, height: 900 });
      for (const slug of ['bme280', 'dht22', 'esp32-cam', 'esp32-devkit', 'hc-sr04', 'pir-sensor', 'relay-module', 'ssd1306-oled']) {
        await page.goto(`/components/${slug}.html`);
        await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
        await expect(page.locator('h1')).toHaveCount(1);
        const hero = page.locator('.component-hero-photo img');
        await expect.poll(() => hero.evaluate((img: HTMLImageElement) => img.naturalWidth > 0)).toBe(true);
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
      }
    });
  }
}

test('All eight existing YouTube attributes and fallback mappings remain intact; no playback attempted', async ({ page }) => {
  const videos: Record<string, string> = {
    'blink-led-esp32': '8pv1U53mXcU', 'button-led-control': 'g8iKRpT9oZk',
    'read-temperature-dht22': 'zLHl_6ToUck', 'connect-oled-esp32': 'lyu31EtokpQ',
    'digital-inputs-floating-pins': 'XU8GkY_MVvQ', 'pull-up-vs-pull-down-resistors': 'pkLKrbIEdjI',
    'debouncing-buttons': 'U5waBMmadpY', 'multiple-buttons-state-detection': 'CvMPiLwxPwc',
  };
  for (const [slug, id] of Object.entries(videos)) {
    await page.goto(`/guides/${slug}.html`);
    const frame = page.locator(`iframe[src*="youtube-nocookie.com/embed/${id}"]`);
    await expect(frame).toHaveCount(1);
    await expect(frame).toHaveAttribute('loading', 'lazy');
    await expect(frame).toHaveAttribute('title', /\S/);
    expect(await frame.getAttribute('src')).not.toMatch(/autoplay=1/);
    await expect(page.locator(`a[href="https://www.youtube.com/watch?v=${id}"]`)).toHaveCount(1);
    if (slug === 'read-temperature-dht22') await expect(page.locator('h1')).toContainText('DHT11');
  }
});
