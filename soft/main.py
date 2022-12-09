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
    ScatterChart,
    Reference,
    Series,
)

sg.theme("DarkAmber")

def xuatfiledothi(data):
    wb = Workbook()
    ws = wb.active

    rows = [
        ["Lần thử", "Lực kéo (lt)", "Khối lượng", "Thời gian", "Quãng đường", "Gia tốc", "Lực kéo (tt)"],
    ]

    for d in data: 
        rows.append(d)

    for row in rows:
        ws.append(row)

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

    wb.save("soft//test//dothi.xlsx")

def portselector():
    # hien thi tat ca cong serial dang mo tren may tinh
    ports = serial.tools.list_ports.comports()
    ports = sorted(ports)

    portlist = ""
    for i in range(len(ports)):
        port = ports[i].name
        desc = ports[i].description
        hwid = ports[i].hwid
        portlist += "{}. {}: {} [{}] \n".format(i+1, port, desc, hwid)
        # print("{}: {} [{}]".format(port, desc, hwid))

    # print(portlist)

    layout = [[sg.Text("Chọn cổng COM đến ESP32: ")],[sg.Text(portlist)], [sg.InputText()], [sg.Submit()]]
    win = sg.Window("Chọn COM", layout, finalize=True)
    e, v = win.read()
    win.close()

    # chon cong com den esp32
    # i = int(input("Chọn cổng COM để kết nối đến ESP32: "))
    ser = serial.Serial(str(ports[int(v[0])-1].name), 9600, timeout=0.050)
    return ser

def datain(ser, testcount, data):
    sout = ser.readline()
    sout_decoded = str(sout).split(";")
    print(sout_decoded)
    try:
        print(testcount, ". ", sout_decoded[2], "(ms)")
        testcount += 1
        layout = [
            [sg.Text(f"Nhập dữ liệu còn thiếu của lần đo thứ {testcount}:")],
            [sg.Text(f"Dữ liệu thời gian từ bộ đo: {sout_decoded[2]}(ms)")],
            [sg.Text("Lực kéo (Lý thuyết): "), sg.InputText()],
            [sg.Text("Khối lượng: "), sg.InputText()],
            [sg.Text("Quãng đường: "), sg.InputText()],
            [sg.Submit()]
        ]
        win = sg.Window("Nhập dữ liệu đo", layout, finalize=True)
        e, v = win.read()
        win.close()
        time = float(sout_decoded[2]) / 1000 #ms to s
        acceleration = round(((float(v[2])*2)/(time*time)), 2)
        data.append([testcount, float(v[0]), float(v[1]), time, float(v[2]), acceleration, round((acceleration*float(v[1])),2)])
        print(data)
        return data, testcount
    except Exception as e:
        print("oops ", e)
        return data, testcount

if __name__ == "__main__":
    # init serial port
    ser = portselector()
    print(ser.name)
    # bien dem so lan thu
    testcount = 0

    # du lieu cua bang trong gui
    data = []
    headings = ["Lần thử", "Lực kéo (lt)", "Khối lượng", "△t", "Quãng đường", "Gia tốc", "Lực kéo"]

    # tao cua so chuong trinh
    layout = [
        [sg.Table(values=data, headings=headings, key="-t-", auto_size_columns=False,  def_col_width=10, num_rows=10, justification="center", expand_x=True, expand_y=True, font=("Arial", 15, "bold"))], 
        [sg.Button("Xuất đồ thị .xlsx", key="-dt-", font=("Arial", 15))],]
    win = sg.Window("Test", layout, resizable=True, finalize=True)

    # event loop
    while True:
        if (ser.in_waiting != 0):
            data, testcount = datain(ser, testcount, data)
            print(data)
            win["-t-"].update(values=data)
        e, v = win.read(timeout=500)
        if e == sg.WIN_CLOSED:
            break
        if e == "-dt-":
            xuatfiledothi(data)
            sg.Popup("Đã xuất dothi.xlsx tại folder chứa script!")

    win.close()