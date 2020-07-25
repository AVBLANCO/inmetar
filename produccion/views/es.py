from django.shortcuts import render
from ..models import OdpCriba, RolloCriba, InventarioCriba
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from django.views.generic import ListView, TemplateView, DetailView
from .views import barra_lateral

class TableroEsView(TemplateView):
  template_name = 'produccion/tablero_es.html'
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context 

class InventarioEsView(TemplateView):
  template_name = 'produccion/inventario_es.html'
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context 