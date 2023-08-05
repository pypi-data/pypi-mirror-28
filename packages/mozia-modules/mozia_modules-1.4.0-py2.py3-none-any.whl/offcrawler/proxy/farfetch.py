# -*- coding: UTF-8 -*-
import re
import os
import json
from offcrawler import network
from bs4 import BeautifulSoup
from offcrawler.repository import dao

ERROR = {"status": 500, "message": "Farfetch server error"}
SOLD_OUT = {"status": 100, "message": "Product sold out"}
NO_FOUND = {"status": 101, "message": "No product found"}
KEYWORD_MAPPED = {
    "HIPS": "臀围",
    "BUST": "胸围",
    "WAIST": "腰围",
    "HEIGHT": "身高",
    "MODEL": "模特",
    "HEEL": "鞋跟"
}

COLOR_MAPPED = {
    "BLACK": "黑色"
}


def replace_words(string):
    keyword = string.split(":")[0]
    value = KEYWORD_MAPPED.get(keyword.upper())
    if value:
        return string.replace(keyword, value)
    return string


def crawl_product_sizes(product, catalog):
    product_id = product["id"]
    store_id = product.get("storeId")
    category_id = product["categoryId"],
    manufacturer_id = product["manufacturerId"]
    language_id = catalog["language_id"]

    if language_id == 2:
        url = "/it/product/GetDetailState?productId=%s&storeId=%s&sizeId=&categoryId=%s&designerId=%s"
    else:
        url = "/it/product/GetDetailState?productId=%s&storeId=%s&sizeId=&categoryId=%s&designerId=%s"
    url = url % (product_id, store_id, category_id, manufacturer_id)

    sizes_string = network.download("https://www.farfetch.cn%s" % url)

    try:
        return json.loads(sizes_string)["SizesInformationViewModel"]["AvailableSizes"]
    except:
        return None


def get_product_size(sku, product):
    price = sku["PriceInfo"]
    return {
        "original_price": int(price["Price"]),
        "size": sku["Description"],
        "currency": "EURO",
        "color": product["color"],
        "label": sku["MessageLabel"]
    }


def get_product_sizes(product, catalog):
    return [
        get_product_size(size, product)
        for size in crawl_product_sizes(product, catalog)
    ]


# /cn/shopping/women/dolce-gabbana-bellucci--item-11845899.aspx?storeid=9306&from=listing
def get_product_gender(url):
    pos = url.find("women")
    return 2 if -1 == pos else 1


def get_product_text_strings(soup):
    if not soup:
        return None

    lines = []
    dt = soup.find("dt")
    while dt:
        dd = dt.find_next_sibling("dd")
        lines.append(dt.string.strip() + dd.string.strip() if dd else "")
        dt = dd.find_next_sibling("dt")
    return lines


def get_product_image_urls(soup):
    images = []
    soup = soup.find("ul", class_="sliderProduct js-sliderProduct js-sliderProductPage")
    for image in soup.find_all("img", itemprop="image"):
        image_url = image["src"]
        # 图片只是 70 换成 1000
        images.append(image_url[:-6] + "1000.jpg")
    return images


def get_product_constitute(soup):
    # data - tstid = "Content_Composition&amp;Care" >
    ingredients = soup.find("div", attrs={
        "data-tstid": re.compile("Content_Composition")
    })
    lines = get_product_text_strings(ingredients)
    return "\n".join(lines)


def get_product_color(product):
    # soup = soup.find("span", itemprop="color")
    color_string = product["color"]
    if not color_string:
        return None

    [color_word, color_code] = color_string.split(",")
    color = dao.catalog.get_product_color(color_code, 1)
    if not color:
        dao.catalog.save_product_color({
            "color_code": color_code,
            "description": color_word,
            "source_type": 1,
            "color_name": COLOR_MAPPED.get(color_word)
        })
        return color_word
    return color["name"]


def get_product_measures(soup):
    strings = []
    if soup.dl.p:
        strings.append(soup.dl.p.string.strip())
    if soup.dl:
        measure_strings = get_product_text_strings(soup.dl)
        strings += measure_strings

    return [replace_words(item) for item in strings]


