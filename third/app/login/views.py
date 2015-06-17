# encoding: utf-8

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import User


class UserForm(forms.Form):
	username = forms.CharField(label='用户名', max_length=100)
	password = forms.CharField(label='密码', widget=forms.PasswordInput())


def login(request):
	return render_to_response('login/home.html')


def register(request):
	if request.method == "POST":
		uf = UserForm(request.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			User.objects.create(username=username, password=password)
			return HttpResponse('regist success')
	else:
		uf=UserForm()
	return render_to_response('login/register.html', {'uf': uf})

# def login(req):
#     if req.method == 'POST':
#         uf = UserForm(req.POST)
#         if uf.is_valid():
#             username = uf.cleaned_data['username']
#             password = uf.cleaned_data['password']
#             user = User.objects.filter(username__exact = username,password__exact = password)
#             if user:
#                 response = HttpResponseRedirect('/auth/index/')
#                 response.set_cookie('username',username,3600)
#                 return response
#             else:
#                 return HttpResponseRedirect('/auth/login/')
#     else:
#         uf = UserForm()
#     return render_to_response('account/login.html',{'uf':uf},context_instance=RequestContext(req))

def index(request):
	username = request.COOKIES.get('user_name', '')
	return render_to_response('login/home.html', {'user_name': username})

	def logout(request):
		response = HttpResponse('logout!!')
		response.delete_cookie('username')
		return response


