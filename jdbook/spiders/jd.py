# -*- coding: utf-8 -*-
import json
import scrapy
from copy import deepcopy


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', 'p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath("//div[@class='mc']/dl/dt")  # 大分类列表
        item = {}
        for dt in dt_list:
            item['b_cate'] = dt.xpath("./a/text()").extract_first()
            """extract():这个方法返回的是一个数组list，，里面包含了多个string，如果只有一个string，则返回['ABC']这样的形式。
extract_first()：这个方法返回的是一个string字符串，是list数组里面的第一个字符串。"""
            # following-sibling::div[1] 表示当前节点的兄弟节点中的 第 1 个 div标签
            em_list = dt.xpath("./following-sibling::dd[1]/em")  # em_list 小分类列表
            for em in em_list:
                item['s_href'] = em.xpath("./a/@href").extract_first()
                item['s_cate'] = em.xpath("./a/text()").extract_first()
                if item['s_href'] is not None:
                    item['s_href'] = "https:" + item['s_href']
                yield scrapy.Request(
                    item['s_href'],
                    callback=self.parse_book_list,
                    meta={'item': deepcopy(item)}
                )

    def parse_book_list(self, response):  # 解析列表页
        item = response.meta['item']  # 通过meta传回来
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:

            item['book_img'] = li.xpath(".//div[@class='p-img']/a/img/@src").extract_first()
            if item['book_img'] is None:
                item['book_img'] = li.xpath(".//div[@class='p-img']/a/img/@data-lazy-img").extract_first()
            item["book_img"] = "https:" + item['book_img'] if item['book_img'] is not None else None
            item['book_name'] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first().strip()
            item['book_author'] = li.xpath(".//span[@class='author_type_1']//a/text()").extract()
            item['book_press'] = li.xpath(".//span[@class='p-bi-store']/a/text()").extract_first()
            item['book_publish_date'] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first().strip()
            # item['book_sku'] = li.xpath("//div[@class='p-operate']/a/@data-sku").extract_first()  # 同下
            item['book_sku'] = li.xpath("./div/@data-sku").extract_first()
            yield scrapy.Request(  # 构造请求
                'https://p.3.cn/prices/mgets?skuIds=J_{}'.format(item['book_sku']),  # 完整的url
                callback=self.parse_book_price_json,
                meta={"item": deepcopy(item)}
            )
        # 列表页翻页
        next_url = response.xapth("//span/a[@class='p-next']/@href").extract_first()  # 不完整
        if next_url is not None:
            yield scrapy.Request(
                'https:' + next_url,
                callback=self.parse_book_list(),
                meta={"item": deepcopy(item)}
            )

    def parse_book_price_json(self, response):
        item = response.meta['item']  # 取meta
        # 取json数据 json.load
        item['book_price'] = json.loads(response.body.decode())[0]['op']
        item.pop('s_href')
        yield item
