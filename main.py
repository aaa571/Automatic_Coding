import Execute
import keyboard
import Settings as set
import Input_Settings
import re
import Execute_Base as eb
import subprocess
import os
import tkinter as tk
import time
import signal
import threading

# バッチファイルの絶対パス
batch_file_path = os.path.join(set.program_path, "main.bat")

def exit_program():
    print("! ESCキーが押されたため、プログラムを終了します。 !\n")
    #Execute.tk_window(display_text="終了しました")
    # バッチファイルを再起動
    restart_batch(batch_file_path)
    # プログラムを終了する
    os._exit(0)

# Ctrl+Cを無視する関数
def ignore_signal(signum, frame):
    print(f"Ignored signal: {signum}")


# 以前のサブプロセスを格納する変数
previous_process = None

def restart_batch(batch_file):
    global previous_process

    # 以前のプロセスがあれば終了する
    if previous_process and previous_process.poll() is None:  # プロセスが生きている場合
        print(f"以前のプロセスを終了します (PID: {previous_process.pid})。")
        previous_process.terminate()  # SIGTERMで終了
        try:
            previous_process.wait(timeout=5)  # 終了を待つ
        except subprocess.TimeoutExpired:
            print("強制終了します。")
            previous_process.kill()  # 強制終了

    # 新しいプロセスを開始
    print(f"バッチファイルを再起動します。")#: {batch_file}")
    previous_process = subprocess.Popen(["cmd.exe", "/c", batch_file])

