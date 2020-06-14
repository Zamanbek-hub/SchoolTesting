from django.urls import path
from . import views
# from .views import *
from django.urls import reverse_lazy

urlpatterns = [
    path('',                views.index,            name = 'index'),
    # path('',                views.check,            name = 'check'),
    path('input',           views.input,            name = 'input'),
    path('test',            views.test,             name = 'test'),
    path('pag',             views.pagination,       name = 'pag'),
    path('pagination_p',    views.pagination_pro,   name = 'pagination_p'),
    path('serial_answers',  views.serial_answers,   name = 'serial_answers'),
    path('create_test',     views.create_test,      name = 'create_test'),
    path('moderator',       views.moderator,         name = 'moderator')
]
