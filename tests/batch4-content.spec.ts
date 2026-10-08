import { test, expect } from '@playwright/test';
import path from 'node:path';

const slugs = ['esp32-oled-weather-clock', 'esp32-smart-thermostat', 'esp32-led-matrix-display'];
test.beforeEach(async ({ page }) => {
  await page.route('**/*', route => new URL(route.request().url()).hostname === '127.0.0.1'
    ? route.continue() : route.fulfill({ status: 200, body: '' }));
});

for (const width of [320, 768, 1440]) for (const theme of ['light', 'dark']) for (const slug of slugs) {
  test(`${slug} layout and keyboard at ${width}px ${theme}`, async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.setViewportSize({ width, height: 900 });
    const response = await page.goto(`/projects/${slug}.html`);
    expect(response?.status()).toBe(200);
    const reject = page.getByRole('button', { name: 'Reject optional', exact: true });
    if (await reject.isVisible()) await reject.click();
    await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('#assumptions')).toContainText('ESP32-WROOM-32');
    await expect(page.locator('#assumptions')).toContainText('3.3.2');
    const sections = ['build', 'components', 'wiring', 'libraries', 'code', 'output', 'troubleshooting'];
    const positions = await page.evaluate(ids => ids.map(id => document.getElementById(id)!.offsetTop), sections);
    expect(positions).toEqual([...positions].sort((a, b) => a - b));
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
    await expect.poll(() => page.locator('#code-heading').evaluate(el => el.getBoundingClientRect().top)).toBeGreaterThan(210);
    await page.keyboard.press('Tab'); await expect(page.locator('#code .btn-copy')).toBeFocused();
    await page.keyboard.press('Tab'); await expect(page.locator('#code pre')).toBeFocused();
    const table = page.locator('#gpio-map .wiring-table-wrap');
    await table.focus(); await expect(table).toBeFocused(); await expect(table).toHaveAttribute('role', 'region');
    await page.locator('#wiring img').scrollIntoViewIfNeeded();
    await expect.poll(() => page.locator('#wiring img').evaluate((img: HTMLImageElement) => img.complete && img.naturalWidth > 0)).toBe(true);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    expect(errors).toEqual([]);
    if (process.env.BATCH4_QA_DIR && width !== 768) {
      await page.waitForTimeout(300);
      await page.screenshot({ path: path.join(process.env.BATCH4_QA_DIR, `${slug}-${width}-${theme}.png`) });
    }
  });
}

for (const slug of slugs) test(`${slug} copy sends complete displayed sketch`, async ({ page }) => {
  await page.addInitScript(() => Object.defineProperty(navigator, 'clipboard', { configurable: true,
    value: { writeText: async (text: string) => { (window as any).copiedSketch = text; } } }));
  await page.goto(`/projects/${slug}.html`);
  const expected = await page.locator('#code code').textContent();
  await page.locator('#code .btn-copy').click();
  await expect.poll(() => page.evaluate(() => (window as any).copiedSketch)).toBe(expected);
});

for (const slug of slugs) test(`${slug} full-size diagram, FAQ keyboard and mobile code`, async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 900 });
  await page.goto(`/projects/${slug}.html`);
  const reject = page.getByRole('button', { name: 'Reject optional', exact: true });
  if (await reject.isVisible()) await reject.click();
  const link = page.getByRole('link', { name: 'Open wiring diagram full size', exact: true });
  await link.focus(); await expect(link).toBeFocused();
  expect(await link.getAttribute('href')).toBe(await page.locator('#wiring img').getAttribute('src'));
  const response = await page.request.get((await link.getAttribute('href'))!);
  expect(response.status()).toBe(200); expect(await response.text()).toContain('<svg');
  const summary = page.locator('#faqs summary').first();
  await summary.focus(); await page.keyboard.press('Enter');
  await expect(summary.locator('..')).toHaveAttribute('open', '');
  await expect(summary.locator('..').locator('.accordion-content')).toBeVisible();
  await page.keyboard.press('Enter'); await expect(summary.locator('..')).not.toHaveAttribute('open', '');
  const pre = page.locator('#code pre');
  await pre.scrollIntoViewIfNeeded();
  const metrics = await pre.evaluate(el => ({ width: el.getBoundingClientRect().width,
    font: parseFloat(getComputedStyle(el.querySelector('code')!).fontSize), overflow: getComputedStyle(el).overflowX }));
  expect(metrics.width).toBeGreaterThan(250); expect(metrics.width).toBeLessThan(320);
  expect(metrics.font).toBeGreaterThanOrEqual(12); expect(metrics.overflow).toBe('auto');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  if (process.env.BATCH4_QA_DIR) for (const theme of ['light', 'dark']) {
    await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(process.env.BATCH4_QA_DIR, `${slug}-code-320-${theme}.png`) });
  }
});

test('clock keeps BME280 weather, bounded network retries and timezone rules', async ({ page }) => {
  await page.goto('/projects/esp32-oled-weather-clock.html');
  const code = page.locator('#code code');
  for (const text of ['YOUR_WIFI_SSID', 'YOUR_WIFI_PASSWORD', 'configTzTime', 'WiFi.reconnect()', 'getLocalTime(&timeinfo, 10)', 'bme.readPressure() / 100.0F']) await expect(code).toContainText(text);
  await expect(page.locator('#configuration')).toContainText('PKT-5');
  await expect(page.locator('#behavior')).toContainText('30 seconds');
});
test('thermostat matches polarity and resets hysteresis memory on fault', async ({ page }) => {
  await page.goto('/projects/esp32-smart-thermostat.html');
  const code = await page.locator('#code code').textContent();
  expect(code).toContain('DHT dht(DHT_PIN, DHT22)');
  expect(code).toMatch(/if \(!isfinite\(tempC\)\) \{\s*fanOn = false/);
  expect(code!.indexOf('pinMode(RELAY_PIN, OUTPUT)')).toBeLessThan(code!.indexOf('digitalWrite(RELAY_PIN, RELAY_OFF)'));
  await expect(page.locator('#configuration')).toContainText('2.5 seconds');
  await expect(page.locator('#safety')).toContainText('Mains wiring is not covered or verified');
  await expect(page.locator('a[href="/guides/read-temperature-dht22.html"]')).toContainText('DHT11');
});
test('matrix setup qualifies mapping, power and logic translation', async ({ page }) => {
  await page.goto('/projects/esp32-led-matrix-display.html');
  await expect(page.locator('#code code')).toContainText('DATA_PIN, CLK_PIN, CS_PIN, MAX_DEVICES');
  await expect(page.locator('#configuration')).toContainText('3.5 V');
  await expect(page.locator('#configuration')).toContainText('2.0 V');
  await expect(page.locator('#components')).toContainText('SN74AHCT125');
  await expect(page.locator('#assumptions')).toContainText('four-chip FC16 board needs 4');
});
