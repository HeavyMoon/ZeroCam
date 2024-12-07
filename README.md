# ZeroCam
## 13890 128x64 1.3inch OLED DISPLAY HAT
I couldn't change the interface from SPI to i2c...

## PiCamera2
Note: Picamera2 does not support rotating images in 90 degree increments.

## PiSugar2
### REST API SAMPLE
```python
import socket

def ps_api(cmd: str) -> str:
    HOST, PORT = 'localhost', 8423
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.send(cmd.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
    return response

ps_api('get battery')
```

Note: Pressing the PiSugar physical button will cause the REST API to return a bug that add prefix 'single'.

## systemd
```
[Unit]
Description=PiZeroCamera
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/work_dir
ExecStart=sudo --user=${YourName} ${/path/to/work_dir}/venv/bin/python ${/path/to/work_dir}/main.py
User=${YourName}
Group=${YourGoup}
Restart=always

[Install]
WantedBy=multi-user.target
```

## REFERENCES
- [PiSugar](https://www.pisugar.com/)
- [PiSugar - GitHub](https://github.com/PiSugar/PiSugar)
- [PiSugar - GitHub - REST API](https://github.com/PiSugar/pisugar-power-manager-rs#unix-domain-socket--webscoket--tcp)
- [13890 128x64, 1.3inch OLED display HAT for Raspberry Pi](https://www.waveshare.com/1.3inch-oled-hat.htm)
- [1.3inch OLED HAT](https://www.waveshare.com/wiki/1.3inch_OLED_HAT)
- [PiCamera2 Manual](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [RaspberryPi Documentation - Camera](https://www.raspberrypi.com/documentation/accessories/camera.html)
