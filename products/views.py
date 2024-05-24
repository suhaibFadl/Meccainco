from django.shortcuts import render, get_object_or_404, \
                            HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponse
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Avg
from django.db.models import Q
from django.core import serializers


from .models import Product, Comment, ProductImage
from orders.models import Order
from parts.models import Part, Category, Brand, Car
from stars_rating.models import ProductStarRating, WorkshopStarRating, \
    StoreStarRating
from profiles.models import StoreProfile, WorkshopProfile,\
    WorkshopBranch, StoreBranch, Location
from .forms import AddProductForm, AddCommentForm


def index(request):
    products = Product.objects.all()
    brands = Brand.objects.all()[:4]
    categories = Category.objects.all()
    stores = StoreProfile.objects.all()
    best_seller = Product.objects.all().order_by('-sales_counter')[:10]
    best_stores =  StoreProfile.objects.annotate(average_rating=Avg('store_rating__rating')).order_by('-average_rating')[:10]
    best_workshops = WorkshopProfile.objects.annotate(average_rating=Avg('workshop_rating__rating')).order_by('-average_rating')[:10]
    # my_orders = Order.objects.filter(customer=request.user.customerprofile).exclude(status__in=[3, 4]) or None
    context = {
        'products': products,
        'brands': brands,
        'categories': categories,
        'stores': stores,
        'best_workshops': best_workshops[:5],
        'best_seller': best_seller[:5],
        'best_stores': best_stores[:5],        
        }
    return render(request, 'products/index.html', context)

def product_details(request, id):
    product = Product.objects.get(id=id)
    comments = Comment.objects.filter(product_id=id)
    num_of_comments = comments.count
    comment_form = AddCommentForm(request.POST or None)
    star_rating = ProductStarRating.objects.filter(product=product).first()
    average_rating =  star_rating.calculate_average_rating() if star_rating else 0
    related_workshops = WorkshopProfile.objects.filter(branches__location__city='Tripoli') 

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        for image in images:
            image = ProductImage.objects.create(
                product = product,
                image=image,
            )

        return redirect(f'../../products/{product.id}')
    
    context = {
        'product': product,
        'comments': comments,
        'num_of_comments': num_of_comments,
        'comment_form': comment_form,
        'average_rating': average_rating,
        'related_workshops': related_workshops
        }
    return render(request, 'products/product_details.html', context)

def add_comment(request):
    if request.method == 'POST':
        response_data = {}
        content = request.POST.get('content')
        product_id = request.POST.get('product_id')
        print(product_id)

        product = Product.objects.get(id=product_id)
        try:
            parent = request.Post.get('parent')
        except:
            parent=None
        new_comment = Comment(content=content ,product=product ,parent=parent , user=request.user)
        new_comment.save()

        response_data['content'] = content
        response_data['author'] = new_comment.author
        response_data['date'] = new_comment.created.strftime('%b. %d, %Y, %I:%M %p')

        # response_data['created'] = new_comment.created

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'{product_id}_product_comments', {
                'type':'add_comment',
                'value':json.dumps(response_data),
            }
        )
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json")
    else:
        return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )

def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'products/categories_list.html', {'categories': categories})

def category_details(request, category):
    products = Product.objects.filter(part__category__name=category)
    cities_q =  Location.objects.values_list('city', flat=True).distinct()
    cities_list = [city for city in cities_q if city.strip()]
    brands_q =  Brand.objects.values_list('name', flat=True).distinct()
    brands_list = [brand for brand in brands_q if brand.strip()]
    context = {
        'category': category,
        'products': products,
        'cities': cities_list,
        'brands': brands_list
    }
    return render(request, 'products/category_details.html', context)

def brands_list(request):
    brands = Brand.objects.filter(is_car_maker=True)
    return render(request, 'products/brands_list.html', {'brands':brands})

def brand_details(request, brand):
    brand = Brand.objects.get(name=brand)
    workshops = WorkshopProfile.objects.filter(brands=brand)
    stores = StoreProfile.objects.filter(brands=brand)
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'brand': brand,
        'workshops': workshops[:4],
        'stores': stores[:4],
        }
    return render(request, 'products/brand_details.html', context)

def brand_stores_details(request, brand):
    brand = Brand.objects.get(name=brand)
    stores = StoreProfile.objects.filter(brands=brand)
    cities_q =  Location.objects.values_list('city', flat=True).distinct()
    cities_list = [city for city in cities_q if city.strip()]
    categories_q = Category.objects.values_list('name', flat=True).distinct()
    categories_list = [category for category in categories_q if category.strip()]

    context = {
        'brand': brand,
        'stores': stores,
        'cities': cities_list,
        'categories': categories_list,
        }
    return render(request, 'products/brand_stores_details.html', context)

