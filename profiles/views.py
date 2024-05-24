from django.shortcuts import render, HttpResponseRedirect,\
    get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Count
from django.views.generic.edit import CreateView
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import CustomerProfile ,StoreProfile, StoreBranch,\
    Location, WorkshopProfile,WorkshopBranch
from parts.models import Category, Brand
from stars_rating.models import StoreStarRating, WorkshopStarRating
from .forms import AddStoreProfile, AddWorkshopProfile,\
    AddStoreBranchForm, AddWorkshopBranchForm, CustomerProfileForm
from orders.models import WorkshopReservation
from products.models import Product

########## Customer ##########
def my_profile(request):
    profile = CustomerProfile.objects.get(user=request.user)
    return render(request, 'profiles/my_profile.html', {'profile': profile})

def add_user_location(request, id):
    return render(request, 'profiles/add_user_location.html', {'id': id})

def ajax_add_user_location(request):
    userId = request.GET.get('userId')
    longt = request.GET.get('longitude')
    lat = request.GET.get('latitude')
    city = request.GET.get('city')
    country = request.GET.get('country')
    location =  Location.objects.create(
        longtitude=longt,
        latitude=lat,
        city=city,
        country=country
    )
    CustomerProfile.objects.filter(id=userId).update(location=location)
    return JsonResponse({'data': 'Done'})

def update_user_location(request, id):
    location = CustomerProfile.objects.get(id=id).location
    context = {
        'id': id,
        'location': location,
        }
    return render(request, 'profiles/update_user_location.html', context)

def ajax_update_user_location(request):
    userId = request.GET.get('userId')
    longt = request.GET.get('longitude')
    lat = request.GET.get('latitude')
    city = request.GET.get('city')
    country = request.GET.get('country')
    Location.objects.filter(id=userId).update(
        longtitude=longt,
        latitude=lat,
        city=city,
        country=country
    )
    return JsonResponse({'data': 'Done'})

########## Business ##########
def stores_profiles_list(request):
    stores_profiles = StoreProfile.objects.all()
    cities_q =  Location.objects.values_list('city', flat=True).distinct()
    cities_list = [city for city in cities_q if city.strip()]
    brands_q =  Brand.objects.values_list('name', flat=True).distinct()
    brands_list = [brand for brand in brands_q if brand.strip()]
    categories_q =  Category.objects.values_list('name', flat=True).distinct()
    categories_list = [category for category in categories_q if category.strip()]
    context = {
        'stores_profiles': stores_profiles,
        'cities': cities_list,
        'brands': brands_list,
        'categories': categories_list
        }
    return render(request, 'profiles/stores_profiles_list.html', context)

def store_profile_details(request, store_profile):
    store_profile = StoreProfile.objects.get(name=store_profile)
    branches = StoreBranch.objects.filter(store__name=store_profile)
    star_rating = StoreStarRating.objects.filter(store=store_profile).first()
    print(star_rating)
    average_rating =  star_rating.calculate_average_rating() if star_rating else 0
    products_count = Product.objects.filter(store__store=store_profile).aggregate(total_products=Count('id'))['total_products']
    print("count", products_count)
    context = {
        'store_profile': store_profile,
        'branches': branches,
        'average_rating': average_rating,
        'products_count' : products_count
    }

    return render(request, 'profiles/store_profile_details.html', context)

def workshops_profiles_list(request):
    workshops_profiles = WorkshopProfile.objects.all()
    cities_q =  Location.objects.values_list('city', flat=True).distinct()
    cities_list = [city for city in cities_q if city.strip()]
    brands_q =  Brand.objects.values_list('name', flat=True).distinct()
    brands_list = [brand for brand in brands_q if brand.strip()]
    categories_q =  Category.objects.values_list('name', flat=True).distinct()
    categories_list = [category for category in categories_q if category.strip()]
    context = {
        'workshops_profiles': workshops_profiles,
        'cities': cities_list,
        'brands': brands_list,
        'categories': categories_list
        }
    return render(request, 'profiles/workshops_profiles_list.html', context)

def workshop_profile_details(request, workshop_profile):
    workshop_profile = WorkshopProfile.objects.get(name=workshop_profile)
    branches = WorkshopBranch.objects.filter(workshop__name=workshop_profile)
    star_rating = WorkshopStarRating.objects.filter(workshop=workshop_profile).first()
    average_rating =  star_rating.calculate_average_rating() if star_rating else 0
    can_request = True
    # reservation = ''
    for branch in workshop_profile.branches.all():
        reservation = WorkshopReservation.objects.filter(
            customer = request.user.customerprofile,
            status__in=[1,2,3,4,5]
        ) or None
        if reservation != None :
            can_request = False
            break

    context = {
        'workshop_profile': workshop_profile,
        'branches': branches,
        'average_rating': average_rating,
        'can_request': can_request
    }

    return render(request, 'profiles/workshop_profile_details.html', context)

