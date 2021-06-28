"""typeideas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .custom_site import custom_site
from django.conf.urls import url

from blog.views import post_list, post_detail
from config.views import links

urlpatterns = [
    path('', post_list),
    # url(r'^category/(?P<category_id>\d+)/$', post_list),
    # url(r'^tag/(?P<tag_id>\d+)/$', post_list),
    # url(r'^post/(?P<post_id>\d+).html$', post_detail),
    # url(r'^links/$', links),

    path('category/<int:category_id>/', post_list),
    path('tag/<int:tag_id>/', post_list),
    path('post/<post_id>/', post_detail),
    path('links/', links),

    path('super_admin/', admin.site.urls),  # 超级用户的后台admin。密码admin123456
    path('admin/', custom_site.urls),       # 普通用户的后台admin。密码admin123456

]
