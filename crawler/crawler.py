"""
Main crawler module for fetching ebike data from configured websites.
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
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.websites import WEBSITES

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ebike_crawler")

# Define paths
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CURRENT_DATA_DIR = BASE_DIR / "data" / "current"
ARCHIVE_DATA_DIR = BASE_DIR / "data" / "archive"
IMAGES_DIR = BASE_DIR / "webapp" / "static" / "images" / "bikes"
IMAGES_ARCHIVE_DIR = BASE_DIR / "data" / "archive" / "images"

def setup_directories():
    """Ensure all required directories exist."""
    CURRENT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

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
    """
    Extract the product ID from a product URL.
    
    Args:
        url: Product URL
        base_url: Base URL of the website
        product_url_template: URL template for product pages
        
    Returns:
        Product ID or None if not found
    """
    # Normalize URLs and remove query parameters
    url = url.split('?')[0].rstrip('/')
    base_url = base_url.rstrip('/')
    
    # Extract the path part of the URL
    parsed_url = urlparse(url)
    path = parsed_url.path
    
    # For relative URLs, add the base URL
    if not url.startswith(('http://', 'https://')):
        url = urljoin(base_url, url)
        parsed_url = urlparse(url)
        path = parsed_url.path
    
    # Find the marker in the product URL template
    template_path = urlparse(product_url_template).path
    marker_match = re.search(r'\{product_id\}', template_path)
    
    if marker_match:
        # Get the pattern before the {product_id} marker
        marker_index = template_path.index('{product_id}')
        pattern_before = template_path[:marker_index]
        
        # Find where this pattern occurs in the URL path
        if pattern_before in path:
            product_id_start = path.index(pattern_before) + len(pattern_before)
            product_id = path[product_id_start:]
            
            # Remove trailing slash if present
            product_id = product_id.rstrip('/')
            
            if product_id:
                logger.debug(f"Extracted product ID '{product_id}' from {url}")
                return product_id
    
    # Fallback to the old method if the above approach doesn't work
    # Split the path into components
    path_parts = path.strip('/').split('/')
    
    # Look for the product ID in different URL patterns
    markers = ['products', 'bikes', 'p']
    for marker in markers:
        if marker in path_parts:
            marker_index = path_parts.index(marker)
            if marker_index < len(path_parts) - 1:
                # Everything after the marker is the product ID
                product_id = '/'.join(path_parts[marker_index + 1:])
                logger.debug(f"Extracted product ID '{product_id}' from {url} using fallback method")
                return product_id
    
    logger.warning(f"Could not extract product ID from {url}")
    return None

def discover_product_ids(website_config: Dict[str, Any]) -> List[str]:
    """
    Discover product IDs by crawling product listing pages.
    
    Args:
        website_config: Configuration dictionary for the website
        
    Returns:
        List of discovered product IDs
    """
    product_ids = set()
    discovery_config = website_config.get("discovery", {})
    
    if not discovery_config:
        logger.warning(f"No discovery configuration found for {website_config['name']}")
        return []
    
    # Get the initial discovery URL
    discovery_url = discovery_config.get("url")
    if not discovery_url:
        logger.warning(f"No discovery URL found for {website_config['name']}")
        return []
    
    # Get the product link selector
    product_link_selector = discovery_config.get("product_link_selector")
    if not product_link_selector:
        logger.warning(f"No product link selector found for {website_config['name']}")
        return []
    
    logger.debug(f"Starting discovery for {website_config['name']} with URL: {discovery_url} and selector: {product_link_selector}")
    
    # Get the pagination selector (if any)
    pagination_selector = discovery_config.get("pagination_selector")
    
    # Set maximum pages to crawl to avoid infinite loops
    max_pages = 10
    pages_crawled = 0
    current_url = discovery_url
    
    base_url = website_config["base_url"]
    product_url_template = website_config["product_url_template"]
    
    logger.info(f"Starting product discovery for {website_config['name']} at {discovery_url}")
    
    while current_url and pages_crawled < max_pages:
        logger.debug(f"Crawling product listing page: {current_url}")
        
        # Fetch and parse the page
        soup = get_soup(current_url)
        if not soup:
            logger.error(f"Failed to get soup for {current_url}")
            break
        
        # Extract product links
        product_links = soup.select(product_link_selector)
        logger.debug(f"Found {len(product_links)} product links on page {current_url}")
        logger.debug(f"Links found: {[link.get('href') for link in product_links]}")
        
        # Extract product IDs from links
        for link in product_links:
            href = link.get("href")
            if not href:
                logger.warning(f"Found link without href in {current_url}")
                continue
            
            # Convert relative URL to absolute
            if not href.startswith(("http://", "https://")):
                href = urljoin(base_url, href)
            
            # Extract product ID from URL
            product_id = extract_product_id_from_url(href, base_url, product_url_template)
            if product_id:
                logger.debug(f"Extracted product ID {product_id} from {href}")
                product_ids.add(product_id)
            else:
                logger.warning(f"Could not extract product ID from {href}")
        
        # Find the next page link, if available
        next_page = None
        if pagination_selector:
            next_page_link = soup.select_one(pagination_selector)
            if next_page_link and next_page_link.get("href"):
                next_page = next_page_link["href"]
                if not next_page.startswith(("http://", "https://")):
                    next_page = urljoin(base_url, next_page)
                logger.debug(f"Found next page link: {next_page}")
            else:
                logger.debug("No next page link found")
        
        # Update loop variables
        current_url = next_page
        pages_crawled += 1
        
        # Be nice to the server
        time.sleep(2)
    
    logger.info(f"Discovered {len(product_ids)} product IDs for {website_config['name']}: {list(product_ids)}")
    return list(product_ids)

def get_image_filename(url: str, product_id: str) -> str:
    """
    Generate a unique filename for an image URL.
    
    Args:
        url: Image URL
        product_id: Product ID
        
    Returns:
        Filename for the image
    """
    # Get file extension from URL
    parsed_url = urlparse(url)
    path = parsed_url.path
    ext = os.path.splitext(path)[1].lower()
    if not ext or ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        ext = '.jpg'  # Default to jpg
    
    # Replace slashes with hyphens in the product_id for filesystem safety
    safe_product_id = product_id.replace('/', '-')
    
    # Create a unique filename using product_id and URL hash
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    return f"{safe_product_id}_{url_hash}{ext}"

def download_image(url: str, product_id: str) -> Optional[str]:
    """
    Download an image from URL and save it locally.
    
    Args:
        url: Image URL
        product_id: Product ID
        
    Returns:
        Local path to the image relative to static directory, or None if failed
    """
    try:
        # Clean up the URL
        url = url.replace('{width}x', '800x').replace('_{width}x.', '_800x.')
        
        # Generate filename
        filename = get_image_filename(url, product_id)
        filepath = IMAGES_DIR / filename
        
        # Download the image
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        # Save the image
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.debug(f"Downloaded image {url} to {filepath}")
        return f"images/bikes/{filename}"
    
    except Exception as e:
        logger.warning(f"Failed to download image {url}: {e}")
        return None

def cleanup_unused_images(current_image_paths: List[str]):
    """
    Move unused images to archive.
    
    Args:
        current_image_paths: List of image paths that are currently in use
    """
    # Skip this function if no images are provided (safety check)
    if not current_image_paths:
        logger.warning("No current image paths provided, skipping cleanup to prevent data loss")
        return
        
    current_filenames = {os.path.basename(path) for path in current_image_paths if path}
    logger.info(f"Cleanup: Current image count: {len(current_filenames)}")
    
    # Extract product IDs from the current filenames (before the underscore)
    # Note: Product IDs with slashes are stored with hyphens in filenames
    current_product_ids = set()
    for filename in current_filenames:
        if '_' in filename:
            product_id = filename.split('_')[0]
            current_product_ids.add(product_id)
            # Also add variants with hyphens replaced by slashes for matching
            if '-' in product_id:
                current_product_ids.add(product_id.replace('-', '/'))
    
    logger.info(f"Cleanup: Current product IDs: {current_product_ids}")
    
    # Check all files in the images directory, but only move those that match our current product IDs
    moved_count = 0
    for file in IMAGES_DIR.glob('*'):
        # Get the product ID from the filename
        file_product_id = file.name.split('_')[0] if '_' in file.name else ''
        
        # Also check variants with slashes replaced by hyphens
        match_found = (file_product_id in current_product_ids)
        
        # If the product ID matches but the full filename doesn't exist in current_filenames
        if match_found and file.name not in current_filenames:
            # Move to archive
            archive_path = IMAGES_ARCHIVE_DIR / f"{datetime.datetime.now().strftime('%Y%m%d')}_{file.name}"
            shutil.move(str(file), str(archive_path))
            logger.info(f"Moved unused image {file.name} to archive")
            moved_count += 1
    
    logger.info(f"Cleanup complete: {moved_count} images moved to archive")

def parse_product_page(soup: BeautifulSoup, selectors: Dict[str, str], product_id: str) -> Dict[str, Any]:
    """
    Parse a product page using the provided selectors.
    
    Args:
        soup: BeautifulSoup object of the product page
        selectors: Dictionary of CSS selectors for each attribute
        product_id: Product ID for image handling
        
    Returns:
        Dictionary of extracted product data
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
    
    # Extract and download images
    if "images" in selectors:
        images = []
        
        # Extract image URLs
        for img in soup.select(selectors["images"]):
            # Get src attribute
            src = img.get('src', '')
            if src and src not in images:
                if src.startswith('//'):
                    src = 'https:' + src
                images.append(src)
            
            # Get data-src attribute (for lazy-loaded images)
            data_src = img.get('data-src', '')
            if data_src and data_src not in images:
                if data_src.startswith('//'):
                    data_src = 'https:' + data_src
                images.append(data_src)
        
        # Store original image URLs directly without downloading
        if images:
            product_data["images"] = images
            product_data["original_images"] = images  # Keep original URLs for reference
    
    return product_data

