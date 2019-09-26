from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
import time
from Buyer import models
from fresh import models as fm
import hashlib
from alipay import AliPay

# Create your views here.

# 验证登录
def checkLogin(func):
    def inner(request,*args,**kwargs):
        ck_username = request.COOKIES.get('username')
        sn_username = request.session.get('username')
        print('11111111111',ck_username,sn_username)
        if ck_username and sn_username and ck_username ==sn_username:

            return func(request,*args,**kwargs)
        else:
            return redirect('/buy/index/')
    return inner


# 密码加密
def secret_pwd(password):
    md = hashlib.md5()
    password = password.encode()
    md .update(password)
    return md.hexdigest()


# index页面
def index(request):
    goods_type_list = fm.Goods_type.objects.all()

    return render(request, 'buyer/index.html',{'goods_type_list':goods_type_list})

# 登录
def login(request):
    if request.method == "POST":
        # 获取表单传过来的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 数据库中查询数据
        user = models.Buyer.objects.filter(username=username).first()
        if user:
            db_pwd = user.password  # 验证密码
            if password == db_pwd:
                # 设置cookies session
                request.session['username'] = username
                request.session['password'] = password
                response = redirect('/buy/index/')
                response.set_cookie('username',username)
                print('-----------',request.session,request.COOKIES)
                return response
    return render(request, 'buyer/login.html')

# 登出
def logout(request):
    # 删除cookies 和session
    response = redirect('/buy/index/')
    for i in request.COOKIES:
        response.delete_cookie(i)
    if request.session.get('username'):
        del request.session['username']
    if request.session.get('password'):
        del request.session['password']
    return response


#注册
def register(request):
    if request.method == "POST":
        # 获取表单数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # 数据库添加
        buyer = models.Buyer.objects.create(
            username = username,
            password = password,
            email = email
        )
        return redirect('/buy/login/')
    return render(request, 'buyer/register.html')

# 用户中心
@checkLogin
def home(request):
    # 登录后从cookies中获取用户，查出数据
    username = request.COOKIES.get('username')
    user = models.Buyer.objects.filter(username=username).first()
    if user:

        return render(request,'buyer/user_center_info.html',{'user':user})
    return render(request,'buyer/user_center_info.html')

# 商品列表页
def goods_list(request):
    # 从index页上获取商品类型id，
    id = request.GET.get('id')
    # 获取类型的对象
    type = fm.Goods_type.objects.filter(id = id).first()
    # 反向查出商品
    goodslist = type.goods_set.filter(goods_down = 1)
    return render(request,'buyer/list.html',{'goodslist':goodslist,'type':type})


# 商品详情ye
def detail(request):
    # 从index上获取商品id
    id = request.GET.get('id')
    goods = fm.Goods.objects.filter(id=id).first()
    return render(request,'buyer/detail.html',{'goods':goods})

def setOrderId(user_id,goods_id,store_id):
    """
    设置订单编号
    时间+用户id+商品id
    """
    strtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
    return strtime+str(user_id)+str(goods_id)+str(store_id)

# 购物车
@checkLogin
def shoppingcart(request):
    username = request.COOKIES.get('username')
    user = models.Buyer.objects.get(username=username)
    goods_list = models.Cart.objects.filter(user_id = user.id)
    if request.method == 'POST':
        postdata = request.POST
        cart_data = []
        for k,v in postdata.items():
            if k.startswith('goods_items_'):
                cart_data.append(models.Cart.objects.get(id=int(v)))
        goods_count = len(cart_data)# 商品总数
        goods_totalprice = sum([int(i.goods_totalprice) for i in cart_data])# 商品总价
        # 保存订单
        order = models.Order()
        order.order_id = setOrderId(user.id,goods_count,'2')
        order.goods_count = goods_count
        order.order_user = user
        order.order_totalprice = goods_totalprice
        order.order_status = 1
        order.order_address = user.address_set.first()
        order.save()

        # 保存订单详情
        for detail in cart_data:
            order_detail = models.OrderDetail()
            order_detail.order_id = order
            order_detail.goods_id = detail.id
            order_detail.goods_store = detail.goods_store
            order_detail.goods_name = detail.goods_name
            order_detail.goods_price = detail.goods_price
            order_detail.goods_total = detail.goods_totalprice
            order_detail.goods_number = detail.goods_number
            order_detail.goods_img = detail.goods_img
            order_detail.save()
        return redirect('/buy/place_order/?order_id=%s'%order.id)

    return render(request,'buyer/cart.html',{'goods_list':goods_list})
