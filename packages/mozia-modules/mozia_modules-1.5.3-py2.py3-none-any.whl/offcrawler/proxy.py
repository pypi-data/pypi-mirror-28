# -*- coding: UTF-8 -*-
import network
import re
import json
from bs4 import BeautifulSoup

ERROR = {"status": 500, "message": "Farfetch server error"}
SOLD_OUT = {"status": 100, "message": "Product sold out"}
NO_FOUND = {"status": 101, "message": "No product found"}


def crawl_product_sizes(product, catalog):
    product_id = product["id"]
    store_id = product.get("storeId")
    category_id = product["categoryId"],
    manufacturer_id = product["manufacturerId"]
    language_id = catalog["language_id"]

    if language_id == 2:
        url = "/it/product/GetDetailState?productId=%s&storeId=%s&sizeId=&categoryId=%s&designerId=%s"
    else:
        url = "/cn/product/GetDetailState?productId=%s&storeId=%s&sizeId=&categoryId=%s&designerId=%s"
    url = url % (product_id, store_id, category_id, manufacturer_id)

    sizes_string = network.download("https://www.farfetch.cn%s" % url)

    try:
        return json.loads(sizes_string)["SizesInformationViewModel"]["AvailableSizes"]
    except Exception as e:
        return None


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


def get_product_color(soup):
    soup = soup.find("span", itemprop="color")
    return soup.string.strip() if soup else None


# 尺码信息
def get_product_size_description(soup):
    content_size_soup = soup.find("div", attrs={"data-tstid": "Content_Size&Fit"})
    if not content_size_soup:
        return None

    size_soup = content_size_soup.find("div", class_="mb30")
    strings = []
    if size_soup:
        strings += [string for string in size_soup.stripped_strings]

    measure_info_soup = content_size_soup.find("div", class_="measure-info")
    if measure_info_soup:
        for string in measure_info_soup.stripped_strings:
            strings.append(string)

    measure_wrapper_soup = content_size_soup.find("div", class_="measures_wrapper")
    if measure_wrapper_soup:
        for string in measure_wrapper_soup.stripped_strings:
            strings.append(string)

    centimeters_soup = content_size_soup.find(id="centimeters_wrapper")
    if centimeters_soup:
        if centimeters_soup.dl.p:
            strings.append(centimeters_soup.dl.p.string.strip())
        if centimeters_soup.dl:
            measure_strings = get_product_text_strings(centimeters_soup.dl)
            strings += measure_strings

    model_is_wearing_soup = content_size_soup.find("p", class_="model_is_wearing")
    if model_is_wearing_soup:
        strings.append("".join([x for x in model_is_wearing_soup.stripped_strings]))

    return "\n".join(strings)


def crawl_product(catalog):
    html = network.download("https://www.farfetch.cn%s" % catalog["url"])
    if re.search("HTTP/1.0 500 Server Error", html):
        return ERROR

    soup = BeautifulSoup(html, "html.parser")

    if soup.find("div", class_="soldOut color-red bold h4"):
        return SOLD_OUT

    script_soup = soup.find("script", text=re.compile("window.universal_variable.product\s*=\s*"))
    # 找不到商品信息
    if not script_soup or not script_soup.string:
        return NO_FOUND

    product_string = script_soup.string.strip().replace("window.universal_variable.product =", "")
    product = json.loads(product_string.strip().rstrip(";"))
    product["sizes"] = crawl_product_sizes(product, catalog)
    product["image_urls"] = get_product_image_urls(soup)
    product["color"] = get_product_color(soup)
    product["constitute"] = get_product_constitute(soup)
    product["size_description"] = get_product_size_description(soup)

    return product


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

    print json.dumps(crawl_product(catalog))
