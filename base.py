import requests
from bs4 import BeautifulSoup

def article_no_list(url_stem, params, html2no_list):
    resp = requests.get(url_stem, params)
    resp.raise_for_status() 
    soup = BeautifulSoup(resp.text, 'html.parser')
    #print('wtf:',resp.url)
    return html2no_list(soup)

def article_html_url(url_stem, params):
    resp = requests.get(url_stem, params)
    resp.raise_for_status() # 200 OK otherwise error occur 
    return BeautifulSoup(resp.text,'html.parser'), resp.url

def post_comment_pages_seq(
        url_stem, headers, data, page_no_key,
        continue_condition, 
        response2page = lambda resp:resp.json(),
        page2yield = lambda x:x,
        init_page_no=1):
    cmt_page_no = init_page_no
    while True:
        #print(cmt_page_no)
        data[page_no_key] = str(cmt_page_no)
        resp = requests.post(url_stem, 
                             headers=headers, data=data)
        resp.raise_for_status()
        comment_page = response2page(resp)
        if continue_condition(comment_page):
            cmt_page_no += 1
            yield page2yield(comment_page)
        else:
            break
