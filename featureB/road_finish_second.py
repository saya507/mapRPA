
from selenium import webdriver
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select



def half_to_full_width_num(n: str) -> str:
    """
    Convert half-width numbers to full-width.
    """
    # 半角数字と全角数字の対応関係
    half = '0123456789'
    full = '０１２３４５６７８９'
    table = str.maketrans(half, full)

    return n.translate(table)


def extract_address_info(input_string):
    # ブラウザを起動します（ここではChromeを例としています）
    driver = webdriver.Chrome()

    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")  # ヘッドレスモードを有効にする

    #driver = webdriver.Chrome(options=chrome_options)

    # 指定されたURLにアクセスします
    driver.get("http://asp.ncm-git.co.jp/AddressConvert/Seikika.aspx")

    # <input> 要素に任意の文字列を入力
    input_element = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_txtAddress")
    input_element.clear()
    input_element.send_keys(input_string)

    # 変換ボタンを探してクリック
    convert_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnConvert")
    convert_button.click()

    # ページの要素が読み込まれるまで少し待機（これはページの読み込み速度により調整が必要）
    time.sleep(1)

    # 住所情報を取得
    district_text = driver.find_element(By.XPATH, "//td[contains(text(), '（')][3]").text
    district = re.sub(r"（.*?）", "", district_text)  # 括弧とその中身を削除



    town_text = driver.find_element(By.XPATH, "//td[contains(text(), '（')][4]").text
    town = re.sub(r"（.*?）", "", town_text)  # 括弧とその中身を削除


    block_num = driver.find_element(By.XPATH, "//td[8]").text
    block_num = half_to_full_width_num(block_num)
    combined_town_block = f"{town}{block_num}丁目"

    street_num = driver.find_element(By.XPATH, "//td[9]").text

    # ブラウザを閉じる
    driver.quit()

    return {"区": district, "町名": combined_town_block, "街区番号": street_num}

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

def filter_address_list_1(address_list):
    # 「区」という文字列が含まれている要素だけを残す
    filtered_list = [addr for addr in address_list if "区" in addr]

    # 削除された要素がある場合のメッセージを表示
    if len(filtered_list) < len(address_list) :
        print("区外なので削除した要素がありました。")



    return filtered_list
def filter_address_list_2(address_list):
     # 「千葉」という文字列が含まれている要素だけを残す
    filtered_list = [addr for addr in address_list if "千葉" in addr]

    # 削除された要素がある場合のメッセージを表示
    if len(filtered_list) < len(address_list):
        print("千葉県ではなので削除した要素がありました。")
    return filtered_list




address_list = [
    '千葉県千葉市稲毛区稲毛３丁目７−３０',
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

if __name__ == "__main__":
    address_list = filter_address_list_1(address_list)
    address_list = filter_address_list_2(address_list)
    # Normalize addresses
    addresses_v29 = [extract_address_info(addr) for addr in address_list]
    print(addresses_v29)
    get_map_pdf(addresses_v29)
