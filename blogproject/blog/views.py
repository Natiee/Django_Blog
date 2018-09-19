from django.shortcuts import render,get_object_or_404
from .models import Post
# Create your views here.
from django.http import HttpResponse


def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    # 如果pk对应的文章不存在,就返回404错误
    post = get_object_or_404(Post, pk=pk)
    return render(request,'blog/detail.html',context={'post':post})