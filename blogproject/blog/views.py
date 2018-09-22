import markdown
from django.shortcuts import render,get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
# Create your views here.
from django.http import HttpResponse
from markdown.extensions.toc import TocExtension


def index(request):
    post_list = Post.objects.all().order_by('-create_time')

    context = {
        'post_list': post_list,

    }
    return render(request, 'blog/index.html', context=context)


def detail(request, pk):
    # 如果pk对应的文章不存在,就返回404错误
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(
        post.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',  # 语法高亮扩展
            'markdown.extensions.toc',  # 自动生成目录
        ]
    )
    form = CommentForm()

    # 获取这篇文章下的全部评论
    comment_list = post.comments_set.all()
    # 将文章,表单,以及评论
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }

    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):
    """归档页面"""
    post_list = Post.objects.filter(
        create_time__year=year,
        create_time__month=month).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})


def category(request, pk):
    """分类页面"""
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})