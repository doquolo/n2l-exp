from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.styles import colors
from openpyxl.cell import Cell
from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference,
)

wb = Workbook()
ws = wb.active

rows = [
    ["Lần thử" , "△t"]
]

for row in rows:
    ws.append(row)

c1 = LineChart()
c1.title = "Đồ thị"
c1.style = 13
c1.y_axis.title = '△t (ms)'
c1.x_axis.title = 'Lần thử'

data = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=len(rows))
c1.add_data(data, titles_from_data=True)

ws.add_chart(c1, "D1")

ws['A1'].fill = PatternFill(start_color='35b1de', end_color='35b1de', fill_type='solid')
ws['A1'].font = Font(bold=True)
ws['B1'].fill = PatternFill(start_color='35b1de', end_color='35b1de', fill_type='solid')
ws['B1'].font = Font(bold=True)

for rows in ws.iter_rows(min_row=2, min_col=1, max_col=2, max_row=len(rows)):
    for cell in rows:
        cell.fill = PatternFill(start_color='35de8c', end_color='35de8c', fill_type='solid')

wb.save("dothi.xlsx")