import { test, expect } from '@playwright/test';
import path from 'node:path';

const pages = [
  '/components/dht22.html',
  '/components/esp32-devkit.html',
  '/guides/installing-arduino-ide-esp32.html',
];

test.beforeEach(async ({ page }) => {
  await page.route('**/*', route => {
    const url = new URL(route.request().url());
    return url.hostname === '127.0.0.1' ? route.continue() : route.fulfill({ status: 200, body: '' });
  });
});

for (const width of [320, 768, 1440]) {
  for (const theme of ['light', 'dark']) {
    for (const url of pages) {
      test(`${url} navigation and layout at ${width}px in ${theme}`, async ({ page }) => {
        const errors: string[] = [];
        page.on('pageerror', e => errors.push(e.message));
        await page.setViewportSize({ width, height: 900 });
        await page.goto(url);
        const reject = page.getByRole('button', { name: 'Reject optional', exact: true });
        if (await reject.isVisible()) await reject.click();
        await page.evaluate(t => document.documentElement.setAttribute('data-theme', t), theme);
        await expect(page.locator('h1')).toHaveCount(1);
        if (url.startsWith('/components/') && width >= 768) {
          expect(await page.locator('h1').evaluate(el => el.getBoundingClientRect().width)).toBeGreaterThan(450);
        }
        await expect(page.locator('#setup')).toContainText('ESP32-WROOM-32');
        await expect(page.locator('#setup')).toContainText('3.3.2');
        await page.locator('.article-contents > summary').click();
        const nav = page.getByRole('navigation', { name: 'On this page', exact: true });
        const links = nav.getByRole('link');
        expect(await links.count()).toBeGreaterThan(6);
        for (const link of await links.all()) {
          const target = await link.getAttribute('href');
          await expect(page.locator(target!)).toHaveCount(1);
          await expect(page.locator(target!)).toHaveAttribute('tabindex', '-1');
        }
        const codeLink = nav.getByRole('link', { name: 'Wiring and matching Arduino code' });
        await codeLink.focus();
        await expect(codeLink).toBeFocused();
        await page.keyboard.press('Enter');
        await expect(page.locator('#code-heading')).toBeFocused();
        await expect.poll(() => page.locator('#code-heading').evaluate(el => el.getBoundingClientRect().top)).toBeGreaterThan(width === 320 ? 205 : 150);
        await page.keyboard.press('Tab');
        await expect(page.locator('#code .btn-copy').first()).toBeFocused();
        await page.keyboard.press('Tab');
        await expect(page.locator('#code pre').first()).toBeFocused();
        if (url.includes('pull-up') && width >= 768) {
          expect(await page.locator('#input-comparison .wiring-table-wrap').evaluate(el => el.scrollWidth <= el.clientWidth + 1)).toBe(true);
        }
        const table = page.locator('.article-concise .wiring-table-wrap').first();
        if (await table.count()) {
          await table.focus();
          await expect(table).toBeFocused();
          await expect(table).toHaveAttribute('role', 'region');
        }
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
        await expect(page.locator('.article-concise')).toBeVisible();
        const articleWidth = await page.locator('.article-concise').evaluate(el => el.getBoundingClientRect().width);
        expect(articleWidth).toBeGreaterThan(Math.min(width - 40, 680));
        expect(errors).toEqual([]);
        if (process.env.BATCH3_QA_DIR && width !== 768) {
          await page.locator('.article-contents > summary').click();
          await page.locator('#setup').scrollIntoViewIfNeeded();
          await page.screenshot({ path: path.join(process.env.BATCH3_QA_DIR, `${path.basename(url, '.html')}-${width}-${theme}.png`) });
        }
      });
    }
  }
}

for (const url of pages) {
  test(`${url} FAQ supports keyboard and synchronized expanded state`, async ({ page }) => {
    await page.goto(url);
    const buttons = page.locator('.component-faq .faq-q');
    await expect(buttons).toHaveCount(3);
    for (const i of [0, 1]) {
      await buttons.nth(i).focus();
      await page.keyboard.press('Enter');
      await expect(buttons.nth(i)).toHaveAttribute('aria-expanded', 'true');
      await expect(buttons.nth(i).locator('..').locator('.faq-a')).toBeVisible();
    }
    await expect(buttons.first()).toHaveAttribute('aria-expanded', 'false');
    await expect(buttons.first().locator('..').locator('.faq-a')).toBeHidden();
  });
}

test('DHT22 labels DHT11 historical link and retains the DHT22 example', async ({ page }) => {
  await page.goto('/components/dht22.html');
  await expect(page.locator('#code pre')).toContainText('DHT dht(DHT_PIN, DHT22)');
  await expect(page.locator('#code pre')).toContainText('delay(2500)');
  await expect(page.locator('#guides a[href="/guides/read-temperature-dht22.html"]')).toContainText('DHT11');
  await expect(page.locator('#pinout')).toContainText('vented front');
});

test('IDE first sketch needs no assumed LED GPIO', async ({ page }) => {
  await page.goto('/guides/installing-arduino-ide-esp32.html');
  const code = page.locator('#code pre');
  await expect(code).toContainText('ESP32 upload OK');
  await expect(code).not.toContainText('LED');
  await expect(page.locator('#board-package')).toContainText('https://espressif.github.io/arduino-esp32/package_esp32_index.json');
  await expect(page.locator('#usb-drivers')).toContainText('hardware ID');
});

for (const url of pages) {
  test(`${url} copy button sends displayed code to clipboard API`, async ({ page }) => {
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'clipboard', { value: {
        writeText: async (text: string) => { (window as any).__copiedCode = text; }
      }});
    });
    await page.goto(url);
    const code = await page.locator('#code pre code').first().textContent();
    await page.locator('#code .btn-copy').first().click();
    await expect(page.locator('#code .btn-copy').first()).toHaveAttribute('aria-label', 'Code copied to clipboard');
    expect(await page.evaluate(() => (window as any).__copiedCode)).toBe(code);
  });
}

for (const url of ['/components/dht22.html', '/components/esp32-devkit.html', '/components/bme280.html']) {
  test(`${url} specification table fits tablet and desktop without losing notes`, async ({ page }) => {
    await page.goto(url);
    const table = page.locator('#specs .wiring-table-wrap');
    for (const width of [768, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      expect(await table.evaluate(el => el.scrollWidth <= el.clientWidth + 1)).toBe(true);
    }
    await page.setViewportSize({ width: 320, height: 900 });
    await table.focus();
    await expect(table).toBeFocused();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  });
}
