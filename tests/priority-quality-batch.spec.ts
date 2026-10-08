import { test, expect } from '@playwright/test';
import path from 'node:path';

const pages = [
  '/components/relay-module.html',
  '/projects/esp32-voice-controlled-relay.html',
  '/guides/blink-led-esp32.html',
];

test.beforeEach(async ({ page }) => {
  // Local layout checks deliberately do not load analytics or YouTube.
  await page.route('**/*', route => new URL(route.request().url()).hostname === '127.0.0.1'
    ? route.continue() : route.fulfill({ status: 200, body: '' }));
});

for (const url of pages) for (const width of [320, 768, 1440]) for (const theme of ['light', 'dark']) {
  test(`${url} layout, assets and keyboard at ${width}px ${theme}`, async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.setViewportSize({ width, height: 900 });
    expect((await page.goto(url))?.status()).toBe(200);
    const reject = page.getByRole('button', { name: 'Reject optional', exact: true });
    if (await reject.isVisible()) await reject.click();
    await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('article')).not.toContainText('Golden version');
    await expect(page.locator('article .mission-illustration-frame')).toHaveCount(0);
    const summary = page.locator('.article-contents > summary');
    await summary.focus(); await page.keyboard.press('Enter');
    const nav = page.getByRole('navigation', { name: 'On this page', exact: true });
    for (const link of await nav.getByRole('link').all()) {
      const target = await link.getAttribute('href');
      await expect(page.locator(target!)).toHaveCount(1);
      await expect(page.locator(target!)).toHaveAttribute('tabindex', '-1');
    }
    const codeLink = nav.locator('a[href="#code-heading"]');
    await codeLink.focus(); await page.keyboard.press('Enter');
    await expect(page.locator('#code-heading')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.locator('#code .btn-copy')).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.locator('#code pre')).toBeFocused();
    const pre = page.locator('#code pre');
    expect(await pre.evaluate(el => getComputedStyle(el).overflowX)).toBe('auto');
    expect(await pre.locator('code').evaluate(el => parseFloat(getComputedStyle(el).fontSize))).toBeGreaterThanOrEqual(12);
    await page.locator('#wiring img').scrollIntoViewIfNeeded();
    await expect.poll(() => page.locator('#wiring img').evaluate((img: HTMLImageElement) => img.complete && img.naturalWidth > 0)).toBe(true);
    const image = await page.locator('#wiring img').evaluate((img: HTMLImageElement) => ({
      natural: img.naturalWidth / img.naturalHeight,
      rendered: img.getBoundingClientRect().width / img.getBoundingClientRect().height,
    }));
    expect(image.rendered).toBeCloseTo(image.natural, 1);
    const fullSize = page.getByRole('link', { name: /^Open wiring diagram/ });
    await fullSize.focus(); await expect(fullSize).toBeFocused();
    expect(await fullSize.getAttribute('href')).toBe(await page.locator('#wiring img').getAttribute('src'));
    expect((await page.request.get((await fullSize.getAttribute('href'))!)).status()).toBe(200);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    expect(errors).toEqual([]);
    if (process.env.PRIORITY_QA_DIR && width !== 768) {
      await page.screenshot({ path: path.join(process.env.PRIORITY_QA_DIR, `${url.split('/').pop()}-${width}-${theme}-wiring.png`) });
    }
  });
}

for (const url of pages) test(`${url} copies the complete displayed sketch`, async ({ page }) => {
  await page.addInitScript(() => Object.defineProperty(navigator, 'clipboard', { configurable: true,
    value: { writeText: async (text: string) => { (window as any).copiedSketch = text; } } }));
  await page.goto(url);
  const expected = await page.locator('#code code').textContent();
  await page.locator('#code .btn-copy').click();
  await expect.poll(() => page.evaluate(() => (window as any).copiedSketch)).toBe(expected);
  expect(expected).toContain('void setup()');
  expect(expected).toContain('void loop()');
});

test('supported relay assumptions, complete examples and single Blink diagnostics', async ({ page }) => {
  await page.goto(pages[0]);
  await expect(page.locator('#setup')).toContainText('4409');
  await expect(page.locator('#setup')).toContainText('active HIGH');
  await expect(page.locator('article .component-code-tab')).toHaveCount(0);
  await expect(page.locator('article')).not.toContainText('Add component read/write code here');
  await expect(page.locator('#downloads')).toHaveCount(0);
  await expect(page.locator('#wiring')).toContainText('10 kΩ');
  await expect(page.locator('#code code')).toContainText('RELAY_OFF = LOW');
  await page.goto(pages[1]);
  await expect(page.locator('#assumptions')).toContainText('not compiled');
  await expect(page.locator('#wiring')).toContainText('external +5 V');
  const code = await page.locator('#code code').textContent();
  expect(code).toContain('#include <ESP_I2S.h>');
  expect(code).not.toContain('driver/i2s.h');
  expect(code).toContain('I2S_STD_SLOT_LEFT');
  expect(code).toContain('setRelay(false);');
  expect(code).toContain('count != sizeof(samples)');
  expect(code).toContain('now - lastAboveQuiet >= QUIET_MS');
  expect(code).toContain('armed = false;');
  await page.goto(pages[2]);
  await expect(page.locator('#common-mistakes')).toHaveCount(0);
  await expect(page.locator('#troubleshooting')).toHaveCount(1);
  await expect(page.locator('#setup')).toContainText('GPIO2');
  await expect(page.locator('iframe')).toHaveAttribute('src', 'https://www.youtube-nocookie.com/embed/8pv1U53mXcU');
  await expect(page.locator('a[href="https://www.youtube.com/watch?v=8pv1U53mXcU"]')).toHaveCount(1);
});
