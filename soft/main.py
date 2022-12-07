# thu vien gui
import PySimpleGUI as sg
# thu vien lay du lieu serial
import time
import serial
import serial.tools.list_ports
# thu vien chinh sua file excel
from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.styles import colors
from openpyxl.cell import Cell
from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    Reference,
)

sg.theme("DarkAmber")

def xuatfiledothi(data):
    wb = Workbook()
    ws = wb.active

    rows = [
        ["Lần thử" , "△t"]
    ]

    for d in data: 
        rows.append(d)

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

# hien thi tat ca cong serial dang mo tren may tinh
ports = serial.tools.list_ports.comports()
ports = sorted(ports)

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

# chon cong com den esp32
i = int(input("Chọn cổng COM để kết nối đến ESP32: "))
ser = serial.Serial(str(ports[i-1].name), 9600, timeout=0.050)

# du lieu cua bang trong gui
data = []
headings = ["Lan Thu", "△t"]

# tao cua so chuong trinh
layout = [
    [sg.Table(values=data, headings=headings, key="-t-", auto_size_columns=False,  def_col_width=10, num_rows=10, justification="center", )], 
    [sg.Button("Xuất đồ thị .xlsx", key="-dt-")],]
win = sg.Window("Test", layout, resizable=True, finalize=True)

# bien dem so lan thu
testcount = 0

# event loop
while True:
    if (ser.in_waiting != 0):
        sout = ser.readline()
        sout_decoded = str(sout).split(";")
        print(sout_decoded)
        try:
            print(testcount, ". ", sout_decoded[2], "(ms)")
            testcount += 1
            data.append([testcount, int(sout_decoded[2])])
            win["-t-"].update(values=data)
        except:
            continue
    e, v = win.read(timeout=500)
    if e == sg.WIN_CLOSED:
        break
    if e == "-dt-":
        xuatfiledothi(data)
        sg.Popup("Đã xuất dothi.xlsx tại folder chứa script!")

win.close()