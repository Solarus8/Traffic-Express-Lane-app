const puppeteer = require('puppeteer');
const fs = require('fs');

// Function to generate Google Maps URL from coordinates
const generateGoogleMapsUrl = (lat, lng) => {
    return `https://www.google.com/maps/@${lat},${lng},16.5z/data=!5m1!1e1?authuser=0&entry=ttu`;
};

// Read coordinates from coordinates.json
fs.readFile('target_coordinates.json', 'utf8', async (err, data) => {
    if (err) {
        console.log('Error reading coordinates.json:', err);
        return;
    }

    const coordinates = JSON.parse(data);

    // Launch Puppeteer browser instance
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({ width: 360, height: 800 });

    for (const coord of coordinates) {
        const { lat, lng } = coord;
        const websiteUrl = generateGoogleMapsUrl(lat, lng);

        // Open URL in current page. Wait until all network requests are finished.
        await page.goto(websiteUrl, { waitUntil: 'networkidle0' });

        // Capture screenshot.
        const screenshotPath = `gmaps_${lat}_${lng}_360x800.png`;
        await page.screenshot({ path: screenshotPath });

        console.log(`Screenshot saved: ${screenshotPath}`);
    }
console.log('All screenshots saved!');
    // Close the browser instance.
    await browser.close();
});