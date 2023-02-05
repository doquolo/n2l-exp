# thu vien chinh sua file excel
from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.styles import colors
from openpyxl.cell import Cell
from openpyxl import Workbook
from openpyxl.chart import (
    ScatterChart,
    Reference,
    Series,
)

path = r"C:\Users\doquo\Documents\PlatformIO\Projects\newton2ndlaw-experiment\test"

def export_to_excel(path, name, headers, data, fig1_headers, fig1_data, fig2_headers, fig2_data):

    # create a workbook
    wb = Workbook()
    ws = wb.active

    # main data
    rows = []
    rows.append(headers)
    for d in data: rows.append(d)

    # data for creating fig1
    r1 = []
    r1.append(fig1_headers)
    for d in fig1_data: r1.append(d)

    # data for creating fig2
    r2 = []
    r2.append(fig2_headers)
    for d in fig2_data: r2.append(d)

    
    for r in rows: ws.append(r)
    for r in r1: ws.append(r)
    for r in r2: ws.append(r)

    for r in ws.iter_rows(min_row=4, max_row=9, min_col=1, max_col=2):
        for cell in r:
            print(cell.value)

    wb.save(path+"\\"+name+'.xlsx')


export_to_excel(path, "test", [1, 1, 1, 1], [[1, 2, 3, 4], [5, 6, 7, 8]], [1, 1], [[1, 2], [3, 4]], [1, 1], [[1, 2], [3, 4]])
