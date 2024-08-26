import puppeteer from 'puppeteer'

const sleep = time => new Promise(resolve => setTimeout(resolve, time));

const browser = await puppeteer.launch({ headless: false, devtools: true });
const page = await browser.newPage();
await page.goto('http://localhost:8080/', { waitUntil: 'networkidle2' });

await page.locator('input[name=name]').fill('FizzBuzz101');

await Promise.all([
	page.waitForNavigation({ waitUntil: 'networkidle2' }),
	page.click('button')
]);

await page.evaluate(flag => {
	const w = window.open('about:blank', 'secret');
	const wrapper = document.createElement('div');
	wrapper.id = 'flag';
	const img = document.createElement('img');
	img.src = `/render/${flag}`;
	const shadow = wrapper.attachShadow({ mode: 'closed' });
	shadow.appendChild(img);
	w.document.body.appendChild(wrapper);
}, [process.env.FLAG || 'corctf{test_flag}']);

await sleep(1000);
await page.evaluate(() => {
	document.querySelector("button").click()
});

await sleep(30_000);
await browser.close();