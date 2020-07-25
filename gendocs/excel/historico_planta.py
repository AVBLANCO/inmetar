import openpyxl
from gendocs.excel import excel_base
from openpyxl.styles import NamedStyle, Font, Border, Side

class ReporteHistoricoPlanta():
    def __fecha_excel(self, fecha):
        out = str(fecha).split('-')
        return "{}/{}/{}".format(out[2], out[1], out[0])
    def __init__(self, archivo, planta):

        campos = ('fecha', 'tipo_malla', 'planta__cliente__razon_social', 'planta__denominacion', 'no_odp', 'hueco', 'diametro', 'ancho', 'largo', 'tipo_gancho', 'cantidad')
        nombres_campos = ('Fecha', 'Tipo', 'Cliente', 'Planta', 'Órden No.', 'Hueco', 'Diámetro', 'Ancho', 'Largo', 'Gancho', 'Cantidad')
        formatos = (self.__fecha_excel, str, str, str, int, float, float, int, int, str, int)
        datos = planta.itemmallacribahistorico_set.values(*campos)
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(nombres_campos)
        for col in ws.iter_cols(min_col=1, max_col=7, max_row=1):
            for cell in col:
                cell.font = Font(bold=True, size=10)
        for i in datos:
            m = [k(i[j]) for j,k in zip(campos, formatos)]
            print(m)
            ws.append(m)
        wb.save(archivo)
