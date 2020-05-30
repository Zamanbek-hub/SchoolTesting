from django.urls import path
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('',                views.check,            name = 'check'),
]
