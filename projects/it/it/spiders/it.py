# -*- coding: utf-8 -*-
import scrapy, logging


class LkSpider(scrapy.Spider):
    name = 'it'
    logging.getLogger('protego').setLevel(logging.WARNING)
    logging.getLogger('scrapy.statscollectors').propagate = False
    logging.getLogger('scrapy.middleware').propagate = False
    def __init__(self):
        self.base_url = "https://itviec.com"

    def start_requests(self):
        url = "https://itviec.com/it-jobs"

        yield scrapy.Request(url=url, callback=self.extract_job_href)
    
    def extract_job_href(self, response):
        result = []
        for i in response.xpath("//a[@target='_blank'][@data-controller='utm-tracking'][contains(@href, '/it-jobs/')]"):
            job_link = i.xpath("./@href").get()
            job_details = job_link.split("/")[2]
            result.append(job_details)
            # yield scrapy.Request(
            #     url="{}{}".format(self.base_url, job_link), 
            #     callback=self.extract_content
            #     )
        return result
            
            
    
    
