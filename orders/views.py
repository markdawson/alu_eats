from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from menu.models import MenuItem
from .forms import OrderAddMenuItemForm, FilterDateForm
from .models import OrderItem, VendorEmail
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template
from django import forms
import datetime
from datetime import date
from django.contrib import messages

@require_POST
def order_add(request, menu_item_id):
	menu_item = get_object_or_404(MenuItem, id=menu_item_id)
	menu_item_form = OrderAddMenuItemForm(request.POST)
	if menu_item_form.is_valid():
		cd = menu_item_form.cleaned_data
		date = cd['date']
		item = MenuItem.objects.get(id=menu_item_id)
		new_order = OrderItem.objects.create(user=request.user,
								menu_item=item,
								price=item.price,
								quantity=cd['quantity'],
								date=date,
								comments=cd['comments'])
		new_order.save()
		return redirect('orders:upcoming_orders')
	else:
		return render(request,'menu/menu_detail.html',
					{'menu_item': menu_item,
					'menu_item_form': menu_item_form})

def order_remove(request, order_id):
	OrderItem.objects.get(id=order_id).delete()
	return redirect('orders:upcoming_orders')

def order_remove_all_staff_list(request, order_id):
	OrderItem.objects.get(id=order_id).delete()
	return redirect('orders:all_staff_orders')

def upcoming_orders(request):
	today = date.today()
	if datetime.datetime.now().hour >= 16:
		today = today + datetime.timedelta(days=1)
	orders = OrderItem.objects.filter(user=request.user,
								date__gt=today).order_by('date')
	return render(request, 'orders/orders_list.html',
				 { "orders" : orders,
					"title_message": 'Upcoming Orders'})

def past_orders(request):
	today = date.today()
	if datetime.datetime.now().hour >= 16:
		today = today + datetime.timedelta(days=1)
	orders = OrderItem.objects.filter(user=request.user,
								date__lte=today).order_by('-date')[:15]
	return render(request, 'orders/orders_list.html',
				 { "orders" : orders,
					"title_message": 'Past Orders'})

@staff_member_required
def all_staff_orders(request):
	orders = OrderItem.objects.all()
	if request.method =='POST':
		filter_date_form = FilterDateForm(request.POST)
		if filter_date_form.is_valid():
			cd = filter_date_form.cleaned_data
			orders = OrderItem.objects.filter(date__gte=cd['start_date'], date__lte=cd['end_date'])
			if filter_date_form.send_email:
				send_email(request, orders=orders, filter_date_form=filter_date_form, start_date=cd['start_date'], end_date=cd['end_date'])		
	else:
		filter_date_form = FilterDateForm()
	return render(request, 
		'orders/all_staff_orders_list.html',
	 	{'orders':orders,
	 	'filter_date_form': filter_date_form,
	 	'now': datetime.datetime.now()})

def send_email(request, orders, filter_date_form, start_date, end_date):
	# add subject
	subject = 'Orders for {}'
	if start_date == end_date:
		subject = subject.format(str(start_date))
	else:
		subject = subject.format(str(start_date) + ' to ' + str(end_date))

	# render body
	template = get_template('orders/email_vendors.html')
	context = Context({'orders':orders,
	 				'filter_date_form': filter_date_form})
	html_message = template.render(context)

	# get vendors
	to = VendorEmail.objects.filter(active='True')
	send_mail(subject=subject,
			 message= '',
			 html_message=html_message,
			 from_email='alueats@bplunch.alueducation.com',
			 recipient_list=to)

	messages.success(request, 'Email sent to ' + str([e.email for e in to])[1:-1])
