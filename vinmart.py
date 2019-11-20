import requests, re, json
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as BS
old_URL = "https://vinmart.com/products/collection/khuyen-mai-hom-nay-1/?sort_by=-updated_at"
URL = "https://vinmart.com/products/uc-ga-cong-nghiep-phi-le-khong-da-binh-minh-5241/i"
new_URL = "https://vinmart.com/products/category/thit-thuy-hai-san-1-4893/?category_ids=4894"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"}

slack_webhook_url = "https://hooks.slack.com/services/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"

def extract_html(url):
    page = requests.get(url, headers=headers)
    soup = BS(page.content, "html.parser")
    return soup

def Slack_send(url, data):
    headers = {'Content-type': 'application/json'}
    try:
        act = requests.post(
            url,
            data=json.dumps(data),
            headers=headers)
    except requests.exceptions.HTTPError as e:
        print(e)
    #return act.status_code 

def get_the_price(soup):
    for i in soup.find_all("a", class_="product-name text-body text-hover-primary small font-weight-medium mb-1"):
        #if i.get("href") == "/products/uc-ga-cong-nghiep-phi-le-khong-da-binh-minh-5241/"
        # if i.get("href") == "/products/gau-bo-3845/":
        #     price_entry = i.find_next_sibling("span")
        #     print(price_entry)
        print(i.get("href"))
    #print(price.get("data-product-price"))
    
if __name__ == '__main__':    
    get_the_price(extract_html(new_URL))

