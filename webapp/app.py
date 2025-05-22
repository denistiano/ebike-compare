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
IMAGES_DIR = BASE_DIR / "webapp" / "static" / "images" / "bikes"

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

def find_images_for_product(product_id):
    """
    Find all images in the static/images/bikes directory that match the product ID pattern.
    
    Args:
        product_id: Product ID to match
        
    Returns:
        List of image paths relative to the static directory
    """
    image_paths = []
    
    # Check if the images directory exists
    if not IMAGES_DIR.exists():
        logger.warning(f"Images directory {IMAGES_DIR} does not exist")
        return image_paths
    
    # Get all files in the images directory
    files = os.listdir(IMAGES_DIR)
    
    # Filter files by the product ID pattern
    pattern = re.compile(f"^{re.escape(product_id)}_[a-zA-Z0-9]+\\.(jpg|jpeg|png|webp)$", re.IGNORECASE)
    matching_files = [f for f in files if pattern.match(f)]
    
    # Convert to relative paths for the static directory
    for file in matching_files:
        image_paths.append(f"images/bikes/{file}")
    
    logger.debug(f"Found {len(image_paths)} images for product ID {product_id}: {image_paths}")
    return image_paths

def get_all_bikes():
    """
    Get a list of all available bikes with complete details.
    
    Returns:
        List of dictionaries with bike information
    """
    bikes = []
    data = get_latest_data()
    
    # Get all product images from the static directory
    logger.info(f"Scanning {IMAGES_DIR} for product images")
    
    for website_key, df in data.items():
        for _, row in df.iterrows():
            # Create a unique bike ID that includes the website_key to avoid collisions
            unique_id = f"{website_key}_{row['product_id']}_{row['language']}"
            
            # Convert the row to a dictionary for the bike data
            bike_data = row.to_dict()
            
            # Add additional fields for consistency
            bike_data["id"] = unique_id
            bike_data["website_key"] = website_key
            
            # Find images for this product ID
            product_id = bike_data["product_id"]
            images = find_images_for_product(product_id)
            bike_data["images"] = images
            
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