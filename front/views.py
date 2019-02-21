from django.shortcuts import render,redirect,reverse
from django.db import connection

from administrator.models import Commodity,Type
from administrator.models import User,UserExtension

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator


"""
 首页
"""
class IndexView(View):
	def get(self,request,*args,**kwargs):
		commodities = Commodity.objects.order_by('-buy_quantity')[:5]
		types = Type.objects.all()
		return render(request, 'index.html',context={"types":types,"commodities":commodities})

"""
 商品缩略展示
"""
#全部商品
class CommodityShowView(ListView):
	model = Commodity
	template_name = 'commodity_show.html'
	paginate_by = 20
	context_object_name = 'commodities'
	ordering = 'id'
	page_kwarg = 'page'

	def get_queryset(self):
		try:
			category = self.kwargs['type_id']
		except:
			category = ''
		if (category != ''):
			commodities = self.model.objects.filter(type_id=category)
		else:
			commodities = self.model.objects.all()
		return commodities

	def get_context_data(self, **kargs):
		Context = super().get_context_data(**kargs)
		types = Type.objects.all()
		try:
			category = self.kwargs['type_id']
			current_type = Type.objects.get(id=category)
			current_typename = current_type.typename
		except:
			current_typename = "分类商品"

		Context['types'] = types
		Context['typename'] = current_typename
		return Context
"""
 商品详情展示
"""
class CommodityDetailShowView(DetailView):
	model = Commodity
	template_name = 'commodity_detail_show.html'
	context_object_name = 'commodity'
	pk_url_kwarg = 'commodity_id'

	def get_context_data(self, **kargs):
		Context = super().get_context_data(**kargs)
		types = Type.objects.all()
		Context['types'] = types
		return Context




