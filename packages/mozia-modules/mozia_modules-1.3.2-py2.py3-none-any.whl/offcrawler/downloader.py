# -*- coding: UTF-8 -*-
import oss2
import time
import re
import requests
from repository import dao
from modules.repository import repositories
from modules.scheduler import task_scheduler
import os

endpoint = "oss-cn-shanghai.aliyuncs.com";
access_key_id = "Ik486j07fnzdJxVC";
access_key_secret = "zv8ESNdIrZ7wv2CZOeEMEgJhiDIoKC";
bucket_name = "images-media";
aliasUrl = "http://cdn.fashionfinger.com";

# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)


def download_and_retry(url, times=3):
    try:
        return requests.get(url)
    except Exception as e:
        print("download error, retry...", repr(e))
        if times > 0:
            return download_and_retry(url, times - 1)


def save_image_to_oss(task, image_url, index):
    if is_oss_url(image_url):
        return image_url

    print("image url:", image_url)
    oss_url = "s%02d/%04d/%08d/%02d.jpg" % (task["source_type"], task["designer_id"], task["product_id"], index)
    page = download_and_retry(image_url)
    result = bucket.put_object(oss_url, page.content)
    if 200 != result.status:
        raise Exception("save to oss error", result.status)

    return "https://images-media.oss-cn-shanghai.aliyuncs.com/%s" % oss_url


def is_oss_url(image_url):
    pattern = re.compile("http(s)?://images-media\.oss-cn-shanghai\.aliyuncs\.com/.*")
    match = pattern.match(image_url)
    return match


def download_images(task):
    image_urls = dao.platform.get_product_sku_images(task["product_id"])
    if not image_urls or len(image_urls) == 0:
        print("[%s]no images download" % task["product_id"])
        return

    oss_urls = [save_image_to_oss(task, image_url, index) for (index, image_url) in enumerate(image_urls)]
    cover = oss_urls[0]
    dao.platform.save_product_images(task["product_id"], cover, oss_urls)
    dao.task.set_product_image_task_status(task["product_id"], 1)
    save_cover_to_dir(task, cover)


def save_cover_to_dir(task, cover_url):
    cover_dir = "/home/fashion/monitor/cover/%s" % time.strftime('%Y%m%d', time.localtime(time.time()))
    if not os.path.isdir(cover_dir):
        os.makedirs(cover_dir)
    path = cover_url.replace("https://images-media.oss-cn-shanghai.aliyuncs.com/", "")
    cover_path = "%s/%s" % (cover_dir, "-".join(path.split("/")))
    print("save cover:", cover_path)
    page = download_and_retry(cover_url)
    cover_file = open(cover_path, "wb")
    cover_file.write(page.content)
    cover_file.close()


def start_images_downloader(sleep_seconds=600):
    while True:
        task = dao.task.get_product_image_task()
        if task:
            download_images(task)
        else:
            print("No task, sleep %s seconds" % sleep_seconds)
            time.sleep(int(sleep_seconds))
            dao.task.create_product_image_task()


if __name__ == "__main__":
    repositories.connect()
    task_scheduler.connect()
    start_images_downloader(10)
