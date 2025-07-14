/**
 * CSV Parser Utility for E-Bike Compare
 * 
 * This module handles loading and parsing CSV files containing bike data.
 */

class CSVParser {
    constructor() {
        this.cache = new Map();
    }

    /**
     * Parse CSV text into array of objects
     * @param {string} csvText - Raw CSV text
     * @returns {Array} Array of objects with headers as keys
     */
    parseCSV(csvText) {
        const lines = csvText.split('\n').filter(line => line.trim());
        if (lines.length < 2) return [];

        const headers = this.parseCSVLine(lines[0]);
        const data = [];

        for (let i = 1; i < lines.length; i++) {
            const values = this.parseCSVLine(lines[i]);
            if (values.length === headers.length) {
                const row = {};
                headers.forEach((header, index) => {
                    row[header.trim()] = values[index]?.trim() || '';
                });
                data.push(row);
            }
        }

        return data;
    }

    /**
     * Parse a single CSV line, handling quoted values
     * @param {string} line - CSV line
     * @returns {Array} Array of values
     */
    parseCSVLine(line) {
        const result = [];
        let current = '';
        let inQuotes = false;
        let i = 0;

        while (i < line.length) {
            const char = line[i];
            const nextChar = line[i + 1];

            if (char === '"') {
                if (inQuotes && nextChar === '"') {
                    current += '"';
                    i += 2;
                    continue;
                }
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                result.push(current);
                current = '';
            } else {
                current += char;
            }
            i++;
        }

        result.push(current);
        return result;
    }

    /**
     * Load CSV file from URL
     * @param {string} url - URL to CSV file
     * @returns {Promise<Array>} Promise resolving to parsed data
     */
    async loadCSV(url) {
        // Check cache first
        if (this.cache.has(url)) {
            return this.cache.get(url);
        }

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const csvText = await response.text();
            const data = this.parseCSV(csvText);
            
            // Cache the result
            this.cache.set(url, data);
            
            return data;
        } catch (error) {
            console.error(`Error loading CSV from ${url}:`, error);
            throw error;
        }
    }

    /**
     * Load multiple CSV files
     * @param {Array<string>} urls - Array of CSV URLs
     * @returns {Promise<Array>} Promise resolving to combined data
     */
    async loadMultipleCSVs(urls) {
        try {
            const promises = urls.map(url => this.loadCSV(url));
            const results = await Promise.allSettled(promises);
            
            const combinedData = [];
            const errors = [];

            results.forEach((result, index) => {
                if (result.status === 'fulfilled') {
                    combinedData.push(...result.value);
                } else {
                    errors.push({ url: urls[index], error: result.reason });
                    console.error(`Failed to load ${urls[index]}:`, result.reason);
                }
            });

            if (errors.length > 0) {
                console.warn(`${errors.length} CSV files failed to load:`, errors);
            }

            return combinedData;
        } catch (error) {
            console.error('Error loading multiple CSVs:', error);
            throw error;
        }
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }

    /**
     * Get available CSV files by detecting them from a directory
     * This is a fallback method when we don't know the exact filenames
     * @param {string} baseUrl - Base URL of the data directory
     * @returns {Promise<Array>} Promise resolving to array of CSV URLs
     */
    async discoverCSVFiles(baseUrl) {
        // Since we can't list directory contents in a browser,
        // we'll try common patterns based on known manufacturers
        const manufacturers = [
            'trek_international',
            'specialized_usa', 
            'cube_bikes',
            'riese_muller',
            'haibike',
            'engwe_us',
            'engwe_eu',
            'fiido',
            'rad_power_bikes_us',
            'aventon',
            'lectric_ebikes'
        ];

        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        
        const dates = [
            today.toISOString().slice(0, 10).replace(/-/g, ''),
            yesterday.toISOString().slice(0, 10).replace(/-/g, '')
        ];

        const possibleUrls = [];
        
        // Generate possible filename combinations
        manufacturers.forEach(manufacturer => {
            dates.forEach(date => {
                possibleUrls.push(`${baseUrl}/${manufacturer}_${date}.csv`);
            });
        });

        // Test which URLs actually exist
        const existingUrls = [];
        const testPromises = possibleUrls.map(async (url) => {
            try {
                const response = await fetch(url, { method: 'HEAD' });
                if (response.ok) {
                    existingUrls.push(url);
                }
            } catch (error) {
                // Ignore errors - file doesn't exist
            }
        });

        await Promise.all(testPromises);
        return existingUrls;
    }
}

// Global instance
window.csvParser = new CSVParser(); 