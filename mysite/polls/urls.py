from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

#https://docs.djangoproject.com/en/2.2/intro/tutorial01/