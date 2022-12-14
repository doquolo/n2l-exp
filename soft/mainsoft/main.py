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
# thu vien hinh anh
from PIL import Image, ImageTk
# thu vien he thong 
import os
import datetime
import base64
# thu vien ve do thi
import numpy as np
import matplotlib.pyplot as plt
# This is to include a matplotlib figure in a Tkinter canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Embedding the Matplotlib toolbar into your application
def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

# xuat do thi excel
def xuatfiledothi(data, dir):
    wb = Workbook()
    ws = wb.active

    rows = [
    ]
    rows.append(headings)
    for d in data: 
        rows.append(d)

    for row in rows:
        ws.append(row)

    rowcount = len(rows)

    for cell in ws["1:1"]:
        cell.fill = PatternFill(start_color='35b1de', end_color='35b1de', fill_type='solid')
        cell.font = Font(bold=True)

    for rows in ws.iter_rows(min_row=2, min_col=1, max_col=6, max_row=len(rows)):
        for cell in rows:
            cell.fill = PatternFill(start_color='35de8c', end_color='35de8c', fill_type='solid')

    chart = ScatterChart()
    chart.title = "????? th??? F-a"
    chart.style = 13
    chart.x_axis.title = "L???c k??o F (N)"
    chart.y_axis.title = "Gia t???c a (m/s)"
    chart.legend = None

    xvalues = Reference(ws, min_col=6, min_row=2, max_row=rowcount)
    yvalues = Reference(ws, min_col=2, min_row=2, max_row=rowcount)
    series = Series(xvalues, yvalues, title="")
    chart.series.append(series)

    ws.add_chart(chart, "I1")

    wb.save(dir)

# trinh chon cong com
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

    layout = [
        [sg.Text("Ch???n c???ng COM ?????n ESP32: ", background_color='#eeeeee', text_color='#000')],
        [sg.Text(portlist.strip(), background_color='#eeeeee', text_color='#000')], 
        [sg.InputText(background_color='#fff', text_color='#000', border_width=0)], 
        [sg.Submit(button_text="K???t n???i", button_color=('#fff', '#000'))]
    ]
    win = sg.Window("Ch???n c???ng COM", layout, finalize=True, background_color='#eeeeee', font=("Arial", 10))
    e, v = win.read()
    win.close()

    # chon cong com den esp32
    # i = int(input("Ch???n c???ng COM ????? k???t n???i ?????n ESP32: "))
    ser = serial.Serial(str(ports[int(v[0])-1].name), 9600, timeout=0.050)
    return ser, str(ports[int(v[0])-1].description)

# ham su li du lieu vao tu thiet bi do
def datain(ser, testcount, data, x, y):
    sout = ser.readline()
    sout_decoded = str(sout).split(";")
    print(sout_decoded)
    try:
        print(testcount, ". ", sout_decoded[2], "(ms)")
        testcount += 1
        while True:
            # t???o input box tr???ng -> ?????t key -> update n???i dung theo key
            # d??ng h??m ngo??i ????? parse c??ng th???c
            layout = [
                [sg.Text(f"Nh???p d??? li???u c??n thi???u c???a l???n ??o th??? {testcount}:",  background_color='#eeeeee', text_color='#000')],
                [sg.Text(f"D??? li???u th???i gian t??? b??? ??o: {sout_decoded[2]}(ms)",  background_color='#eeeeee', text_color='#000')],
                [sg.Text("L???c k??o (L?? thuy???t): ",  background_color='#eeeeee', text_color='#000'), sg.InputText( background_color='#fff', text_color='#000', border_width=0)],
                [sg.Text("Kh???i l?????ng:             ",  background_color='#eeeeee', text_color='#000'), sg.InputText( background_color='#fff', text_color='#000', border_width=0)],
                [sg.Text("Qu??ng ???????ng:         ",  background_color='#eeeeee', text_color='#000'), sg.InputText( background_color='#fff', text_color='#000', border_width=0)],
                [sg.Submit(button_text="Ho??n t???t",  button_color=('#fff', '#000'))]
            ]
            win = sg.Window("Nh???p d??? li???u ??o", layout, finalize=True, background_color='#eeeeee', font=('Arial', 14))
            e, v = win.read()
            win.close()
            if (v[0] != "" and v[1] != "" and v[2] != ""): break
            else: sg.Popup("C??c ?? d??? li???u kh??ng ???????c ????? tr???ng!", title="Ch?? ??", background_color='#eeeeee', text_color='#000', button_color=('#fff', '#000'))
        time = float(sout_decoded[2]) / 1000 #ms to s
        acceleration = round(((float(v[2])*2)/(time*time)), 2)
        data.append([testcount, float(v[0]), float(v[1]), time, float(v[2]), acceleration])
        print(data)
        # cap nhat du lieu tren do thi
        x.append(float(v[0]))
        y.append(acceleration)
        hl.set_ydata(y)
        hl.set_xdata(x)
        plt.xticks(np.arange(min(x), max(x)+1, 1.0))
        plt.yticks(np.arange(min(y), max(y)+1, 1.0))
        plt.draw()
        return data, testcount
    except Exception as e:
        print("oops ", e)
        sg.Popup(e, title="L???i", background_color='#eeeeee', text_color='#000', button_color=('#fff', '#000'))
        testcount =  (testcount - 1) if testcount >= 2 else testcount
        return data, testcount

