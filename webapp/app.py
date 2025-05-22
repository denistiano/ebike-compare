"""
Flask web application API for comparing ebikes.
"""

import os
import glob
import json
import pandas as pd
from pathlib import Path
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

def get_all_bikes():
    """
    Get a list of all available bikes.
    
    Returns:
        List of dictionaries with bike information
    """
    bikes = []
    data = get_latest_data()
    
    for website_key, df in data.items():
        for _, row in df.iterrows():
            # Create a unique bike ID that includes the website_key to avoid collisions
            unique_id = f"{website_key}_{row['product_id']}_{row['language']}"
            
            bike_data = {
                "id": unique_id,
                "name": row["name"],
                "website": row["website"],
                "price": row.get("price", "N/A"),
                "product_id": row["product_id"],
                "language": row["language"],
                "website_key": website_key  # Add website_key to differentiate between US/EU
            }
            
            # Handle image data
            if "images" in row:
                try:
                    # If images is a string, try to parse it as JSON
                    if isinstance(row["images"], str):
                        images = json.loads(row["images"])
                        bike_data["images"] = images
                    # If images is already a list, use it
                    elif isinstance(row["images"], list):
                        bike_data["images"] = row["images"]
                    else:
                        bike_data["images"] = None
                except (json.JSONDecodeError, TypeError):
                    bike_data["images"] = None
            
            bikes.append(bike_data)
    
    return bikes

def get_bike_details(bike_ids):
    """
    Get detailed information for the specified bikes.
    
    Args:
        bike_ids: List of bike IDs (website_key_product_id_language)
        
    Returns:
        List of bike data dictionaries
    """
    bikes = []
    data = get_latest_data()
    
    for bike_id in bike_ids:
        parts = bike_id.split("_")
        if len(parts) < 3:
            continue  # Skip invalid IDs
            
        website_key = parts[0]
        product_id = parts[1]
        language = parts[2]
        
        if website_key in data:
            df = data[website_key]
            
            # Filter by product_id
            bike_df = df[df["product_id"] == product_id]
            
            # Filter by language
            bike_df = bike_df[bike_df["language"] == language]
            
            if not bike_df.empty:
                # Convert the first matching row to a dictionary
                bike_data = bike_df.iloc[0].to_dict()
                
                # Add the id field and website_key for consistency
                bike_data["id"] = bike_id
                bike_data["website_key"] = website_key
                
                # Handle image data
                if "images" in bike_data:
                    try:
                        # If images is a string, try to parse it as JSON
                        if isinstance(bike_data["images"], str):
                            images = json.loads(bike_data["images"])
                            bike_data["images"] = images
                        # If images is already a list, use it
                        elif isinstance(bike_data["images"], list):
                            bike_data["images"] = bike_data["images"]
                        else:
                            bike_data["images"] = None
                    except (json.JSONDecodeError, TypeError):
                        bike_data["images"] = None
                
                bikes.append(bike_data)
    
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
    """API endpoint to get all bikes."""
    all_bikes = get_all_bikes()
    
    # Clean up NaN values in the response
    for bike in all_bikes:
        for key, value in bike.items():
            if isinstance(value, float) and pd.isna(value):
                bike[key] = None
    
    return jsonify(all_bikes)

@app.route("/api/compare", methods=["GET"])
def api_compare():
    """API endpoint to get comparison data."""
    bike_ids = request.args.getlist("bike_ids")
    bikes = get_bike_details(bike_ids)
    
    # Clean up NaN values in the response
    for bike in bikes:
        for key, value in bike.items():
            if isinstance(value, float) and pd.isna(value):
                bike[key] = None
    
    return jsonify(bikes)

if __name__ == "__main__":
    app.run(debug=True) 