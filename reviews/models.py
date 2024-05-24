# from django.db import models
# from django.contrib.auth.models import User

# from products.models import Product
# from stars_rating.models import ProductStarRating

# # Create your models here.

# class Comment(models.Model):
#     # comment_user = models.CharField(max_length=100)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     content = models.TextField(max_length=1000)
#     # rating = models.FloatField(default=0)
#     created = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey(
#                             'self',
#                             null=True,
#                             blank=True,
#                             on_delete=models.CASCADE,
#                             related_name='replies'
#                             )
#     class Meta:
#         ordering=['-created']
    
#     @property
#     def author(self):
#         if self.user == self.product.store.store.owner:
#             return self.user.storeprofile.name
#         return self.user.username
    
#     @property
#     def children(self):
#         return Comment.objects.filter(parent=self).reverse()

#     @property
#     def is_parent(self):
#         if self.parent is None:
#             return True
#         return False

# class ProductReview(models.Model):
#     rating = models.OneToOneField(ProductStarRating, on_delete=models.CASCADE)
