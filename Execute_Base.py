import pyautogui
import time
import pyperclip
import sys
import Search_Img
import Mouse_Operation
import Settings as set
import re
import Error_Fix

pyautogui.PAUSE = set.pause # キー入力の間隔を設定

# ターミナルをリセットする
def reset_terminal():
    
    pyautogui.click(set.x_terminal, set.y_terminal)
    pyautogui.press('enter') # ターミナルをクリアしても、1行前の結果が残ってしまうので、Enterを押し1行前のコマンドを残さないようにする
    pyautogui.typewrite('cls', interval=0.01)
    pyautogui.press('enter')

# コードを書く部分をリセットする
def reset():
    
    # 適当なスペースをクリック
    pyautogui.click(set.x_blanc_space, set.y_blanc_space)
    
    # 全消去
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    
def reset_all():
    # コードを書く部分とターミナルの両方をリセット
    reset()
    reset_terminal()
    
def call_copilot(request):
    # クリップボードに要求をコピー
    pyperclip.copy(request)
    
    # Ctrl+I コマンドを送信
    pyautogui.click(set.x_blanc_space, set.y_blanc_space)
    pyautogui.hotkey('ctrl', 'i')

    # 要求入力 (requestをCopilotにコピペする)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    
def execute():
    # 「同意する」ボタン、あるいは、「なしで再実行」（「チャットで表示」と表示された場合）が表示されたらすぐにクリックする
    img = Search_Img.wait_and_click_2(set.agreement_button, set.re_execute_button, set.re_execute_button_2, set.agreement_timeout)
    
    # 追加
    # 「なしで再実行」を押した後、再び生成を行い「同意ボタン/なしで再実行」が表示されるため、再度クリックする
    # whileの中で、「同意ボタン」あるいは「なしで再実行」を押す
    # 「同意ボタン」ならブレイクして正常に移行
    if img == 're_execute':
        k = 0
        while k < 3:
            img = Search_Img.wait_and_click_2(set.agreement_button, set.re_execute_button, set.re_execute_button_2, set.agreement_timeout)
            if img == 're_execute':
                k += 1
            else:
                break
            # 「なしで再実行」をカウントして3回になったらブレイクして異常終了
            if k == 2:
                img = 'exit main'
                break
            
    # 「同意する」ボタンが見つからない or 「なしで再実行」が3回以上表示された場合        
    if img == 'exit main':
        return 'exit main'

    # 保存
    pyautogui.hotkey('ctrl', 's')

    # 実行
    pyautogui.click(set.x_execute, set.y_execute)
    time.sleep(set.execution_interval)

    return
    

# 実行後、input()があれば、入力を行う
def input_cml():
    input = r'.*input\(.*\).*'
    #int_input = r'.*int\(input\(.*\)\).*'
    #float_input = r'.*float\(input\(.*\)\).*'
    #complex_input = r'.*complex\(input\(.*\)\).*'
    
    # 生成されたコードをコピー
    pyautogui.click(set.x_blanc_space, set.y_blanc_space)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    # クリップボードのコード文を取得
    code = pyperclip.paste()
    
    # コードを取得→input()が含まれているか判定→含まれていれば、入力を行う→Enterを押す
    # 改行も含む文字列を検索するため、re.DOTALLを指定
    while re.match(input, code, re.DOTALL):
        #print(f'code: {code}')
        # input()がある場所を検索
        # 正規表現パターンをコンパイル
        compiled_pattern = re.compile(input)
        match = compiled_pattern.search(code)
        
        # (文字型でも数型でも'1'を入力するように変更した)
        if re.match(input, code, re.DOTALL):
            pyautogui.click(set.x_terminal, set.y_terminal)
            pyautogui.typewrite('1', interval=0.01)
            print('input()が含まれたため、1を入力しました。')
            
        pyautogui.press('enter')
        
        # 見つけたinput()部分までをcodeから消去する
        # 一致部分の開始位置を取得
        end_index = match.end()
        # 一致部分の直後からの文字列を取得
        code = code[end_index:]
        #print('code:')
        #print(code)
    

# 実行が終わったか判定する
def execution_completion_check(timeout):
    #print('timeout: ' + str(timeout))
    pyautogui.click(set.x_terminal, set.y_terminal)
    # 1回Enterを押して、確実に一番最後の行に移動する
    # pyautogui.press('enter')
    # pyautogui.press('enter')  # 追加
    # ターミナル内の'PS [folder_path]'を検索
    pyperclip.copy('PS ' + set.folder_path)
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.hotkey('ctrl', 'v')
    
    # 実行完了 + Enterキー2回ならば、検索結果が4件になる（※reset()で全消去しているが、前の1文が残っている場合があるため5件でも判定する）
    # (2件や3件では誤判定の恐れがあるため、4件以上で判定する)
    pyautogui.click(set.x_terminal, set.y_terminal)
    pyautogui.press('enter')
    pyautogui.press('enter')
    # 検索結果が4件 or 5件ならば、実行完了と判定
    if Search_Img.search_and_wait(set.four_match_found, set.five_match_found, timeout)==True:
        return True
    
    # 実行が終わらない時、実行を中断する（中断するまでの時間は、Settings.pyで設定可能）
    elif Search_Img.search_and_wait(set.four_match_found, set.five_match_found, timeout)==False:
        return False

