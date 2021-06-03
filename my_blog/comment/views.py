from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from article.models import ArticlePost
from .forms import CommentForm

# 文章评论
def post_comment(request, article_id):
    article = get_object_or_404(ArticlePost, id=article_id)

    comment_form = CommentForm(request.GET)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.article = article
        new_comment.save()
        return redirect(article)
    else:
        context = {'errtxt': '表单内容有误，请重新填写', 'atc': article}
        return render(request, 'cmt404.html', context)


