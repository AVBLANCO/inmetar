"""inmeweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('hello_world', views.hello_world, name='index'),
    # path('cotizacion', views.ejcotizacion, name='ejcotizacion'),
    path('cotizacion<int:cot_id>.pdf', views.pdfcotizacion, name='pdfcotizacion'),
    path('cotizacionmaa<int:cot_id>.pdf', views.pdfcotizacionmaa, name='pdfcotizacionmaa'),
    path('odpcriba<int:odp_id>.pdf', views.pdfordenpncriba, name='pdfodpcriba'),
    path('reportepnplanta<int:planta_id>', views.xlshistoricoplanta, name='reportepnplanta'),
]
