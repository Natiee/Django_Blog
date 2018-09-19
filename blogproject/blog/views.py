from django.shortcuts import render
from .models import Post
# Create your views here.
from django.http import HttpResponse


def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})