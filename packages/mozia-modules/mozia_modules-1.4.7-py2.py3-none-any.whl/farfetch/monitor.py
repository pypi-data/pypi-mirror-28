# -*- coding: UTF-8 -*-
import json
import time
import network
import re
from bs4 import BeautifulSoup

from keys import KEY_MONITOR_PRODUCT_TASKS
from modules.scheduler import task_scheduler
from repository import dao


def get_monitor_task_length():
    return task_scheduler.redis.llen(KEY_MONITOR_PRODUCT_TASKS)


def create_monitor_product_tasks():
    task_length = get_monitor_task_length()
    if task_length > 0:
        print "Have task in queue:", task_length
        return

    for monitor_task in dao.monitor.get_monitor_products():
        print "create monitor task:", monitor_task
        monitor_task["time"] = int(time.time())
        task_scheduler.push(KEY_MONITOR_PRODUCT_TASKS, json.dumps(monitor_task))


def get_monitor_product_task():
    task_length = get_monitor_task_length()
    print "tasks in queue:", task_length
    task_string = task_scheduler.pop(KEY_MONITOR_PRODUCT_TASKS)
    if not task_string:
        return None
    return json.loads(task_string)


def get_product_sizes_url(product_id, store_id, category_id, manufacturer_id):
    url = "https://www.farfetch.cn/it/product/GetDetailState?productId=%s&storeId=%s&sizeId=&categoryId=%s&designerId=%s"
    return url % (product_id, store_id, category_id, manufacturer_id)


def is_from_farfetch(monitor_task):
    source_url = monitor_task["source_url"]
    return source_url.startswith("https://www.farfetch.cn/")


def is_need_crawl(monitor_task):
    last_crawl = dao.monitor.get_last_crawl_time(monitor_task["product_id"])
    if not last_crawl:
        return True

    print last_crawl


def crawl_product_for_monitor(monitor_task):
    if not is_from_farfetch(monitor_task):
        return

    if not is_need_crawl(monitor_task):
        return

    source_url = monitor_task["source_url"].replace("https://www.farfetch.cn/cn/", "https://www.farfetch.cn/it/")
    monitor_task["source_url"] = source_url
    monitor_task["source_type"] = "FARFETCH"
    timestamp = int(time.time())

    print "begin task:", json.dumps(monitor_task)
    page = network.download(source_url)

    soup = BeautifulSoup(page, "html.parser")
    script_soup = soup.find("script", text=re.compile("window.universal_variable.product\s*=\s*"))

    # 找不到商品信息
    if not script_soup:
        # 商品已售罄
        print "product sold out:", json.dumps(monitor_task)
        dao.monitor.set_platform_product_status(monitor_task["product_id"], 0)
        return

    product = json.loads(
        script_soup.string.strip().replace("window.universal_variable.product =", "").strip().rstrip(";"))
    sizes_url = get_product_sizes_url(product["id"], product.get("storeId"), product["categoryId"],
                                      product["manufacturerId"])

    sizes_string = network.download(sizes_url)
    if sizes_string:
        sizes_info = json.loads(sizes_string)["SizesInformationViewModel"]
        sizes = sizes_info["AvailableSizes"]
        if not sizes:
            print "product no available sizes:", sizes_string
            dao.monitor.set_platform_product_status(monitor_task["product_id"], 0)
            dao.monitor.update_crawl_time(monitor_task, 0)
        else:
            dao.monitor.update_crawl_time(monitor_task, 1)
    else:
        # 没有尺码则下架
        print "product no size info:", sizes_string
        dao.monitor.set_platform_product_status(monitor_task["product_id"], 0)
        dao.monitor.update_crawl_time(monitor_task, 0)

    print "end task, cost(%d):" % (int(time.time()) - timestamp), json.dumps(monitor_task)


def start_farfetch_monitor():
    create_monitor_product_tasks()
    task = get_monitor_product_task()
    while task:
        crawl_product_for_monitor(task)
        task = get_monitor_product_task()


if __name__ == "__main__":
    task_scheduler.connect()
    while True:
        start_farfetch_monitor()