def crawl_website(website_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Crawl a website for product data based on its configuration.
    
    Args:
        website_config: Configuration dictionary for the website
        
    Returns:
        List of product data dictionaries
    """
    products = []
    website_name = website_config["name"]
    logger.info(f"Starting crawl for {website_name}")
    
    # Discover product IDs
    product_ids = discover_product_ids(website_config)
    
    if not product_ids:
        logger.warning(f"No product IDs discovered for {website_name}")
        return []
    
    for product_id in product_ids:
        for lang in website_config["languages"]:
            # Format the product URL
            # Handle product IDs with slashes correctly
            product_url = website_config["product_url_template"].format(product_id=product_id)
            
            # Add language parameter if needed
            if lang != website_config["languages"][0]:  # Skip for default language
                if "?" in product_url:
                    product_url += f"&lang={lang}"
                else:
                    product_url += f"?lang={lang}"
            
            logger.info(f"Crawling {product_url}")
            
            # Fetch and parse the product page
            soup = get_soup(product_url)
            if not soup:
                continue
            
            # Extract product data
            product_data = parse_product_page(soup, website_config["selectors"], product_id)
            
            # Add metadata
            product_data["website"] = website_name
            product_data["product_id"] = product_id
            product_data["language"] = lang
            product_data["url"] = product_url
            product_data["crawl_date"] = datetime.datetime.now().isoformat()
            
            products.append(product_data)
            
            # Be nice to the server
            time.sleep(1)
    
    logger.info(f"Completed crawl for {website_name}, found {len(products)} products")
    return products

def save_to_csv(products: List[Dict[str, Any]], website_key: str):
    """
    Save product data to CSV.
    
    Args:
        products: List of product data dictionaries
        website_key: Website identifier
    """
    if not products:
        logger.warning(f"No products to save for {website_key}")
        return
    
    # Get current date for filename
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"{website_key}_{date_str}.csv"
    filepath = CURRENT_DATA_DIR / filename
    
    # Archive existing file if it exists
    if filepath.exists():
        archive_path = ARCHIVE_DATA_DIR / filename
        shutil.move(str(filepath), str(archive_path))
        logger.info(f"Archived existing file to {archive_path}")
    
    # Save new data
    df = pd.DataFrame(products)
    df.to_csv(filepath, index=False)
    logger.info(f"Saved {len(products)} products to {filepath}")

def run_crawler():
    """Main function to run the crawler for all configured websites."""
    logger.info("Starting crawler run")
    
    # Ensure data directories exist
    os.makedirs(CURRENT_DATA_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DATA_DIR, exist_ok=True)
    
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