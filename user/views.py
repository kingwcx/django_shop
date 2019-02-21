from django.shortcuts import render, redirect, reverse
from django.db import connection
# 视图
from django.views import View
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator
# 模型
from administrator.models import Commodity, Type
from administrator.models import User, UserExtension, Cart,UserMessage,UserReadMessage
from administrator.models import CartCommodityMid
from administrator.models import Order,OrderCommodityMid
# 表单
from administrator.forms import LoginForm, RegisterForm
# 用户与权限
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
#时间
from pytz import datetime

"""
登陆
"""
class LoginView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'login.html')

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		next_href = request.GET.get('next', '')  # 之前登录页面
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username, password=password)
			if user and user.is_active:
				login(request, user)
				# request.session.set_expriy(0)
				if next_href == "":
					return redirect(reverse('user:cart'))
				else:
					return redirect(next_href)
			else:
				return redirect(reverse('user:login'))
		else:
			print(form.errors)
			return redirect(reverse('user:login'))

#登出
def UserLogout(request):
	logout(request)
	return redirect(reverse('front:index'))


"""
注册
"""
class RegisterView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'register.html')

	def post(self, request, *args, **kwargs):
		form = RegisterForm(request.POST)
		# next_href = request.GET.get('next', '') #之前登录页面
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			# re_password = form.cleaned_data.get('re_password')
			User.objects.create_user(username, ".@.", password)
			return redirect(reverse('user:login'))
		else:
			print(form.errors.get_json_data())
			return redirect(reverse('user:register'))

"""
个人中心
"""
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class ProfileView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'user_profile.html')

@method_decorator(login_required(login_url='user:login'),name='dispatch')
class UserEditAddress(View):
	def post(self, request, *args, **kwargs):
		new_address = request.POST.get('address')
		user = User.objects.get(id=request.user.id)
		user.extension.address = new_address
		user.save()
		return redirect(reverse('user:profile'))

"""
用户订单
"""
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class OrderView(View):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=request.user.id)
		try:
			unpay_order = Order.objects.get(user_id=user.id,is_confirm=False)
		except:
			unpay_order = None

		try:
			unfinish_order = Order.objects.filter(user_id=user.id,is_confirm=True,is_finish=False)
		except:
			unfinish_order = None

		try:
			finish_order = Order.objects.filter(user_id=user.id,is_finish=True)
		except:
			finish_order = None
		return render(request, 'user_order.html',
		              context={"unpay_order":unpay_order,"unfinish_order":unfinish_order,"finish_order":finish_order})

"""
消息中心"""
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class MessageView(View):
	def get(self, request, *args, **kwargs):
		new_messages = UserMessage.objects.filter(user_id=request.user.id)
		read_messages = UserReadMessage.objects.filter(user_id=request.user.id)
		return render(request, 'user_message.html',
		              context={"new_messages":new_messages,"read_messages":read_messages})

@method_decorator(login_required(login_url='user:login'),name='dispatch')
class MessageDetailView(View):
	def get(self, request, *args, **kwargs):
		new_messages = UserMessage.objects.filter(user_id=request.user.id)
		return render(request, 'user_message.html',context={"new_messages":new_messages})

#一键已读
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class MessageReadAllView(View):
	def post(self, request, *args, **kwargs):
		new_messages = UserMessage.objects.filter(user_id=request.user.id)
		for new_message in new_messages:
			message = UserReadMessage(status_key=new_message.status_key,content=new_message.content,
			                          order=new_message.order,user=new_message.user,
			                          creat_time=new_message.creat_time)
			message.save()
			new_message.delete()
		return redirect(reverse('user:message'))

"""
购物车
"""
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class CartView(View):
	def get(self, request, *args, **kwargs):
		cart = Cart.objects.get(user_id=request.user.id)
		return render(request, 'cart.html',context={"cart":cart})