if __name__ == "__main__":
    exp_temp = {
        "name": "?????nh lu???t 2 newton",
        "desc": '''Ti???n h??nh:
B?????c 1: L???c k??o F c?? ????? l???n t??ng d???n 1 N, 2 N v?? 3 N (b???ng c??ch m??c th??m c??c qu??? n???ng v??o ?????u d??y v???t qua r??ng r???c). 
B?????c 2: Ghi v??o B???ng 15.1 ????? l???n l???c k??o F v?? t???ng kh???i l?????ng c???a h??? (g???m xe tr?????t v?? c??c qu??? n???ng ?????t v??o xe), ???ng v???i m???i l???n th?? nghi???m.
B?????c 3: Do th???i gian chuy???n ?????ng c???a xe; ?????ng h??? b???t ?????u ?????m t??? l??c t??m ch??n s??ng ??i qua c???ng quang ??i???n 1 v?? k???t th??c ????m khi t???m ch???n v?????t qua c???ng quang ??i???n 2.
B?????c 4: Gia t???c a ???????c t??nh t??? c??ng th???c: a = v0*t + 1/2*a*t^2 (?????t xe tr?????t c?? g???n t???m ch???n s??ng sao cho t???m ch???n n??y s??t v???i c???ng quang ??i???n 1 ????? v = 0; s= 0,5 m l?? kho???ng c??ch gi???a hai c???ng quang ??i???n trong th?? nghi???m). ??o th???i gian t??ng v???i m???i l??n th?? nghi???m.

Th???o lu???n:
a) D???a v??o s??? li???u trong B???ng 15.1, h??y v??? ????? th??? ch??? s??? ph??? thu???c c???a gia t???c a:
- V??o F (???ng v???i m + M = 0,5 kg), (H??nh 15.3a). ???? th??? c?? ph???i l?? ???????ng th??ng kh??ng? T???i sao?
- V??o 1 m+M (???ng v???i F - 1 N), ????? th??? c?? ph???i l?? ???????ng th???ng kh??ng? T???i sao?
b) N???u k???t lu???n v??? s??? ph??? thu???c c???a gia t???c v??o ????? l???n c???a l???c t??c d???ng v?? kh???i l?????ng
c???a v???t.''',
        "img": "assets//img1.png",
        "table_data": {
            "headers": ["L???n th???", "L???c k??o (lt)", "Kh???i l?????ng", "Th???i gian", "Qu??ng ???????ng", "Gia t???c"],
            "measuring_data": 3,
            "input_data": [1, 2, 4],
            "calucating_data": {"5": {
                    "formula": "(2*{})/({}*{})",
                    "attrs": [4, 3, 3]
                }
            },
        },
        "plot": {
            "name": "????? th??? F-a",
            "x_name": "L???c k??o F (N)",
            "y_name": "Gia t???c a (m/s)",
            "x_data": 1,
            "y_data": 5,
        }
    }
    # init serial port
    ser, ser_desc = portselector()
    print(ser.name, ser_desc)
    # bien dem so lan thu
    testcount = 0

    # du lieu cua bang
    data = []
    headings = exp_temp["table_data"]["headers"]

    # du lieu de ve do thi (x: luc keo - y: gia toc)
    x = []
    y = []

    # tao cua so chuong trinh
    menu = [
        ['&T???p', ['&Xu???t ????? th???...', '&Tho??t']],
        ['&Tr??? gi??p', ['&Th??ng tin']]
    ]
    layout = [
        [sg.Menu(menu, tearoff=False)],
        [
            # noi dung thi nghiem
            sg.Frame("M?? t??? th?? nghi???m", [
                [sg.Multiline(
                    default_text=exp_temp["desc"],
                    expand_x=True,
                     expand_y=True,
                     background_color='#fff',
                     sbar_trough_color='#fff',
                     sbar_background_color='#eeeeee',
                     sbar_arrow_color='#fff',
                     sbar_frame_color='#eeeeee'
                )]
            ], background_color='#eeeeee', title_color="#000", key="-1-"),
            # bang so lieu
            sg.Frame("B???ng s??? li???u", [
            [sg.Table(
                values=data, 
                headings=headings, 
                key="-t-", 
                # auto_size_Frames=False,  
                def_col_width=10, 
                num_rows=10, 
                justification="center", 
                expand_x=True, 
                expand_y=True, 
                font=("Arial", 14, "bold"), 
                # header_background_color=(), header_text_color=(),
                header_relief=sg.RELIEF_SOLID,
                background_color='#fff', 
                text_color='#000',
                sbar_trough_color='#fff', 
                sbar_background_color='#eeeeee', 
                sbar_arrow_color='#fff', 
                sbar_frame_color='#eeeeee', 
                sbar_relief=sg.RELIEF_FLAT
            )]], background_color='#eeeeee', title_color="#000", key="-2-"),  
        ],
        [
            # hinh anh thi nghiem
            sg.Frame("Thi???t l???p th?? nghi???m", [
                [sg.Image(expand_x=True, expand_y=True, key="-img-", background_color='#eeeeee')]
            ], background_color='#eeeeee', title_color="#000", key="-3-"),
            # do thi bieu dien ket qua thi nghiem
            sg.Frame("????? th???", [
                [sg.Canvas(key='controls_cv', background_color='#eeeeee')],
                [sg.Column(
                    layout=[
                        [sg.Canvas(key='fig_cv', expand_x=True, expand_y=True)]
                        ],
                    background_color='#eeeeee', pad=(0, 0), expand_x=True, expand_y=True),
                ],
            ], background_color='#eeeeee', title_color="#000", key="-4-"),
        ],
        [sg.StatusBar(f"???? k???t n???i t???i c???ng {ser.name} ({ser_desc})", background_color='#eeeeee', text_color='#000', size=(100,1), pad=(0,0), relief=sg.RELIEF_FLAT, justification='right', visible=True,)]
    ]
    # tao cua so chuong trinh chinh
    win = sg.Window(f"K???t qu??? ??o", layout, resizable=True, finalize=True, background_color='#eeeeee', size=(1400, 600))
    win.bind('<Configure>', "Configure")

    # load anh lan dau
    path = exp_temp["img"]
    im = Image.open(path)
    im = im.resize((int(win.size[0] / 2), int(win.size[1] / 2)), resample=Image.BICUBIC)
    image = ImageTk.PhotoImage(image=im)
    win["-img-"].update(data=image)

    # tao do thi
    plt.figure(1)
    fig = plt.gcf()
    DPI = fig.get_dpi()

    ax = plt.gca()
    ax.set_xlim(xmin = 0)
    ax.set_ylim(ymin = 0)

    # you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
    # fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

    hl, = plt.plot(x, y)
    plt.title(exp_temp["plot"]["name"])
    plt.xlabel(exp_temp["plot"]["x_name"])
    plt.ylabel(exp_temp["plot"]["y_name"])
    plt.grid()
    plt.xticks(np.arange(min([x for x in range(5)]), max([x for x in range(5)])+1, 1.0))
    plt.yticks(np.arange(min([y for y in range(5)]), max([y for y in range(5)])+1, 1.0))
    draw_figure_w_toolbar(win['fig_cv'].TKCanvas, fig, win['controls_cv'].TKCanvas)
    plt.draw()

    # event loop
    while True:
        try:
            if (ser.in_waiting != 0):
                data, testcount = datain(ser, testcount, data, x, y)
                print(data)
                win["-t-"].update(values=data)
        except serial.serialutil.SerialException:
            sg.Popup("Thi???t b??? ??o ???? ng???t k???t n???i!", title="Th??ng b??o", background_color='#eeeeee', text_color='#000', button_color=('#fff', '#000'))
            break
        e, v = win.read(timeout=500)
        if e == 'Configure':
            # lay chieu dai chieu rong
            wlength = int(win.size[0] / 2) - 20
            wheight = int(win.size[1] / 2) - 20
            # cap nhat kich thuoc cua so
            win["-1-"].set_size((wlength, wheight))
            win["-2-"].set_size((wlength, wheight))
            win["-3-"].set_size((wlength, wheight))
            win["-4-"].set_size((wlength, wheight))
            # cap nhat kich thuoc hinh anh
            img_length = int(wlength) - int(int(wlength) * 5 / 100)
            img_height = int(wheight) - int(int(wheight) * 10 / 100)
            im = Image.open(path)
            im = im.resize((img_length, img_height), resample=Image.BICUBIC)
            image = ImageTk.PhotoImage(image=im)
            win["-img-"].update(data=image)
        if e == sg.WIN_CLOSED or e == "Tho??t":
            break
        if e == "Xu???t ????? th???...":
            dir = str(os.getcwd())
            name = datetime.datetime.now()
            name = name.strftime("%d%m%y_%H%M%S") + ".xlsx"
            layout = [
                [
                    sg.Text("Ch???n th?? m???c: ", background_color='#eeeeee', text_color='#000'), 
                    sg.Input(key="-IN2-" ,change_submits=True, default_text=dir, background_color='#fff', text_color='#000', border_width=0), 
                    sg.FolderBrowse(key="-IN-", button_color=('#fff', '#000'))
                ],
                [
                    sg.Button("Ch???n", key="Submit", button_color=('#fff', '#000'))
                ]
            ]
            exp_win = sg.Window("Xu???t ????? th???", layout, finalize=True, background_color='#eeeeee')
            while True:
                event, values = exp_win.read()
                if event == sg.WIN_CLOSED or event=="Exit":
                    break
                elif event == "Submit":
                    dir = values["-IN2-"]
                    dir = dir + f"/{name}"
                    xuatfiledothi(data, dir)
                    sg.Popup(f"???? xu???t {name} t???i ???????ng d???n {dir}.", title="Ho??n t???t", background_color='#eeeeee', text_color='#000', button_color=('#fff', '#000'))
                    break
            exp_win.close()

    win.close()