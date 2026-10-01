from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io
from datetime import datetime
from models import CrowdDetector, BehaviorAnalyzer

app = Flask(__name__)
CORS(app)

# Initialize detectors
crowd_detector = None
behavior_analyzer = None

def initialize_detectors():
    global crowd_detector, behavior_analyzer
    if crowd_detector is None:
        crowd_detector = CrowdDetector('yolov8n.pt')
    if behavior_analyzer is None:
        behavior_analyzer = BehaviorAnalyzer()
    return crowd_detector, behavior_analyzer

def analyze_image(image_array):
    """
    Analyze image for crowd density and abnormal behaviors
    """
    try:
        # Initialize detectors
        detector, analyzer = initialize_detectors()

        # Detect persons
        persons = detector.detect_persons(image_array)

        # Calculate crowd density
        density = detector.calculate_density(persons, image_array.shape)

        # Analyze behaviors
        abnormal_behaviors = analyzer.analyze(persons, image_array)

        return {
            'crowdDensity': density,
            'abnormalBehaviors': abnormal_behaviors,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Error in analyze_image: {str(e)}")
        return {
            'crowdDensity': {'count': 0, 'density': 0, 'level': 'low'},
            'abnormalBehaviors': [],
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload for analysis
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        is_stream = request.form.get('stream', 'false') == 'true'
        is_batch = request.form.get('batch', 'false') == 'true'

        # Read file
        file_bytes = file.read()

        # Convert to image
        image = Image.open(io.BytesIO(file_bytes))
        image_array = np.array(image)

        # Convert to RGB if needed
        if len(image_array.shape) == 3 and image_array.shape[2] == 4:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        elif len(image_array.shape) == 2:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)

        # Analyze
        result = analyze_image(image_array)

        if is_batch:
            # For batch processing, return multiple frames' results
            result['batchMode'] = True
            result['framesProcessed'] = 1

        return jsonify(result)

    except Exception as e:
        print(f"Error in upload_file: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    global crowd_detector
    return jsonify({
        'status': 'healthy',
        'model_loaded': crowd_detector is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/info', methods=['GET'])
def info():
    """
    API information endpoint
    """
    return jsonify({
        'name': 'AI Crowd Density & Abnormal Behavior Detection API',
        'version': '1.0.0',
        'endpoints': {
            '/api/upload': 'POST - Upload image/video for analysis',
            '/api/health': 'GET - Health check',
            '/api/info': 'GET - API information'
        }
    })

if __name__ == '__main__':
    # Initialize detectors on startup
    initialize_detectors()
    print("Model loaded successfully")
    print("Starting Flask server on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
