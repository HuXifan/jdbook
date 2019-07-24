# -*- coding: utf-8 -*-

import pymysql


class BookPipeline(object):

    def open_spider(self, spider):
        self.client = pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='Root1',
            db='jdbook',
            charset='utf8'
        )

    def process_item(self, item, spider):
        print(item)
        self.client.cursor().execute(
            "insert into jdbook (b_cate, s_cate, book_img, book_name, book_author, book_press, book_publish_date, book_price) values (%s, %s, %s, %s, %s, %s, %s, %s)",

            (item["b_cate"], item["s_cate"], item["book_img"], item["book_name"],
             item["book_author"][0], item["book_press"], item['book_publish_date'], item["book_price"]))
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.client.close()
