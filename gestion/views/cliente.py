from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import *
from ..forms import *
from produccion.models import InventarioCriba
from django.views.decorators.csrf import csrf_exempt
from .views import barra_lateral

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'gestion/detalle_cliente.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "gestion/listaclientes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = 'gestion/formbase.html'
    fields = ['razon_social', 'sigla', 'nit', 'direccion', 'telefono',
         'pagina_web', 'email_facturacion', 'observaciones_cm', 'departamento']
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = 'gestion/formbase.html'
    fields = ['razon_social', 'sigla', 'nit', 'direccion', 'telefono',
         'pagina_web', 'email_facturacion', 'observaciones_cm', 'departamento']
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context