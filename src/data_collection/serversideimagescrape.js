const puppeteer = require('puppeteer');
const fs = require('fs');

// Read the JSON file that takes the target route from "target_config.json"
fs.readFile('target_config.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading target_config.json:', err);
        return;
    }
    // Parse the JSON data
    const config = JSON.parse(data);
    const targetRoute = config.target_route;

    // THe name of the JSON file created by "scrape_lat_lng_by_clicking.py"
    const jsonFileName = targetRoute + '_coordinates.json'

    
    
    // Function to generate Google Maps URL from coordinates
    const zoom = 16; // Zoom level for Google Maps
    const generateGoogleMapsUrl = (lat, lng, zoom) => {
        return `https://www.google.com/maps/@${lat},${lng},${zoom}z/data=!5m1!1e1?authuser=0&entry=ttu`;
    };
    // Read coordinates from coordinates.json
    fs.readFile(jsonFileName, 'utf8', async (err, data) => {
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
            const websiteUrl = generateGoogleMapsUrl(lat, lng, zoom);

            // Open URL in current page. Wait until all network requests are finished.
            await page.goto(websiteUrl, { waitUntil: 'networkidle0' });

            // Capture screenshot.
            // ToDo: targetRoute needs to be dynamic
            const screenshotPath = `raw_traffic_images/${targetRoute}_${lat}_${lng}.png`;
            await page.screenshot({ path: screenshotPath });

            console.log(`Screenshot saved: ${screenshotPath}`);
        }
    console.log('All screenshots saved!');
        // Close the browser instance.
        await browser.close();
    });
});