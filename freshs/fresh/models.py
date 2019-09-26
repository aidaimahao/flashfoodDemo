from django.db import models
from django.db.models import Manager


class GoodsManage(Manager):
    def up_goods(self):
        """
        返回上架商品
        :return:
        """
        return Goods.objects.filter(goods_down=1)
    def getone(self):
        return Goods.objects.all().first()

# Create your models here.
#  卖家
class Seller(models.Model):
    username = models.CharField(max_length=20,verbose_name='用户名')
    password = models.CharField(max_length=20,verbose_name='密码')
    nickname = models.CharField(max_length=20,verbose_name='昵称')
    phone = models.CharField(max_length=20,verbose_name='电话')
    email = models.EmailField(verbose_name='邮箱')
    picture = models.ImageField(upload_to='fresh/images/',verbose_name='头像',blank=True)
    address = models.CharField(max_length=20,verbose_name='地址',null=True,blank=True)
    card_id = models.CharField(max_length=20,verbose_name='身份证',null=True,blank=True)

    def __str__(self):
        return self.username
# 店铺
class Store(models.Model):
    store_name = models.CharField(max_length=20,verbose_name='店铺名称')
    store_address = models.CharField(max_length=20,verbose_name='店铺地址')
    store_description = models.TextField(verbose_name='店铺描述')
    store_logo = models.ImageField(upload_to='fresh/images/',verbose_name='店铺图片')
    store_phone = models.CharField(max_length=22,verbose_name='店铺电话')
    user_id = models.IntegerField(verbose_name='店铺主人')
    store_type = models.ManyToManyField(to='StoreType',verbose_name='店铺类型')

    def __str__(self):
        return self.store_name
# 店铺类型
class StoreType(models.Model):
    type_name = models.CharField(max_length=20)
    type_dep = models.TextField()

    def __str__(self):
        return self.type_name

# 商品
class Goods(models.Model):
    goods_name = models.CharField(max_length=20,verbose_name='商品名称')
    goods_price = models.FloatField(verbose_name='商品价格')
    goods_image = models.ImageField(upload_to='fresh/images/',verbose_name='商品图片')
    goods_number = models.IntegerField(verbose_name='商品库存')
    goods_descirption = models.TextField(verbose_name='商品描述')
    goods_date = models.DateField(verbose_name='出厂日期')
    goods_safeDate = models.IntegerField(verbose_name='保质期')
    goods_down = models.CharField(max_length=10,default=1,verbose_name='上架')# 1为上架 0为下架
    store_id = models.ManyToManyField(to='Store',related_name='store',verbose_name='商品店铺')
    goods_type = models.ForeignKey(to='Goods_type',on_delete=models.CASCADE,default=1,verbose_name='商品类型')

    objects = GoodsManage()

    def __str__(self):
        return self.goods_name
# 商品图片表，
class GoodsImg(models.Model):
    img_address = models.ImageField(upload_to='fresh/images/',verbose_name='图片地址')
    img_description = models.TextField(verbose_name='图片描述')
    goods_id = models.ForeignKey(to='Goods',on_delete=models.CASCADE,verbose_name='商品id')

    def __str__(self):
        return self.img_address

class Goods_type(models.Model):
    type_name = models.CharField(max_length=20,verbose_name='商品类型名称')
    type_img = models.ImageField(upload_to='fresh/images/',verbose_name='商品图片')
    type_description = models.TextField(verbose_name='类型介绍')

    def __str__(self):
        return self.type_name