from django.urls import path
from . import views

urlpatterns = [
    path('values', views.ValueList.as_view(), name='values'),
]
