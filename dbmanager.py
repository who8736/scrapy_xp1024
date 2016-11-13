# -*- coding: utf-8 -*-
'''
Created on 2016年11月8日

@author: who8736
'''

import sqlite3
from xp1024.pagemanager import read_page_list


def init_table():
    conn = sqlite3.connect('xp1024.db')
    conn.execute('create table if not exists pages'
                 '(id integer primary key,'
                 'pagecode varchar(6) UNIQUE,'
                 'pagetitle varchar(200))')
    conn.close()


def read_page_list():
    conn = sqlite3.connect('xp1024.db')
    curs = conn.cursor()
    curs.execute(
        'select pagecode, pagetitle from pages order by pagecode desc;')
    page_list = curs.fetchall()
#     print 'rows type:', type(page_list)
#     page_list = []
#     for pagecode, pagetitle in page_list:
#         print repr(pagecode), repr(pagetitle)
#     for i in rows:
#         print i
    conn.close()
    return page_list


def write_pages(pages):
    conn = sqlite3.connect('xp1024.db')
    curs = conn.cursor()
    for pagecode, pagetitle in pages:
        print pagecode, pagetitle
        curs.execute((u'insert or ignore into pages (pagecode, pagetitle) '
                      u'values(?, ?);'), (pagecode, pagetitle))
    conn.commit()
    conn.close()


def write_page(page):
    conn = sqlite3.connect('xp1024.db')
    curs = conn.cursor()
    pagecode, pagetitle = page
    print '-' * 10 + 'write pages' + '-' * 10
    print repr(pagecode), repr(pagetitle)
    curs.execute((u'insert or ignore into pages (pagecode, pagetitle) '
                  u'values(?, ?);'), (pagecode, pagetitle))
    conn.commit()
    conn.close()


def write_pages_test():
    conn = sqlite3.connect('xp1024.db')
    curs = conn.cursor()
    pagecode = u'471882'
    pagetitle = u'[11.08] ★★国产高清の最新合集★☆ [11.09]'
#     for pagecode, pagetitle in pages:
    print repr(pagecode), repr(pagetitle)
#     curs.execute(('insert into pages(pagecode, pagetitle) '
#                   'values(`%s`,`%s`);')
#                  % (pagecode, pagetitle))
    curs.execute((u'insert or ignore into pages(pagecode, pagetitle) '
                  u'values(?,?);'), (pagecode, pagetitle))
    conn.commit()
    conn.close()


def del_pages():
    conn = sqlite3.connect('xp1024.db')
    curs = conn.cursor()
    curs.execute(u'delete from pages where pagecode="471882";')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    #     init_table()
    #     pages = read_page_list()
    #     print pages
    #     print '-' * 10 + 'write pages' + '-' * 10
    # #     write_pages_test()
    #     write_pages(pages)

    #     del_pages()

    print '-' * 10 + 'read pages' + '-' * 10
    pages_list = read_page_list()
    print pages_list


#     curs = conn.cursor()

    # 检查users表是否存在，不存在则创建
    # 很强大，不需要使用管理工具事先创建
#     curs.execute(
#         'CREATE TABLE if not exists users(username VARCHAR(20) UNIQUE,password VARCHAR(32),groupe INTEGER);')
    # 对数据库有修改的操作要调用commit提交事务
    # 对数据库没有修改的操作不需要用commit提交事务

#     db.commit()
#     curs.execute(
#         "select * from users where username=?;", (raw_input("请输入要查询的用户名称："),))
#     row = curs.fetchone()
#     if row:
#         print row
#
#     db.close()
