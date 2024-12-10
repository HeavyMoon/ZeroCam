import SH1106
import config
import os
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def get_latest_jpg_file(directory):
    """
    Retrieve the latest file with a .jpg extension from the specified directory.
    """
    try:
        jpg_files = [
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith('.jpg')
        ]
        if not jpg_files:
            return None  # No .jpg files found
        
        latest_jpg_file = max(jpg_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        return latest_jpg_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_to_grayscale_and_resize(file_path, size=(128, 64)):
    """
    Convert a JPEG file to grayscale and resize it to the specified dimensions.
    
    :param file_path: Path to the target JPEG file
    :param size: The size (width, height) to resize the image to
    :return: The grayscale and resized image object
    """
    try:
        with Image.open(file_path) as img:
            # Convert to grayscale
            grayscale = img.convert("L")  # Grayscale (L mode)
            # Resize to the specified dimensions
            #resized = grayscale.resize(size, Image.ANTIALIAS)
            resized = grayscale.resize(size, Image.Resampling.LANCZOS)
            return resized
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_to_binary(file_path, size=(128, 64), threshold=128):
    """
    Convert a JPEG file to a binary (black and white) image.
    
    :param file_path: Path to the target JPEG file
    :param size: The size (width, height) to resize the image to
    :param threshold: The threshold for binarization (0-255)
    :return: The binary image object
    """
    try:
        with Image.open(file_path) as img:
            # Convert to grayscale
            grayscale = img.convert("L")  # Grayscale (L mode)
            # Resize to the specified dimensions
            resized = grayscale.resize(size, Image.Resampling.LANCZOS)
            resized = resized.filter(ImageFilter.FIND_EDGES)
            # Apply binary thresholding
            #binary = resized.point(lambda x: 255 if x > threshold else 0, "1")
            binary = resized.point(lambda x: 0 if x > threshold else 255, "1")

            return binary
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def handle_button_press(buttons: dict, rpi: config.RaspberryPi, opt: dict):
    """Handles button presses and updates menu state."""
    for key, action in buttons.items():
        if rpi.digital_read(key) == 1:
            opt['update'] = True
            action(opt)
            break


def preview_latest(disp: SH1106, th: int):
    font  = ImageFont.truetype('Consolas.ttf', 10)

    buttons = {
        disp.RPI.GPIO_KEY_UP_PIN:    lambda opt: opt.update(th=min(opt['th'] + 10, 255)),
        disp.RPI.GPIO_KEY_DOWN_PIN:  lambda opt: opt.update(th=max(opt['th'] - 10, 0)),
        disp.RPI.GPIO_KEY_LEFT_PIN:  lambda opt: opt.update(loop=False),
    }
    
    preview_opt = {
        'th':     th,
        'update': True,
        'loop':   True,
    }
    
    directory_path = f'{os.path.dirname(__file__)}/photo'
    latest_jpg_file = get_latest_jpg_file(directory_path)
    
    if latest_jpg_file:
        file_path = os.path.join(directory_path, latest_jpg_file)
    
        while preview_opt['loop']:
            handle_button_press(buttons, disp.RPI, preview_opt)
            if preview_opt['update']: 
                preview_opt['update'] = False
                #resized_image = convert_to_grayscale_and_resize(file_path)
                resized_image = convert_to_binary(file_path, threshold=preview_opt['th'])
                draw = ImageDraw.Draw(resized_image)
                draw.text((0,0), f"{preview_opt['th']}",font=font)
                disp.ShowImage(disp.getbuffer(resized_image))

            time.sleep(0.2)
    else:
        print("No .jpg files found in the specified directory.")
    

if __name__ == "__main__":
    disp = SH1106.SH1106()
    disp.Init()
    disp.clear()
    preview_latest(disp, 0)
