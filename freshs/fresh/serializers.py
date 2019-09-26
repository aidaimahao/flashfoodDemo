from rest_framework import serializers
from fresh import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    声明数据,序列化
    """
    class Meta:# 元类
        model = models.Goods # 要进行接口序列化的模型
        fields = ['goods_name','goods_price','goods_number']# 序列返回的字段

class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Goods_type
        fields = ['type_name','type_description']
