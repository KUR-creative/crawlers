#-*- coding: utf-8 -*-
import pickle
import base
import json
import os
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

    ''' 
    def response2page(resp):
        try:
            return resp.json()
        except:
            with open(str(gall_id)+'_'+str(article_no)+'.problem') as f:
                pickle.dump(resp,f)
                print(type(resp))
                print(resp.status_code)
    '''

    if str(gall_id) not in article_url:
        raise ValueError('gall_id must be matched with article_url')
    if str(article_no) not in article_url:
        raise ValueError('article_no must be matched with article_url')

    def resp2page(resp):
        tagged_json = resp.content
        # split headed <script> tag and join rest
        only_json = b'{' + tagged_json.split(b'{',maxsplit=1)[1]
        return json.loads(only_json.decode('utf-8'))
    try:
        return \
        list(base.post_comment_pages_seq(
            DC_COMMENT_STEM, headers, data, 'comment_page',
            lambda comment_dict:comment_dict['comments'],
            response2page=resp2page
            )
        )
    except Exception as exception:
        print(exception)
        print(exception.doc)
        print(exception.pos)
        print(exception.lineno)
        print(exception.msg)
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

#------------ logger ------------
import traceback
from datetime import datetime
from tqdm import tqdm
import time
import sys
import yaml
if __name__ == '__main__':
    #unittest.main()
    usage =\
    '''
    Usage:
        python dc_core.py gall_id begin_article_no end_article_no  # make gall_id.yml and crawl.
        python dc_core.py gall_id.yml  # continue crawling
    ex)
        python dc_core.py programming 802496 963561
        python dc_core.py programming.yml

    if you have already "some_id.yml", then you can't create same "some_id.yml"
    '''
    if len(sys.argv) == 3 + 1:
        brand_new = True
        gall_id = sys.argv[1]
        beg_no  = int(sys.argv[2])
        end_no  = int(sys.argv[3])
        crawl_info = dict(
            gall_id = gall_id,
            beg_no = beg_no,
            now_no = beg_no,
            end_no = end_no
        )
    elif len(sys.argv) == 1 + 1:
        brand_new = False
        log_file = sys.argv[1] 
        with open(log_file, 'r') as f:
            crawl_info = yaml.load(f)
            gall_id= crawl_info['gall_id']
            beg_no = crawl_info['beg_no']
            end_no = crawl_info['end_no']
    else:
        print(usage)
        sys.exit()
    
    now_no = crawl_info['now_no']
    #now_no = beg_no if brand_new else 4
    #print(now_no)

    #begin_no = 802496
    #end_no   = 963561
    start_time = time.time()
    #for no in tqdm(range(802426,802526)):
    log_name = gall_id + '.yml'
    if brand_new and os.path.exists(log_name):
        print('Crawling log [',log_name,'] is already exists! Deal with it...')
        sys.exit()
    with open(log_name,'w') as log: # brand new case
        try:
            for no in tqdm(range(crawl_info['now_no'], crawl_info['end_no'])):
                time.sleep(1)
                '''
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
                '''
                now_no += 1
        except Exception as err:
            #log.write('-------[%s,%d]-------' % (gall_id,no))
            print(err)
            #traceback.print_tb(err.__traceback__)
            #traceback.print_tb(err.__traceback__,file=log)

        finally:
            crawl_info['now_no'] = now_no
            yaml.dump(crawl_info, log)
            print(log_name, 'saved successfully!')
            '''
            try:
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
            except Exception as err:
                log.write('-------[%s,%d]-------' % ('programming',no))
                traceback.print_tb(err.__traceback__)
                traceback.print_tb(err.__traceback__,file=log)
            '''

    print("--- %s seconds ---" % (time.time() - start_time))
    
'''
no = 924802#826976
html,url = article_html_url('programming',no)
cmt_dicts = comment_pages(html,url,'programming',no)
print(cmt_dicts)
#'programming',
'''
