#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#import  django.db

#定义模型
#模型就是一个类，每个类包含属性和方法

#from datetime import  datetime

from django.db import models
from django.contrib.auth.models import User  #1

class Topic(models.Model):
    #创建名为Topic的类，继承Model，Topic类有两个属性text和date_added
    #Model是Django中一个定义类模型基本功能的类
    #学习的主题
    text = models.CharField(max_length=200)
    #属性text是一个CharField，由字符或文本组成的数据，存储少量文本，可使用CharField,定义CharField属性时，需告诉Django该在数据库中预留多少空间
    date_added = models.DateTimeField(auto_now_add=True)
    #属性date_added是一个DateField，记录日期和时间的数据，每当创建新主题时，让Django将这个属性自动设置成当前日期和时间
    owner = models.ForeignKey(User)     #2

    # def __str__(self):      #python3.6
    def __unicode__(self):
        #返回模型的字符串表示
        return self.text

class Entry(models.Model):      #像Topic一样，Entry也继承了Django基类Model
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic)    #属性topic是一个ForeignKey实例
    #外键是数据库术语，引用了数据库中的另一条记录，这些代码将每个条目关联到特定的主题，每个主题创建时，都给它分配了一个键(或ID)
    #需要在两项数据之间建立联系时，Django使用与每项信息相关联的键，稍后将根据这些联系获取与特定主题相关联的所有条目
    text = models.TextField()           #属性text,是一个TextField实例，这种字段不需长度限制
    date_added = models.DateTimeField(auto_now_add=True)    #属性date_added能按创建顺序呈现条目，并在每个条目旁边放置时间戳

    class Meta:     #在Entry类中嵌套了Meta类，Meta存储用于管理模型的额外信息，在这里，它让我们能够设置一个特殊属性
        verbose_name_plural = 'entries'     #让Django在需要时使用Entries来表示多个条目，如果没有这个类，Django将使用Entrys来表示多个条目

    def  __unicode__(self):     #方法 __unicode__()告诉Django，呈现条目时应显示哪些信息，由于条目包含的文本可能很长，让Django只显示text的前50个字符，添加省略号，指出显示的并非整个条目
        return self.text[:50] + "..."

"""
    #1、导入django.contrib.auth中的模型User
    #2、在Topic中添加了字段owner，它建立到模型User的外键关系
"""