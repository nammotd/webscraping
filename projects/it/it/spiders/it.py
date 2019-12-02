# -*- coding: utf-8 -*-
import scrapy, logging, html2text, requests, json, os


class LkSpider(scrapy.Spider):
    name = 'it'
    logging.getLogger('protego').setLevel(logging.WARNING)
    logging.getLogger('scrapy.statscollectors').propagate = False
    logging.getLogger('scrapy.middleware').propagate = False
    def __init__(self):
        self.base_url = "https://itviec.com"

    def start_requests(self):
        #url = "https://itviec.com/it-jobs"
        url = "https://itviec.com/it-jobs/devops/ho-chi-minh-hcm"

        yield scrapy.Request(url=url, callback=self.main_flow)

    def main_flow(self, response):
        # job_data = self.extract_job_details(response)
        # modified_job_data = self.slack_data_modified(job_data)
        # self.slack_send(modified_job_data)
        self.compare_date(response)

    def extract_job_href(self, response):
        result = []
        for i in response.xpath("//a[@target='_blank'][@data-controller='utm-tracking'][contains(@href, '/it-jobs/')]"):
            job_link = i.xpath("./@href").get()
            job_details = job_link.split("/")[2]
            result.append(job_link)
        
        yield scrapy.Request(
            url=f"{self.base_url}{result[0]}", 
            callback=self.main_flow
            )

    def extract_job_details(self, response):
        job_title = response.xpath("//h1[@class='job_title']/text()").get().strip()
        company_name = response.xpath("//h3[@class='name']/a/text()").get().strip()
        job_description = response.xpath("//div[@class='job_description']").get()
        skill_requirements = response.xpath("//div[@class='skills_experience']").get()

        raw_text_skill_requirements = self.convert_html_to_text(skill_requirements)
        raw_text_job_description = self.convert_html_to_text(job_description)

        full_job_details = "{desc}{skill}".format(
            desc = raw_text_job_description,
            skill = raw_text_skill_requirements
        )
        
        return {
            'job_title': job_title,
            'company_name': company_name,
            'job_details': full_job_details,
            'link': response.url
        }
        
    def slack_data_modified(self, data):
        output = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*{job_title}* - *{company_name}* - <{link}|link>\n```{job_details}```".format(
                            job_title=data['job_title'],
                            company_name=data['company_name'],
                            job_details=data['job_details'],
                            link=data['link'])
                    }
                }
            ]
        }
        return output
    
    def slack_send(self, data):
        slack_url = os.environ['IT_VIEC_SLACK_WEBHOOK_URL']
        headers = {'Content-type': 'application/json'}
        try:
            act = requests.post(
                slack_url,
                data=json.dumps(data),
                headers=headers)
        except act.exceptions.HTTPError as e:
            print(e)
            
    def convert_html_to_text(self, response):
        return html2text.html2text(response)

    def compare_date(self, response):
        a = response.xpath("//span[@class='distance-time']")
        for i in a:
            print(i.xpath("./text()").get().strip())