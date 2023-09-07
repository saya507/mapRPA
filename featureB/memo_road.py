from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import re

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
            time.sleep(3)
        except Exception:
            print(f"{address['町名']}は選べませんでした。")
            continue

        try:
            # "街区"のドロップダウンから指定された街区を選択
            block_select = Select(driver2.find_element(By.ID, 'srh_search_drilldown_1_attrvalue_3'))
            block_select.select_by_visible_text(address["街区番号"])
            time.sleep(3)
        except Exception:
            print(f"{address['街区番号']}は選べませんでした。")
            continue

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

# テストデータ
addresses = [
    {"区": "稲毛区", "町名": "稲毛２丁目", "街区番号": "o"}
]


get_map_pdf(addresses)
