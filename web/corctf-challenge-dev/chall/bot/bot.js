const puppeteer = require("puppeteer");

const FLAG = process.env.FLAG || "corctf{test_flag}";

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

const path = require("path");
const ext = path.resolve(__dirname, "./extension/");

const visit = async (url) => {
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: "new",
            pipe: true,
            args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                `--disable-extensions-except=${ext}`,
                `--load-extension=${ext}`
            ],
            dumpio: true
        });

        const page = await browser.newPage();
        // NOTE: this is where the flag is on remote
        await page.goto("http://localhost:8080", { timeout: 5000, waitUntil: 'networkidle2' });

        page.evaluate((flag) => {
            document.cookie = "flag=" + flag;
        }, FLAG);

        // go to exploit page
        await page.goto(url, { timeout: 5000, waitUntil: 'networkidle2' });
        await sleep(10_000);

        await browser.close();
        browser = null;
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }
};

module.exports = { visit };