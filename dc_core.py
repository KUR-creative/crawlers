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
    try:
        html,url = base.article_html_url(
            DC_ARTICLE_STEM, {'id':gall_id, 'no':article_no}
        )
    except Exception as e:
        html,url = 1,2
    finally:
        return html,url

def comment_pages(article_html, article_url, gall_id, article_no):
    # comment page type: json
    # return [comment_page1_json, comment_page2_json ...]
    headers = {
        'Referer':article_url, 
        'X-Requested-With':'XMLHttpRequest'
    }
    data = {
        'comment_page':'1',
        'id':str(gall_id),
        'no':str(article_no),
        'cmt_id':str(gall_id),
        'cmt_no':str(article_no),
        'e_s_n_o':article_html.find('input',{'id':'e_s_n_o'})['value'],
        'sort':'D' # 등록순
    }

    return list(base.post_comment_pages_seq(
        DC_COMMENT_STEM, headers, data, 'comment_page',
        lambda comment_dict:comment_dict['comments'])
    )


'''
article_no_li = article_no_list('programming', 1)
print(article_no_li, type(article_no_li[0]))

html,url = article_html_url('programming', article_no_li[4])
print(html, url)

html,url = article_html_url('hit', 14933)
cmt_dicts = comment_pages(html, url, 'hit', 14933)

html,url = article_html_url('programming', 969366)
cmt_dicts = comment_pages(html, url, 'programming', 969366)
print(cmt_dicts)
print(len(cmt_dicts))

html,url = article_html_url('programming', 975801)
cmt_dicts = comment_pages(html, url, 'programming', 975801)
print(cmt_dicts)
print(len(cmt_dicts))
'''

import vcr
my_vcr = vcr.VCR(path_transformer=vcr.VCR.ensure_suffix('.yml'),
                 cassette_library_dir='fixtures/cassettes')
import unittest
class test_article_html_url_core(unittest.TestCase):
    @my_vcr.use_cassette
    def test_If_404_then_Return_tuple_of_exception_url(self):
        ret = article_html_url('programming',975801)
        self.assertIsInstance(ret,tuple)
        exception,url = ret
        self.assertEqual(exception.status_code, 404)

if __name__ == '__main__':
    unittest.main()
'''
for no in range(975799,975804):
    print( type(article_html_url('programming',no)) )
'''
