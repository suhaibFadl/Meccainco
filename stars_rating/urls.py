from django.contrib import admin
from django.urls import path
from .views import business_rate_model, product_rate_model
app_name = 'stars_rating'
urlpatterns = [
    path('business_rate_model', business_rate_model, name='business_rate_model'), 
    path('product_rate_model', product_rate_model, name='product_rate_model'), 
]