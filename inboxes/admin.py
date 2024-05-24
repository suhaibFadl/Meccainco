from django.contrib import admin

from .models import Inbox, Message, Contact, MessageNotification


admin.site.register(Inbox)
admin.site.register(Message)
admin.site.register(Contact)
admin.site.register(MessageNotification)