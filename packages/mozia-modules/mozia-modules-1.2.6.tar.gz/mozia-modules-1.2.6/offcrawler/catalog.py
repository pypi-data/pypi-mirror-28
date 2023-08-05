# -*- coding: UTF-8 -*-
import json
import re
import time
import network
from bs4 import BeautifulSoup
from repository import dao
from modules.repository import repositories


class IntramirrorCatalogCrawler:
    def __init__(self, task):
        self.task = task

    def start(self):
        url = self.task["url"]
        products = json.loads(network.download(url))
        self.create_catalogs(products["productList"])

    @staticmethod
    def get_product_url(catalog):
        return "http://106.14.205.107:8083/shoplus-buyer/api/product?id=%s" % catalog["shop_product_id"]

    @staticmethod
    def get_product_name(catalog):
        if catalog.get("skuList"):
            return catalog["skuList"][0]["name"]
            # skus = catalog["skuList"]

    @staticmethod
    def get_product_cover(catalog):
        if catalog.get("cover_img"):
            return json.loads(catalog["cover_img"])[0]

    def create_catalogs(self, products):
        print(json.dumps(products))
        for product in products["list"]:
            catalog = {
                "source_type": 3,
                "url": self.get_product_url(product),
                "source_id": product["shop_product_id"],
                "catalog_context": json.dumps(product),
                "catalog_status": 0,
                "product_name": self.get_product_name(product),
                "thumbnail": self.get_product_cover(product),
                "language_id": self.task["language_id"]
            }
            # product["extend"] = extend
            dao.catalog.save_catalog(catalog)


class FarfetchCatalogCrawler:
    def __init__(self, task):
        self.task = task

    @staticmethod
    def get_total_page(soup):
        pagination = soup.find("li", class_="pagination-label")
        total_page = pagination.find("span", attrs={
            "data-tstid": "paginationTotal"
        }).string
        return int(total_page)

    def create_catalogs(self, soup):
        soup = soup.find(text=re.compile("window.universal_variable.listing"))
        products = json.loads(soup.string.strip().replace("window.universal_variable.listing =", "").rstrip(";"))
        extend = json.loads(self.task.get("extend") or "{}")
        extend["catalog_id"] = products.get("categoryId")

        for product in products["items"]:
            catalog = {
                "source_type": 1,
                "url": product["url"],
                "source_id": product["id"],
                "catalog_context": json.dumps(product),
                "catalog_status": 0,
                "product_name": product["name"],
                "thumbnail": product["imageUrl"],
                "language_id": self.task["language_id"]
            }
            product["extend"] = extend
            dao.catalog.save_catalog(catalog)

    def crawl(self, page_url, task):
        print "begin url:", page_url
        html = network.download(page_url)
        soup = BeautifulSoup(html, "html.parser")
        self.create_catalogs(soup)
        print "end url:", page_url
        return soup

    def start(self):
        task = self.task
        try:
            url = task["url"]
            soup = self.crawl(url, task)
            quo = url.find("?") 
            total_page = self.get_total_page(soup)

            print "total page(%d):" % total_page, url
            for i in range(2, total_page):
                page_url = "%s&page=%d" % (url, i) if quo > 0 else "%s?page=%d" % (url, i)
                self.crawl(page_url, task)

            dao.task.update_task_status(task)
        except Exception as e:
            print 'repr(e):\t', repr(e)


if __name__ == "__main__":
    repositories.connect()
    # task = {
    #     "url": "http://106.14.205.107:8083/shoplus-buyer/Home/get/getProductList?pageNumber=0&pageSize=5000",
    #     "language_id": 1
    # }
    # IntramirrorCatalogCrawler(task).start()
    task = {
        "url": "https://www.farfetch.cn/cn/shopping/women/julian-fashion/items.aspx",
        "language_id": 1
    }
    FarfetchCatalogCrawler(task).start()
    #
    # task = {
    #     "url": "https://www.farfetch.cn/it/shopping/women/julian-fashion/items.aspx",
    #     "language_id": 2
    # }
    # FarfetchCatalogCrawler(task).start()
