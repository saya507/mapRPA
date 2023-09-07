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
            #street_num = street_num_parts[0] + "番" if street_num_parts[0].isdigit() else ""
            street_num = street_num_parts[0] if street_num_parts[0].isdigit() else ""

    return {"区": district, "町名丁目": town+block_num, "街区番号": street_num}


def normalize_address_v26(address):
    # 住所の基本的な正規化
    address = address.replace("－", "-").replace("ー", "-")

    # 各部分を抽出するための正規表現
    district_match = re.search(r"([^市]+市)([^区]*区)?", address)
    if not district_match:
        district_match = re.search(r"([^市]+市)([^0-9\-丁目]+)?", address)  # Handle cases like "千葉県浦安市北栄1-15-9"
    town_match = re.search(r"([^市]+市)?([^区]*区)?([^0-9\-]+)?", address)
    block_num_match = re.search(r"(\d+丁目)?", address)
    street_num_match = re.search(r"(\d+[-−]?(\d+)?(番\d+号?)?)?$", address)

    district, town, block_num, street_num = "", "", "", ""
    if district_match:
        district = district_match.group(2) if district_match.group(2) else ""
    if town_match:
        town = town_match.group(3) if town_match.group(3) else ""
    if block_num_match:
        block_num = block_num_match.group(1) if block_num_match.group(1) else ""
        if block_num and not block_num.endswith("丁目"):  # Ensure "丁目" is added appropriately
            block_num += "丁目"
    if street_num_match:
        street_num = street_num_match.group(1) if street_num_match.group(1) else ""

    return {"区": district, "町名": town, "丁目": block_num, "街区番号": street_num}

def format_address_v14(address):
    # 大字名、字町名、街区の取得
    district = address["区"]
    town = address["町名"]
    block_num = address["丁目"]
    street_num = re.search(r"(\d+)", address["街区番号"]).group(1) if re.search(r"(\d+)", address["街区番号"]) else ""

    formatted_str = ""
    if district:
        formatted_str += f"大字名：{district}、"
    if town and block_num:
        formatted_str += f"字町名：{town}{block_num}、"
    elif town:
        formatted_str += f"字町名：{town}、"
    if street_num:
        formatted_str += f"街区：{street_num}"
    return formatted_str

# 住所データのリスト
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
    # Normalize addresses
    addresses_v26 = [normalize_address_v26(addr) for addr in address_list]

    # Format addresses
    formatted_addresses_v40 = [format_address_v14(addr) for addr in addresses_v26]
    print(formatted_addresses_v40)
