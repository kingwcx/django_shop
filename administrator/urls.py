"""project_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
	path('', views.AdminIndexView.as_view(), name='index'),
	path('home/', views.AdminIndexView.as_view(), name='home'),

	path('login/', views.AdminLoginView.as_view(), name='login'),
	path('logout/', views.AdminLogout, name='logout'),
	#商品
	path('commodity_list/', views.AdminCommodityListView.as_view(), name='commodity_list'),
	path('add_commodity/', views.AddCommodityView.as_view(), name='add_commodity'),
	path('commodity_detail/<int:commodity_id>/', views.AdminCommodityDetailView.as_view(), name='commodity_detail'),
    path('delete_commodity/', views.delete_commodity,name='delete_commodity'),
	path('add_type/',views.AddCommodityTypeView.as_view(),name='add_type'),

	#用户
    path('user_list/', views.AdminUserListView.as_view(),name='user_list'),
    path('user_detail/<int:user_id>/', views.AdminUserDetailView.as_view(),name='user_detail'),
	#修改用户状态
    path('user_detail/edit/active', views.AdminUserEditActiveView.as_view(),name='user_edit_active'),
	path('delete_user/', views.delete_user,name='delete_user'),

	#订单
    path('order_list/', views.AdminOrderListView.as_view(),name='order_list'),
	path('order_detail/<int:order_id>/', views.AdminOrderDetailView.as_view(), name='order_detail'),
	#修改订单状态
	path('order_detail/edit/pay/', views.AdminOrderEditPayView.as_view(), name='order_edit_pay'),
	path('order_detail/edit/send/', views.AdminOrderEditSendView.as_view(), name='order_edit_send'),
	path('order_detail/edit/finish/', views.AdminOrderEditFinishView.as_view(), name='order_edit_finish'),
	path('order_detail/edit/quit/', views.AdminOrderEditQuitView.as_view(), name='order_edit_quit'),

]
