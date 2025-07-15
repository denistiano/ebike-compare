/**
 * E-Bike Compare - Main Application
 * 
 * This is the main JavaScript application for the static e-bike comparison site.
 * It handles loading bike data from CSV files, filtering, sorting, and displaying results.
 */

class EBikeApp {
    constructor() {
        this.allBikes = [];
        this.filteredBikes = [];
        this.currentPage = 1;
        this.itemsPerPage = 12;
        this.filters = {
            manufacturer: '',
            priceRange: '',
            search: ''
        };
        this.sortBy = 'name';
        
        this.init();
    }

    async init() {
        try {
            await this.loadBikeData();
            this.setupEventListeners();
            this.populateFilters();
            this.applyFilters();
            this.displayBikes();
        } catch (error) {
            console.error('Failed to initialize app:', error);
            this.showError('Failed to load bike data. Please try again later.');
        }
    }

    async loadBikeData() {
        const loadingIndicator = document.getElementById('loading-indicator');
        const controlsSection = document.getElementById('controls-section');
        
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
            controlsSection.style.display = 'block';
            
            console.log(`Loaded ${this.allBikes.length} bikes from ${csvUrls.length} sources`);
        } catch (error) {
            console.error('Error loading bike data:', error);
            throw error;
        }
    }

    async loadExistingData() {
        // Try to load from existing CSV files in the data directory
        // This is a fallback when discovery fails
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
                    // Try to parse as JSON array
                    if (bike.images.startsWith('[')) {
                        images = JSON.parse(bike.images);
                    } else {
                        // Split by comma if it's a string
                        images = bike.images.split(',').map(img => img.trim()).filter(img => img);
                    }
                } catch (error) {
                    // If parsing fails, treat as single image
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
            this.filters.manufacturer = e.target.value;
            this.applyFilters();
        });

        document.getElementById('price-filter').addEventListener('change', (e) => {
            this.filters.priceRange = e.target.value;
            this.applyFilters();
        });

        document.getElementById('sort-filter').addEventListener('change', (e) => {
            this.sortBy = e.target.value;
            this.sortBikes();
            this.displayBikes();
        });

        document.getElementById('search-input').addEventListener('input', (e) => {
            this.filters.search = e.target.value;
            this.applyFilters();
        });

        document.getElementById('clear-filters').addEventListener('click', () => {
            this.clearFilters();
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
        this.filteredBikes = this.allBikes.filter(bike => {
            // Manufacturer filter
            if (this.filters.manufacturer && bike.manufacturer !== this.filters.manufacturer) {
                return false;
            }

            // Price filter
            if (this.filters.priceRange && bike.price) {
                const [min, max] = this.filters.priceRange.split('-').map(Number);
                if (bike.price < min || bike.price > max) {
                    return false;
                }
            }

            // Search filter
            if (this.filters.search) {
                const searchTerm = this.filters.search.toLowerCase();
                const searchableText = [
                    bike.name,
                    bike.description,
                    bike.manufacturer,
                    bike.battery,
                    bike.motor_type
                ].join(' ').toLowerCase();
                
                if (!searchableText.includes(searchTerm)) {
                    return false;
                }
            }

            return true;
        });

        this.sortBikes();
        this.currentPage = 1;
        this.displayBikes();
        this.updateResultsSummary();
    }

    sortBikes() {
        this.filteredBikes.sort((a, b) => {
            switch (this.sortBy) {
                case 'name':
                    return a.name.localeCompare(b.name);
                case 'price-low':
                    return (a.price || 999999) - (b.price || 999999);
                case 'price-high':
                    return (b.price || 0) - (a.price || 0);
                case 'manufacturer':
                    return a.manufacturer.localeCompare(b.manufacturer);
                default:
                    return 0;
            }
        });
    }

    displayBikes() {
        const container = document.getElementById('bikes-container');
        const resultsSection = document.getElementById('results-summary');
        const paginationSection = document.getElementById('pagination-section');
        
        container.innerHTML = '';

        if (this.filteredBikes.length === 0) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="empty-state">
                        <i class="bi bi-search"></i>
                        <h3>No bikes found</h3>
                        <p>Try adjusting your filters or search terms.</p>
                    </div>
                </div>
            `;
            resultsSection.style.display = 'none';
            paginationSection.style.display = 'none';
            return;
        }

        // Calculate pagination
        const totalPages = Math.ceil(this.filteredBikes.length / this.itemsPerPage);
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = Math.min(startIndex + this.itemsPerPage, this.filteredBikes.length);

        // Display bikes for current page
        for (let i = startIndex; i < endIndex; i++) {
            const bike = this.filteredBikes[i];
            const bikeCard = this.createBikeCard(bike);
            container.appendChild(bikeCard);
        }

        // Add fade-in animation
        container.classList.add('fade-in');

        resultsSection.style.display = 'block';
        paginationSection.style.display = totalPages > 1 ? 'block' : 'none';
        
        if (totalPages > 1) {
            this.updatePagination(totalPages);
        }
    }

    createBikeCard(bike) {
        const col = document.createElement('div');
        col.className = 'col-md-4 mb-4';

        // Format price
        let priceDisplay = 'Price not available';
        if (bike.price) {
            priceDisplay = `$${bike.price.toLocaleString()}`;
        }

        // Get main image
        let imageHtml = '<div class="no-image">No image available</div>';
        if (bike.images && bike.images.length > 0) {
            imageHtml = `<img src="${bike.images[0]}" class="card-img-top bike-card-image" alt="${bike.name}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=&quot;no-image&quot;>Image not available</div>'">`;
        }

        col.innerHTML = `
            <div class="card h-100 bike-card">
                <div class="data-badge">Latest</div>
                ${imageHtml}
                <div class="card-header">
                    <h5 class="card-title text-truncate" title="${bike.name}">${bike.name}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">${bike.manufacturer}</h6>
                </div>
                <div class="card-body">
                    <p class="price-highlight mb-3">${priceDisplay}</p>
                    <div class="card-text">
                        ${bike.battery ? `<div><span class="attribute-label">Battery:</span> ${bike.battery}</div>` : ''}
                        ${bike.motor_type ? `<div><span class="attribute-label">Motor:</span> ${bike.motor_type}</div>` : ''}
                        ${bike.max_speed ? `<div><span class="attribute-label">Max Speed:</span> ${bike.max_speed}</div>` : ''}
                        ${bike.range ? `<div><span class="attribute-label">Range:</span> ${bike.range}</div>` : ''}
                    </div>
                    <div class="mt-3">
                        <a href="compare.html?bikes=${bike.id}" class="btn btn-primary btn-sm">
                            <i class="bi bi-bar-chart"></i> Compare
                        </a>
                        ${bike.url ? `<a href="${bike.url}" target="_blank" class="btn btn-outline-secondary btn-sm ms-2">
                            <i class="bi bi-box-arrow-up-right"></i> View
                        </a>` : ''}
                    </div>
                </div>
            </div>
        `;

        return col;
    }

    updateResultsSummary() {
        const resultsCount = document.getElementById('results-count');
        const sourcesCount = document.getElementById('sources-count');
        
        const uniqueManufacturers = new Set(this.filteredBikes.map(bike => bike.manufacturer)).size;
        
        resultsCount.textContent = this.filteredBikes.length;
        sourcesCount.textContent = uniqueManufacturers;
    }

    updatePagination(totalPages) {
        const pagination = document.getElementById('pagination');
        pagination.innerHTML = '';

        // Previous button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${this.currentPage === 1 ? 'disabled' : ''}`;
        prevLi.innerHTML = `<a class="page-link" href="#" data-page="${this.currentPage - 1}">Previous</a>`;
        pagination.appendChild(prevLi);

        // Page numbers
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
            const li = document.createElement('li');
            li.className = `page-item ${i === this.currentPage ? 'active' : ''}`;
            li.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
            pagination.appendChild(li);
        }

        // Next button
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${this.currentPage === totalPages ? 'disabled' : ''}`;
        nextLi.innerHTML = `<a class="page-link" href="#" data-page="${this.currentPage + 1}">Next</a>`;
        pagination.appendChild(nextLi);

        // Add click handlers
        pagination.addEventListener('click', (e) => {
            e.preventDefault();
            if (e.target.classList.contains('page-link') && !e.target.parentElement.classList.contains('disabled')) {
                const page = parseInt(e.target.dataset.page);
                if (page >= 1 && page <= totalPages) {
                    this.currentPage = page;
                    this.displayBikes();
                    // Scroll to top
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            }
        });
    }

    clearFilters() {
        this.filters = {
            manufacturer: '',
            priceRange: '',
            search: ''
        };

        document.getElementById('manufacturer-filter').value = '';
        document.getElementById('price-filter').value = '';
        document.getElementById('search-input').value = '';

        this.applyFilters();
    }

    showError(message) {
        const container = document.getElementById('bikes-container');
        const loadingIndicator = document.getElementById('loading-indicator');
        
        loadingIndicator.style.display = 'none';
        
        container.innerHTML = `
            <div class="col-12">
                <div class="error-message">
                    <h3><i class="bi bi-exclamation-triangle"></i> Error</h3>
                    <p>${message}</p>
                    <button class="btn btn-primary" onclick="location.reload()">Retry</button>
                </div>
            </div>
        `;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.ebikeApp = new EBikeApp();
}); 