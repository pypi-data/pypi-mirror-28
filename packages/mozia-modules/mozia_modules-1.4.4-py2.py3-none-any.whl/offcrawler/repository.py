# -*- coding: UTF-8 -*-
from modules.repository import Repository
from modules.scheduler import task_scheduler
import json


class PlatformRepository(Repository):
    def __init__(self):
        Repository.__init__(self, db="fashion_product")

    def get_product_sku_images(self, product_id):
        sql = """
        SELECT a.* FROM fashion_product.t_product_sku a 
        WHERE a.product_id=%s 
        AND a.sku_images IS NOT NULL 
        AND a.sku_images <> 'null' 
        AND trim(a.sku_images) <> '' 
        """

        with self.connection.cursor() as cursor:
            cursor.execute(sql, product_id)
            sku = cursor.fetchone()
        try:
            return json.loads(sku["sku_images"] or '[]') if sku else None
        except:
            return None

    def save_product_images(self, product_id, cover, image_urls):
        sql = """
        UPDATE fashion_product.t_product a,
         fashion_product.t_product_sku b
        SET a.cover = %s,
         b.sku_cover = %s,
         b.sku_images = %s,
         b.remark = 'crawler'
        WHERE
            a.product_id = b.product_id
        AND a.product_id = %s
        """
        print("set product cover:", cover)
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (cover, cover, json.dumps(image_urls), product_id))
        self.connection.commit()


class BuyerRepository(Repository):
    def __init__(self):
        Repository.__init__(self, db="fashion_buyer")

    def create_picture(self, picture):
        sql = """
               INSERT INTO `fashion_buyer`.`t_picture` 
               (`picture_id`,`name`, `cover`, `cover_type`, `description`, `type`, `date`, `tags`, `image_urls`, `date_added`) 
               VALUES 
               (%(picture_id)s, %(picture_name)s, %(cover)s, '0', %(description)s , '3',now(), %(tags)s, %(image_urls)s, now());
               """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, picture)
            lastrowid = cursor.lastrowid
        self.connection.commit()
        return lastrowid

    def check_picture_source(self, picture):
        sql = """
        SELECT * FROM fashion_buyer.t_picture_source WHERE source_id=%s AND source_type=%s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (picture["source_id"], picture["source_type"]))
            return cursor.fetchone()

    def create_picture_source(self, picture):
        sql = """
        INSERT INTO `fashion_buyer`.`t_picture_source` 
        (`source_id`, `source_type`, `url`, `date_added`) 
        VALUES 
        (%(source_id)s, %(source_type)s, %(url)s, now());
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, picture)
            lastrowid = cursor.lastrowid
        self.connection.commit()
        return lastrowid

    def update_picture_source(self, picture):
        sql = """
        UPDATE `fashion_buyer`.`t_picture_source` 
        SET 
        `source_id`=%(source_id)s, 
        `source_type`=%(source_type)s, 
        `url`=%(url)s,  
        `date_modified`=now() WHERE (`picture_id`=%(picture_id)s);
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, picture)
        self.connection.commit()

    def update_picture(self, picture):
        print "update picture:", picture
        sql = """
        UPDATE `fashion_buyer`.`t_picture` SET 
        `name`=%(picture_name)s, 
        `cover`=%(cover)s, 
        `cover_type`='0', 
        `description`=%(description)s, 
        `type`='3', 
        `image_urls`=%(image_urls)s, 
        `date_modified`=now() 
        WHERE (`picture_id`=%(picture_id)s);
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, picture)
        self.connection.commit()

    def check_picture(self, picture):
        sql = """
        SELECT * FROM fashion_buyer.t_picture WHERE `picture_id` = %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, picture["picture_id"])
            return cursor.fetchone()

    def save_picture(self, picture):
        # FIXME: 应该创建picture_source 再创建picture,这样可以支持name相同多个图片来源
        picture_source = self.check_picture_source(picture)
        if picture_source:
            picture["picture_id"] = picture_source["picture_id"]
            self.update_picture_source(picture)
        else:
            picture["picture_id"] = self.create_picture_source(picture)

        if self.check_picture(picture):
            self.update_picture(picture)
        else:
            self.create_picture(picture)

    def get_picture_by_source(self, source_id, source_type):
        sql = """
        SELECT
            b.*
        FROM
            fashion_buyer.t_picture b,
            fashion_buyer.t_picture_source a
        WHERE
            a.picture_id = b.picture_id
        AND a.source_id = %s
        AND a.source_type = %s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (source_id, source_type))
            return cursor.fetchone()

    def add_picture_tags(self, source_id, source_type, tags):
        if not tags:
            return

        picture = self.get_picture_by_source(source_id, source_type)
        if not picture:
            print("picture source no found:", source_id, source_type)
            return

        exists_tags = set(json.loads(picture["tags"]) or [])
        new_tags = list(set(tags) | exists_tags)

        sql = """
        UPDATE fashion_buyer.t_picture SET tags=%s WHERE picture_id=%s
        """
        print("add tags for picture:", picture["picture_id"], new_tags)
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (json.dumps(new_tags).decode("unicode-escape"), picture["picture_id"]))
        self.connection.commit()


