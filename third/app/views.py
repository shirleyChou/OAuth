# encoding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from models import LoginInfo
from social.douban import DouBan
from social.qzone import Qzone
from social.weibo import WeiBo


douban = DouBan()
weibo = WeiBo()
qzone = Qzone()

douban_name = ""
weibo_name = ""
qzone_name = ""

login_db_id = None


def login(request):
    if login_db_id is not None:
        return show_result()
    else:
        return render_to_response('home.html')


def handle_data(request):
    global login_db_id
    global douban_name
    global weibo_name
    global qzone_name
      
    # get code and state used for getting access taken
    if request.method == 'GET':
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')
    # if it is going to login
    if login_db_id is None:
        # if user login using weibo
        if state == "weibo":
            # use code(状态码) to access weibo uid
            weibo.get_access_token(code=code)
            # whether or not the user is registered 
            lst = LoginInfo.objects.filter(weibo_id=weibo.uid)
            # if is not, create record into database
            if not lst:
                new = LoginInfo(weibo_id=weibo.uid)
                new.save()
            # login_db_id used for recognizing which row of data(a user) login
                login_db_id = new.id
            else:
                login_db_id = lst[0].id
            weibo_name = weibo.name
        elif state == "douban":
            douban.get_access_token(code=code)
            lst = LoginInfo.objects.filter(douban_id=douban.uid)
            if not lst:
                new = LoginInfo(douban_id=douban.uid)
                new.save()
                login_db_id = new.id
            else:
                login_db_id = lst[0].id
            douban_name = douban.name
        else:
            qzone.get_access_token(code=code)
            lst = LoginInfo.objects.filter(qzone_id=qzone.uid)
            if not lst:
                new = LoginInfo(qzone_id=qzone.uid)
                new.save()
                login_db_id = new.id
            else:
                login_db_id = lst[0].id
            qzone_name = qzone.name
    # if user has login to the website, 
    # and user want to bind another social account
    else:
        # if user want to bind weibo
        if state == "weibo":
            weibo.get_access_token(code=code)
            lst = LoginInfo.objects.filter(weibo_id=weibo.uid)
            # but weibo accout exist in the database, 
            # which means another user has binded to this account
            if lst and lst[0].id != login_db_id:
                return render_to_response('duplicate.html')
            else:
                LoginInfo.objects.filter(id=login_db_id).update(weibo_id=weibo.uid)
                weibo_name = weibo.name

        elif state == "douban":
            douban.get_access_token(code=code)
            lst = LoginInfo.objects.filter(douban_id=douban.uid)
            if lst and lst[0].id != login_db_id:
                return render_to_response('duplicate.html')
            else:
                LoginInfo.objects.filter(id=login_db_id).update(douban_id=douban.uid)
                douban_name = douban.name
        else:
            qzone.get_access_token(code=code)
            lst = LoginInfo.objects.filter(qzone_id=qzone.uid)
            if lst and lst[0].id != login_db_id:
                return render_to_response('duplicate.html')
            else:
                LoginInfo.objects.filter(id=login_db_id).update(qzone_id=qzone.uid)
                qzone_name = qzone.name
    return HttpResponseRedirect('/account/bind/')


def cancel_qzone(request):
    global qzone_name
    LoginInfo.objects.filter(id=login_db_id).update(qzone_id="")
    qzone_name = ""
    return HttpResponseRedirect('/account/bind/')


def cancel_weibo(request):
    global weibo_name
    LoginInfo.objects.filter(id=login_db_id).update(weibo_id="")
    weibo_name = ""
    return HttpResponseRedirect('/account/bind/')


def cancel_douban(request):
    global douban_name
    LoginInfo.objects.filter(id=login_db_id).update(douban_id="")
    douban_name = ""
    return HttpResponseRedirect('/account/bind/')


def delete_account(request):
    LoginInfo.objects.filter(id=login_db_id).delete()
    return HttpResponseRedirect('/auth/logout/')


def show_result(request):
    weibo_found = Falseg
    douban_found = False
    qzone_found = False
    remain_one = False

    obj = LoginInfo.objects.get(id=login_db_id)
    if obj.weibo_id:
        weibo_found = True
    if obj.douban_id:
        douban_found = True
    if obj.qzone_id:
        qzone_found = True

    if weibo_found is True and douban_found is False and qzone_found is False:
        remain_one = True
    if weibo_found is False and douban_found is True and qzone_found is False:
        remain_one = True
    if weibo_found is False and douban_found is False and qzone_found is True:
        remain_one = True

    return render_to_response(
        'index.html', {'weibo_found': weibo_found,
                       'douban_found': douban_found,
                       'qzone_found': qzone_found,
                       'remain_one': remain_one,
                       'weibo_name': weibo_name,
                       'douban_name': douban_name,
                       'qzone_name': qzone_name}
    )


def logout(request):
    global login_db_id

    login_db_id = None
    douban_name = ""
    weibo_name = ""
    qzone_name = ""

    return HttpResponseRedirect('/')    
