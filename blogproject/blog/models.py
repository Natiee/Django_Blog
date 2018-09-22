import markdown
from django.db import models
from django.urls import reverse
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags


class Category(models.Model):
    """
    分类
    Django模型必须继承models.Model类
    CharField,max_length=100
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签
    CharField,max_length=100
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章标题;
    文章正文;
    创建时间;
    最后修改时间;
    文章摘要;
    作者
    """
    # 标题
    title = models.CharField(max_length=70)

    # 正文,使用TextField
    body = models.TextField()

    # 创建时间和最后修改时间,使用DateTiemField
    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要 可以为空,blank=True
    excerpt = models.CharField(max_length=200,blank=True)

    category = models.ForeignKey(Category)  # 一对多关系,一篇文章只能对一个分类
    tags = models.ManyToManyField(Tag,blank=True)  # 多对多关系,一个文章可以有多个标签,一个标签有多个文章

    # 作者,使用原生的user
    author = models.ForeignKey(User)

    # views字段记录阅读量
    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        """统计阅读量"""
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    # 自定义get_absolute_url方法
    # 记得要从django.urls中导入reverse函数
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """文章摘要"""
        # 如果没有填写摘要
        if not self.excerpt:
            # 实例化一个Markdown 类,用于渲染body的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save方法 保存到数据库
        super(Post, self).save(*args, **kwargs)


    class Meta:
        """统一以降序排序"""
        ordering = ['-create_time']