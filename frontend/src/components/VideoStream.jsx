import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './VideoStream.css'

function VideoStream({ onDetectionComplete }) {
  const [streaming, setStreaming] = useState(false)
  const [error, setError] = useState(null)
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const intervalRef = useRef(null)

  const startStream = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      videoRef.current.srcObject = stream
      setStreaming(true)
      setError(null)

      intervalRef.current = setInterval(() => {
        captureAndSendFrame()
      }, 1000) // Send frame every second
    } catch (err) {
      setError('Failed to access camera. Please allow camera permissions.')
      console.error('Camera error:', err)
    }
  }

  const stopStream = () => {
    if (videoRef.current?.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop())
    }
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
    }
    setStreaming(false)
  }

  const captureAndSendFrame = async () => {
    if (!videoRef.current || !canvasRef.current) return

    const canvas = canvasRef.current
    const context = canvas.getContext('2d')
    canvas.width = videoRef.current.videoWidth
    canvas.height = videoRef.current.videoHeight
    context.drawImage(videoRef.current, 0, 0)

    canvas.toBlob(async (blob) => {
      if (!blob) return

      const formData = new FormData()
      formData.append('file', blob, 'frame.jpg')
      formData.append('stream', 'true')

      try {
        const response = await axios.post('/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        onDetectionComplete(response.data)
      } catch (err) {
        console.error('Stream frame error:', err)
      }
    }, 'image/jpeg', 0.8)
  }

  useEffect(() => {
    return () => {
      stopStream()
    }
  }, [])

  return (
    <div className="video-stream">
      <div className="stream-container">
        <div className="video-wrapper">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="video-feed"
          />
          <canvas ref={canvasRef} className="hidden-canvas" />
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="stream-controls">
          {!streaming ? (
            <button onClick={startStream} className="start-button">
              Start Camera
            </button>
          ) : (
            <button onClick={stopStream} className="stop-button">
              Stop Camera
            </button>
          )}
        </div>

        {streaming && (
          <div className="stream-status">
            <span className="status-indicator live"></span>
            <span>Live Stream Active</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default VideoStream
