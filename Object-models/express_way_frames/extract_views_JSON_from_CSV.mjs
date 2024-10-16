import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import csv from 'csv-parser';

// Define __filename and __dirname for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const directory = __dirname;

async function processCSV(filePath) {
    return new Promise((resolve, reject) => {
        const vertices = [];
        let isFirstRow = true;

        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (row) => {
                if (isFirstRow) {
                    isFirstRow = false;
                    return;
                }

                const latitude = parseFloat(row.Latitude);
                const longitude = parseFloat(row.Longitude);

                if (!isNaN(latitude) && !isNaN(longitude)) {
                    vertices.push([latitude, longitude]);
                } else {
                    console.warn(`Invalid data in row: ${JSON.stringify(row)}`);
                }
            })
            .on('end', () => {
                resolve(vertices);
            })
            .on('error', (error) => {
                reject(error);
            });
    });
}

async function main() {
    const outputData = [];
    const files = fs.readdirSync(directory);
    for (const filename of files) {
        if (filename.endsWith('.csv')) {
            const filePath = path.join(directory, filename);
            try {
                const jsonData = await processCSV(filePath);
                outputData.push({
                    filename: filename,
                    vertices: jsonData
                });
            } catch (error) {
                console.error(`Error processing file ${filename}:`, error);
            }
        }
    }

    fs.writeFileSync(path.join(directory, 'output.json'), JSON.stringify(outputData, null, 4));
}

main().catch(error => {
    console.error('Error in main function:', error);
});