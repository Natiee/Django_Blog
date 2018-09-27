import markdown
from django.shortcuts import render,get_object_or_404
from .models import Post, Category,Tag
from comments.forms import CommentForm
from django.views.generic import ListView,DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    # 指定paginator,每一页多少篇文章
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        类视图中,需要传递的模板变量字典是通过get_context_data获得
        所以重写该方法,以便能够插入一些自定义模板变量
        """
        # 获取父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)

        # 从context中获取paginator,page,is_paginated
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')  # 是否分页

        # 调用自己写的 pagination_data方法获取显示分页导航需要的数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 更新到context中
        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页,则无需显示分页导航条,不用数据
            return {}

        # 当前页左边连续的页码号,初始为空
        left = []
        # 当前页右边连续的页码号,初始为空
        right = []

        # 第1页页码后是否需要显示省略号
        left_has_more = False
        # 末页页码后是够需要显示省略号
        right_has_more = False

        # 第1页页码始终是需要显示的,初始False
        first = False
        # 末页页码显示,初始False
        last = False

        # 获取用户当前请求的页码号
        page_number = page.number

        # 获取分页后的总页数
        total_pages = paginator.num_pages

        # 获取整个分页页码列表
        page_range = paginator.page_range

        if page_number == 1:
            '''
            如果用户请求的是第1页的数据,那么当前页左边是不需要数据的,因此 left=[],已默认为空
            此时只要获取当前页右边的连续页码号,比如分页页码列表是[1,2,3,4],那么获取的就是right=[2,3]
            数值可自主更改
            '''
            right = page_range[page_number:page_number+2]

            if right[-1] < total_pages -1:
                '''
                如果最右边的页码号比末页的页码号减去1还要小,
                说明最右边的页码号和末页的页码号之间还有其他页码,因为需要显示省略号,right_has_more来指示
                '''
                right_has_more = True

            if right[-1] < total_pages:
                '''
                如果最右边的页码号比末页页码号小,说明当前页右边的连续页码号中不包含末页页码
                所以需要显示最后一页的页码号,last来指示
                '''
                last = True

        elif page_number == total_pages:
            '''
            如果用户请求的是末页的数据,那么当前页右边就不需要数据,right=[](已默认为空)
            此时只要获取当前页左边的连续页码号
            '''
            left = page_range[(page_number -3) if (page_number -3) > 0 else 0:page_number -1]

            if left[0] > 2:
                '''
                如果最左边的页码号比第2页页码号大,
                说明最左边的页码号和第1页的页码号之间还有其他页码,就需要显示省略号,left_has_more指示
                '''
                left_has_more = True

            if left[0] > 1:
                '''
                如果最左边的页码号比第1页的页码号大,说明当前页左边的连续页码号中不包含第1页的页码
                所以需要显示第1页的页码号,first指示
                '''
                first = True

        else:
            # 用户既不是第1页也不是末页,需要获取当前页左右两边的连续页码号,
            # 暂时只获取当前页码前后连续两个页码
            left = page_range[(page_number -3) if (page_number -3) > 0 else 0:page_number -1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data

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
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',  # 语法高亮扩展
                TocExtension(slugify=slugify)
            ])
        post.body = md.convert(post.body)
        post.toc = md.toc

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

class TagView(IndexView):
    """标签"""
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView,self).get_queryset().filter(tags=tag)

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})