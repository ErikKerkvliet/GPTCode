import pyautogui
from pyautogui import Size, Point
from PIL import Image


class Control:
    def __init__(self):
        Size(width=1366, height=768)
        pyautogui.click(250, 50)

        pyautogui.typewrite('https://www.vndb.org')
        # pyautogui.typewrite('https://web.bitpanda.com/home', interval=0.1)
        pyautogui.press('enter')

        pyautogui.click(250, 200)

        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")

        image = Image.open("screenshot.png")

        # Haal de RGB-waarde op van een bepaalde pixel
        x = 100   # x-coördinaat van de pixel op het scherm
        y = 200   # y-coördinaat van de pixel op het scherm

        rgb_value = image.getpixel((x, y))
        pyautogui.position()
        Point(x=750, y=293)
        print(rgb_value)
        pyautogui.moveTo(1000, 700, 4)


if __name__ == '__main__':
    cp = Control()
