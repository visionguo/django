# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
#向管理网站注册模型
#Django自动在管理网站中添加了一些模型，如User和Group，但对于我们创建的模型，必须手工进行注册
# Register your models here.

# from learning_logs.models import  Topic     #导入我们要注册的模型Topic
# admin.site.register(Topic)                  #让Django通过管理网站管理我们的模型

#向管理网站注册Entry
#需注册模型Entry
from learning_logs.models import Topic,Entry

admin.site.register(Topic)
admin.site.register(Entry)

