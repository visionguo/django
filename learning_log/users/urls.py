#!/usr/bin/env python
# coding:utf-8

from django.conf.urls import url
from django.contrib.auth.views import login     #1

from . import views

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'users/login.html'},  #2
        name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),  # 11
    url(r'^register/$', views.register, name='register'),   #21
]

"""
    #为应用程序users 定义URL模式
    #1、导入默认视图login
    #2、登录页面的URL模式与URL http://127.0.0.1:8000/users/login/匹配
    #这个URL中的单词users让Django在users/urls.py中查找，而单词login让它将请求发送给Django默认视图login
    #鉴于没有编写自己的视图函数，传递了一个字典，告诉Django去哪里查找我们将编写的模版，这个模版包含在应用程序users而不是learning_logs中
    
    #11、为注销定义来URL模式，该模式匹配http://localhost:8000/users/logout/
    #这个URL模式将请求发送给函数logout_view(),给这个函数命名，旨在将其与我们将在其中调用的函数logout()区分开来
    
    #21、注册页面的URL模式，模式与URl http://localhost:8000/users/register匹配，并将请求发送给函数register()
"""