import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from .utils import get_driver, random_sleep

class FlipkartScraper:
    def __init__(self):
        self.driver = get_driver()
        self.wait = WebDriverWait(self.driver, 10)  # Standard 10s wait

    def open_product_page(self, url):
        """
        Opens the product page and handles the initial popup.
        """
        print(f"Opening URL: {url}")
        self.driver.get(url)
        random_sleep(2, 4)
        self.close_login_popup()

    def close_login_popup(self):
        """
        Check for the intrusive login popup and close it if it appears.
        Step 4 in instructions.
        """
        try:
            print("Checking for login popup...")
            # Flipkart's popup close button selector (class: _30XB9F is common for the 'X' button)
            # Also checking for older selectors just in case
            close_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='_30XB9F'] | //button[contains(@class, '_2KpZ6l')]"))
            )
            # Click it
            close_btn.click()
            print("Login popup closed.")
            random_sleep(1, 2)
        except TimeoutException:
            print("No login popup appeared (or couldn't find close button).")
        except Exception as e:
            print(f"Error closing popup: {e}")

    def go_to_all_reviews(self):
        """
        Navigates from the main product page to the 'All Reviews' page.
        Skips if already on a reviews page.
        """
        if "/product-reviews/" in self.driver.current_url:
            print("Already on 'All Reviews' page. Skipping navigation.")
            return

        try:
            print("Navigating to 'All Reviews' section...")
            
            # Strategy: Look for multiple potential selectors for the "All Reviews" button
            # 1. New/Common class (often looks like a big block with text)
            # 2. Text-based search (most robust)
            
            potential_xpaths = [
                "//div[@class='_3UAT2v _16PBlm']",  # Standard specific class
                "//span[contains(text(), 'All') and contains(text(), 'reviews')]/parent::div", # Text based parent
                "//div[contains(text(), 'All') and contains(text(), 'reviews')]", # Direct text div
                "//a[contains(@href, '/product-reviews/')]" # Link to reviews
            ]
            
            all_reviews_btn = None
            for xpath in potential_xpaths:
                try:
                    # Short wait for each strategy
                    wait_short = WebDriverWait(self.driver, 3)
                    all_reviews_btn = wait_short.until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    print(f"   Found 'All Reviews' button with XPath: {xpath}")
                    break
                except TimeoutException:
                    continue
            
            if not all_reviews_btn:
                print("Could not find 'All Reviews' button. The product might have very few reviews or the layout is different.")
                return

            # Scroll to it
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", all_reviews_btn)
            random_sleep(1, 2)
            
            try:
                all_reviews_btn.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", all_reviews_btn)
            
            print("Clicked 'All Reviews' button.")
            random_sleep(3, 5) # wait for the new page to load
            
        except Exception as e:
            print(f"Error navigating to all reviews: {e}")

    def quit(self):
        print("Closing driver...")
        self.driver.quit()

    def extract_page_data(self):
        """
        Extracts all reviews from the current page.
        Returns a list of dictionaries.
        """
        reviews_data = []
        try:
            # 1. Wait for page to be "ready" (evidence of reviews)
            # Standard review rating blocks are very reliable indicators
            print("   Waiting for review elements to appear...")
            try:
                # MKiFS6 is a very common rating class in the 2026 layout
                # _3LWZlK is the classic rating class
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MKiFS6')] | //div[contains(@class, '_3LWZlK')]"))
                )
            except TimeoutException:
                print("   Timeout waiting for review elements. Trying extraction anyway...")

            # 2. Multi-strategy selector for review containers
            strategies = [
                # A. Container that wraps the whole review column
                "//div[contains(@class, 'gMdEY7')]//div[contains(@class, 'col')]",
                # B. Direct content wrapper parent
                "//div[contains(@class, 'x_CUu6')]/parent::div",
                # C. Find ANY div that contains a rating block (Very Robust)
                "//div[(.//div[contains(@class, 'MKiFS6')] or .//div[contains(@class, '_3LWZlK')]) and .//p]",
                # D. Classic layout
                "//div[contains(@class, '_2wzgFH')]",
                # E. Mobile/Responsive layout
                "//div[contains(@class, 'cPHDOP')]"
            ]

            review_blocks = []
            for xpath in strategies:
                blocks = self.driver.find_elements(By.XPATH, xpath)
                # Filter out small blocks (e.g. sidebar info)
                # True review blocks usually have some height/text
                valid_blocks = [b for b in blocks if len(b.text.strip()) > 20]
                if valid_blocks:
                    review_blocks = valid_blocks
                    print(f"   Success with strategy: {xpath} (Found {len(review_blocks)})")
                    break
            
            if not review_blocks:
                print("   Found 0 reviews on this page. Saving debug snapshot...")
                with open("debug_last_failed.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                return []

            for block in review_blocks:
                data = {
                    "platform": "Flipkart",
                    "reviewer_name": None,
                    "rating": None,
                    "review": None,
                    "review_date": None
                }
                
                # 0. Extract Reviewer Name
                try:
                    # New layout: Name usually has class 'ZDi3w2' (often combined with zJ1ZGa)
                    try:
                        name_elem = block.find_element(By.XPATH, ".//p[contains(@class, 'ZDi3w2')]")
                        data["reviewer_name"] = name_elem.text.strip()
                    except:
                        pass
                    
                    # Old layout fallback: _2V5EHH
                    if not data["reviewer_name"]:
                         try:
                            name_elem = block.find_element(By.XPATH, ".//p[contains(@class, '_2V5EHH')]")
                            data["reviewer_name"] = name_elem.text.strip()
                         except:
                            pass
                except:
                    pass
                
                if not data["reviewer_name"]:
                    data["reviewer_name"] = "Anonymous"

                # 1. Extract Rating (New layout uses MKiFS6 or XdJ...]
                try:
                    # Try new selector first
                    rating_elem = block.find_element(By.XPATH, ".//div[contains(@class, 'MKiFS6')]")
                    data["rating"] = int(rating_elem.text.strip())
                except:
                    # Fallback old selector
                    try:
                        rating_elem = block.find_element(By.XPATH, ".//div[contains(@class, '_3LWZlK')]")
                        data["rating"] = int(rating_elem.text.strip())
                    except:
                        data["rating"] = 0
                
                # 2. Extract Review Text & Title
                try:
                    full_text_parts = []
                    # Title (New: qW2QI1, Old: _2-N8zT)
                    try:
                        title_elem = block.find_element(By.XPATH, ".//p[contains(@class, 'qW2QI1')] | .//p[contains(@class, '_2-N8zT')]")
                        full_text_parts.append(title_elem.text.strip())
                    except:
                        pass
                    
                    # Body (New: G4PxIA, Old: t-ZTKy)
                    try:
                        text_elem = block.find_element(By.XPATH, ".//div[contains(@class, 'G4PxIA')]//div[1] | .//div[contains(@class, 't-ZTKy')]")
                        body = text_elem.text.replace("READ MORE", "").strip()
                        full_text_parts.append(body)
                    except:
                        pass
                        
                    data["review"] = self._clean_text(" - ".join(full_text_parts))
                except:
                    data["review"] = ""

                # 3. Extract Date
                try:
                    # New layout: Date is often a simple <p class="zJ1ZGa">10 months ago</p>
                    # But author name also uses zJ1ZGa or similar? 
                    # In sample: Name is <p class="zJ1ZGa ZDi3w2">Name</p>
                    # Date is <p class="zJ1ZGa">10 months ago</p> (Second occurrence in footer or distinct class)
                    
                    # Strategy: Get all 'zJ1ZGa' or '_2sc7ZR'
                    date_candidates = block.find_elements(By.XPATH, ".//p[contains(@class, 'zJ1ZGa')] | .//p[contains(@class, '_2sc7ZR')]")
                    
                    # Usually the last one or the one with 'ago' or year is the date
                    valid_date_found = False
                    for dc in date_candidates:
                        txt = dc.text.strip()
                        # Simple heuristic: if it contains "ago" or "202" (year)
                        if "ago" in txt or "202" in txt or "201" in txt:
                             data["review_date"] = txt
                             valid_date_found = True
                             break
                    
                    if not valid_date_found and date_candidates:
                         # Fallback: take the last one
                         data["review_date"] = date_candidates[-1].text.strip()
                         
                except:
                    data["review_date"] = None
                
                if data["rating"] or data["review"]:
                    reviews_data.append(data)
                
        except Exception as e:
            print(f"Error extracting data from page: {e}")
            
        return reviews_data

    def _clean_text(self, text):
        """Helper to remove newlines and extra spaces."""
        if not text:
            return ""
        return " ".join(text.split())

    def has_next_button(self):
        """
        Checks if a 'Next' pagination button exists.
        Returns True if pagination is available, False otherwise.
        """
        try:
            next_btns = self.driver.find_elements(By.XPATH, 
                "//a[span[contains(text(), 'Next')]] | //a[contains(text(), 'Next')] | //nav//a[contains(@class, '_1LKTO3')]"
            )
            return len(next_btns) > 0
        except:
            return False
    
    def click_next_button(self):
        """
        Clicks the 'Next' button for pagination.
        Returns True if successful, False otherwise.
        """
        try:
            print("   Found pagination - clicking 'Next' button...")
            next_btn = self.driver.find_elements(By.XPATH, 
                "//a[span[contains(text(), 'Next')]] | //a[contains(text(), 'Next')]"
            )
            
            if next_btn:
                btn = next_btn[0]
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                random_sleep(1, 2)
                
                try:
                    btn.click()
                except:
                    self.driver.execute_script("arguments[0].click();", btn)
                
                print("   ✓ Navigated to next page")
                random_sleep(3, 5)
                return True
            return False
        except Exception as e:
            print(f"   Error clicking Next button: {e}")
            return False
    
    def scroll_to_load_more(self):
        """
        Scrolls down to trigger infinite scroll and load more reviews.
        Returns True if new content loaded, False if reached the end.
        """
        try:
            print("   Using infinite scroll - scrolling down...")
            
            # Get current number of review elements before scrolling
            before_count = len(self.driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'MKiFS6')] | //div[contains(@class, '_3LWZlK')]"
            ))
            
            # Get current scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            random_sleep(3, 5)
            
            # Get new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Get new count of review elements
            after_count = len(self.driver.find_elements(By.XPATH, 
                "//div[contains(@class, 'MKiFS6')] | //div[contains(@class, '_3LWZlK')]"
            ))
            
            # Check if new content loaded
            if new_height > last_height or after_count > before_count:
                print(f"   ✓ Loaded more reviews ({before_count} → {after_count})")
                return True
            else:
                print("   ✗ No new content (reached end)")
                return False
                
        except Exception as e:
            print(f"   Error during scroll: {e}")
            return False
    
    def next_page(self):
        """
        Smart hybrid method that auto-detects pagination type.
        Tries pagination button first, falls back to infinite scroll.
        Returns True if more content available, False if reached the end.
        """
        try:
            # Strategy 1: Check for pagination button
            if self.has_next_button():
                return self.click_next_button()
            
            # Strategy 2: Use infinite scroll
            else:
                return self.scroll_to_load_more()
                
        except Exception as e:
            print(f"Error in next_page: {e}")
            return False

