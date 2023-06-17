import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import datetime


def screenshot_window(window_name):
    hwnd = win32gui.FindWindowEx(None, None, "UnityWndClass", window_name)
    print(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    print(class_name)  
    
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
    print(result)

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
        im.save(f"screenshots/{filename}")
