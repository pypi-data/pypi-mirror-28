# -*- coding: UTF-8 -*-
from __future__ import division
import sys

sys.path.append("..")
import json
import re
from db.dbconnecter import get_param_conn
from db.daos import ProductDao, ProductSkuDao, FarfetchDesignerDao
from db.models import DBParams, ProductSku
from netvisiter.net_openner import NetOpener

PDAO = None
PSDAO = None
FDDAO = None
OPENER = None


def init_daos():
    db_params = DBParams()
    db_params.host = "10.26.235.6"
    db_params.port = "3066"
    db_params.user = "spider"
    db_params.passwd = "spider@1919"
    db_params.db = "spider_sku"
    conn = get_param_conn(db_params)
    if conn is None:
        print("没有此数据库")
        return False
    cur = conn.cursor()
    global PDAO
    global PSDAO
    global FDDAO
    PDAO = ProductDao(conn, cur)
    PSDAO = ProductSkuDao(conn, cur)
    FDDAO = FarfetchDesignerDao(conn, cur)


def init_opener():
    global OPENER
    OPENER = NetOpener("https://www.farfetch.cn/it/shopping/women/items.aspx", "farfetch_cookie.txt")
    OPENER.init_cookie()
    OPENER.load_cookie()
    OPENER.load_opener()


def update_size_info(spid, sizes, prices):
    global PSDAO
    for size in sizes:
        for price in prices:
            if size["variantId"] == price["variantId"]:
                if not price["isInStock"]:
                    PSDAO.set_sku_out_of_stock(spid, size["size"])
                    print "".join([str(spid), ":", str(size["size"])])


def do_visit(url):
    try:
        global OPENER
        rsp = OPENER.visit_url(url, None)
        return json.loads(rsp.read())
    except Exception:
        return do_visit(url)


# 弃用方法，原用于获取商品的designer，因接口调用需要
def init_designer_dic():
    global FDDAO
    datas = FDDAO.get_all_designer()
    designerDic = {}
    for item in datas:
        designerDic[item[1]] = item[2]
    return designerDic


def match_size(sku, sizes):
    for size in sizes:
        size_str = size["Description"]
        size_scale = size["ScaleDescription"]
        if size_scale is not None:
            size_str = "".join([size_str, "[", size_scale, "]"])
        if size_str == sku[2]:
            return size
        if sku[2] == "One Size" and size_str == "OS":
            return size
    return None


def get_price_num(priceStr):
    if priceStr == "":
        return None
    pstr = str(priceStr.split(" ")[0])
    pstr = pstr.replace(".", "")
    return pstr


def update_skus(spid, sizes):
    global PSDAO
    skus = PSDAO.get_on_skus_by_spid(spid)
    for sku in skus:
        # 找出爬虫库相对应的尺码信息
        msize = match_size(sku, sizes)
        # 尺码为空则商品已售罄
        if msize is None:
            PSDAO.set_sku_out_of_stock(sku[1], sku[2])
            print "".join([str(sku[1]), ":", str(sku[2])])
        else:
            # 封装并更新sku信息
            pinfo = msize["PriceInfo"]
            oprice = get_price_num(pinfo["FormatedPriceWithoutPromotion"])
            dprice = get_price_num(pinfo["FormatedPrice"])
            psku = ProductSku()
            psku.discount_price = dprice
            if oprice is not None:
                psku.price = oprice
            else:
                psku.price = dprice
            psku.spider_product_sku_id = sku[0]
            PSDAO.update_product_sku(psku)
            print "".join([str(spid), ":", str(psku.spider_product_sku_id), ":", sku[2], ":", str(psku.price)])


# 查看尺码信息集中是否有对应该店铺id的记录
def no_store(availableSizes, storeid):
    for item in availableSizes:
        if item['StoreId'] == storeid:
            return False
    return True


def do_update():
    init_daos()
    init_opener()
    global PDAO

    # designerDic = init_designer_dic()

    # 获取需要更新的爬虫商品
    products = PDAO.get_need_update_products_by_site("farfetch")
    for product in products:
        spid = product[0]
        farfetchId = product[9]
        flag_num = int(product[6])
        storeid = 0
        # 标识小12的为farfetch 特定11家店铺的商品，该店铺中有此商品才算在架
        if flag_num < 12:
            # 获取店铺id
            storeid = re.findall(r'storeid=([0-9]*)', product[10])[0]
        # designerId = designerDic[product[1]]
        farfetchUrl = "".join(
            ["https://www.farfetch.cn/it/product/GetDetailState?productId=", farfetchId, "&designerId=0"])
        # 有店铺id的拼上店铺id
        if storeid != 0:
            farfetchUrl = "".join([farfetchUrl, "&storeid=", str(storeid)])
        skus = do_visit(farfetchUrl)
        # 获得尺码信息
        availableSizes = skus["SizesInformationViewModel"]["AvailableSizes"]
        # 没有尺码信息则商品下架
        if len(availableSizes) == 0:
            PSDAO.set_skus_out_of_stock_by_spid(spid)
            print "".join([str(spid), " all out of stock"])
            continue
        # 有店铺id的，要确定在架商品的店铺id与该id一致，不一致的则该店已没有该商品
        if storeid != 0 and no_store(availableSizes, storeid):
            PSDAO.set_skus_out_of_stock_by_spid(spid)
            print "".join([str(spid), " all out of stock"])
            continue
        update_skus(spid, availableSizes)


if __name__ == "__main__":
    do_update()
