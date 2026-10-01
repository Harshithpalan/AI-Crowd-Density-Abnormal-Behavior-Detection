"""
Model loading and inference utilities for crowd detection
"""
import torch
from ultralytics import YOLO
import cv2
import numpy as np

class CrowdDetector:
    def __init__(self, model_name='yolov8n.pt'):
        """
        Initialize the crowd detector with YOLO model
        """
        self.model = None
        self.model_name = model_name
        self.load_model()

    def load_model(self):
        """
        Load the YOLO model for person detection
        """
        try:
            print(f"Loading model: {self.model_name}")
            self.model = YOLO(self.model_name)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise

    def detect_persons(self, image, conf_threshold=0.5):
        """
        Detect persons in an image

        Args:
            image: numpy array of the image
            conf_threshold: confidence threshold for detections

        Returns:
            list of detected persons with bounding boxes and confidence
        """
        if self.model is None:
            raise ValueError("Model not loaded")

        # Run detection
        results = self.model(image, conf=conf_threshold)

        # Extract person detections
        persons = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if box.cls == 0:  # class 0 is 'person' in COCO dataset
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    persons.append({
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'confidence': float(confidence)
                    })

        return persons

    def calculate_density(self, persons, image_shape):
        """
        Calculate crowd density based on person count and image area

        Args:
            persons: list of detected persons
            image_shape: tuple of (height, width, channels)

        Returns:
            dict with count, density value, and level
        """
        person_count = len(persons)
        image_area = image_shape[0] * image_shape[1]
        density = person_count / (image_area / 10000)  # persons per 10,000 pixels

        # Determine density level
        if density < 1:
            level = 'low'
        elif density < 3:
            level = 'medium'
        elif density < 5:
            level = 'high'
        else:
            level = 'critical'

        return {
            'count': person_count,
            'density': round(density, 2),
            'level': level
        }

class BehaviorAnalyzer:
    """
    Analyze behaviors from detected persons
    """
    def __init__(self):
        self.behavior_types = [
            'crowding',
            'clustering',
            'rapid_movement',
            'fighting',
            'running',
            'falling'
        ]

    def analyze(self, persons, image_array):
        """
        Analyze behaviors from person detections

        Args:
            persons: list of detected persons
            image_array: numpy array of the image

        Returns:
            list of detected abnormal behaviors
        """
        behaviors = []

        if len(persons) < 2:
            return behaviors

        # Check for crowding
        behaviors.extend(self._detect_crowding(persons))

        # Check for clustering
        behaviors.extend(self._detect_clustering(persons))

        # Check for rapid movement (simplified)
        if len(persons) > 10:
            behaviors.append({
                'type': 'rapid_movement',
                'confidence': 0.7,
                'location': 'detected across frame'
            })

        return behaviors

    def _detect_crowding(self, persons, threshold=50):
        """
        Detect crowding (people too close together)
        """
        behaviors = []
        for i in range(len(persons)):
            for j in range(i + 1, len(persons)):
                bbox1 = persons[i]['bbox']
                bbox2 = persons[j]['bbox']

                center1 = [(bbox1[0] + bbox1[2]) / 2, (bbox1[1] + bbox1[3]) / 2]
                center2 = [(bbox2[0] + bbox2[2]) / 2, (bbox2[1] + bbox2[3]) / 2]

                distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)

                if distance < threshold:
                    behaviors.append({
                        'type': 'crowding',
                        'confidence': min(0.9, 0.5 + (threshold - distance) / 100),
                        'location': f"Between persons at ({int(center1[0])}, {int(center1[1])})"
                    })

        return behaviors

    def _detect_clustering(self, persons, threshold=100):
        """
        Detect clustering (many people in small area)
        """
        behaviors = []

        if len(persons) < 5:
            return behaviors

        avg_x = sum([p['bbox'][0] for p in persons]) / len(persons)
        avg_y = sum([p['bbox'][1] for p in persons]) / len(persons)

        spread = np.sqrt(sum([(p['bbox'][0] - avg_x)**2 + (p['bbox'][1] - avg_y)**2 for p in persons]) / len(persons))

        if spread < threshold:
            behaviors.append({
                'type': 'clustering',
                'confidence': min(0.95, 0.6 + (threshold - spread) / 200),
                'location': f"Cluster center at ({int(avg_x)}, {int(avg_y)})"
            })

        return behaviors
