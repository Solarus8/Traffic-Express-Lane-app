const fs = require('fs');
const path = require('path');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Absolute path to the JSON file
const jsonFilePath = path.join(__dirname, 'travelPathtest.json');

// Step 1: Read the JSON file
let data;
try {
    const jsonData = fs.readFileSync(jsonFilePath, 'utf8');
    data = JSON.parse(jsonData);
} catch (err) {
    if (err.code === 'ENOENT') {
        console.error(`Error: The file '${jsonFilePath}' was not found.`);
    } else if (err instanceof SyntaxError) {
        console.error(`Error: Failed to decode JSON - ${err.message}`);
    } else {
        console.error(`Error: ${err.message}`);
    }
    process.exit(1);
}

// Step 2: Extract latitude and longitude
const coordinates = [];
data.forEach(entry => {
    const coords = entry.coords || {};
    const latitude = coords.latitude;
    const longitude = coords.longitude;
    if (latitude !== undefined && longitude !== undefined) {
        coordinates.push({ latitude, longitude });
    } else {
        console.warn(`Warning: Missing latitude or longitude in entry: ${JSON.stringify(entry)}`);
    }
});

// Step 3: Write to CSV
const csvWriter = createCsvWriter({
    path: 'output_JS.csv',
    header: [
        { id: 'latitude', title: 'latitude' },
        { id: 'longitude', title: 'longitude' }
    ]
});

csvWriter.writeRecords(coordinates)
    .then(() => {
        console.log("CSV file 'output_JS.csv' created successfully.");
    })
    .catch(err => {
        console.error(`Error: Failed to write to CSV file - ${err.message}`);
    });