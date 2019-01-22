#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import base
from base import is_not_empty 
from fp import cmap, pipe, cfilter

PPOM_LIST_STEM = 'http://www.ppomppu.co.kr/zboard/zboard.php'
PPOM_ARTICLE_STEM = 'http://www.ppomppu.co.kr/zboard/view.php'
PPOM_COMMENT_STEM = 'http://www.ppomppu.co.kr/zboard/list2_comment.php'

def article_no_list(board_name, page_no, category=''):
    html2no_list = \
        pipe(lambda html:
                 html.find_all('td', class_='eng list_vspace'),
             list)
    return base.article_no_list(
        PPOM_LIST_STEM, 
        {'id':board_name, 'page':str(page_no), 'category':str(category)},
        pipe(lambda html:
                 html.find_all('td', class_='eng list_vspace'),
             cfilter(lambda tag:tag.get('nowrap') == None),
             cfilter(lambda tag:tag.text.isdigit()),
             cmap(lambda tag:tag.text),
             list)
    )

def article_html_url(board_name, article_no):
    return base.article_html_url(
        PPOM_ARTICLE_STEM, {'id':board_name, 'no':article_no}
    )

def comment_pages(article_html, article_url, 
                  board_name, article_no):
    def continue_condition(comment_page):
        soup = BeautifulSoup(comment_page, 'html.parser')
        return is_not_empty(
            soup.find_all('div', class_='comment_wrapper')
        )

    headers = {'Referer':article_url}
    params = {
        'id':board_name,
        'no':article_no,
        'c_page':'1',
        'comment_mode':''
    }

    return list(base.get_comment_pages_seq(
        PPOM_COMMENT_STEM, headers, params, 'c_page',
        continue_condition)
    )

#print(*article_no_list('humor', 1), sep='\n')
#print(len(article_no_list('humor', 1)))

html,url = article_html_url('humor', 326422)
html,url = article_html_url('humor', 306679)
#print(html,url)

#print(len(comment_pages(PPOM_COMMENT_STEM, url, 'ppomppu', '306012')))
#expted 4
#print(len(comment_pages(PPOM_COMMENT_STEM, url, 'freeboard', 6229954)))
#expted 16
print(html)