# 尺码信息
def get_product_size_description(soup):
    content_size_soup = soup.find("div", attrs={"data-tstid": "Content_Size&Fit"})
    if not content_size_soup:
        return None

    size_soup = content_size_soup.find("div", class_="mb30")
    strings = []
    if size_soup:
        strings += [string for string in size_soup.stripped_strings]

    centimeters_soup = soup.find(id="centimeters_wrapper")
    if centimeters_soup:
        strings += get_product_measures(centimeters_soup)

    model_is_wearing_soup = content_size_soup.find("p", class_="model_is_wearing")
    if model_is_wearing_soup:
        strings.append("".join([x for x in model_is_wearing_soup.stripped_strings]))

    return "\n".join(strings)


def get_product_description(product, soup):
    description = product.get("description")
    constitute = get_product_constitute(soup)
    size_description = get_product_size_description(soup)
    descriptions = [item for item in [description, constitute, size_description] if item]
    return "\n".join(descriptions)


def get_product_label(soup):
    label_soup = soup.find(class_="productLabel")
    return label_soup.string.strip() if label_soup else None


def crawl_farfetch_product(catalog):
    html = network.download("https://www.farfetch.cn%s" % catalog["url"])
    if re.search("HTTP/1.0 500 Server Error", html):
        return ERROR

    soup = BeautifulSoup(html, "html.parser")
    # html_path = "cookies/%s.html" % catalog["source_id"]
    # html_file = open(html_path, "w")
    # html_file.write(soup.prettify())
    # html_file.close()

    if soup.find("div", class_="soldOut color-red bold h4"):
        return SOLD_OUT

    pattern = re.compile("window.universal_variable.product\s*=\s*({.*});")
    script_soup = soup.find("script", text=pattern)
    if not script_soup or not script_soup.string:
        return NO_FOUND

    match = re.search(pattern, script_soup.string.strip())
    if not match:
        return NO_FOUND

    # product_string = script_soup.string.strip().replace("window.universal_variable.product =", "")
    product = json.loads(match.group(1).strip())
    product["color"] = get_product_color(product)
    # product["sizes"] = get_product_sizes(product, catalog)

    return {
        "name": product["name"],
        "label": get_product_label(soup),
        "gender": get_product_gender(catalog["url"]),
        "image_urls": get_product_image_urls(soup),
        "designer_name": product["designerName"],
        "designer_code": product["designerStyleId"],
        "source_id": catalog["source_id"],
        "source_type": catalog["source_type"],
        "categories": [product["category"], product["subcategory"]],
        "description": get_product_description(product, soup),
        "sizes": get_product_sizes(product, catalog),
        "context": product
    }


if __name__ == "__main__":
    catalog = {
        "source_type": 1,
        "catalog_id": 7909,
        "language_id": 1,
        "source_id": "12587559",
        "url": "/cn/shopping/women/dolce-gabbana-leopard-trim-cropped-trousers-item-12587559.aspx?storeid=9306&from=listing",
        "thumbnail": "https://cdn-images.farfetch-contents.com/12/58/75/59/12587559_12078291_255.jpg",
        "product_name": "leopard trim cropped trousers",
        "catalog_context": "{\"imageUrl\": \"https://cdn-images.farfetch-contents.com/12/58/75/59/12587559_12078291_255.jpg\", \"unit_sale_price\": 5617.1645, \"color\": \"\", \"CurrencyCode\": \"CNY\", \"name\": \"leopard trim cropped trousers\", \"skuCode\": \"12587559\", \"url\": \"/cn/shopping/women/dolce-gabbana-leopard-trim-cropped-trousers-item-12587559.aspx?storeid=9306&from=listing\", \"currencyCode\": \"CNY\", \"storeId\": 9306, \"sku_code\": \"12587559\", \"unit_price\": 5617.1645, \"currency\": \"CNY\", \"designerName\": \"Dolce & Gabbana\", \"image_url\": \"https://cdn-images.farfetch-contents.com/12/58/75/59/12587559_12078291_255.jpg\", \"stock\": 8, \"unitSalePrice\": 5617.1645, \"unitPrice\": 5617.1645, \"id\": \"12587559\", \"hasStock\": true, \"manufacturer\": \"Dolce & Gabbana\"}",
        "catalog_status": 0
    }

    print json.dumps(crawl_farfetch_product(catalog)).decode("unicode_escape")
