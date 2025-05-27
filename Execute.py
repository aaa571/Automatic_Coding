import os
import Settings as set
import Execute_Base as eb
import time
import pyautogui
import sys


# main.pyで使う
def create_and_fix(question, request, i): #, generated_code):  # <- 生成テスト用_記録 generated_code
    eb.reset_all()
    eb.call_copilot(request)
    exe = eb.execute()
    # テスト用_e_1
    if exe == 'exit main':  # 「同意する」ボタンが見つからなかった時
        new_request = None
        question = 1  # 1 = 異常終了のための返り値(正常終了なら 0)
        return question, new_request, i
    
    eb.input_cml()

    # 実行が終わったか判定する(終わっていなければCtrl+Cで中断する)　→　エラー判定に移る　→　エラーがあれば、新しい要求を作成する
    eb.execution_completion(timeout = set.execution_timeout)
    time.sleep(set.execution_interval)
    
    
    # 生成されたコードの記録
    import pyperclip
    pyautogui.click(set.x_blanc_space, set.y_blanc_space)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    generated_code = pyperclip.paste()  # 生成されたコードを取得
    
    # テスト用_記録
    #with open(f"{set.output_path}/screen_rate_{set.screen_rate}/{set.error_name}/{set.num}_codes.txt", mode='a', encoding='utf-8') as text_file:
    #    text_file.write(f"\n-------------\ngenerated_code_{i}: \n{generated_code}\n")
    
    
    # エラー文を取得
    error_text = eb.error_check()
        
    # テスト用_e_1
    if error_text == 'exit main':
        new_request = None
        question = 0  # 0 = 正常終了のための返り値(異常終了なら 1)
        return question, new_request, i  #, generated_code  # <- 生成テスト用_記録 generated_code
        
    # エラーの種類によって処理を分ける
    error_type = eb.kind_of_error(error_text)
        #env_error = eb.if_enviromental_errors(error_text, error_type, question)
        
        # テスト用_e_1
        #if env_error == 'exit main':
        #    new_request = None
        #    question = 1  # 1 = 異常終了のための返り値(正常終了なら 0)
        #    return question, new_request, i
    
    # 変数の初期化
    fixed_result = None
    
    # 複数のモジュールが見つからない場合があるため、ループで試行する
    while error_type =='ModuleNotFoundError':
        i+=1  # カウンタ
        print(f"\ntrial {i}:")
        # モジュールインストールを試す
        fixed_result = eb.fix_module_not_found_error(error_text)
        
        # インストールが終わらなかった場合、異常終了するための処理に移る
        # テスト用_e_1
        if fixed_result == 'exit main':
            print('インストールに失敗しました。パッケージ/モジュール名が間違っていたか、インストールにかかる時間が長すぎたようです。')
            new_request = None
            question = 1  # 1 = 異常終了のための返り値(正常終了なら 0)
            return question, new_request, i
            
        eb.reset_terminal()  # ターミナルリセット
        error_text = eb.execute_fixed_enviromental_error()  # 再度実行し、エラー文を取得
            
        # エラーがない場合、正常終了するための処理に移る
        # テスト用_e_1
        if error_text == 'exit main':
            new_request = None
            question = 0  # 0 = 正常終了のための返り値(異常終了なら 1)
            return question, new_request, i
            
        # 再度取得したエラー文内の、エラーの種類を取得
        error_type = eb.kind_of_error(error_text)
        # エラーの種類がimport_errorならループが続く
        #env_error = eb.if_enviromental_errors(error_text, error_type, question)


    
    # 複数のファイルが見つからない場合があるため、ループで試行する
    while error_type =='FileNotFoundError':
        i+=1  # カウンタ
        print(f"\ntrial {i}:")
        # モジュールインストールを試す
        fixed_result = eb.fix_file_not_found_error(question, error_text)
        
        # ファイルが見つからなければ、異常終了するための処理に移る
        # テスト用_e_1
        if fixed_result == 'exit main':
            new_request = None
            question = 1  # 1 = 異常終了のための返り値(正常終了なら 0)
            return question, new_request, i
        
        # ファイルパスが見つかった場合、コード内に含まれるファイル名を直接、パスに変更して、コピペし、再度実行する
        # また、ファイルパスを追加した新たな要求文に更新する
        filename = fixed_result[0]
        file_path = fixed_result[1]
        question = fixed_result[2]  # プロンプトにファイルパスを追加したものに更新
        # 生成されたコード内のファイル名（相対パス）を絶対パスに置き換える
        generated_code = generated_code.replace(filename, file_path)
        
        # テスト用_記録
        #with open(f"{set.output_path}/screen_rate_{set.screen_rate}/{set.error_name}/{set.num}_codes.txt", mode='a', encoding='utf-8') as text_file:
        #    text_file.write(f"\n-------------\ngenerated_code_{i}: \n{generated_code}\n")

        
        pyperclip.copy(generated_code)
        pyautogui.click(set.x_blanc_space, set.y_blanc_space)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'v')
        
        eb.reset_terminal()  # ターミナルリセット
        error_text = eb.execute_fixed_enviromental_error()  # 再度実行し、エラー文を取得
            
        # エラーがない場合、正常終了するための処理に移る
        # テスト用_e_1
        if error_text == 'exit main':
            new_request = None
            question = 0  # 0 = 正常終了のための返り値(異常終了なら 1)
            return question, new_request, i
            
        # 再度取得したエラー文内の、エラーの種類を取得
        error_type = eb.kind_of_error(error_text)
        # エラーの種類が 'FileNotFoundError' ならループが続く
        
            
    # エラーの種類がUnicodeDecodeErrorの場合、エンコードを修正するように促す
    if error_type == 'UnicodeDecodeError':
        print('! ファイルのエンコーディングを直してください。 !')
        # テスト用_e_1
        new_request = None
        question = 1  # 1 = 異常終了のための返り値(正常終了なら 0)
        return question, new_request, i
                   
    # 異常がなく、上記以外のエラーならば、新たな要求文を返す
    new_request = eb.create_new_request(error_text, question, generated_code)
    return question, new_request, i  #, generated_code  # <- テスト用_記録 generated_code


