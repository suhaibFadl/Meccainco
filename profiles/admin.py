from django.contrib import admin
from .models import CustomerProfile, StoreProfile, StoreBranch,\
    StoreImage, StoreReview, Location, WorkshopProfile, WorkshopBranch, \
    WorkshopImage, WorkshopReview, MeccanicoAdmin


admin.site.register(CustomerProfile)
admin.site.register(StoreProfile)
admin.site.register(StoreBranch)
admin.site.register(StoreImage)
admin.site.register(StoreReview)
admin.site.register(WorkshopProfile)
admin.site.register(WorkshopBranch)
admin.site.register(WorkshopImage)
admin.site.register(WorkshopReview)
admin.site.register(Location)
admin.site.register(MeccanicoAdmin)

# @admin.register(StoreProfile) 
# class StoreProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'full_name', 'email')