def add_workshop_branch(request, id):
    obj = get_object_or_404(WorkshopProfile, id = id)
    business_owner = obj.owner
    form = AddWorkshopBranchForm(request.POST or None, request=request)
    
    if request.user != business_owner:
        return redirect("/")
    
    if request.method == 'POST':
        form = AddWorkshopBranchForm(request.POST, initial={'workshop': obj}, request=request)
        if form.is_valid():
            workshop_branch = form.save(commit=False)
            workshop_branch.workshop = obj  # Set the 'store' field to the current StoreProfile
            workshop_branch.save()
            form.save()
            return redirect(f"../workshops/{request.user.workshopprofile.name}")
    else:
        form = AddWorkshopBranchForm(request.POST)

    # dictionary for initial data with
    # field names as keys
    context ={}
    
    context["form"] = form 
    return render(request, "profiles/add_workshop_branch.html", context)

def add_store_branch(request, id):
    obj = get_object_or_404(StoreProfile, id = id)
    business_owner = obj.owner
    form = AddStoreBranchForm(request.POST or None, request=request)
    
    if request.user != business_owner:
        return redirect("/")
    
    if request.method == 'POST':
        form = AddStoreBranchForm(request.POST, initial={'store': obj}, request=request)
        if form.is_valid():
            store_branch = form.save(commit=False)
            store_branch.store = obj  # Set the 'store' field to the current StoreProfile
            store_branch.save()
            form.save()
            return redirect(f"../stores/{request.user.storeprofile.name}")
    else:
        form = AddStoreBranchForm(request.POST)

    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")
    print("\\\\\\\\\\\\",form)
    # add form dictionary to context
    context["form"] = form 
    return render(request, "profiles/add_store_branch.html", context)

def update_branch(request, type, id):
    if type == 'store':
        obj = get_object_or_404(StoreBranch, id = id)
        business_owner = obj.store.owner
        form = AddStoreBranchForm(request.POST or None, instance = obj, request=request)
    elif type == 'workshop':
        obj = get_object_or_404(WorkshopBranch, id = id)
        business_owner = obj.workshop.owner
        form = AddWorkshopBranchForm(request.POST or None, instance = obj, request=request)
    
    if request.user != business_owner:
        return redirect("/")
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id

    # pass the object as instance in form
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        if type == 'store':
            return redirect(f"../../stores/{request.user.storeprofile.name}")
        elif type == 'workshop':
            return redirect(f"../../workshops/{request.user.workshopprofile.name}")
 
    # add form dictionary to context
    context["form"] = form
    context["branch"] = obj
    context["type"] = type
 
    return render(request, "profiles/update_branch.html", context)

# def update_branch(request, type, id):
#     if type == 'store':
#         obj = get_object_or_404(StoreBranch, id = id)
#         business_owner = obj.store.owner
#         form = AddStoreBranchForm(request.POST or None, instance = obj)
#     elif type == 'workshop':
#         obj = get_object_or_404(WorkshopBranch, id = id)
#         business_owner = obj.workshop.owner
#         form = AddWorkshopBranchForm(request.POST or None, instance = obj)
    
#     if request.user != business_owner:
#         return redirect("/")
#     # dictionary for initial data with
#     # field names as keys
#     context ={}
 
#     # fetch the object related to passed id

#     # pass the object as instance in form
 
#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect("/")
 
#     # add form dictionary to context
#     context["form"] = form
#     context["branch"] = obj
#     context["type"] = type
 
#     return render(request, "profiles/update_branch.html", context)

########## Business Location ##########
def add_location(request, id, type):
    context = {
        'id': id,
        'business_type': type
        }
    return render(request, 'profiles/add_location.html', context)

def create_location(request):
    branch_id = request.GET.get('branchId')
    business_type = request.GET.get('businessType')
    longt = request.GET.get('longitude')
    lat = request.GET.get('latitude')
    city = request.GET.get('city')
    country = request.GET.get('country')
    location =  Location.objects.create(
        longtitude=longt,
        latitude=lat,
        city=city,
        country=country
        )
    
    if business_type == "store":
        StoreBranch.objects.filter(id=branch_id).update(location=location)
    elif business_type == "workshop":
        WorkshopBranch.objects.filter(id=branch_id).update(location=location)

    return JsonResponse({'data': 'Done'})

