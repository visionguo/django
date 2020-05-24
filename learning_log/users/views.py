# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
#from django.contrib.auth import logout  #1

from django.shortcuts import render     #10
from django.contrib.auth import login, logout, authenticate #10
from django.contrib.auth.forms import UserCreationForm  #10

def logout_view(request):
    logout(request)     #2
    return HttpResponseRedirect(reverse('learning_logs:index'))     #3

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()   #11
    else:
        form = UserCreationForm(data=request.POST)  #12
        if form.is_valid(): #13
            new_user = form.save()  #14
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1']) #15
            login(request,authenticated_user)   #16
            return HttpResponseRedirect(reverse('learning_logs:index'))     #17
    context = {'form': form}
    return render(request, 'users/register.html', context)

"""
    # 函数logout_view(),导入Django函数logout(),并调用它，再重定向到主页
    # 1、从django.contrib.auth中导入来函数logout()
    # 2、调用了函数logout(),它要求将request对象作为实参，然后重定向到主页 #3
    
    #10、导入了函数render(),login()和authenticate(),以便在用户正确地填写了注册信息时让其自动登录，导入默认表单UserCreationForm
    #11、在函数register()中，检查响应是否是POST请求，若不是，就创建一个UserCreationForm实例，且不给它提供任何初始数据
    #12、若是POST请求，就根据提交的数据创建一个UserCreationForm实例，并检查数据是否有效：是用户名未包含非法字符，输入的两个密码相同，以及用户没有视图做恶意的事
    #13、若提交的数据有效，就调用表单的方法save(),将username and password的散列值保存到数据库中 #14，方法save()返回新创建的用户对象，将其存储在new_user中
    #15、保存用户的信息后，让用户自动登录，包含两个步骤：首先 调用authenticate(),并将实参new_user.username和password传递给它
    #16、用户注册时，被要求输入两次密码；由于表单是有效的，输入的这两个密码是相同的，因此可以使用其中任何一个，此处，从表单的POST数据中获取与键'password1'相关联的值
    #若用户名和密码无误，方法authenticate()将返回一个通过了身份验证的用户对象，将其存储在authenticated_user中
    #调用函数login()，并将对象request和authenticated_user传递给它
    #这将为新用户创建有效的会话，最后，将用户重定向到主页，其页眉中显示了一条个性化的问候语，让用户知道注册成功了
"""