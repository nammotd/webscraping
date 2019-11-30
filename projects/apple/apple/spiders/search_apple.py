# -*- coding: utf-8 -*-
import scrapy, logging, re
from scrapy_selenium import SeleniumRequest
from scrapy import Request

class SearchAppleSpider(scrapy.Spider):
    name = 'search_apple'
    logging.getLogger('protego').setLevel(logging.WARNING)
    logging.getLogger('scrapy.statscollectors').setLevel(logging.WARNING)
    logging.getLogger('scrapy.middleware').propagate = False

    def start_requests(self):
        bach_hoa_xanh_urls = [
            'https://www.bachhoaxanh.com/trai-cay'
        ]
        for url in bach_hoa_xanh_urls:
            yield scrapy.Request(url=url, callback=self.bach_hoa_xanh)
        
        vinmart_urls = [
            #"https://vinmart.com/account/set-location/HCM?url=/"
            "https://vinmart.com/search/?q=T%C3%A1o&page=1",
            "https://vinmart.com/search/?q=T%C3%A1o&page=2"
        ]
        for url in vinmart_urls:
            # yield SeleniumRequest(url=url, cookies={'csrftoken':'8mNDiaNb6PKgQSBmMZd2l3nkB2bHi8OxXOVUISSdmqdaBm6AShummCPJnMpk3oNc',
            # 'location':'HCM:1iaKZh:_HQPcs_HTiQFTSKq7Od_0XSASyc'}, callback=self.vinmart)
            yield scrapy.Request(url=url, cookies={'csrftoken':'8mNDiaNb6PKgQSBmMZd2l3nkB2bHi8OxXOVUISSdmqdaBm6AShummCPJnMpk3oNc',
            'location':'HCM:1iaKZh:_HQPcs_HTiQFTSKq7Od_0XSASyc'}, callback=self.vinmart)

    def bach_hoa_xanh(self, response):
        shop_name = "BachHoaXanh"
        for i in response.xpath("//a[starts-with(@href, '/trai-cay/')]"):
            name = i.xpath("./div[@class='product-name']/text()").extract()[0]
            price = i.xpath("./div[@class='price']/strong/text()").extract()[0]
            if re.search("^Táo.*Gala $", name):
                yield {
                    'name': name,
                    'price': price
                }

    def vinmart(self, response):
        shop_name = "Vinmart"
        location = response.xpath("//span[@class='d-none d-sm-inline-block text-body']/text()").extract()
        if location != 'Tp.HCM':
            for i in response.xpath("//form[@id='product-form']"):
                product_name = i.xpath(".//a[contains(@href, '/products/')]/@title").get()
                produce_price = i.xpath(".//span[@class='h5 text-danger font-weight-bold']/text()").get().strip()
                #if product_name.split(" ")[0] == "Táo":
                if re.search("^Táo Gala", product_name):
                    yield {
                        'name': product_name,
                        'price': produce_price
                    }
        else:
            print("Website location is {}, because of CSRFToken is expired".format(location))
