from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import re
import os
import configparser
from PIL import Image
from io import BytesIO

def save_as_pdf(png_data, output_path):
    image = Image.open(BytesIO(png_data))
    image.convert('RGB').save(output_path + ".pdf")
    print(f"Saved as: {output_path}.pdf")

# 1

# Chromeのオプションを設定
chrome_options = webdriver.ChromeOptions()

#2

# Chromeを操作
driver = webdriver.Chrome(options=chrome_options)
driver.get('http://s-page.tumsy.com/chibagesui/index.html')

# すべての<frame>と<iframe>タグを取得
frames = driver.find_elements(By.TAG_NAME, "frame")
iframes = driver.find_elements(By.TAG_NAME, "iframe")

#3

# <frame>と<iframe>の両方を順番に確認
for frame in frames + iframes:
    try:
        # フレームに移動
        driver.switch_to.frame(frame)

        # id="LinkButton1"の要素を探してクリックする
        agree_button = driver.find_element(By.ID, "LinkButton1")
        agree_button.click()

        # 3秒間待機
        time.sleep(3)

        # ボタンがクリックされたら、ループを抜ける
        break
    except Exception as e:
        # エラーが発生した場合、メインのコンテンツに戻る
        driver.switch_to.default_content()

# テストデータ
addresses = [
    {"区": "稲毛区", "町名": "稲毛", "丁目": "２丁目", "街区番号": "１番"},
    # ... その他のテストデータもこの形式で追加 ...
]
ids = ["ELM_CMB_LEV1", "ELM_CMB_LEV2", "ELM_CMB_LEV3", "ELM_CMB_LEV4"]
elements = {i: driver.find_element(By.ID, i) for i in ids}

for address in addresses:
    # 区の情報を入力
    elements["ELM_CMB_LEV1"].send_keys(address["区"])
    time.sleep(1)
    # 町名の情報を入力
    elements["ELM_CMB_LEV2"].send_keys(address["町名"])
    time.sleep(1)
    # 丁名の情報を入力
    elements["ELM_CMB_LEV3"].send_keys(address["丁目"])
    time.sleep(1)
    # 番地の情報を入力
    elements["ELM_CMB_LEV4"].send_keys(address["街区番号"])

    # 検索ボタンをクリック
    decision_button = driver.find_element(By.ID, "btnAddSchDlgOK")
    decision_button.click()
    # 5秒間待機
    time.sleep(5)

#4

driver.maximize_window()

# イメージ取得
element = driver.find_element(By.ID, 'divMapControl')
png_data = element.screenshot_as_png  # png = 画像


# 既存のディレクトリの定義を変更
directory = "C:\\Users\\たくみ\\Documents\\Summer Intern mapRPA\\mapRPA\\ss"

# スクショ保存ディレクトリが存在しなければ生成
if not os.path.isdir(directory):
    os.makedirs(directory)  # os.makedirsは、複数の階層のディレクトリも作成可能

# 保存するPDFファイル名
fname = os.path.join(directory, "千葉市下水道地図1")

# イメージをPDFとして保存
save_as_pdf(png_data, fname)
