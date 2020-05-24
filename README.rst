Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Thanks for checking it out.


```

1、安装virtualenv
    pip install --user virtualenv

2、创建虚拟环境env
    sudo virtualenv env

3、激活虚拟环境env
    source env/bin/activate

4、安装Django
    sudo pip install Django

5、让Django新建一个名为learning_log的项目
    sudo   django-admin.py startproject learning_log .
    #句点让新项目使用合适的目录结构

6、创建数据库，存储大部分与项目相关的信息
    sudo python manage.py migrate
    #db.sqlite3，SQLite是一种使用单个文件的数据库

7、启动django
    python manage.py runserver
    #以特定端口开启 django python manage.py runserver 8001

8、创建应用程序
    source env/bin/activate
    sudo python  manage.py startapp learning_logs
    #startapp appname 让Django建立创建应用程序所需的基础设施

9、sudo python manage.py makemigrations learning_logs
    #makemigrations 让Django确定该如何修改数据库，使其能够存储与我们定义的新模型相关联的数据
    Migrations for 'learning_logs':
    learning_logs/migrations/0001_initial.py
        - Create model Topic
    输出表明Django创建了一个名为0001_initial.py的迁移文件，这个文件将在数据库中为模型Topic创建一个表

10、应用这种迁移，让Django替我们修改数据库
    sudo python manage.py migrate

11、每次修改"学习笔记"管理的数据时，都采取如下三个步骤：
    1.修改models.py
    2.对learning_logs调用makemigrations
    3.让Django迁移项目

12、Django管理网站，创建超级用户
    sudo python manage.py createsuperuser
    Username:
    Email:
    pass:
    #ps：Django并不存储你输入的密码，而存储从该密码派生出来的一个字符串 -- 散列值
    每当你输入密码时，Django都计算其散列值，并将结果与存储的散列值进行比较，如果散列值相同，就通过了身份验证
    即便hacker获得了网站数据库的访问权，也只能获取其中存储的散列值，而无法获得密码，在网站配置正确的情况下，几乎无法根据散列值推导出原始密码

13、迁移模型Entry
    由于添加了新模型，需再次迁移数据库
    sudo python manage.py makemigrations learning_logs
    sudo python manage.py migrate

    流程：
        1.修改 models.py
        2.执行 sudo python manage.py makemigrations learning_logs
        Migrations for 'learning_logs':
            learning_logs/migrations/0002_entry.py
                - Create model Entry
        生成一个新的迁移文件 -0002_entry.py，它告诉Django如何修改数据库，使其能存储与模型Entry相关的信息，
        3.再执行 sudo python manage.py migrate
        Operations to perform:
            Apply all migrations: admin, auth, contenttypes, learning_logs, sessions
        Running migrations:
            Applying learning_logs.0002_entry... OK
        执行命令migrate，发现Django应用了这种迁移且一切顺利

14、Django shell, 是测试项目和排除故障的理想之地，输入数据后，可通过交互式终端会话以编程方式查看这些数据了
    python manage.py shell      #启动一个python解释器，使用它来探索存储在项目数据库中的数据
    from learning_logs.models import Topic  #导入了模块learning_logs.models中的模型Topic
    Topic.objects.all()         #使用方法Topic.objects.all()来获取模型Topic的所有实例，返回的是一个列表，称为查询集(queryset)

    >>> topics = Topic.objects.all()    #将返回的查询集存储在topics中，然后打印每个主题的id属性和字符串表示
    >>> for topic in topics:
    >>>     print(topic.id,topic)

    (1, <Topic: chess>)
    (2, <Topic: Rock Climbing>)

    >>> t = Topic.objects.get(id=1)     #知道对象的ID后，就可获取该对象并查看其任何属性
    >>> t.text
    u'chess'
    >>> t.date_added
    datetime.datetime(2018, 11, 12, 4, 25, 2, 511810, tzinfo=<UTC>)

    >>> t.entry_set.all()       #查看与主题相关联的条目，我们给模型Entry定义了属性topic,这是一个ForeignKey,将条目与主题关联起来，利用这种关联，Django能够获取与特定主题相关联的所有条目
    <QuerySet [<Entry: This is my first entry...>, <Entry: In the opening phase of the game, it's important t...>, <Entry: The opening is the first part of the game, roughly...>]>

15、创建网页：学习笔记主页
    1.定义URL      #定义URL模式，URL模式描述了URL是如何设计的，让Django知道如何将浏览器请求与网站URL匹配，以确定返回哪个网页
    2.编写视图      #每个URL都被映射到特定的视图，视图函数获取并处理网页所需的数据。视图函数通过调用一个模版，后者生成浏览器能够理解的网页
    3.编写模版

16、创建网页时，将URL、视图、模版分离的效果实际上很好
    1.DBA专注于模型
    2.程序员专注于视图代码
    3.Web设计专注于模版

17、查看django版本
    python -m django --version

18、使用命令startapp 来创建一个名为users的应用程序（目录）
    python manage.py startapp users

19、迁移数据库时，Django将对数据库进行修改，使其能存储主题和用户之间的关联
    为执行迁移，Django需要知道该将各个既有主题关联到哪个用户
    最简单的方法是：将既有主题都关联到同一个用户，如超级用户
    python manage.py shell
    from django.contrib.auth.models import User     #在shell会话中导入模型User
    User.objects.all()      #查看目前为止都创建了哪些用户
    for user in User.objects.all():
        print(user.username, user.id)   #遍历用户列表，打印每位用户的用户名和ID,Django询问要将既有主题关联到哪个用户时，我们将指定其中到一个ID值

20、迁移数据库
    python manage.py makemigrations learning_logs   #1
    You are trying to add a non-nullable field 'owner' to topic without a default;
    we can't do that (the database needs something to populate existing rows).  #2
    Please select a fix:    #3
        1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
        2) Quit, and let me add a default in models.py
    Select an option: 1     #4
    Please enter the default value now, as valid Python     #5
    The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
    Type 'exit' to exit this prompt
    >>> 1   #6
    Migrations for 'learning_logs':
        learning_logs/migrations/0003_topic_owner.py
            - Add field owner to topic

    #1、执行makemigrations
    #2、Django指出我们视图给既有模型Topic添加一个必不可少的字段，而该字段没有默认值
    #3、两种选择：要么现在提供默认值，要么推出并在models.py中添加默认值
    #4、选择第一个选项，因此Django让我们输入默认值 #5
    #6、为将所有既有主题都关联到管理用户,输入了用户ID值1

    #并非必须使用超级用户，而可使用已创建到任何用户的ID
    #Django使用这个值来迁移数据库，并生成了迁移文件0003_topic_owner.py，它在模型Topic中添加字段owner

21、Django应用新的迁移
    (env) ➜  learning_log git:(master) ✗ python manage.py migrate
    Operations to perform:
        Apply all migrations: admin, auth, contenttypes, learning_logs, sessions
    Running migrations:
        Applying learning_logs.0003_topic_owner... OK

22、验证迁移符合预期
    python manage.py shell
    >>> from learning_logs.models import Topic  #11
    >>> for topic in Topic.objects.all():       #12
    ...     print(topic, topic.owner)
    ...
    (<Topic: chess>, <User: admin>)
    (<Topic: Rock Climbing>, <User: admin>)
    (<Topic: cheetah>, <User: admin>)

    #11、从learning_logs.models中 导入 Topic
    #12、再遍历所有的既有主题，并打印每个主题机器所属的用户，每个主题都属于用户admin

23 、活动的虚拟环境中执行
    pip install django-bootstrap3

24、笔记
    #15、导航栏是一个以<ul> 打头的列表，每个链接都是一个列表项（<li>）
    #要添加更多的链接，可插入更多使用下述结构的行
         <li><a href="{% url 'learning_logs:title' %}">Title</a></li>
        这行表示导航栏中的一个链接，这个链接是直接从base.html的前一个版本中复制而来的

```