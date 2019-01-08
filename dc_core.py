#-*- coding: utf-8 -*-
import base
from fp import cmap, pipe, cfilter

# stem: url without query
DC_LIST_STEM = 'http://gall.dcinside.com/board/lists'
DC_ARTICLE_STEM = 'http://gall.dcinside.com/board/view'
DC_COMMENT_STEM = 'http://gall.dcinside.com/board/comment'

def article_no_list(gall_id, page_no):
    html2no_list = \
        pipe(lambda html:html.find_all('td', class_='gall_num'),
             cfilter(lambda tag:tag.text != '공지'), 
             cmap(lambda tag:tag.text),
             list)
    return base.article_no_list(
        DC_LIST_STEM, 
        {'id':gall_id, 'page':str(page_no)},
        html2no_list
    )

def article_html_url(gall_id, article_no):
    return base.article_html_url(
        DC_ARTICLE_STEM, {'id':gall_id, 'no':article_no}
    )

def comment_pages(article_html, article_url, gall_id, article_no):
    # comment page type: json
    # return [comment_page1_json, comment_page2_json ...]
    headers = {
        'Referer':article_url, 
        'X-Requested-With':'XMLHttpRequest'
    }
    data = {
        'comment_page':'1',
        'id':'hit',
        'no':'14949',
        'cmt_id':'hit',
        'cmt_no':'14949',
        'e_s_n_o':article_html.find('input',{'id':'e_s_n_o'})['value'],
        'sort':'D' # 등록순
    }

    return list(base.post_comment_pages_seq(
        DC_COMMENT_STEM, headers, data, 'comment_page',
        lambda comment_dict:comment_dict['comments'])
    )


    '''
    def comment_dict_seq(headers, data):
        cmt_page = 1
        while True:
            data['comment_page'] = str(cmt_page)
            resp = requests.post(DC_COMMENT_STEM, 
                                 headers=headers, data=data)
            resp.raise_for_status() 
            comment_dict = resp.json()
            if comment_dict['comments']:
                cmt_page += 1
                yield comment_dict 
            else:
                break
    return list(comment_dict_seq(headers, data))
    '''


'''
article_no_li = article_no_list('programming', 1)
print(article_no_li, type(article_no_li[0]))

html,url = article_html_url('programming', article_no_li[4])
print(html, url)
'''
html,url = article_html_url('hit', 14933)
cmt_dicts = comment_pages(html, url, 'hit', 14933)
print(cmt_dicts)
print(len(cmt_dicts))
