import pyautogui
import time

'''
# ターミナルの座標から、左上に(10, 400)だけドラッグする場合
start_x, start_y = set.x_terminal, set.y_terminal
dx, dy = -10, -400
Mouse_Operation.drag_mouse(start_x, start_y, dx, dy)
'''

def drag_mouse(start_x, start_y, dx, dy, duration=0.5):
    # 指定した座標にマウスを移動して、マウスボタンを押す
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()

    # 指定した分だけドラッグする
    pyautogui.dragRel(dx, dy, duration=duration)

    # マウスボタンを離す
    pyautogui.mouseUp()


