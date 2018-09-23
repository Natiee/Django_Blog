import markdown
from django.shortcuts import render,get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

# def detail(request, pk):
#     # 如果pk对应的文章不存在,就返回404错误
#     post = get_object_or_404(Post, pk=pk)
#
#     # 阅读量+1
#     post.increase_views()
#
#     post.body = markdown.markdown(
#         post.body,
#         extensions=[
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',  # 语法高亮扩展
#             'markdown.extensions.toc',  # 自动生成目录
#         ]
#     )
#     form = CommentForm()
#
#     # 获取这篇文章下的全部评论
#     comment_list = post.comments_set.all()
#     # 将文章,表单,以及评论
#     context = {
#         'post': post,
#         'form': form,
#         'comment_list': comment_list
#     }
#
#     return render(request, 'blog/detail.html', context=context)

class PostDetailViews(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        """
        重写get方法,目的是为了可以将阅读量+1
        只有当get方法被调用后,才有self.object属性
        """
        response = super(PostDetailViews, self).get(request, *args, **kwargs)

        # 文章阅读量+1
        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        # 重写get_object方法 对post的body值进行渲染
        post = super(PostDetailViews, self).get_object(queryset=None)
        post.body = markdown.markdown(
            post.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',  # 语法高亮扩展
                'markdown.extensions.toc',  # 自动生成目录
            ])
        return post

    def get_context_data(self, **kwargs):
        """
        重写get_context_data
        目的:1.对post的body进行渲染
             2.把评论表单和评论列表传递给模板
        """
        context = super(PostDetailViews, self).get_context_data(**kwargs)
        form = CommentForm()
        # 获取这篇文章下的全部评论
        comment_list = self.object.comments_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context

class ArchivesView(IndexView):
    """归档"""
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().\
            filter(create_time__year=year,
                   create_time__month=month)

class CategoryView(IndexView):
    """分类"""
    def get_queryset(self):
        """覆写获取指定分类下的文章列表数据"""
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)