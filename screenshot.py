import datetime
from ctypes import windll
from pathlib import Path

import pyautogui
import win32gui
import win32ui
from PIL import Image

from feature_match import find_match


def screenshot(window_name):
    hwnd = win32gui.FindWindowEx(None, None, "UnityWndClass", window_name)
    print(f"Window ID: {hwnd}", end=", ")
    class_name = win32gui.GetClassName(hwnd)
    print(f"Class name: {class_name}", end=", ")

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
    print(f"PrintWindow result: {result}")

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1
    )

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        return im


def screenshot_window_check(window_name):
    hwnd = win32gui.FindWindowEx(None, None, "UnityWndClass", window_name)
    print(f"Window ID: {hwnd}", end=", ")
    class_name = win32gui.GetClassName(hwnd)
    print(f"Class name: {class_name}", end=", ")

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
    print(f"PrintWindow result: {result}")

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1
    )

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        # PrintWindow Succeeded

        now = datetime.datetime.now()

        # format the date and time as a string
        date_string = now.strftime("%Y-%m-%d_%H-%M-%S")

        filename = f"shot_{date_string}.png"
        full_path = f"screenshots/{filename}"
        Path("screenshots").mkdir(exist_ok=True)
        im.save(full_path)
        try:
            coords = pyautogui.locate("login_screen.png", full_path, confidence=0.9)
            print(f"Coords if found: {coords}")
            return find_match(full_path)
        except pyautogui.ImageNotFoundException:
            return False
