import datetime
import os
import time
from pathlib import Path

from screenshot import screenshot_window_check

p = Path("F:/NIKKE/AppData-LocalLow-Unity/com_proximabeta_NIKKE")


def in_use():
    for i in range(3):
        found = screenshot_window_check("NIKKE")
        if not found:
            log("file is downloading")
            return True
        else:
            log("file isn't downloading. Trying again in 10 seconds...")
            time.sleep(10)
    log("file isn't downloading after 3 attempts. Shutting down pc...")

    os.system("shutdown /s /t 300")
    return False


def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"{msg} - {now}"
    print(msg)
    with open("nikke_log.txt", "a") as f:
        f.write(f"{msg}\n")


while True:
    if not in_use():
        break
    time.sleep(60)
