
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
   path('criba', views.TableroCribaView.as_view(), name='tablero_criba'),
   path('criba/odp/<int:pk>', views.OdpCribaDetailView.as_view(), name='detalle_odpcriba'),
   path('criba/inventario', views.InventarioCribaView.as_view(), name='inventario_criba'),

   path('es', views.TableroEsView.as_view(), name='tablero_es'),
   path('es/inventario', views.InventarioEsView.as_view(), name='inventario_es'),


   path('bitacora_pn', views.bitacora_pn, name='bitacora_pn'),
   path('bitacora_mtto', views.bitacora_mtto, name='bitacora_mtto'),
]