/**
 * E-Bike Compare - Comparison Page
 * 
 * This handles the bike comparison functionality for the static site.
 */

class EBikeCompare {
    constructor() {
        this.allBikes = [];
        this.filteredBikes = [];
        this.selectedBikes = [];
        this.maxSelection = 4;
        
        this.init();
    }

    async init() {
        try {
            await this.loadBikeData();
            this.setupEventListeners();
            this.populateFilters();
            this.displayBikeSelection();
            this.checkUrlParams();
        } catch (error) {
            console.error('Failed to initialize compare app:', error);
            this.showError('Failed to load bike data. Please try again later.');
        }
    }

    async loadBikeData() {
        const loadingIndicator = document.getElementById('loading-indicator');
        const selectionSection = document.getElementById('selection-section');
        
        try {
            // Try to discover available CSV files
            const csvUrls = await csvParser.discoverCSVFiles('data');
            
            if (csvUrls.length === 0) {
                // Fallback: try to load from existing data
                const existingData = await this.loadExistingData();
                this.allBikes = existingData;
            } else {
                // Load discovered CSV files
                const rawData = await csvParser.loadMultipleCSVs(csvUrls);
                this.allBikes = this.processRawData(rawData);
            }

            this.filteredBikes = [...this.allBikes];
            
            loadingIndicator.style.display = 'none';
            selectionSection.style.display = 'block';
            
            console.log(`Loaded ${this.allBikes.length} bikes for comparison`);
        } catch (error) {
            console.error('Error loading bike data:', error);
            throw error;
        }
    }

    async loadExistingData() {
        // Try to load from existing CSV files
        const possibleFiles = [
            'data/aventon_20250523.csv',
            'data/cube_bikes_20250523.csv',
            'data/engwe_eu_20250523.csv',
            'data/engwe_us_20250523.csv',
            'data/fiido_20250523.csv',
            'data/lectric_ebikes_20250523.csv',
            'data/rad_power_bikes_us_20250523.csv'
        ];

        const combinedData = [];
        for (const file of possibleFiles) {
            try {
                const data = await csvParser.loadCSV(file);
                combinedData.push(...data);
            } catch (error) {
                console.warn(`Could not load ${file}:`, error);
            }
        }

        return this.processRawData(combinedData);
    }

    processRawData(rawData) {
        return rawData.map((bike, index) => {
            // Create a unique ID
            const id = `${bike.website || 'unknown'}_${bike.product_id || index}_${bike.language || 'en'}`;
            
            // Process images
            let images = [];
            if (bike.images) {
                try {
                    if (bike.images.startsWith('[')) {
                        images = JSON.parse(bike.images);
                    } else {
                        images = bike.images.split(',').map(img => img.trim()).filter(img => img);
                    }
                } catch (error) {
                    images = bike.images ? [bike.images] : [];
                }
            }

            // Clean and process price
            let price = null;
            if (bike.price && bike.price !== 'N/A' && bike.price !== '') {
                const priceStr = bike.price.toString().replace(/[^\d.,]/g, '');
                const priceNum = parseFloat(priceStr.replace(/,/g, ''));
                if (!isNaN(priceNum)) {
                    price = priceNum;
                }
            }

            return {
                id,
                name: bike.name || 'Unnamed Bike',
                price,
                description: bike.description || '',
                website: bike.website || 'Unknown',
                manufacturer: this.extractManufacturer(bike.website),
                product_id: bike.product_id || '',
                language: bike.language || 'en',
                url: bike.url || '',
                crawl_date: bike.crawl_date || '',
                battery: bike.battery || '',
                motor_type: bike.motor_type || '',
                max_speed: bike.max_speed || '',
                range: bike.range || '',
                weight: bike.weight || '',
                max_load: bike.max_load || '',
                images: images
            };
        }).filter(bike => bike.name && bike.name !== 'Unnamed Bike');
    }

    extractManufacturer(website) {
        if (!website) return 'Unknown';
        
        const manufacturerMap = {
            'Trek International': 'Trek',
            'Specialized USA': 'Specialized',
            'Cube Bikes': 'Cube',
            'Riese & Müller': 'Riese & Müller',
            'Haibike': 'Haibike',
            'Engwe US': 'Engwe',
            'Engwe EU': 'Engwe',
            'Fiido': 'Fiido',
            'Rad Power Bikes (US)': 'Rad Power Bikes',
            'Aventon': 'Aventon',
            'Lectric eBikes': 'Lectric'
        };

        return manufacturerMap[website] || website;
    }

