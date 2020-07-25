from django.db import models
from gestion.models import ItemMallaCriba
from django.db.models import Sum, Count, Avg

class OdpCriba(models.Model):
    ESTADOS_MCR = (
        ('IN', 'Inicial'),
        ('AC', 'Aprobado Cliente'),
        ('AP', 'Aprobado Producción'),
        ('RN', 'Rizando'),
        ('TN', 'Tejiendo'),
        ('TR', 'Terminación'),
        ('FP', 'Falta pintura'),
        ('BO', 'Bodega'),
        ('DE', 'Despachado'),
        ('EE', 'Entregado'))

    estado = models.CharField(max_length=2, choices=ESTADOS_MCR, default='IN')  
    fecha_aprobacion_produccion = models.DateField(auto_now_add=True)
    numero_odp = models.IntegerField(default=None, null=True)
    item = models.OneToOneField(
        ItemMallaCriba,
        null = True,
        on_delete=models.SET_NULL
    )
    
    @property
    def paso(self):
        return float(self.item.hueco + self.item.diametro)

    @property
    def cliente(self):
        return self.item.cotizacion.cliente
        
    @property
    def planta(self):
        return self.item.cotizacion.planta
    
    @property
    def largueros_long(self):
        return self.item.ancho*self.item.cantidad+50
    
    @property
    def traviesas_long(self):
        return self.item.ancho+10
    
    @property
    def largueros_cant(self):
        return round(self.item.ancho/(self.paso/10.0))

    @property
    def traviesas_cant(self):
        return round(self.item.largo/(self.paso/10.0))

    def __str__(self):
        return "ODP No. {} {}".format(self.pk, self.item.descripcion_verbose)

class RolloCriba(models.Model):

    MATERIALES = (
        ('1018', 'Acero 1018'),
        ('1045', 'Acero 1045'),
        ('1070', 'Acero 1070'),
    )   
    peso_inicial = models.IntegerField()
    peso_actual = models.IntegerField()
    diametro = models.DecimalField(max_digits=4, decimal_places=2)
    identificador = models.CharField(max_length=10)
    material = models.CharField(max_length=10, choices=MATERIALES)
    odp = models.ManyToManyField(OdpCriba, blank=True)
    fecha_recibo = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-material']

    def __str__(self):
        return "{} D:{} Id:{} Peso:{} Fecha:{}".format(self.material, self.diametro, self.identificador, self.peso_actual, self.fecha_recibo)

class InventarioCriba():
    def __init__(self):
        self.rollos = RolloCriba.objects.all()
        self.lista_materiales = self.rollos.values_list("material", flat=True).distinct()
        self.resumen = self.actualizar_resumen()
    
    def actualizar_resumen(self):
        resumen = {}
        for mat in self.lista_materiales:
            rollos_mat = self.rollos.filter(material__exact=mat)
            diametros = rollos_mat.values_list("diametro", flat=True).distinct()
            m = {}
            for diam in diametros:
                aggr = rollos_mat.filter(diametro__exact=diam).aggregate(suma=Sum('peso_actual'), count=Count('identificador'))
                par = {str(diam): aggr}
                m.update(par)
            resumen.update({mat: m})
        return resumen
    
    def disponible(self, diametro, material=None):
        disp = {}
        rdisp = self.rollos.filter(diametro__gt=diametro*0.9, diametro__lt=diametro*1.1)
        if material == None:
            for mat in self.lista_materiales:
                rdisp_mat = rdisp.filter(material__exact=mat)
                par = {mat: rdisp_mat}
                disp.update(par)
        else:
            rdisp_mat = rdisp.filter(material__exact=material)
            par = {material: rdisp_mat}
            disp.update(par)
        return disp
        
