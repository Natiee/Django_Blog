from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comments
from .forms import CommentForm
# Create your views here.


def post_comment(request, post_pk):

    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        # 构造实例
        form = CommentForm(request.POST)

        # 校验数据是否符合要求
        if form.is_valid():

            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来。
            comment.post = post

            # 最终将评论数据保存进数据库
            comment.save()

            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        else:
            comment_list = post.comments_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)

    return redirect(post)

