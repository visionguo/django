# -*- coding: utf-8 -*-
#coding:utf-8

from __future__ import unicode_literals

from django.shortcuts import render
#from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect, Http404      #61 服务器上没有请求的资源时，标准的做法是返回404响应，导入了异常Http404，并在用户请求它不能查看的主题时引发这个异常
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required  #31 导入函数login_required(),将login_required（）作为修饰器用于视图函数topics()

#from .models import Topic   #导入与所需数据相关联的模型
from .models import Topic, Entry
#from .forms import TopicForm
from .forms import TopicForm, EntryForm

#导入函数render(),它根据视图提供的数据渲染响应

#编写视图
#视图函数接受请求中的信息，准备好生成网页所需的数据，再将这些数据发送给浏览器，通过模版实现，这个模版定义了网页是什么样的
#learning_logs中的文件views.py是你执行命令python manage.py startapp时自动生成的

# Create your views here.

#代码演示了该如何为主页编写视图
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')
    #URL请求与我们刚才定义的模式匹配时，Django将在文件views.py中查找函数index(),再将请求对象传递给这个视图函数
    #此处，不需要处理任何数据，这个函数只包含调用render()的代码，这里向函数render()提供了两个实参：原始请求对象以及一个可用于创建网页的模版

@login_required       #32 在topic（）加上@和login_required，login_required()的代码检查用户是否已登录
                      # 仅当用户已登录时，Django()才运行topics()的代码，如果用户未登录，就重定向登录页面，需修改settings.py
def topics(request):  # 包含一个形参，Django从服务器哪里收到的request对象,函数topic()需要从数据中获取一些数据，并将其发送给模版
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  #51 用户登录后，request对象将有一个user属性，这个属性存储了有关该用户的信息
                                                                              # 代码Topic.objects.filter(owner=request.user)让Django只从数据库中获取owner属性为当前用户的Topic对象
                                                                              # 由于没有修改主题的显示方式，因此无需对页面topics的模版做任何修改
                                                                              # topics = Topic.objects.order_by('date_added') #查询数据库，请求提供Topic对象，并按属性date_added对它们进行排序，将返回的查询集存储在topics中
    context = {'topics': topics}     #定义一个将要发送给模版的上下文，上下文是一个字典，键是将在模版中用来访问数据的名称，值是我们要发送给模版的数据
    return render(request, 'learning_logs/topics.html',context) #一个键值对，包含将在网页中显示的一组主题，创建使用数据的网页时
    #  除对象request和模版的路径外，还将变量content传递给render()

#视图函数，函数topic()需要从数据库中获取指定的主题以及与之相关联的所有条目
@login_required #40
def topic(request, topic_id):   #接受正则表达式(?P<topic_id>\d+) 捕获的值，并将其存储到topic_id 中
    """显示单个主题及其所有条目"""
    topic = Topic.objects.get(id=topic_id)   #62 get()来获取指定的主题，查询，因为它向数据库查询特定的信息，显示单个主题及其所有的条目
    if topic.owner != request.user:          #63 收到主题请求后，在渲染网页前检查该主题是否属于当前登录的用户，如果请求的主题不归当前用户所有，就引发Http404异常 #64
                                             # 若视图查看其他用户的主题条目，将看到Django发送的消息Page Not Found
        raise Http404
    entries = topic.entry_set.order_by('-date_added')   #获取与该主题相关联的条目，并按date_added排序，降序，显示最近的条目，查询，因为它向数据库查询特定的信息
    context = {'topic':topic,'entries': entries}        #将主题和条目都存储在条目context中
    return render(request, 'learning_logs/topic.html',context)  #将这个字典发送给模版topic.html

