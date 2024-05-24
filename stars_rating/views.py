from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import StoreStarRating, WorkshopStarRating,\
    ProductStarRating

from profiles.models import StoreProfile, WorkshopProfile
from products.models import Product

@login_required
def business_rate_model(request):
        rating_value = int(request.GET.get('rating'))
        business_type = request.GET.get('businessType')
        business_id = request.GET.get('businessId')
        if business_type == 'store':
            store = StoreProfile.objects.get(id=business_id)
            StoreStarRating.objects.update_or_create(
            customer=request.user.customerprofile,
            store = store,    
            defaults={'rating': rating_value}
            )
            store_rating = StoreStarRating.objects.filter(store=store).first()
            new_average = store_rating.calculate_average_rating() if new_average else 0

        elif business_type == 'workshop':
            workshop = WorkshopProfile.objects.get(id=business_id)
            WorkshopStarRating.objects.update_or_create(
            customer=request.user.customerprofile,
            workshop = workshop,    
            defaults={'rating': rating_value}
            )
            workshop_rating = WorkshopStarRating.objects.filter(workshop=workshop).first()
            new_average = workshop_rating.calculate_average_rating() if workshop_rating else 0
    
        return JsonResponse({'new_average': new_average})

@login_required
def product_rate_model(request):
    print('heeeeeeeeeeeey')
    rating_value = int(request.GET.get('rating'))
    print("rate rate rate", rating_value)
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    ProductStarRating.objects.update_or_create(
        customer=request.user.customerprofile,
        product=product,
        defaults={'rating': rating_value}
    )
    return JsonResponse({'success': False})

