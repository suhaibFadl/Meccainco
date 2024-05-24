from django.shortcuts import render
from .models import Part, Category, Brand
from profiles.models import StoreProfile


def main(request):
    parts = Part.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    stores = StoreProfile.objects.all()
    context = {
        'parts': parts,
        'brands': brands,
        'categories': categories,
        'stores': stores,
        }
    return render(request, 'parts/main.html', context)


def part_details(request, pk):
    part = Part.objects.get(pk=pk)
    return render(request, 'parts/part_details.html', {'part': part})


def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'parts/categories_list.html', {'categories': categories})

def category_details(request, category):
    parts = Part.objects.filter(category=category)
    return render(request, 'parts/categories_details.html', {'parts': parts})


def brands_list(request):
    brands = Brand.objects.filter(is_car_maker=True)
    return render(request, 'parts/brands_list.html', {'brands':brands})

def brand_details(request, brand):
    brand = Brand.objects.get(name=brand)
    categories = Category.objects.all()
    print(brand, categories)
    context = {
        'categories': categories,
        'brand': brand,
        }
    return render(request, 'parts/brand_details.html', context)

def brand_categories_details(request, brand, category):
    parts = Part.objects.filter(car__brand__name=brand, category__name=category)
    context = {
        'parts': parts
        }
    return render(request, 'parts/brand_categories_details.html', context)