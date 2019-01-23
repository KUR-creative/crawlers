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
    url = ''
    try:
        html,url = base.article_html_url(
            DC_ARTICLE_STEM, {'id':gall_id, 'no':article_no}
        )
        return html,url
    except Exception as exception:
        return exception.response,url

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

    if str(gall_id) not in article_url:
        raise ValueError('gall_id must be matched with article_url')
    if str(article_no) not in article_url:
        raise ValueError('article_no must be matched with article_url')

    try:
        return \
        list(base.post_comment_pages_seq(
            DC_COMMENT_STEM, headers, data, 'comment_page',
            lambda comment_dict:comment_dict['comments'])
        )
    except Exception as exception:
        return exception.response

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
import unittest
my_vcr = vcr.VCR(path_transformer=vcr.VCR.ensure_suffix('.yml'),
                 cassette_library_dir='fixtures/cassettes')
class test_article_html_url_core(unittest.TestCase):
    @my_vcr.use_cassette
    def test_If_404_then_Return_tuple_of_response_emptystr(self):
        ret = article_html_url('programming', 975801)
        self.assertIsInstance(ret,tuple)
        response,_ = ret
        self.assertEqual(response.status_code, 404)

    @my_vcr.use_cassette
    def test_If_200_then_Return_tuple_of_html_url(self):
        ret = article_html_url('programming', 975800)
        self.assertIsInstance(ret, tuple)
        html,url = ret
        self.assertEqual(len(html), 112)
        self.assertEqual(url, 'http://gall.dcinside.com/board/view?id=programming&no=975800')

class test_comment_pages(unittest.TestCase):
    @my_vcr.use_cassette
    def test_If_unmatched_article_no_then_Raise_value_error(self):
        html,url = article_html_url('programming', 975800)
        other_no = 968246
        with self.assertRaises(ValueError):
            comment_pages(html, url, 'programming', other_no)

    @my_vcr.use_cassette
    def test_If_unmatched_gall_id_then_Raise_value_error(self):
        html,url = article_html_url('programming', 975800)
        with self.assertRaises(ValueError):
            response = comment_pages(
                html, url, 'unmatched_gall_id', 975800)

    @my_vcr.use_cassette
    def test_If_no_comments_then_Return_empty_list(self):
        html,url = article_html_url('programming', 973445)
        cmt_dicts = comment_pages(
            html, url, 'programming', 973445)
        self.assertTrue(base.is_empty(cmt_dicts))

from tqdm import tqdm
import time
import json
if __name__ == '__main__':
    begin_no = 826976
    end_no = 963561
    start_time = time.time()
    #for no in tqdm(range(802426,802526)):
    for no in tqdm(range(begin_no ,end_no)):
        with vcr.use_cassette('last_request.yml', record_mode='all'):
            html,url = article_html_url('programming',no)
            #print( base.is_bs4html(article_html_url('programming',no)[0]) )
            #print('->', base.is_bs4html(html))
            cmt_dicts = []
            if base.is_bs4html(html):
                with open('pages/%s_%d.html' % ('programming',no), 'w', encoding='utf8') as f:
                    f.write(str(html))
                cmt_dicts = comment_pages(html,url,'programming',no)
            if base.is_not_empty(cmt_dicts):
                with open('comments/%s_%d.json' % ('programming',no), 'w', encoding='utf8') as f:
                    json.dump(cmt_dicts, f)

    print("--- %s seconds ---" % (time.time() - start_time))
    unittest.main()
'''
no = 826976
html,url = article_html_url('programming',no)
cmt_dicts = comment_pages(html,url,'programming',no)
print(cmt_dicts)
#'programming',
'''
