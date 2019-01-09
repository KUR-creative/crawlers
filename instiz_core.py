#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

import base
from fp import cmap, pipe, cfilter

INSTIZ_LIST_STEM = 'https://www.instiz.net/bbs/list.php'
def article_stem(board_name):
    return 'https://www.instiz.net/%s' % str(board_name)
INSTIZ_COMMENT_STEM = 'https://www.instiz.net/bbs/view_comment.php'

def article_no_list(board_name, page_no, category):
    return base.article_no_list(
        INSTIZ_LIST_STEM,
        {'id':board_name, 
         'page':str(page_no), 'category':str(category)},
        pipe(lambda html:html.find_all('td', class_='listno'),
             cmap(lambda tag:tag.find('a')),
             cfilter(lambda x:x is not None),
             cmap(lambda a:a.text),
             list)
    )

def article_html_url(board_name, article_no):
    return base.article_html_url(
        article_stem(board_name), {'no':article_no}
    )

def all_comments_html(board_name, article_no):
    params = { 'id': board_name, 'no': str(article_no)}

    resp = requests.post(INSTIZ_COMMENT_STEM, params=params)
    resp.raise_for_status()
    html = BeautifulSoup(resp.text, 'html.parser')
    return html

'''
print(*article_no_list('fan', 1, 1), sep='\n')
print( len(article_no_list('fan', 1, 1)) )

print(article_stem('free'))

html,url = article_html_url('name', 29866852)
print(html, url)
'''

#def comment_html2comment_list(comment_html):
def view_comments(comment_html):
    gen = \
    pipe(lambda html:
             html.find_all('div', class_='comment_line'),
         cmap(lambda tag:tag.find('span')),
         cfilter(lambda x:x is not None),
         cmap(lambda span:span.text),
         enumerate,
         cmap(lambda s:'[%d] %s \n' % s))
    print(*gen(comment_html))

html = all_comments_html('name', 29866852)
view_comments(html)
