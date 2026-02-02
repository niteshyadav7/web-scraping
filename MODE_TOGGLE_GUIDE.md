# Mode Toggle Feature - Single vs Multiple Products

## Overview

The scraper now features a **smart mode toggle** that adapts the UI based on whether you want to scrape a single product or multiple products.

## How It Works

### 🔘 **Mode Toggle (Top of Form)**

```
┌─────────────────────────────────────────────┐
│  [📦 Single Product]  [📚 Multiple Products] │
└─────────────────────────────────────────────┘
```

Click to switch between modes:
- **Single Product**: Traditional single URL input
- **Multiple Products**: Multi-line textarea for bulk scraping

## Single Product Mode

### **When to Use:**
- Scraping one product
- Quick analysis
- Testing the scraper
- Small data collection

### **UI Elements:**
```
🔗 Product URL
┌────────────────────────────────────────────┐
│ https://www.flipkart.com/product/...       │
└────────────────────────────────────────────┘

📅 From Date          📅 To Date
┌──────────────┐     ┌──────────────┐
│ 2020-01-01   │     │ 2024-02-03   │
└──────────────┘     └──────────────┘

📄 Max Pages                    (~1000 reviews)
├────────────────────────────────────────┤ 100

┌────────────────────────────────────────────┐
│          🚀 Start Scraping                 │
└────────────────────────────────────────────┘
```

### **Features:**
- ✅ Single URL input field
- ✅ Simple, clean interface
- ✅ Estimated reviews: `~{max_pages * 10} reviews`
- ✅ Button text: "Start Scraping"

## Multiple Products Mode

### **When to Use:**
- Comparing products
- Bulk data collection
- Market research
- Product variant analysis

### **UI Elements:**
```
🔗 Product URLs                    (3 products)
┌────────────────────────────────────────────┐
│ https://www.flipkart.com/product1/...      │
│ https://www.flipkart.com/product2/...      │
│ https://www.flipkart.com/product3/...      │
│                                            │
└────────────────────────────────────────────┘

📅 From Date          📅 To Date
┌──────────────┐     ┌──────────────┐
│ 2020-01-01   │     │ 2024-02-03   │
└──────────────┘     └──────────────┘

📄 Max Pages                  (~3000 reviews total)
├────────────────────────────────────────┤ 100

┌────────────────────────────────────────────┐
│      🚀 Start Scraping 3 Products          │
└────────────────────────────────────────────┘
```

### **Features:**
- ✅ Multi-line textarea (resizable)
- ✅ Live URL counter: `(X products)`
- ✅ Total estimated reviews: `~{max_pages * 10 * product_count} reviews`
- ✅ Dynamic button text: "Start Scraping X Products"

## Smart UI Adaptations

### **1. URL Counter**
- **Single Mode**: No counter shown
- **Multiple Mode**: Shows `(3 products)` or `(one URL per line)` if empty

### **2. Review Estimate**
- **Single Mode**: `(~1000 reviews)`
- **Multiple Mode**: `(~3000 reviews total)` (multiplied by product count)

### **3. Submit Button**
- **Single Mode**: "Start Scraping"
- **Multiple Mode**: "Start Scraping 3 Products"

### **4. Input Field**
- **Single Mode**: `<input type="url">` - validates single URL
- **Multiple Mode**: `<textarea>` - accepts multiple lines

## Mode Switching Behavior

### **Automatic URL Clearing**
When you switch modes, the URL field is automatically cleared to prevent confusion:

```
Single Mode: "https://flipkart.com/product1"
   ↓ (switch to Multiple)
Multiple Mode: "" (cleared)
```

This prevents accidentally submitting a single URL in multiple mode or vice versa.

### **Disabled During Scraping**
Both toggle buttons are disabled while scraping is in progress to prevent mode changes mid-operation.

## Visual Design

### **Toggle Buttons**

**Inactive State:**
- Transparent background
- Dim gray text
- Subtle border

**Active State:**
- Blue-purple gradient background
- White text
- Glowing shadow effect
- Slightly elevated (translateY)

**Hover State:**
- Light background overlay
- Brighter text
- Slight elevation

### **Transitions**
All state changes use smooth CSS transitions:
- Background: 0.3s cubic-bezier
- Transform: 0.3s cubic-bezier
- Color: 0.3s cubic-bezier

## Code Structure

### **State Management**
```jsx
const [mode, setMode] = useState('single')

const handleModeChange = (newMode) => {
  setMode(newMode)
  setFormData({ ...formData, url: '' }) // Clear URL
}
```

### **Conditional Rendering**
```jsx
{mode === 'single' ? (
  <input type="url" ... />
) : (
  <textarea rows="5" ... />
)}
```

### **Dynamic Calculations**
```jsx
const getUrlCount = () => {
  if (!formData.url.trim()) return 0
  return formData.url.trim().split('\n').filter(u => u.trim()).length
}
```

## User Experience Benefits

### ✅ **Clarity**
- Clear distinction between single and multiple modes
- No confusion about input format
- Visual feedback on active mode

### ✅ **Flexibility**
- Easy switching between modes
- Adapts to different use cases
- Maintains consistent UX

### ✅ **Smart Defaults**
- Starts in single mode (most common)
- Clears URL when switching
- Prevents input errors

### ✅ **Visual Feedback**
- Active mode clearly highlighted
- URL count shown in real-time
- Estimated review count updates dynamically

## Keyboard Shortcuts (Future Enhancement)

Potential additions:
- `Ctrl+1`: Switch to Single mode
- `Ctrl+2`: Switch to Multiple mode
- `Tab`: Navigate between toggle buttons

## Accessibility

- Semantic HTML (`<button>` elements)
- Clear labels and icons
- Keyboard navigable
- Disabled state properly indicated
- Focus states visible

---

**Enjoy the new mode toggle! 🎉**
