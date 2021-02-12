from django.contrib import admin
from .models import Post, Category, Tag
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count') # 显示页面所显示的字段
    fields = ('name', 'status', 'is_nav')  # 编辑页面所显示的字段
    # fields = ('name', 'status', 'is_nav', 'owner')

    def save_model(self, request, obj, form, change):
        '''在保存数据时，将owner字段设定为当前的登录用户'''
        obj.owner = request.user    # 当前已经登录的用户，赋值给obj.owner
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        '''自定义文章数量的统计方法'''
        return obj.post_set.count()
    post_count.short_description = "文章数量"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator',
    ]
    list_display_links = []     # 配置哪些字段可以作为链接，点击它们，则可以进入编辑页面

    list_filter = ('category', )
    search_fields = ['title', 'category']

    actions_on_top = True   # 动作相关的配置，是否展示在顶部
    actions_on_bottom = True    # 动作相关的配置，是否展示在底部

    # 编辑页面
    save_on_top = True  # 保存、编辑、编辑并新建按钮是否在顶部显示

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        '''自定义函数，其参数为当前行的对象'''
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))   # 根据名称解析出URL地址
        )
    operator.short_description = '操作'   # 指定表头的展示文案

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)


