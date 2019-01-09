#-*- coding: utf-8 -*-
import base
from fp import cmap, pipe, cfilter

INSTIZ_LIST_STEM = 'https://www.instiz.net/bbs/list.php'
def article_stem(board_name):
    return 'https://www.instiz.net/%s' % str(board_name)

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
             #lambda x:x)
    )

def article_html_url(board_name, article_no):
    return base.article_html_url(
        PPOM_ARTICLE_STEM, {'id':board_name, 'no':article_no}
    )

print(*article_no_list('fan', 1, 1), sep='\n')
print( len(article_no_list('fan', 1, 1)) )

print(article_stem('free'))

