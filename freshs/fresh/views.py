from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from rest_framework import viewsets,routers
from fresh import models,serializers
from django.core.paginator import Paginator
# Create your views here.
# def check(func):
#     @wraps(func)
#     def inner(requset,*args,**kwargs):
#         ret = requset.session.get('username')
#         if ret:
#             return func(requset,*args,**kwargs)
#         else:
#             return redirect('/login/login/')
#
#     return inner

def checklogin(func):
    def inner(request,*args,**kwargs):
        uid = request.session.get('uid')
        username = request.session.get('username')
        if uid:
            user = models.Seller.objects.filter(username=username).first()
            store = models.Store.objects.filter(user_id=user.id).first()
            if store:
                is_store = store.user_id
                if is_store:
                    request.session['is_store'] = is_store
            return func(request,*args,**kwargs)
        else:
            return redirect('/fresh/index/')
    return inner
# 登录
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 用户输入不为空
        if username and password:
            db_user = models.Seller.objects.filter(username=username).first()
            # s数据库中存在用户
            if db_user:
                db_pwd = db_user.password
                # 密码正确
                if password == db_pwd:
                    request.session['username'] = db_user.username
                    request.session['uid'] = db_user.id
                    pic = str(db_user.picture)
                    request.session['pic'] = pic
                    # 判断有没有商铺
                    store = models.Store.objects.filter(user_id=db_user.id).first()
                    if store:
                        request.session['is_store'] = store.user_id
                    return redirect('/fresh/index/')
                else:
                    print('密码不正确')
            else:
                print('用户不存在')
        else:
            print('用户名密码不能为空')

    return render(request, 'freshstore/login.html')

# 注销
def logout(request):
    del request.session['username']
    del request.session['uid']
    if request.session.get('is_store'):
        del request.session['is_store']
    return redirect('/fresh/index/')

# 注册

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        repwd = request.POST.get('repwd')
        pic = request.FILES.get('pic')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        card_id = request.POST.get('card_id')
        # 判断是否获取到用户名密码
        if username and password and repwd:
            # 判断密码和确认密码是否相同
            if password == repwd:
                models.Seller.objects.create(
                    username = username,
                    password = password,
                    nickname = nickname,
                    phone = phone,
                    email = email,
                    picture = pic,
                    address = address,
                    card_id = card_id
                )
                print('注册ok')
            else:
                print('密码不相等')
        else:
            print('字段必须填写')
    return render(request,'freshstore/register.html')

# index
def index(request):
    username = request.session.get('username')
    if username:
        user = models.Seller.objects.filter(username=username).first()

        return render(request, 'freshstore/index.html',{'username':username,'user':user})

    return render(request,'freshstore/index.html')

#　添加商铺
@checklogin
def store_add(request):
    if request.method == "POST":
        store_name = request.POST.get('store_name')
        store_address = request.POST.get('store_address')
        store_description = request.POST.get('store_description')
        store_logo = request.FILES.get('store_logo')
        store_phone = request.POST.get('store_phone')
        user_id = request.POST.get('user_id')
        store_type = request.POST.getlist('store_type')
        print(store_type)
        if store_name and store_address  and store_type:
            store = models.Store()
            store.store_name = store_name
            store.store_address = store_address
            store.store_description = store_description
            store.store_logo = store_logo
            store.store_phone = store_phone
            store.user_id = request.session.get('uid')
            store.save()
            for i in store_type:
                store.store_type.add(
                    models.StoreType.objects.filter(type_name=i).first()
                )
            store.save()
            request.session['is_store'] = store.id
            return redirect('/fresh/index/')

    seller_obj = models.Seller.objects.all()
    store_types = models.StoreType.objects.all()
    return render(request,'freshstore/store_add.html',{'store_types':store_types,'seller_obj':seller_obj})


# 添加商品
@checklogin
def goods_add(request):
    if request.method == "POST":
        goods_name = request.POST.get('goods_name')
        goods_price = request.POST.get('goods_price')
        goods_image = request.FILES.get('goods_image')
        goods_number = request.POST.get('goods_number')
        goods_descirption = request.POST.get('goods_descirption')
        goods_date = request.POST.get('goods_date')
        goods_safeDate = request.POST.get('goods_safeDate')

        if goods_name and goods_price and goods_number and goods_date:
            goods_obj = models.Goods()
            goods_obj.goods_name = goods_name
            goods_obj.goods_price = goods_price
            goods_obj.goods_image = goods_image
            goods_obj.goods_number = goods_number
            goods_obj.goods_descirption = goods_descirption
            goods_obj.goods_date = goods_date
            goods_obj.goods_safeDate = goods_safeDate
            goods_obj.save()
            store = request.POST.getlist('store')
            for i in store:
                store_obj = models.Store.objects.filter(store_name=i).first()

                goods_obj.store_id.add(models.Store.objects.filter(id = store_obj.id).first())
            goods_obj.save()
            return redirect('/fresh/goods_show/up/')

    store_list = models.Store.objects.all()
    return render(request,'freshstore/goods_add.html',{'store_list':store_list})


# 展示商品
@checklogin
def goods_show(request,state):

    if state == 'up':
        state_num = 1
    else:
        state_num = 0
    keyword = request.GET.get('keyword','')
    page_num = request.GET.get('page_num','1')
    uid = request.session.get('uid')
    store = models.Store.objects.filter(user_id = uid).first()
    if keyword:
        goods_obj = models.Goods.objects.filter(store_id=store.id,goods_name__contains=keyword,goods_down=state_num)
    else:
        goods_obj = models.Goods.objects.filter(store_id=store,goods_down=state_num)
    paginator = Paginator(goods_obj,4)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    # 商品数量
    goods_count = models.Goods.objects.filter(store_id=store).count()



    return render(request,'freshstore/goods_show.html',{'keyword':keyword,'page':page,'page_range':page_range,'goods_count':goods_count,'state':state})

