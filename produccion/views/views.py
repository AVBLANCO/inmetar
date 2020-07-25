from django.shortcuts import render
from ..models import OdpCriba, RolloCriba, InventarioCriba
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg


barra_lateral = (
    ("Tablero Criba", "fas fa-list", "tablero_criba"),
    ("Inv. Criba", "fas fa-dolly", "inventario_criba"),
    ("Tablero E.S.", "fas fa-list", "tablero_es"),
    ("Inv. E.S.", "fas fa-dolly", "inventario_es"),
    ("Bitácora Pn.", "fas fa-thumbtack", "bitacora_pn"),
    ("Bitácora Mt.", "fas fa-tools", "bitacora_mtto")    
)


@login_required 
def bitacora_pn(request):
    context = {'sb': barra_lateral}
    return render(request, 'produccion/bitacora_pn.html', context)

@login_required 
def bitacora_mtto(request):
    context = {'sb': barra_lateral}
    return render(request, 'produccion/bitacora_mtto.html', context)

