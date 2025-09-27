import os
from PIL import Image, ImageDraw, ImageFont, ImageColor

def _get_font(font_family, font_size):
    """Helper function to load a font, with fallbacks."""
    font_name_to_file = {
        "SimSun": "C:\\Windows\\Fonts\\simsun.ttc",
        "Microsoft YaHei": "C:\\Windows\\Fonts\\msyh.ttc",
        "SimHei": "C:\\Windows\\Fonts\\simhei.ttf",
        "KaiTi": "C:\\Windows\\Fonts\\simkai.ttf",
        "FangSong": "C:\\Windows\\Fonts\\simfang.ttf",
        "NSimSun": "C:\\Windows\\Fonts\\simsun.ttc",
        "Arial": "C:\\Windows\\Fonts\\arial.ttf"
    }
    fallback_font_files = [
        "C:\\Windows\\Fonts\\simsun.ttc",
        "C:\\Windows\\Fonts\\msyh.ttc",
        "C:\\Windows\\Fonts\\simhei.ttf",
        "C:\\Windows\\Fonts\\arial.ttf"
    ]
    
    font = None
    if font_family in font_name_to_file:
        try:
            font = ImageFont.truetype(font_name_to_file[font_family], size=font_size)
        except IOError:
            pass
    
    if font is None:
        try:
            font = ImageFont.truetype(font_family, size=font_size)
        except IOError:
            for font_file in fallback_font_files:
                try:
                    font = ImageFont.truetype(font_file, size=font_size)
                    break
                except IOError:
                    continue
    
    if font is None:
        font = ImageFont.load_default()
        
    return font

def create_text_watermark_layer(settings):
    """Creates a transparent PIL image layer with the text watermark."""
    text = settings.get("text", "")
    if not text:
        return None

    font_family = settings.get("font_family", "SimSun")
    font_size = int(settings.get("font_size", 36))
    font = _get_font(font_family, font_size)

    # Get text size including stroke
    stroke_size = settings.get("stroke_size", 0) if settings.get("stroke", False) else 0
    text_bbox = ImageDraw.Draw(Image.new("RGBA", (1,1))).textbbox((0, 0), text, font=font, stroke_width=stroke_size)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Create a layer just big enough for the text
    layer = Image.new("RGBA", (text_width, text_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(layer)

    x, y = -text_bbox[0], -text_bbox[1]

    # Shadow
    if settings.get("shadow", False):
        shadow_size = settings.get("shadow_size", 2)
        shadow_color = (0, 0, 0, 128)
        draw.text((x + shadow_size, y + shadow_size), text, font=font, fill=shadow_color, stroke_width=stroke_size)

    # Stroke
    if settings.get("stroke", False):
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
        layer = layer.rotate(rotation, expand=True, resample=Image.BICUBIC)

    return layer

def create_image_watermark_layer(watermark_image, settings):
    """Creates a transparent PIL image layer for the image watermark."""
    if not watermark_image:
        return None

    if watermark_image.mode != 'RGBA':
        watermark_image = watermark_image.convert('RGBA')

    # Scaling
    width_scale = settings.get("width_scale", 1.0)
    height_scale = settings.get("height_scale", 1.0)
    if width_scale != 1.0 or height_scale != 1.0:
        orig_width, orig_height = watermark_image.size
        new_width = int(orig_width * width_scale)
        new_height = int(orig_height * height_scale)
        if new_width > 0 and new_height > 0:
            watermark_image = watermark_image.resize((new_width, new_height), Image.LANCZOS)

    # Opacity
    opacity = float(settings.get("opacity", 1.0))
    if opacity < 1.0:
        alpha = watermark_image.getchannel('A')
        alpha = alpha.point(lambda i: int(i * opacity))
        watermark_image.putalpha(alpha)

    # Rotation
    rotation = settings.get("rotation", 0)
    if rotation != 0:
        watermark_image = watermark_image.rotate(rotation, expand=True, resample=Image.BICUBIC)
    
    return watermark_image

def _calculate_position(image_size, watermark_size, position_str, margin=10):
    """Calculates x, y coordinates from a position string."""
    img_w, img_h = image_size
    wm_w, wm_h = watermark_size

    if "Left" in position_str:
        x = margin
    elif "Right" in position_str:
        x = img_w - wm_w - margin
    else: # Center
        x = (img_w - wm_w) // 2
        
    if "Top" in position_str:
        y = margin
    elif "Bottom" in position_str:
        y = img_h - wm_h - margin
    else: # Middle or Center
        y = (img_h - wm_h) // 2
        
    return x, y

def apply_text_watermark(image, settings):
    """Applies a text watermark to a PIL image for final export."""
    if not image:
        return None

    watermark_layer = create_text_watermark_layer(settings)
    if not watermark_layer:
        return image

    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Position
    if "x" in settings and "y" in settings:
        x, y = settings["x"], settings["y"]
    else:
        position = settings.get("position", "Center")
        x, y = _calculate_position(image.size, watermark_layer.size, position)

    # Composite the layer onto the image
    composite_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    composite_layer.paste(watermark_layer, (x, y))
    
    watermarked_image = Image.alpha_composite(image, composite_layer)
    return watermarked_image

def apply_image_watermark(image, watermark_image, settings):
    """Applies an image watermark to a PIL image for final export."""
    if not image or not watermark_image:
        return image

    watermark_layer = create_image_watermark_layer(watermark_image, settings)

    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Position
    if "x" in settings and "y" in settings:
        x, y = settings["x"], settings["y"]
    else:
        position = settings.get("position", "Center")
        x, y = _calculate_position(image.size, watermark_layer.size, position)

    # Composite the layer onto the image
    composite_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    composite_layer.paste(watermark_layer, (x, y), watermark_layer)

    watermarked_image = Image.alpha_composite(image, composite_layer)
    return watermarked_image