@checkLogin
def addCart(request):
    response = {'state':'error','data':''}
    if request.method == "POST":
        goods_id  = request.POST.get('goods_id')
        count = int(request.POST.get('count'))
        print(goods_id,count,'=============')
        goods = fm.Goods.objects.filter(id = goods_id).first()
        username = request.COOKIES.get('username')
        user = models.Buyer.objects.get(username=username)

        cart = models.Cart()
        cart.goods_name = goods.goods_name
        cart.goods_price = goods.goods_price
        cart.goods_totalprice = goods.goods_price*count
        cart.goods_number = count
        cart.goods_img = goods.goods_image
        cart.goods_id = goods.id
        cart.goods_store = goods.store_id.first().id
        cart.user_id = user.id
        cart.save()
        response['state'] = 'success'
        response['data'] = '添加成功'
    return JsonResponse(response)
# 我的订单
@checkLogin
def order(request):
    return render(request,'buyer/user_center_order.html')

# 订单处理
@checkLogin
def place_order(request):
    if request.method == "POST":
        count = int(request.POST.get('count'))
        goods_id = request.POST.get('goods_id')
        username = request.COOKIES.get('username')
        user = models.Buyer.objects.filter(username=username).first()
        goods = fm.Goods.objects.get(id = goods_id)
        store_id = goods.store_id.get(id=1).id
        price = goods.goods_price

        order = models.Order()
        order.order_id = setOrderId(str(user.id),str(goods_id),str(store_id))
        order.goods_count = count
        order.order_user  = models.Buyer.objects.get(id = user.id)
        order.order_totalprice = count*price
        order.save()

        order_detail = models.OrderDetail()
        order_detail.order_id = order
        order_detail.goods_id = goods.id
        order_detail.goods_name = goods.goods_name
        order_detail.goods_price = goods.goods_price
        order_detail.goods_number = count
        order_detail.goods_total = count*goods.goods_price
        order_detail.goods_store = store_id
        order_detail.goods_img = goods.goods_image
        order_detail.save()

        detail = [order_detail,]
        return render(request,'buyer/place_order.html',locals())
    order_id = request.GET.get('order_id')
    if order_id:
        order = models.Order.objects.get(id=order_id)
        detail = order.orderdetail_set.all()
        return render(request,'buyer/place_order.html',locals())
    else:
        return HttpResponse('非法访问')
