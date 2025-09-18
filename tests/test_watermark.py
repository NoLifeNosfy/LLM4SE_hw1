import os
import sys
from PIL import Image

# Add src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import add_watermark

def test_add_watermark():
    # Create a dummy image
    assets_dir = os.path.join(os.path.dirname(__file__), '../assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    test_image_path = os.path.join(assets_dir, "test_image.png")
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save(test_image_path)

    # Define output path
    output_dir = os.path.join(assets_dir, "_watermark")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, "test_image_watermarked.png")

    # Run the watermark function
    add_watermark(test_image_path, "test", output_path)

    # Check if the output file exists
    assert os.path.exists(output_path)

    # Check if the output file is a valid image
    try:
        with Image.open(output_path) as out_img:
            assert out_img.format.lower() in ['png', 'jpeg']
    except IOError:
        assert False, "Output file is not a valid image"

    # Clean up
    os.remove(test_image_path)
    os.remove(output_path)
