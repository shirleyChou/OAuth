创建了一个第三方登陆系统，实现了一下功能：  
* 一个用户可以同时绑定多个社交帐号  
* 每解绑一个账户会有解绑提醒
* 解绑最后一个帐号时会提醒解绑后帐号会被注销
* 一个社交网站的不同帐号想同时绑定另一个社交网站的一个帐号是会报错  

=

技术实现：
* Django 1.8.2 
* Python 2.7.10
* 数据库用的是Herok云平台上的PostgreSQL
* 前端用了Bootstrap，也自己写了一部分  

=

project架构：
```bash
third
├── app
│   ├── admin.py
│   ├── __init__.py
│   ├── models.py
│   ├── social
│   │   ├── base.py
│   │   ├── douban.py
│   │   ├── __init__.py
│   │   ├── qzone.py
│   │   └── weibo.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── __init__.py
├── settings.py
├── static
│   ├── css
│   ├── font-awesome
│   ├── fonts
│   ├── img
│   └── js
├── templates
│   ├── duplicate.html
│   ├── home.html
│   └── index.html
├── urls.py
└── wsgi.py
```