# 添加到购物车
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class AddToCart(View):
	def post(self, request, *args, **kwargs):
		commodity_id = request.POST.get('commodity_id')
		commodity = Commodity.objects.get(id=commodity_id)

		cart = Cart.objects.get(user_id=request.user.id)

		commodity_number = 1

		try:
			commodity_mid = CartCommodityMid.objects.get(commodity_id=commodity_id)
			if commodity_mid in cart.commodities.all():
				commodity_mid.number += commodity_number
				commodity_mid.save()
			else:
				commodity_mid = CartCommodityMid(number=commodity_number,commodity=commodity)
				commodity_mid.save()
				cart.commodities.add(commodity_mid)
		except:
			commodity_mid = CartCommodityMid(number=commodity_number,commodity=commodity)
			commodity_mid.save()
			cart.commodities.add(commodity_mid)

		cart.update()
		next_url = kwargs['re_path']
		if next_url != "":
			#return redirect(next_url)
			return redirect(reverse('front:commodity_show'))
		else:
			return redirect(reverse('user:cart'))

# 从购物车中删除
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class RemoveCart(View):
	def post(self, request, *args, **kwargs):
		commodity_mid_id = request.POST.get('commodity_mid_id')
		commodity_mid = CartCommodityMid.objects.get(id=commodity_mid_id)
		#print(request.user.id)
		cart = Cart.objects.get(user_id=request.user.id)
		cart.commodities.remove(commodity_mid)
		cart.update()
		commodity_mid.delete()
		return redirect(reverse('user:cart'))

# 清空
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class ClearCart(View):
	def post(self, request, *args, **kwargs):
		cart = Cart.objects.get(user_id=request.user.id)
		commodities = cart.commodities.all()
		for commodity in commodities:
			commodity_mid = CartCommodityMid.objects.get(id=commodity.id)
			commodity_mid.delete()

		cart.commodities.clear()
		cart.update()
		return redirect(reverse('user:cart'))

# 结算
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class SettleCart(View):
	def post(self, request, *args, **kwargs):
		user = User.objects.get(id=request.user.id)
		try:
			order = Order.objects.get(user_id=user.id,is_confirm=False)
			return render(request, "order_error.html", context={"error_message": "还有未支付订单"})
		except:
			pass

		cart = Cart.objects.get(user_id=user.id)
		mid_commodities = cart.commodities.all()
		order = Order(user_id=request.user.id,address=request.user.extension.address)
		order.save()
		for mid_commodity in mid_commodities:
			cart_commodity_mid = CartCommodityMid.objects.get(id=mid_commodity.id)
			#商品销售数目增加
			commodity = cart_commodity_mid.commodity
			commodity.buy_quantity += cart_commodity_mid.number
			commodity.save()
			#转移到订单库中
			commodity_mid = OrderCommodityMid(number=cart_commodity_mid.number, commodity=cart_commodity_mid.commodity)
			cart_commodity_mid.delete()
			commodity_mid.save()
			order.commodities.add(commodity_mid)

		user.extension.confirm_order_id = order.id
		user.save()
		cart.commodities.clear()
		cart.update()
		order.update()
		return redirect(reverse('user:order_confirm'))

#订单确认页面
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class OrderConfirm(View):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=request.user.id)
		try:
			order = Order.objects.get(user_id=user.id,is_confirm=False)
			return render(request, 'order_confirm.html', context={"order": order})
		except:
			return render(request, "order_error.html", context={"error_message": "不存在未支付订单"})

#订单支付页面模拟
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class OrderPay(View):
	def get(self, request, *args, **kwargs):
		order = Order.objects.get(id=kwargs['order_id'])
		if (order.user_id == request.user.id):
			return render(request, 'pay.html',context={"order_id":order.id})
		else:
			return render(request, "order_error.html", context={"error_message": "非法操作"})

#支付成功
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class OrderPaySuccess(View):
	def get(self, request, *args, **kwargs):
		order = Order.objects.get(id=kwargs['order_id'])
		if (order.user_id == request.user.id):
			order.is_confirm = True
			order.is_pay = True
			order.pay_time = datetime.datetime.now()
			order.save()
			return render(request, 'pay_success.html')
		else:
			return render(request, "order_error.html", context={"error_message": "非法操作"})

#完成订单
@method_decorator(login_required(login_url='user:login'),name='dispatch')
class FinishOrder(View):
	def post(self, request, *args, **kwargs):
		order_id = request.POST.get('order_id')
		order = Order.objects.get(id=order_id)
		if( order.user_id == request.user.id):
			order.is_send = True
			order.is_finish = True
			order.send_time = datetime.datetime.now()
			order.finish_time = datetime.datetime.now()
			order.save()
			return redirect(reverse('user:order'))
		else:
			return render(request, "order_error.html", context={"error_message": "非法操作"})




