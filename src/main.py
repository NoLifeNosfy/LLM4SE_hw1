import os
import argparse
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# A dictionary to map color names to RGBA values
COLOR_MAP = {
    "white": (255, 255, 255, 128),
    "black": (0, 0, 0, 128),
    "red": (255, 0, 0, 128),
    "green": (0, 255, 0, 128),
    "blue": (0, 0, 255, 128),
}

def add_watermark(image_path, text, output_path, font_size=40, font_color="white", position="bottom-right"):
    """Adds a text watermark to an image."""
    try:
        image = Image.open(image_path).convert("RGBA")
        txt = Image.new("RGBA", image.size, (255, 255, 255, 0))

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(txt)

        # Get text size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Position logic
        pos_y, pos_x = position.split('-')
        margin = 10

        if pos_x == 'left':
            x = margin
        elif pos_x == 'center':
            x = (image.width - text_width) / 2
        elif pos_x == 'right':
            x = image.width - text_width - margin
        else: # default to right
            x = image.width - text_width - margin

        if pos_y == 'top':
            y = margin
        elif pos_y == 'middle':
            y = (image.height - text_height) / 2
        elif pos_y == 'bottom':
            y = image.height - text_height - margin
        else: # default to bottom
            y = image.height - text_height - margin

        color = COLOR_MAP.get(font_color.lower(), (255, 255, 255, 128)) # Default to white

        draw.text((x, y), text, font=font, fill=color)

        watermarked = Image.alpha_composite(image, txt)
        watermarked.convert("RGB").save(output_path)
        print(f"Watermarked {os.path.basename(image_path)}")
    except Exception as e:
        print(f"Could not process {os.path.basename(image_path)}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Add watermarks to images.")
    parser.add_argument("folder_path", help="Path to the folder containing images.")
    parser.add_argument("--font_size", type=int, default=40, help="Font size of the watermark text.")
    parser.add_argument("--font_color", type=str, default="white", help="Font color of the watermark text (e.g., white, black, red).")
    parser.add_argument("--position", type=str, default="bottom-right", help="Position of the watermark (e.g., top-left, bottom-center).")

    args = parser.parse_args()

    folder_path = args.folder_path
    output_folder = os.path.join(folder_path, "_watermark")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(folder_path, filename)
            
            try:
                with Image.open(image_path) as img:
                    exif_data = img._getexif()
                    creation_time_str = exif_data.get(36867) if exif_data else None
            except Exception:
                creation_time_str = None

            if creation_time_str:
                watermark_text = creation_time_str.split(" ")[0].replace(":", "-")
            else:
                m_time = os.path.getmtime(image_path)
                watermark_text = datetime.fromtimestamp(m_time).strftime('%Y-%m-%d')
                print(f"Warning: No EXIF creation time for {filename}. Using modification date.")

            output_path = os.path.join(output_folder, filename)
            add_watermark(image_path, watermark_text, output_path, args.font_size, args.font_color, args.position)

if __name__ == "__main__":
    main()