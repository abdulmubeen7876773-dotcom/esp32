import { test, expect } from '@playwright/test';
import path from 'node:path';

const pages = [
  '/guides/pull-up-vs-pull-down-resistors.html',
  '/guides/digital-inputs-floating-pins.html',
  '/components/bme280.html',
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
        if (process.env.BATCH2_QA_DIR && width !== 768) {
          await page.locator('.article-contents > summary').click();
          await page.locator('#setup').scrollIntoViewIfNeeded();
          await page.screenshot({ path: path.join(process.env.BATCH2_QA_DIR, `${path.basename(url, '.html')}-${width}-${theme}.png`) });
        }
      });
    }
  }
}

for (const url of pages.slice(0, 2)) {
  test(`${url} quiz gives explanatory feedback by keyboard`, async ({ page }) => {
    await page.goto(url);
    const questions = page.locator('.quiz-question');
    await expect(questions).toHaveCount(3);
    for (let i = 0; i < 3; ++i) {
      const question = questions.nth(i);
      const choice = question.locator(i === 1 ? '[data-correct="1"]' : '[data-correct="0"]').first();
      await choice.focus();
      await page.keyboard.press('Enter');
      const feedback = question.getByRole('status');
      await expect(feedback).toBeVisible();
      const explanation = await question.getAttribute('data-explanation');
      await expect(feedback).toContainText(explanation!);
      await expect(feedback).toContainText((await question.getAttribute(i === 1 ? 'data-correct-feedback' : 'data-wrong-feedback'))!);
    }
  });
}

test('BME280 FAQs keep keyboard and expanded state synchronized', async ({ page }) => {
  await page.goto('/components/bme280.html');
  const buttons = page.locator('.component-faq .faq-q');
  for (const i of [0, 1]) {
    await buttons.nth(i).focus();
    await page.keyboard.press('Enter');
    await expect(buttons.nth(i)).toHaveAttribute('aria-expanded', 'true');
    await expect(buttons.nth(i).locator('..').locator('.faq-a')).toBeVisible();
  }
  await expect(buttons.first()).toHaveAttribute('aria-expanded', 'false');
  await expect(buttons.first().locator('..').locator('.faq-a')).toBeHidden();
});
