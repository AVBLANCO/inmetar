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
# from cStringIO import StringIO
import PIL
from reportlab.lib.utils import ImageReader
from io import StringIO

# io_img = StringIO(data)
# pil_img = PIL.Image.open(StringIO(data))

# reportlab_io_img = ImageReader(io_img)
# reportlab_pil_img = ImageReader(pil_img)

class PDFEtiqueta():
    def __init__(self, encabezado, archivo="etiquetas_es.pdf"):
        # self.lista = lista
        self.cliente = encabezado[0]
        self.proyecto = encabezado[1]
        self.archivo = archivo
        self.verde_inmetar = colors.HexColor("#23C32D")
        # self.verde_inmetar = colors.black
        self.colorqr = "green"
        ancho_letter, largo_letter = letter
        self.tamaño = ancho_letter, largo_letter/4
        self.doc = SimpleDocTemplate(
			self.archivo,
			pagesize=self.tamaño,
			rightMargin=5,
			leftMargin=5,
			topMargin=2,
			bottomMargin=2
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
        # cli = "Paisaje Urbano"
        # proy = "Vallarta"
        self.ref = lista[0]
        self.dim = lista[1]
        self.dia = lista[2]
        self.sep = lista[3]
        self.pls = lista[4]
        self.cant = lista[5]
        self.peso = lista[6]
        
        
        texto_qr = \
              "Inmetar SAS - NIT 901.111.798-3\n" \
            + "Cliente: {}\n".format(self.cliente) \
            + "Proyecto: {}\n".format(self.proyecto) \
            + "Referencia: {}\n".format(self.ref) \
            + "Dimensiones: {}\n".format(self.dim) \
            + "Calibre: {}\n".format(self.dia) \
            + "Cantidad: {}\n".format(self.cant) \
            + "cel. 3102709225\n" \
            + "www.inmetar.com\n" 
            
        Iqr = Image(self.__generar_qr(texto_qr))
        Iqr.drawHeight = 1.3*inch*Iqr.drawHeight / Iqr.drawWidth
        Iqr.drawWidth = 1.3*inch
        
        Ilogo = Image('./inmetarvt.png')
        Ilogo.drawHeight = 2.8*inch*Ilogo.drawHeight / Ilogo.drawWidth
        Ilogo.drawWidth = 2.8*inch
        
        if len(self.ref) >= 15:
           self.ref = self.__partir_string(self.ref)
        
        data = [[Ilogo, "|", "CLIENTE", self.cliente, "", ""],
                ["x", "|", "PROYECTO", self.proyecto, "", ""],
                ["x", "|", "REFERENCIA", self.ref, "", Iqr],
                #["x", "|", "", "", "", ""],
                ["x", "|", "DIMENSION (m)", "{:.2f}".format(self.dim[0]), "{:.2f}".format(self.dim[1]), ""], 
                ["x", "|", "PELO (cm)","{:.0f} - {:.0f}".format(self.pls[2], self.pls[3]), "{:.0f} - {:.0f}".format(self.pls[0], self.pls[1]), ""], 
                ["x", "|", "DIÁM. (mm)", "{:.1f}".format(self.dia[0]), "{:.1f}".format(self.dia[1]), ""],
                ["x", "|", "ESPDO. (cm)", self.sep[0], self.sep[1], ""],
                ["x", "|", "CONTIENE", "{} UND.".format(self.cant), "", "{:.0f}kg".format(self.peso)]]
        return data
        
    def __mostrar_lista(self, lista):
        for i in lista:
            print(i)
    
    def __generar_tabla_principal(self, lista):
        data = self.__procesar_datos_info(lista)

        # self.__mostrar_lista(data)
        anc = self.tamaño[0]-36
        
        tam_col = [anc*.46, anc*.08, anc*.14, anc*.07, anc*.07, anc*.18]
        alt = .31*inch
        tam_fil = (len(data))*[alt]
        
        if len(self.ref) <= 10:
            textsize_ref, align_ref = (15, "TOP")
        elif len(self.ref) < 15:
            textsize_ref, align_ref = (12, "MIDDLE")
        else:
            # self.ref = self.__partir_string(self.ref)
            textsize_ref, align_ref = (10, "MIDDLE")
            
         # if len(self.ref)<=10 else (10, "MIDDLE")
        textsize_anchoylargo = 8
        textsize_cliente = 15
        textsize_proyecto = 16
        
        style = TableStyle([
                ('SPAN', (-3,0), (-1,0)),
                ('SPAN', (-3,1), (-1,1)),
                ('SPAN', (-3,2), (-2,2)),
                ('SPAN', (-1,2), (-1,-2)),
                ('SPAN', (-3,-1), (-2,-1)),
                ('SPAN', (0,0), (0,-1)),
                # ('ALIGN',(0,0),(-1,-1),'CENTER'),
                # ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('FONTNAME', (-3, 0), (-1, -1), "Helvetica-Bold"),
                ('FONTSIZE', (-3, 0), (-1, -1), 13),
                ('FONTSIZE', (-3,0), (-1,0), textsize_cliente),
                ('FONTSIZE', (-3,1), (-1,1), textsize_proyecto),
                ('INNERGRID', (-4,0), (-1,-1), 0.75, self.verde_inmetar),
                ('FONTSIZE', (-3,3),(-2,3), textsize_anchoylargo),
                ('FONTSIZE', (-3, -4), (-2, -4), 10),##
                ('FONTSIZE', (-4,-1), (-1,-1), 15),##
                ('FONTSIZE', (-3,2), (-2,2), textsize_ref),##
                ('TEXTCOLOR', (-4,0), (-4,-1), colors.white),
                ('TEXTCOLOR', (-4,-1), (-1,-1), colors.white),
                ('TEXTCOLOR', (-1,0), (-1,-1), colors.white),
                ('BACKGROUND', (-4,0), (-4,-1), self.verde_inmetar),
                ('BACKGROUND', (-4,-1), (-1,-1), self.verde_inmetar),
                ('FONTNAME', (-4, 0), (-4, -1), "Helvetica-Bold"),
                ('FONTSIZE', (-4, 0), (-4, -1), 10),
                ('ALIGN',(-4,0),(-4,-1), 'LEFT'),
                ('BOX', (0,0), (0,-1), 2, self.verde_inmetar),
                ('BOX', (2,0), (-1,-1), 2, self.verde_inmetar),
                ('INNERGRID', (-4,0), (-4,-1), 0.75, colors.white),
                ('INNERGRID', (-4,-1), (-1,-1), 0.75, colors.white),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                
                ('VALIGN', (-3,2), (-2,2),align_ref),
                ('VALIGN', (-3,0), (-1,1), "TOP"), #CLIENTE Y PROYECTO
                ('VALIGN', (-3,-1), (-1,-1), "TOP"), #UND Y KGS
                ])
        
        
        t = Table(data, tam_col, tam_fil)
        t.setStyle(style)
        return t
    
    # def __obtener_info(self):
        # lista = ["Hola", (6,6), (6,6), (15,15), (1,2,3,4), 45]
        # lista = 
        # ref = lista[0]
        # dim = lista[1]
        # dia = lista[2]
        # sep = lista[3]
        # pls = lista[4]
        # cant = lista[5]
        # return lista
        
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
    
    def __partir_string(self, pstri):
        # print("Parto string: {}".format(pstri))
        i = len(pstri)//2
        lstr = list(pstri)
        while i < len(lstr):
            # print("Iteración {}".format(i))
            if lstr[i] == ' ' or lstr[i] == ',' or lstr[i] == 'y':
                lstr[i] = '\n'
                break
            else:
                i += 1
        out = "".join(lstr)
        return out

if __name__ == "__main__":    
    encabezado = ("Pa", "Va")
    et = PDFEtiqueta(encabezado)
    lista = ["Hola", (6,6), (6,6), (15,15), (1,2,3,4), 45]
    et.añadir_etiqueta(lista)
    lista = ["Hola", (6,6), (6.0,6.0), (15,15), (10,2.2,3,60), 45]
    et.añadir_etiqueta(lista)
    lista = ["Hola", (6.00,2.35), (5.0,5.0), (15,15), (1,2,3,4), 45]
    et.añadir_etiqueta(lista)
    et.terminar()
