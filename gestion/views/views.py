from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import *
from ..forms import *
from produccion.models import InventarioCriba
from django.views.decorators.csrf import csrf_exempt


barra_lateral = (
    ("Cotizaciones", "fas fa-list", "lista_cotizaciones"),
    ("Clientes", "	fas fa-hard-hat", "lista_clientes"),
    ("Productos", "fas fa-tags", "lista_precios"),
    ("Aprobaciones", "fas fa-clipboard-check", "aprobacion_pn_criba")
)


class IndexTemplateView(TemplateView):
    template_name = "gestion/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sb'] = barra_lateral
        return context


@login_required

def aprobacion_pn_criba(request):
    lista_cotiz = Cotizacion.objects.all()
    context = {'lista_cotiz': lista_cotiz, 'sb': barra_lateral}
    return render(request, "gestion/aprobacion_pn_criba.html", context)


def aprobacion_item_pn_criba(request, item_id):
    inv = InventarioCriba()
    item = ItemMallaCriba.objects.get(pk=item_id)
    diam = float(item.diametro)
    disp = inv.disponible(diam)
    context = {'item': item, 'sb': barra_lateral, 'disp': disp}
    return render(request, "gestion/aprobacion_pn_criba_item.html", context)


class ItemMallaCribaList(ListView):
    model = ItemMallaCribaHistorico
    template_name = 'gestion/listaitemshistoricos.html'
