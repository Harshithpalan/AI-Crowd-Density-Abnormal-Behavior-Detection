import React from 'react'
import './AlertPanel.css'

function AlertPanel({ alerts }) {
  return (
    <div className="alert-panel">
      <h2>Alerts</h2>
      <div className="alert-list">
        {alerts.length === 0 ? (
          <div className="no-alerts">
            <span className="icon">🔔</span>
            <p>No alerts</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div key={alert.id} className="alert-item">
              <div className="alert-header">
                <span className="alert-type">{alert.type}</span>
                <span className="alert-time">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <div className="alert-details">
                <div className="alert-confidence">
                  Confidence: {(alert.confidence * 100).toFixed(1)}%
                </div>
                {alert.location && (
                  <div className="alert-location">
                    Location: {alert.location}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default AlertPanel
