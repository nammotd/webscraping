# -*- coding: utf-8 -*-
import scrapy


class CaSpider(scrapy.Spider):
    name = 'ca'
    allowed_domains = ['https://www.indeed.ca/jobs?q=devops+engineer&l=']
    start_urls = ['http://https://www.indeed.ca/jobs?q=devops+engineer&l=/']

    def parse(self, response):
        pass
