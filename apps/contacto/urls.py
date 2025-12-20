from django.urls import path
from . import views

app_name = 'apps.contacto'

urlpatterns = [
    path('contacto/', views.ContactoUsuario.as_view(), name='contacto'),
    path('acerca_de/', views.AcercaDeView.as_view(), name='acerca_de'),
]