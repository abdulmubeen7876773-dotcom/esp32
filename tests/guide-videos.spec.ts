import { test, expect } from '@playwright/test';

const videos: Record<string, string> = {
  'blink-led-esp32': '8pv1U53mXcU',
  'button-led-control': 'g8iKRpT9oZk',
  'read-temperature-dht22': 'zLHl_6ToUck',
  'connect-oled-esp32': 'lyu31EtokpQ',
  'digital-inputs-floating-pins': 'XU8GkY_MVvQ',
  'pull-up-vs-pull-down-resistors': 'pkLKrbIEdjI',
  'debouncing-buttons': 'U5waBMmadpY',
  'multiple-buttons-state-detection': 'CvMPiLwxPwc',
};

for (const width of [320, 768, 1440]) {
  for (const [slug, id] of Object.entries(videos)) {
    test(`${slug} tutorial at ${width}px`, async ({ page }) => {
      await page.route('**/*', route => {
        const url = new URL(route.request().url());
        return url.hostname === '127.0.0.1' ? route.continue() : route.fulfill({ status: 200, body: '' });
      });
      const errors: string[] = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.setViewportSize({ width, height: 900 });
      await page.goto(`/guides/${slug}.html`);
      const section = page.locator('#watch-tutorial');
      await expect(section).toHaveCount(1);
      const iframe = section.locator('iframe');
      await expect(iframe).toHaveAttribute('src', `https://www.youtube-nocookie.com/embed/${id}`);
      await expect(iframe).toHaveAttribute('loading', 'lazy');
      await expect(iframe).toHaveAttribute('title', /.+video tutorial/);
      await expect(iframe).toHaveAttribute('allowfullscreen', '');
      await expect(iframe).toHaveAttribute('allow', /fullscreen/);
      await expect(section.getByRole('link')).toHaveAttribute('href', `https://www.youtube.com/watch?v=${id}`);
      const geometry = await section.evaluate(el => {
        const frame = el.querySelector('iframe')!.getBoundingClientRect();
        const intro = document.querySelector('.guide-friendly-intro')!;
        const wiring = document.querySelector('#wiring');
        const code = document.querySelector('#code');
        return {
          ratio: frame.width / frame.height,
          fits: frame.left >= 0 && frame.right <= innerWidth + 1,
          afterIntro: !!(intro.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING),
          beforeBuild: [wiring, code].filter(Boolean).every(node => !!(el.compareDocumentPosition(node!) & Node.DOCUMENT_POSITION_FOLLOWING)),
          overflow: document.documentElement.scrollWidth > innerWidth + 1,
        };
      });
      expect(geometry.ratio).toBeCloseTo(16 / 9, 2);
      expect(geometry.fits).toBe(true);
      expect(geometry.afterIntro).toBe(true);
      expect(geometry.beforeBuild).toBe(true);
      expect(geometry.overflow).toBe(false);
      await page.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
      await expect(section).toBeVisible();
      await section.getByRole('link').focus();
      await expect(section.getByRole('link')).toBeFocused();
      if (slug === 'read-temperature-dht22') {
        await expect(page.locator('h1')).toContainText('DHT11');
        await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', /\/guides\/read-temperature-dht22\.html$/);
      }
      expect(errors).toEqual([]);
    });
  }
}
