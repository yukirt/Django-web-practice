from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from mysite import models, forms
from django.contrib.sessions.models import Session
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request, pid=None, del_pass=None):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
        try:
            user = models.User.objects.get(username=username)
            diaries = models.Diary.objects.filter(user=user).order_by("-ddate")
        except:
            pass
    messages.get_messages(request)
    return render(request, 'index.html', locals())

def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['user_name'].strip()
            login_password = request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, "成功登入了！")
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, "帳號尚未啟用！")
            else:
                messages.add_message(request, messages.WARNING, "登入失敗")
        else:
            messages.add_message(request, messages.INFO, "請檢查輸入的欄位內容")
    else:
        login_form = forms.LoginForm()
    return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功登出了！")
    return redirect('/')

@login_required(login_url="/login/")
def userinfo(request):
    if request.user.is_authenticated:
        username = request.user.username
        try:
            user = User.objects.get(username=username)
            profile = models.Profile.objects.get(user=user)
        except:
            profile = models.Profile(user=user)

        if request.method == "POST":
            profile_form = forms.ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                messages.add_message(request, messages.INFO, "個人資料已儲存")
                profile_form.save()
                return HttpResponseRedirect('/userinfo')
            else:
                messages.add_message(request, messages.INFO, "要修改個人資料，每一個欄位都要填！")
        else:
            profile_form = forms.ProfileForm()
    return render(request, 'userinfo.html', locals())


@login_required(login_url="/login/")
def posting(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)

    if request.method == "POST":
        user = User.objects.get(username=username)
        diary = models.Diary(user=user)
        post_form = forms.DiaryForm(request.POST, instance=diary)
        if post_form.is_valid():
            messages.add_message(request, messages.INFO, "日記已儲存！")
            post_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, "要張貼日記，每一個欄位都要填！")
    else:
        post_form = forms.DiaryForm()
        messages.add_message(request, messages.INFO, "要張貼日記，每一個欄位都要填！")
    return render(request, 'posting.html', locals())
