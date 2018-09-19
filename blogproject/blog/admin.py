from django.contrib import admin
from .models import Post,Category,Tag
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'category', 'author']


# 新增的PostAdmin也注册进去
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
