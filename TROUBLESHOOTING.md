# Troubleshooting Guide - No Data Generated

## Common Issues & Solutions

### 🔍 **Issue 1: Product Has No Reviews**

**Symptom**: Scraper completes but collects 0 reviews

**Cause**: The product genuinely has no reviews on Flipkart

**Solution**:
1. Open the product URL in your browser
2. Check if there are any reviews visible
3. Try a different product with known reviews

**Test URL** (known to have reviews):
```
https://www.flipkart.com/apple-iphone-15-black-128-gb/product-reviews/itm6ac6485c40c76
```

---

### 🔍 **Issue 2: Wrong URL Format**

**Symptom**: Scraper can't navigate to reviews page

**Cause**: URL is not a Flipkart product page

**Correct URL formats**:
✅ `https://www.flipkart.com/product-name/p/itm...`
✅ `https://www.flipkart.com/product-name/product-reviews/itm...`

**Incorrect formats**:
❌ `https://www.flipkart.com/search?q=...` (search page)
❌ `https://www.flipkart.com/category/...` (category page)
❌ Short URLs or redirects

---

### 🔍 **Issue 3: Date Range Too Narrow**

**Symptom**: Scraper finds reviews but saves 0

**Cause**: No reviews exist within your date range

**Solution**:
1. Widen the date range
2. Use `From Date: 2020-01-01` to `To Date: Today`
3. Check console output for "filtered by date" messages

**Example**:
```
From: 2024-01-01
To:   2024-01-31
Result: 0 reviews (all reviews are from 2023)
```

---

### 🔍 **Issue 4: Flipkart Changed Page Structure**

**Symptom**: "Timeout waiting for review elements"

**Cause**: Flipkart updated their HTML/CSS classes

**Solution**:
1. Check `debug_last_failed.html` file
2. Look for review elements in the HTML
3. Update XPath selectors in `scraper/flipkart.py`

**How to check**:
```powershell
# Open debug file in browser
start debug_last_failed.html

# Look for review text and inspect the HTML structure
```

---

### 🔍 **Issue 5: Bot Detection / Captcha**

**Symptom**: Page loads but no content appears

**Cause**: Flipkart detected automated browsing

**Solution**:
1. Wait a few minutes before retrying
2. Use a different product URL
3. Check if browser window shows captcha
4. Clear browser cache/cookies

**Prevention**:
- Don't scrape too many products rapidly
- Use reasonable delays (already built-in)
- Avoid scraping the same product repeatedly

---

### 🔍 **Issue 6: Network/Connection Issues**

**Symptom**: Scraper hangs or times out

**Cause**: Slow internet or Flipkart is down

**Solution**:
1. Check your internet connection
2. Try opening Flipkart in a regular browser
3. Wait and retry later
4. Increase timeout in code (if needed)

---

## Diagnostic Steps

### **Step 1: Check Console Output**

Look for these messages:

```
✅ Good signs:
   "Found 10 reviews on this page"
   "✓ Saved 10 reviews"
   "Success with strategy: ..."

❌ Bad signs:
   "Found 0 reviews on this page"
   "Timeout waiting for review elements"
   "⚠ No new reviews found"
```

### **Step 2: Check Debug File**

```powershell
# Open debug HTML in browser
start debug_last_failed.html

# Look for:
- Are there reviews visible?
- Is it the correct page?
- Is there a captcha?
- Is there an error message?
```

### **Step 3: Test with Known URL**

Try this URL (known to work):
```
https://www.flipkart.com/apple-iphone-15-black-128-gb/product-reviews/itm6ac6485c40c76
```

Settings:
- From Date: 2020-01-01
- To Date: Today
- Max Pages: 10

Expected: Should collect 100+ reviews

### **Step 4: Check Output Files**

```powershell
# List output files
ls output/

# Check latest CSV
Get-Content output/reviews_*.csv -Head 5
```

If previous scrapes worked, the issue is likely with the current URL.

---

## Quick Fixes

### **Fix 1: Use Product Review URL**

Instead of product page, use direct review page:

**Product page**:
```
https://www.flipkart.com/product-name/p/itm123
```

**Review page** (better):
```
https://www.flipkart.com/product-name/product-reviews/itm123
```

### **Fix 2: Widen Date Range**

```
From: 2020-01-01  (or earlier)
To:   2026-12-31  (or today)
```

### **Fix 3: Increase Max Pages**

```
Max Pages: 100 (instead of 10)
```

### **Fix 4: Try Single Product Mode**

If using multiple products, try one at a time to isolate the issue.

---

## Console Output Examples

### **Successful Scrape**:
```
🔍 Detected mode: PAGINATION

   Waiting for review elements to appear...
   Success with strategy: //div[contains(@class, 'col')]
   Found 10 reviews on this page
   ✓ Saved 10 reviews | Total: 10

   Found pagination - clicking 'Next' button...
   ✓ Navigated to next page
   
✓ Scraping complete
📊 Total Reviews Collected: 100
✨ Styled Excel file created: output/reviews_xxx.xlsx
```

### **Failed Scrape** (No Reviews):
```
🔍 Detected mode: INFINITE SCROLL

   Timeout waiting for review elements. Trying extraction anyway...
   Found 0 reviews on this page. Saving debug snapshot...
   ⚠ No new reviews found on this iteration
   
✓ Scraping complete
📊 Total Reviews Collected: 0
```

---

## Getting Help

If none of these solutions work:

1. **Share the URL** you're trying to scrape
2. **Share console output** (copy from terminal)
3. **Check debug_last_failed.html** and describe what you see
4. **Share date range** you're using

---

## Prevention Tips

✅ **Always verify**:
- Product has reviews (check in browser first)
- URL is correct format
- Date range is reasonable
- Internet connection is stable

✅ **Best practices**:
- Start with small max_pages (10-20)
- Use wide date ranges initially
- Test with known working URLs first
- Don't scrape too rapidly

---

**Most common issue**: Product has no reviews or date range is too narrow! 🎯