class TaskRepository(Repository):
    KEY_PICTURE_TASKS = "platform:picture:tasks"
    KEY_PRODUCT_TASKS = "platform:product:tasks"
    KEY_COVER_TASKS = "platform:cover:tasks"

    def __init__(self):
        Repository.__init__(self, db="spider")

    def get_picture_task_length(self):
        return task_scheduler.length(self.KEY_PICTURE_TASKS)

    def create_picture_tasks(self):
        task_length = self.get_picture_task_length()
        if task_length > 0:
            print ("no create tasks, has task in queue:", task_length)
            return

        sql = """
        SELECT url, source_id, source_type FROM fashion_buyer.t_picture_source WHERE date(date_added) = date(now())
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            product_sources = cursor.fetchall()

        for source in product_sources:
            task_scheduler.push(self.KEY_PICTURE_TASKS, json.dumps(source))

    def get_picture_task(self):
        picture_task = task_scheduler.pop(self.KEY_PICTURE_TASKS)
        return json.loads(picture_task) if picture_task else None

    def get_product_task_length(self):
        return task_scheduler.length(self.KEY_PRODUCT_TASKS)

    def set_product_task_status(self, product_id, task_status, cover_url):
        sql = """
        UPDATE spider.t_product_task SET `status`=%s, cover_url=%s WHERE product_id=%s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (task_status, cover_url, product_id))
        self.connection.commit()

    def create_product_tasks(self):
        task_length = self.get_product_task_length()
        if task_length > 0:
            print ("no create tasks, has task in queue:", task_length)
            return

        sql = """
        SELECT
            b.*, c.source_type,
            c.source_id
        FROM
            spider.t_product_task a,
            fashion_product.t_product b,
            spider.t_product_source c
        WHERE
            a.product_id = b.product_id
        AND c.product_id = a.product_id
        AND a.`status` = 0
        """

        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            download_tasks = cursor.fetchall()

        for product_task in download_tasks:
            print("create product task:", product_task)
            task_scheduler.push(self.KEY_PRODUCT_TASKS, json.dumps(product_task))

    def get_product_task(self):
        product_task = task_scheduler.pop(self.KEY_PRODUCT_TASKS)
        return json.loads(product_task) if product_task else None

    def add_ftp_cover_task(self, cover_task):
        task_scheduler.push(self.KEY_COVER_TASKS, json.dumps(cover_task))

    def get_ftp_cover_task(self):
        cover_task = task_scheduler.pop(self.KEY_COVER_TASKS)
        return json.loads(cover_task) if cover_task else None


class CatalogRepository(Repository):
    def __init__(self):
        Repository.__init__(self, db="spider")

    def check_catalog(self, catalog):
        sql = "SELECT * FROM t_catalog WHERE url=%s"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, catalog["url"])
            return cursor.fetchone()

    def update_catalog(self, catalog):
        print "update catalog[%s]:" % catalog["product_name"], catalog["url"]
        sql = """
        UPDATE `spider`.`t_catalog` SET 
        `url`=%(url)s, 
        `name`=%(product_name)s, 
        `source_type`=%(source_type)s, 
        `source_id`=%(source_id)s, 
        `thumbnail`=%(thumbnail)s, 
        `language_id`=%(language_id)s, 
        `context`=%(catalog_context)s, `date_modified`=now() 
        WHERE (`catalog_id`=%(catalog_id)s)
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, catalog)
        self.connection.commit()

    def create_catalog(self, catalog):
        print "create catalog[%s]:" % catalog["product_name"], catalog["url"]
        sql = """
        INSERT INTO `spider`.`t_catalog` 
        (`url`, `name`, `source_type`, `source_id`,`language_id`, `thumbnail`, `status`, `context`, `date_added`) 
        VALUES 
        (%(url)s,%(product_name)s,%(source_type)s,%(source_id)s,%(language_id)s,%(thumbnail)s,%(catalog_status)s,%(catalog_context)s,now());
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, catalog)
        self.connection.commit()

    def save_catalog(self, catalog):
        exists_catalog = self.check_catalog(catalog)
        if exists_catalog:
            catalog["catalog_id"] = exists_catalog["catalog_id"]
            self.update_catalog(catalog)
        else:
            self.create_catalog(catalog)

    def set_catalog_status(self, catalog, status):
        sql = """
        UPDATE t_catalog SET status=%s WHERE url=%s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (status, catalog["url"]))
        self.connection.commit()

    def save_product_color(self, color):
        if self.get_product_color(color["color_code"], 1):
            return

        sql = """
        INSERT INTO `spider`.`t_color` 
        (`color_code`, `source_type`, `name`, `description`, `date_added`) 
        VALUES 
        (%(color_code)s, %(source_type)s, %(color_name)s, %(description)s, now());
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, color)
        self.connection.commit()

    def get_product_color(self, color_code, source_type):
        sql = """
        SELECT * FROM spider.t_color WHERE color_code=%s AND source_type=%s
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (color_code, source_type))
            return cursor.fetchone()


class Dao:
    def __init__(self):
        self.catalog = None
        self.create_repositories()

    def create_repositories(self):
        self.catalog = CatalogRepository()
        self.platform = PlatformRepository()
        self.task = TaskRepository()

    def reset(self):
        self.create_repositories()


dao = Dao()
