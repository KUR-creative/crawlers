#-*- coding: utf-8 -*-
import base
from fp import cmap, pipe, cfilter

def list_stem(kind, board_id):
    return 'http://bbs.ruliweb.com/%s/board/%s/list' \
            % (kind, str(board_id))
def article_stem(kind, board_id, article_id):
    return 'http://bbs.ruliweb.com/%s/board/%s/read/%s' \
            % (kind, str(board_id), str(article_id))
RULI_COMMENT_STEM = 'https://api.ruliweb.com/commentView' 

def article_id_list(url_stem, page_no):
    all_tr = lambda html:html.find_all('tr',class_='table_body')
    is_not_notice = lambda tag:'notice' not in tag['class']
    get_id = lambda tag:tag.find('td', class_='id').text.strip()
    return base.article_no_list(
        url_stem,
        {'page':str(page_no)},
        pipe(all_tr,
             cfilter(is_not_notice),
             cmap(get_id),
             list)
    )

def article_html_url(kind, board_id, article_id):
    return base.article_html_url(
        article_stem(kind, board_id, article_id), None)

def comment_pages(article_html, article_url,
                  board_id, article_id, cmtimg=0):
    headers = {
        'Referer':article_url, 
    }
    data = {
        'page':'1',
        'board_id':str(board_id),
        'article_id':str(article_id),
        'cmtimg':'0' # 0: no image / 1: view image
    }

    def continue_condition(page_dict):
        page_no = page_dict['page_info']['current_page']
        max_page_no = page_dict['page_info']['end_page']
        return page_no <= max_page_no

    return list(base.post_comment_pages_seq(
        RULI_COMMENT_STEM, headers, data, 'page',
        continue_condition,
        page2yield = lambda page_dict:page_dict['view'])
    )

#li = article_id_list(list_stem('ps',300421), 3))

#print(article_id_list(list_stem('ps',300421), 3))
#print(len(article_id_list(list_stem('ps',300421), 3)))

#html,url = article_html_url('ps', 300421, 30828285)
#print(html,url)


html,url = article_html_url('hobby', 300143, 39599965)
li = comment_pages(html, url, 300143, 39599965)
print(li)
print('len:', len(li))
