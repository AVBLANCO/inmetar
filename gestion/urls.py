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
from django.urls import path, include
# from gendocs import views

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path('ajax/', views.GestionAjaxView.as_view(), name='gestion_ajax'),
    path('cliente/', views.ClienteListView.as_view(), name='lista_clientes'),   
    path('cliente/<int:pk>/', views.ClienteDetailView.as_view(), name='detalle_cliente'),
    path('cliente/nuevo', views.ClienteCreateView.as_view(), name='nuevo_cliente'),
    path('cliente/editar/<int:pk>', views.ClienteUpdateView.as_view(), name='editar_cliente'),
    
    path('litemshis', views.ItemMallaCribaList.as_view()),
    path('aprpn_criba', views.aprobacion_pn_criba, name='aprobacion_pn_criba'),
    path('aprpn_criba/<int:item_id>', views.aprobacion_item_pn_criba, name='aprobacion_pn_criba_item'),
    

    path('precio/', views.PrecioListView.as_view(), name='lista_precios'),
    path('cotizacion/', views.CotizacionListView.as_view(), name='lista_cotizaciones'),
    path('cotizacion/<int:pk>', views.CotizacionDetailView.as_view(), name='detalle_cotizacion'),
    path('cotizacion/<int:pk>/aprobacion', views.AprobacionMallaCribaView.as_view(), name='aprobacion_malla_criba'),
    path('cotizacion/nueva', views.CotizacionCreateView.as_view(), name='nueva_cotizacion'),
    path('cotizacion/editar/<int:pk>', views.CotizacionUpdateView.as_view(), name='editar_cotizacion'),
    path('cotizacion/<int:cotizacion_pk>/nitem', views.ItemMallaCribaCreateView.as_view(), name='nuevo_item'),
    path('cotizacion/item/borrar/<int:pk>', views.ItemMallaCribaDeleteView.as_view(), name='borrar_item'),
    path('cotizacion/item/editar/<int:pk>', views.ItemMallaCribaUpdateView.as_view(), name='editar_item'),

    path('planta/nueva/<int:pk>/', views.PlantaCreateView.as_view(), name='nueva_planta'),
    path('planta/editar/<int:pk>/', views.PlantaUpdateView.as_view(), name='editar_planta'),
    path('planta/borrar/<int:pk>/', views.PlantaDeleteView.as_view(), name='borrar_planta'),

    path('equipo/nuevo/<int:planta_pk>/', views.EquipoCreateView.as_view(), name='nuevo_equipo'),
    path('equipo/editar/<int:pk>/', views.EquipoUpdateView.as_view(), name='editar_equipo'),
    path('equipo/borrar/<int:pk>/', views.EquipoDeleteView.as_view(), name='borrar_equipo'),
    
    path('mallagenerica/nueva/<int:equipo_pk>/', views.MallaCribaGenericaCreateView.as_view(), name='nueva_malla_criba_generica'),
    path('mallagenerica/editar/<int:pk>/', views.MallaCribaGenericaUpdateView.as_view(), name='editar_malla_criba_generica'),
    path('mallagenerica/borrar/<int:pk>/', views.MallaCribaGenericaDeleteView.as_view(), name='borrar_malla_criba_generica'),

    path('gd/', include('gendocs.urls')),
    path('historico_planta/<int:planta_id>/', views.historico_planta, name='historico_planta'),
]