def brand_workshops_details(request, brand):
    brand = Brand.objects.get(name=brand)
    workshops = WorkshopProfile.objects.filter(brands=brand)
    cities_q =  Location.objects.values_list('city', flat=True).distinct()
    cities_list = [city for city in cities_q if city.strip()]
    categories_q = Category.objects.values_list('name', flat=True).distinct()
    categories_list = [category for category in categories_q if category.strip()]
    context = {
        'brand': brand,
        'workshops': workshops,
        'cities': cities_list,
        'categories': categories_list,
        }
    return render(request, 'products/brand_workshops_details.html', context)

def brand_categories_details(request, brand, category):
    products = Product.objects.filter(part__car__brand__name=brand, part__category__name=category)
    cities_q =  Location.objects.values_list('city', flat=True).distinct()
    cities_list = [city for city in cities_q if city.strip()]
    models_q = Car.objects.values_list('name', flat=True).distinct()
    models_list = [car for car in models_q if car.strip()]
    context = {
        'products': products,
        'cities': cities_list,
        'models': models_list,
        'brand': brand,
        'category': category
        }
    return render(request, 'products/brand_categories_details.html', context)

# def add_product(request):
#     context ={}
#     form = AddProductForm(request.POST or None)
#     if form.is_valid():
#         form.instance.store_name = request.user.storeprofile.name
#         print(form.instance.name)
#         form.save()
  
#     context['form']= form
#     return render(request, "products/add_product.html", context)

def crud_permission(user, store_owner):
    return user == store_owner

class AddProduct(CreateView):    
    model = Product
    form_class = AddProductForm
    template_name = "products/add_product.html"
    success_url = reverse_lazy('profiles:')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(AddProduct, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        # Assuming 'store_profile' is a string variable representing the store's profile name
        store_profile = self.request.user.storeprofile.name

        # Construct the URL using reverse_lazy and provide the store_profile argument
        return reverse_lazy('profiles:store_profile_details', kwargs={'store_profile': store_profile})
    
def ajax_delete_product(request):
    product_id = request.GET.get('obj-id')
    product = Product.objects.filter(id=product_id)
    product.delete()
    return JsonResponse({'data': 'done'})

def load_parts(request):
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')
    parts = Part.objects.filter(category_id=category_id)
    return render(request, 'products/ajax/parts_dropdown_list_options.html', {'parts': parts})

def update_product(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Product, id = id)
 
    # pass the object as instance in form
    form = AddProductForm(request.POST or None, instance = obj, user=request.user)
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "products/update_product.html", context)

def delete_product(request, id):     
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Product, id = id)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")
 
    return render(request, "products/delete_product.html", context)

def add_product_image(request, id):
    product = get_object_or_404(Product, id = id)
    if not crud_permission(request.user, product.store.store.owner):
        return redirect("/")
    
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        for image in images:
            image = ProductImage.objects.create(
                product = product,
                image=image,
            )

        return redirect(f'../../products/{product.id}')

    return render(request, 'products/add_product_image.html', {})

def delete_product_image(request, id):     

    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(ProductImage, id = id)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")
 
    return render(request, "products/delete_product_image.html", context)

