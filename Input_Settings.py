import pyperclip
import pyautogui
import time
import Settings as set
import Execute_Base as eb


# 文章に含まれる改行を削除する
def remove_newlines(text):
    return text.replace('\n', ' ').replace('\r', ' ')


# 文字列内に使えない文字（全角文字）が含まれていないかどうかをチェックする
def find_unsupported_chars(text):
    unsupported_chars = []
    for char in text:
        # 半角文字以外の場合
        if ord(char) > 256:
            unsupported_chars.append(char)
    # 半角文字以外が見つかった場合は、そのリストを返す
    if unsupported_chars:
        return unsupported_chars
    # 全て半角文字の場合は、Noneを返す
    else:
        return None


# 入力先の画面が半角入力以外の場合、半角入力に切り替える
def check_and_switch_to_english_input(test_string='test strings', type_interval=0.01):
    pyautogui.PAUSE = set.pause  # キー入力の間隔を設定
    
    # コードを書く部分をリセットする
    eb.reset()
    
    # 適当な確認用文字列を入力
    pyautogui.click(set.x_blanc_space, set.y_blanc_space)
    pyautogui.typewrite(test_string, type_interval)
    pyautogui.hotkey('enter')
    
    # 入力済み文字を全選択でコピー
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    
    # クリップボードの内容を取得
    copied_text = pyperclip.paste()
    
    # 全角文字が含まれているかをチェック
    unsupported_chars = find_unsupported_chars(copied_text)
    if unsupported_chars is not None:
        # 日本語キーボードの場合、「半角/全角(漢字)」キーを押して英字入力に切り替える
        pyautogui.click(set.x_terminal, set.y_terminal)
        pyautogui.press('kanji')
        print(f"全角入力から半角入力に切り替えました。")


