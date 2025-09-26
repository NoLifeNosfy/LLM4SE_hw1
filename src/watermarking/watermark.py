import os
from PIL import Image, ImageDraw, ImageFont, ImageColor

# A dictionary to map color names to RGBA values
COLOR_MAP = {
    "white": (255, 255, 255, 128),
    "black": (0, 0, 0, 128),
    "red": (255, 0, 0, 128),
    "green": (0, 255, 0, 128),
    "blue": (0, 0, 255, 128),
}

def apply_text_watermark(image, settings):
    """Applies a text watermark to a PIL image based on a settings dictionary."""
    if not image:
        return None

    # Create a transparent layer for the text
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Font
    font_family = settings.get("font_family", "arial.ttf")
    font_size = settings.get("font_size", 36)
    try:
        font = ImageFont.truetype(font_family, font_size)
    except IOError:
        font = ImageFont.load_default()

    # Text
    text = settings.get("text", "")
    if not text:
        return image # Return original image if no text

    # Position
    position = settings.get("position", "Center")
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    margin = 10

    if "Top" in position:
        y = margin
    elif "Middle" in position or "Center" in position:
        y = (image.height - text_height) / 2
    elif "Bottom" in position:
        y = image.height - text_height - margin
    else:
        y = (image.height - text_height) / 2 # Default to center

    if "Left" in position:
        x = margin
    elif "Center" in position:
        x = (image.width - text_width) / 2
    elif "Right" in position:
        x = image.width - text_width - margin
    else:
        x = (image.width - text_width) / 2 # Default to center

    # Shadow
    if settings.get("shadow", False):
        shadow_size = settings.get("shadow_size", 2)
        shadow_color = (0, 0, 0, 128) # Default shadow color
        draw.text((x + shadow_size, y + shadow_size), text, font=font, fill=shadow_color)

    # Stroke
    if settings.get("stroke", False):
        stroke_size = settings.get("stroke_size", 1)
        stroke_color = settings.get("stroke_color", "#000000")
        draw.text((x, y), text, font=font, fill=stroke_color, stroke_width=stroke_size, stroke_fill=stroke_color)

    # Main Text
    font_color = settings.get("font_color", "#000000")
    opacity = int(settings.get("opacity", 1.0) * 255)
    font_color_rgba = ImageColor.getrgb(font_color) + (opacity,)
    draw.text((x, y), text, font=font, fill=font_color_rgba)

    # Rotation
    rotation = settings.get("rotation", 0)
    if rotation != 0:
        txt_layer = txt_layer.rotate(rotation, expand=True, center=(x + text_width / 2, y + text_height / 2))

    # Composite the text layer onto the image
    watermarked_image = Image.alpha_composite(image.convert("RGBA"), txt_layer)
    return watermarked_image
