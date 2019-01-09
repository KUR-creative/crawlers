#-*- coding: utf-8 -*-
import base
from fp import cmap, pipe, cfilter

PPOM_LIST_STEM = 'http://www.ppomppu.co.kr/zboard/zboard.php'
PPOM_ARTICLE_STEM = 'http://www.ppomppu.co.kr/zboard/view.php'

def article_no_list(board_name, page_no, category=''):
    html2no_list = \
        pipe(lambda html:
                 html.find_all('td', class_='eng list_vspace'),
             #cfilter(lambda tag:tag['.
             list)
    return base.article_no_list(
        PPOM_LIST_STEM, 
        {'id':board_name, 'page':str(page_no), 'category':str(category)},
         #lambda html: html.find('table', id='revolution_main_table')
        pipe(lambda html:
                 html.find_all('td', class_='eng list_vspace'),
             cfilter(lambda tag:tag.get('nowrap') == None),
             cfilter(lambda tag:tag.text.isdigit()),
             cmap(lambda tag:tag.text),
             list)
        #lambda x:x
    )

def article_html_url(board_name, article_no):
    return base.article_html_url(
        PPOM_ARTICLE_STEM, {'id':board_name, 'no':article_no}
    )

print(*article_no_list('humor', 1), sep='\n')
print(len(article_no_list('humor', 1)))

html,url = article_html_url('humor', 326422)
print(html,url)