# 実行完了か判定した後の処理。完了していなければ、Ctrl+Cで実行を中断する        
def execution_completion(timeout):
    # 完了しているため、何もしない
    execution_result = execution_completion_check(timeout)
    if execution_result==True:
        return
    # 完了していないため、Ctrl+Cで実行を中断する
    elif execution_result==False: 
        print('実行を中断します...')
        pyautogui.click(set.x_terminal, set.y_terminal)
        pyautogui.hotkey('ctrl', 'c')  # 実行を中断し、エラー処理に移る
        print('Ctrl+C が押されました.')
        return
    
# エラー判定　→　エラーがあればバグ取得　→　バグ修正
def error_check():
    # ターミナル内の文字列をコピー
    pyautogui.click(set.x_terminal, set.y_terminal)
    # ターミナルの座標から、左上に(10, 400)だけドラッグする
    start_x, start_y = set.x_terminal, set.y_terminal
    dx, dy = -10, -400
    Mouse_Operation.drag_mouse(start_x, start_y, dx, dy)
    pyautogui.hotkey('ctrl', 'c')

    # クリップボードのエラー文を取得
    terminal_text = pyperclip.paste()
    
    # テスト用_記録
    # import Settings_for_Test as set_t
    #with open(f"{set.output_path}/screen_rate_{set.screen_rate}/{set.error_name}/{set.num}_terminal.txt", mode='a', encoding='utf-8') as text_file:
    #    text_file.write(f"\n-------------\nterminal text: \n{terminal_text}\n")
    #with open(f"{set_t.output_path}/terminal_{main_g.num}.txt", mode='a', encoding='utf-8') as text_file:
    #            text_file.write(f"\n-------------\nterminal text: \n{terminal_text}\n")
    
    # エラーがあれば、エラー文を取得
    # 'Traceback','Error','File','line'が含まれているかどうかで判定
    if ('Error' in terminal_text and 'File' in terminal_text and 'line' in terminal_text) or ('Traceback' in terminal_text and 'File' in terminal_text and 'line' in terminal_text):
        #print('Error found!')
        # 取得した文字列に含まれる 'PS [folder_path]' をすべて削除
        error_text = terminal_text.replace('PS ' + set.folder_path, '')
        return error_text

    # エラーがなければ、プログラムを終了
    #if 'Traceback' not in terminal_text and 'Error' not in terminal_text and 'File' not in terminal_text and 'line' not in terminal_text:
    else:
        print('コード生成が成功しました。')
        #sys.exit()
        # テスト用_1
        return 'exit main'



def kind_of_error(error_text):
        # 正規表現を利用してエラータイプを取得する
        # 例: 'TypeError: 'int' object is not iterable' ならば、TypeErrorを取得する
        #error_type = re.search(r'^\w*Error', error_text, re.MULTILINE).group()
        error_type = re.search(r'^\w*Error', error_text, re.MULTILINE)
        error_type = error_type.group() if error_type else " 'Error' type not found."  # 'Error'という文字列が見つからない場合は、'Error' type not found.を返す
        print(error_type)
        return error_type

        
        

def fix_module_not_found_error(error_text):
    if Error_Fix.import_error(error_text)==True:        
            return 'ModuleNotFoundError'  # モジュール名返して、インストール完了したか確認できるようにする？
    elif Error_Fix.import_error(error_text)==False:
        return 'exit main'
    
def fix_file_not_found_error(question, error_text):
    filename, file_path = Error_Fix.file_path_error(error_text)
    # ファイルが見つからなければ、プログラム終了
    # テスト用_2_2
    if filename == 'exit main' and file_path == 'exit main':
        return 'exit main'
     
    # ファイルが見つかれば、新しい問題文(問題文にファイルパスを追加したもの)を返す
    # questionにファイル名が含まれる場合、絶対パスに置き換える
    if filename in question:
        question = question.replace(filename, file_path, 1)
    # ファイル名が含まれていない場合、ファイル名とファイルパスを追加する
    else:
        question = question + f'\n "{filename}" のファイルパスは、{file_path} です。\n'
    
    return (filename, file_path, question) #file_path #'enviromental_error'


    
# 環境的なエラーを直した（とされる）後の処理
# 再度実行、エラーが出た場合、エラー文を取得し、エラーの種類によって処理を分ける
def execute_fixed_enviromental_error():
        pyautogui.click(set.x_blanc_space, set.y_blanc_space)
        # 保存
        pyautogui.hotkey('ctrl', 's')
        # 実行
        pyautogui.click(set.x_execute, set.y_execute)
        time.sleep(set.execution_interval)
        # input()があれば、入力を行う
        input_cml()
        
        # 実行が終わったかチェック
        execution_completion(timeout=set.execution_timeout)
        # エラーが出たら、エラー文を取得。なければそのまま終わるはず
        error_text = error_check()
        return error_text
        
        #return



def create_new_request(error_text, question, generated_code):
    # テキストを追加
    # 'Fix the error.'の部分を、より修正率が高まるように変更しておく
    # new_request = f'Fix the error.\nrequest:\n{first_request}\n\ncode:\n{generated_code}\n\nerror:\n{error_text}'
    # テスト用に日本語文に変更
    
    # 要求文
    new_request = f'要求:\n{question}\n\n 以下のエラーを解決した、新しいコードを生成してください。\n\nコード:\n{generated_code}\n\nエラー:\n{error_text}'
    # 以下のエラーを直してください。
    # 以下のエラーを解決してください。
    # \n\ncode:\n{generated_code} なしでエラー文のみ
    return new_request

