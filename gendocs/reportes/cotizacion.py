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


class PDFCotizacion():
    def __init__(self, archivo, cotizacion, marca):
        self.verde_inmetar = colors.HexColor("#23C32D")        
        self.cotizacion = cotizacion
        self.items = self.cotizacion.itemmallacriba_set.all()
        self.asesor = self.cotizacion.autor
        self.cotno = "{}-{:04d}".format(self.asesor.perfil.prefijo , self.cotizacion.id)
        self.marca = marca
        self.anc = 7*inch
        elements = []
        elements.append(self.__crear_tabla_membrete())
        elements.append(Spacer(20,20))
        elements.append(self.__crear_tabla_encabezado())
        elements.append(Spacer(20,20))
        elements.append(self.__crear_tabla_contenido())
        elements.append(Spacer(20,20))
        elements.append(self.__crear_tabla_pie())
        self.titulo = "COT {} {}".format(self.cotno, self.cotizacion.cliente)
        doc = SimpleDocTemplate(archivo, pagesize=letter, title=self.titulo, author=self.asesor.username)
        doc.build(elements)
        
        return None

    def __crear_tabla_membrete(self):     
    
        I = Image('./static/img/inmetarv.png')

        I.drawHeight = 2.5*inch*I.drawHeight / I.drawWidth
        I.drawWidth = 2.5*inch
        somos = "Somos Fabricantes de mallas cribas\ntrenzadas, autolimpiantes y soldadas.\nRodillos, Bandas, laminas perforadas,\nprensamallas y caucho soporte en 'U'"
        
        data =  [["",I, "", "COTIZACIÓN No.", self.cotno],
                    ["","", "","{}\nNIT {} Régimen Común".format(self.marca['razon_social'], self.marca['nit']), ""],
                    ["","", "", somos, ""]]
                    
        style = TableStyle([
                ('SPAN', (1,0), (1,2)),
                ('FONTSIZE', (1,0), (1,2), 18),
                ('TEXTCOLOR', (1,0), (1,2), colors.white),
                ('SPAN', (3,1), (4,1)),
                ('FONTSIZE', (3,1), (4,1), 10),
                ('SPAN', (3,2), (4,2)),
                ('FONTSIZE', (3,2), (4,2), 8),
                ('BACKGROUND', (3,0), (4,0), self.verde_inmetar),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('INNERGRID', (3,0), (-1,-1), 0.5, colors.black),
                ('BOX', (3,0), (-1,-1), 1, colors.black),
                ])
                    
        t = Table(data, [self.anc*.02, self.anc*.4, self.anc*.18, self.anc*0.25, self.anc*.15], [0.2*inch,0.4*inch,0.8*inch])
        t.setStyle(style)  
        return t
        
    def __crear_tabla_encabezado(self):
        col_izqn = ("Fecha", "Cliente", "Dirección", "Atención", "Telefono")
        col_izq = (self.cotizacion.obtener_fecha_larga(), 
                    self.cotizacion.cliente.razon_social,
                    self.cotizacion.cliente.direccion,
                    "",
                    self.cotizacion.obtener_telefono())
        col_dern = ("NIT", "Ciudad", "Teléfono", "Cargo", "E-mail")
        col_der =  (self.cotizacion.cliente.nit,
                    "",
                    self.cotizacion.cliente.telefono,
                    "",
                    "")
        
        enc_table = []
        for i in range(len(col_izq)):
            enc_table.append([col_izqn[i], col_izq[i], col_dern[i], col_der[i]])
        
        t = Table(enc_table,[0.1*self.anc, 0.5*self.anc, 0.1*self.anc, 0.3*self.anc], 5*[0.2*inch])
        t.setStyle(TableStyle([
                            ('ALIGN',(0,0),(-1,-1),'LEFT'),
                            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 1, colors.black),
                            ]))
        
        return t
    
    def __crear_tabla_contenido(self):
    
        cols_elems = ["ITEM", "DESCR", "HUECO", "DIAM\n(mm)", "ANCHO\n(cm)", "LARGO\n(cm)", "CANT", "VR. UNIT", "VR. TOTAL"]
        cont_table = []
        cont_table = [["MALLAS"] + 8*[""]] #Encabezado de la tabla "MALLAS"
        cont_table.append(cols_elems)
        
        cant_items = len(self.items)
        cant_relleno = 12-cant_items
        precio_cotizacion = 0
        for ni, item in enumerate(self.items):
            
            print("{} {}".format(item.precio.hueco_mm, item.precio.diametro))
            ancho = item.ancho
            largo = item.largo
            cant = item.cantidad
            area_und = item.area_unidad
            area_tot = item.area_total
            precio_item = item.precio_unidad*cant
            precio_cotizacion += precio_item
            fila = [str(ni+1), 
                item.descripcion_verbose, 
                item.precio.hueco_mm, 
                item.precio.diametro, 
                ancho, 
                largo, 
                cant, 
                "$ {:,.0f}".format(item.precio_unidad),
                "$ {:,.0f}".format(precio_item),
                ]
            cont_table.append(fila)
        
        for i in range(cant_relleno):
            cont_table.append(9*[""])
        
        cont_table[-1][-2] = "TOTAL"
        cont_table[-1][-1] = "$ {:,.0f}".format(precio_cotizacion*1.19)
        cont_table[-2][-2] = "IVA 19%"
        cont_table[-2][-1] = "$ {:,.0f}".format(precio_cotizacion*0.19)
        cont_table[-3][-2] = "SUBTOTAL"
        cont_table[-3][-1] = "$ {:,.0f}".format(precio_cotizacion)
        cont_table[-3][0] = "OBSERVACIONES: {}".format(self.cotizacion.observacion)
        
        style = TableStyle([
                ('SPAN', (0,0), (-1, 0)),
                ('FONTNAME', (0,0), (-1, 1), "Helvetica-Bold"),
                ('SPAN', (0,-3), (-3, -1)),
                ('BACKGROUND', (0,0), (-1,1), self.verde_inmetar),
                ('FONTSIZE', (0,0), (-1,-1), 9),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('INNERGRID', (0,0), (-1,-1), 0.75, colors.black),
                ('BOX', (0,0), (-1,-1), 1, colors.black),
                ])
        
        t = Table(cont_table,10*[.05*self.anc, 0.25*self.anc, .08*self.anc, .08*self.anc, .08*self.anc, 
                .08*self.anc, .06*self.anc, .15*self.anc, .17*self.anc], [.2*inch, .5*inch] + 12*[.2*inch])
        t.setStyle(style)   
        return t
    
    def __crear_tabla_pie(self):
        
        convenciones = "T: Trenzada\n"+"S: Soldada\n"+"A: Autolimpiante\n"+"G: Gancho\n"+"EG: Enganche"
        autorizacion = "El presente documento firmado y sellado por su personal de compras es\n válido y equivalente a una orden de compra."
        condiciones = "Transporte: Inmetar\n" +\
                    "Forma de pago: {}\n".format(self.cotizacion.get_forma_pago_display()) +\
                    "Tiempo entrega: {} días háb.\n".format(self.cotizacion.dias_entrega) +\
                    "Validez oferta: 20 días háb."
        pago = "Favor consignar a nombre de \n{}\n{}\n{}".format(self.marca['razon_social'], self.marca['cuenta'], self.marca['nota'])
        data = [["CONVENCIONES", "CONDICIONES COMPRA", "PAGO"],
        [convenciones,condiciones,pago],
        ["ASESOR COMERCIAL", "AUTORIZACIÓN", ""],
        ["{}\n{}\n{}".format(self.asesor.get_full_name(), self.asesor.email, self.asesor.perfil.celular),autorizacion,""]]
        
        style = TableStyle([
                ('BACKGROUND', (0,0), (-1,0), self.verde_inmetar),
                ('BACKGROUND', (0,2), (-1,2), self.verde_inmetar),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('SPAN', (1,2), (2,2)),
                ('SPAN', (1,3), (2,3)),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX', (0,0), (0,1), 1, colors.black),
                ('BOX', (1,0), (1,1), 1, colors.black),
                ('BOX', (2,0), (2,1), 1, colors.black),
                ('BOX', (0,2), (0,3), 1, colors.black),
                ('BOX', (1,2), (1,3), 1, colors.black),
                ('BOX', (0,0), (-1,-1), 1, colors.black),
                ])
        
        t = Table(data,[self.anc*.333, self.anc*.333, self.anc*.333], [.2*inch, 1.1*inch, 0.2*inch, 0.6*inch])
        t.setStyle(style)    
        return t              
