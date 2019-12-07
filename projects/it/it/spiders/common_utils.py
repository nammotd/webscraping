import html2text

def convert_html_to_text(response):
    return html2text.html2text(response)
