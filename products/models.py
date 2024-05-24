from django.db import models

from django.contrib.auth.models import User
from parts.models import Part
from profiles.models import CustomerProfile, StoreProfile, StoreBranch

# Create your models here.
class ProductStatus(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Prdoduct Status'


class Product(models.Model):
    store = models.ForeignKey(StoreBranch, on_delete=models.CASCADE, null=True)
    part = models.ForeignKey(Part,on_delete=models.CASCADE)
    status = models.ForeignKey(ProductStatus, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    created = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    sales_counter = models.IntegerField(default=0)
    description = models.CharField(max_length=1000, default="Product")
    max_quantity = models.PositiveIntegerField(default=5)  # Set a reasonable default maximum quantity
    min_quantity = models.PositiveIntegerField(default=1)    # Set a reasonable default minimum quantity
    
    def products_count(self):
        return Product.objects.filter(store__store=self.store.store)
    
    def average_rating(self):
        star_rating = self.product_rating.first()
        average_rating =  star_rating.calculate_average_rating() if star_rating else 0
        return average_rating
    
    def __str__(self):
        definition =  f"{self.store.branch_name}-{self.part}"
        for car in self.part.car.all():
            definition += f" - {car.name}"
        return definition

    class Meta:
        ordering = ("-created",)


class ProductImage(models.Model):
    image = models.ImageField(default='products_images/default-image.jpg', upload_to='products_images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Image for {str(self.product.id)}, Store {self.product.store}'


class Comment(models.Model):
    # comment_user = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    # rating = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
                            'self',
                            null=True,
                            blank=True,
                            on_delete=models.CASCADE,
                            related_name='replies'
                            )
    class Meta:
        ordering=['-created']
    
    @property
    def author(self):
        if self.user == self.product.store.store.owner:
            return self.user.storeprofile.name
        return self.user.username
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    

# class CustomerComment(Comment):
#     customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Comment {self.customer} on {self.product}'


# class StoreComment(Comment):
#     Store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Comment {self.store} on {self.product}'