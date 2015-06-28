# encoding: utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

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


def login(request):
    pk = request.session.get('login_db_id', '')
    if pk:
        return HttpResponseRedirect('/account/bind/')
    else:
        return render_to_response('home.html')


def handle_data(request):
    global douban_name
    global weibo_name
    global qzone_name

    if request.method == 'GET':
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')
    pk = request.session.get('login_db_id', '')
    if pk == '':
        if state == "weibo":
            weibo.get_access_token(code=code)
            lst = LoginInfo.objects.filter(weibo_id=weibo.uid)
            if not lst:
                new = LoginInfo(weibo_id=weibo.uid)
                new.save()
                pk = new.id
            else:
                pk = lst[0].id
            weibo_name = weibo.name
        elif state == "douban":
            douban.get_access_token(code=code)
            lst = LoginInfo.objects.filter(douban_id=douban.uid)
            if not lst:
                new = LoginInfo(douban_id=douban.uid)
                new.save()
                pk = new.id
            else:
                pk = lst[0].id
            douban_name = douban.name
        else:
            qzone.get_access_token(code=code)
            lst = LoginInfo.objects.filter(qzone_id=qzone.uid)
            if not lst:
                new = LoginInfo(qzone_id=qzone.uid)
                new.save()
                pk = new.id
            else:
                pk = lst[0].id
            qzone_name = qzone.name
        request.session['login_db_id'] = pk
    else:
        if state == "weibo":
            weibo.get_access_token(code=code)
            lst = LoginInfo.objects.filter(weibo_id=weibo.uid)
            if lst and lst[0].id != pk:
                return render_to_response('duplicate.html')
            else:
                LoginInfo.objects.filter(id=pk).update(weibo_id=weibo.uid)
                weibo_name = weibo.name

        elif state == "douban":
            douban.get_access_token(code=code)
            lst = LoginInfo.objects.filter(douban_id=douban.uid)
            if lst and lst[0].id != pk:
                return render_to_response('duplicate.html')
            else:
                LoginInfo.objects.filter(
                    id=pk).update(douban_id=douban.uid)
                douban_name = douban.name
        else:
            qzone.get_access_token(code=code)
            lst = LoginInfo.objects.filter(qzone_id=qzone.uid)
            if lst and lst[0].id != pk:
                return render_to_response('duplicate.html')
            else:
                LoginInfo.objects.filter(id=pk).update(qzone_id=qzone.uid)
                qzone_name = qzone.name
    return HttpResponseRedirect('/account/bind/')


def cancel_qzone(request):
    global qzone_name
    LoginInfo.objects.filter(
        id=request.session['login_db_id']).update(qzone_id="")
    qzone_name = ""
    return HttpResponseRedirect('/account/bind/')


def cancel_weibo(request):
    global weibo_name
    LoginInfo.objects.filter(
        id=request.session['login_db_id']).update(weibo_id="")
    weibo_name = ""
    return HttpResponseRedirect('/account/bind/')


def cancel_douban(request):
    global douban_name
    LoginInfo.objects.filter(
        id=request.session['login_db_id']).update(douban_id="")
    douban_name = ""
    return HttpResponseRedirect('/account/bind/')


def delete_account(request):
    LoginInfo.objects.filter(id=request.session['login_db_id']).delete()
    return HttpResponseRedirect('/auth/logout/')


def show_result(request):
    weibo_found = False
    douban_found = False
    qzone_found = False
    remain_one = False

    obj = LoginInfo.objects.filter(id=request.session['login_db_id'])

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
    del request.session['login_db_id']
    douban_name = ""
    weibo_name = ""
    qzone_name = ""

    return HttpResponseRedirect('/')
