from django.db import models
from django.contrib.auth.models import User

from profiles.models import StoreProfile, CustomerProfile, \
    WorkshopProfile
from products.models import Product

class StoreStarRating(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(default=0)
    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE, related_name='store_rating')

    def calculate_average_rating(self):
        ratings = StoreStarRating.objects.filter(store=self.store)
        count = ratings.count()
        total_rating = ratings.aggregate(models.Sum('rating')).get('rating__sum')
        if total_rating is not None and count > 0:
            return total_rating / count
        return 0
    
    def __str__(self):
        return f'Rating {self.customer.user} on {self.store}'
    
    
class WorkshopStarRating(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(default=0)
    workshop = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE, related_name='workshop_rating')

    def calculate_average_rating(self):
        ratings = WorkshopStarRating.objects.filter(workshop=self.workshop)
        count = ratings.count()
        total_rating = ratings.aggregate(models.Sum('rating')).get('rating__sum')
        if total_rating is not None and count > 0:
            return total_rating / count
        return 0
    
    def __str__(self):
        return f'Rating {self.customer.user} on {self.workshop}'


class ProductStarRating(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_rating')
    
    def calculate_average_rating(self):
        ratings = ProductStarRating.objects.filter(product=self.product)
        count = ratings.count()
        total_rating = ratings.aggregate(models.Sum('rating')).get('rating__sum')
        if total_rating is not None and count > 0:
            return total_rating / count
        return 0
    
    def __str__(self):
        return f'Rating {self.customer.user} on {self.product}'