import markdown
from django.shortcuts import render,get_object_or_404
from .models import Post
# Create your views here.
from django.http import HttpResponse
from markdown.extensions.toc import TocExtension


def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


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
    return render(request,'blog/detail.html',context={'post':post})