from django.db import models
from menu.models import MenuItem
from django.contrib.auth.models import User

class OrderItem(models.Model):
	user = models.ForeignKey(User, related_name='orders')
	menu_item = models.ForeignKey(MenuItem, related_name='menu_items', null=True, on_delete=models.SET_NULL)
	price = models.PositiveIntegerField()
	quantity = models.PositiveIntegerField()
	date = models.DateField()
	comments = models.CharField(verbose_name='Comments for vendor', max_length=200, default='', null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-date',)

	def __str__(self):
		return "{} for {} on {}".format(self.menu_item,
										 self.user,
										 self.date)

	def total_price(self):
		return self.price * self.quantity

class VendorEmail(models.Model):
	vendor_name = models.CharField(max_length=200)
	email = models.EmailField()
	active = models.BooleanField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email