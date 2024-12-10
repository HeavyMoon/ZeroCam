#!/usr/bin/env python
import SH1106
import time
import datetime
import socket
import re
import ipget
from PIL import Image, ImageDraw, ImageFont
import os

from photo   import photo
from video   import video
from preview import preview_latest

def ps_api(cmd: str) -> str:
    """Communicates with a local API to fetch system information."""
    HOST, PORT = 'localhost', 8423
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.send(cmd.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
    return re.sub(r'.*: (.+)\n', r'\1', response)


def handle_button_press(buttons: dict, key_states: dict, menu_state: dict):
    """Handles button presses and updates menu state."""
    for key, action in buttons.items():
        if disp.RPI.digital_read(key) == 1:
            menu_state["DISPLAY_UPDATE"] = True
            action(menu_state)
            update_menu_state(menu_state)
            break


def update_menu_state(menu_state: dict):
    """Updates the menu position and ID."""
    if menu_state["MENU_ID"] == 0:
        if menu_state["MENU_POS"] < menu_state["MENU_POS_MIN"]:
            menu_state["MENU_POS"] = menu_state["MENU_POS_MAX"]
        elif menu_state["MENU_POS_MAX"] < menu_state["MENU_POS"]:
            menu_state["MENU_POS"] = menu_state["MENU_POS_MIN"]


def key1_action(menu_state: dict):
    """KEY1 button pressed function"""
    if menu_state["MENU_ID"] == 1:
        draw.rectangle((0, 0, disp.width, disp.height), fill=1)
        draw.ellipse((54,32,74,52), outline=0, fill=0)
        disp.ShowImage(disp.getbuffer(image))
        photo()

    if menu_state["MENU_ID"] == 2:
        draw.rectangle((0, 0, disp.width, disp.height), fill=1)
        draw.ellipse((54,32,74,52), outline=0, fill=0)
        disp.ShowImage(disp.getbuffer(image))
        video(5)

    if menu_state["MENU_ID"] == 3:
       preview_latest(disp, 0) 


def key2_action(menu_state: dict):
    """KEY2 button pressed function"""
    if menu_state["MENU_ID"] == 3:
        draw.rectangle((0, 0, disp.width, disp.height), fill=1)
        draw.text((0, 30), "SYNC TIME...", font=font)
        disp.ShowImage(disp.getbuffer(image))

        if 'wlan0' in addr.list:
            ps_api('rtc_web')
        ps_api('rtc_rtc2pi')


def key3_action(menu_state: dict):
    """KEY3 button pressed function"""
    if menu_state["MENU_ID"] == 3:
        if 'wlan0' in addr.list:
            draw.rectangle((0, 0, disp.width, disp.height), fill=1)
            draw.text((0, 30), "UPLOADING...", font=font)
            disp.ShowImage(disp.getbuffer(image))
            os.system(f'{os.path.dirname(__file__)}/upload-data.sh')


# Initialize OLED Display
disp = SH1106.SH1106()
disp.Init()
disp.clear()

# Create a blank image for drawing
image     = Image.new('1', (disp.width, disp.height), 'WHITE')
draw      = ImageDraw.Draw(image)
font      = ImageFont.truetype('Consolas.ttf', 10)

# Initialize menu and display settings
menu_state = {
    "DISPLAY_UPDATE": True,
    "MENU_ID":      0,
    "MENU_POS":     0,
    "MENU_POS_MIN": 0,
    "MENU_POS_MAX": 3,
}

host = socket.gethostname()
addr = ipget.ipget()
prev_time = time.time()

# Button actions
buttons = {
    disp.RPI.GPIO_KEY_UP_PIN:    lambda state: state.update(MENU_POS=state["MENU_POS"] - 1),
    disp.RPI.GPIO_KEY_DOWN_PIN:  lambda state: state.update(MENU_POS=state["MENU_POS"] + 1),
    disp.RPI.GPIO_KEY_LEFT_PIN:  lambda state: state.update(MENU_ID=0),
    disp.RPI.GPIO_KEY_RIGHT_PIN: lambda state: state.update(MENU_ID=state["MENU_POS"] + 1),
    disp.RPI.GPIO_KEY_PRESS_PIN: lambda state: print("Center pressed"),
    disp.RPI.GPIO_KEY1_PIN:      key1_action,
    disp.RPI.GPIO_KEY2_PIN:      key2_action,
    disp.RPI.GPIO_KEY3_PIN:      key3_action,
}

try:
    while True:
        # Handle button presses
        handle_button_press(buttons, disp.RPI, menu_state)

        # Update display every second or when a button is pressed
        if time.time() - prev_time >= 10.0 or menu_state["DISPLAY_UPDATE"]:
            prev_time = time.time()
            menu_state["DISPLAY_UPDATE"] = False

            # Clear screen
            draw.rectangle((0, 0, disp.width, disp.height), fill=1)

            # Header: Date and Time
            ctime = datetime.datetime.now().strftime('%y/%m/%d %H:%M')
            draw.text((0, 0), ctime, font=font)

            # Header: Battery Level
            blevel = str(round(float(ps_api('get battery'))))
            draw.text((110, 0), blevel, font=font)

            # Menu
            if menu_state["MENU_ID"] == 0:
                menu_items = [
                    '  1. PHOTO ',
                    '  2. VIDEO ',
                    '  3. TOOLS',
                    '  4. INFO  ',
                ]
                for i, item in enumerate(menu_items):
                    draw.text((5, 14 + 11 * i), item, font=font)
                draw.text((5, 14 + 11 * menu_state["MENU_POS"]), '>', font=font)

            elif menu_state["MENU_ID"] == 1:
                draw.text((50, 20), "PHOTO", font=font)
                draw.ellipse((54,32,74,52), outline=0, fill=255)

            elif menu_state["MENU_ID"] == 2:
                draw.text((50, 20), "VIDEO", font=font)
                draw.ellipse((54,32,74,52), outline=0, fill=255)
                draw.text((61, 37), "5", font=font)

            elif menu_state["MENU_ID"] == 3:
                draw.text((0, 20), " PREVIEW LATEST", font=font)
                draw.text((0, 30), " SYNC TIME     ", font=font)
                draw.text((0, 40), " UPLOAD DATA   ", font=font)

            elif menu_state["MENU_ID"] == 4:
                addr = ipget.ipget()
                draw.text((0, 20), f'{host}', font=font)
                if 'wlan0' in addr.list:
                    draw.text((0, 40), f'wlan0 {addr.ipaddr("wlan0")}', font=font)

            # Display the image
            disp.ShowImage(disp.getbuffer(image))

        # Sleep to prevent high CPU usage
        time.sleep(0.07)

except IOError as e:
    print(f"IOError: {e}")
    disp.clear()

except KeyboardInterrupt:
    disp.RPI.module_exit()
    print("Exiting program...")
    exit()

