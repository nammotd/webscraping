import requests, re, json
import matplotlib.pyplot as plt
import html2text
import datetime
from bs4 import BeautifulSoup as BS

URL = "https://ielts-simon.com/ielts-help-and-english-pr/ielts-writing-task-2"
vocab_grammar_url = "https://ielts-simon.com/ielts-help-and-english-pr/mistakesgrammar/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"}
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

def main_page(soup):
    result = []
    for i in soup.find_all("h3", class_="entry-header"):
        if re.search("IELTS Vocabulary", i.a.text):
            result.append({"header": f"{i.a.text}", "link": f"{i.a['href']}"})
    # This returns a list of url               
    return result
    
def get_the_vocabulary(soup):
    for entry in soup.find_all("div", class_="entry-inner"):
        h3_header_a_tag_content = entry.h3.a.text
        h3_header_a_tag_href = entry.h3.a['href']
        if re.search("IELTS Vocabulary", h3_header_a_tag_content):
            link = h3_header_a_tag_href
            header = h3_header_a_tag_content
            content = []
            for i in entry.div.div.ul.find_all("li"):
                content.append(f"- {i.text}")
        
    modified_content = "\n".join(content)
    output = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{link}|{header}>\n```{modified_content}```"
                    }
                }
            ]
        }

    return output

def get_header_date(soup):
    default_month_format = {
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

    saved_date = open('the_day', 'r').read().strip().split("-")
    '''
        data writen in the 'the_day' file is like '2019-11-16'
    '''
    the_day = datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(saved_date[2]))
    final_result = []
    self_comparing = []
    for date_entry in soup.find_all(class_="date-header"):
        """
            date_entry returns 'Saturday, November 16, 2019' 
        """
        result = date_entry.text.split(",")
        #day_name = result[0]
        year = int(result[2])
        month_name = result[1].split(" ")[1]
        day_number = int(result[1].split(" ")[2])
        month_number = int(default_month_format[month_name])
        if the_day < datetime.datetime(year, month_number, day_number):            
            # print(year, month_number, day_number)
            # print(content_header)
            self_comparing.append([year, month_number, day_number])
            final_result.append(date_entry)
    if self_comparing != []:
        the_day = datetime.datetime(int(self_comparing[0][0]), int(self_comparing[0][1]), int(self_comparing[0][2]))
        the_day_write_down = f"{int(self_comparing[0][0])}-{int(self_comparing[0][1])}-{int(self_comparing[0][2])}"        
        for a in self_comparing:
            if datetime.datetime(int(a[0]), int(a[1]), int(a[2])) > the_day:
                the_day = a
                the_day_write_down = f"{int(a[0])}-{int(a[1])}-{int(a[2])}"
        with open("the_day", "w") as f:
            f.write(the_day_write_down)

    return final_result

def get_entry_content(soup):
    '''
    <div class="entry-inner">		
		<h3 class="entry-header">
		<a href="https://ielts-simon.com/ielts-help-and-english-pr/2019/11/ielts-grammar-clause-lists.html">IELTS Grammar: clause lists</a></h3>
		<div class="entry-content">
        <div class="entry-body">
            <p>A student asked me about the following type of sentence:</p>
            <p><em>It was a lovely day, the children were playing happily, and everyone was enjoying the party.</em></p>
            <p>Can we put three independent clauses together in a 'list' like this? The answer is yes. This is a normal sentence structure in English. Maybe you could try writing an IELTS-style sentence in the same way.</p>
        </div>
	</div>
    '''
    content_parent = soup.find_next_sibling("div")
    date = soup.text
    entry_body = content_parent.find("div", class_="entry-body")
    entry_info = content_parent.find("h3", class_="entry-header")

    modified_content = html2text.html2text(entry_body.prettify())
    link = entry_info.a.get('href')
    header = entry_info.text.strip()
    output = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{link}|{header}> - *{date}*\n```{modified_content}```"
                    }
                }
            ]
        }
    return output

    
if __name__ == '__main__':
    #Slack_send(slack_webhook_url, get_the_vocabulary(extract_html(URL)))
    for newer in get_header_date(extract_html(vocab_grammar_url)):
        Slack_send(slack_webhook_url, get_entry_content(newer))

