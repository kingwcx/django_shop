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

app_name = 'user'

urlpatterns = [
	path('register/', views.RegisterView.as_view(), name='register'),
	path('login/', views.LoginView.as_view(), name='login'),
	path('logout/', views.UserLogout, name='logout'),

	path('profile/', views.ProfileView.as_view(), name='profile'),
	path('message/', views.MessageView.as_view(), name='message'),
	path('message/<int:message_id>', views.MessageDetailView.as_view(), name='message_detail'),
	path('message/read_all', views.MessageReadAllView.as_view(), name='message_read_all'),
	path('profile/edit/address/', views.UserEditAddress.as_view(), name='edit_address'),
	path('order/', views.OrderView.as_view(), name='order'),

	path('cart/', views.CartView.as_view(), name='cart'),
	path('add_to_cart/<path:re_path>/',views.AddToCart.as_view(), name='add_to_cart'),
	path('remove_cart/',views.RemoveCart.as_view(), name='remove_cart'),
	path('clear_cart/',views.ClearCart.as_view(), name='clear_cart'),
	path('settle_cart/',views.SettleCart.as_view(), name='settle_cart'),

	path('order_confirm/',views.OrderConfirm.as_view(), name='order_confirm'),
	path('order_pay/<int:order_id>/',views.OrderPay.as_view(), name='order_pay'),
	path('pay_success/<int:order_id>/',views.OrderPaySuccess.as_view(), name='pay_success'),
	path('order/finish_order', views.FinishOrder.as_view(), name='finish_order'),
]
