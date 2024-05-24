from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


from profiles.models import CustomerProfile, StoreProfile, \
    WorkshopBranch, WorkshopProfile
from products.models import Product
from parts.models import Car, Category


class Order(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE)
    ORDER_STATUS = (
        (1, 'Waiting'),
        (2, 'In Progress'),
        (3, 'En Route'),
        (4, 'Delivered'),
        (5, 'Store Canceled'),
        (6, 'Customer Canceled'),
        (7, 'Product Unavailable')
    )
    status = models.IntegerField(choices=ORDER_STATUS, default=1)
    created_date = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    confirmed = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    # order_total = models.IntegerField(default=0)
    
    def __str__(self):
        """display text"""
        return f'Order {self.customer} at {self.store }- Date: {self.created_date}'
    
    @property
    def total(self):
        """sum the total cost of all items"""
        # products = self.orders.all().values_list('product_id')
        items = self.orders.all()
        # print('products:', products)
        total = 0

        if items:
            for item in items:
                print(item.quantity)
                total += item.item_total_price
        return total
    
    # def save(self, *args, **kwargs):
    #     self.order_total = self.total()
    #     super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='order_item')
    quantity = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(10)])
    added_date = models.DateTimeField(auto_now_add=True)
    item_total_price = models.IntegerField()
    
    def __str__(self):
        # return str(self.added_date)
        return f'Item Total: {self.quantity * self.product.price} (Quantity: ' \
        f'{self.quantity}, Price: {self.product.price}) - ' \
        f'Product: {self.product.part.name} '

    def subtotal(self):
        """Return per item total's"""
        total = self.quantity * self.product.price

        if total is None:
            total = 0

        return total
    
    def save(self, *args, **kwargs):
        self.item_total_price = self.subtotal()
        super(OrderItem, self).save(*args, **kwargs)


class OrderItemsList(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, null=True, blank=True)

    def __str__(self):
        return f'{self.customer.user.username} Order Items List'
    

class StoreOrderNotification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        StoreProfile ,
        on_delete=models.CASCADE, 
        related_name='order_notifications'
    )
    is_seen = models.BooleanField(default=False)
    ORDER_STATUS = (
        (1, 'Waiting'),
        (5, 'Customer Canceled'),
    )
    status = models.IntegerField(choices=ORDER_STATUS, default=1)
    def __str__(self):
        return f'{self.order.customer} requested a \
                order at {self.receiver}'

    
class CustomerOrderNotification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        CustomerProfile , 
        on_delete=models.CASCADE, 
        related_name='order_notifications')
    ORDER_STATUS = (
       (2, 'In Progress'),
        (3, 'Delivered'),
        (4, 'Store Canceled'),
    )
    status = models.IntegerField(choices=ORDER_STATUS, default=2)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.order.customer} requested a \
            order at {self.receiver}'


class WorkshopReservation(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    workshop = models.ForeignKey(WorkshopBranch, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Category, null=True, blank=True)
    RESERVATION_STATUS = (
        (1, 'Requested'),
        (2, 'Make an Appointment'),
        (3, 'Confirmed'),
        (4, 'Car In The Garage'),
        (5, 'Under The Maintenance'),
        (6, 'Fixed'),
        (7, 'Workshop Canceled'),
        (8, 'Customer Canceled'),
        (8, 'Expired'),
    )
    status = models.IntegerField(choices=RESERVATION_STATUS, default=1)
    time = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.customer} reservation with {self.workshop} - {self.time}'
    

class ReservationImage(models.Model):
    image = models.ImageField(upload_to='reservations_images')
    reservation = models.ForeignKey(WorkshopReservation, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return f'Image for {self.reservation.customer}, car{self.reservation.car}, Workshop {self.reservation.workshop}'
    

class WorkshopReservationNotification(models.Model):
    reservation = models.ForeignKey(WorkshopReservation, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        WorkshopProfile ,
        on_delete=models.CASCADE, 
        related_name='reservation_notifications')
    is_seen = models.BooleanField(default=False)
    RESERVATION_STATUS = (
        (1, 'Requested'),
        (5, 'Customer Canceled'),
    )
    status = models.IntegerField(choices=RESERVATION_STATUS, default=1)
    def __str__(self):
        return f'{self.reservation.customer} requested a \
            resevation at {self.receiver}'

    
class CustomerReservationNotification(models.Model):
    reservation = models.ForeignKey(WorkshopReservation, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        CustomerProfile , 
        on_delete=models.CASCADE, 
        related_name='reservation_notifications')
    RESERVATION_STATUS = (
        (2, 'Confirmed'),
        (3, 'Done'),
        (4, 'Workshop Canceled'),
    )
    status = models.IntegerField(choices=RESERVATION_STATUS, default=2)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.reservation.customer} requested a \
            resevation at {self.receiver}'

    