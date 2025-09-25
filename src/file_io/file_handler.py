import os
from datetime import datetime
from PIL import Image

def get_image_files(folder_path):
    """Yields paths of image files in a folder."""
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            yield os.path.join(folder_path, filename)

def get_watermark_text(image_path):
    """Extracts creation date from image EXIF data, or uses modification date as a fallback."""
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            creation_time_str = exif_data.get(36867) if exif_data else None
    except Exception:
        creation_time_str = None

    if creation_time_str:
        return creation_time_str.split(" ")[0].replace(":", "-")
    else:
        m_time = os.path.getmtime(image_path)
        print(f"Warning: No EXIF creation time for {os.path.basename(image_path)}. Using modification date.")
        return datetime.fromtimestamp(m_time).strftime('%Y-%m-%d')
