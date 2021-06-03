from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# 别忘了引入模块
from .forms import ProfileForm
from .models import Profile

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            
            # .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect("myadmin:admin_home")
            else:
                context = {'errtxt': '账号或密码输入有误'}
                return render(request, '404.html', context)
        else:
            context = {'errtxt': '账号或密码输入不合法'}
            return render(request, '404.html', context)
    elif request.method == 'GET':
        return render(request, 'userprofile/login.html')
    else:
        context = {'errtxt': '请使用GET或POST请求数据'}
        return render(request, '404.html', context)

# 用户退出
# 检查登录
@login_required(login_url='/userprofile/login/')
def user_logout(request):
    logout(request)
    return redirect("my_home")

# 注册用户
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form':user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('"请使用GET或POST请求数据"')

# 删除用户
@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 验证待删除用户与当前登录用户是否是同一人
        if request.user == user:
            # 退出登录并删除用户
            logout(request)
            user.delete()
            return redirect('userprofile:login')
        else:
            return HttpResponse('您没有删除用户的权限')
    else:
        return HttpResponse('仅接受POST请求！')

# 编辑用户信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)

    # 旧代码
    # user_id 是 OneToOneField 自动生成的字段
    # profile = Profile.objects.get(user_id=id)
    # 修改后的代码
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")
            
        # 修改本行 
        # profile_form = ProfileForm(data=request.POST)
        # 上传的文件保存在 request.FILES 中，通过参数传递给表单类
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            # 如果 request.FILES 存在文件，则保存
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]

            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        # 实际上GET方法中不需要将profile_form这个表单对象传递到模板中去，因为模板中已经用Bootstrap写好了表单，所以profile_form并没有用到。
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")





