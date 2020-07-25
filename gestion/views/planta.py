from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from ..models import *
from ..forms import *
from django.urls import reverse_lazy
from produccion.models import InventarioCriba
from django.views.decorators.csrf import csrf_exempt
from .views import barra_lateral

class PlantaCreateView(LoginRequiredMixin, CreateView):
    model = Planta
    template_name = 'gestion/formbase.html'
    fields = ('denominacion', 'coordenadas', 'lugar')
    def form_valid(self, form):
        cliente_pk = self.kwargs['pk']
        cliente = Cliente.objects.get(pk=cliente_pk)
        form.instance.cliente = cliente
        return super(PlantaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        context['titulo'] = "Nueva Planta"
        return context

class PlantaUpdateView(LoginRequiredMixin, UpdateView):
    model = Planta
    template_name = 'gestion/formbase.html'
    fields = ('denominacion', 'coordenadas', 'lugar')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        context['titulo'] = "Editar Planta"
        return context

class PlantaDeleteView(LoginRequiredMixin, DeleteView):
    model = Planta
    template_name = 'gestion/delete_confirmation.html'
    def get_success_url(self):
        cliente = self.object.cliente
        return reverse_lazy('detalle_cliente', kwargs={'pk': cliente.pk})

@login_required
def historico_planta(request, planta_id):
    planta = Planta.objects.get(pk=planta_id)
    context = {'planta': planta, 'sb': barra_lateral}
    return render(request, 'gestion/historico_planta.html', context)

