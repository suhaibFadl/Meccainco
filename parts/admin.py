from django.contrib import admin

from .models import Category, Part, Brand, Car


admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(Category)
admin.site.register(Part)
