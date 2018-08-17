from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import form
import hashlib


def index(request):
    pass
    return render(request, 'mysite/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = form.UserForm(request.POST)
        message = "所有字段都要填写!"
        if login_form.is_valid():
            user_name = login_form.cleaned_data['user_name']
            password = login_form.cleaned_data['password']
            try:
                user = models.ShopUser.objects.get(user_name=user_name)
                if hash_code(password) == user.password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'mysite/login.html', locals())
    login_form = form.UserForm()
    return render(request, 'mysite/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect("/index/")


def register(request):
    if request.method == 'POST':
        register_form = form.RegisterForm(request.POST)
        message = "请检查填写的内容!"
        if register_form.is_valid():
            user_name = register_form.cleaned_data['user_name']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            real_name = register_form.cleaned_data['real_name']
            company = register_form.cleaned_data['company']
            if password1 != password2:
                message = "两次输入密码不同！"
                return render(request, 'mysite/register.html', locals())
            else:
                is_same_name = models.ShopUser.objects.filter(user_name=user_name)
                if is_same_name:
                    message = "用户名已存在！"
                    return render(request, 'mysite/register.html', locals())
                is_same_email = models.ShopUser.objects.filter(email=email)
                if is_same_email:
                    message = "邮箱已被注册!"
                    return render(request, 'mysite/register.html', locals())

                new_user = models.ShopUser()
                new_user.user_name = user_name
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.real_name = real_name
                new_user.company = company
                new_user.save()
                return redirect('/login/')
    register_form = form.RegisterForm()
    return render(request, 'mysite/register.html', locals())


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
