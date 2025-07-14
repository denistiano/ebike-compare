"""
Flask web application API for comparing ebikes.
"""

import os
import glob
import json
import pandas as pd
from pathlib import Path
import re
from flask import Flask, render_template, request, jsonify, url_for, send_from_directory
import logging
from flask_cors import CORS

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("webapp.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ebike_webapp")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define paths
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CURRENT_DATA_DIR = BASE_DIR / "data" / "current"
ARCHIVE_DATA_DIR = BASE_DIR / "data" / "archive"

def get_latest_data():
    """
    Get the latest data for all websites.
    
    Returns:
        Dictionary mapping website keys to DataFrames
    """
    data = {}
    
    # Get all CSV files in the current directory
    csv_files = glob.glob(str(CURRENT_DATA_DIR / "*.csv"))
    logger.info(f"Found {len(csv_files)} CSV files in {CURRENT_DATA_DIR}")
    
    for csv_file in csv_files:
        # Extract website key from filename (website_YYYYMMDD.csv or website_region_YYYYMMDD.csv)
        filename = os.path.basename(csv_file)
        # Split by underscore and remove the date part (last component)
        parts = filename.split("_")
        if len(parts) > 2:  # For multi-part names like engwe_us_20250522.csv
            website_key = "_".join(parts[:-1])  # Join all parts except the date
        else:
            website_key = parts[0]  # Simple case like fiido_20250522.csv
        
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Add to data dictionary
        data[website_key] = df
        logger.info(f"Loaded data for {website_key} from {filename}: {len(df)} rows")
    
    return data

def get_original_images(product_data):
    """
    Get original image URLs from product data.
    
    Args:
        product_data: Product data dictionary with original_images field
        
    Returns:
        List of image URLs
    """
    image_urls = []
    
    if 'original_images' in product_data and product_data['original_images']:
        # Handle string representation of list
        if isinstance(product_data['original_images'], str):
            try:
                urls = eval(product_data['original_images'])
                if isinstance(urls, list):
                    image_urls = urls
            except (SyntaxError, ValueError):
                logger.warning(f"Could not parse original_images: {product_data['original_images']}")
        # Handle actual list
        elif isinstance(product_data['original_images'], list):
            image_urls = product_data['original_images']
    
    # Clean up URLs
    valid_urls = []
    for url in image_urls:
        if url:
            # Ensure URL has proper scheme
            if url.startswith('//'):
                url = 'https:' + url
            # Replace variable width placeholders with fixed width
            url = re.sub(r'\{width\}x', '1000x', url)
            valid_urls.append(url)
    
    return valid_urls

def get_all_bikes():
    """
    Get a list of all available bikes with complete details.
    
    Returns:
        List of dictionaries with bike information
    """
    bikes = []
    data = get_latest_data()
    
    for website_key, df in data.items():
        for _, row in df.iterrows():
            # Create a unique bike ID that includes the website_key to avoid collisions
            unique_id = f"{website_key}_{row['product_id']}_{row['language']}"
            
            # Convert the row to a dictionary for the bike data
            bike_data = row.to_dict()
            
            # Add additional fields for consistency
            bike_data["id"] = unique_id
            bike_data["website_key"] = website_key
            
            # Get original image URLs instead of local file paths
            image_urls = get_original_images(bike_data)
            bike_data["images"] = image_urls
            
            bikes.append(bike_data)
    
    logger.info(f"Processed {len(bikes)} bikes with images")
    return bikes

@app.route("/")
def index():
    """Serve the index.html page"""
    return send_from_directory('static', 'index.html')

@app.route("/compare")
def compare():
    """Serve the compare.html page"""
    return send_from_directory('static', 'compare.html')

@app.route("/api/bikes")
def api_bikes():
    """API endpoint to get all bikes with complete details."""
    all_bikes = get_all_bikes()
    
    # Clean up NaN values in the response
    for bike in all_bikes:
        for key, value in bike.items():
            if isinstance(value, float) and pd.isna(value):
                bike[key] = None
    
    return jsonify(all_bikes)

if __name__ == "__main__":
    app.run(debug=True) 