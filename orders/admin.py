from django.contrib import admin

from .models import Order, OrderItem, OrderItemsList, \
    WorkshopReservation, \
    WorkshopReservationNotification, CustomerReservationNotification,\
    StoreOrderNotification, CustomerOrderNotification, ReservationImage


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemsList)
# admin.site.register(OrderNotification)
admin.site.register(WorkshopReservation)
admin.site.register(ReservationImage)
admin.site.register(WorkshopReservationNotification)
admin.site.register(CustomerReservationNotification)
admin.site.register(StoreOrderNotification)
admin.site.register(CustomerOrderNotification)