'''
# グローバル変数で経過時間を記録
elapsed_time = 0
stop_timer = False  # タイマーを終了するためのフラグ

# バックグラウンドで時間を計測する関数
def timer_function():
    global elapsed_time, stop_timer
    while not stop_timer:
        time.sleep(1)
        elapsed_time += 1
'''

        
def main():
    i = 0  # 試行回数 (trial 1, 2, 3, ...)
    a = 9  # 終了の仕方を変えるための変数。初期値は適当な値
    
    '''
    # グローバル変数を使用するための宣言
    global stop_timer, elapsed_time
    # タイマーをスレッドで開始
    timer_thread = threading.Thread(target=timer_function)
    timer_thread.start()
    '''
    
    # キーボードのイベントを監視し、エスケープキーが押されたらプログラムを終了(し、再起動する)
    keyboard.add_hotkey('esc',exit_program)
    
    # 現在のハンドラを保存
    original_handler = signal.getsignal(signal.SIGINT)
    
    # 念のため、元のハンドラに戻す(初期化)
    #signal.signal(signal.SIGINT, original_handler)
    
    # プロパティの設定
    while True:
        key_1 = input("\n---------------------\n\nプロパティ設定->c, 変更しない->Enter： ")
        if key_1 == "c":
            # 念のため、元のハンドラに戻す(初期化)
            signal.signal(signal.SIGINT, original_handler)
            
            # プロパティの設定
            # Settings.pyの絶対パス
            settings_path = os.path.join(set.program_path, "Settings.py")
            
            print("\nプロパティを変更し終えたら、Ctrl+Sを押してください。")
            time.sleep(1)
            
            # SIGINT (Ctrl+C) を無視する
            signal.signal(signal.SIGINT, ignore_signal)
            
            # Settings.pyをデフォルトのエディタで開く
            subprocess.Popen(['start', settings_path], shell=True)
            
            # Ctrl+Sが押されたら、プログラムを再起動する
            #keyboard.wait('ctrl+s')
            while True:
                if keyboard.is_pressed('ctrl+s'):
                    print("Ctrl+S が押されました。")
                    break
            # Ctrl+Sが押されたら、元のハンドラに戻す(再起動すれば元のハンドラに戻るはずだが、念のため)
            signal.signal(signal.SIGINT, original_handler)
            
            # バッチファイルの再起動
            print("\nプロパティが変更されました。")#\nバッチファイルを再起動します。\n")
            #subprocess.run(["cmd", "/c", batch_file_path], shell=True)
            restart_batch(batch_file_path)
            os._exit(0)
            break
        
        # Enterが押された場合、次の処理に進む    
        elif key_1 == "":
            '''
            # タイマーが20秒を超えた場合、バッチファイルを再起動する
            if elapsed_time > 20:
                # タイマーを停止
                stop_timer = True
                timer_thread.join()  # スレッドが終了するまで待機
                print("\n時間経過のため、")
                restart_batch(batch_file_path)
                os._exit(0)
            '''
            break
        
        print("無効な入力です。")
    

    # 追加
    print("\n\nコード生成先のディレクトリ：", set.folder_path)
    
    # 他のキーが押された場合、もう一度聞くようにする
    while True:
        key = input("\nパス変更->c, 変更しない->Enter： ")
        #("\nパスに変更がなければEnterを押すと開始します。変更する場合はCを入力してください：")
        
        # Settings.pyの絶対パス
        set_path = set.program_path + r"\Settings.py"
        set_path = set_path.replace('\\', '/')
        
        if key == "c":
            while True:
                folder_path = input("コード生成先ファイルがあるディレクトリの絶対パスを入力してください： ")
                # 入力が「大文字のアルファベット + :」で始まるかチェック
                if len(folder_path) > 1 and folder_path[0].isupper() and folder_path[1] == ":":
                    print(f"folder path: {folder_path}")
                    break
                else:
                    print('\n' + r"正しいパスを入力してください (例, C:\User or D:\User)")
            
            # folder_pathに'、または、"が含まれていない場合、最初と最後に"を追加する
            if not (folder_path.startswith('"') and folder_path.endswith('"')) and not (folder_path.startswith("'") and folder_path.endswith("'")):
                folder_path = f'"{folder_path}"'
            
            # フォルダーパスをバックスラッシュとロウ文字にする
            folder_path = folder_path.replace("/", "\\")
            folder_path = f'r{folder_path}'  # rを追加
                
            # ファイル全体を文字列として読み込む
            with open(set_path, "r", encoding="utf-8") as file:
                content = file.read()

            # 正規表現でフォルダーパスを含む行を新しい行に置き換える
            pattern = r".*folder.*\n"  # "folder" を含む行全体をマッチさせる正規表現
            replacement = r"folder = " + re.escape(folder_path) + "\n"  # folderパスの更新（改行を追加）

            # 1つ目のマッチした行だけを、re.subを使って置き換え (複数行の置き換え防止)
            updated_content = re.sub(pattern, replacement, content, count=1)

            # 変更後の内容をファイルに書き戻す
            with open(set_path, "w", encoding="utf-8") as file:
                file.write(updated_content)
            
            # バッチファイルの再起動
            print("\nパスが変更されました。")#\nバッチファイルを再起動します。\n")
            #subprocess.run(["cmd", "/c", batch_file_path], shell=True)
            restart_batch(batch_file_path)
            os._exit(0)
            break
        
        # Enterが押された場合、次の処理に進む        
        elif key == "":
            break
            
        print("無効な入力です。")



    # ! 分かりやすくfirst_requestとしているが、他のファイルでは、questionとして扱っている !
    while True:  # 要求が入力されるまで繰り返す
        first_request = input("\n\n要求を入力してください： ")  # 最初の要求文、これを基準の問題文とし、新しいプロンプトの中に組み込んで(new_)requestとする
        if first_request != "":
            break
        
    request = first_request  # 最初は、first_requestと同じ（エラーが出ると、request(要求)の内容が更新される）
    
    
    # 英語(半角)入力以外の場合、英語入力に切り替える
    Input_Settings.check_and_switch_to_english_input()
    

    while True:
        i+=1  # 試行回数 (trial 1, 2, 3, ...)
        
        
        # 追記モードでtxtファイルに書き込む
        # テスト用_記録、プロンプトを記録
        #with open(f"{set.output_path}/screen_rate_{set.screen_rate}/{set.error_name}/{set.num}_prompt.txt", mode='a', encoding='utf-8') as text_file:
        #    text_file.write(f"\n-------------\ntrial: {i}, prompt: {request}\n")
        #import Settings_for_Test as set_t
        #with open(f"{set_t.output_path}/trial&prompt_{set_t.j}.txt", mode='a', encoding='utf-8') as text_file:
        #     text_file.write(f"\n-------------\ntrial: {i}, prompt: {request}\n")
        
        print(f"\ntrial {i}:")
        # 要求文
        first_request, request, i = Execute.create_and_fix(first_request, request, i)
        
        # 処理を抜ける、ここをテスト用に追加
        if request == None:
            # 終了の仕方(Tkinterが開くかどうか)を変えるために場合分けする
            # 正常終了
            if first_request == 0:   # first_request は、他のファイルでは question として扱っているため注意
                a = 0
                break
            # 異常終了
            elif first_request == 1:
                a = 1
                break
            # プログラムにエラーが起こった場合
            else :
                a = 2
                break
            
    if a == 0:
        return 'done'
    elif a == 1:
        return 'not done'
    else:
        return 'error'



#if __name__ == "__main__":
#main()
def cycle():
    while True:
        main_text = main()

        if main_text == 'done':
            Execute.tk_window(display_text="生成終了")
        elif main_text == 'not done':
            Execute.tk_window(display_text="問題が発生しました")
        elif main_text == 'error':
            print("プログラムにエラーが発生しました")
            Execute.tk_window(display_text="プログラム側にエラーが発生しました")

cycle()
    