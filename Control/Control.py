import pyautogui
from pyautogui import Size
from PIL import Image
import time
from Trade import Trade


class Control:
    def __init__(self):
        Size(width=1366, height=768)
        time.sleep(1)

        if not self.check_logged_in():
            self.login()

        image = self.make_screenshot()
        if image.getpixel((1245, 181)) == (47, 209, 132):
            pyautogui.click(1223, 191)

        self.trade()

    def trade(self):
        image = self.make_screenshot()

        # Move and click green trade button
        if image.getpixel((787, 192)) == (47, 209, 132):
            pyautogui.moveTo(787, 192, duration=1)
            pyautogui.click(787, 192)

        time.sleep(0.5)

        image = self.make_screenshot()
        # Move and click green buy button
        if image.getpixel((339, 529)) == (47, 209, 132):
            pyautogui.moveTo(339, 529, duration=1)
            pyautogui.click(339, 529)

        image = self.make_screenshot()
        # Move to crypto button and click
        pyautogui.moveTo(406, 350, duration=0.5)
        pyautogui.click(406, 350)

        time.sleep(0.2)

        # Move and click search field
        pyautogui.moveTo(406, 345, duration=0.5)
        pyautogui.click(406, 345)

        pyautogui.typewrite('REEF', interval=0.02)
        pyautogui.press('enter')

        input('Correct')

        # Go to found currency
        pyautogui.moveTo(468, 598, duration=1)
        pyautogui.click(468, 598)

        # Move to currency input and click
        pyautogui.moveTo(452, 565, duration=0.7)
        pyautogui.click(452, 565)

        pyautogui.typewrite('10', interval=0.6)

        # Move to summary
        pyautogui.moveTo(553, 853, duration=0.6)
        pyautogui.click(553, 853)

        time.sleep(1)

        image = self.make_screenshot()
        if image.getpixel((975, 751)) == (176, 176, 176):
            # Move to checkbox 1
            pyautogui.moveTo(975, 751, duration=0.5)
            pyautogui.click(975, 751)

            if image.getpixel((977, 695)) == (176, 176, 176):
                # Move to checkbox 2
                pyautogui.moveTo(977, 695, duration=1.2)
                pyautogui.click(977, 695)
        elif image.getpixel((978, 723)) == (176, 176, 176):
            # Move to single checkbox
            pyautogui.moveTo(976, 723, duration=1.2)
            pyautogui.click(976, 723)

        input('Buy?')
        # Buy
        pyautogui.moveTo(720, 833, duration=0.6)
        pyautogui.click(720, 833)

    def login(self):
        pyautogui.click(200, 120)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('del')

        # pyautogui.typewrite('https://www.vndb.org')
        pyautogui.typewrite('https://web.bitpanda.com/home', interval=0.05)
        pyautogui.press('enter')

        time.sleep(5)

        image = self.make_screenshot()

        # Accept cookie
        if image.getpixel((1183, 999)) == (47, 209, 132):
            pyautogui.click(1183, 999)

        time.sleep(0.5)

        # Is password filled. If so Login
        if image.getpixel((1183, 999)) == (255, 255, 255) and image.getpixel((742, 770)) == (47, 209, 132):
            pyautogui.click(742, 770)

    def check_logged_in(self):
        image = self.make_screenshot()

        logged_id = False
        times = 0
        while not logged_id:
            if times > 3:
                return False
            # Check Bitpanda icon in top left and check green trade button
            if image.getpixel((157, 196)) != (10, 11, 9) or image.getpixel((788, 194)) != (47, 209, 132):
                times += 1
                time.sleep(3)
            else:
                return True

    @staticmethod
    def make_screenshot():
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return Image.open("screenshot.png")


if __name__ == '__main__':
    # cp = Control()
    trade = Trade()
    #      XRP  EUROC ETH PAN SOL ANT
    trade.buy('1INCH', 15)
