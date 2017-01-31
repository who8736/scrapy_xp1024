# -*- coding: utf-8 -*-
'''
Created on 2017年1月31日

@author: who8736
'''

import os
from datetime import datetime
import shutil

from xp1024.settings import CLEARDAYS
from dbmanager import read_page_list, del_pages


def clearHTMLFile():
    absDir = os.path.abspath('./static/html')
    print absDir
    fileList = os.walk(absDir)
    nowtime = datetime.now()
    for root, _dirs, files in fileList:
        for f in files:
            filename = os.path.join(root, f)
            filetime = datetime.fromtimestamp(os.stat(filename).st_ctime)
            if (nowtime - filetime).days > CLEARDAYS:
                os.remove(filename)
            print filename, (nowtime - filetime).days


def clearIMGFile():
    absDir = os.path.abspath('./static/img/full')
    print absDir
    fileList = os.walk(absDir)
    nowtime = datetime.now()
    for root, dirs, files in fileList:
        for d in dirs:
            filename = os.path.join(root, d)
            filetime = datetime.fromtimestamp(os.stat(filename).st_ctime)
            if (nowtime - filetime).days > CLEARDAYS:
                shutil.rmtree(filename)
            print filename, (nowtime - filetime).days


def clearDatabase():
    pageList = read_page_list()
    for pageCode, _pagename in pageList:
        filename = './static/html/%s.html' % pageCode
        if not os.path.isfile(filename):
            del_pages(pageCode)
    print read_page_list()


if __name__ == '__main__':
    print 'ok1'
    clearHTMLFile()
    clearIMGFile()
    clearDatabase()
    print 'ok2'
