from django.contrib import admin
from .models import Post, Category, Tag
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry


class PostInLine(admin.TabularInline):
    '''设置内置的编辑操作，包括字段，模块'''
    fields = ('title', 'desc')
    extra = 1      # 默认内置编辑操作的数量
    model = Post

@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInLine, ]    # 在“分类”页，内置“添加文章”的操作

    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time', 'post_count') # 显示页面所显示的字段
    fields = ('name', 'status', 'is_nav')  # 编辑页面所显示的字段
    # fields = ('name', 'status', 'is_nav', 'owner')

    # def save_model(self, request, obj, form, change):
    #     '''在保存数据时，将owner字段设定为当前的登录用户'''
    #     obj.owner = request.user    # 当前已经登录的用户，赋值给obj.owner
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        '''自定义文章数量的统计方法'''
        return obj.post_set.count()
    post_count.short_description = "文章数量"

@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)

class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户分类'''
    title = "分类过滤"     # 用于展示标题
    parameter_name = 'owner_category'       # 设置查询时URL参数的名字，如查询分类id为1的内容时，URL后面的Query部分是?owner_category=1

    def lookups(self, request, model_admin):
        '''返回要展示的内容和查询用的id'''
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        '''根据URL Query的内容返回列表页数据'''
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset

#@admin.register(Post)
@admin.register(Post, site=custom_site)     # 将“文章”模块的后台分隔到自定义custom_site中
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm    # form为固定名称
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator',
    ]
    list_display_links = []     # 配置哪些字段可以作为链接，点击它们，则可以进入编辑页面

    # list_filter = ('category', )
    list_filter = [CategoryOwnerFilter]     # 自定义“分类过滤器”
    search_fields = ['title', 'category__name']     # category是外键，所以得写成category__name，指明其是外键

    actions_on_top = True   # 动作相关的配置，是否展示在顶部
    actions_on_bottom = True    # 动作相关的配置，是否展示在底部

    # 编辑页面
    save_on_top = True  # 保存、编辑、编辑并新建按钮是否在顶部显示

    # exclude = ('owner',)    # 设置该字段不展示

    # fields限定要展示的字段，及要配置展示字段的顺序
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    #     'owner',
    # )

    # fieldsets用来控制布局，格式为两个元素的tuple的list
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        }),
    )

    def operator(self, obj):
        '''自定义函数，其参数为当前行的对象'''
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('admin:blog_post_change', args=(obj.id,))   # 根据名称解析出URL地址
            reverse('cus_admin:blog_post_change', args=(obj.id,))  # 根据名称解析出URL地址
        )
    operator.short_description = '操作'   # 指定表头的展示文案

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # def get_queryset(self, request):
    #     '''自定义列表页数据，让当前登录的用户只能看到自己创建的文章'''
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # class Media:
    #     '''通过自定义Media类来往页面上添加想要添加的JavaScript以及css资源'''
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #     js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)

@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    '''增加操作日志查看'''
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']





