from django.db import models
# django 自带用户表
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# 用户扩展表
class UserExtension(models.Model):
	confirm_order_id = models.IntegerField(default=0)
	address = models.CharField(blank=True, max_length=50)
	telephone = models.CharField('Telephone', max_length=50, blank=True)
	sex = models.IntegerField(null=True, blank=True)
	age = models.IntegerField(null=True, blank=True)
	# 一对一外键（User）
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')

	class Meta:
		db_table = 'user_extension'


# 购物车表
class Cart(models.Model):
	id = models.AutoField(primary_key=True)
	number = models.IntegerField(default=0)
	total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
	# 一对一外键（User）
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
	# 多对多外键（Commodity）
	commodities = models.ManyToManyField("CartCommodityMid", related_name="cart_commodities")

	def update(self):
		commodities = self.commodities.all()
		self.total_price = 0
		self.number = 0
		for commodity in commodities:
			#数目为0时清除这个中间件
			if(commodity.number == 0):
				self.commodities.remove(commodity)
			else:
				commodity.total_price = 0
				commodity.total_price += commodity.commodity.price*commodity.number
				commodity.save()
			self.number +=  commodity.number
			self.total_price += commodity.total_price
		super(Cart,self).save()

	class Meta:
		db_table = 'cart'

#购物车商品中间件 计数目表
class CartCommodityMid(models.Model):
	id = models.AutoField(primary_key=True)
	number = models.IntegerField(default=1)
	total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
	#多对一外键
	commodity = models.ForeignKey("Commodity", on_delete=models.CASCADE)

	class Meta:
		db_table = 'cart_commodity_mid'

@receiver(post_save, sender=User)
def create_user_extension(sender, instance, created, **kwargs):
	if created:
		UserExtension.objects.create(user=instance)
		Cart.objects.create(user=instance)
	else:
		instance.extension.save()
		instance.cart.save()

# 商品类型表
class Type(models.Model):
	id = models.AutoField(primary_key=True)
	typename = models.CharField(max_length=20, default="")

	class Meta:
		db_table = 'type'


# 商品表
class Commodity(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	creat_time = models.DateTimeField(blank=True, auto_now_add=True)
	img = models.ImageField(upload_to='commodity/thumbnail', default="0.jpg")
	description = models.CharField(max_length=500, null=True)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	quantity = models.IntegerField(default=0)
	buy_quantity = models.IntegerField(default=0)
	is_exist = models.BooleanField(default=True)
	# 多对一外键（Type）
	type = models.ForeignKey("Type", on_delete=models.CASCADE)

	class Meta:
		db_table = 'commodity'

# 订单表
class Order(models.Model):
	id = models.AutoField(primary_key=True)
	is_confirm = models.BooleanField(blank=True, default=False) #订单确认状态
	is_pay = models.BooleanField(blank=True, default=False) #订单支付状态
	is_send = models.BooleanField(blank=True, default=False) #订单发货状态
	is_finish = models.BooleanField(blank=True, default=False) #订单完成状态
	id_quit = models.BooleanField(blank=True, default=False)  #订单退货状态
	creat_time = models.DateTimeField(blank=True, auto_now_add=True)
	pay_time = models.DateTimeField(null=True, blank=True)
	send_time = models.DateTimeField(null=True, blank=True)
	finish_time = models.DateTimeField(null=True, blank=True)
	quit_time = models.DateTimeField(null=True, blank=True)
	total_price = models.DecimalField(blank=True, max_digits=9, decimal_places=2, default=0)
	number = models.IntegerField(blank=True, default=0)
	address = models.CharField(blank=True, max_length=50)
	# 多对一外键（User）
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# 多对多外键（Commodity）
	commodities = models.ManyToManyField("OrderCommodityMid", related_name="order_commodities")

	class Meta:
		db_table = 'order'

	def update(self):
		commodities = self.commodities.all()
		self.total_price = 0
		self.number = 0
		for commodity in commodities:
			#数目为0时清除这个中间件
			if(commodity.number == 0):
				self.commodities.remove(commodity)
			else:
				commodity.total_price = 0
				commodity.total_price += commodity.commodity.price*commodity.number
				commodity.save()
			self.number +=  commodity.number
			self.total_price += commodity.total_price
		super(Order,self).save()

#订单商品中间件 计数目表
class OrderCommodityMid(models.Model):
	id = models.AutoField(primary_key=True)
	number = models.IntegerField(default=1)
	total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
	#多对一外键
	commodity = models.ForeignKey("Commodity", on_delete=models.CASCADE)

	class Meta:
		db_table = 'order_commodity_mid'


#用户通知消息表(未读)
class UserMessage(models.Model):
	status_key = models.IntegerField(null=True, blank=True) #1:已发货；2：已完成；3：已确认退单
	content = models.CharField(max_length=500, null=True)
	creat_time = models.DateTimeField(blank=True, auto_now_add=True)
	is_read = models.BooleanField(blank=True, default=False)
	#多对一外键
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='new_message')
	#多对一外键
	order = models.ForeignKey(Order, on_delete=models.CASCADE)

	class Meta:
		db_table = 'new_message'

#用户通知消息表（已读）
class UserReadMessage(models.Model):
	status_key = models.IntegerField(null=True, blank=True) #1:已发货；2：已完成；3：已确认退单
	content = models.CharField(max_length=500, null=True)
	creat_time = models.DateTimeField(blank=True, auto_now_add=True)
	is_read = models.BooleanField(blank=True, default=True)
	#多对一外键
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='read_message')
	#多对一外键
	order = models.ForeignKey(Order, on_delete=models.CASCADE)

	class Meta:
		db_table = 'read_message'
# 使用 python manage.py makemigrations 生成迁移脚本文件

# 使用python manage.py migrate  映射2
# 到数据库
