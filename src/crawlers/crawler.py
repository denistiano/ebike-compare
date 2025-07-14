"""
Modernized E-Bike Crawler for GitHub Actions

This crawler is designed to run in GitHub Actions environments.
It fetches e-bike data from manufacturer websites and saves to CSV files.
"""

import os
import csv
import json
import time
import logging
import datetime
import re
import hashlib
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
import shutil
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
import pandas as pd

# Import website configurations
from .config.websites import WEBSITES

# Configure logging for GitHub Actions
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # GitHub Actions captures stdout
)
logger = logging.getLogger("ebike_crawler")

# Define paths relative to repository root
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CURRENT_DATA_DIR = BASE_DIR / "data" / "current"
ARCHIVE_DATA_DIR = BASE_DIR / "data" / "archive"
WEB_DATA_DIR = BASE_DIR / "src" / "web" / "data"

def setup_directories():
    """Ensure all required directories exist."""
    CURRENT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)

def get_soup(url: str, retries: int = 3, delay: int = 2) -> Optional[BeautifulSoup]:
    """
    Fetch HTML content from a URL and parse it with BeautifulSoup.
    
    Args:
        url: URL to fetch
        retries: Number of retry attempts
        delay: Delay between retries in seconds
        
    Returns:
        BeautifulSoup object or None if failed
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.warning(f"Attempt {attempt+1}/{retries} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    
    logger.error(f"Failed to fetch {url} after {retries} attempts")
    return None

def extract_text(soup: BeautifulSoup, selector: str) -> str:
    """Extract text from an element using a CSS selector."""
    element = soup.select_one(selector)
    if element:
        return element.get_text(strip=True)
    return ""

def extract_attribute(soup: BeautifulSoup, selector: str, attribute: str) -> str:
    """Extract an attribute from an element using a CSS selector."""
    element = soup.select_one(selector)
    if element and element.has_attr(attribute):
        return element[attribute]
    return ""

def extract_multiple(soup: BeautifulSoup, selector: str, attribute: Optional[str] = None) -> List[str]:
    """Extract multiple elements or attributes using a CSS selector."""
    elements = soup.select(selector)
    if attribute:
        return [element[attribute] for element in elements if element.has_attr(attribute)]
    return [element.get_text(strip=True) for element in elements]

def extract_product_id_from_url(url: str, base_url: str, product_url_template: str) -> Optional[str]:
    """Extract the product ID from a product URL."""
    url = url.split('?')[0].rstrip('/')
    base_url = base_url.rstrip('/')
    
    parsed_url = urlparse(url)
    path = parsed_url.path
    
    if not url.startswith(('http://', 'https://')):
        url = urljoin(base_url, url)
        parsed_url = urlparse(url)
        path = parsed_url.path
    
    template_path = urlparse(product_url_template).path
    marker_match = re.search(r'\{product_id\}', template_path)
    
    if marker_match:
        marker_index = template_path.index('{product_id}')
        pattern_before = template_path[:marker_index]
        
        if pattern_before in path:
            product_id_start = path.index(pattern_before) + len(pattern_before)
            product_id = path[product_id_start:]
            product_id = product_id.rstrip('/')
            
            if product_id:
                logger.debug(f"Extracted product ID '{product_id}' from {url}")
                return product_id
    
    # Fallback method
    path_parts = path.strip('/').split('/')
    markers = ['products', 'bikes', 'p']
    for marker in markers:
        if marker in path_parts:
            marker_index = path_parts.index(marker)
            if marker_index < len(path_parts) - 1:
                product_id = '/'.join(path_parts[marker_index + 1:])
                logger.debug(f"Extracted product ID '{product_id}' from {url} using fallback method")
                return product_id
    
    logger.warning(f"Could not extract product ID from {url}")
    return None

def discover_product_ids(website_config: Dict[str, Any]) -> List[str]:
    """
    Discover product IDs by crawling product listing pages.
    """
    product_ids = set()
    discovery_config = website_config.get("discovery", {})
    
    if not discovery_config:
        logger.warning(f"No discovery configuration found for {website_config['name']}")
        return []
    
    discovery_url = discovery_config.get("url")
    if not discovery_url:
        logger.warning(f"No discovery URL found for {website_config['name']}")
        return []
    
    product_link_selector = discovery_config.get("product_link_selector")
    if not product_link_selector:
        logger.warning(f"No product link selector found for {website_config['name']}")
        return []
    
    logger.debug(f"Starting discovery for {website_config['name']} with URL: {discovery_url}")
    
    pagination_selector = discovery_config.get("pagination_selector")
    max_pages = 5  # Reduced for GitHub Actions
    pages_crawled = 0
    current_url = discovery_url
    
    base_url = website_config["base_url"]
    product_url_template = website_config["product_url_template"]
    
    logger.info(f"Starting product discovery for {website_config['name']} at {discovery_url}")
    
    while current_url and pages_crawled < max_pages:
        logger.debug(f"Crawling product listing page: {current_url}")
        
        soup = get_soup(current_url)
        if not soup:
            logger.error(f"Failed to get soup for {current_url}")
            break
        
        product_links = soup.select(product_link_selector)
        logger.debug(f"Found {len(product_links)} product links on page {current_url}")
        
        for link in product_links:
            href = link.get("href")
            if not href:
                continue
            
            if not href.startswith(("http://", "https://")):
                href = urljoin(base_url, href)
            
            product_id = extract_product_id_from_url(href, base_url, product_url_template)
            if product_id:
                logger.debug(f"Extracted product ID {product_id} from {href}")
                product_ids.add(product_id)
        
        # Find next page
        next_page = None
        if pagination_selector:
            next_page_link = soup.select_one(pagination_selector)
            if next_page_link and next_page_link.get("href"):
                next_page = next_page_link["href"]
                if not next_page.startswith(("http://", "https://")):
                    next_page = urljoin(base_url, next_page)
                logger.debug(f"Found next page link: {next_page}")
        
        current_url = next_page
        pages_crawled += 1
        time.sleep(2)  # Be nice to servers
    
    logger.info(f"Discovered {len(product_ids)} product IDs for {website_config['name']}")
    return list(product_ids)

def parse_product_page(soup: BeautifulSoup, selectors: Dict[str, str], product_id: str) -> Dict[str, Any]:
    """
    Parse a product page using the provided selectors.
    """
    product_data = {}
    
    # Extract basic product info
    for field in ["name", "price", "description"]:
        if field in selectors:
            value = extract_text(soup, selectors[field])
            if field == "price":
                # Clean price (remove currency symbols, commas, etc.)
                value = re.sub(r'[^\d.,]', '', value)
                try:
                    value = float(value.replace(',', ''))
                    product_data[field] = value
                except ValueError:
                    logger.warning(f"Could not parse price: {value}")
            else:
                product_data[field] = value
    
    # Extract specifications
    for field in ["battery", "motor_type", "max_speed", "range", "weight", "max_load"]:
        if field in selectors:
            value = extract_text(soup, selectors[field])
            if value:
                product_data[field] = value
    
    # Extract image URLs (store URLs directly, no local downloads)
    if "images" in selectors:
        images = []
        for img in soup.select(selectors["images"]):
            src = img.get('src', '')
            if src and src not in images:
                if src.startswith('//'):
                    src = 'https:' + src
                images.append(src)
            
            data_src = img.get('data-src', '')
            if data_src and data_src not in images:
                if data_src.startswith('//'):
                    data_src = 'https:' + data_src
                images.append(data_src)
        
        if images:
            product_data["images"] = images
    
    return product_data

def crawl_website(website_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Crawl a website for product data based on its configuration.
    """
    products = []
    website_name = website_config["name"]
    logger.info(f"Starting crawl for {website_name}")
    
    # Discover product IDs
    product_ids = discover_product_ids(website_config)
    
    if not product_ids:
        logger.warning(f"No product IDs discovered for {website_name}")
        return []
    
    # Limit products for GitHub Actions (avoid timeout)
    max_products = 10
    if len(product_ids) > max_products:
        product_ids = product_ids[:max_products]
        logger.info(f"Limiting to {max_products} products for {website_name}")
    
    for product_id in product_ids:
        for lang in website_config["languages"]:
            product_url = website_config["product_url_template"].format(product_id=product_id)
            
            if lang != website_config["languages"][0]:
                if "?" in product_url:
                    product_url += f"&lang={lang}"
                else:
                    product_url += f"?lang={lang}"
            
            logger.info(f"Crawling {product_url}")
            
            soup = get_soup(product_url)
            if not soup:
                continue
            
            product_data = parse_product_page(soup, website_config["selectors"], product_id)
            
            # Add metadata
            product_data["website"] = website_name
            product_data["product_id"] = product_id
            product_data["language"] = lang
            product_data["url"] = product_url
            product_data["crawl_date"] = datetime.datetime.now().isoformat()
            
            products.append(product_data)
            time.sleep(1)  # Be nice to servers
    
    logger.info(f"Completed crawl for {website_name}, found {len(products)} products")
    return products