# 付钱
@checkLogin
def pay_order(request):
    money = str(request.GET.get('money'))
    order_id = str(request.GET.get('order_id'))
    print(money,order_id,']]]]]]]]]]]')
    # 几乎固定的写法
    publickey_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0A+kWgu1UXkkIbtilUkD1BHB4wdyVkesWf62lwdQxQVH+qyVwKvMoyAPtO02DNtaTRFx8otfLHfqPo35XTUsMT1EugX9WyffdC7rRcsv4i7YWbs3tGd/0chd32kuacyE5wWUGpxFpoR0jVpnsos0zNA2EFkIn9e8dyNtOrqrkc/smkl7ZJdjKj8AgiFPVvvfb+0hzZFCKH0BjhmO0nkOOknsTGD94R/ui3O3JSWg0VjGUl23j7aVfPzf33sfyitknWR1BFA9dTpj913xWaVA8QI+9PstF8Jv7VNadHYKXpNtRkuFWJGvOgT0HbUlDml2OMSrnALHh2muX0GExHewDwIDAQAB
    -----END PUBLIC KEY-----"""

    privatekey_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDQD6RaC7VReSQhu2KVSQPUEcHjB3JWR6xZ/raXB1DFBUf6rJXAq8yjIA+07TYM21pNEXHyi18sd+o+jfldNSwxPUS6Bf1bJ990LutFyy/iLthZuze0Z3/RyF3faS5pzITnBZQanEWmhHSNWmeyizTM0DYQWQif17x3I206uquRz+yaSXtkl2MqPwCCIU9W+99v7SHNkUIofQGOGY7SeQ46SexMYP3hH+6Lc7clJaDRWMZSXbePtpV8/N/fex/KK2SdZHUEUD11OmP3XfFZpUDxAj70+y0Xwm/tU1p0dgpek21GS4VYka86BPQdtSUOaXY4xKucAseHaa5fQYTEd7APAgMBAAECggEARdzavPmtepwIy+LV6XbI+E62IfuAIwSSFO34daIZNu7dCoklB7soTaYYYBI+0fZdzf8Lmfu+i3oAh9y4XNnb6vS9vREBz7gFykdu7NKbU4GTWB4LSGJwgwqaqsfws8ne3ov6/Sx4Hr/fOw+ePk+L/TH01Wxv/uw79m1I4i2IKr9hnvwU3ObRIsSKXV8ApG0nFYVHSlY1snlbG7c1osOSJeZGbnKax6EoECUtgbreDmm15O8UVySST4YjTG21L0DHW5X/QNVb91oiLIcKLIzYfLdsyNq6NCFVm4knvGSsc13bj1cBy6RqEZpOV5C500rGRRGGQqcBDscw5LCNoUnmwQKBgQDn9+ZK8GPwzJ+dvBrKoV5HPIQV9MIjSDA9QO7bdC3+moyA+8eYYqWdlaTL5j/Gel7sgCzR8MVoExhWTXUSUTKJB8ema5KfWXd6G1fXAnaK9N6zBS7oVBcu4DAarJjBZJe3iOoJB5zdRLmNPogyUWTGigSN5i2bYjyDJJhk8THB/wKBgQDlnbDsjRmHDepuFP+5dgH4rb2iJvd20K0GUadMt6U1KKhb+VCg0hMcMz2IBvwBRdTUmhWdKrFRSg8g6WCQN+ty/29/Y2I9wQtqxVMzE9ZzDXksNy9TFiFhbZFmki8gWllYqQoVeKV2Pe2Fy1cXOEbQfXON4B3EVUnWPQpN5QHx8QKBgQDRustW+h4CO6AdR1OZ3WiWU9rA1zkoGT60Qx8y/8oOJsHeZMbDun0vC3uidx02YLGudv0PG/f/7zPT49hzpUJhrs0OZLh+pq9lkY9L8Qgo/tjTV15f5JfJZB1aIK9EO6UI5htj6qQjUt3JHL6bcAgDkgooGfMmSB2aHN5EdeadFQKBgHGh7XnThkuY7mhWCgwNQ4J+8Pb7U8JAGTCkXigQRjkditwhcO51qDFvhkb4NeSnW2Fvc7zY8PGqtfvyovAcTHAXy2T+mRK4o17OkpMXgSxlAY+JK+lxbUmbALcDJ0FalRbUaQIhN7lhgleRPuNl3V22h+YxgGm2T5kvkhbke2bxAoGAQLaHjT6MEjxI8w1e6a3rSwQCoFMWKHKnGqSQiSSTM6pBFnfChGnsk9Cuy78EAR54h5HgF9fVSyzcoueN4sElgWeRX8rEdAY6EAVXJlGB7PuZZ5TtDPHq5MKvM9eQYjFTiBvaEdc0ZGY5itiEcCH5GA3rxy6A1SZMRXREx6JRCpI=
    -----END RSA PRIVATE KEY-----"""

    pay = AliPay(
        appid='2016101000652493',
        app_notify_url=None,
        app_private_key_string=privatekey_string,
        alipay_public_key_string=publickey_string,
        sign_type='RSA2',
    )

    order_string = pay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=money,
        subject='违法交易',
        return_url='http://127.0.0.1:8000/buy/pay_result/',
        notify_url='http://127.0.0.1:8000/buy/pay_result/'
    )

    return redirect('https://openapi.alipaydev.com/gateway.do?' + order_string)

# 付钱返回
@checkLogin
def pay_result(request):
    order_id = request.GET.get('out_trade_no')
    money = request.GET.get("total_amount")
    time = request.GET.get('timestamp')
    return render(request,'buyer/order_result.html',{'order_id':order_id,'money':money,'time':time})