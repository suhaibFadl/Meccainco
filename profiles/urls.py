from django.contrib import admin
from django.urls import path
from .views import my_profile,stores_profiles_list, \
    store_profile_details, add_workshop_branch,update_branch, \
    add_user_location, ajax_add_user_location,add_location, \
    create_location, update_user_location, ajax_update_user_location,\
    update_location, confirm_update_location, direction, \
    workshops_profiles_list, workshop_profile_details, \
    adminstration, ajax_activation, ajax_delete, add_store_branch,\
    business_selection, add_store_profile, add_workshop_profile,\
    update_store_profile, update_workshop_profile, update_customer_profile

app_name = 'profiles'
urlpatterns = [
    path('my_profile/', my_profile, name='my_profile'),
    path('stores/', stores_profiles_list, name='stores_profiles_list'),
    path('workshops/', workshops_profiles_list, name='workshops_profiles_list'),
    path('stores/<str:store_profile>', store_profile_details, name='store_profile_details'),
    path('workshops/<str:workshop_profile>', workshop_profile_details, name='workshop_profile_details'),
    path('add_workshop_branch/<str:id>', add_workshop_branch, name='add_workshop_branch'),
    path('add_store_branch/<str:id>', add_store_branch, name='add_store_branch'),
    path('update_branch/<str:type>/<str:id>', update_branch, name='update_branch'),
    path('locations/add_location/<str:type>/<int:id>', add_location, name='add_location'),
    path('locations/ajax_add_location/', create_location, name='create_location'),
    path('locations/add_user_location/<int:id>', add_user_location, name='add_user_location'),
    path('locations/ajax_add_user_location/', ajax_add_user_location, name='ajax_add_user_location'),
    path('locations/update_user_location/<int:id>', update_user_location, name='update_user_location'),
    path('locations/ajax_update_user_location/', ajax_update_user_location, name='ajax_update_user_location'),
    path('locations/update_location/<int:id>', update_location, name='update_location'),
    path('locations/ajax_update_location/', confirm_update_location, name='confirm_update_location'),
    path('locations/direction/<int:id>', direction, name='direction'),
    path('adminstration/', adminstration, name='adminstration'),
    path('ajax-activation/', ajax_activation, name='ajax-activation'),
    path('ajax-delete/', ajax_delete, name='ajax-delete'),
    path('make-a-business/', business_selection, name='business_selection'),
     path('add_store_profile/', add_store_profile, name='add_store_profile'),
     path('update_store_profile/', update_store_profile, name='update_store_profile'),
     path('add_workshop_profile/', add_workshop_profile, name='add_workshop_profile'),
     path('update_workshop_profile/', update_workshop_profile, name='update_workshop_profile'),
     path('update_customer_profile/', update_customer_profile, name='update_customer_profile'),
]