    setupEventListeners() {
        // Filter controls
        document.getElementById('manufacturer-filter').addEventListener('change', (e) => {
            this.applyFilters();
        });

        document.getElementById('search-input').addEventListener('input', (e) => {
            this.applyFilters();
        });

        // Compare button
        document.getElementById('compare-btn').addEventListener('click', () => {
            this.showComparison();
        });

        // New comparison button
        document.getElementById('new-comparison-btn').addEventListener('click', () => {
            this.resetComparison();
        });
    }

    populateFilters() {
        // Populate manufacturer filter
        const manufacturers = [...new Set(this.allBikes.map(bike => bike.manufacturer))].sort();
        const manufacturerSelect = document.getElementById('manufacturer-filter');
        
        manufacturers.forEach(manufacturer => {
            const option = document.createElement('option');
            option.value = manufacturer;
            option.textContent = manufacturer;
            manufacturerSelect.appendChild(option);
        });
    }

    applyFilters() {
        const manufacturerFilter = document.getElementById('manufacturer-filter').value;
        const searchFilter = document.getElementById('search-input').value.toLowerCase();

        this.filteredBikes = this.allBikes.filter(bike => {
            // Manufacturer filter
            if (manufacturerFilter && bike.manufacturer !== manufacturerFilter) {
                return false;
            }

            // Search filter
            if (searchFilter) {
                const searchableText = [
                    bike.name,
                    bike.description,
                    bike.manufacturer
                ].join(' ').toLowerCase();
                
                if (!searchableText.includes(searchFilter)) {
                    return false;
                }
            }

            return true;
        });

        this.displayBikeSelection();
    }

    displayBikeSelection() {
        const grid = document.getElementById('bike-selection-grid');
        grid.innerHTML = '';

        if (this.filteredBikes.length === 0) {
            grid.innerHTML = `
                <div class="col-12">
                    <div class="text-center py-4">
                        <i class="bi bi-search display-4 text-muted"></i>
                        <h4>No bikes found</h4>
                        <p class="text-muted">Try adjusting your filters.</p>
                    </div>
                </div>
            `;
            return;
        }

        // Display bikes (limit to 20 for performance)
        const displayBikes = this.filteredBikes.slice(0, 20);
        
        displayBikes.forEach(bike => {
            const col = document.createElement('div');
            col.className = 'col-md-6 col-lg-4 mb-3';

            const isSelected = this.selectedBikes.some(selected => selected.id === bike.id);
            const isDisabled = this.selectedBikes.length >= this.maxSelection && !isSelected;

            // Format price
            let priceDisplay = 'Price not available';
            if (bike.price) {
                priceDisplay = `$${bike.price.toLocaleString()}`;
            }

            col.innerHTML = `
                <div class="card h-100 ${isSelected ? 'border-primary' : ''} ${isDisabled ? 'opacity-50' : ''}">
                    <div class="card-body">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="bike-${bike.id}" 
                                   ${isSelected ? 'checked' : ''} ${isDisabled ? 'disabled' : ''}
                                   onchange="window.ebikeCompare.toggleBike('${bike.id}')">
                            <label class="form-check-label w-100" for="bike-${bike.id}">
                                <h6 class="card-title text-truncate" title="${bike.name}">${bike.name}</h6>
                                <p class="card-subtitle text-muted small">${bike.manufacturer}</p>
                                <p class="text-primary fw-bold mb-2">${priceDisplay}</p>
                                <div class="small">
                                    ${bike.battery ? `<div><strong>Battery:</strong> ${bike.battery}</div>` : ''}
                                    ${bike.motor_type ? `<div><strong>Motor:</strong> ${bike.motor_type}</div>` : ''}
                                </div>
                            </label>
                        </div>
                    </div>
                </div>
            `;

            grid.appendChild(col);
        });

        if (this.filteredBikes.length > 20) {
            const moreCol = document.createElement('div');
            moreCol.className = 'col-12';
            moreCol.innerHTML = `
                <div class="text-center py-3">
                    <p class="text-muted">Showing first 20 bikes. Use filters to narrow down results.</p>
                </div>
            `;
            grid.appendChild(moreCol);
        }
    }

    toggleBike(bikeId) {
        const bike = this.allBikes.find(b => b.id === bikeId);
        if (!bike) return;

        const existingIndex = this.selectedBikes.findIndex(b => b.id === bikeId);
        
        if (existingIndex >= 0) {
            // Remove bike
            this.selectedBikes.splice(existingIndex, 1);
        } else if (this.selectedBikes.length < this.maxSelection) {
            // Add bike
            this.selectedBikes.push(bike);
        }

        this.updateSelectedBikesDisplay();
        this.updateCompareButton();
        this.displayBikeSelection(); // Refresh to update disabled states
    }

