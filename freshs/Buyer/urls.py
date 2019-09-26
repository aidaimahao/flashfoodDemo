from django.urls import path,include,re_path
from Buyer import views
urlpatterns = [
    path('index/',views.index),
    path('login/',views.login),
    path('register/',views.register),
    path('logout/',views.logout),
    path('home/',views.home),
    path('shoppingcart/',views.shoppingcart),
    path('addCart/',views.addCart),
    path('order/',views.order),
    path('goods_list/',views.goods_list),
    path('detail/',views.detail),
    path('place_order/',views.place_order),
    path('pay_order/',views.pay_order),
    path('pay_result/',views.pay_result),

]