from scraper.flipkart import FlipkartScraper
from scraper.utils import parse_review_date
import pandas as pd
from datetime import datetime
import os

import csv

def append_to_csv(reviews, filename):
    """
    Appends a list of reviews to a CSV file.
    Creates the file with header if it doesn't exist.
    """
    if not reviews:
        return

    # Define columns
    fieldnames = ['platform', 'reviewer_name', 'rating', 'review', 'review_date', 'relative_date']
    
    file_exists = os.path.isfile(filename)
    
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
                
            # Filter and write rows
            for r in reviews:
                # Ensure only valid keys are written
                row_to_write = {k: r.get(k, None) for k in fieldnames}
                writer.writerow(row_to_write)
                
        # print(f"   [CSV] Appended {len(reviews)} rows.")
            
    except Exception as e:
        print(f"   [CSV Error] {e}")

def convert_csv_to_excel(csv_filename, excel_filename):
    """
    Converts the final CSV to Excel.
    """
    try:
        print("   Converting CSV to Excel...")
        df = pd.read_csv(csv_filename)
        df.to_excel(excel_filename, index=False)
        print(f"   Success! Excel saved: {excel_filename}")
    except Exception as e:
        print(f"   [Excel Conversion Error] {e}")

def main():
    print("=== Flipkart Review Scraper ===")
    
    # 1. User Inputs
    product_url = input("Enter Flipkart Product URL: ").strip()
    
    print("\n--- Date Filter (YYYY-MM-DD) ---")
    from_date_str = input("From Date (e.g., 2023-01-01): ").strip()
    to_date_str = input("To Date (e.g., 2024-12-31): ").strip()
    
    try:
        from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    MAX_PAGES = 50000 # 50k support
    print(f"\nSettings: Max {MAX_PAGES} pages, Filter {from_date.date()} to {to_date.date()}")
    
    # Setup output
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"{output_dir}/reviews_{timestamp}.csv"
    excel_filename = f"{output_dir}/reviews_{timestamp}.xlsx"

    # 2. Init Scraper
    scraper = FlipkartScraper()
    # Note: We NO LONGER store all_reviews in memory. We just count total.
    total_reviews_collected = 0
    
    try:
        # 3. Navigation
        scraper.open_product_page(product_url)
        scraper.go_to_all_reviews()
        
        # 4. Scraping Loop
        page_count = 0
        while page_count < MAX_PAGES:
            page_count += 1
            print(f"\n--- Scraping Page {page_count} ---")
            
            # Extract data
            raw_reviews = scraper.extract_page_data()
            
            # Process & Filter immediately (Streaming Mode)
            processed_reviews = []
            for r in raw_reviews:
                raw_date_str = r['review_date']
                r['relative_date'] = raw_date_str 
                r_date = parse_review_date(raw_date_str)
                
                if r_date:
                    r_date = r_date.replace(hour=0, minute=0, second=0, microsecond=0)
                    if from_date <= r_date <= to_date:
                        r['review_date'] = r_date.strftime("%Y-%m-%d")
                        processed_reviews.append(r)
            
            # Write batch to CSV immediately
            if processed_reviews:
                append_to_csv(processed_reviews, csv_filename)
                total_reviews_collected += len(processed_reviews)
                print(f"   Saved {len(processed_reviews)} reviews to CSV (Total: {total_reviews_collected})")
            else:
                print("   No valid reviews on this page (filtered out or empty).")
                
            # No huge list in memory
            
            # Pagination
            if page_count < MAX_PAGES:
                if not scraper.next_page():
                    break
            else:
                print("Max pages reached.")
                
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        scraper.quit()
        
        # Finally convert to Excel
        if total_reviews_collected > 0:
            convert_csv_to_excel(csv_filename, excel_filename)
        else:
            print("No reviews collected.")

if __name__ == "__main__":
    main()
