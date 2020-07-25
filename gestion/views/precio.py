from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import *
from .views import barra_lateral

class PrecioListView(LoginRequiredMixin, ListView):
  model = PrecioMallaCriba
  template_name = "gestion/listaprecios.html"
  context_object_name = 'lista_precios'
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        context['titulo'] = "Nueva Planta"
        return context
