import pyautogui
#
# # Continu de huidige positie van de muis weergeven
# while True:
#     x, y = pyautogui.position()
#     print(f"x: {x}, y: {y}")
#


from pynput.mouse import Listener

# Callback function for mouse clicks
def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y})")

# Create and start the listener
with Listener(on_click=on_click) as listener:
    listener.join()
