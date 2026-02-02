# Multi-Product Scraping Feature

## Overview

The Flipkart Review Scraper now supports **scraping multiple products in a single session**! All reviews from all products are combined into one Excel file for easy analysis.

## How to Use

### 1. **Enter Multiple URLs**

In the "Product URLs" textarea, enter one URL per line:

```
https://www.flipkart.com/product1/...
https://www.flipkart.com/product2/...
https://www.flipkart.com/product3/...
```

### 2. **URL Counter**

The form automatically counts and displays how many products you've added:
- Shows `(1 product)` for single URL
- Shows `(3 products)` for multiple URLs
- Shows `(one URL per line)` when empty

### 3. **Start Scraping**

Click "Start Scraping" - the system will:
1. Process each product sequentially
2. Show progress for each product
3. Combine all reviews into one file
4. Track which product each review came from

## Features

### ✅ **Sequential Processing**
- Products are scraped one at a time
- Each product gets its own browser session
- Prevents rate limiting and detection

### ✅ **Progress Tracking**
Console output shows:
```
============================================================
📦 PRODUCT 1/3
🔗 URL: https://www.flipkart.com/product1/...
============================================================

🔍 Detected mode: PAGINATION

   ✓ Saved 10 reviews | Product Total: 10 | Overall Total: 10

✓ Product 1 complete - reached end of content
   📊 Collected 10 reviews from this product
```

### ✅ **Combined Output**
All reviews are saved to a **single Excel file** with columns:
- `platform` - Always "Flipkart"
- `reviewer_name` - Name of the reviewer
- `rating` - Star rating (1-5)
- `review` - Review text
- `review_date` - Formatted date (YYYY-MM-DD)
- `relative_date` - Original date string
- **`product_url`** - ⭐ NEW! Tracks which product the review came from

### ✅ **Error Handling**
- If one product fails, others continue
- Error messages show which product had issues
- Partial results are still saved

## Example Use Cases

### **1. Compare Competing Products**
```
https://www.flipkart.com/iphone-15/...
https://www.flipkart.com/samsung-s24/...
https://www.flipkart.com/pixel-8/...
```
→ Get all reviews in one file, filter by `product_url` in Excel

### **2. Analyze Product Variants**
```
https://www.flipkart.com/shirt-blue/...
https://www.flipkart.com/shirt-red/...
https://www.flipkart.com/shirt-green/...
```
→ Compare reviews across color variants

### **3. Bulk Data Collection**
```
https://www.flipkart.com/product-1/...
https://www.flipkart.com/product-2/...
... (up to 50+ products)
```
→ Collect reviews from entire product catalog

## Technical Details

### **Backend Changes**

**`api.py`:**
- `scrape_task()` now accepts a **list** of URLs
- Loops through each URL sequentially
- Adds `product_url` field to each review
- Shows per-product and overall totals

**CSV Structure:**
```python
fieldnames = [
    'platform', 
    'reviewer_name', 
    'rating', 
    'review', 
    'review_date', 
    'relative_date', 
    'product_url'  # NEW!
]
```

### **Frontend Changes**

**`ScraperForm.jsx`:**
- Changed `<input>` to `<textarea>` for multi-line input
- Added URL counter in label
- Validates and counts URLs dynamically

**`ScraperForm.css`:**
- Added textarea styling
- Added `.label-hint` for URL counter
- Maintains consistent design

### **API Response**

```json
{
  "message": "Scraping started for 3 product(s)",
  "status": "running",
  "product_count": 3
}
```

## Performance Notes

### **Timing**
- Each product takes ~2-5 minutes (depending on review count)
- 3 products ≈ 6-15 minutes total
- 10 products ≈ 20-50 minutes total

### **Recommendations**
- **Small batches**: 3-5 products at a time
- **Large batches**: Use higher `max_pages` value
- **Monitor**: Check console output for progress

### **Browser Resources**
- One browser instance per product
- Properly closed after each product
- No memory leaks

## Limitations

1. **Sequential Only**: Products are processed one at a time (prevents detection)
2. **Same Date Range**: All products use the same date filter
3. **Same Max Pages**: All products use the same scroll/page limit
4. **Single Output**: All reviews go to one file (use `product_url` to filter)

## Tips & Tricks

### **Excel Filtering**
After downloading, use Excel's filter feature:
1. Open the `.xlsx` file
2. Select the `product_url` column
3. Use "Filter" to show reviews from specific products

### **URL Organization**
Keep a text file with your URLs:
```
# Smartphones
https://www.flipkart.com/iphone-15/...
https://www.flipkart.com/samsung-s24/...

# Laptops
https://www.flipkart.com/macbook-pro/...
https://www.flipkart.com/dell-xps/...
```
Copy-paste into the scraper as needed!

### **Error Recovery**
If scraping fails mid-way:
- Check the console output to see which product failed
- Remove failed products from the list
- Re-run with remaining products
- Manually merge Excel files if needed

## Future Enhancements

Potential features for future versions:
- [ ] Parallel scraping (with rate limiting)
- [ ] Per-product date ranges
- [ ] Per-product max pages
- [ ] Separate output files option
- [ ] Resume from failed product
- [ ] Product name extraction
- [ ] Progress bar for multi-product

---

**Happy Scraping! 🚀**
