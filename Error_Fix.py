import pyautogui
import pyperclip
import re
import Execute
import Settings as set
import Search_Img
import time
import os
import Execute_Base as eb
import sys
import threading

# モジュールインポートエラーの解決
def import_error(error_text):
    pyautogui.PAUSE = set.pause # キー入力の間隔を設定
    
    # from ~ import ~ の形式のものもインストールできるようにする
    # 「import numpy as np」であれば、numpyの部分を取得する
    module_name = re.search(r"import (\w+)", error_text).group(1)
    print('ModuleNotFoundError: ' + module_name)
    print('\n' + module_name + 'のインストールを試みます...\n')
    
    # ターミナルリセット
    eb.reset_terminal()
    
    # モジュールのインストール
    pip = 'pip install ' + module_name
    pyperclip.copy(pip)
    pyautogui.click(set.x_terminal, set.y_terminal)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    
    # もし、Y/n の入力要求があれば、Yを入力する
    if Search_Img.search_image(set.yes_or_no)==True:
        pyautogui.click(set.x_terminal, set.y_terminal)
        pyautogui.press('y')
        pyautogui.press('enter')
    
    time.sleep(set.execution_interval)
    
    # インストールの実行が終わったか確認する（エラーの有無は関係なく、実行完了したか否か）
    if eb.execution_completion_check(set.installation_timeout)==True:
        #print('Finished installing ' + module_name + '.')
        return True
    # インストールが終了しない場合
    elif eb.execution_completion_check(set.installation_timeout)==False:
        print('インストールが失敗しました。インストールにかかる時間が長すぎたかもしれません...' + module_name)
        return False
    
 
# ファイルパスによるエラーの解決
def file_path_error(error_text):
    # 現在のディレクトリ (コード生成するファイルがあるディレクトリ)
    directory = set.folder_path
    
    # 見つからなかったファイル名を取得して、代入する
    filename = re.search(r"No such file or directory: '([^']+)'", error_text).group(1)  # (例) 'data.csv' が返る
    #print('FileNotFoundError: ')
    print(f'→ {filename}')

    # ファイルの探索
    found_file_path = search_up_and_down(directory, filename)
    
    start_time = time.time()
    timeout = set.file_search_timeout
    
    while time.time() - start_time < timeout:
        
        # ファイルが見つかった場合
        if found_file_path:
            # 取得したファイルパスに「\」が含まれる場合、「/」に変更する
            found_file_path = found_file_path.replace('\\', '/')
            print(f'"{found_file_path}" が見つかりました。\n')
            return filename, found_file_path
        # ファイルが見つからなかった場合
        else:
            print(f'\n! "{filename}" は見つかりませんでした。 !')
            print(f'! "{directory}"  このディレクトリとその親フォルダ、下層のフォルダ内には存在しません。 !')
            #sys.exit()
            # テスト用_2_1
            return 'exit main', 'exit main'
    print(f'\n! "{directory}" 周辺を探しましたが、"{filename}" は、{set.file_search_timeout} 秒以内には見つかりませんでした。 !')
    return 'exit main', 'exit main'
    

# ↑ file_path_error用の関数（変更）
def search_up_and_down(current_dir, filename):
    
    # 指定したディレクトリと、その同じ階層のディレクトリをチェック
    parent_dir = os.path.dirname(current_dir)
    # print(f'current_dir: {current_dir}')
    # print(f'parent_dir: {parent_dir}')
     
    def search(directory, filename):
        # 指定したディレクトリ内にファイルがあるか確認（下層までは確認しない）
        for file in os.listdir(directory):
            if file == filename:
                return os.path.join(directory, file)
        return None
    
    # 指定したディレクトリから下の階層へ探索
    def search_down(directory, filename):
        # Recursively search down to the specified level
        for root, dirs, files in os.walk(directory):
            if filename in files:
                return os.path.join(root, filename)
            # Search subdirectories if we haven't reached the level limit
            for subdir in dirs:
                result = search_down(os.path.join(root, subdir), filename)
                if result:
                    return result
        return None


    # カレントディレクトリにファイルがあるか確認
    result = search(current_dir, filename)
    if result:
        return result
    # カレントディレクトリにファイルがなければ、親フォルダを調べる
    else:
        result = search(parent_dir, filename)
        if result:
            return result
        # カレントディレクトリと親フォルダにファイルがなければ、カレントディレクトリの下層を探索
        else:
            result = search_down(current_dir, filename)
            if result:
                return result
            # それでも見つからない場合は、親フォルダの下の階層も探索
            else:
                return search_down(parent_dir, filename)
                