def ajax_search_view(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        query = request.GET.get('query', '')
        print('query', query)
        results = []
        # Search in WorkshopProfiles
        workshop_profiles = WorkshopProfile.objects.filter(
            Q(name__icontains=query) |
            Q(brands__name__icontains=query) |
            Q(categories__name__icontains=query) |
            Q(branches__location__city__icontains=query)
        ).distinct()
        results.extend(workshop_profiles)
        # Search in StoreProfiles
        store_profiles = StoreProfile.objects.filter(
            Q(name__icontains=query) |
            Q(brands__name__icontains=query) |
            Q(categories__name__icontains=query) |
            Q(branches__location__city__icontains=query)
        ).distinct()
        results.extend(store_profiles)
        print('store:', store_profiles)
         # Search in Products
        products = Product.objects.filter(
            Q(part__name__icontains=query) |
            Q(part__car__name__icontains=query) |
            Q(part__car__brand__name__icontains=query) |
            Q(part__category__name__icontains=query) |
            Q(store__store__name__icontains=query)
        ).select_related('store', 'part')  # Include related StoreProfile and Part objects
        results.extend(products)

        # Serialize fields of model instances to dictionaries
        products_serialized_results = []
        stores_serialized_results = []
        workshops_serialized_results = []
        for obj in results:
            serialized_fields = serializers.serialize('python', [obj])[0]['fields']
            
            # Include product ID, store ID and name, and part ID and name in serialized fields
            if isinstance(obj, StoreProfile):
                serialized_fields['store_id'] = obj.id  # Include the ID directly
                rating = StoreStarRating.objects.filter(store=obj).first()
                average_rating = rating.calculate_average_rating() if rating else 0
                serialized_fields['store_rating'] = average_rating 
                stores_serialized_results.append(serialized_fields)
            elif isinstance(obj, WorkshopProfile):
                serialized_fields['workshop_id'] = obj.id  # Include the ID directly
                rating = WorkshopStarRating.objects.filter(workshop=obj).first()
                average_rating = rating.calculate_average_rating() if rating else 0
                serialized_fields['workshop_rating'] = average_rating 
                workshops_serialized_results.append(serialized_fields)
            elif isinstance(obj, Product):
                serialized_fields['product_id'] =  obj.id
                rating = ProductStarRating.objects.filter(product=obj).first()
                average_rating = obj.average_rating()
                serialized_fields['brand'] = obj.part.brand.name 
                serialized_fields['product_rating'] = average_rating 
                
                if 'store' in serialized_fields:
                    store_obj = obj.store
                    serialized_fields['store'] = {
                        'id': store_obj.id,
                        'name': store_obj.store.name,
                    }
                
                if 'part' in serialized_fields:
                    part_obj = obj.part
                    serialized_fields['part'] = {
                        'id': part_obj.id,
                        'name': part_obj.name,
                        'image': part_obj.image.url if part_obj.image else None,
                    }
                serialized_fields['status'] = obj.status.name
                products_serialized_results.append(serialized_fields)

        # print('resulsts',products_serialized_results)
        print('resulsts',stores_serialized_results)
        # print('resulsts',workshops_serialized_results)

        all_serialized_results = {
            'products': products_serialized_results,
            'stores': stores_serialized_results,
            'workshops': workshops_serialized_results
        }
        return JsonResponse({'results': all_serialized_results})
    else:
        return JsonResponse({}, status=400)

def load_brands(request):
    brands = Brand.objects.all()
    brand_data = [{'id': brand.id, 'name': brand.name} for brand in brands]
    return JsonResponse({'brands': brand_data})

def load_cars(request):
    brand = request.GET.get('brand')
    print('brand:', brand)
    try:
        cars = Car.objects.filter(brand__id=int(brand))
    except:
        cars = Car.objects.filter(brand__name=brand)
    # if isinstance(brand , int):
       
    # else:
    #     cars = Car.objects.filter(brand__name=brand)
    # if isinstance(brand, int):
    #     cars = Car.objects.filter(brand__id=brand)
    # else:
    #     cars = Car.objects.filter(brand__name=brand)
    car_data = [{'id': car.id, 'name': car.name, 'year': car.manufacturing_year} for car in cars]
    print(car_data)
    return JsonResponse({'cars': car_data})

def load_years(request):
    car = request.GET.get('car')
    print(car)
    years = Car.objects.filter(name=car).values_list('manufacturing_year', flat=True).distinct()
    return JsonResponse({'years': list(years)})

def search_results_view(request):
    return render(request, 'products/search_results.html')

def ajax_filter_view(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        brand = request.GET.get('brand')
        car = request.GET.get('car')
        year = request.GET.get('year')
        results = []
        products = Product.objects.filter(
            Q(part__car__name=car) &
            Q(part__car__brand__name=brand) &
            Q(part__car__manufacturing_year=year) 
        ).select_related('store', 'part')  # Include related StoreProfile and Part objects
        results.extend(products)
        
        serialized_results = [] 
        for obj in results:
            serialized_fields = serializers.serialize('python', [obj])[0]['fields']
            serialized_fields['product_id'] =  obj.id
            rating = ProductStarRating.objects.filter(product=obj).first()
            average_rating = rating.calculate_average_rating() or 0
            serialized_fields['brand'] = obj.part.brand.name 
            serialized_fields['product_rating'] = average_rating 
            
            if 'store' in serialized_fields:
                store_obj = obj.store
                serialized_fields['store'] = {
                    'id': store_obj.id,
                    'name': store_obj.store.name,
                }
            
            if 'part' in serialized_fields:
                part_obj = obj.part
                serialized_fields['part'] = {
                    'id': part_obj.id,
                    'name': part_obj.name,
                    'image': part_obj.image.url if part_obj.image else None,
                }
            serialized_fields['status'] = obj.status.name
            serialized_results.append(serialized_fields)

        return JsonResponse({'results': serialized_results})
    else:
        return JsonResponse({}, status=400)
    
def filter_results_view(request):
    return render(request, 'products/filter_results.html')

def brand_categories_filter(request):
    brand = request.GET.get('brand')
    city = request.GET.get('city')
    car = request.GET.get('car')
    category = request.GET.get('category')
    year = request.GET.get('year')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    results = []
    products = Product.objects.all()
    print(car, year, min_price, max_price)

    if year != '':
        products = products.filter(Q(part__car__manufacturing_year=int(year)))

    if min_price != '' and max_price != '':
        products = products.filter(Q(price__range=(int(min_price), int(max_price))))
    elif min_price != '' and max_price == '': 
        max_price = min_price
        products = products.filter(Q(price__range=(int(min_price), int(max_price))))
    elif min_price == '' and max_price != '':
        min_price = 0
        products = products.filter(Q(price__range=(int(min_price), int(max_price))))

    # Check if 'city' is not empty before applying the filter
    if city != '' :
        products = products.filter(Q(store__location__city=city))
    if car != '' :
        products = products.filter(Q(part__car__name=car))

    if category != '':
        products = products.filter(Q(part__category__name=category))
    
    if brand != '':
        products = products.filter(Q(part__car__brand__name=brand))
    
    products.select_related('store', 'part')  # Include related StoreProfile and Part objects
    results.extend(products)
    
    serialized_results = [] 
    for obj in results:
        serialized_fields = serializers.serialize('python', [obj])[0]['fields']
        serialized_fields['product_id'] =  obj.id
        rating = ProductStarRating.objects.filter(product=obj).first()
        average_rating = obj.average_rating() or 0
        serialized_fields['brand'] = obj.part.brand.name 
        serialized_fields['product_rating'] = average_rating 
        
        if 'store' in serialized_fields:
            store_obj = obj.store
            serialized_fields['store'] = {
                'id': store_obj.id,
                'name': store_obj.store.name,
            }
        
        if 'part' in serialized_fields:
            part_obj = obj.part
            serialized_fields['part'] = {
                'id': part_obj.id,
                'name': part_obj.name,
                'image': part_obj.image.url if part_obj.image else None,
            }
        serialized_fields['status'] = obj.status.name
        serialized_results.append(serialized_fields)
    return JsonResponse({'products': serialized_results})

def brand_stores_filter(request):
    brand = request.GET.get('brand')
    category = request.GET.get('category')
    city = request.GET.get('city')
    results = []
    stores = StoreProfile.objects.all()
    if brand != '':
        stores= StoreProfile.objects.filter(brands__name=brand)
    if city != '' :
        stores = stores.filter(Q(branches__location__city=city))
    if category != '' :
        stores = stores.filter(Q(categories__name=category))

    results.extend(stores)
    serialized_results = [] 
    for obj in results:
        serialized_fields = serializers.serialize('python', [obj])[0]['fields']
        serialized_fields['store_id'] =  obj.id
        average_rating = obj.average_rating() or 0
        serialized_fields['store_rating'] = average_rating
        categories_list = [cateogry.name for cateogry in obj.categories.all()] 
        serialized_fields['categories'] = categories_list
        # if 'store' in serialized_fields:
        #     store_obj = obj.store
        #     serialized_fields['store'] = {
        #         'id': store_obj.id,
        #         'name': store_obj.store.name,
        #     }
        
        # if 'part' in serialized_fields:
        #     part_obj = obj.part
        #     serialized_fields['part'] = {
        #         'id': part_obj.id,
        #         'name': part_obj.name,
        #         'image': part_obj.image.url if part_obj.image else None,
        #     }
        # serialized_fields['status'] = obj.status.name
        serialized_results.append(serialized_fields)
    print('result:', serialized_results)
    
    return JsonResponse({'stores': serialized_results})

def brand_workshops_filter(request):
    brand = request.GET.get('brand')
    category = request.GET.get('category')
    city = request.GET.get('city')
    results = []
    workshops = WorkshopProfile.objects.all()

    if brand != '':
        workshops= WorkshopProfile.objects.filter(brands__name=brand)
    # Check if 'city' is not empty before applying the filter
    print('city', city)
    if city != '' :
        workshops = workshops.filter(Q(branches__location__city=city))
    

    print('category', category)
    if category != '' :
        workshops = workshops.filter(Q(categories__name=category))

    results.extend(workshops)
    serialized_results = [] 
    for obj in results:
        serialized_fields = serializers.serialize('python', [obj])[0]['fields']
        serialized_fields['workshop_id'] =  obj.id
        average_rating = obj.average_rating() or 0
        serialized_fields['workshop_rating'] = average_rating
        categories_list = [cateogry.name for cateogry in obj.categories.all()] 
        serialized_fields['categories'] = categories_list
        
        serialized_results.append(serialized_fields)
    print('result:', serialized_results)
    return JsonResponse({'workshops': serialized_results})

def not_found_404(request):
    return render(request, 'products/404.html')