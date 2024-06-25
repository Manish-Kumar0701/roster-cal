# allocation/urls.py
from django.urls import path
from .views import allocate_seats

urlpatterns = [
    path('', allocate_seats, name='allocate_seats'),
]
