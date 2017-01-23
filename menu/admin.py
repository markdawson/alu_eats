from django.contrib import admin
from .models import Category, MenuItem, MenuItemReview, MenuItemRating

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class MenuItemAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'price', 'category', 'available']
	list_filter = ['available', 'category']
	list_editable = ['price', 'available']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(MenuItem, MenuItemAdmin)
 
admin.site.register(MenuItemReview)
admin.site.register(MenuItemRating)