def save_to_csv(products: List[Dict[str, Any]], website_key: str):
    """
    Save product data to CSV in both data directory and web directory.
    """
    if not products:
        logger.warning(f"No products to save for {website_key}")
        return
    
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"{website_key}_{date_str}.csv"
    
    # Save to data directory (for archival)
    data_filepath = CURRENT_DATA_DIR / filename
    if data_filepath.exists():
        archive_path = ARCHIVE_DATA_DIR / filename
        shutil.move(str(data_filepath), str(archive_path))
        logger.info(f"Archived existing file to {archive_path}")
    
    df = pd.DataFrame(products)
    df.to_csv(data_filepath, index=False)
    logger.info(f"Saved {len(products)} products to {data_filepath}")
    
    # Also save to web directory (for static site)
    web_filepath = WEB_DATA_DIR / filename
    df.to_csv(web_filepath, index=False)
    logger.info(f"Saved {len(products)} products to {web_filepath}")

def run_crawler():
    """Main function to run the crawler for all configured websites."""
    logger.info("Starting e-bike crawler run in GitHub Actions")
    
    setup_directories()
    
    for website_key, website_config in WEBSITES.items():
        try:
            logger.info(f"Processing website: {website_key}")
            products = crawl_website(website_config)
            logger.info(f"Found {len(products)} products for {website_key}")
            save_to_csv(products, website_key)
        except Exception as e:
            logger.error(f"Error crawling {website_key}: {e}", exc_info=True)
    
    logger.info("Crawler run completed")

if __name__ == "__main__":
    run_crawler() 