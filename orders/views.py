from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Q, Max
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Order, OrderItem,  WorkshopReservation, \
    WorkshopReservationNotification, CustomerReservationNotification,\
    CustomerOrderNotification, StoreOrderNotification, ReservationImage
    
from products.models import Product
from parts.models import Car
from stars_rating.models import WorkshopStarRating
from profiles.models import WorkshopProfile,  WorkshopBranch
from .forms import RequestReservationForm
from stars_rating.models import ProductStarRating


def my_orders(request):
    orders = Order.objects.filter(customer=request.user.customerprofile)
    CustomerOrderNotification.objects.filter(is_seen=False)\
    .update(is_seen=True)
    return render(request, 'orders/my_orders.html', {'my_orders': orders})

def store_orders(request, id):
    orders = Order.objects.filter(store__id=id, confirmed=True)
    StoreOrderNotification.objects.filter(is_seen=False)\
    .update(is_seen=True)
    # orders = Order.objects.filter(Q(status=1) | Q(status=2), store=request.user.storeprofile, confirmed=True)
    return render(request, 'orders/store_orders.html', {'orders': orders})

def order(request, id):
    order = Order.objects.get(id=id)
    items = order.orders.all()

    product_ratings = {}

    for item in items:
        # Fetch the rating of the current user for the product
        rating = ProductStarRating.objects.filter(product=item.product, customer=request.user.customerprofile).values('rating').first() or 0
        
        # If there's no rating, set it to 0
        rating_value = rating['rating'] if rating else 0

        product_ratings[item.id] = rating_value

    context = {
        'order': order,
        'product_ratings': product_ratings,
        }
    return render(request, 'orders/order.html', context)

def store_order(request, id):
    order = Order.objects.get(id=id)

    try:
        if (not request.user.meccanicoadmin) or request.user != order.store.owner or  order.confirmed == False:
            return redirect("404-Not-Found")
    except:
        return render(request, 'orders/store_order.html', {'order': order})

def add_order_item(request):
    productId = request.GET.get('productId')
    quantity = request.GET.get('productQuantity')
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        store = product.store.store,
        customer = request.user.customerprofile,
        status = 1 
        )
    order_item = OrderItem.objects.create(
        order = order,
        product = product,
        quantity = int(quantity),
    )
    order.save()
    request.user.customerprofile.orderitemslist.products.add(product)

    return JsonResponse({'data': 'Done'})

def confirm_order(request):
    items_dict = request.GET.get('items_dict')
    items_dict = json.loads(items_dict)
    order_note  = request.GET.get('order_note')

    id = ''
    for id, quantity in items_dict.items():
        item = OrderItem.objects.get(id=id)
        item.quantity = int(quantity)
        item.save()
        
    order_id = OrderItem.objects.get(id=int(id)).order.id
    Order.objects.filter(id=order_id).update(confirmed=True, note=order_note)

    order = OrderItem.objects.get(id=int(id)).order
    print('status:', order.get_status_display())
    channel_layer = get_channel_layer()
    data = {
        'id': order.id,
        'status': order.get_status_display(),
        'customer': order.customer.user.username,
        'city': order.customer.location.city,
        'total': order.total,
    }
    async_to_sync(channel_layer.group_send)(
            f'append-order-{str(order.store.id)}', {
                'type':'append_order',
                'value':json.dumps(data)
            }
        )

    return JsonResponse({'data': 'Done'})

def cancel_order(request):
    order_id = request.GET.get('orderId')
    user = request.GET.get('user')
    if user == 'store':
        Order.objects.filter(id=order_id).update(status=4)
    elif user == 'customer':
        Order.objects.filter(id=order_id).update(status=5)
    order = Order.objects.get(id=order_id)
    customer = order.customer
    for item in order.orders.all():
        product = Product.objects.get(id=item.product.id)
        customer.orderitemslist.products.remove(product)
    return JsonResponse({'data': 'Done'})

def cancel_item(request):
    item_id = request.GET.get('itemId')
    item = OrderItem.objects.get(id=item_id)
    order = item.order
    customer = item.order.customer
    product = Product.objects.get(id=item.product.id)
    customer.orderitemslist.products.remove(product)
    OrderItem.objects.filter(id=item_id).delete()
    if order.orders.all().count() == 0:
        Order.objects.filter(id=order.id).delete()
        return JsonResponse({'data': 'back'})
    return JsonResponse({'data': 'continue'})

def update_store_order(request):
    order_id = request.GET.get('orderId')
    new_status = request.GET.get('newStatus')
    Order.objects.filter(id=order_id).update(status=new_status)
    return JsonResponse({'data': 'Done'})

def store_confirm_order(request):
    order_id = request.GET.get('orderId')
    Order.objects.filter(id=order_id).update(status=2)
    return JsonResponse({'data': 'Done'})

def delivered_order(request):
    order_id = request.GET.get('orderId')
    Order.objects.filter(id=order_id).update(status=3)
    order = Order.objects.get(id=order_id)
    for item in order.orders.all():
        product = Product.objects.get(id=item.product.id)
        product.sales_counter += item.quantity
        print(product.sales_counter)
        product.save()
        print(product.sales_counter)
    return JsonResponse({'data': 'Done'})

