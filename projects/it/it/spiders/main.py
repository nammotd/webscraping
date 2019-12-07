# -*- coding: utf-8 -*-
import scrapy, logging, requests, json, os
from scrapy.crawler import CrawlerProcess
from itviec.logic import *
import slack_utils
import common_utils

"""
export IT_VIEC_SLACK_WEBHOOK_URL='https://hooks.slack.com/services/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'
"""

class LkSpider(scrapy.Spider):
    name = 'it'
    logging.getLogger('protego').setLevel(logging.WARNING)
    logging.getLogger('scrapy.statscollectors').propagate = False
    logging.getLogger('scrapy.middleware').propagate = False
    def __init__(self):
        self.base_url = "https://itviec.com"
        self.base_job_url = "https://itviec.com/it-jobs/"

    def start_requests(self):
        #url = "https://itviec.com/it-jobs"
        url = "https://itviec.com/it-jobs/devops/ho-chi-minh-hcm"

        yield scrapy.Request(url=url, callback=self.main_flow)

    def main_flow(self, response):
        all_current_post = extract_all_jobs_href(response)
        for href in all_current_post:
            data_check_and_import = insert_data([f"{href}"])
            if data_check_and_import == "existed, ignored":
                pass
            elif data_check_and_import == "not existed, imported":
                scrapy.Request(
                    url="{}{}.html".format(self.base_job_url, href),
                    callback=extract_all_jobs_href
                )

    def extract_it_viec(self, response):

        job_title = response.xpath("//h1[@class='job_title']/text()").get().strip()
        company_name = response.xpath("//h3[@class='name']/a/text()").get().strip()
        job_description = response.xpath("//div[@class='job_description']").get()
        skill_requirements = response.xpath("//div[@class='skills_experience']").get()

        raw_text_skill_requirements = convert_html_to_text(skill_requirements)
        raw_text_job_description = convert_html_to_text(job_description)

        full_job_details = "{desc}{skill}".format(
            desc = raw_text_job_description,
            skill = raw_text_skill_requirements
        )
        
        job_data = {
            'job_title': job_title,
            'company_name': company_name,
            'job_details': full_job_details,
            'link': response.url
        }
        modified_job_data = slack_data_modified(job_data)
        slack_send(modified_job_data)

if __name__ == "__main__":
#def run():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(LkSpider)
    process.start() # the script will block here until the crawling is finished