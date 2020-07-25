#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# InmeWeb
# Programó Daniel A. Esteban C. 3002927538

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image
from os import path
from gendocs.reportes.codigosqr import generar_qr_texto

class PDFOrdenPnCriba():
    def __init__(self, archivo, odp):
        self.odp = odp

        self.verde_inmetar = colors.HexColor("#23C32D")   
        self.verde_inmetar_suave = colors.HexColor("#B6FFAD")     
        self.verde_inmetar_titulos = colors.HexColor("#85FF85")     
        self.titulo = "ODP C-{:04d} {}H{:.1f}D{:.1f} A{}L{} x{}".format(self.odp.pk, 
                                        self.odp.item.precio.tipo_malla, 
                                        self.odp.item.hueco, 
                                        self.odp.item.diametro,
                                        self.odp.item.ancho,
                                        self.odp.item.largo,
                                        self.odp.item.cantidad)
        self.anc = 7.5*inch
        elements = []
        elements.append(self.__crear_tabla_membrete())
        elements.append(Spacer(10,10))
        elements.append(self.__crear_tabla_encabezado())
        elements.append(Spacer(10,10))
        elements.append(self.__crear_tabla_contenido())
        elements.append(Spacer(10,10))
        elements.append(self.__crear_tabla_pie())
        elements.append(Spacer(10,10))
        elements.append(self.__crear_tabla_verifmallas())
        doc = SimpleDocTemplate(
			archivo,
			pagesize=letter,
			rightMargin=20,
			leftMargin=20,
			topMargin=25,
			bottomMargin=25,
            title=self.titulo, 
            # author=self.asesor.username
		)
        doc.build(elements)
        return None

    def __crear_tabla_membrete(self):     
    
        I = Image('./static/img/logo.png')

        I.drawHeight = 1.5*inch*I.drawHeight / I.drawWidth
        I.drawWidth = 1.5*inch
        
        data =  [[I, "INMETAR SAS", "CODIGO: FO-PM-06"],
                ["","PROCESO: PRODUCCIÓN DE MALLA CRIBA", "VERSIÓN: 02"],
                ["","ÓRDEN DE PRODUCCIÓN", "ABRIL DE 2020"]]
                    
        style = TableStyle([
                ('SPAN', (0,0), (0,-1)),
                ('FONTSIZE', (1,0), (1,0), 10),
                ('FONTSIZE', (1,1), (1,-1), 10),
                ('FONTSIZE', (2,0), (2,-1), 8),
                ('ALIGN', (0,0), (-1,-1),'CENTER'),
                ('VALIGN', (0,0), (-1,-1),'MIDDLE'),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                ('BOX', (0,0), (-1,-1), 1, colors.black),
                ])
                    
        t = Table(data, [self.anc*.25, self.anc*.55, self.anc*.2], [0.2*inch,0.2*inch,0.2*inch])
        t.setStyle(style)  
    
        return t
        
    def __crear_tabla_encabezado(self):
        col_izqn = ("Cliente", "Planta")
        col_izq = (
            self.odp.cliente.razon_social,
            self.odp.planta.denominacion.upper(),
            
        )
        col_dern = ("Consecutivo", "Fecha")
        try:
            fecha = str(self.odp.t_aprobacion_cliente.date())
        except:
            fecha = "-"
        col_der = (
            "C-{:04d}".format(self.odp.id),
            fecha,
            
        )
        
        enc_table = [["IDENTIFICACIÓN DE LA ORDEN","",""]]
        for i in range(len(col_izqn)):
            enc_table.append((col_izqn[i], col_izq[i], col_dern[i], col_der[i]))
        
        t = Table(enc_table,[0.15*self.anc, 0.5*self.anc, 0.15*self.anc, 0.2*self.anc], [0.2*inch, 0.25*inch, 0.25*inch])
        t.setStyle(TableStyle([
                            ('SPAN', (0,0), (-1,0)),
                            ('FONTNAME', (0,0), (-1, 0), "Helvetica-Bold"),
                            ('BACKGROUND', (0,0), (-1,0), self.verde_inmetar),
                            ('BACKGROUND', (0,1), (0,-1), self.verde_inmetar_titulos),
                            ('BACKGROUND', (2,1), (2,-1), self.verde_inmetar_titulos),
                            ('FONTSIZE', (0,0), (-1,-1), 10),
                            ('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 1, colors.black),
                            ]))
        
        return t
    
    def __crear_tabla_contenido(self):
    
        col_izqn = ("Tipo", "Hueco", "Ancho", "Largueros", "Piñón\nsugerido")
        col_izq = (
            self.odp.item.precio.get_tipo_malla_display().upper(),
            self.odp.item.hueco,
            self.odp.item.ancho,
            self.odp.largueros_cant,
            self.odp.paso,
        )
        col_centin = ("", "Diámetro\nAlambrón", "Largo", "Traviesas", "Densidad")
        col_centi = (
            "",
            self.odp.item.diametro,
            self.odp.item.largo,
            self.odp.traviesas_cant,
            "{:.2f} kg/m2".format(self.odp.item.densidad)
        )

        col_centdn = ("Gancho\nEnganche", "Cantidad", "Superficie\nTotal", 
                        "Peso\nEstimado", "Fecha\nEntrega")
        col_centd = (
            "{} / {}".format(self.odp.item.malla_generica.tipo_gancho, self.odp.item.malla_generica.tipo_enganche),
            "{}".format(self.odp.item.cantidad),
            "{:.1f} m2".format(self.odp.item.area_total),
            "{:.1f} kg".format(self.odp.item.peso_teorico_total),
            "",
        )
        link_qr = "http://sg.inmetar.com/pn/criba/odp{}".format(self.odp.pk)
        I = Image(generar_qr_texto(link_qr))

        I.drawHeight = 1.5*inch*I.drawHeight / I.drawWidth
        I.drawWidth = 1.5*inch

        col_der = (I,"","","","")
        
        
        table = [["DESCRIPCIÓN DEL PRODUCTO", "","","","",""], ]
        for i in range(len(col_izqn)):
            table.append([col_izqn[i], col_izq[i], col_centin[i], 
                col_centi[i], col_centdn[i], col_centd[i], col_der[i]])
        
        t = Table(table,[0.10*self.anc, 0.15*self.anc, 
                        0.10*self.anc, 0.15*self.anc, 
                        0.10*self.anc, 0.15*self.anc, 
                        0.25*self.anc], 
                        [0.2*inch, 0.4*inch, 0.4*inch, 
                        0.4*inch, 0.4*inch, 0.4*inch])

        t.setStyle(TableStyle([
                            ('SPAN', (0,0), (-1,0)),
                            ('SPAN', (1,1), (3,1)),
                            ('SPAN', (-1,1), (-1,-1)),
                            ('FONTSIZE', (0,0), (-1,-1), 10),
                            ('FONTNAME', (0,0), (-1, 0), "Helvetica-Bold"),
                            ('BACKGROUND', (0,0), (-1,0), self.verde_inmetar),
                            ('BACKGROUND', (0,1), (0,-1), self.verde_inmetar_titulos),
                            ('BACKGROUND', (2,2), (2,-1), self.verde_inmetar_titulos),
                            ('BACKGROUND', (4,1), (4,-1), self.verde_inmetar_titulos),
                            ('FONTSIZE', (1, 1), (1, 3), 12),
                            ('FONTSIZE', (3, 2), (3, 3), 12),
                            ('FONTSIZE', (5, 1), (5, 2), 12),
                            ('FONTNAME', (0, 1), (-1, 3), "Helvetica-Bold"),
                            ('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 1, colors.black),
                            ]))
        
        return t
    
    def __crear_tabla_pie(self):
        
        col_izqn = ("Fecha\nTerminación", "Piñón\nUtilizado")
        col_centn = ("Peso\nterminado", "Tipo\ngancho")
        col_dern = ("Encargado\nverificación", "Fecha\nverificación")
        
        table = [["VERIFICACIÓN DE LA ÓRDEN", "","","","",""], ]
        for i in range(len(col_izqn)):
            table.append([col_izqn[i], "", col_centn[i], "", col_dern[i], ""])
        
        t = Table(table,[0.133*self.anc, 0.2*self.anc, 0.133*self.anc, 0.2*self.anc, 0.133*self.anc, 0.2*self.anc], [0.2*inch, 0.4*inch, 0.4*inch])
        t.setStyle(TableStyle([
                            ('SPAN', (0,0), (-1,0)),
                            ('FONTNAME', (0,0), (-1, 0), "Helvetica-Bold"),
                            ('BACKGROUND', (0,0), (-1,0), self.verde_inmetar),
                            ('BACKGROUND', (0,1), (0,-1), self.verde_inmetar_titulos),
                            ('BACKGROUND', (2,1), (2,-1), self.verde_inmetar_titulos),
                            ('BACKGROUND', (4,1), (4,-1), self.verde_inmetar_titulos),
                            ('FONTSIZE', (0,0), (-1,-1), 10),
                            ('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 1, colors.black),
                            ]))
        
        return t

    def __crear_tabla_verifmallas(self):
        cant = self.odp.item.cantidad
        table = [["", "Dimensiones", "", "Hueco", "", "","","","","Diagonal", ""],
                    ["", "Ancho", "Largo", "Transversal", "", "", "Longitudinal", "", "", "A", "B"]]
        for i in range(1, cant+1):
            table.append(["Malla {}".format(i),] + 10*["",])

        print(table)
        anchos = [0.1*self.anc, 0.09*self.anc, 
                    0.09*self.anc, 0.09*self.anc, 0.09*self.anc, 
                    0.09*self.anc, 0.09*self.anc, 0.09*self.anc, 
                    0.09*self.anc, 0.09*self.anc, 0.09*self.anc]

        altos = [0.2*inch, 0.2*inch].extend(cant*[0.2*inch,])

        t = Table(table, anchos, altos)
        t.setStyle(TableStyle([
                            ('SPAN', (0,0), (0,1)),
                            ('SPAN', (1,0), (2,0)),
                            ('SPAN', (3,0), (8,0)),
                            ('SPAN', (9,0), (10,0)),
                            ('SPAN', (3,1), (5,1)),
                            ('SPAN', (6,1), (8,1)),
                            ('FONTSIZE', (0,0), (-1,-1), 10),
                            ('BACKGROUND', (0,2), (0,-1), self.verde_inmetar_titulos),
                            ('BACKGROUND', (1,0), (-1,1), self.verde_inmetar_titulos),
                            ('ALIGN',(0,0),(-1,-1),'CENTER'),
                            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 1, colors.black),
                            ]))
        
        return t


