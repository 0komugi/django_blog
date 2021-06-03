from .models import ArticlePost, ArticleColumn
from comment.models import Comment
from comment.forms import CommentForm
import markdown
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# 引入分页模块
from django.core.paginator import Paginator
# 如果想对多个参数进行查询怎么办？比如同时查询文章标题和正文内容。这时候就需要Q对象
from django.db.models import Q

# 视图函数


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    # 每页显示 3 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    
    comment_count = {}
    for article in articles:
        comment_count[article.id] = len(Comment.objects.filter(article=article.id))
    
    # 取出需要传递给模板templates的对象
    context = {'articles': articles, 'order': order, 'search': search, 'cmt_ct': comment_count }

    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)

# 文章详情


def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)

    
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    
    # 取出文章评论
    comments = Comment.objects.filter(article=id)

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         # 包含 缩写、表格等常用扩展
                                         'markdown.extensions.extra',
                                         # 语法高亮扩展
                                         'markdown.extensions.codehilite',
                                     ])
    # 需要传递给模板的对象
    comment_form = CommentForm()
        
    comment_count = len(Comment.objects.filter(article=id))

    context = { 'article': article, 'comments': comments,'comment_form': comment_form, 'cmt_ct': comment_count }
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

# 检查登录


@login_required(login_url='/userprofile/login/')
# 写文章的视图
def article_create(request):
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
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 增加栏目的上下文，以便模板使用
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns}
        # 返回模板
        return render(request, 'article/create.html', context)

# 更新文章
# 提醒用户登录


@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            # 栏目
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(
                    id=request.POST['column'])
            else:
                article.column = None

            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article,
                   'article_post_form': article_post_form, 'columns': columns, }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)

# 数据查看
def chart(c):
    return render(c, 'article/chart.html')
