import re
import unicodedata
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time

def normalize_address_v29(address):
    # 住所の基本的な正規化
    address = address.replace("－", "-").replace("ー", "-")

    # 各部分を抽出するための正規表現
    district_match = re.search(r"([^市]+市)([^区]*区)?", address)
    if not district_match:

        district_match = re.search(r"([^市]+市)([^0-9\-丁目]+)?", address)
    town_match = re.search(r"([^市]+市)?([^区]*区)?([^0-9\-丁目]+丁目)?", address)
    street_num_match = re.search(r"(\d+[-−]?\d?(番\d+号?)?)?$", address)


    district, town, street_num = "", "", ""
    if district_match:
        district = district_match.group(2) if district_match.group(2) else ""


    if town_match:
        town = town_match.group(3) if town_match.group(3) else ""



    if street_num_match:
        street_num = street_num_match.group(1) if street_num_match.group(1) else ""
        # Convert street_num to half-width characters and remove any characters after a hyphen
        street_num = unicodedata.normalize('NFKC', street_num).split('-')[0]
        street_num_match = re.search(r"^(\d+)", street_num)
    if street_num_match:
        street_num =street_num_match.group(0) if street_num_match.group(0) else ""

    return {"区": district, "町名": town, "街区番号": street_num}

def format_address_v15(address):
    # 大字名、字町名、街区の取得
    district = address["区"]
    town = address["町名"]
    street_num = re.search(r"(\d+)", address["街区番号"]).group(1) if re.search(r"(\d+)", address["街区番号"]) else ""

    formatted_str = ""
    if district:
        formatted_str += f"大字名：{district}、"
    if town:
        formatted_str += f"字町名：{town}、"
    if street_num:
        formatted_str += f"街区：{street_num}"
    return formatted_str

def get_map_pdf(addresses):
    # Chromeの設定
    chromeOptions = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory" : r"C:\Users\たくみ\Documents\Summer Intern mapRPA\mapRPA\ss",
        "download.directory_upgrade" : True,
        "savefile.default_directory" : r"C:\Users\たくみ\Documents\Summer Intern mapRPA\mapRPA\ss",
        "savefile.directory_upgrade" : True
    }
    chromeOptions.add_experimental_option("prefs", prefs)
    driver2 = webdriver.Chrome(options=chromeOptions)

    # 適当な場所の地図を開く
    driver2.get('https://webgis.alandis.jp/chiba12/webgis/index.php/autologin_jswebgis?ap=jsWebGIS&m=2&u=guest1&x=15597323.5479798&y=4262337.39269382&s=5000&rs=3857&li=1&si=0')
    time.sleep(3)

    # 検索ボタンが表示されるまで待つ
    wait1 = WebDriverWait(driver2, 30)  # 最大で30秒待機
    search_button_1 = wait1.until(EC.visibility_of_element_located((By.ID, 'sidemenu_tab_search')))
    search_button_1.click()
    time.sleep(5)

    # 住所検索ボタンが表示されるまで待つ
    wait2 = WebDriverWait(driver2, 30)  # 最大で30秒待機
    address_button = wait2.until(EC.visibility_of_element_located((By.ID, 'sidemenu_menu_search_drilldown_1')))
    address_button.click()
    time.sleep(3)

    for address in addresses:
        try:
            # "大字名"のドロップダウンから指定された区を選択
            district_select = Select(driver2.find_element(By.ID, 'srh_search_drilldown_1_attrvalue_1'))
            district_select.select_by_visible_text(address["区"])
            time.sleep(1)
        except Exception:
            print(f"{address['区']}は選べませんでした。")
            continue

        try:
            # "字町名"のドロップダウンから指定された町名を選択
            town_select = Select(driver2.find_element(By.ID, 'srh_search_drilldown_1_attrvalue_2'))
            town_select.select_by_visible_text(address["町名"])
            time.sleep(2)
        except Exception:
            print(f"{address['町名']}は選べませんでした。")
            continue


            # "街区"のドロップダウンから指定された街区を選択
        block_select = Select(driver2.find_element(By.ID, 'srh_search_drilldown_1_attrvalue_3'))
        try:
                # Convert address["街区番号"] to half-width characters if it contains full-width characters
            street_num = unicodedata.normalize('NFKC', address["街区番号"])
            block_select.select_by_visible_text(street_num)
        except Exception:
                # If the full address is not found, try only the number before the hyphen
            hyphen_index = street_num.find('-')
            if hyphen_index != -1:
                block_select.select_by_visible_text(street_num[:hyphen_index])
                hyphen_index = street_num.find('ー')
            else:
                raise
        time.sleep(2)

        # 検索ボタンが表示されるまで待つ
        wait3 = WebDriverWait(driver2, 30)  # 最大で30秒待機
        search_button_2 = wait3.until(EC.visibility_of_element_located((By.ID, 'srh_search_drilldown_1_btn')))
        search_button_2.click()
        time.sleep(3)

        # ボタンが表示されるまで待つ
        wait4 = WebDriverWait(driver2, 30)  # 最大で30秒待機
        search_button_3 = wait3.until(EC.visibility_of_element_located((By.ID, 'index_hidden')))
        search_button_3.click()
        time.sleep(3)

        # ボタンが表示されるまで待つ
        wait5 = WebDriverWait(driver2, 30)  # 最大で30秒待機
        search_button_4 = wait3.until(EC.visibility_of_element_located((By.ID, 'sidemenu_tab_print')))
        search_button_4.click()
        time.sleep(3)

        # ボタンが表示されるまで待つ
        wait5 = WebDriverWait(driver2, 30)  # 最大で30秒待機
        search_button_5 = wait3.until(EC.visibility_of_element_located((By.ID, 'sidemenu_menu_print_detail')))
        search_button_5.click()
        time.sleep(3)

        # ボタンが表示されるまで待つ
        wait6 = WebDriverWait(driver2, 30)  # 最大で30秒待機
        search_button_6 = wait3.until(EC.visibility_of_element_located((By.ID, 'prt_pdfOutput_printing_output')))
        search_button_6.click()
        time.sleep(20)




# 住所データのリスト
address_list = [

    "千葉県千葉市稲毛区稲毛町５丁目269−１"

]


if __name__ == "__main__":
    # Normalize addresses
    addresses_v29 = [normalize_address_v29(addr) for addr in address_list]
    print(addresses_v29)
    get_map_pdf(addresses_v29)

