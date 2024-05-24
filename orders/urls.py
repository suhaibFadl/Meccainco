from django.contrib import admin
from django.urls import path
from .views import order, my_orders,add_order_item, confirm_order,\
    store_orders, store_order, cancel_order, cancel_item,\
    notAvailable, store_confirm_order, delivered_order, \
    workshop_reservations_list, customer_reservations_list,  \
    workshop_reservation_details, customer_reservation_details, \
    request_reservation_view, load_cars, confirm_reservation, \
    update_reservation, customer_services, update_store_order


app_name = 'orders'
urlpatterns = [
    path('my_orders/', my_orders, name='my_orders'),
    path('store_orders/<int:id>', store_orders, name='store_orders'),
    path('order/<int:id>/', order, name='order'),
    path('store_order/<int:id>/', store_order, name='store_order'),
    path('workshop_reservations/<int:id>', workshop_reservations_list,
        name='workshop_reservations'),
    path('workshop-reservation/<int:id>', workshop_reservation_details,
        name='workshop_reservation'),
    path('customer_services/<str:service>/<int:id>', customer_services,
        name='customer_services'),
    path('my_reservations/', customer_reservations_list,
        name='customer_reservations'),
    path('customer-reservation/<int:id>', customer_reservation_details,
        name='customer_reservation'),
    path('request_reservation/<int:id>', request_reservation_view,
        name='request_reservation'),
    path('ajax/confirm_reservation', confirm_reservation,
        name='confirm_reservation'),
    path('ajax/update_reservation', update_reservation,
        name='update_reservation'),
    # path('request_reservation/', request_reservation.as_view(), name='request_reservation'),
    path('ajax/load-cars/', load_cars, name='ajax_load_cars'),
    path('ajax/add_order_item/', add_order_item, name='add_order_item'),
    path('ajax/confirm_order/', confirm_order, name='confirm_order'),
    path('ajax/store_confirm_order/', store_confirm_order, name='store_confirm_order'),
    path('ajax/cancel_order/', cancel_order, name='cancel_order'),
    path('ajax/delivered_order/', delivered_order, name='delivered_order'),
    path('ajax/cancel_item', cancel_item, name='cancel_item'),
    path('ajax/notAvailable', notAvailable, name='notAvailable'),    
    path('update_store_order', update_store_order, name='update_store_order'),    
    # path('ajax/check_order_item', check_order_item, name='check_order_item'),
]