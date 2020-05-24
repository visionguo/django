#!/usr/bin/env python
# coding=utf-8

#定义了 learning_logs 的URL模式
from django.conf.urls import url    #导入函数url，使用它来将URL映射到视图

from . import views     #导入模块views，句点让python从当前的urls.py模块所在的文件夹导入视图
#实际的URL模式是一个对函数url()的调用，这个函数接受三个实参，第一个是一个正则表达式，
#Django在urlpatterns中查找与请求的URL字符串匹配的正则表达式，因此正则表达式定义了Django可查找的模式

urlpatterns = [
    #变量urlpatterns是一个列表，包含可在应用程序learning_logs中请求的网页
    #主页
    url(r'^$', views.index, name='index'),
    url(r'^topics/$', views.topics, name="topics"),
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),     #使用主题的id属性来指出请求的是哪个主题
    url(r'^new_topic/$', views.new_topic, name='new_topic'),            #这个URL模式将请求交给视图函数new_topic()
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry,name='new_entry'),    #1
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry,name='edit_entry'), #2
]
    #info：
        #1、r让Django将这个字符串视为原始字符串，并指出正则表达式包含在引号内
        #2、(/(?P<topic_id>\d+)/)与包含在两个斜杠内的整数匹配，并将这个整数存储在一个名为topic_id的实参中
        #3、表达式两边的括号捕获URL中的值: ?P<topic_id>将匹配的值存储到topic_id中，而表达式\d+与包含在两个斜杠内的任何数字都匹配，不管这个数字是多少位
        #4、发现URL与这个模式匹配时，Django将调用视图函数topic(),并将存储在topic_id中的值作为实参传递给它，在这个函数中，将使用topic_id的值来获取相应的主题

#只在用于主页URL的正则表达式中添加了topic/，其URL与该模式匹配的请求都交给views.py中的函数topics()进行处理
"""
# r'^$' 让Python查找开头和末尾之间没有任何东西的URL
# r'^$'，r 让Python将接下来的字符串视为原始字符串，引号告诉Python正则表达式始于和终于何处，脱字符(^)让Python查看字符串的开头，$ 让Python查看字符串的末尾
# Python忽略项目的基础URL(http://localhost:8000/)，因此这个正则表达式与基础URL匹配
# 其他URL都与这个正则表达式不匹配，如果请求的URL不与任何URL模式匹配，Django将返回一个错误页面
# url()的第二个实参views，指定了要调用的视图函数，请求的URL与前述正则表达式匹配时，Django将调用views.index
# 第三个实参将这个URL模式的名称指定为index，能在代码的其他地方引用，每当需要提供到这个主页的链接时，将使用这个名称，而不编写URL

#显示所有主题的页面，定义显示所有主题的URL。使用简单的URL片段来指出网页显示的信息，使用topics，因此http://127.0.0.1:8000/topics/将返回显示主题的页面
"""
    #1、用于添加新条目的页面，需包含实参topic_id,因为条目必须与特定的主题相关联
    # (?P<topic_id>\d+)捕获一个数字值，并将其存储在变量topic_id中，请求的URL与这个模式匹配时，Django将请求和主题ID发送给函数new_entry中
    #2、在URL中传递的ID存储在形参entry_id中，这个URl模式将预期匹配的请求发送给视图函数edit_entry()

