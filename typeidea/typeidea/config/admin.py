from django.contrib import admin
from .models import Link, SideBar
from django.contrib.admin.models import LogEntry

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    '''友联'''
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

    def save_model(self, request, obj, form, change):
        '''在保存数据时，将owner字段设定为当前的登录用户'''
        obj.owner = request.user    # 当前已经登录的用户，赋值给obj.owner
        return super(LinkAdmin, self).save_model(request, obj, form, change)

@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    '''侧边栏'''
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        '''在保存数据时，将owner字段设定为当前的登录用户'''
        obj.owner = request.user    # 当前已经登录的用户，赋值给obj.owner
        return super(SideBarAdmin, self).save_model(request, obj, form, change)

@admin.register(LogEntry, site=admin.site)
class LogEntryAdmin(admin.ModelAdmin):
    '''日志记录'''
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']


