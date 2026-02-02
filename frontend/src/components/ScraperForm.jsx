import { useState } from 'react'
import './ScraperForm.css'

function ScraperForm({ onSubmit, isRunning }) {
  const [mode, setMode] = useState('single') // 'single' or 'multiple'
  const [formData, setFormData] = useState({
    url: '',
    from_date: '2020-01-01',
    to_date: new Date().toISOString().split('T')[0],
    max_pages: 100
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const handleChange = (field, value) => {
    setFormData({ ...formData, [field]: value })
  }

  const handleModeChange = (newMode) => {
    setMode(newMode)
    // Clear URL when switching modes
    setFormData({ ...formData, url: '' })
  }

  const getUrlCount = () => {
    if (!formData.url.trim()) return 0
    return formData.url.trim().split('\n').filter(u => u.trim()).length
  }

  return (
    <form onSubmit={handleSubmit} className="scraper-form">
      {/* Mode Toggle */}
      <div className="mode-toggle">
        <button
          type="button"
          className={`mode-btn ${mode === 'single' ? 'active' : ''}`}
          onClick={() => handleModeChange('single')}
          disabled={isRunning}
        >
          <span className="mode-icon">📦</span>
          Single Product
        </button>
        <button
          type="button"
          className={`mode-btn ${mode === 'multiple' ? 'active' : ''}`}
          onClick={() => handleModeChange('multiple')}
          disabled={isRunning}
        >
          <span className="mode-icon">📚</span>
          Multiple Products
        </button>
      </div>

      {/* URL Input - Changes based on mode */}
      {mode === 'single' ? (
        <div className="form-group">
          <label htmlFor="url">
            <span className="label-icon">🔗</span>
            Product URL
          </label>
          <input
            type="url"
            id="url"
            placeholder="https://www.flipkart.com/product/..."
            value={formData.url}
            onChange={(e) => handleChange('url', e.target.value)}
            required
            disabled={isRunning}
          />
        </div>
      ) : (
        <div className="form-group">
          <label htmlFor="url">
            <span className="label-icon">🔗</span>
            Product URLs
            <span className="label-hint">
              {getUrlCount() > 0 ? 
                `(${getUrlCount()} product${getUrlCount() !== 1 ? 's' : ''})` 
                : '(one URL per line)'}
            </span>
          </label>
          <textarea
            id="url"
            placeholder="https://www.flipkart.com/product1/...&#10;https://www.flipkart.com/product2/...&#10;https://www.flipkart.com/product3/..."
            value={formData.url}
            onChange={(e) => handleChange('url', e.target.value)}
            required
            disabled={isRunning}
            rows="5"
            style={{ resize: 'vertical', minHeight: '120px' }}
          />
        </div>
      )}

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="from_date">
            <span className="label-icon">📅</span>
            From Date
          </label>
          <input
            type="date"
            id="from_date"
            value={formData.from_date}
            onChange={(e) => handleChange('from_date', e.target.value)}
            required
            disabled={isRunning}
          />
        </div>

        <div className="form-group">
          <label htmlFor="to_date">
            <span className="label-icon">📅</span>
            To Date
          </label>
          <input
            type="date"
            id="to_date"
            value={formData.to_date}
            onChange={(e) => handleChange('to_date', e.target.value)}
            required
            disabled={isRunning}
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="max_pages">
          <span className="label-icon">📄</span>
          Max Pages
          <span className="label-hint">
            {mode === 'multiple' && getUrlCount() > 0 
              ? `(~${formData.max_pages * 10 * getUrlCount()} reviews total)` 
              : `(~${formData.max_pages * 10} reviews)`}
          </span>
        </label>
        <div className="slider-container">
          <input
            type="range"
            id="max_pages"
            min="1"
            max="500"
            value={formData.max_pages}
            onChange={(e) => handleChange('max_pages', parseInt(e.target.value))}
            disabled={isRunning}
            className="slider"
          />
          <span className="slider-value">{formData.max_pages}</span>
        </div>
      </div>

      <button 
        type="submit" 
        className="btn btn-primary"
        disabled={isRunning}
      >
        {isRunning ? (
          <>
            <span className="spinner"></span>
            Scraping...
          </>
        ) : (
          <>
            <span>🚀</span>
            {mode === 'multiple' && getUrlCount() > 1 
              ? `Start Scraping ${getUrlCount()} Products` 
              : 'Start Scraping'}
          </>
        )}
      </button>
    </form>
  )
}

export default ScraperForm
