from django import forms
from .models import Cliente,  Cotizacion, ItemMallaCriba, Planta, Equipo,MallaCribaGenerica


class ClienteForm(forms.ModelForm):
    class Meta():
        model = Cliente
        fields = ('razon_social', 'sigla', 'nit', 'direccion', 'telefono')

class ItemMallaCribaForm(forms.ModelForm):
    class Meta():
        model = ItemMallaCriba
        fields = ('precio', 'cantidad', 'malla_generica')
