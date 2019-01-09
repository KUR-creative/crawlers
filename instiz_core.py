#-*- coding: utf-8 -*-
import base
from fp import cmap, pipe, cfilter

INSTIZ_LIST_STEM = 'https://www.instiz.net/bbs/list.php'

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

print(*article_no_list('fan', 1, 1), sep='\n')
#print(article_no_list('fan', 1, 1)[0])
print( len(article_no_list('fan', 1, 1)) )


