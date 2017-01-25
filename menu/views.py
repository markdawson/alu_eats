from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, MenuItem, MenuItemReview, MenuItemRating
from orders.models import OrderItem
from orders.forms import OrderAddMenuItemForm
from .forms import RatingForm, ReviewForm
from django.db.models import Avg
import datetime
from django.utils import timezone

@login_required
def menu_list(request, category_slug=None):
	category = None
	categories = Category.objects.all()
	menu_items = MenuItem.objects.filter(available=True)
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		menu_items = menu_items.filter(category=category)
	return render(request, 
					'menu/menu_list.html',
					{'category':category,
					'categories':categories,
					'menu_items':menu_items})

def menu_detail(request, id, slug):
	menu_item = get_object_or_404(MenuItem,
									id=id,
									slug=slug,
									available=True)
	menu_item_form = OrderAddMenuItemForm()
	seven_days_ago = timezone.now() - datetime.timedelta(days=7)
	recent_order_count = OrderItem.objects.filter(menu_item=menu_item, created__gte=seven_days_ago).count()
	try:
		users_rating = MenuItemRating.objects.get(item=menu_item, user=request.user).rating
	except MenuItemRating.DoesNotExist:
	 	users_rating = None
	if users_rating:
		rating_form = RatingForm(initial={'rating': users_rating})
		rating_button_text = 'Change Rating'
	else:
		rating_form = RatingForm()
		rating_button_text = 'Add Rating'
	review_form = ReviewForm()
	reviews = MenuItemReview.objects.filter(item=menu_item)
	overall_rating = MenuItemRating.objects.filter(item=menu_item).aggregate(Avg('rating'))['rating__avg']
	try:
		round(overall_rating, 2)
	except:
		pass
	rating_count = MenuItemRating.objects.filter(item=menu_item).count()
	return render(request,'menu/menu_detail.html',
					{'menu_item': menu_item,
					'menu_item_form': menu_item_form,
					'rating_form' : rating_form,
					'review_form': review_form,
					'reviews' : reviews,
					'overall_rating' : overall_rating,
					'rating_count': rating_count,
					'rating_button_text': rating_button_text,
					'recent_order_count': recent_order_count})

def menu_add_review(request, menu_item_id):
	item = get_object_or_404(MenuItem, id=menu_item_id)
	review_form = ReviewForm(request.POST)
	if review_form.is_valid():
		cd = review_form.cleaned_data
		new_review = MenuItemReview.objects.create(item=item,
												user=request.user,
												review=cd['review'])									
		new_review.save()
		return redirect('menu:menu_detail', menu_item_id, item.slug)
	else:
		menu_item = get_object_or_404(MenuItem,
									id=menu_item_id)
		menu_item_form = OrderAddMenuItemForm()
		rating_form = RatingForm()	
		reviews = MenuItemReview.objects.filter(item=menu_item)
		return render(request,'menu/menu_detail.html',
					{'menu_item': item,
					'menu_item_form': menu_item_form,
					'rating_form' : rating_form,
					'review_form': review_form,
					'reviews' : reviews,})

def menu_add_rating(request, menu_item_id):
	item = get_object_or_404(MenuItem, id=menu_item_id)
	rating_form = RatingForm(request.POST)
	if rating_form.is_valid():
		cd = rating_form.cleaned_data
		# delete old rating
		MenuItemRating.objects.filter(item=item, user=request.user).delete()
		new_rating = MenuItemRating.objects.create(item=item,
													user=request.user,
													rating = cd['rating'])
		new_rating.save()
		return redirect('menu:menu_detail', menu_item_id, item.slug)