def update_location(request, id):
    location = Location.objects.get(id=id)
    context = {
        'id': id,
        'location': location,
        }
    return render(request, 'profiles/update_location.html', context)

def confirm_update_location(request):
    location_id = request.GET.get('locationId')
    longt = request.GET.get('longitude')
    lat = request.GET.get('latitude')
    city = request.GET.get('city')
    country = request.GET.get('country')
    print('heeere', location_id, longt, lat, city, country)
    Location.objects.filter(id=location_id).update(
        longtitude=longt,
        latitude=lat,
        city=city,
        country=country
    )
    return JsonResponse({'data': 'Done'})

def direction(request, id):
    location = Location.objects.get(id=id)
    return render(request, 'profiles/direction.html', {'location': location})

def adminstration(request):
    stores = StoreProfile.objects.all()
    workshops = WorkshopProfile.objects.all()
    customers = CustomerProfile.objects.all()
    context = {}
    context['stores'] = stores
    context['workshops'] = workshops
    context['customers'] = customers
    return render(request, 'profiles/adminstration.html', context)

def ajax_activation(request):
    business_id = request.GET.get('obj-id')
    business_type = request.GET.get('business-type')
    if business_type == 'store':
        business = StoreProfile.objects.get(id=business_id)
    elif business_type == 'workshop':
        business = WorkshopProfile.objects.get(id=business_id)
    
    if business.is_activated:
        business.is_activated = False
    else:
        business.is_activated = True
    business.save()
    return JsonResponse({'data': business.is_activated})

def ajax_delete(request):
    business_id = request.GET.get('obj-id')
    business_type = request.GET.get('business-type')
    if business_type == 'store':
        business = StoreProfile.objects.filter(id=business_id)
    elif business_type == 'workshop':
        business = WorkshopProfile.objects.filter(id=business_id)
    elif business_type == 'free':
        business = CustomerProfile.objects.filter(id=business_id)
    
    business.delete()
    return JsonResponse({'data': 'done'})


def business_selection(request):
    return render(request, 'profiles/business_selection.html')

# class AddStoreProfileView(CreateView):
#     model = StoreProfile
#     form_class = AddStoreProfile
#     template_name = 'profiles/add_store_profile.html'
#     # success_url = '/success/' 

def add_store_profile(request):
    if request.method == 'POST':
        form = AddStoreProfile(request.POST, request.FILES)
        if form.is_valid():
            store_profile = form.save(commit=False)
            store_profile.owner = request.user  # Assign the owner (user) here
            store_profile.save()
            return redirect('/')
    else:
        form = AddStoreProfile()
    
    # Set the user attribute of the form after creating the instance
    form.user = request.user
    
    context = {'form': form}
    return render(request, 'profiles/add_store_profile.html', context)

def update_store_profile(request):
    store_profile = request.user.storeprofile

    if request.method == 'POST':
        form = AddStoreProfile(request.POST, instance=store_profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        # Initialize the form with the current store name
        form = AddStoreProfile(instance=store_profile)

    context = {'form': form}
    return render(request, 'profiles/update_store_profile.html', context)

def add_workshop_profile(request):
    if request.method == 'POST':
        form = AddWorkshopProfile(request.POST, request.FILES)
        if form.is_valid():
            workshop_profile = form.save(commit=False)
            workshop_profile.owner = request.user  # Assign the owner (user) here
            workshop_profile.save()
            return redirect('/')
    else:
        form = AddWorkshopProfile()
    
    # Set the user attribute of the form after creating the instance
    form.user = request.user
    
    context = {'form': form}
    return render(request, 'profiles/add_workshop_profile.html', context)

def update_workshop_profile(request):
    workshop_profile = request.user.workshopprofile

    if request.method == 'POST':
        form = AddWorkshopProfile(request.POST, instance=workshop_profile)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        # Initialize the form with the current store name
        form = AddWorkshopProfile(instance=workshop_profile)
    context = {'form': form}
    return render(request, 'profiles/update_workshop_profile.html', context)

def update_customer_profile(request):
    customer_profile = request.user.customerprofile
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer_profile)
        if form.is_valid():
            if 'image' in request.FILES:
                # If a new image was uploaded, replace the existing one
                uploaded_image = request.FILES['image']
                customer_profile.image = SimpleUploadedFile(uploaded_image.name, uploaded_image.read())
            form.save()
            return redirect('/')
    else:
        # Initialize the form with the current store name
        form = CustomerProfileForm(instance=customer_profile)
    context = {'form': form}
    return render(request, 'profiles/update_customer_profile.html', context)