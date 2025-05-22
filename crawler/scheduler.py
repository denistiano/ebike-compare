"""
Scheduler to run the ebike crawler at regular intervals.
"""

import time
import logging
import datetime
import schedule
from crawler import run_crawler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ebike_scheduler")

def job():
    """Scheduled job to run the crawler."""
    logger.info("Starting scheduled crawler job")
    try:
        run_crawler()
        logger.info("Scheduled crawler job completed successfully")
    except Exception as e:
        logger.error(f"Scheduled crawler job failed: {e}", exc_info=True)

def main():
    """Main function to setup and run the scheduler."""
    logger.info("Starting scheduler")
    
    # Run immediately on startup
    job()
    
    # Schedule to run daily at midnight
    schedule.every().day.at("00:00").do(job)
    
    logger.info("Scheduler running, press Ctrl+C to exit")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")

if __name__ == "__main__":
    main() 