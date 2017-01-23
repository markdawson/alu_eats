from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from ...models import OrderItem, VendorEmail
from django.template import Context
from django.template.loader import get_template
import datetime


class Command(BaseCommand):

	def handle(self, *args, **options):
		tomorrow = datetime.date.today() + datetime.timedelta(1)
		# add subject
		subject = 'Orders for {}'.format(tomorrow)

		# add objects
		orders = OrderItem.objects.filter(date=tomorrow)
		# render body
		template = get_template('orders/email_vendors.html')
		context = Context({'orders': orders})
		html_message = template.render(context)

		# get vendors
		to = VendorEmail.objects.filter(active='True')
		send_mail(subject=subject,
				 message= '',
				 html_message=html_message,
				 from_email='alueats@bplunch.alueducation.com',
				 recipient_list=to)