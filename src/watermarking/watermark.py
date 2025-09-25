import os
from PIL import Image, ImageDraw, ImageFont

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
