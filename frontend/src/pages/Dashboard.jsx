import React, { useState } from 'react'
import FileUpload from '../components/FileUpload'
import VideoStream from '../components/VideoStream'
import DetectionResults from '../components/DetectionResults'
import AlertPanel from '../components/AlertPanel'
import './Dashboard.css'

function Dashboard() {
  const [mode, setMode] = useState('upload') // 'upload' or 'stream'
  const [detectionData, setDetectionData] = useState(null)
  const [alerts, setAlerts] = useState([])

  const handleDetectionComplete = (data) => {
    setDetectionData(data)
    if (data.abnormalBehaviors && data.abnormalBehaviors.length > 0) {
      const newAlerts = data.abnormalBehaviors.map(behavior => ({
        id: Date.now() + Math.random(),
        type: behavior.type,
        timestamp: new Date().toISOString(),
        confidence: behavior.confidence,
        location: behavior.location
      }))
      setAlerts(prev => [...newAlerts, ...prev].slice(0, 50))
    }
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>AI Crowd Density & Abnormal Behavior Detection</h1>
        <div className="mode-toggle">
          <button
            className={mode === 'upload' ? 'active' : ''}
            onClick={() => setMode('upload')}
          >
            Upload Mode
          </button>
          <button
            className={mode === 'stream' ? 'active' : ''}
            onClick={() => setMode('stream')}
          >
            Live Stream
          </button>
        </div>
      </header>

      <div className="dashboard-content">
        <div className="main-panel">
          {mode === 'upload' ? (
            <FileUpload onDetectionComplete={handleDetectionComplete} />
          ) : (
            <VideoStream onDetectionComplete={handleDetectionComplete} />
          )}
          {detectionData && (
            <DetectionResults data={detectionData} />
          )}
        </div>

        <div className="side-panel">
          <AlertPanel alerts={alerts} />
        </div>
      </div>
    </div>
  )
}

export default Dashboard
