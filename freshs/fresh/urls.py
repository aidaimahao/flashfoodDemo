from django.urls import path,re_path,include
from fresh import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('index/', views.index),
    path('logout/', views.logout),
    path('store_add/', views.store_add),
    path('goods_add/', views.goods_add),
    re_path('goods_show/(?P<state>\w+)', views.goods_show),
    path('goods_detail/', views.goods_detail),
    path('goods_edit/', views.goods_edit),
    path('goods_delete/', views.goods_delete),
    re_path(r'goods_set/(?P<state>\w+)', views.goods_set),
    path('home/', views.home),
    path('person_edit/', views.person_edit),
    path('goods_type_show/', views.good_type_show),
    path('goods_type_add/', views.goods_type_add),
    path('goods_type_delete/', views.goods_type_delete),
    path('goods_type_edit/', views.goods_type_edit),
    path('ajaxshow/', views.ajaxshow),

    path('blank/', views.blank),
    path('base/', views.base),

    path('', views.index),

]