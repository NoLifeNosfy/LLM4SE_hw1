# Image Watermark

A command-line tool to add watermarks to images.

## Features

*   Add text watermarks to images in a specified folder.
*   Customize font size, color, and position of the watermark.
*   Outputs watermarked images to a new `_watermark` directory within the original folder.

## Usage

```bash
python src/main.py <folder_path> [options]
```

### Options

*   `--font_size <size>`: Set the font size of the watermark text (default: 40).
*   `--font_color <color>`: Set the font color (e.g., white, black, red; default: white).
*   `--position <position>`: Set the watermark position (e.g., `top-left`, `bottom-right`; default: `bottom-right`).

### Example

```bash
python src/main.py assets --font_size 50 --font_color black --position top-left
```