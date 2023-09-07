
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

def normalize_address(address):
    # 住所の基本的な正規化
    address = address.replace("－", "-").replace("ー", "-")

    # 各部分を抽出するための正規表現
    district_match = re.search(r"([^市]+市)?([^区]+区)", address)
    town_match = re.search(r"([^区]+区)?([^丁目]+)", address)
    block_match = re.search(r"(\d+丁目)?(\d+[-−番号\d+]*[-−番号\d+]?)", address)

    district, town, block_num, street_num = "", "", "", ""
    if district_match:
        district = district_match.group(2) if district_match.group(2) else ""
    if town_match:
        town = re.sub(r'\d+', '', town_match.group(2)) if town_match.group(2) else ""
    if block_match:
        block_num = block_match.group(1) if block_match.group(1) else ""
        street_num_parts = block_match.group(2).replace("番", "").replace("号", "").replace("−", "-").split("-")
        if len(street_num_parts) > 1:
            street_num = street_num_parts[0] + "番" if street_num_parts[0].isdigit() else ""

    return {"区": district, "町名": town, "丁目": block_num, "街区番号": street_num}

# 住所データのリスト
address_list = ['千葉県千葉市稲毛区稲毛３丁目７−３０',
    '千葉県千葉市稲毛区稲毛3-7',
    "千葉県千葉市稲毛区稲毛町５丁目269−１",
    "千葉市稲毛区稲毛町５ー２６９ー１",
    "千葉県浦安市北栄1-15-9",
    "千葉県千葉市美浜区真砂五丁目１５−１",
    "千葉県千葉市美浜区真砂5丁目15−1",
    "千葉県千葉市美浜区真砂５丁目１５番１",
    "千葉県千葉市美浜区真砂５-１５−１",
    "千葉県千葉市美浜区真砂６丁目１−１"
]
# 住所を正規化
addresses = [normalize_address(addr) for addr in address_list]

def refine_address(address):
    # 町名の後の不要なハイフンを取り除く
    address["町名"] = address["町名"].strip('-')
    # 街区番号のハイフンを取り除く
    address["街区番号"] = address["街区番号"].strip('-')
    if address["街区番号"].isdigit():
        address["街区番号"] += "番"
    return address

# 既存の正規化された住所リストを再調整
refined_addresses = [refine_address(addr) for addr in addresses]
print(refined_addresses)
"""
# Chromeを操作
driver = webdriver.Chrome()
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

ids = ["ELM_CMB_LEV1", "ELM_CMB_LEV2", "ELM_CMB_LEV3", "ELM_CMB_LEV4"]
elements = {i: driver.find_element(By.ID, i) for i in ids}

for address in addresses:
    # 各住所情報を入力
    for key, element_id in zip(["区", "町名", "丁目", "街区番号"], ids):
        if elements[element_id].is_enabled() and elements[element_id].is_displayed():
         elements[element_id].clear()
        elements[element_id].send_keys(address[key])
        time.sleep(1)

    # 検索ボタンをクリック
    decision_button = driver.find_element(By.ID, "btnAddSchDlgOK")
    decision_button.click()

    # 5秒間待機
    time.sleep(5)
"""