def notAvailable(request):
    item_id = request.GET.get('itemId')
    item = OrderItem.objects.get(id=item_id)
    order = item.order
    customer = item.order.customer
    product = Product.objects.get(id=item.product.id)
    # items = product.order_item.all()
    # for order_item in items:
    #     if order_item.order.status == 1:     
    #         OrderItem.objects.filter(id=order_item.id).delete()     
    customer.orderitemslist.products.remove(product)
    Product.objects.filter(id=product.id).update(is_available=False)
    unavailable_items = order.orders.filter(product__is_available=False).count()
    print('unavailable_items', unavailable_items)
    if unavailable_items == order.orders.count():
        Order.objects.filter(id=order.id).update(status=5)
        return JsonResponse({'data': 'reload'})
    else:
        Order.objects.filter(id=order.id).update(status=7)
        return JsonResponse({'data': 'continue'})

def request_reservation_view(request, id):
    workshop_branch = WorkshopBranch.objects.get(id=id)
    if request.method == 'POST':
        form = RequestReservationForm(
            request.POST or None,
            branch_id=id,
            workshop= workshop_branch,
            customer_id= request.user.customerprofile.id,
            initial={
                'customer': request.user.customerprofile,
                'workshop': workshop_branch
                }
            )
        if form.is_valid():
            reservation = form.save()
            for image in request.FILES.getlist('images'):
                ReservationImage.objects.create(reservation=reservation, image=image)
            return HttpResponseRedirect("/")
            # Redirect to a success page or do something else
    else:
        form = RequestReservationForm(
            branch_id=id,
            workshop= workshop_branch,
            customer_id= request.user.customerprofile.id,
           initial={
                'customer': request.user.customerprofile,
                'workshop': workshop_branch
                }
            )

    context = {
        'form': form,
    }
    return render(request, 'orders/request_reservation.html', context)

    workshopId = request.GET.get('workshopId')
    workshop = WorkshopProfile.objects.get(id=workshopId)
    reservaion, created =  WorkshopReservation.objects.get_or_create(
        workshop = workshop,
        customer = request.user.customerprofile,
        status = 1        
        )
    return JsonResponse({'data': 'Done'})

def load_cars(request):
    print('hi')
    brand_id = request.GET.get('brand')
    cars = Car.objects.filter(brand_id=brand_id)
    return render(request, 'orders/ajax/cars_dropdown_list_options.html', {'cars': cars})

def confirm_reservation(request):
    reservation_id = request.GET.get('reservationId')
    time = request.GET.get('time')
    # reservation = WorkshopReservation.objects.get(id=reservation_id)
    WorkshopReservation.objects.filter(id=reservation_id).update(
        status = 2,
        time=time
    )
    # print('status:',reservation.get_status_display())
    # channel_layer = get_channel_layer()
    # data = {
    #     'id': order.id,
    #     'status': order.get_status_display(),
    #     'customer': order.customer.user.username,
    #     'total': order.total,
    # }
    # print(data)
    # async_to_sync(channel_layer.group_send)(
    #         str(order.store.id), {
    #             'type':'append_order',
    #             'value':json.dumps(data)
    #         }
    #     )

    return JsonResponse({'data': 'Done'})

def update_reservation(request):
    reservation_id = request.GET.get('reservationId')
    status = request.GET.get('status')
    WorkshopReservation.objects.filter(id=reservation_id).update(
        status = status,
    )
    return JsonResponse({'data': 'Done'})

def workshop_reservations_list(request, id):
    workshop = WorkshopProfile.objects.get(id=id)
    branches = workshop.branches.all()
    reservations= []
    for branch in branches:
        reservations.extend(branch.workshopreservation_set.all())
    
    WorkshopReservationNotification.objects.filter(is_seen=False)\
    .update(is_seen=True)
    return render(request, 
                'orders/workshop_reservations.html', 
                {'reservations': reservations})

def workshop_reservation_details(request, id):
    reservation = WorkshopReservation.objects.get(id=id)
    
    return render(request, 
                'orders/workshop_reservation_details.html', {'reservation': reservation})

def customer_reservations_list(request):
    reservations = request.user.customerprofile.workshopreservation_set.all()
    CustomerReservationNotification.objects.filter(is_seen=False)\
    .update(is_seen=True)

    return render(request, 
                'orders/customer_reservations.html', 
                {'reservations': reservations})

def customer_reservation_details(request, id):
    reservation = WorkshopReservation.objects.get(id=id)
    rating = WorkshopStarRating.objects.filter(workshop=reservation.workshop.workshop, customer=request.user.customerprofile).values('rating').first()
    # workshop_rating = WorkshopStarRating.objects.filter(workshop=reservation.workshop.workshop).first()
    # average = workshop_rating.calculate_average_rating() if workshop_rating else 0
    context = {
        'reservation': reservation,
        'rating': rating
    }
    return render(request, 
                'orders/customer_reservation_details.html', 
                context)

def customer_services(request, id, service):
    print('service',service)
    if service == 'orders':
        services = Order.objects.filter(customer__id=id)
    elif service == 'reservations':
        services = WorkshopReservation.objects.filter(customer__id=id)
    context =  {'services': services,
                'service_type': service
                
                }
    return render(request, 'orders/customer_services.html', context)

        