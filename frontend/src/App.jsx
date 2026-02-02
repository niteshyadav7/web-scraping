import { useState, useEffect } from 'react'
import ScraperForm from './components/ScraperForm'
import StatusPanel from './components/StatusPanel'
import './App.css'

// Update this URL after deploying backend to Render
// Replace 'your-service-name' with your actual Render service name
const API_URL = import.meta.env.VITE_API_URL || 'https://flipkart-scraper-api.onrender.com/api'


function App() {
  const [status, setStatus] = useState({
    is_running: false,
    current_page: 0,
    total_reviews: 0,
    status: 'idle',
    error: null
  })

  // Poll status when scraping
  useEffect(() => {
    let interval
    if (status.is_running) {
      interval = setInterval(async () => {
        try {
          const response = await fetch(`${API_URL}/status`)
          const data = await response.json()
          setStatus(data)

          if (!data.is_running) {
            clearInterval(interval)
          }
        } catch (error) {
          console.error('Error fetching status:', error)
        }
      }, 1000)
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [status.is_running])

  const handleStartScraping = async (formData) => {
    try {
      const response = await fetch(`${API_URL}/scrape`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      })

      const data = await response.json()

      if (response.ok) {
        setStatus({ ...status, is_running: true, status: 'running' })
      } else {
        alert(data.error || 'Failed to start scraping')
      }
    } catch (error) {
      alert('Error connecting to API: ' + error.message)
    }
  }

  const handleDownload = async () => {
    try {
      const response = await fetch(`${API_URL}/download`)
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `flipkart_reviews_${Date.now()}.xlsx`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } else {
        alert('File not found')
      }
    } catch (error) {
      alert('Error downloading file: ' + error.message)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <div className="logo">
            <span className="logo-icon">🛒</span>
            <h1>Flipkart Review Scraper</h1>
          </div>
          <p className="tagline">Extract product reviews with ease and precision</p>
        </header>

        <div className="content">
          <ScraperForm 
            onSubmit={handleStartScraping}
            isRunning={status.is_running}
          />

          <StatusPanel 
            status={status}
            onDownload={handleDownload}
          />
        </div>

        <footer className="footer">
          <p>
            Built with <span className="heart">❤️</span> using React + Flask
          </p>
          <p className="footer-note">
            Scrapes reviews safely with random delays to avoid detection
          </p>
        </footer>
      </div>
    </div>
  )
}

export default App
