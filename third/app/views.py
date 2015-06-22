# encoding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
# from django.template import RequestContext
# from django import forms
# from models import User

from models import LoginInfo
from social.douban import DouBan
from social.qzone import Qzone
from social.weibo import WeiBo


douban = DouBan()
weibo = WeiBo()
qzone = Qzone()

login_db_id = None

weibo_found = False
douban_found = False
qzone_found = False

weibo_duplicate = False
douban_duplicate = False
qzone_duplicate = False

# all_delete = False


def login(request):
    return render_to_response('home.html')


# def bind_weibo(request):
#     return weibo.authorize_url


# def bind_douban(request):
#     return douban.authorize_url


# def bind_qzone(request):
#     return qzone.authorize_url


def handle_data(request):
    global login_db_id
    global weibo_duplicate
    global douban_duplicate
    global qzone_duplicate
    

    if request.method == 'GET':
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')
    if login_db_id is None:
        if state == "weibo":
            weibo.get_access_token(code=code)
            lst = LoginInfo.objects.filter(weibo_id__exact=weibo.uid)
            if not lst:
                new = LoginInfo(weibo_id=weibo.uid)
                new.save()
                login_db_id = new.id
            else:
                login_db_id = lst[0].id
        elif state == "douban":
            douban.get_access_token(code=code)
            lst = LoginInfo.objects.filter(douban_id__exact=douban.uid)
            if not lst:
                new = LoginInfo(douban_id=douban.uid)
                new.save()
                login_db_id = new.id
            else:
                login_db_id = lst[0].id
        else:
            qzone.get_access_token(code=code)
            lst = LoginInfo.objects.filter(qzone_id__exact=qzone.uid)
            if not lst:
                new = LoginInfo(qzone_id=qzone.uid)
                new.save()
                login_db_id = new.id
            else:
                login_db_id = lst[0].id
    else:
        if state == "weibo":
            weibo.get_access_token(code=code)
            lst = LoginInfo.objects.filter(weibo_id__exact=weibo.uid)
            if lst and lst[0].id != login_db_id:
                weibo_duplicate = True
            else:
                weibo_duplicate = False
                LoginInfo.objects.filter(id=login_db_id).update(weibo_id=weibo.uid)
        elif state == "douban":
            douban.get_access_token(code=code)
            lst = LoginInfo.objects.filter(douban_id__exact=douban.uid)
            if lst and lst[0].id != login_db_id:
                douban_duplicate = True
            else:
                douban_duplicate = False
                LoginInfo.objects.filter(id=login_db_id).update(douban_id=douban.uid)
        else:
            qzone.get_access_token(code=code)
            lst = LoginInfo.objects.filter(qzone_id__exact=qzone.uid)
            if lst and lst[0].id != login_db_id:
                qzone_duplicate = True
            else:
                qzone_duplicate = False
                LoginInfo.objects.filter(id=login_db_id).update(qzone_id=qzone.uid)
    return show_result()


def cancel_qzone(request):
    global all_delete
    obj = LoginInfo.objects.get(id=login_db_id)
    if obj.qzone_id != "" and obj.weibo_id == "" and obj.douban_id == "":
        all_delete = True
        LoginInfo.objects.filter(id=login_db_id).update(qzone_id="")
        return HttpResponseRedirect('/auth/logout/')
    else:
        LoginInfo.objects.filter(id=login_db_id).update(qzone_id="")
        return show_result()


def cancel_weibo(request):
    global all_delete
    obj = LoginInfo.objects.get(id=login_db_id)
    if obj.weibo_id != "" and obj.qzone_id == "" and obj.douban_id == "":
        all_delete = True
        LoginInfo.objects.filter(id=login_db_id).update(weibo_id="")
        return HttpResponseRedirect('/auth/logout/')
    else:
        LoginInfo.objects.filter(id=login_db_id).update(weibo_id="")
        return show_result()


def cancel_douban(request):
    global all_delete
    obj = LoginInfo.objects.get(id=login_db_id)
    if obj.douban_id != "" and obj.qzone_id == "" and obj.weibo_id == "":
        all_delete = True
        LoginInfo.objects.filter(id=login_db_id).update(douban_id="")
        return HttpResponseRedirect('/auth/logout/')
    else:
        LoginInfo.objects.filter(id=login_db_id).update(douban_id="")
        return show_result()


def show_result():
    obj = LoginInfo.objects.get(id=login_db_id)
    if obj.weibo_id:
        weibo_found = True
    if obj.douban_id:
        douban_found = True
    if obj.qzone_id:
        qzone_found = True

    return render_to_response(
        'index.html', {'weibo_found': weibo_found,
                       'douban_found': douban_found,
                       'qzone_found': qzone_found,
                       'weibo_duplicate': weibo_duplicate,
                       'douban_duplicate': douban_duplicate,
                       'qzone_duplicate': qzone_duplicate,
                       'all_delete': all_delete}
    )


def logout(request):
    global login_db_id
    global weibo_found
    global douban_found
    global qzone_found
    global weibo_duplicate
    global douban_duplicate
    global qzone_duplicate
    # global all_delete

    login_db_id = None
    weibo_found = False
    douban_found = False
    qzone_found = False

    weibo_duplicate = False
    douban_duplicate = False
    qzone_duplicate = False
  
    all_delete = False
    logout(request)
    return HttpResponseRedirect('/')    
