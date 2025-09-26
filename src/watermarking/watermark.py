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
    font_family = settings.get("font_family", "SimSun")  # 默认使用宋体
    font_size = int(settings.get("font_size", 36))  # 确保字体大小是整数
    
    # 字体名称到Windows字体文件的映射
    font_name_to_file = {
        "SimSun": "C:\\Windows\\Fonts\\simsun.ttc",      # 宋体
        "Microsoft YaHei": "C:\\Windows\\Fonts\\msyh.ttc",  # 微软雅黑
        "SimHei": "C:\\Windows\\Fonts\\simhei.ttf",      # 黑体
        "KaiTi": "C:\\Windows\\Fonts\\simkai.ttf",       # 楷体
        "FangSong": "C:\\Windows\\Fonts\\simfang.ttf",   # 仿宋
        "NSimSun": "C:\\Windows\\Fonts\\simsun.ttc",     # 新宋体
        "Arial": "C:\\Windows\\Fonts\\arial.ttf"         # Arial
    }
    
    # 备用字体文件列表
    fallback_font_files = [
        "C:\\Windows\\Fonts\\simsun.ttc",    # 宋体
        "C:\\Windows\\Fonts\\msyh.ttc",      # 微软雅黑
        "C:\\Windows\\Fonts\\simhei.ttf",    # 黑体
        "C:\\Windows\\Fonts\\arial.ttf"      # Arial
    ]
    
    # 尝试使用用户选择的字体名称对应的字体文件
    font = None
    if font_family in font_name_to_file:
        try:
            font = ImageFont.truetype(font_name_to_file[font_family], size=font_size)
        except IOError:
            pass
    
    # 如果没有找到对应的字体文件或加载失败，尝试直接使用字体名称
    if font is None:
        try:
            font = ImageFont.truetype(font_family, size=font_size)
        except IOError:
            # 如果直接使用字体名称失败，尝试使用备用字体文件
            for font_file in fallback_font_files:
                try:
                    font = ImageFont.truetype(font_file, size=font_size)
                    break  # 找到可用字体后跳出循环
                except IOError:
                    continue
            
            # 如果所有备用字体文件都失败，使用默认字体
        if font is None:
            font = ImageFont.load_default()

    # Text
    text = settings.get("text", "")
    if not text:
        return image # Return original image if no text
    
    # 确保文本是Unicode编码，处理可能的编码问题
    if not isinstance(text, str):
        try:
            text = str(text, 'utf-8')
        except (TypeError, UnicodeDecodeError):
            try:
                text = str(text)
            except:
                pass

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
        # 修复尺寸不一致：将旋转后的txt_layer居中粘贴到与原图同尺寸的新透明层
        new_txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
        paste_x = (image.width - txt_layer.width) // 2
        paste_y = (image.height - txt_layer.height) // 2
        new_txt_layer.paste(txt_layer, (paste_x, paste_y), txt_layer)
        txt_layer = new_txt_layer

    # Composite the text layer onto the image
    watermarked_image = Image.alpha_composite(image.convert("RGBA"), txt_layer)
    return watermarked_image
