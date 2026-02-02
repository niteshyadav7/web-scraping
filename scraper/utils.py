import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    """
    Initializes and returns a Selenium Chrome driver.
    Detects if running on Render and configures headless mode accordingly.
    """
    options = Options()
    
    # Anti-detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Check if running on Render
    is_render = os.environ.get('RENDER', False)
    
    if is_render:
        print("🌍 Running on Render - Configuring Headless Chrome")
        options.add_argument("--headless=new")  # New headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.binary_location = "/usr/bin/google-chrome"
    else:
        print("💻 Running Locally - Chrome UI Visible")

    # Initialize the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

def random_sleep(min_seconds=2, max_seconds=5):
    """
    Sleeps for a random amount of time between min_seconds and max_seconds.
    This mimics human behavior (we don't click instantly).
    """
    sleep_time = random.uniform(min_seconds, max_seconds)
    print(f"   [Sleeping for {sleep_time:.2f} seconds...]")
    time.sleep(sleep_time)

from datetime import datetime, timedelta
import re

def parse_review_date(date_str):
    """
    Parses Flipkart review dates like:
    - "5 days ago"
    - "1 month ago"
    - "Oct, 2023"
    - "Today"
    - "20 Jan 2024" (Standard format)
    
    Returns a datetime object or None.
    """
    if not date_str:
        return None
        
    date_str = date_str.strip()
    today = datetime.now()
    
    try:
        # Relative dates
        if 'today' in date_str.lower():
            return today
        if 'days ago' in date_str.lower():
            days = int(re.search(r'(\d+)', date_str).group(1))
            return today - timedelta(days=days)
        if 'month ago' in date_str.lower() or 'months ago' in date_str.lower():
            months = int(re.search(r'(\d+)', date_str).group(1))
            return today - timedelta(days=months*30) # Approx
            
        # Absolute dates "Oct, 2023"
        if ',' in date_str:
            # Example: Oct, 2023
            try:
                return datetime.strptime(date_str, "%b, %Y")
            except:
                pass
                
        # Absolute dates "20 Jan 2024"
        try:
            return datetime.strptime(date_str, "%d %b %Y")
        except:
            pass

        return None
    except Exception as e:
        print(f"Date parse error for '{date_str}': {e}")
        return None
