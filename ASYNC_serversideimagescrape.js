const puppeteer = require('puppeteer');
const fs = require('fs').promises;
const path = require('path');

////// CONFIGURATION //////
const targetRoute = 'US_36_WB' // make the same as target_route in pixel_processing.py
const jsonFileName = targetRoute + '_coordinates.json'
const zoom = 16; // set zoom level for Google Maps

// Function to generate Google Maps URL
function generateGoogleMapsUrl(lat, lng, zoom) {
    return `https://www.google.com/maps/@${lat},${lng},${zoom}z`;
}

// Function to capture screenshot for a given coordinate
async function captureScreenshot(browser, coord, zoom) {
    const { lat, lng } = coord;
    const page = await browser.newPage();
    await page.setViewport({ width: 360, height: 800 });
    const websiteUrl = generateGoogleMapsUrl(lat, lng, zoom);

    await page.goto(websiteUrl, { waitUntil: 'networkidle0' });

    const screenshotPath = `${targetRoute}_${lat}_${lng}_${zoom}x_360x800.png`;
    await page.screenshot({ path: screenshotPath });

    console.log(`Screenshot saved: ${screenshotPath}`);
    await page.close();
}

// Main function to read coordinates and capture screenshots
async function main() {
    const coordinatesFilePath = path.join(__dirname, jsonFileName);
    const coordinates = JSON.parse(await fs.readFile(coordinatesFilePath, 'utf8'));

    const browser = await puppeteer.launch();

    // Use Promise.all to handle multiple asynchronous operations concurrently
    await Promise.all(coordinates.map(coord => captureScreenshot(browser, coord, zoom)));

    console.log('All screenshots saved!');
    await browser.close();
}

main().catch(console.error);