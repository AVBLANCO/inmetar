from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import *
from .views import barra_lateral

class EquipoCreateView(LoginRequiredMixin, CreateView):
    model = Equipo
    template_name = 'gestion/formbase.html'
    fields = ('denominacion', 'ancho', 'largo', 'distancias')

    def form_valid(self, form):
        planta_pk = self.kwargs['planta_pk']
        planta = Planta.objects.get(pk=planta_pk)
        form.instance.planta = planta
        return super(EquipoCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        context['titulo'] = "Nuevo Equipo"
        return context

class EquipoUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipo
    template_name = 'gestion/formbase.html'
    fields = ('denominacion', 'ancho', 'largo', 'distancias')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        context['titulo'] = "Editar Equipo"
        return context

class EquipoDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipo
    template_name = 'gestion/delete_confirmation.html'
