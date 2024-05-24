"""Meccanico URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import not_found_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('404/', not_found_404, name='404-Not-Found'),
    # path('', include('parts.urls', namespace='parts')),
    path('', include('products.urls', namespace='products')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('users/', include('users.urls', namespace='users')),
    path('inbox/', include('inboxes.urls', namespace='inboxes')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('stars_rating/', include('stars_rating.urls', namespace='stars_rating')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)