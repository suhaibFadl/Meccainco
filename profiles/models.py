from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.db.models import Q


from parts.models import Brand, Category
from phonenumber_field.modelfields import PhoneNumberField
from inboxes.models import Inbox

# from stars_rating.models import WorkshopStarRating


class Location(models.Model):
    longtitude = models.FloatField()
    latitude = models.FloatField()
    city = models.CharField(max_length=250, default='Tripoli')
    country = models.CharField(max_length=250, default='Libya')

    def __str__(self):
        return f'{self.longtitude} ,{self.latitude}'


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='avatar.png', upload_to='users_images')
    phone_num = PhoneNumberField(unique = True, null = True, blank = True)
    inbox = models.OneToOneField(Inbox, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank = True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Customers'
    
    def active_orders(self):
        return self.order_set.filter(status__in=[1, 2, 3]).count()
    
    def active_reservations(self):
        return self.workshopreservation_set.filter(status__in=[1, 2]).count()
    
    def count_unseen_notifications(self):
        return self.message_notification.filter(is_seen=False).count()
    
    def count_unseen_reservations_notifications(self):
        return self.reservation_notifications.filter(is_seen=False).count()
    
    def count_unseen_orders_notifications(self):
        return self.order_notifications.filter(is_seen=False).count()
    
    def save(self, *args, **kwargs):
        self.inbox.owner = self.user.username
        self.inbox.save()
        super(CustomerProfile, self).save(*args, **kwargs)


class StoreProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='storeprofile')
    logo = models.ImageField(default='default_store.png', upload_to='stores_logos')
    name = models.CharField(max_length=50, unique=True)
    brands = models.ManyToManyField(Brand)
    categories = models.ManyToManyField(Category)
    bio = models.CharField(max_length=250)
    facebook = models.EmailField()
    inbox = models.OneToOneField(Inbox, on_delete=models.CASCADE, null=True, blank=True)
    ratings = GenericRelation(Rating, related_query_name='store_rating')
    is_activated = models.BooleanField(default=False)
    ORDER_STATUS = (
        (1, 'New'),
        (2, 'Old'),
    )
    status = models.IntegerField(choices=ORDER_STATUS, default=1)

    
    def branches_locations(self):
        locations = StoreBranch.objects.filter( Q(store_id=self.id) & Q(location__isnull=False))
        return locations
    
    def average_rating(self):
        star_rating = self.store_rating.first()
        average_rating =  star_rating.calculate_average_rating() if star_rating else 0
        return average_rating

    def count_unseen_notifications(self):
        return self.message_notification.filter(is_seen=False).count()
    
    def count_unseen_orders_notifications(self):
        return self.order_notifications.filter(
            is_seen=False
            ).count()
      
    def new_orders(self):
        return self.order_set.filter(
            status__in=[1], 
            confirmed=True
            ).count()
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = 'Stores'
    
    def save(self, *args, **kwargs):
        if self.inbox:
            self.inbox.owner = self.name + ' Store'
            self.inbox.save()
        super(StoreProfile, self).save(*args, **kwargs)


class StoreBranch(models.Model):
    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE, related_name='branches')
    branch_name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    phone_number = PhoneNumberField(unique = True, null = False, blank = False)

    def __str__(self):
        return f"{self.store}-{self.branch_name}"
    
    class Meta:
        verbose_name_plural = 'Stores Branches'


class StoreImage(models.Model):
    image = models.ImageField(upload_to='stores_images')
    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store.name}'
    
    class Meta:
        verbose_name_plural = 'Stores Images'


class StoreReview(models.Model):
    store = models.ForeignKey(StoreProfile, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.customer.user.username + self.store.name + 'Review'
    
    class Meta:
        verbose_name_plural = 'Stores Reviews'
    

class WorkshopProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(default='workshops_logos/workshop.png', upload_to='workshops_logos')
    name = models.CharField(max_length=50)
    brands = models.ManyToManyField(Brand)
    categories = models.ManyToManyField(Category)
    bio = models.CharField(max_length=250)
    facebook = models.EmailField()
    inbox = models.OneToOneField(Inbox, on_delete=models.CASCADE, null=True, blank=True)
    ratings = GenericRelation(Rating, related_query_name='workshop_rating')
    is_activated = models.BooleanField(default=False)
    ORDER_STATUS = (
        (1, 'New'),
        (2, 'Old'),
    )
    status = models.IntegerField(choices=ORDER_STATUS, default=1)

    def branches_locations(self):
        locations = WorkshopBranch.objects.filter( Q(workshop_id=self.id) & Q(location__isnull=False))
        return locations

    def average_rating(self):
        star_rating = self.workshop_rating.first()
        average_rating =  star_rating.calculate_average_rating() if star_rating else 0
        return average_rating

    def count_unseen_reservations_notifications(self):
        return self.reservation_notifications.filter(
            is_seen=False
            ).count()
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = 'Workshops'
    # def new_reservations(self):
    #     return self.reservation_set.filter(status__in=[1], confirmed=True).count()
    
    def save(self, *args, **kwargs):
        if self.inbox != None:
            self.inbox.owner = self.name + ' Workshop'
            self.inbox.save()
        super(WorkshopProfile, self).save(*args, **kwargs)


class WorkshopBranch(models.Model):
    workshop = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE, related_name='branches')
    branch_name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = PhoneNumberField(unique = True, null = False, blank = False)
    
    def __str__(self):
        return f"{self.workshop}-{self.branch_name}"
    
    class Meta:
        verbose_name_plural = 'Workshops Branches'


class WorkshopImage(models.Model):
    image = models.ImageField(upload_to='stores_images')
    Workshop = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.workshop.name}'
    
    class Meta:
        verbose_name_plural = 'Workshops Images'


class WorkshopReview(models.Model):
    workshop = models.ForeignKey(WorkshopProfile, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.customer.user.username + self.store.name \
            + 'Review' + self.workshop.name
    
    class Meta:
        verbose_name_plural = 'Workshops Reviews'


class MeccanicoAdmin(models.Model):
    image = models.ImageField(default='admin.png')
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    inbox = models.OneToOneField(Inbox, on_delete=models.CASCADE, null=True, blank=True)
    
    def new_businesses(self):
        new_stores = StoreProfile.objects.filter(status=1).count()
        new_workshops = WorkshopProfile.objects.filter(status=1).count()
        return new_stores + new_workshops

    def __str__(self):
        return str(self.admin)
    
    class Meta:
        verbose_name_plural = 'Meccainco Admins'