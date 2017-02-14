from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu:menu_list_by_category', args=[self.slug])

class MenuItem(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    category = models.ForeignKey(Category,
                        related_name='menu_items')
    price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu:menu_detail', args=[self.id, self.slug])

class MenuItemReview(models.Model):
	item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	review = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'Review of {} by {}'.format(self.item, self.user)

class MenuItemRating(models.Model):
	item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
	user= models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.PositiveIntegerField()

	def __str__(self):
		return '{} from {} on {}'.format(self.rating, self.user, self.item)