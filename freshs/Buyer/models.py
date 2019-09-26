from django.db import models
from django.db.models import manager


# Create your models here.

class Buyer(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=11,verbose_name='密码')
    phone = models.CharField(max_length=16,verbose_name='电话',null=True)
    email = models.EmailField(verbose_name='邮箱')
    connect_address = models.TextField(verbose_name='联系地址',null=True)

class Address(models.Model):
    """
    收货地址
    """
    address = models.TextField(verbose_name='收货地址')
    reciver = models.CharField(max_length=32,verbose_name='接件人')
    recv_phone = models.CharField(max_length=32,verbose_name='接件人电话')
    post_number = models.CharField(max_length=32,verbose_name='邮编')
    buy_id = models.ForeignKey(to='Buyer',on_delete=models.CASCADE,verbose_name='买家id')


class Order(models.Model):
    """
    订单表
    """
    order_id = models.CharField(max_length=32,verbose_name='订单编号')
    goods_count = models.IntegerField(verbose_name='商品数量')
    order_user = models.ForeignKey(to='Buyer',on_delete=models.CASCADE,verbose_name='订单用户')
    order_address = models.ForeignKey(to='Address',on_delete=models.CASCADE,null=True,verbose_name='订单地址')
    order_totalprice = models.FloatField(verbose_name='订单总价')
    order_status = models.IntegerField(verbose_name='订单状态',default=1)


class OrderDetail(models.Model):
    order_id = models.ForeignKey(to='Order',on_delete=models.CASCADE,verbose_name='订单编号')
    goods_id = models.IntegerField(verbose_name='商品id')
    goods_name  = models.CharField(max_length=32,verbose_name='商品名称')
    goods_price = models.FloatField(verbose_name='商品价格')
    goods_number = models.IntegerField(verbose_name='商品购买数量')
    goods_total = models.FloatField(verbose_name='商品总价')
    goods_store = models.IntegerField(verbose_name='商店id')
    goods_img = models.ImageField(verbose_name='商品图片')


class Cart(models.Model):
    goods_name = models.CharField(max_length=32,verbose_name='商品名称')
    goods_price = models.FloatField(verbose_name='商品价格')
    goods_totalprice = models.FloatField(verbose_name='商品总价')
    goods_number  = models.IntegerField(verbose_name='商品数量')
    goods_img = models.ImageField(verbose_name='商品图片',upload_to='buyer/image')
    goods_id = models.IntegerField(verbose_name='商品id')
    goods_store = models.IntegerField(verbose_name='商铺id')
    user_id = models.IntegerField(verbose_name='用户id')