@login_required #40 除index()外的每个视图都应用了装饰器@login_required
                #如果在未登录的情况下访问这些页面，将被重定向到登录页面；
                #还不能单击到new_topic等页面的链接，但如果输入（http://127.0.0.1:8000/new_topic/）,将重定向到登录页面；
                #对于所有与私有用户数据相关的URL，都应限制对它们的访问；
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':        #1 测试确定请求方法是GET还是POST，不确定，就需返回一个空表单
        #未提交数据：创建一个新表单
        form = TopicForm()              #2 创建一个TopicForm实例，将其存储在变量form中，再通过上下文字典将这个表单发送给模版 #7 ，由于实例化TopicForm时没有指定任何实参，Django将创建一个可供用户填写的空表单
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)  #3 如果请求方法为POST、将执行else代码块，对提交的表单进行处理，使用用户输入的数据（存储在request.POST中）创建一个TopicForm实例，这样对象form将包含用户提交的信息
        if form.is_valid():             #4 要将提交的信息保存到数据库，须先通过检查确定它们是有效的。函数is_valid（）核实用户填写了所有必不可少的字段
            #form.save()                #5 如果所有字段都有效，可调用save()

            new_topic= form.save(commit=False)  #81 首先调用form.save(),并传递实参commit=False，因为我们先修改新主题，再将其保存到数据库中
            new_topic.owner = request.user      #82 将新主题的owner属性设置为当前用户
            new_topic.save()                    #83 对刚定义的主题实例调用save()，每个用户都只能访问自己的数据，无论查看数据，输入新数据还是修改旧数据
            return HttpResponseRedirect(reverse('learning_logs:topics'))  #6 将表单中的数据写入数据库，保存数据后，就可离开这个页面，
                                                                          # 使用reverse()获取页面topics的URL，并将其传递给HttpResponseRedirect()
                                                                          # 后者将用户的浏览器重定向到页面topics,在页面topics中，用户将在主题列表中看到他刚输入的主题
                                                                          # 导入了 HttpResponseRedirect 类，用户提交主题后我们将使用这个类将用户重定向到网页topics
                                                                          # 函数reverse()根据指定对URL模型确定URL，Django将在页面被请求时生成URL
    context = {'form': form}            #7
    return render(request, 'learning_logs/new_topic.html',context)

@login_required #40
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)       #11 new_entry()中的形参topic_id，用于存储从URL中获得的值，渲染页面以及处理表单数据，需使用topic_id来获得正确的主题
    if request.method != 'POST':                 #12 如果是GET请求，将执行if代码块，创建一个空的EntryForm实例 #13
        form = EntryForm()                       #13
    else:
        form = EntryForm(data=request.POST)      #14 如果请求方法为POST,就对数据进行处理，创建EntryForm实例，使用request对象中的POST数据来填充它
                                                 # 再检查表单是否有效，如果有效，就设置条目对象的属性topic，再将条目对象保存到数据库
        if form.is_valid():
            new_entry = form.save(commit=False)  #15 调用save()时，传递来实参commit=False
            new_entry.topic = topic              #16 让Django创建了一个新的条目对象，并将其存储到new_entry中，但不能将它保存到数据库中
                                                 # 将new_entry的属性topic设置为在这个函数开头从数据库中获取的主题
                                                 # 然后调用save(),且不指定任何实参，这将把条目保存到数据库，并将其与正确的主题相关联
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))  #17 将用户重定向到显示相关主题的页面，调用reverse()时，需提供两个实参：
                                                                                         # 根据它来生成URL的URL模式的名称；列表args，其中包含要包含在URL中的所有实参
                                                                                         # 调用 HttpResponseRedirect()将用户重定向到显示新增条目所属主题的页面
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required #40
def edit_entry(request, entry_id):         #21 编辑既有条目
    entry = Entry.objects.get(id=entry_id) #22 获取用户要修改的条目对象，以及与该条目相关联的主题
    topic = entry.topic

    if topic.owner != request.user:       #71 获取指定的条目以及与之相关联的主题，然后检查主题的所有者是否是当前登录的用户，如果不是，就引发Http404异常
        raise Http404

    if request.method != 'POST':          #23 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)  #24 在请求方法为GET时将执行的if代码块中，使用实参instance=entry创建一个EntryForm实例
                                          # 这个实参让Django创建一个表单，并使用既有条目对象中的信息填充它，用户将看到既有的数据，并能够编辑它们
    else:                                 #25 POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry,data = request.POST)  #26 处理POST请求时，传递实参instance=entry和data=request.POST
        if form.is_valid():
            form.save()                   #27 让Django根据既有条目对象创建一个表单实例，并根据request.POST中的相关数据对其进行修改
                                          # 然后我们检查表单是否有效，如果有效，就调用save(),且不指定任何实参
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id])) #28 重定向到显示条目所属主题的页面，用户将在其中看到其编辑的条目的新版本

    context = {'entry':entry,'topic':topic,'form':form}
    return render(request, 'learning_logs/edit_entry.html',context)

#对于只是从服务器读取数据的页面，使用GET请求
#在用户需要通过表单提交信息时，使用POST请求，使用所有表单时，指定使用POST方法
#函数new_topic()将请求对象作为参数。用户初次请求该网页时，浏览器将发送GET请求；用户填写并提交表单时，其浏览器将发送POST请求
#根据请求的类型，可确定用户请求的是空表单(GET请求)，还是要求对填写好对表单进行处理(POST请求)
