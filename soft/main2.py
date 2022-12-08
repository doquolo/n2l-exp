from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.styles import colors
from openpyxl.cell import Cell
from openpyxl import Workbook
from openpyxl.chart import (
    ScatterChart,
    Reference,
    Series,
)

wb = Workbook()
ws = wb.active

rows = [
    ["Lần thử", "Lực kéo (lt)", "Khối lượng", "Thời gian", "Quãng đường", "Gia tốc", "Lực kéo (tt)"],
    [2, 1, 0.4, 0.64, 0.5],
    [3, 1, 0.5, 0.71, 0.5],
    [1, 1, 0.3, 0.55, 0.5],
    [4, 2, 0.5, 0.5, 0.5],
]

ws.append(rows[0])
for i in range(1, len(rows)):
    rows[i].append(f"=Round((2*E{i+1})/(D{i+1}*D{i+1}), 2)")
    rows[i].append(f"=Round(F{i+1}*C{i+1}, 2)")
    ws.append(rows[i])

for cell in ws["1:1"]:
    cell.fill = PatternFill(start_color='35b1de', end_color='35b1de', fill_type='solid')
    cell.font = Font(bold=True)

for rows in ws.iter_rows(min_row=2, min_col=1, max_col=7, max_row=len(rows)):
    for cell in rows:
        cell.fill = PatternFill(start_color='35de8c', end_color='35de8c', fill_type='solid')

chart = ScatterChart()
chart.title = "Đồ thị F-a"
chart.style = 13
chart.x_axis.title = "Lực kéo F (N)"
chart.y_axis.title = "Gia tốc a (m/s)"
chart.legend = None

xvalues = Reference(ws, min_col=6, min_row=2, max_row=len(rows)-2)
yvalues = Reference(ws, min_col=7, min_row=2, max_row=len(rows)-2)
series = Series(xvalues, yvalues, title="")
chart.series.append(series)

ws.add_chart(chart, "I1")

wb.save("test//dothi.xlsx")