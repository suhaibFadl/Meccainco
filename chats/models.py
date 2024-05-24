# from django.db import models
# from customers.models import Customer
# from stores.models import Store


# class Chat(models.Model):

#     def __str__(self):
#         return str(self.id)


# class CustomerMessage(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
#     message = models.CharField(max_length=1500)
#     image = models.ImageField(upload_to='messages_images')
#     time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.id)


# class StoreMessage(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
#     store = models.OneToOneField(Store, on_delete=models.CASCADE)
#     message = models.CharField(max_length=1500)
#     image = models.ImageField(upload_to='messages_images')
#     time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.id)