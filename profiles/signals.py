from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import CustomerProfile, StoreProfile, WorkshopProfile,\
    MeccanicoAdmin
from inboxes.models import Inbox, Contact
from orders.models import OrderItemsList


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        inbox = Inbox.objects.create(owner=instance.username)
        customer = CustomerProfile.objects.create(user=instance, inbox=inbox)
        OrderItemsList.objects.create(customer=customer)
    
    
@receiver(post_save, sender=CustomerProfile)
def post_save_customer_profile(sender, instance, created, **kwargs):
    for Admin in MeccanicoAdmin.objects.all():
        if Admin.admin != instance.user:
            contact = Contact.objects.get_or_create(mainInbx=instance.inbox, contactInbx= Admin.inbox)
    

@receiver(pre_save, sender=StoreProfile)
@receiver(pre_save, sender=WorkshopProfile)
def pre_save_create_store_profile(sender, instance,**kwargs):
    if  instance.inbox == None:
        if sender == StoreProfile:
            inbx_type = 2
            owner = instance.name + " Store"
        elif sender == WorkshopProfile:
            inbx_type = 3
            owner = instance.name + " Workshop"
        inbox = Inbox.objects.create(owner=owner, type=inbx_type)
        instance.inbox = inbox

@receiver(post_save, sender=StoreProfile)
@receiver(post_save, sender=WorkshopProfile)
def post_save_create_store_profile(sender, instance,**kwargs):
    for Admin in MeccanicoAdmin.objects.all():
        if Admin.admin != instance.owner:
            contact = Contact.objects.get_or_create(mainInbx=instance.inbox, contactInbx= Admin.inbox)
            contact = Contact.objects.get_or_create(mainInbx=instance.inbox, contactInbx= Admin.inbox)