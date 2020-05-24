#!/usr/bin/env python
# coding=utf-8

"""learning_log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

#这两行导入为项目和管理网站管理URL的函数和模块

urlpatterns = [ #0
    url(r'^admin/', include(admin.site.urls)),   #1
    #url(r'', include('learning_logs.urls',namespace='learning_logs')),
    url(r'^users/', include('users.urls',namespace='users')),   #2
    url(r'', include('learning_logs.urls',namespace='learning_logs')),  #3
]

"""
    #映射URL
    #用户通过在浏览器输入URL以及单击链接来请求网页，因此我们需要确定项目需要哪些URL
    #0、文件的主体定义了变量urlpatterns，此变量包含项目中的应用程序的URL
    #1、包含模块admin.site.urls，该模块定义了可在管理网站中请求的所有URL
    #2、添加一行代码来包含模块learning_logs.urls,此行包含实参namespace，使我们能将learning_logs的URL同项目中的其他URL区分开来
    #3、与以单词users打头的URL (如http://localhost:8000/users/login/) 都匹配;
    #还创建了命名空间'users',以便将应用程序learning_logs 的URL同应用程序users 的URL区分开来
"""