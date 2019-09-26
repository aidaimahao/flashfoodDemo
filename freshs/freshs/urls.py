"""freshs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include,re_path
from django.views.static import serve
from django.conf import settings
from Buyer import views as vb
from rest_framework import  routers
from fresh import views as vf
# 生命一个默认的路由注册器
routers = routers.DefaultRouter()
routers.register(r'goods',vf.UserViewSet)
routers.register(r'goodsType',vf.TypeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buy/', include('Buyer.urls')),
    path('fresh/', include('fresh.urls')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root':settings.MEDIA_ROOT}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path('^API',include(routers.urls)), # restful 根路由
    re_path('^api-auth',include('rest_framework.urls')) # 接口认证

]
