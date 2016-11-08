# -*- coding: utf-8 -*-
'''
Created on 2016年11月8日

@author: who8736
'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'xp1024.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# 激活 跨站点请求伪造 保护
# form.hidden_tag() 模板参数将被替换为一个隐藏字段，用来是实现在配置中激活的 CSRF 保护。
# 如果你已经激活了 CSRF，这个字段需要出现在你所有的表单中。
CSRF_ENABLED = True
# SECRET_KEY 配置仅仅当 CSRF 激活的时候才需要，它是用来建立一个加密的令牌，用于验证一个表单。
# 生产环境应重新设置该值
SECRET_KEY = 'you-will-never-guess'