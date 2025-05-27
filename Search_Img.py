# HSV(カラー)：Copilotによるコード生成後の「同意」ボタンをクリックするため
# グレースケール：ターミナルの検索結果を認識するため
# グレースケールの方が白黒画像の認識精度が高いが、カラー画像はHSVの方が精度が高い

import cv2
import numpy as np
import pyautogui
import time
import Settings as set


# HSV(カラー)画像に合致する座標を返す関数
def get_color_coordinates(image_path, confidence=set.color_confidence):
    try:
        # スクリーンショットを撮影してOpenCV形式に変換
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # スクリーンショットをHSV色空間に変換
        screenshot_hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

        # ターゲット画像を読み込み
        target_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if target_image is None:
            print(f"{image_path} を読み込めませんでした。")
            return None

        # ターゲット画像をHSV色空間に変換
        target_image_hsv = cv2.cvtColor(target_image, cv2.COLOR_BGR2HSV)

        # HSVチャンネルごとにテンプレートマッチングを実行
        result_h = cv2.matchTemplate(screenshot_hsv[:, :, 0], target_image_hsv[:, :, 0], cv2.TM_CCOEFF_NORMED)
        result_s = cv2.matchTemplate(screenshot_hsv[:, :, 1], target_image_hsv[:, :, 1], cv2.TM_CCOEFF_NORMED)
        result_v = cv2.matchTemplate(screenshot_hsv[:, :, 2], target_image_hsv[:, :, 2], cv2.TM_CCOEFF_NORMED)

        # H, S, Vチャンネルのマッチング結果を平均化
        result_avg = (result_h + result_s + result_v) / 3

        # マッチング結果から最大値の場所を取得
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_avg)

        if max_val >= confidence:
            # マッチした場所を取得
            #print(max_loc)
            target_height, target_width = target_image_hsv.shape[:2]
            #print(target_height, target_width)
            center_x = max_loc[0] + target_width // 2
            center_y = max_loc[1] + target_height // 2
            bottom_y = max_loc[1] + target_height
            #print(center_x, center_y, bottom_y)
            return (center_x, center_y, bottom_y)
        else:
            # print("Image not found with sufficient confidence.")
            return None
    except Exception as e:
        print(f"エラーが発生しました：{e}")
        return None
    
# グレースケールの画像に合致する座標を返す関数
def get_gray_coordinates(image_path, confidence=set.gray_confidence):
    try:
        # スクリーンショットを撮影してOpenCV形式に変換
        screenshot = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # ターゲット画像を読み込み
        target_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if target_image is None:
            print(f"{image_path} を読み込めませんでした。")
            return None
        
        # ターゲット画像をグレースケールに変換
        if len(target_image.shape) == 3:
            target_image_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
        else:
            target_image_gray = target_image

        # テンプレートマッチングを実行
        result = cv2.matchTemplate(screenshot_gray, target_image_gray, cv2.TM_CCOEFF_NORMED)

        # マッチングの閾値を設定
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            # マッチした場所を取得
            # print(max_loc)
            target_height, target_width = target_image_gray.shape[:2]
            # print(target_height, target_width)
            center_x = max_loc[0] + target_width // 2
            center_y = max_loc[1] + target_height // 2
            # print(center_x, center_y)
            return (center_x, center_y)
        else:
            # print("Image not found with sufficient confidence.")
            return None
    except Exception as e:
        print(f"エラーが発生しました：{e}")
        return None



# 画像(「同意する」ボタン)が見つかるまで待機してからクリックする関数
def wait_and_click(image_path, timeout):
    pyautogui.PAUSE = set.pause
    
    start_time = time.time()  # 開始時間
    #timeout = set.agreement_timeout  # タイムアウト時間(秒)
    
    while time.time() - start_time < timeout:
        time.sleep(0.1)
        coordinates = get_color_coordinates(image_path)
        # 座標が取得できた場合
        if coordinates is not None:
            # クリックする
            pyautogui.click(coordinates[0], coordinates[1])
            return
        time.sleep(set.check_interval)
    print("画像にマッチする箇所が見つからず、タイムアウトしました。")
    # sys.exit()
    # テスト用_1
    return 'exit main'

# ↓ 変更
# # 画像1か2（「同意する」/「なしで再実行」）のどちらかが見つかった場合、クリックする関数
def wait_and_click_2(image_path_1, image_path_2, image_path_3, timeout):
    pyautogui.PAUSE = set.pause
    
    start_time = time.time()  # 開始時間
    #timeout = set.agreement_timeout  # タイムアウト時間(秒)
    
    while time.time() - start_time < timeout:
        #time.sleep(0.1)
        # 画像1（「同意する」画像）
        coordinates_1 = get_color_coordinates(image_path_1)
        # 座標が取得できた場合
        if coordinates_1 is not None:
            # クリックする
            pyautogui.click(coordinates_1[0], coordinates_1[1])
            return
        
        # 画像2（「なしで再実行」画像）
        coordinates_2 = get_color_coordinates(image_path_2)
        # 座標が取得できた場合
        if coordinates_2 is not None:
            pyautogui.click(coordinates_2[0], coordinates_2[1])
            
            # 「なしで実行」の座標が移動してしまう可能性があるため、再度座標を取得
            time.sleep(set.check_interval)
            coordinates_2 = get_color_coordinates(image_path_2)
            # 再度座標が取得できた(「なしで実行」の座標が移動してしまっていた)場合、クリックするループ
            while coordinates_2 is not None:
                pyautogui.click(coordinates_2[0], coordinates_2[1])
                #pyautogui.click(coordinates_2[0], coordinates_2[2])  # 「なしで実行」が見切れている時、中央ではなく下部をクリックするため
                time.sleep(set.check_interval)
                
                coordinates_3 = get_color_coordinates(image_path_3)  # 「なしで実行」が見切れている画像を使用して座標を取得
                if coordinates_3 is not None:
                    pyautogui.click(coordinates_3[0], coordinates_3[2])  # 「なしで実行」が見切れている時、中央ではなく下部をクリックするため
                    time.sleep(set.check_interval)

                coordinates_2 = get_color_coordinates(image_path_2)
            return "re_execute"
        time.sleep(set.check_interval)
    
    
    print("画像にマッチする箇所が見つからず、タイムアウトしました。")
    # sys.exit()
    # テスト用_1
    return 'exit main'

# 画像が見つかるまで待機する関数。ターミナル検索結果取得（実行完了判定）用
def search_and_wait(image_path_1, image_path_2, timeout):
    start_time = time.time()
    #timeout = set.execution_timeout
    
    while time.time() - start_time < timeout:
        coordinates_1 = get_gray_coordinates(image_path_1)
        coordinates_2 = get_gray_coordinates(image_path_2)
        # 画像1か2のどちらかが見つかった場合、Trueを返す
        if coordinates_1 is not None:
            #pyautogui.click(coordinates[0], coordinates[1])
            #print(f"Clicked on image at: ({coordinates[0]}, {coordinates[1]})")
            return True
        if coordinates_2 is not None:
            return True
        time.sleep(set.check_interval)
    return False


# 画像を見つける関数
def search_image(image_path):
    coordinates = get_gray_coordinates(image_path)
    if coordinates is not None:
        return True
    else:
        return False
