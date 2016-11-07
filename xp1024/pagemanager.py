# -*- coding: utf-8 -*-
'''
Created on 2016年11月6日

@author: who8736
'''
import json
import traceback
import codecs


def read_page_list():
    f = codecs.open('scraped_data.json', 'rb', encoding='utf-8')
    page_list = []
    for jsonstr in f.readlines():
        #         unicodestr = jsonstr
        try:
            #             unicodestr = jsonstr.decode('utf-8')
            jsonobj = json.loads(jsonstr)
            pagecode = jsonobj['pagecode']
            pagetitle = jsonobj['pagetitle']
            page = [pagecode, pagetitle]
            if page not in page_list:
                page_list.append(page)
        except Exception, e:
            print 'str(Exception):\t', str(Exception)
            print 'str(e):\t\t', str(e)
            print 'repr(e):\t', repr(e)
            print 'e.message:\t', e.message
            print 'traceback.print_exc():'
            traceback.print_exc()
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
    f.close()
#     page_list = list(set(page_list))
    page_list = sorted(page_list, key=lambda page: page[0], reverse=True)
    write_page_list(page_list)
#     for code, title in page_list:
#         print code, title
    return page_list


def write_page_list(page_list):
    f = codecs.open('scraped_data.json', 'wb', encoding='utf-8')
    jsonstr_list = []
    for page in page_list:
        pagecode, pagetitle = page
        page_dict = {'pagecode': pagecode, 'pagetitle': pagetitle}
        jsonstr = json.dumps(page_dict, ensure_ascii=False)
        jsonstr_list.append(jsonstr)
    f.write(u'\n'.join(jsonstr_list))
    f.close()

if __name__ == '__main__':
    read_page_list()
