import React, { useState } from 'react'
import axios from 'axios'
import './FileUpload.css'

function FileUpload({ onDetectionComplete }) {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError(null)

      if (selectedFile.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onloadend = () => setPreview(reader.result)
        reader.readAsDataURL(selectedFile)
      } else if (selectedFile.type.startsWith('video/')) {
        setPreview(URL.createObjectURL(selectedFile))
      }
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onDetectionComplete(response.data)
    } catch (err) {
      setError('Failed to process file. Please try again.')
      console.error('Upload error:', err)
    } finally {
      setUploading(false)
    }
  }

  const handleBatchUpload = async () => {
    if (!file) return

    setUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('batch', 'true')

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onDetectionComplete(response.data)
    } catch (err) {
      setError('Failed to process batch. Please try again.')
      console.error('Batch upload error:', err)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="file-upload">
      <div className="upload-container">
        <div className="upload-area">
          {preview ? (
            <div className="preview">
              {file?.type.startsWith('image/') ? (
                <img src={preview} alt="Preview" />
              ) : (
                <video src={preview} controls />
              )}
            </div>
          ) : (
            <div className="upload-placeholder">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              <p>Drag & drop an image or video here, or click to select</p>
            </div>
          )}
          <input
            type="file"
            accept="image/*,video/*"
            onChange={handleFileChange}
            className="file-input"
          />
        </div>

        {file && (
          <div className="file-info">
            <p className="file-name">{file.name}</p>
            <p className="file-size">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
          </div>
        )}

        {error && <div className="error-message">{error}</div>}

        <div className="upload-buttons">
          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="upload-button"
          >
            {uploading ? 'Processing...' : 'Analyze'}
          </button>
          <button
            onClick={handleBatchUpload}
            disabled={!file || uploading}
            className="batch-button"
          >
            {uploading ? 'Processing...' : 'Batch Process'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default FileUpload
