from django.shortcuts import render
from ..models import OdpCriba, RolloCriba, InventarioCriba
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from django.views.generic import ListView, TemplateView, DetailView
from .views import barra_lateral


class TableroCribaView(TemplateView):
  template_name = 'produccion/tablero_criba.html'
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['odps'] =  OdpCriba.objects.all()
        context['sb'] = barra_lateral
        return context 

class OdpCribaDetailView(DetailView):
  model = OdpCriba
  template_name = 'produccion/detalle_odpcriba.html'
  context_object_name = 'odp'
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['sb'] = barra_lateral
        return context 

class InventarioCribaView(TemplateView):
  template_name = 'produccion/inventario_criba.html'
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inv = InventarioCriba()
        context['rollos'] = inv.rollos
        context['resumen'] = inv.resumen
        context['sb'] = barra_lateral
        return context 