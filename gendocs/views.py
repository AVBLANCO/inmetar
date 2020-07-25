from django.shortcuts import render

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .reportes import PDFCotizacion, PDFOrdenPnCriba
from .excel import ReporteHistoricoPlanta
from gestion.models import Cotizacion, ItemMallaCriba, Planta
from produccion.models import OdpCriba

def hello_world(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, "Hello world.")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

def pdfcotizacion(request, cot_id):
    buffer = io.BytesIO()
    cotizacion = Cotizacion.objects.get(pk=cot_id)
    marca = {}
    marca.update(nit = '901.111.798-3')
    marca.update(cuenta = 'Cta. Corriente 834-000112-99\nBancolombia')
    marca.update(razon_social = 'INMETAR SAS')
    marca.update(nota = 'Régimen ZESE. Favor no aplicar\nretención en la fuente.')
    cot = PDFCotizacion(buffer, cotizacion, marca)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=cot.titulo+".pdf")

def pdfcotizacionmaa(request, cot_id):
    buffer = io.BytesIO()
    cotizacion = Cotizacion.objects.get(pk=cot_id)
    marca = {}
    marca.update(nit = '1.090.451.240')
    marca.update(cuenta = 'Cta. Corriente 834-380052-08\nBancolombia')
    marca.update(razon_social = 'MARÍA ANGÉLICA ARÉVALO A.')
    marca.update(nota = '')
    cot = PDFCotizacion(buffer, cotizacion, marca)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=cot.titulo+".pdf")


def pdfordenpncriba(request, odp_id):
    buffer = io.BytesIO()
    odp = OdpCriba.objects.get(pk=odp_id)
    podp = PDFOrdenPnCriba(buffer, odp)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=podp.titulo+".pdf")

def xlshistoricoplanta(request, planta_id):
    buffer = io.BytesIO()
    planta = Planta.objects.get(pk=planta_id)
    
    rep = ReporteHistoricoPlanta(buffer, planta)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename="algo.xlsx")