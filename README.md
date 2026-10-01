# AI Crowd Density & Abnormal Behavior Detection

A full-stack web application for real-time crowd density analysis and abnormal behavior detection using computer vision and deep learning.

## Features

- **Real-time Video Processing**: Live camera feed analysis for crowd monitoring
- **Image Upload**: Upload static images for analysis
- **Batch Processing**: Process multiple images at once
- **Crowd Density Detection**: Real-time counting and density level assessment
- **Abnormal Behavior Detection**: Identify crowding, clustering, and rapid movement
- **Alert System**: Real-time notifications for detected anomalies
- **Interactive Dashboard**: Modern React-based user interface

## Tech Stack

### Frontend
- React 19
- Vite
- Axios for API calls
- CSS3 with modern styling

### Backend
- Flask (Python)
- YOLOv8 for object detection
- OpenCV for image processing
- PyTorch for deep learning
- NumPy for numerical operations

## Project Structure

```
AI Crowd Density & Abnormal Behavior Detection/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── styles/         # CSS stylesheets
│   │   ├── App.jsx         # Main App component
│   │   └── main.jsx        # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/                 # Flask backend API
│   ├── app.py              # Main Flask application
│   ├── models.py           # ML model utilities
│   ├── batch_processor.py  # Batch processing utilities
│   └── requirements.txt   # Python dependencies
└── README.md
```

## Installation

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.8 or higher)
- pip

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the Flask server:
```bash
python app.py
```

The backend API will be available at `http://localhost:5000`

## Usage

### Upload Mode
1. Click "Upload Mode" in the dashboard
2. Drag and drop an image or video, or click to select a file
3. Click "Analyze" for single file processing or "Batch Process" for batch mode
4. View detection results including crowd density and abnormal behaviors

### Live Stream Mode
1. Click "Live Stream" in the dashboard
2. Click "Start Camera" to begin real-time analysis
3. The system will continuously analyze frames from your camera
4. Alerts will appear in the side panel when abnormal behaviors are detected
4. Click "Stop Camera" to end the stream

## API Endpoints

### POST /api/upload
Upload an image or video for analysis.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (image or video)

**Response:**
```json
{
  "crowdDensity": {
    "count": 5,
    "density": 2.5,
    "level": "medium"
  },
  "abnormalBehaviors": [
    {
      "type": "crowding",
      "confidence": 0.85,
      "location": "Between persons at (250, 300)"
    }
  ],
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

### GET /api/info
API information endpoint.

**Response:**
```json
{
  "name": "AI Crowd Density & Abnormal Behavior Detection API",
  "version": "1.0.0",
  "endpoints": {
    "/api/upload": "POST - Upload image/video for analysis",
    "/api/health": "GET - Health check",
    "/api/info": "GET - API information"
  }
}
```

## Model Information

The application uses YOLOv8n (nano) model for person detection:
- Fast inference suitable for real-time applications
- Trained on COCO dataset (class 0 = person)
- Confidence threshold: 0.5
- Can be replaced with larger models (YOLOv8s, m, l, x) for higher accuracy

## Density Levels

- **Low**: < 1 person per 10,000 pixels
- **Medium**: 1-3 persons per 10,000 pixels
- **High**: 3-5 persons per 10,000 pixels
- **Critical**: > 5 persons per 10,000 pixels

## Abnormal Behaviors Detected

- **Crowding**: People standing too close together
- **Clustering**: Many people gathered in a small area
- **Rapid Movement**: Fast movement detected across the frame

## Development

### Running in Development Mode

1. Start the backend:
```bash
cd backend
python app.py
```

2. Start the frontend (in a new terminal):
```bash
cd frontend
npm run dev
```

### Building for Production

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. The built files will be in the `frontend/dist` directory

3. Serve the built files with a production web server (nginx, Apache, etc.)

## Troubleshooting

### Camera Access Issues
- Ensure camera permissions are granted in your browser
- Check if another application is using the camera
- Try using HTTPS if running in production (camera requires secure context)

### Model Loading Issues
- Ensure all dependencies are installed correctly
- Check internet connection (first run downloads YOLO model)
- Verify PyTorch installation matches your system

### Performance Issues
- Use YOLOv8n for faster inference
- Reduce video frame rate in VideoStream component
- Lower image resolution before uploading

## Future Enhancements

- [ ] Add more sophisticated behavior detection (fighting, falling, etc.)
- [ ] Implement temporal analysis for better movement detection
- [ ] Add video export with detection overlays
- [ ] Support for multiple camera feeds
- [ ] Historical data and analytics dashboard
- [ ] Integration with alert systems (email, SMS, etc.)
- [ ] Mobile application support

## License

This project is for educational and research purposes.

## Acknowledgments

- YOLOv8 by Ultralytics
- React team
- Flask community
