# PCの画面サイズを取得し、マウスカーソルの座標を表示するプログラムです。
# このプログラムを使用したら、Tkinterウィンドウを閉じてください。
# 開いたままだと他のプログラムを実行できません。

import tkinter as tk

# 解像度と拡大率は、PCのディスプレイ設定を確認してください。
# 画面解像度1920x1080の場合
screen_width = 1920
screen_height = 1080
# Windowsの画面拡大率を設定して下さい。
scale_factor = 1.25  # 画面拡大率125%の場合


def get_window_position():
    root.update_idletasks()  # ウィンドウの情報を更新
    x = root.winfo_rootx()  # ウィンドウの左上隅のx座標（フレームを含む）
    y = root.winfo_rooty()  # ウィンドウの左上隅のy座標（フレームを含む）
    return x, y

def update_coordinates(event, screen_width, screen_height, scale_factor):
    # 現在のウィンドウの位置を取得
    window_x, window_y = get_window_position()

    # ウィンドウ内での座標を画面全体での座標に変換
    screen_x = window_x + event.x
    screen_y = window_y + event.y

    # 実際の座標にスケーリング係数を適用
    actual_x = int(screen_x * scale_factor)
    actual_y = int(screen_y * scale_factor)

    # 座標を表示
    label.config(text=f"X: {actual_x}, Y: {actual_y}\n"
                      f"Screen Width: {screen_width}, Screen Height: {screen_height}")

def on_motion(event):
    update_coordinates(event, screen_width, screen_height, scale_factor)

root = tk.Tk()

# ウィンドウを250x50ピクセルで開く
root.geometry("250x50")

# ラベルを作成して配置
label = tk.Label(root, text="")
label.pack(padx=10, pady=10)

# マウスの動きを監視
root.bind("<Motion>", on_motion)

root.mainloop()
