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


def login(request):
    pk = request.session.get('login_db_id', '')
    if pk:
        return HttpResponseRedirect('/account/bind/')
    else:
        return render_to_response('home.html')

def handle_data(request):
    if request.method == 'GET':
        code = request.GET.get('code', '')
        state = request.GET.get('state', '')
    pk = request.session.get('login_db_id', '')
    if pk == '':
        if state == "weibo":
            weibo.get_access_token(code=code)
            lst = LoginInfo.objects.filter(weibo_id=weibo.uid)
            if not lst:
                new = LoginInfo(weibo_id=weibo.uid, weibo_name=weibo.name)
                new.save()
                pk = new.id
            else:
                pk = lst[0].id
        elif state == "douban":
            douban.get_access_token(code=code)
            lst = LoginInfo.objects.filter(douban_id=douban.uid)
            if not lst:
                new = LoginInfo(douban_id=douban.uid, douban_name=douban.name)
                new.save()
                pk = new.id
            else:
                pk = lst[0].id
        else:
            qzone.get_access_token(code=code)
            lst = LoginInfo.objects.filter(qzone_id=qzone.uid)
            if not lst:
                new = LoginInfo(qzone_id=qzone.uid, qzone_name=qzone.name)
                new.save()
                pk = new.id
            else:
                pk = lst[0].id
        request.session['login_db_id'] = pk
    else:
        if state == "weibo":
            weibo.get_access_token(code=code)
            lst = LoginInfo.objects.filter(weibo_id=weibo.uid)
            if lst and lst[0].id != pk:
                return render_to_response('duplicate.html')
            else:
                LoginInfo.objects.filter(id=pk).update(weibo_id=weibo.uid)
                LoginInfo.objects.filter(id=pk).update(weibo_name=weibo.name)
        elif state == "douban":
            douban.get_access_token(code=code)
            lst = LoginInfo.objects.filter(douban_id=douban.uid)
            if lst and lst[0].id != pk:
                return render_to_response('duplicate.html')
            else:
                LoginInfo.objects.filter(id=pk).update(douban_id=douban.uid)
                LoginInfo.objects.filter(id=pk).update(douban_name=douban.name)
        else:
            qzone.get_access_token(code=code)
            lst = LoginInfo.objects.filter(qzone_id=qzone.uid)
            if lst and lst[0].id != pk:
                return render_to_response('duplicate.html')
            else:
                LoginInfo.objects.filter(id=pk).update(qzone_id=qzone.uid)
                LoginInfo.objects.filter(id=pk).update(qzone_name=qzone.name)
    return HttpResponseRedirect('/account/bind/')

def cancel_qzone(request):
    LoginInfo.objects.filter(
        id=request.session['login_db_id']).update(qzone_id='')
    LoginInfo.objects.filter(
        id=request.session['login_db_id']).update(qzone_name='')
    return HttpResponseRedirect('/account/bind/')

def cancel_weibo(request):
    LoginInfo.objects.filter(
        id=request.session['login_db_id']).update(weibo_id='')
    LoginInfo.objects.filter(
        id=request.session['login_db_id']).update(weibo_name='')
    return HttpResponseRedirect('/account/bind/')

def cancel_douban(request):
    LoginInfo.objects.filter(
        id=request.session['login_db_id']).update(douban_id='')
    LoginInfo.objects.filter(
        id=request.session['login_db_id']).update(douban_name='')
    return HttpResponseRedirect('/account/bind/')

def delete_account(request):
    LoginInfo.objects.filter(id=request.session['login_db_id']).delete()
    return HttpResponseRedirect('/auth/logout/')

def show_result(request):
    if request.session.get('login_db_id', ''):
        obj = LoginInfo.objects.filter(id=request.session['login_db_id'])
        if len(obj) == 0:
            request.session['login_db_id'] = ''
            return HttpResponseRedirect('/')
        else:
            obj = obj[0]
    else:
        return HttpResponseRedirect('/')

    lst = [obj.weibo_id, obj.douban_id, obj.qzone_id]
    count = 0
    for i in xrange(len(lst)):
        if lst[i]:
            count += 1

    return render_to_response(
        'index.html', {'weibo_found': True if obj.weibo_id else False,
                       'douban_found': True if obj.douban_id else False,
                       'qzone_found': True if obj.qzone_id else False,
                       'remain_one': True if count == 1 else False,
                       'weibo_name': obj.weibo_name if obj.weibo_name else '',
                       'douban_name': obj.douban_name if obj.douban_name else '',
                       'qzone_name': obj.qzone_name if obj.qzone_name else ''}
    )

def logout(request):
    del request.session['login_db_id']
    return HttpResponseRedirect('/')
