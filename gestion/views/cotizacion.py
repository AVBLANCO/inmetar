from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ..models import *
from produccion.models import InventarioCriba, OdpCriba
from django.views.decorators.csrf import csrf_exempt
from .views import barra_lateral
from django.urls import reverse_lazy

class CotizacionListView(LoginRequiredMixin, ListView):
  model = Cotizacion
  template_name = "gestion/listacotiz.html"
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context

class CotizacionCreateView(LoginRequiredMixin, CreateView):
  model = Cotizacion
  fields = ('planta', 'contacto', 'forma_pago',
            'dias_entrega', 'observacion')
  template_name = 'gestion/nueva_cotizacion.html'

  def form_valid(self, form):
      user = self.request.user
      form.instance.autor = user
      return super(CotizacionCreateView, self).form_valid(form)

  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context


class CotizacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Cotizacion
    fields = ('planta', 'contacto', 'forma_pago',
              'dias_entrega', 'observacion')
    template_name = 'gestion/nueva_cotizacion.html'


class CotizacionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'gestion/detalle_cotizacion.html'
    model = Cotizacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context

class ItemMallaCribaCreateView(LoginRequiredMixin, CreateView):
    model = ItemMallaCriba
    template_name = 'gestion/nuevo_item_mallacriba.html'
    fields = ('precio', 'cantidad', 'malla_generica')

    def form_valid(self, form):
        cotizacion_pk = self.kwargs['cotizacion_pk']
        cotizacion = Cotizacion.objects.get(pk=cotizacion_pk)
        form.instance.cotizacion = cotizacion
        return super(ItemMallaCribaCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        context['titulo'] = "Nuevo Ítem Malla Criba"
        return context

class ItemMallaCribaUpdateView(LoginRequiredMixin, UpdateView):
    model = ItemMallaCriba
    fields = ('precio', 'cantidad', 'malla_generica')
    template_name = 'gestion/formbase.html'

class ItemMallaCribaDeleteView(LoginRequiredMixin, DeleteView):
    model = ItemMallaCriba
    template_name = 'gestion/delete_confirmation.html'
    def get_success_url(self):
        cotizacion = self.object.cotizacion
        return reverse_lazy('detalle_cotizacion', kwargs={'pk': cotizacion.pk})

class AprobacionMallaCribaView(LoginRequiredMixin, View):
    template_name = 'gestion/aprobacion_malla_criba.html'

    def get(self, request, *args, **kwargs):
        cotizacion = Cotizacion.objects.get(pk=kwargs['pk'])
        return render(request, self.template_name, {'cotizacion': cotizacion})

    def post(self, request, *args, **kwargs):
        aprobado = request.POST.getlist('aprobado')
        for pk in aprobado:
            item = ItemMallaCriba.objects.get(pk=pk)
            odp = OdpCriba(
                estado = 'AP',
                item = item
            )
            odp.save()
            
        return HttpResponseRedirect(reverse('tablero_criba'))

class GestionAjaxView(View):
    def get(self, request, *args, **kwargs):
        objeto = request.GET.get("objeto")
        if objeto == "cliente":
            f_razon_social = objeto = request.GET.get("razon_social")
            print("Busco {}".format(f_razon_social))
            clientes = Cliente.objects.filter(razon_social__icontains=f_razon_social)
            respuesta = list(clientes.values("razon_social", "nit", "departamento", "pk"))
            print(respuesta)
            return JsonResponse(respuesta, safe=False)
        return JsonResponse({})