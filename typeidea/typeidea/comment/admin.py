from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')     # 列表展示的字段
    fields = ('target', 'nickname', 'content')      # 编辑页的字段




