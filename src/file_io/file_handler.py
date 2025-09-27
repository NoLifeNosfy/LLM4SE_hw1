import os
from datetime import datetime
from PIL import Image
from watermarking.watermark import apply_text_watermark, apply_image_watermark

def get_image_paths(path, recursive=False):
    """
    Yields image file paths from a given path.
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    if os.path.isfile(path):
        if path.lower().endswith(image_extensions):
            yield path
    elif os.path.isdir(path):
        if recursive:
            for root, _, files in os.walk(path):
                for filename in files:
                    if filename.lower().endswith(image_extensions):
                        yield os.path.join(root, filename)
        else:
            for filename in os.listdir(path):
                if filename.lower().endswith(image_extensions):
                    yield os.path.join(path, filename)

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
        return datetime.fromtimestamp(m_time).strftime('%Y-%m-%d')

def export_images(
    image_paths,
    output_dir,
    watermark_settings=None,
    prefix="",
    suffix="",
    width_scale_ratio=1.0,
    height_scale_ratio=1.0,
    jpeg_quality=95
):
    """
    Exports images with various processing options, including applying a watermark.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_watermark_obj = None
    if watermark_settings and watermark_settings.get("type") == "image":
        image_path = watermark_settings.get("image_path")
        if image_path and os.path.exists(image_path):
            image_watermark_obj = Image.open(image_path)

    for image_path in image_paths:
        try:
            with Image.open(image_path) as img:
                # Apply watermark first
                if watermark_settings and watermark_settings.get("type") != "none": # Add a way to disable watermarking
                    if watermark_settings.get("type") == "text":
                        img = apply_text_watermark(img, watermark_settings)
                    elif image_watermark_obj:
                        img = apply_image_watermark(img, image_watermark_obj, watermark_settings)

                # Handle scaling based on ratios
                if width_scale_ratio != 1.0 or height_scale_ratio != 1.0:
                    orig_width, orig_height = img.size
                    new_width = int(orig_width * width_scale_ratio)
                    new_height = int(orig_height * height_scale_ratio)
                    if new_width > 0 and new_height > 0:
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Construct new filename
                original_filename = os.path.basename(image_path)
                name, ext = os.path.splitext(original_filename)
                new_filename = f"{prefix}{name}{suffix}{ext}"
                output_path = os.path.join(output_dir, new_filename)

                # Save the image
                if ext.lower() in ['.jpg', '.jpeg']:
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    img.save(output_path, 'JPEG', quality=jpeg_quality)
                else:
                    img.save(output_path)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
