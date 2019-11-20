import requests, re, json
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as BS
URL = "https://www.cicnews.com"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"}
slack_webhook_url = "https://hooks.slack.com/services/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"

def extract_html(url):
    page = requests.get(url, headers=headers)
    soup = BS(page.content, "html.parser")
    return soup

def main_page(soup):
    glues = ["inviting", "invitations", "crs", "issues"]
    list_of_url = []
    
    for i in soup.find_all(class_="entry-title-link"):
        for need in glues:
            if re.search(need, i['href']):
                list_of_url.append(i['href'])

    # This returns a list of url               
    return list(dict.fromkeys(list_of_url))

def invitation_page():
    u2 = "https://www.cicnews.com/2019/11/new-express-entry-draw-invites-3600-candidates-to-apply-for-canadian-permanent-residence-2-1113167.html"
    page2 = requests.get(u2, headers=headers)
    soup = BS(page2.content, "html.parser")
    for i in soup.find_all("img"):
        #print(i['src']
        plt.figure()
        plt.imshow(i['src'])
        plt.show()
        
def Slack_send(url, content):
    headers = {'Content-type': 'application/json'}
    data = {'text': f"{content}"}
    try:
        act = requests.post(
            url,
            data=json.dumps(data),
            headers=headers)
    except requests.exceptions.HTTPError as e:
        print(e)
    #return act.status_code 

for i in main_page(extract_html(URL)):
    content = i.split("/")[-1].split(".")[0]
    Slack_send(slack_webhook_url, f"<{i}|{content}>")
            
         
