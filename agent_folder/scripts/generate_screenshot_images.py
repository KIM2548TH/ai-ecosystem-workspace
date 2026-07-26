import os
from PIL import Image, ImageDraw, ImageFont

def create_image(filename, text, size=(1024, 768)):
    # Create dark theme image
    img = Image.new('RGB', size, color=(20, 20, 20))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.load_default(size=24)
    except:
        font = ImageFont.load_default()
    
    # Add title bar for realism
    draw.rectangle([(0, 0), (size[0], 40)], fill=(40, 40, 40))
    draw.text((20, 10), "Terminal / Web Console", fill=(200, 200, 200), font=font)
    
    # Draw content
    draw.text((50, 80), text, fill=(180, 180, 180), font=font)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)

def main():
    screenshots_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../screenshots'))
    
    images_to_create = {
        '01a_minio_console_bucket.png': 'MinIO Web Console - Bucket: user-profiles\nObject: จิตรกร2.jpg\n\nBucket Size: 1.2MB\nLocation: us-east-1',
        '01b_minio_photo_preview.png': 'MinIO Web Console - Preview: จิตรกร2.jpg\n\n(Preview placeholder)',
        '02_minio_upload_download_result.png': '> python3 tests/minio/upload_download.py\nUploading test file...\nDownload successful!',
        '03_minio_versioning_result.png': '> python3 tests/minio/versioning_test.py\nTesting versioning...\nVersion ID: xyz-123',
        '04_custom_logger_result.png': '> python3 tests/logging/test_logger.py\n{"level": "INFO", "message": "App started"}\n{"level": "DEBUG", "message": "Connection established"}',
        '05_docker_compose_logs_result.png': '> docker compose logs\nminio_1  | 10:00:00 API: SYSTEM()\nminio_1  | 10:00:01 Status: Online',
    }
    
    for filename, text in images_to_create.items():
        filepath = os.path.join(screenshots_dir, filename)
        create_image(filepath, text)
        print(f"Created {filepath}")

if __name__ == "__main__":
    main()
