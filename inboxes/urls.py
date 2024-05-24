from django.urls import path
from .views import my_inbox, chat


app_name = 'inboxes'
urlpatterns = [
    path('<int:type>', my_inbox, name='my_inbox'),
    path('chat/<int:type>-<int:id>/', chat, name='chat'),
]