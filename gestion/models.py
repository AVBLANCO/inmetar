from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.template.defaultfilters import date as _date
from django.template.defaultfilters import truncatewords as _truncatewords
from django.urls import reverse

from .models_choices import *


class Cliente(models.Model):
    razon_social = models.CharField(max_length=50)
    sigla = models.CharField(max_length=50, blank=True, default='')
    nit = models.CharField(max_length=50, blank=True, default='')
    direccion = models.CharField(max_length=100, blank=True, default='')
    telefono = models.CharField(max_length=50, blank=True, default='')
    pagina_web = models.CharField(max_length=50, blank=True, default='')
    email_facturacion = models.EmailField(
        max_length=50, verbose_name="Email Facturación", blank=True, default='')
    observaciones_cm = models.CharField(
        max_length=50, verbose_name="Observación comercial", blank=True, default='')
    departamento = models.ForeignKey(
        Departamento, on_delete=models.CASCADE, default=None)

    @property
    def departamento_verbose(self):
        return self.departamento.nombre

    def __str__(self):
        return self.razon_social

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def get_absolute_url(self):
        return reverse('detalle_cliente', kwargs={'pk': self.pk})


class Planta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=1)
    denominacion = models.CharField(max_length=50, blank=True)
    coordenadas = models.CharField(max_length=50, blank=True)
    direccion = models.CharField(max_length=50, blank=True)
    lugar = models.CharField(max_length=50, blank=True)
    observaciones_pn = models.CharField(
        max_length=50, verbose_name="Observación producción", blank=True, default='')

    def __str__(self):
        return self.denominacion + "/" + str(self.cliente)

    class Meta:
        verbose_name = "Planta"
        verbose_name_plural = "Plantas"

    def get_absolute_url(self):
        return reverse('detalle_cliente', kwargs={'pk': self.cliente.pk})


