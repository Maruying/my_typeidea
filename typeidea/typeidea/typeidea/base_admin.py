
# 所有App都需要用到

from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    '''
    1、用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
    2、用来针对queryset过滤当前用户的数据，只能展示当前用户的数据
    '''
    exclude = ('owner', )
    
    def get_queryset(self, request):
        '''自定义列表页数据，让当前登录的用户只能看到自己创建的文章'''
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        '''在保存数据时，将owner字段设定为当前的登录用户'''
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

