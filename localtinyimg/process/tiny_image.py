from PIL import Image
import io
import os
import subprocess

def resize_image(image, scale_percent):
    width, height = image.size
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    return image.resize((new_width, new_height), Image.LANCZOS)

def compress_jpg(image_file, quality=75, scale_percent=100):
    img = Image.open(image_file)
    if scale_percent != 100:
        img = resize_image(img, scale_percent)
    img_io = io.BytesIO()
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(img_io, format="JPEG", quality=quality, optimize=True)
    img_io.seek(0)
    return img_io

def compress_png(image_file, scale_percent=100):
    img = Image.open(image_file)
    if scale_percent != 100:
        img = resize_image(img, scale_percent)
    temp_input = "temp_input.png"
    temp_output = "temp_output.png"
    img.save(temp_input, format="PNG", optimize=True)

    subprocess.run(["optipng", "-o2", temp_input, "-out", temp_output], check=True)

    with open(temp_output, "rb") as f:
        compressed_data = f.read()

    os.remove(temp_input)
    os.remove(temp_output)

    return io.BytesIO(compressed_data)