class Equipo(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    denominacion = models.CharField(max_length=20)
    ancho = models.IntegerField(default=0)
    largo = models.IntegerField(default=0)
    distancias = models.CharField(max_length=50, blank=True)
    observacion = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.denominacion + "/" + str(self.planta)

    def get_absolute_url(self):
        return reverse('detalle_cliente', kwargs={'pk': self.planta.cliente.pk})


class MallaCribaGenerica(models.Model):
    TIPOS_ENGANCHE = (
        ('N', 'Normal'),
        ('Z', 'Zeta'),
        ('S', 'Sin enganche'),
        ('I', 'Indefinido'))

    TIPOS_GANCHO = (
        ('U', 'U'),
        ('C', 'C'),
        ('N', 'N'),
        ('S', 'Sin gancho'),
        ('I', 'Indefinido'))
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    ancho = models.IntegerField(default=0)
    largo = models.IntegerField(default=0)
    mallas_por_tendido = models.IntegerField(default=1)
    tipo_gancho = models.CharField(
        max_length=3, choices=TIPOS_GANCHO, default='N')
    tipo_enganche = models.CharField(
        max_length=3, choices=TIPOS_ENGANCHE, default='N')
    observacion = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "{} A:{} L:{} G:{} E:{}".format(self.equipo.planta.denominacion.upper(), self.ancho,
                                               self.largo, self.tipo_gancho, self.tipo_enganche)

    def get_absolute_url(self):
        return reverse('detalle_cliente', kwargs={'pk': self.equipo.planta.cliente.pk})


class Contacto(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    cargo = models.CharField(max_length=50,  verbose_name='Cargo')
    email = models.CharField(max_length=50, verbose_name='E-mail')
    telefono = models.CharField(max_length=50)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, default=1, verbose_name='Empresa')
    planta = models.ForeignKey(
        Planta, on_delete=models.CASCADE, default=1, verbose_name='Planta')

    class Meta:
        verbose_name = "Persona de Contacto"
        verbose_name_plural = "Personas de Contactos"


class PrecioMallaCriba(models.Model):
    TIPOS_MALLA = (
        ('TC', 'Trenzada estándar'),
        ('TR', 'Tr. h. rectangular'),
        ('TG', 'Tr. tipo guitarra'),
        ('A', 'Autolimpiante'),
        ('S', 'Soldada'))

    referencia = models.CharField(max_length=10)
    hueco_p = models.CharField(max_length=10)
    hueco_mm = models.DecimalField(max_digits=5, decimal_places=2)
    precio_z1 = models.IntegerField()
    precio_z2 = models.IntegerField()
    precio_z3 = models.IntegerField()
    precio_z4 = models.IntegerField()
    precio_z5 = models.IntegerField()
    precio_z6 = models.IntegerField()
    precio_z7 = models.IntegerField()
    precio_z8 = models.IntegerField()
    tipo_malla = models.CharField(
        max_length=3, choices=TIPOS_MALLA, default='TC')
    diametro = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return "T:{} H:{} D:{}".format(self. tipo_malla, self.hueco_mm, self.diametro)


class Cotizacion(models.Model):
    FORMAS_PAGO = (
        ('CR', 'Crédito'),
        ('CO', 'Contado'),
        ('AC', 'Acordar'))

    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    contacto = models.CharField(max_length=25, default="")
    observacion = models.TextField(blank=True, default="")
    fecha = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateField(blank=True, null=True, default=None)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    forma_pago = models.CharField(
        max_length=3, choices=FORMAS_PAGO, default='AC')
    dias_entrega = models.PositiveIntegerField(
        validators=[MinValueValidator(8)], default=8)

    def __str__(self):
        return "{}: {}".format(self.fecha, self.planta)

    class Meta:
        verbose_name = "cotización"
        verbose_name_plural = "cotizaciones"

    def obtener_telefono(self):
        return _truncatewords(self.cliente.telefono, 2)

    @property
    def forma_pago_verbose(self):
        return self.forma_pago.label

    @property
    def cliente(self):
        return self.planta.cliente

    def obtener_fecha_larga(self):
        return _date(self.fecha, "F d \d\e Y")

    def get_absolute_url(self):
        return reverse('detalle_cotizacion', kwargs={'cot_id': self.pk})


class ItemMallaCribaHistorico(models.Model):
    TIPOS_GANCHO = (
        ('U', 'U'),
        ('C', 'C'),
        ('N', 'N'))
    TIPOS_MALLA = (
        ('TC', 'Trenzada estándar'),
        ('TR', 'Tr. h. rectangular'),
        ('TG', 'Tr. tipo guitarra'),
        ('A', 'Autolimpiante'),
        ('S', 'Soldada'))
    hueco = models.DecimalField(max_digits=5, decimal_places=2)
    diametro = models.DecimalField(max_digits=5, decimal_places=2)
    planta = models.ForeignKey(Planta, null=True, on_delete=models.CASCADE)
    tipo_malla = models.CharField(
        max_length=3, choices=TIPOS_MALLA, default='')
    tipo_gancho = models.CharField(
        max_length=3, choices=TIPOS_GANCHO, default='N')
    ancho = models.IntegerField(default=0)
    largo = models.IntegerField(default=0)
    cantidad = models.IntegerField(default=0)
    no_odp = models.IntegerField(default=0)
    observacion = models.CharField(default='', max_length=64)
    fecha = models.DateField(null=True, default=None)
    malla_generica = models.ForeignKey(
        MallaCribaGenerica, null=True, on_delete=models.SET_NULL, default=None)

    def __str__(self):
        return "{} ODP{} H{} C{} A{} L{} G{}".format(self.planta, self.no_odp, self.hueco, self.diametro, self.ancho, self.largo, self.tipo_gancho)


class ItemMallaCriba(models.Model):

    MATERIALES = (
        ('1018', 'Acero 1018'),
        ('1045', 'Acero 1045'),
        ('1070', 'Acero 1070'),
    )
    material = models.CharField(
        max_length=6, choices=MATERIALES, default='1045')
    ancho = models.IntegerField(default=0)
    largo = models.IntegerField(default=0)
    cantidad = models.IntegerField(default=0)
    cotizacion = models.ForeignKey(
        Cotizacion, on_delete=models.CASCADE, default=1)
    precio = models.ForeignKey(
        PrecioMallaCriba, on_delete=models.CASCADE, default=1)
    malla_generica = models.ForeignKey(
        MallaCribaGenerica, null=True, on_delete=models.SET_NULL, default=None)

    @property
    def hueco(self):
        return self.precio.hueco_mm

    @property
    def diametro(self):
        return self.precio.diametro

    @property
    def descripcion_verbose(self):
        return "{}".format(self.precio.get_tipo_malla_display())

    @property
    def area_unidad(self):
        area_und = self.ancho*self.largo
        # print("ÁreaUnd: {}".format(area_und))
        return area_und/10000.0

    @property
    def area_total(self):
        return self.area_unidad*self.cantidad

    @property
    def precio_unidad(self):
        return self.area_unidad*self.precio.precio_z1

    @property
    def densidad(self):
        h = float(self.hueco)
        d = float(self.diametro)
        lng = 2 * (1000 / (h + d))
        dens_alambre = ((d/2.0)**2) * (3.141592654 * 0.00786)
        dens_malla = lng * dens_alambre
        return dens_malla

    @property
    def peso_teorico_unidad(self):
        return self.densidad*self.area_unidad

    @property
    def peso_teorico_total(self):
        return self.densidad*self.area_total

    def __str__(self):
        return "H:{} C:{} {}".format(self.precio.hueco_mm, self.precio.diametro, self.descripcion_verbose)

    class Meta:
        verbose_name = "item malla criba"
        verbose_name_plural = "items malla criba"

    def get_absolute_url(self):
        return reverse('detalle_cotizacion', kwargs={'pk': self.cotizacion.pk})
