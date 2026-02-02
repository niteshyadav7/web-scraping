import './StatusPanel.css'

function StatusPanel({ status, onDownload }) {
  if (status.status === 'idle') return null

  return (
    <div className="status-panel">
      <div className="status-header">
        <h2>📊 Engine Status</h2>
        <div className={`status-badge ${status.status}`}>
          <span className="dot"></span>
          {status.status.toUpperCase()}
        </div>
      </div>

      <div className="status-grid">
        <div className="status-card">
          <div className="card-label">SCROLL DEPTH</div>
          <div className="card-value">{status.current_page}</div>
        </div>

        <div className="status-card highlight">
          <div className="card-label">TOTAL REVIEWS</div>
          <div className="card-value">{status.total_reviews}</div>
        </div>
      </div>

      {status.is_running && status.recent_reviews && status.recent_reviews.length > 0 && (
        <div className="live-feed">
          <h3>⚡ LIVE REVIEW FEED</h3>
          <div className="feed-items">
            {status.recent_reviews.map((rev, i) => (
              <div key={i} className="feed-item" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="feed-meta">
                  <span className="feed-rating">{"★".repeat(rev.rating)}</span>
                  <span className="feed-name">{rev.reviewer_name}</span>
                </div>
                <p className="feed-text">{rev.review.substring(0, 100)}...</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {status.is_running && (
        <div className="progress-container">
          <div className="progress-bar-glow"></div>
          <div className="progress-bar-fill"></div>
          <p>SCANNING DATA PACKETS...</p>
        </div>
      )}

      {status.status === 'completed' && (
        <div className="final-actions">
          {status.error ? (
            <div className="error-box">{status.error}</div>
          ) : (
            <button onClick={onDownload} className="btn-download">
              📥 EXPORT TO EXCEL (.XLSX)
            </button>
          )}
        </div>
      )}
    </div>
  )
}

export default StatusPanel
