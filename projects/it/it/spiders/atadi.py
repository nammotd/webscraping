# -*- coding: utf-8 -*-
import scrapy, json, requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Origin': 'https://www.atadi.vn',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://www.atadi.vn/',
}
data = '{"startDate":"20191201","endDate":"20200930","minPrice":0,"maxPrice":900000,"providers":["VJ","BL","VN"],"routes":["SGNHUI","HUISGN"],"type":"month"}'

new_data = '{"startDate":"20200101","endDate":"20200131","minPrice":0,"maxPrice":900000,"providers":["VJ","BL","VN"],"routes":["SGNHUI"],"type":"date"}'

response = requests.post('https://www.atadi.vn/addon/prodash/getlist', headers=headers, data=new_data)
content = response.content.decode('utf-8')
for i in json.loads(content):
    print(json.dumps(i, sort_keys=True, indent=4))