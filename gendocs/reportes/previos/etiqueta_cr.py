#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Inmesoft v0.1
# Programó Daniel A. Esteban C. 3002927538

# from datos import DBCotizacion

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image, PageBreak
import qrcode
import PIL
from reportlab.lib.utils import ImageReader
from io import StringIO

class PDFEtiqueta():
    def __init__(self, archivo="etiquetas_cr.pdf"):
        # self.cliente = encabezado[0]
        # self.proyecto = encabezado[1]
        self.archivo = archivo
        self.verde_inmetar = colors.HexColor("#23C32D")
        self.colorqr = "green"
        ancho_letter, largo_letter = letter
        self.tamaño = ancho_letter, largo_letter/6
        self.doc = SimpleDocTemplate(
			self.archivo,
			pagesize=self.tamaño,
			rightMargin=3,
			leftMargin=3,
			topMargin=13,
			bottomMargin=10
		)
        
        self.elem = []
        
        
    def añadir_etiqueta(self, lista):
        self.lista = lista
        t = self.__generar_tabla_principal(lista)
        self.elem.append(t)
        self.elem.append(PageBreak())
        
    def terminar(self):
        self.doc.build(self.elem)
    
    def __procesar_datos_info(self, lista):
    
        [tipo, cli, dest, plan, odp, hue, cal, dim, gan, cant, n] = lista
        if plan is None and dest is None:
            sdest = ""
        elif plan is None:
            sdest = "{}".format(dest)
        elif dest is None:
            sdest = "{}".format(plan)
        else:
            sdest = "{} - {}".format(dest, plan)
        
        texto_qr = \
              "Inmetar SAS - NIT 901.111.798-3\n" \
            + "Cliente: {}\n".format(cli) \
            + "Planta: {}\n".format(plan) \
            + "Ancho:{} Largo:{}\n".format(dim[0],dim[1]) \
            + "HCO:{} CAL:{}\n".format(hue, cal) \
            + "Ítem {} de {}\n".format(n, cant) \
            + "cel. 3102709225\n" \
            + "www.inmetar.com\n" 
            
        Iqr = Image(self.__generar_qr(texto_qr))
        Iqr.drawHeight = 1.25*inch*Iqr.drawHeight / Iqr.drawWidth
        Iqr.drawWidth = 1.25*inch
        
        Ilogo = Image('./inmetarvtcriba.png')
        Ilogo.drawHeight = 4.42*inch*Ilogo.drawHeight / Ilogo.drawWidth
        Ilogo.drawWidth = 4.42*inch

        
        data = [[Ilogo , "DESTINO", sdest, ""        , "", Iqr],
                ["logo", "CLIENTE", cli, ""        , "", "qr"],
                ["logo", "HUECO"  , "{}mm".format(hue) , "CAL.", "{}mm".format(cal), "qr"],
                ["logo", "LARGO"  , "{}m".format(dim[0]), "ANCHO"   , "{}m".format(dim[1]), "qr"],
                ["logo", "", "MALLA {} de {}".format(n, cant), "qr"]]
        return data
        
    def __mostrar_lista(self, lista):
        for i in lista:
            print(i)
    
    def __generar_tabla_principal(self, lista):
        data = self.__procesar_datos_info(lista)
        anc = self.tamaño[0]-36
        tam_col = [anc*.56, anc*.07, anc*.1, anc*.07, anc*.07, anc*.17]
        alt = .26*inch
        tam_fil = (len(data))*[alt]
        textsize_anchoylargo = 8
        textsize_cliente = 15
        textsize_proyecto = 16
        
        style = TableStyle([
                ('SPAN', (0,   0), (0, 4)),
                ('SPAN', (-1,  0), (-1, 4)),
                ('SPAN', (-4,0), (-2,0)), #destino
                ('SPAN', (-4,1), (-2,1)), #cliente
                ('SPAN', (-4,-1), (-2,-1)), #cliente
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),                            
                ('BOX', (1,0), (-1,-1), 1, self.verde_inmetar),
                ('INNERGRID', (1,0), (-1,-1), 1, self.verde_inmetar),
                ('FONTNAME', (1,0), (-1,-1), "Helvetica-Bold"),
                ('FONTSIZE', (1,0), (-1,-1), 8),
                ('BACKGROUND', (1,0), (1,-1), self.verde_inmetar), #relleno verde
                ('TEXTCOLOR', (1,0), (1,-1), colors.white), #lineas blancas
                ('FONTNAME', (1,0), (1,-1), "Helvetica-Bold"),
                ('BACKGROUND', (3,2), (3,3), self.verde_inmetar), #relleno verde
                ('TEXTCOLOR', (3,2), (3,3), colors.white), #lineas blancas
                ('FONTNAME', (3,2), (3,3), "Helvetica-Bold"),
                ('INNERGRID', (1,0), (1,-1), 1, colors.white),
                ('INNERGRID', (3,2), (3,3), 1, colors.white),
                ])
        
        
        t = Table(data, tam_col, tam_fil)
        t.setStyle(style)
        return t
    
        
    def __generar_qr(self, info):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        nombre ="algo.png"
        qr.add_data(info)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.colorqr, back_color="white")
        file = open(nombre, "wb")
        img.save(file)
        return nombre


if __name__ == "__main__":    
    encabezado = ("Pa", "Va")
    et = PDFEtiqueta(encabezado)
    et.añadir_etiqueta(None) 
    et.añadir_etiqueta(None) 
    et.añadir_etiqueta(None) 
    et.añadir_etiqueta(None) 
    et.añadir_etiqueta(None) 

    et.añadir_etiqueta(None) 
    et.terminar()
