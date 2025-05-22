# E-Bike Compare

A web application for crawling e-bike websites and comparing e-bike specifications side by side.

## Features

- Web crawler for fetching e-bike data from different websites
- Automatic product discovery from website catalogs
- Support for multiple languages per website
- Configurable CSS selectors for extracting product information
- CSV storage with historical data archiving
- Web interface for comparing e-bikes side by side
- Scheduled data updates (daily or on-demand)

## Project Structure

```
ebike-compare/
├── config/              # Configuration files
│   └── websites.py      # Website configuration
├── crawler/             # Web crawler modules
│   ├── crawler.py       # Main crawler logic
│   └── scheduler.py     # Scheduler for regular updates
├── data/                # Data storage
│   ├── current/         # Current CSV data files
│   └── archive/         # Historical CSV data files
├── webapp/              # Web application
│   ├── app.py           # Flask application
│   ├── static/          # Static assets
│   │   ├── css/         # CSS files
│   │   └── js/          # JavaScript files
│   └── templates/       # HTML templates
├── requirements.txt     # Python dependencies
├── start.sh             # Startup script for crawler and web app
├── start_scheduler.sh   # Startup script for scheduled updates
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ebike-compare.git
   cd ebike-compare
   ```

2. Make sure you have Conda installed:
   ```
   conda --version
   ```
   If Conda is not installed, follow the instructions at https://docs.conda.io/en/latest/miniconda.html

## Usage

### Quick Start

The easiest way to run the application is to use the provided startup script:

```
./start.sh
```

This script will:
1. Create a Conda environment if it doesn't exist
2. Install dependencies
3. Run the crawler once to collect initial data
4. Start the web application

Then open your browser and navigate to http://127.0.0.1:5000/

### Scheduled Updates

To run the crawler with scheduled daily updates:

```
./start_scheduler.sh
```

This will run the crawler immediately and then schedule it to run daily at midnight.

### Manual Execution

If you prefer to run components individually:

#### Running the Crawler

To run the crawler once:

```
cd ebike-compare
conda activate ebike-compare
python -m crawler.crawler
```

To run the crawler with the scheduler (runs immediately and then daily at midnight):

```
cd ebike-compare
conda activate ebike-compare
python -m crawler.scheduler
```

#### Running the Web Application

```
cd ebike-compare
conda activate ebike-compare
python -m webapp.app
```

Then open your browser and navigate to http://127.0.0.1:5000/

## Adding a New Website

To add a new website for crawling:

1. Open `config/websites.py`
2. Add a new entry to the `WEBSITES` dictionary with the required configuration:
   - `name`: Display name of the website
   - `base_url`: Base URL of the website
   - `product_url_template`: URL template for product pages
   - `languages`: List of supported languages
   - `discovery`: Configuration for finding products:
     - `url`: URL of the product listing page
     - `product_link_selector`: CSS selector for product links
     - `pagination_selector`: CSS selector for pagination links (optional)
   - `selectors`: CSS selectors for product attributes

## How Product Discovery Works

The crawler automatically discovers e-bike products from each website by:

1. Starting at the product listing page specified in the `discovery.url` configuration
2. Finding all product links using the CSS selector in `discovery.product_link_selector`
3. Extracting product IDs from the URLs
4. Following pagination links (if available) to discover more products
5. Crawling each product page for detailed information

This eliminates the need to manually specify product IDs in the configuration, making the system more dynamic and requiring less maintenance.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Flask](https://flask.palletsprojects.com/) for the web application
- [Bootstrap](https://getbootstrap.com/) for the UI components 