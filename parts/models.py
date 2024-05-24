from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# from django_countries.fields import CountryField
import datetime


YEAR_CHOICES = [(r,r) for r in range(1984, datetime.date.today().year+1)]

class Brand(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='cars_logos')
    is_car_maker = models.BooleanField(default=False)
    is_part_maker = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=50)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE)
    manufacturing_year = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year
        )
    image = models.ImageField(upload_to='cars_images', default='cars_imagaes/car.png')
    engine = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    def __str__(self):
        return f'{self.brand.name} - {self.name}'


class Category(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(default='category.png',upload_to='categories_logos')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Part(models.Model):
    name = models.CharField(max_length=50)
    car = models.ManyToManyField(Car)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,  null=True, blank=True)
    image = models.ImageField(default='mark.jpeg', upload_to='parts_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.brand}"

    class Meta:
        ordering = ("-created",)