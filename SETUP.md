# Setup Guide

## Quick Start

### Option 1: Using the startup script (Windows)

1. Double-click `start.bat` to start both servers
2. Wait for both servers to start
3. Open http://localhost:3000 in your browser

### Option 2: Manual startup

#### Terminal 1 - Backend:
```bash
cd backend
python app.py
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

Then open http://localhost:3000 in your browser.

## Detailed Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- pip (Python package manager)
- npm (Node package manager)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install Flask Flask-CORS opencv-python Pillow ultralytics
```

Note: The first time you run the app, it will automatically download the YOLOv8n model (about 6MB).

3. Start the Flask server:
```bash
python app.py
```

The backend will be available at http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Troubleshooting

### Backend Issues

**Issue: "Module not found" errors**
- Make sure you're in the backend directory
- Install dependencies: `pip install -r requirements.txt` or individual packages

**Issue: Model download fails**
- Check your internet connection
- The model will be downloaded automatically on first run
- If it fails, manually download from: https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8n.pt

**Issue: Port 5000 already in use**
- Change the port in `backend/app.py` (line 128)
- Or stop the process using port 5000

### Frontend Issues

**Issue: Vite won't start**
- Make sure you're in the frontend directory
- Run `npm install` to ensure all dependencies are installed
- Try using `node node_modules/vite/bin/vite.js` directly

**Issue: Port 3000 already in use**
- Change the port in `frontend/vite.config.js` (line 6)
- Or stop the process using port 3000

**Issue: Can't connect to backend**
- Make sure the backend server is running
- Check that CORS is enabled (it is by default)
- Verify the proxy configuration in `vite.config.js`

### Camera Issues

**Issue: Camera not accessible**
- Allow camera permissions in your browser
- Try using a different browser (Chrome, Firefox, Edge)
- Check if another application is using the camera
- For production, you need HTTPS (camera requires secure context)

## Testing the Application

1. Open http://localhost:3000
2. Test Upload Mode:
   - Upload an image with people
   - Click "Analyze"
   - View the detection results
3. Test Live Stream:
   - Click "Live Stream" tab
   - Click "Start Camera"
   - Allow camera permissions
   - View real-time analysis

## Production Deployment

### Backend

For production, use a WSGI server like Gunicorn or uWSGI:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend

Build the frontend for production:

```bash
cd frontend
npm run build
```

Serve the `dist` folder with nginx, Apache, or any web server.

## Additional Resources

- YOLOv8 Documentation: https://docs.ultralytics.com/
- Flask Documentation: https://flask.palletsprojects.com/
- React Documentation: https://react.dev/
- Vite Documentation: https://vitejs.dev/
