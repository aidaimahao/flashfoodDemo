# import hashlib
# def secret_pwd(password):
#     md = hashlib.md5()
#     password = password.encode()
#     md .update(password)
#     return md.hexdigest()
#
# pwd = secret_pwd('123')
# print(pwd)
import os
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freshs.settings')
    import django
    django.setup()
    from fresh import models
    goods = models.Goods.objects.getone()
    print(goods)