    updateSelectedBikesDisplay() {
        const selectedSection = document.getElementById('selected-bikes');
        const selectedList = document.getElementById('selected-bikes-list');

        if (this.selectedBikes.length === 0) {
            selectedSection.style.display = 'none';
            return;
        }

        selectedSection.style.display = 'block';
        selectedList.innerHTML = '';

        this.selectedBikes.forEach(bike => {
            const badge = document.createElement('span');
            badge.className = 'badge bg-primary';
            badge.innerHTML = `
                ${bike.name} 
                <button type="button" class="btn-close btn-close-white" 
                        onclick="window.ebikeCompare.toggleBike('${bike.id}')" 
                        aria-label="Remove"></button>
            `;
            selectedList.appendChild(badge);
        });
    }

    updateCompareButton() {
        const compareBtn = document.getElementById('compare-btn');
        compareBtn.disabled = this.selectedBikes.length < 2;
        compareBtn.textContent = this.selectedBikes.length < 2 
            ? 'Select at least 2 bikes to compare'
            : `Compare ${this.selectedBikes.length} Bikes`;
    }

    showComparison() {
        if (this.selectedBikes.length < 2) return;

        const selectionSection = document.getElementById('selection-section');
        const comparisonResults = document.getElementById('comparison-results');
        
        selectionSection.style.display = 'none';
        comparisonResults.style.display = 'block';

        this.generateComparisonTable();
        
        // Scroll to comparison
        comparisonResults.scrollIntoView({ behavior: 'smooth' });
    }

    generateComparisonTable() {
        const table = document.getElementById('comparison-table');
        table.innerHTML = '';

        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');

        // Header row
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = '<th>Specification</th>';
        this.selectedBikes.forEach(bike => {
            headerRow.innerHTML += `<th>${bike.name}</th>`;
        });
        thead.appendChild(headerRow);

        // Data rows
        const specs = [
            { key: 'manufacturer', label: 'Manufacturer' },
            { key: 'price', label: 'Price', format: (value) => value ? `$${value.toLocaleString()}` : 'N/A' },
            { key: 'battery', label: 'Battery' },
            { key: 'motor_type', label: 'Motor Type' },
            { key: 'max_speed', label: 'Max Speed' },
            { key: 'range', label: 'Range' },
            { key: 'weight', label: 'Weight' },
            { key: 'max_load', label: 'Max Load' },
            { key: 'url', label: 'Official Link', format: (value) => value ? `<a href="${value}" target="_blank" class="btn btn-outline-primary btn-sm">View</a>` : 'N/A' }
        ];

        specs.forEach(spec => {
            const row = document.createElement('tr');
            row.innerHTML = `<td class="fw-bold">${spec.label}</td>`;
            
            this.selectedBikes.forEach(bike => {
                const value = bike[spec.key] || 'N/A';
                const displayValue = spec.format ? spec.format(value) : value;
                row.innerHTML += `<td>${displayValue}</td>`;
            });
            
            tbody.appendChild(row);
        });

        table.appendChild(thead);
        table.appendChild(tbody);
    }

    resetComparison() {
        const selectionSection = document.getElementById('selection-section');
        const comparisonResults = document.getElementById('comparison-results');
        
        comparisonResults.style.display = 'none';
        selectionSection.style.display = 'block';
        
        // Clear selections
        this.selectedBikes = [];
        this.updateSelectedBikesDisplay();
        this.updateCompareButton();
        this.displayBikeSelection();
        
        // Scroll to selection
        selectionSection.scrollIntoView({ behavior: 'smooth' });
    }

    checkUrlParams() {
        // Check if bikes are specified in URL
        const urlParams = new URLSearchParams(window.location.search);
        const bikeIds = urlParams.get('bikes');
        
        if (bikeIds) {
            const ids = bikeIds.split(',');
            ids.forEach(id => {
                const bike = this.allBikes.find(b => b.id === id);
                if (bike && this.selectedBikes.length < this.maxSelection) {
                    this.selectedBikes.push(bike);
                }
            });
            
            if (this.selectedBikes.length >= 2) {
                this.updateSelectedBikesDisplay();
                this.updateCompareButton();
                this.showComparison();
            }
        }
    }

    showError(message) {
        const selectionSection = document.getElementById('selection-section');
        const loadingIndicator = document.getElementById('loading-indicator');
        
        loadingIndicator.style.display = 'none';
        
        selectionSection.innerHTML = `
            <div class="col-12">
                <div class="error-message">
                    <h3><i class="bi bi-exclamation-triangle"></i> Error</h3>
                    <p>${message}</p>
                    <button class="btn btn-primary" onclick="location.reload()">Retry</button>
                </div>
            </div>
        `;
        selectionSection.style.display = 'block';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.ebikeCompare = new EBikeCompare();
}); 