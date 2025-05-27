# Automatic_code_generation\program のフォルダのパス
program_path = r"C:\Automatic_code_generation\program"

# コードを生成するファイルがあるディレクトリのパス(ドライブ名のみでも可)　バッチから変更可能
folder = r"C:\py_test"

# Windowsの画面拡大率（%）
screen_rate = 125

# タイムアウトするまでの時間(秒)
agreement_timeout = 20  # 同意ボタンの表示で待つ最大値 (コード生成されるまでの待ち時間)
execution_timeout = 10  # 実行完了で待つ最大値 (実行ボタンを押してから実行完了までの待ち時間)
installation_timeout = 120  # インストール完了で待つ最大値 (モジュールがない場合のインストール完了までの待ち時間)
file_search_timeout = 10  # ファイルが見つかるまでの待ち時間

# 処理の間の待ち時間（0.1~0.3程度）
pause = 0.2  # キー入力の間隔
check_interval = 0.2  # time.sleep()の時間(秒)。主に画像検索の間隔に使用。
execution_interval = 0.2  # 実行ボタンを押してから待つ秒数。PCの動作が遅いときなど、必要に応じて変更する。

#'''
# 画面解像度1920x1080, 画面拡大率125% での設定(座標の値はTkinter.pyを使って適宜変更してください。)
# 適当なスペース(ターミナル以外)の座標。VSCode右端の何もないスペースを指定してください。
x_blanc_space = 1800
y_blanc_space = 400

# VSCode右上にある実行ボタンの座標
x_execute = 1805
y_execute = 64

# ターミナルの座標。ターミナルの右下を指定して下さい。
x_terminal = 1200
y_terminal = 975  # y座標は、ターミナル内のなるべく下の部分を指定してください。（エラーがあった場合、ドラッグでターミナルの文字を全選択するため）
#'''

'''
# 画面拡大率100% の場合の設定（参考）
x_blanc_space = 1750 
y_blanc_space = 400 
x_execute = 1830 
y_execute = 50 
x_terminal = 1600 
y_terminal = 1003 
'''

'''
# 画面拡大率150% の場合の設定（参考）
x_blanc_space = 1790 
y_blanc_space = 400 
x_execute = 1780 
y_execute = 75 
x_terminal = 1710 
y_terminal = 964 
'''


# 画像の検索精度(0.1~1.0)（同意ボタンなどを認識しにくい場合は精度を少し下げてください。）
gray_confidence = 0.8
color_confidence = 0.6


# 画像のパス。  (以下の5つの画像は日本語環境でのみ使用可能。)
four_match_found = program_path + "\\picture\\" + fr"four_match_found_{screen_rate}.png"  # 検索結果が「4/4 件」のときの画像
five_match_found = program_path + "\\picture\\" + fr"five_match_found_{screen_rate}.png"  # 検索結果が「5/5 件」のときの画像
agreement_button = program_path + "\\picture\\" + fr"agreement_button_{screen_rate}.png"  # コード生成後のCopilotの「同意する」ボタン
re_execute_button = program_path + "\\picture\\" + fr"re_execute_button_{screen_rate}.png"  # コード生成後のCopilotに「チャットで表示する」と表示された場合の再実行「なしで実行」ボタン
re_execute_button_2 = program_path + "\\picture\\" + fr"re_execute_button_2_{screen_rate}.png"  # 「なしで実行」ボタンが見切れた時用の画像

yes_or_no = program_path + "\\picture\\" + fr"y_n_{screen_rate}.png"  # インストール時の「(Y/n)?」の画像
yes_or_no_2 = program_path + "\\picture\\" + fr"y_n_2_{screen_rate}.png"  # インストール時の「([y]/n)?」の画像
# proceed_yes_or_no = program_path + "\\picture\\" + r"proceed_y_n_125.png"  # インストール時の「Proceed? ([y]/n)?」の画像


# 以下、変更の必要なし
# ターミナル内でPS [path]を検索するときにように、「/」があれば「\」に置き換える
folder_path = folder.replace('/', '\\')
# ファイルパスを出力する場合は、エラーが出る可能性があるから、「/」に置き換える
four_match_found = four_match_found.replace('\\', '/')
five_match_found = five_match_found.replace('\\', '/')
agreement_button = agreement_button.replace('\\', '/')
re_execute_button = re_execute_button.replace('\\', '/')
re_execute_button_2 = re_execute_button_2.replace('\\', '/')
yes_or_no = yes_or_no.replace('\\', '/')
yes_or_no_2 = yes_or_no_2.replace('\\', '/')


