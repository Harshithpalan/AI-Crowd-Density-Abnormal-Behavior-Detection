import React from 'react'
import './DetectionResults.css'

function DetectionResults({ data }) {
  if (!data) return null

  const { crowdDensity, abnormalBehaviors, timestamp } = data

  return (
    <div className="detection-results">
      <h2>Detection Results</h2>

      <div className="results-grid">
        <div className="result-card density-card">
          <h3>Crowd Density</h3>
          <div className="density-meter">
            <div
              className="density-fill"
              style={{
                width: `${Math.min(crowdDensity.density * 10, 100)}%`,
                background: getDensityColor(crowdDensity.density),
              }}
            />
          </div>
          <div className="density-value">
            <span className="count">{crowdDensity.count}</span>
            <span className="label">people detected</span>
          </div>
          <div className="density-level">
            Level: <span className={`level ${crowdDensity.level}`}>{crowdDensity.level}</span>
          </div>
        </div>

        <div className="result-card behavior-card">
          <h3>Abnormal Behaviors</h3>
          {abnormalBehaviors && abnormalBehaviors.length > 0 ? (
            <div className="behavior-list">
              {abnormalBehaviors.map((behavior, index) => (
                <div key={index} className="behavior-item">
                  <div className="behavior-type">{behavior.type}</div>
                  <div className="behavior-confidence">
                    Confidence: {(behavior.confidence * 100).toFixed(1)}%
                  </div>
                  {behavior.location && (
                    <div className="behavior-location">
                      Location: {behavior.location}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-behaviors">
              <span className="check-icon">✓</span>
              <span>No abnormal behaviors detected</span>
            </div>
          )}
        </div>
      </div>

      <div className="timestamp">
        Analyzed at: {new Date(timestamp).toLocaleString()}
      </div>
    </div>
  )
}

function getDensityColor(density) {
  if (density < 3) return '#2ecc71'
  if (density < 6) return '#f39c12'
  if (density < 9) return '#e67e22'
  return '#e74c3c'
}

export default DetectionResults
