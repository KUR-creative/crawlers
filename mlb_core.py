#-*- coding: utf-8 -*-
import base
from fp import cmap, pipe, cfilter

MLB_LIST_STEM = 'http://mlbpark.donga.com/mp/b.php'

def article_url_list(board_name, page_no):
    html2urls = \
        pipe(lambda html:html.find('table', class_='tbl_type01')
                             .find_all('tr'),
             cfilter(lambda tag:tag.find('td').text.isdigit()),
             cmap(lambda tag:tag.find('a')['href']),
             list)
        
    return base.article_no_list(
        MLB_LIST_STEM,
        {'p':(int(page_no) - 1)*30 + 1,
         'b':board_name, 
         'm':'list'},
        html2urls
    )

def article_comments_html(article_url):
    return base.article_html_url(article_url, None)[0]

#print(article_url_list('mlbtown', 2))
#print(len(article_url_list('mlbtown', 2)))

li = article_url_list('mlbtown', 2)
print(article_comments_html(li[2]))
print(article_comments_html(li[2]).find('div',class_='reply_list'))
