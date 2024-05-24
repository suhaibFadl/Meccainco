from django.contrib import admin
from .models import Product,ProductStatus, \
    ProductImage, Comment


admin.site.register(Product)
admin.site.register(ProductStatus)
admin.site.register(ProductImage)
admin.site.register(Comment)