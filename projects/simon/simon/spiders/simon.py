import scrapy, logging
import html2text, datetime, requests, json
from scrapy.crawler import CrawlerProcess

class QuotesSpider(scrapy.Spider):
    name = "simon"
    
    def __init__(self):
        self.default_month_format = {
            "January": 1,
            "February": 2,
            "March": 3,
            "April": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11,
            "December": 12
        }
        logging.getLogger('protego').setLevel(logging.WARNING)
        logging.getLogger('scrapy.statscollectors').setLevel(logging.WARNING)

    def start_requests(self):
        urls = [
            'https://ielts-simon.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        beta_inner = response.xpath('//*[@id="beta"]')
        general_info = self.extract_general_info(beta_inner)
        list_of_newer_date = []
        
        for i in general_info:
            date_converted = self.date_converter(i['date'])
            if self.a_newer_date(date_converted) == True:

                list_of_newer_date.append(date_converted)
                modified_data = self.modified_data(i)
                self.slack_send(modified_data)

        self.note_the_newest_day(list_of_newer_date)

    def extract_general_info(self, data):
        final_result = []
        date_header = data.xpath("//h2[@class='date-header']")
        for a_date in date_header:
            a_date_text = a_date.xpath("text()").extract()[0]
            entry_parent = a_date.xpath('following-sibling::div')[0]
            entry_content = entry_parent.xpath(".//div[@class='entry-body']")
            entry_content_text = html2text.html2text(entry_content[0].extract())
            entry_header = entry_parent.xpath(".//h3[@class='entry-header']")
            entry_header_href = entry_header.xpath("./a//@href").getall()[0]
            entry_header_text = entry_header.xpath("./a/text()").getall()[0]
            
            final_result.append(
                {
                    'date': f"{a_date_text}",
                    'content': f"{entry_content_text}",
                    'link': f"{entry_header_href}",
                    'header': f"{entry_header_text}"
                }
            )
        return final_result

    def a_newer_date(self, data):
        saved_date = open('../the_day', 'r').read().strip().split("-")
        '''
            data writen in the 'the_day' file is like '2019-11-16'
        '''
        the_day = datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(saved_date[2]))
        if the_day < data:            
            return True
            
    def note_the_newest_day(self, data):
        if data != []:
            the_day = data[0]
            for i in data:
                if the_day < i:
                    the_day = i
            
            with open("../the_day", "w") as f:
                f.write(datetime.datetime.strftime(the_day, "%Y-%m-%d"))
        else:
            pass

    def slack_send(self, data):
        slack_url = "https://hooks.slack.com/services/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"
        headers = {'Content-type': 'application/json'}
        try:
            act = requests.post(
                slack_url,
                data=json.dumps(data),
                headers=headers)
        except act.exceptions.HTTPError as e:
            print(e)

    def modified_data(self, data):
        output = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "<{link}|{header}> - *{date}*\n```{content}```".format(
                            link=data['link'],
                            header=data['header'],
                            date=data['date'],
                            content=data['content'])
                    }
                }
            ]
        }
        return output
    
    def date_converter(self, data_in_string):
        result = data_in_string.split(",")
        year = int(result[2])
        month_name = result[1].split(" ")[1]
        day_number = int(result[1].split(" ")[2])
        month_number = int(self.default_month_format[month_name])
        
        return datetime.datetime(year, month_number, day_number)


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(QuotesSpider)
    process.start() # the script will block here until the crawling is finished