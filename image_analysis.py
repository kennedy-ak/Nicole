import os
import json
from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd
from datetime import datetime
import numpy as np

def extract_exif_data(image_path):
    """Extract EXIF metadata from an image"""
    try:
        image = Image.open(image_path)
        exif_data = {}

        # Get EXIF data if available
        exif = image._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = str(value)

        # Basic image properties
        exif_data['Width'] = image.width
        exif_data['Height'] = image.height
        exif_data['Format'] = image.format
        exif_data['Mode'] = image.mode

        return exif_data
    except Exception as e:
        return {'Error': str(e)}

def calculate_image_quality_metrics(image_path):
    """Calculate basic quality metrics for an image"""
    try:
        image = Image.open(image_path)
        img_array = np.array(image)

        metrics = {
            'resolution': f"{image.width}x{image.height}",
            'megapixels': round((image.width * image.height) / 1_000_000, 2),
            'aspect_ratio': round(image.width / image.height, 2),
            'file_size_kb': round(os.path.getsize(image_path) / 1024, 2),
        }

        # Calculate brightness (mean pixel intensity)
        if len(img_array.shape) == 3:  # Color image
            brightness = np.mean(img_array)
        else:  # Grayscale
            brightness = np.mean(img_array)
        metrics['brightness'] = round(brightness, 2)

        # Calculate sharpness approximation (Laplacian variance)
        from scipy import ndimage
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
        laplacian_var = ndimage.laplace(gray).var()
        metrics['sharpness_score'] = round(laplacian_var, 2)

        return metrics
    except Exception as e:
        return {'Error': str(e)}

def analyze_eye_images():
    """Analyze all eye images and create tracking spreadsheet"""

    base_dir = r"C:\Users\User2\Desktop\Nicole"

    # Define paths
    left_eye_dir = os.path.join(base_dir, "Upload Image of Your Left Eye (Taken with your smartphone)  Untitled Question (File responses)-20251215T225135Z-3-001",
                                "Upload Image of Your Left Eye (Taken with your smartphone)  Untitled Question (File responses)")
    right_eye_dir = os.path.join(base_dir, "Upload Image of Your Right Eye (Taken with your smartphone) (File responses)-20251215T225137Z-3-001",
                                 "Upload Image of Your Right Eye (Taken with your smartphone) (File responses)")

    results = []

    # Process left eye images
    if os.path.exists(left_eye_dir):
        for filename in os.listdir(left_eye_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(left_eye_dir, filename)
                print(f"Processing left eye: {filename}")

                exif = extract_exif_data(filepath)
                quality = calculate_image_quality_metrics(filepath)

                result = {
                    'participant_id': filename.split('.')[0],
                    'eye_side': 'LEFT',
                    'filename': filename,
                    'filepath': filepath,
                    'width': exif.get('Width', 'N/A'),
                    'height': exif.get('Height', 'N/A'),
                    'resolution': quality.get('resolution', 'N/A'),
                    'megapixels': quality.get('megapixels', 'N/A'),
                    'file_size_kb': quality.get('file_size_kb', 'N/A'),
                    'brightness': quality.get('brightness', 'N/A'),
                    'sharpness_score': quality.get('sharpness_score', 'N/A'),
                    'camera_make': exif.get('Make', 'N/A'),
                    'camera_model': exif.get('Model', 'N/A'),
                    'datetime': exif.get('DateTime', 'N/A'),
                    'flash': exif.get('Flash', 'N/A'),
                    'focal_length': exif.get('FocalLength', 'N/A'),
                    'iso': exif.get('ISOSpeedRatings', 'N/A'),
                    'exposure_time': exif.get('ExposureTime', 'N/A'),
                }
                results.append(result)

    # Process right eye images
    if os.path.exists(right_eye_dir):
        for filename in os.listdir(right_eye_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = os.path.join(right_eye_dir, filename)
                print(f"Processing right eye: {filename}")

                exif = extract_exif_data(filepath)
                quality = calculate_image_quality_metrics(filepath)

                result = {
                    'participant_id': filename.split('.')[0],
                    'eye_side': 'RIGHT',
                    'filename': filename,
                    'filepath': filepath,
                    'width': exif.get('Width', 'N/A'),
                    'height': exif.get('Height', 'N/A'),
                    'resolution': quality.get('resolution', 'N/A'),
                    'megapixels': quality.get('megapixels', 'N/A'),
                    'file_size_kb': quality.get('file_size_kb', 'N/A'),
                    'brightness': quality.get('brightness', 'N/A'),
                    'sharpness_score': quality.get('sharpness_score', 'N/A'),
                    'camera_make': exif.get('Make', 'N/A'),
                    'camera_model': exif.get('Model', 'N/A'),
                    'datetime': exif.get('DateTime', 'N/A'),
                    'flash': exif.get('Flash', 'N/A'),
                    'focal_length': exif.get('FocalLength', 'N/A'),
                    'iso': exif.get('ISOSpeedRatings', 'N/A'),
                    'exposure_time': exif.get('ExposureTime', 'N/A'),
                }
                results.append(result)

    # Create DataFrame
    df = pd.DataFrame(results)

    # Save to CSV
    output_csv = os.path.join(base_dir, 'phase_a_image_tracking.csv')
    df.to_csv(output_csv, index=False)
    print(f"\nTracking spreadsheet saved to: {output_csv}")

    # Generate summary statistics
    print("\n" + "="*60)
    print("PHASE A - IMAGE ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total images analyzed: {len(df)}")
    print(f"Left eye images: {len(df[df['eye_side'] == 'LEFT'])}")
    print(f"Right eye images: {len(df[df['eye_side'] == 'RIGHT'])}")
    print(f"\nUnique camera models detected: {df['camera_model'].nunique()}")
    print(f"Camera models: {df['camera_model'].unique()}")

    print("\n" + "-"*60)
    print("IMAGE QUALITY METRICS")
    print("-"*60)

    # Filter numeric columns for statistics
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        print(f"Average resolution: {df['megapixels'].mean():.2f} MP")
        print(f"Resolution range: {df['megapixels'].min():.2f} - {df['megapixels'].max():.2f} MP")
        print(f"Average file size: {df['file_size_kb'].mean():.2f} KB")
        print(f"Average brightness: {df['brightness'].mean():.2f}")
        print(f"Average sharpness: {df['sharpness_score'].mean():.2f}")

    return df

if __name__ == "__main__":
    try:
        df = analyze_eye_images()

        # Save detailed JSON report
        report = {
            'analysis_date': datetime.now().isoformat(),
            'total_images': len(df),
            'summary': df.describe().to_dict(),
            'camera_models': df['camera_model'].value_counts().to_dict()
        }

        with open(r'C:\Users\User2\Desktop\Nicole\analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)

        print("\nDetailed report saved to: analysis_report.json")

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
