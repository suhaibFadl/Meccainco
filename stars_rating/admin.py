from django.contrib import admin
from .models import StoreStarRating, WorkshopStarRating,\
    ProductStarRating

admin.site.register(StoreStarRating)
admin.site.register(WorkshopStarRating)
admin.site.register(ProductStarRating)