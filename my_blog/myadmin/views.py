from django.shortcuts import render, redirect
from django.http import HttpResponse
from article.models import ArticlePost, ArticleColumn
from article.forms import ArticlePostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import markdown
from comment.models import Comment

# 后台主页
# 检查登录
@login_required(login_url='/userprofile/login/')
def home(request):
    # 取出所有博客文章（数据表的属性值）
    article_list = ArticlePost.objects.all()
    # 获取博客文章数据表的所有属性
    article_attrs = ArticlePost._meta.fields
    # 将所有文章放入需要传递给模板的字典中
    context = {'article_attrs': article_attrs, 'article_list': article_list}
    return render(request, 'myadmin/home.html', context)  

# 后台查看文章详情
# 检查登录
@login_required(login_url='/userprofile/login/')
def article_detail(re, id):
    article = ArticlePost.objects.get(id=id)

    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    context = {'article': article}
    return render(re, 'myadmin/article_detail.html', context)

# 检查登录
@login_required(login_url='/userprofile/login/')
def create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定登录用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
                
            # 将新文章保存到数据库中
            new_article.save()
            return redirect("myadmin:admin_home")
        
        # 如果数据不合法，返回错误信息
        else:
            context = {'errtxt': '表单内容有误，请重新填写'}
            return render(request, 'myadmin/404.html', context)

    # 如果用户请求获取数据
    else:
        # GET请求表示显示空表单
        columns = ArticleColumn.objects.all()
        context = {  'columns': columns }
        return render(request, 'myadmin/create.html', context)

# 文章删除界面
# 检查登录
@login_required(login_url='/userprofile/login/')
def delete(d):
    # 取出所有博客文章（数据表的属性值）
    article_list = ArticlePost.objects.all()
    context = {'article_list': article_list}
    return render(d, 'myadmin/delete.html', context)

# 删除某篇文章
# 检查登录
@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.body = markdown.markdown(article.body,
                                    extensions=[
                                        # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    context = {'article': article}
    return render(request, 'myadmin/delete_article.html', context)

# 安全删除某篇文章
# 检查登录
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':    
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("myadmin:admin_home")
    else:
        return HttpResponse("仅允许post请求")

# 文章更新界面  
# # 检查登录
@login_required(login_url='/userprofile/login/')     
def update(u):
    article_list = ArticlePost.objects.all()
    context = {'article_list': article_list}
    return render(u, 'myadmin/update.html', context)

# 更新文章
# 检查登录
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
                
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("myadmin:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = { 'article': article,  'columns': columns, }
        # 将响应返回到模板中
        return render(request, 'myadmin/update_article.html', context)
    
# 数据统计
@login_required(login_url='/userprofile/login/')
def chart(c):
    return render(c, 'myadmin/chart.html')

# 评论管理
@login_required(login_url='/userprofile/login/')
def comment(c):
    comments = Comment.objects.all()
    contxt = {'cmts': comments}
    return render(c, 'myadmin/comment.html', contxt)

# 评论删除
def comment_delete(request, id):
        comment = Comment.objects.get(id=id)
        comment.delete()
        return redirect("myadmin:comment")
