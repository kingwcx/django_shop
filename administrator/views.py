from django.shortcuts import HttpResponse, render, redirect, reverse
from django.db import connection
from .models import Commodity, Type
from .models import User, UserExtension,UserMessage
from .models import Order
# 视图
from django.views import View
from django.views.generic.list import ListView
from django.core.paginator import Paginator
# 表单
from .forms import LoginForm
#时间
from pytz import datetime
# 用户与权限
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

"""
 获取数据库连接
"""
def get_cursor():
	return connection.cursor()

"""
添加一条消息通知"""
def add_message(order:Order,key:int):
	if key == 1:
		content = "已发货"
	elif key == 2:
		content = "已完成"
	elif key == 3:
		content = "已确认退单"
	else:
		print("未知请求！")
		content = ""
	contents = "您的订单编号为" + str(order.id) + "的订单" + content + "!"
	user = User.objects.get(id=order.user_id)
	message = UserMessage(status_key=key,content=contents,user=user,order=order)
	message.save()



"""
装饰器
"""


"""
 管理员登陆页面
"""
class AdminLoginView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_login.html')

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST)
		next_href = request.GET.get('next', '') #之前登录页面
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username, password=password)
			if user and user.is_superuser:
				login(request, user)
				# request.session.set_expriy(0)
				if next_href == "":
					return redirect(reverse('admin:home'))
				else:
					return redirect(next_href)
		else:
			print(form.errors)
			return redirect(reverse('admin:login'))


def AdminLogout(request):
	logout(request)
	return redirect(reverse('admin:login'))


""" 
 管理员主页面
"""
@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminIndexView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'admin_home.html')


"""
 管理员商品页面
"""
@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminCommodityListView(ListView):
	model = Commodity
	template_name = 'admin_commodity_list.html'
	paginate_by = 6
	context_object_name = 'commodities'
	ordering = 'id'
	page_kwarg = 'page'

	"""def get(self,request,*args,**kwargs):
		commodities = Commodity.objects.all()
		return render(request, 'admin_commodity_list.html', context={"commodities": commodities})"""

@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AddCommodityTypeView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'add_type.html')

	def post(self, request, *args, **kwargs):
		typename = request.POST.get("typename")
		type = Type(typename=typename)
		type.save()
		return redirect(reverse('admin:commodity_list'))

@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AddCommodityView(View):
	def get(self, request, *args, **kwargs):
		types = Type.objects.all()
		return render(request, 'add_commodity.html', context={"types": types})

	def post(self, request, *args, **kwargs):
		name = request.POST.get("name")
		content = request.POST.get("content")
		price = request.POST.get("price")
		store = request.POST.get("store")
		type_id = request.POST.get("type")
		img = request.FILES.get("image")
		type = Type.objects.get(id=int(type_id))
		commodity = Commodity(name=name, description=content, img=img, price=price, quantity=store)
		commodity.type = type
		commodity.save()
		return redirect(reverse('admin:commodity_list'))

@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminCommodityDetailView(View):
	def get(self, request, *args, **kwargs):
		# print(args,kwargs)
		commodity = Commodity.objects.get(id=kwargs['commodity_id'])
		return render(request, 'admin_commodity_detail.html', context={"commodity": commodity})

@login_required(login_url='admin:login')
@permission_required('add_logentry',login_url='admin:login')
def delete_commodity(request):
	if request.method == 'POST':
		commodity_id = request.POST.get('commodity_id')
		commodity = Commodity.objects.filter(id=commodity_id)
		commodity.delete()
		return redirect(reverse('admin:commodity_list'))
	else:
		raise RuntimeError("删除商品时错误")


"""
 管理员用户页面
"""
@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminUserListView(ListView):
	model = User
	template_name = 'admin_user_list.html'
	paginate_by = 6
	context_object_name = 'users'
	ordering = 'id'
	page_kwarg = 'page'

	def get_queryset(self):
		users = self.model.objects.filter(is_superuser=False)
		return users

@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminUserDetailView(View):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(id=kwargs['user_id'])
		return render(request, 'admin_user_detail.html', context={"user": user})
# user.userextension

@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminUserEditActiveView(View):
	def post(self, request, *args, **kwargs):
		user = User.objects.get(id=request.POST.get('user_id'))
		if user.is_active == True:
			user.is_active = False
		else:
			user.is_active = True
		user.save()
		return redirect(reverse('admin:user_detail',kwargs={"user_id":user.id}))
# user.userextension

@login_required(login_url='admin:login')
@permission_required('add_logentry',login_url='admin:login')
def delete_user(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		user = User.objects.filter(id=user_id)
		user.delete()
		return redirect(reverse('admin:user_list'))
	else:
		raise RuntimeError("删除用户时错误")


"""
 管理员订单页面
"""
@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminOrderListView(ListView):
	model = Order
	template_name = 'admin_order_list.html'
	paginate_by = 6
	context_object_name = 'orders'
	ordering = 'id'
	page_kwarg = 'page'


@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminOrderDetailView(View):
	def get(self, request, *args, **kwargs):
		order = Order.objects.get(id=kwargs['order_id'])
		return render(request, 'admin_order_detail.html', context={"order": order})

@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminOrderEditPayView(View):
	def post(self, request, *args, **kwargs):
		order = Order.objects.get(id=request.POST.get('order_id'))
		if(order.is_pay == True):
			order.is_pay = False
		else:
			order.is_pay = True
			order.pay_time = datetime.datetime.now()
		order.save()
		return redirect(reverse('admin:order_detail',kwargs={"order_id":order.id}))

@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminOrderEditSendView(View):
	def post(self, request, *args, **kwargs):
		order = Order.objects.get(id=request.POST.get('order_id'))
		if(order.is_send == True):
			order.is_send = False
		else:
			order.is_send = True
			order.send_time = datetime.datetime.now()
			add_message(order,1)
		order.save()
		return redirect(reverse('admin:order_detail',kwargs={"order_id":order.id}))

@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminOrderEditFinishView(View):
	def post(self, request, *args, **kwargs):
		order = Order.objects.get(id=request.POST.get('order_id'))
		if(order.is_finish == True):
			order.is_finish = False
		else:
			order.is_finish = True
			order.finish_time = datetime.datetime.now()
			add_message(order, 2)
		order.save()

		return redirect(reverse('admin:order_detail',kwargs={"order_id":order.id}))

@method_decorator(login_required(login_url='admin:login'),name='dispatch')
@method_decorator(permission_required('add_logentry',login_url='admin:login'),name='dispatch')
class AdminOrderEditQuitView(View):
	def post(self, request, *args, **kwargs):
		order = Order.objects.get(id=request.POST.get('order_id'))
		if(order.is_quit == True):
			order.is_quit = False
		else:
			order.is_quit = True
			order.quit_time = datetime.datetime.now()
			add_message(order, 3)
		order.save()
		return redirect(reverse('admin:order_detail',kwargs={"order_id":order.id}))

