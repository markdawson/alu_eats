from django.contrib import admin
from .models import Category, MenuItem, MenuItemReview, MenuItemRating


class MenuItemInline(admin.TabularInline):
    model = MenuItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'available']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['activate_category', 'deactivate_category']
    inlines = [MenuItemInline]

    def activate_category(self, request, queryset):
        for c in queryset:
            c.available = True
            c.save()
            for item in c.menu_items.all():
                item.available = True
                item.save()

    activate_category.short_description = "Activate category and all items in category"

    def deactivate_category(self, request, queryset):
        for c in queryset:
            c.available = False
            c.save()
            for item in c.menu_items.all():
                item.available = False
                item.save()

    deactivate_category.short_description = "Deactivate category and all items in category"


admin.site.register(Category, CategoryAdmin)

class MenuItemAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'price', 'category', 'available']
	list_filter = ['available', 'category']
	list_editable = ['price', 'available']
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(MenuItem, MenuItemAdmin)
 
admin.site.register(MenuItemReview)
admin.site.register(MenuItemRating)