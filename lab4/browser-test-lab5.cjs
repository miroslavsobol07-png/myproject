// Uruchom przy działającym serwerze: node lab4/browser-test-lab5.cjs
// Dodatkowo potrzebne są Playwright i Edge (nie są zależnościami aplikacji).
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
    const output = process.env.LAB5_SCREENSHOTS || path.join(__dirname, 'materialy-lab5', 'zrzuty');
    fs.mkdirSync(output, {recursive: true});
    const browser = await chromium.launch({channel: 'msedge', headless: true});
    try {
        const page = await browser.newPage({viewport: {width: 1360, height: 1100}});
        const errors = [];
        page.on('pageerror', error => errors.push(error.message));
        await page.goto('http://127.0.0.1:8005/lab4/');
        await page.waitForFunction(() => !document.querySelector('#load').disabled);
        assert.equal(await page.locator('.book').count(), 6);
        assert.equal(await page.locator('#filters select').count(), 4);
        assert.equal(await page.locator('.rating').first().textContent(), 'Ocena: 4 / 5');
        await page.screenshot({path: path.join(output, '01_katalog.png'), fullPage: true});
        const navigationStart = await page.evaluate(() => performance.timeOrigin);
        async function load(count) {
            await page.locator('#load').click();
            await page.waitForFunction(() => !document.querySelector('#load').disabled);
            assert.equal(await page.locator('.book').count(), count);
            assert.equal(await page.evaluate(() => performance.timeOrigin), navigationStart);
        }
        await page.locator('#available').selectOption('true');
        await page.locator('#sort').selectOption('-rating');
        await load(4);
        assert.equal(await page.locator('.book h3').first().textContent(), 'Hobbit');
        assert.equal(await page.locator('.unavailable').count(), 0);
        await page.screenshot({path: path.join(output, '02_filtry.png'), fullPage: true});
        const apiUrl = await page.locator('#json-link').getAttribute('href');
        const apiResponse = await page.request.get('http://127.0.0.1:8005' + apiUrl);
        const data = await apiResponse.json();
        assert.equal(data.items.length, 4);
        assert(data.items.every(book => book.available && book.rating >= 4));
        fs.writeFileSync(path.join(output, '..', 'odpowiedz_API.json'), JSON.stringify(data, null, 2));
        const apiPage = await browser.newPage({viewport: {width: 1200, height: 1000}});
        await apiPage.goto('http://127.0.0.1:8005' + apiUrl);
        await apiPage.screenshot({path: path.join(output, '03_json.png'), fullPage: true});
        await apiPage.close();
        // Limit pozostaje dostępny bezpośrednio w API.
        const limited = await page.request.get('http://127.0.0.1:8005/lab4/api/ksiazki/?min_rating=4&sort=-rating&limit=3');
        assert.equal((await limited.json()).items.length, 3);
        await page.locator('#genre').selectOption('Fantasy');
        await page.locator('#min-rating').selectOption('5');
        await load(1);
        assert.equal(await page.locator('.book h3').textContent(), 'Hobbit');
        await page.locator('#genre').selectOption('Powieść');
        await load(0);
        assert.match(await page.locator('#status').textContent(), /Brak książek/);
        await page.locator('#genre').selectOption('');
        await page.locator('#min-rating').selectOption('');
        await page.locator('#available').selectOption('');
        await page.locator('#sort').selectOption('title');
        await load(6);
        await page.setViewportSize({width: 390, height: 844});
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
        await page.screenshot({path: path.join(output, '04_telefon.png'), fullPage: true});
        // Awaria sieci: komunikat, odblokowanie kontrolek i ponowna próba.
        await page.route('**/api/ksiazki/**', route => route.abort());
        await load(0);
        assert.match(await page.locator('#status').textContent(), /Nie udało się/);
        assert.equal(await page.locator('#books').getAttribute('aria-busy'), 'false');
        await page.unroute('**/api/ksiazki/**');
        await load(6);
        assert.deepEqual(errors, []);
        console.log('PASS: 6 books, four selectors, combined availability/genre/rating filters, sorting, API limit, JSON, empty results, mobile, network recovery, no page reload or JS errors.');
    } finally {
        await browser.close();
    }
})().catch(error => {console.error(error); process.exit(1);});
