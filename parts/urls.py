from django.contrib import admin
from django.urls import path
from .views import main, part_details, categories_list, category_details,\
        brands_list,brand_details, brand_categories_details


app_name = 'parts'
urlpatterns = [
    path('', main, name='main'),
    path('categories', categories_list, name='categories_list'),
    path('categories/<str:category>/', category_details, name='category_details'),
    path('cars/', brands_list, name='brands_list'),
    path('cars/<str:brand>/', brand_details, name='brand_details'),
    path('cars/<str:brand>/<str:category>/', brand_categories_details,
        name='brand_categories_details'
    ),
    path('parts/<int:pk>/', part_details, name='part_details'),
]