# 商品详情页
@checklogin
def goods_detail(request):
    goods_id = request.GET.get('id')
    goods_obj = models.Goods.objects.filter(id = goods_id).first()
    return render(request,'freshstore/goods_detail.html',{'goods_obj':goods_obj})

# 删除商品
def goods_delete(request):
    referer = request.META.get('HTTP-REFERER')
    id = request.GET.get('id')
    models.Goods.objects.filter(id = id).delete()
    return redirect(referer)
# 商品修改
@checklogin
def goods_edit(request):
    if request.method == "POST":
        goods_name = request.POST.get('goods_name')
        goods_price = request.POST.get('goods_price')
        goods_image = request.POST.get('goods_image')
        goods_number = request.POST.get('goods_number')
        goods_descirption = request.POST.get('goods_descirption')
        goods_date = request.POST.get('goods_date').lstrip()
        goods_safeDate = request.POST.get('goods_safeDate')
        id = request.POST.get('id')

        goods_obj = models.Goods.objects.filter(id=id).first()
        goods_obj.goods_name = goods_name
        goods_obj.goods_price = goods_price
        goods_obj.goods_number = goods_number
        goods_obj.goods_descirption = goods_descirption
        goods_obj.goods_date = goods_date
        goods_obj.goods_safeDate = goods_safeDate
        if goods_image:
            goods_obj.goods_image = goods_image

        goods_obj.save()
        return redirect('/fresh/goods_detail/?id=%s'%id)

    id = request.GET.get('id')
    goods_obj = models.Goods.objects.filter(id = id).first()
    return render(request,'freshstore/goods_edit.html',{'goods_obj':goods_obj})


# 商品类型列表
def good_type_show(request):
    goods_type = models.Goods_type.objects.all()
    return render(request,'freshstore/goods_type.html',{'goods_type':goods_type})

# 商品类型添加
def goods_type_add(request):
    if request.method == "POST":
        type_name = request.POST.get('type_name')
        type_description = request.POST.get('type_description')
        type_img = request.FILES.get('type_img')

        models.Goods_type.objects.create(
            type_name = type_name,
            type_description = type_description,
            type_img = type_img
        )
    return redirect('/fresh/goods_type_show/')

# 商品类型修改
def goods_type_edit(request):
    if request.method == "POST":
        id = request.POST.get('id')
        type_name = request.POST.get('type_name')
        type_img = request.FILES.get('type_img')
        type_description = request.POST.get('type_description')

        type = models.Goods_type.objects.filter(id =id).first()
        if type:
            type.type_name = type_name
            if type_img:
                type.type_img = type_img
            type.type_description = type_description
            type.save()
    return redirect('/fresh/goods_type_show/')

# 商品类型删除
def goods_type_delete(request):
    id = request.GET.get('id')
    models.Goods_type.objects.filter(id = id).delete()

    return redirect('/fresh/goods_type_show/')

# 商品上下架
def goods_set(request,state):
    if state =='up':
        state_num = 1
    else:
        state_num = 0
    id = request.GET.get("id")
    refer = request.META.get('HTTP_REFERER')
    if id:
        goods_obj = models.Goods.objects.filter(id =id).first()
        if state == 'delete':
            goods_obj.delete()
        else:
            goods_obj.goods_down =state_num
            goods_obj.save()
    return redirect(refer)

# 个人主页
@checklogin
def home(request):
    uid = request.session.get('uid')
    user = models.Seller.objects.filter(id = uid).first()
    if user:
        id = user.id
        username = user.username
        nickname = user.nickname
        phone = user.phone
        email = user.email
        picture = user.picture
        address = user.address
        card_id = user.card_id

        return render(request,'freshstore/home.html',{
            'id':id,
            'username':username,
            'nickname':nickname,
            'phone':phone,
            'email':email,
            'picture':picture,
            'address':address,
            'card_id':card_id,
        })
    return render(request,'freshstore/home.html')

# 个人信息修改
def person_edit(request):
    if request.method == "POST":
        id = request.POST.get('id')
        nickname = request.POST.get('nickname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        picture = request.FILES.get('pic')
        address = request.POST.get('address')
        card_id = request.POST.get('card_id')

        user = models.Seller.objects.filter(id = id ).first()
        user.nickname = nickname
        user.phone = phone
        user.email = email
        user.address = address
        user.card_id = card_id
        if picture:
            user.picture = picture

        user.save()
        pic = models.Seller.objects.get(id = id).picture
        request.session['pic'] = str(pic)
        return redirect('/fresh/home/')
    id = request.GET.get('id')
    user = models.Seller.objects.filter(id = id).first()
    return render(request,'freshstore/person_edit.html',{'user':user})


# 找回密码
# def retrieve_pwd(request):
#     return render(request,'')

class TypeViewSet(viewsets.ModelViewSet):
    queryset = models.Goods_type.objects.all()
    serializer_class = serializers.GoodsTypeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.Goods.objects.all() # 具体返回的数据
    serializer_class = serializers.UserSerializer





def base(request):
    username = request.session.get('username')
    obj = models.Seller.objects.filter(username=username).first()
    pic = obj.picture
    return render(request, 'freshstore/base.html',{'username':username,'pic':pic})
def blank(request):
    return render(request, 'blank.html')

def ajaxshow(request):
    return render(request,'freshstore/ajaxshow.html')
