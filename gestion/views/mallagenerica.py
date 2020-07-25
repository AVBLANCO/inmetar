from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import *
from .views import barra_lateral

class MallaCribaGenericaDetailView(LoginRequiredMixin, DetailView):
    model = MallaCribaGenerica


class MallaCribaGenericaUpdateView(LoginRequiredMixin, UpdateView):
    model = MallaCribaGenerica
    template_name = 'gestion/formbase.html'
    fields = ('ancho', 'largo', 'tipo_gancho', 'tipo_enganche')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        context['titulo'] = "Editar Malla Criba Genérica"
        return context

class MallaCribaGenericaDeleteView(LoginRequiredMixin, DeleteView):
    model = MallaCribaGenerica


class MallaCribaGenericaCreateView(LoginRequiredMixin, CreateView):
    model = MallaCribaGenerica
    template_name = 'gestion/formbase.html'
    fields = ('ancho', 'largo', 'tipo_gancho', 'tipo_enganche')

    def form_valid(self, form):
        equipo_pk = self.kwargs['equipo_pk']
        equipo = Equipo.objects.get(pk=equipo_pk)
        form.instance.equipo = equipo
        return super(MallaCribaGenericaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        context['titulo'] = "Nueva Malla Criba Genérica"
        return context