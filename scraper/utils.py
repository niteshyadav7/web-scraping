import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    """
    Initializes and returns a Selenium Chrome driver with anti-detection options.
    We do NOT use headless mode to mimic a real user.
    """
    options = Options()
    
    # 1. Disable the "AutomationControlled" flag to hide Selenium from basic detection
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # 2. Maximize window to ensure all elements are visible
    options.add_argument("--start-maximized")
    
    # 3. Standard 'user-agent' just in case (optional but good practice)
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the driver using WebDriverManager
    # This automatically downloads the correct driver for your Chrome version
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
