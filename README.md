# Flipkart Review Scraper - Web Application

A modern web application to scrape Flipkart product reviews with a beautiful React frontend and Flask API backend.

## 🚀 Features

- **Beautiful UI**: Modern, dark-themed React interface with smooth animations
- **Real-time Progress**: Live updates on scraping status
- **Date Filtering**: Filter reviews by date range
- **High Volume Support**: Stream data to CSV for memory efficiency
- **Download Results**: Get Excel files directly from the browser
- **API-based**: Separate backend and frontend for flexibility

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Chrome browser (for Selenium)

## 🛠️ Installation

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies (if not already done):
```bash
npm install
```

## 🎯 Running the Application

### Step 1: Start the Backend API

Open a terminal and run:
```bash
python api.py
```

The API will start on `http://localhost:5000`

### Step 2: Start the Frontend

Open a **new terminal** and run:
```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

### Step 3: Use the Application

1. Open your browser and go to `http://localhost:5173`
2. Enter the Flipkart product URL
3. Set the date range for filtering reviews
4. Set max pages to scrape (10 reviews per page)
5. Click "Start Scraping"
6. Watch real-time progress
7. Download the Excel file when complete

## 📁 Project Structure

```
flipkart_scraper/
├── api.py                 # Flask API backend
├── main.py               # CLI version (original)
├── scraper/
│   ├── flipkart.py       # Scraper logic
│   └── utils.py          # Helper functions
├── frontend/             # React application
│   ├── src/
│   │   ├── App.jsx       # Main component
│   │   └── App.css       # Styles
│   └── package.json
├── output/               # Scraped data files
└── requirements.txt      # Python dependencies
```

## 🔧 API Endpoints

- `POST /api/scrape` - Start scraping
- `GET /api/status` - Get current status
- `GET /api/download` - Download Excel file
- `POST /api/stop` - Stop scraping (graceful)

## 💡 Tips

- Start with a small number of pages (e.g., 10) to test
- The scraper uses random delays (3-6 seconds) to avoid detection
- Data is saved to CSV in real-time, so you won't lose progress if stopped
- For large scrapes (1000+ pages), let it run overnight

## 🎨 Features

- **Streaming Mode**: Reviews are written to CSV immediately, no memory issues
- **Auto-save**: Data is saved continuously during scraping
- **Date Filtering**: Only saves reviews within your specified date range
- **Excel Export**: Automatic conversion from CSV to Excel at the end

## 🐛 Troubleshooting

**API not connecting?**
- Make sure Flask is running on port 5000
- Check that CORS is enabled in api.py

**Scraper not finding reviews?**
- The website layout may have changed
- Check the console for errors
- Verify the product URL is correct

**Frontend not loading?**
- Make sure you're on `http://localhost:5173`
- Check that npm dev server is running

## 📝 License

MIT License - Feel free to use and modify!
