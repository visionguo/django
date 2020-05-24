#!/usr/bin/env python
#coding:utf-8

#创建基于表单的页面的方法几乎与创建网页一样：定义URL，编写一个视图函数并编写一个模版
#用于添加主题的表单

from django  import forms           #导入模块forms
from .models import Topic, Entry    #使用的模型Topic

class TopicForm(forms.ModelForm):   #定义名为TopicForm的类，继承forms.ModelForm
    class Meta:
        model = Topic               #根据模型Topic创建一个表单
        fields = ['text']           #该表单只包含字段text
        labels = {'text':''}        #让Django不要为字段text生成标签

class EntryForm(forms.ModelForm):   #1
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}       #1
        widgets = {'text': forms.Textarea(attrs={'cols':80})}   #2

"""
    #1、新类EntryForm继承了forms.ModelForm，包含的Meta类指出了表单基于的模型以及要在表单中包含哪些字段，也给字段'text'指定了一个空标签
    #2、定义了属性widgets。小部件（widget）是一个HTML表单元素，如单行文本框，多行文本区域或下拉列表   
    #让Django使用forms.Textarea，定制了字段'text'的输入小部件，将文本区域的宽度设置为80列（默认40列），
"""
