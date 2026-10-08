import { test, expect } from '@playwright/test';
import path from 'node:path';
const steps=['installing-arduino-ide-esp32','blink-led-esp32','button-led-control','read-temperature-dht22','connect-oled-esp32'];
test.beforeEach(async ({page})=>{await page.route('**/*',r=>new URL(r.request().url()).hostname==='127.0.0.1'?r.continue():r.fulfill({status:200,body:''}));});
async function open(page:any,url:string,theme:string){await page.goto(url);const b=page.getByRole('button',{name:'Reject optional',exact:true});if(await b.isVisible())await b.click();await page.evaluate((t:string)=>document.documentElement.setAttribute('data-theme',t),theme);}
for(const width of [320,768,1440])for(const theme of ['light','dark']){
 test(`complete beginner route ${width} ${theme}`,async({page})=>{
 await page.setViewportSize({width,height:900});await open(page,'/',theme);
 const start=page.getByRole('link',{name:'Start here: set up Arduino IDE',exact:true});await start.focus();await expect(start).toBeFocused();await page.keyboard.press('Enter');
 for(let i=0;i<steps.length;i++){
 await expect(page).toHaveURL(new RegExp(steps[i]+'.html$'));await page.evaluate(t=>document.documentElement.setAttribute('data-theme',t),theme);
 const nav=page.getByRole('navigation',{name:'Beginner route',exact:true});await expect(nav).toContainText(`Step ${i+1} of 5`); if(i>0) await expect(page.locator('.beginner-continue a')).toHaveAttribute('href',i<4?`/guides/${steps[i+1]}.html`:'/learning.html#display-basics');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
 const next=nav.locator('.beginner-next');await next.focus();await expect(next).toBeFocused();expect(await next.evaluate(el=>getComputedStyle(el).outlineStyle)).not.toBe('none');await page.keyboard.press('Enter');
 }
 await expect(page).toHaveURL(/learning.html#display-basics$/);await expect(page.locator('#display-basics')).toBeVisible();
 });
 for(const url of ['/','/guides.html','/learning.html'])test(`entry layout ${url} ${width} ${theme}`,async({page})=>{
 await page.setViewportSize({width,height:900});const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await open(page,url,theme);
 await expect(page.locator('h1')).toHaveCount(1);await expect(page.locator('.beginner-step')).toHaveCount(5);
 expect(await page.locator('.beginner-step h3 a').evaluateAll(es=>es.map(e=>e.getAttribute('href')))).toEqual(steps.map(s=>`/guides/${s}.html`));
 await expect(page.locator('.beginner-step').nth(3)).toContainText('DHT11');
 const link=page.locator('.beginner-step h3 a').first();await link.focus();await page.keyboard.press('Tab');await page.keyboard.press('Shift+Tab');await expect(link).toBeFocused();expect(await link.evaluate(el=>getComputedStyle(el).outlineStyle)).toBe('solid');
 for(const jump of await page.locator('.journey-jumps a[href^="#"]').all()){const href=(await jump.getAttribute('href'))!;await expect(page.locator(href)).toHaveCount(1);await jump.focus();await page.keyboard.press('Enter');await expect(page).toHaveURL(new RegExp(href+'$'));}
 await page.locator('.beginner-route').scrollIntoViewIfNeeded();expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
 // Poll settled theme colors; the existing stylesheet animates theme transitions.
 await expect.poll(async()=>page.locator('.beginner-step').first().evaluate(el=>{
   const lum=(rgb:string)=>{const v=rgb.match(/[\d.]+/g)!.slice(0,3).map(Number).map(n=>n/255).map(n=>n<=.04045?n/12.92:((n+.055)/1.055)**2.4);return .2126*v[0]+.7152*v[1]+.0722*v[2];};
   const bg=lum(getComputedStyle(el).backgroundColor);
   return Math.min(...[el,el.querySelector('h3 a')!,el.querySelector('p')!,el.querySelector('.meta')!].map(node=>{const fg=lum(getComputedStyle(node).color);return (Math.max(fg,bg)+.05)/(Math.min(fg,bg)+.05);}));
 })).toBeGreaterThanOrEqual(4.5);

 if(width===320){const toggle=page.locator('.nav-toggle');await toggle.focus();await page.keyboard.press('Enter');await expect(toggle).toHaveAttribute('aria-expanded','true');await expect(page.locator('.top-nav').getByRole('link',{name:'Guides',exact:true})).toBeVisible();await page.keyboard.press('Enter');await expect(toggle).toHaveAttribute('aria-expanded','false');}
 expect(errors).toEqual([]);if(process.env.BATCH5_QA_DIR){await page.locator('.beginner-route').evaluate(el=>el.scrollIntoView({block:'start'}));await page.screenshot({path:path.join(process.env.BATCH5_QA_DIR,`${url.replace(/[^a-z]/gi,'')||'home'}-${width}-${theme}.png`)});}
 });
}

for(const theme of ['light','dark'])for(const url of ['/projects/esp32-oled-weather-clock.html','/components/bme280.html','/guides/pull-up-vs-pull-down-resistors.html'])test(`preserved page ${url} ${theme}`,async({page})=>{
 await page.setViewportSize({width:320,height:900});await open(page,url,theme);await expect(page.locator('h1')).toHaveCount(1);await expect(page.locator('.beginner-route,.beginner-navigation,.beginner-continue')).toHaveCount(0);expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);await expect(page.locator('pre code').first()).toBeVisible();
});