# main.pyで使う
# ESCキーでプログラムを終了するための関数
def exit_program():
    print("! ESCキーが押されたため、プログラムを終了します。 !\n")
    tk_window(display_text="終了しました")
    os._exit(0)


    

# コード生成終了時に、生成終了のウィンドウを表示する関数
# EnterキーまたはSpaceキーを押すとウィンドウが閉じる
import tkinter as tk
def tk_window(display_text):
    
    # 表示するテキストが長い場合、改行する
    if 5 < len(display_text) < 12:
        display_text = display_text[:5] + "\n" + display_text[5:]
    elif 12 < len(display_text):
        display_text = display_text[:6] + "\n" + display_text[6:12] + "\n" + display_text[12:]
    
    # ウィンドウを閉じる関数（イベントを引数として受け取る）
    def close_window(event):
        root.destroy()
        #exit_program2()
        
    # ウィンドウを作成
    root = tk.Tk()
    root.title("コード生成")
    root.lift()  # 新しいウィンドウを一番前面に持ってくる
    
    # ウィンドウのサイズを設定
    root.geometry("500x400")

    # ラベルを作成してウィンドウに追加
    label = tk.Label(root, text=display_text, font=("MS Gosic", 40))
    label.pack(expand=True)
    
    # ウィンドウを常に前面に表示する設定
    root.attributes("-topmost", True)
    
    # ラベルの追加
    label = tk.Label(root, text="Enter/Spaceでウィンドウを閉じます")
    label.pack(pady=80)
    
    # Tkinterウィンドウの位置を取得
    x = root.winfo_rootx() + root.winfo_width() // 2
    y = root.winfo_rooty() + root.winfo_height() // 2

    # 少し待ってからウィンドウをクリック(Enter/Spaseキーで閉じるため、ウィンドウをアクティブにする)
    time.sleep(set.check_interval)
    pyautogui.click(x, y)
    
    # EnterキーまたはSpaceキーを押したときにclose_windowを呼び出して、ウィンドウを閉じる
    root.bind('<Return>', close_window)  # Enterキー
    root.bind('<space>', close_window)   # Spaceキー

    # ウィンドウのメインループを開始
    root.mainloop()
    
