"""
Batch processing utility for multiple images/videos
"""
import os
import cv2
import numpy as np
from PIL import Image
from models import CrowdDetector, BehaviorAnalyzer
import json
from datetime import datetime

class BatchProcessor:
    def __init__(self, model_name='yolov8n.pt'):
        """
        Initialize batch processor
        """
        self.detector = CrowdDetector(model_name)
        self.analyzer = BehaviorAnalyzer()

    def process_directory(self, input_dir, output_dir):
        """
        Process all images in a directory

        Args:
            input_dir: path to input directory
            output_dir: path to output directory for results
        """
        os.makedirs(output_dir, exist_ok=True)

        # Get all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        files = [f for f in os.listdir(input_dir)
                 if any(f.lower().endswith(ext) for ext in image_extensions)]

        results = []

        for file in files:
            file_path = os.path.join(input_dir, file)
            print(f"Processing: {file}")

            try:
                result = self.process_image(file_path)
                result['filename'] = file
                results.append(result)

                # Save individual result
                output_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}_result.json")
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)

            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
                results.append({
                    'filename': file,
                    'error': str(e)
                })

        # Save summary
        summary = {
            'total_files': len(files),
            'processed': len([r for r in results if 'error' not in r]),
            'failed': len([r for r in results if 'error' in r]),
            'results': results,
            'timestamp': datetime.now().isoformat()
        }

        summary_file = os.path.join(output_dir, 'batch_summary.json')
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"\nBatch processing complete!")
        print(f"Processed: {summary['processed']}/{summary['total_files']}")
        print(f"Results saved to: {output_dir}")

        return summary

    def process_image(self, image_path):
        """
        Process a single image

        Args:
            image_path: path to image file

        Returns:
            dict with detection results
        """
        # Read image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect persons
        persons = self.detector.detect_persons(image)

        # Calculate density
        density = self.detector.calculate_density(persons, image.shape)

        # Analyze behaviors
        behaviors = self.analyzer.analyze(persons, image)

        return {
            'crowdDensity': density,
            'abnormalBehaviors': behaviors,
            'timestamp': datetime.now().isoformat()
        }

if __name__ == '__main__':
    # Example usage
    processor = BatchProcessor()

    # Process a directory
    input_dir = 'input_images'
    output_dir = 'output_results'

    if os.path.exists(input_dir):
        processor.process_directory(input_dir, output_dir)
    else:
        print(f"Input directory '{input_dir}' not found.")
        print("Create an 'input_images' directory and add images to process.")
