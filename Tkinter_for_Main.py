import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox  # 追加: messageboxのインポート
import os

# 保存するファイルのパス
save_file = "tk_save_text.txt"


# 前回保存された内容を取得
def load_saved_text():
    if os.path.exists(save_file):
        with open(save_file, "r") as file:
            return file.read().strip()
    return ""

# 内容を保存
def save_text():
    # entry1はEntryウィジェットなので、そのままget()を使用
    text1 = entry1.get()

    # entry2はTextウィジェットなので、"1.0"（開始位置）から"end-1c"（終了位置）まで取得
    # text2 = entry2.get("1.0", "end-1c")  # "end-1c"で最後の改行を除外

    # ファイルに保存
    #save_file = "output.txt"  # 保存するファイル名
    with open(save_file, "w") as file:
        file.write(text1 + "\n")
        # file.write("Text2 content: " + text2 + "\n")

    print("内容を保存しました。")

# フォントサイズの設定
def apply_settings():
    new_size = font_size_var.get()
    entry1.config(font=("Arial", new_size))
    settings_window.destroy()  # 設定完了後にサブウィンドウを閉じる

# プロパティボタンの機能 (サブウィンドウを開いて設定変更できるようにする)
def open_properties():
    global settings_window
    settings_window = tk.Toplevel(root)
    settings_window.title("プロパティ設定")

    # サブウィンドウサイズの設定
    settings_window.geometry("600x700")
        
    # フォントサイズ設定
    tk.Label(settings_window, text="フォントサイズ:").pack()

    global font_size_var
    font_size_var = tk.IntVar(value=12)  # 初期値を12に設定
    font_size_entry = ttk.Entry(settings_window, textvariable=font_size_var)
    font_size_entry.pack()

    # 適用ボタン
    apply_button = ttk.Button(settings_window, text="適用", command=apply_settings)
    apply_button.pack()


# メインウィンドウの作成
root = tk.Tk()
root.title("コード生成")

# ウィンドウサイズの設定
root.geometry("700x600")

# ラベル
label = tk.Label(root, text="コード作成場所のフォルダのパス:")
label.pack()

# 前回の内容を表示するラベル
previous_text = load_saved_text()
label1 = tk.Label(root, text=previous_text)
label1.pack()

# 入力欄1：コード作成時のフォルダパスの確認/変更
entry1 = tk.Entry(root, width=80)
entry1.pack(pady=10)

# 入力欄2：プロンプトの入力
label2 = tk.Label(root, text="要求を入力してください:")
label2.pack()
entry2 = tk.Text(root, width=80, height=5)
entry2.pack(pady=10)

# ラベル、作成するプログラム中に使用するパスの指定（任意）
label_file = tk.Label(root, text="\nコード生成時に使用したいファイル/フォルダがある場合、パスを入力してください。") # 相対パスの場合、ファイル名だけでもOK？

label_file.pack()

# 入力欄3：パス1（任意）
label3 = tk.Label(root, text="パス1:")
label3.pack()
entry3 = tk.Text(root, width=80, height=1)
entry3.pack(pady=10)

# 入力欄4：パス2（任意）
label4 = tk.Label(root, text="パス2:")
label4.pack()
entry4 = tk.Text(root, width=80, height=1)
entry4.pack(pady=10)

# 入力欄3：パス3（任意）
label5 = tk.Label(root, text="パス3:")
label5.pack()
entry5 = tk.Text(root, width=80, height=1)
entry5.pack(pady=10)

# フレームを作成してOKボタンを配置する
button_frame1 = tk.Frame(root)
button_frame1.pack(side=tk.BOTTOM, pady=20, anchor=tk.CENTER)  # 中央に配置

# OKボタン
ok_button = tk.Button(button_frame1, text="OK", command=save_text, width=15, height=2)
ok_button.pack(pady=10)  # OKボタンをフレーム内で配置

# プロパティボタンをOKボタンの下に配置する
property_button1 = tk.Button(button_frame1, text="プロパティを開く", command=open_properties)
property_button1.pack(side=tk.TOP, pady=30)



# ウィンドウを開く
root.mainloop()
