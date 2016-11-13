#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2016年11月4日

@author: who8736
'''

from flask import Flask, request, render_template, url_for
# import json
# import traceback

from xp1024.pagemanager import read_page_list
from dbmanager import read_page_list


app = Flask(__name__)
app.debug = True
app.config.from_object('flaskconfig')


@app.route('/', methods=['GET', 'POST'])
def home():
    #     my_page_list = {
    #         "pagetitle": "[11.04] ♠유最新日本騎兵웃♣新片合集♥95℃ [11.04]",
    #         "pagecode": "469049"}
    my_page_list = read_page_list()
#     print url_for('static')
    for (k, v) in my_page_list:
        print k, repr(v)
    return render_template('index.html', page_list=my_page_list)


@app.route('/index_nav', methods=['GET', 'POST'])
def home_nav():
    #     my_page_list = {
    #         "pagetitle": "[11.04] ♠유最新日本騎兵웃♣新片合集♥95℃ [11.04]",
    #         "pagecode": "469049"}
    my_page_list = read_page_list()
#     print url_for('static')
    for (k, v) in my_page_list:
        print k, repr(v)
    return render_template('index_nav.html', page_list=my_page_list)


@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        return render_template('signin-ok.html', username=username)
    return render_template('form.html',
                           message='Bad username or password',
                           username=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

# from flask import Flask
# from flask import request, render_template
#
# app = Flask(__name__)
#
#
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return render_template('index.html')
# #     return '<h1>Home</h1>'
#
#
# if __name__ == '__main__':
#     app.run()
