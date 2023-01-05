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
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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

# add point to existing scatter chart
def addPoint(scat, new_point, c='k'):
    old_off = scat.get_offsets()
    new_off = np.concatenate([old_off,np.array(new_point, ndmin=2)])
    old_c = scat.get_facecolors()
    new_c = np.concatenate([old_c, np.array(mcolors.to_rgba(c), ndmin=2)])

    scat.set_offsets(new_off)
    scat.set_facecolors(new_c)

    scat.axes.figure.canvas.draw_idle()

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
    chart.title = "Đồ thị F-a"
    chart.style = 13
    chart.x_axis.title = "Lực kéo F (N)"
    chart.y_axis.title = "Gia tốc a (m/s)"
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
        [sg.Text("Chọn cổng COM đến ESP32: ", background_color='#eeeeee', text_color='#000')],
        [sg.Text(portlist.strip(), background_color='#eeeeee', text_color='#000')], 
        [sg.InputText(background_color='#fff', text_color='#000', border_width=0)], 
        [sg.Submit(button_text="Kết nối", button_color=('#fff', '#000'))]
    ]
    win = sg.Window("Chọn cổng COM", layout, finalize=True, background_color='#eeeeee', font=("Arial", 10))
    e, v = win.read()
    win.close()

    # chon cong com den esp32
    # i = int(input("Chọn cổng COM để kết nối đến ESP32: "))
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
            # tạo input box trống -> đặt key -> update nội dung theo key
            # dùng hàm ngoài để parse công thức
            layout = [
                [sg.Text(f"Nhập dữ liệu còn thiếu của lần đo thứ {testcount}:",  background_color='#eeeeee', text_color='#000')],
                [sg.Text(f"Dữ liệu thời gian từ bộ đo: {sout_decoded[2]}(ms)",  background_color='#eeeeee', text_color='#000')],
                [sg.Text("Lực kéo (Lý thuyết): ",  background_color='#eeeeee', text_color='#000'), sg.InputText( background_color='#fff', text_color='#000', border_width=0)],
                [sg.Text("Khối lượng:             ",  background_color='#eeeeee', text_color='#000'), sg.InputText( background_color='#fff', text_color='#000', border_width=0)],
                [sg.Text("Quãng đường:         ",  background_color='#eeeeee', text_color='#000'), sg.InputText( background_color='#fff', text_color='#000', border_width=0)],
                [sg.Submit(button_text="Hoàn tất",  button_color=('#fff', '#000'))]
            ]
            win = sg.Window("Nhập dữ liệu đo", layout, finalize=True, background_color='#eeeeee', font=('Arial', 14))
            e, v = win.read()
            win.close()
            if (v[0] != "" and v[1] != "" and v[2] != ""): break
            else: sg.Popup("Các ô dữ liệu không được để trống!", title="Chú ý", background_color='#eeeeee', text_color='#000', button_color=('#fff', '#000'))
        time = float(sout_decoded[2]) / 1000 #ms to s
        acceleration = round(((float(v[2])*2)/(time*time)), 2)
        data.append([testcount, float(v[0]), float(v[1]), time, float(v[2]), acceleration])
        print(data)
        # cap nhat du lieu tren do thi
        x.append(float(v[0]))
        y.append(acceleration)
        # hl.set_ydata(y)
        # hl.set_xdata(x)
        addPoint(hl, [x[-1], y[-1]], 'pink')
        # plt.xticks(np.arange(min(x), max(x)+1, 1.0))
        # plt.yticks(np.arange(min(y), max(y)+1, 1.0))
        plt.draw()
        return data, testcount
    except Exception as e:
        print("oops ", e)
        sg.Popup(e, title="Lỗi", background_color='#eeeeee', text_color='#000', button_color=('#fff', '#000'))
        testcount =  (testcount - 1) if testcount >= 2 else testcount
        return data, testcount

if __name__ == "__main__":
    exp_temp = {
        "name": "Định luật 2 newton",
        "desc": '''Tiến hành:
Bước 1: Lực kéo F có độ lớn tăng dần 1 N, 2 N và 3 N (bằng cách móc thêm các quả nặng vào đầu dây vắt qua ròng rọc). 
Bước 2: Ghi vào Bảng 15.1 độ lớn lực kéo F và tổng khối lượng của hệ (gồm xe trượt và các quả nặng đặt vào xe), ứng với mỗi lần thí nghiệm.
Bước 3: Do thời gian chuyển động của xe; đồng hồ bắt đầu đếm từ lúc tám chân sáng đi qua cổng quang điện 1 và kết thúc đêm khi tấm chắn vượt qua cổng quang điện 2.
Bước 4: Gia tốc a được tính từ công thức: a = v0*t + 1/2*a*t^2 (đặt xe trượt có gắn tấm chấn sáng sao cho tấm chắn này sát với cổng quang điện 1 để v = 0; s= 0,5 m là khoảng cách giữa hai cổng quang điện trong thí nghiệm). Đo thời gian túng với mỗi làn thí nghiệm.

Thảo luận:
a) Dựa vào số liệu trong Bảng 15.1, hãy vẽ đồ thị chỉ sự phụ thuộc của gia tốc a:
- Vào F (ứng với m + M = 0,5 kg), (Hình 15.3a). Đô thị có phải là đường tháng không? Tại sao?
- Vào 1 m+M (ứng với F - 1 N), đồ thị có phải là đường thẳng không? Tại sao?
b) Nếu kết luận về sự phụ thuộc của gia tốc vào độ lớn của lực tác dụng và khối lượng
của vật.''',
        "img": "assets//img1.png",
        "table_data": {
            "headers": ["Lần thử", "Lực kéo (lt)", "Khối lượng", "Thời gian", "Quãng đường", "Gia tốc"],
            "measuring_data": 3,
            "input_data": [1, 2, 4],
            "calucating_data": {"5": {
                    "formula": "(2*{})/({}*{})",
                    "attrs": [4, 3, 3]
                }
            },
        },
        "plot": {
            "name": "Đồ thị F-a",
            "x_name": "Lực kéo F (N)",
            "y_name": "Gia tốc a (m/s)",
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
        ['&Tệp', ['&Xuất đồ thị...', '&Thoát']],
        ['&Trợ giúp', ['&Thông tin']]
    ]
    layout = [
        [sg.Menu(menu, tearoff=False)],
        [
            # noi dung thi nghiem
            sg.Frame("Mô tả thí nghiệm", [
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
            sg.Frame("Bảng số liệu", [
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
            sg.Frame("Thiết lập thí nghiệm", [
                [sg.Image(expand_x=True, expand_y=True, key="-img-", background_color='#eeeeee')]
            ], background_color='#eeeeee', title_color="#000", key="-3-"),
            # do thi bieu dien ket qua thi nghiem
            sg.Frame("Đồ thị", [
                [sg.Canvas(key='controls_cv', background_color='#eeeeee')],
                [sg.Column(
                    layout=[
                        [sg.Canvas(key='fig_cv', expand_x=True, expand_y=True)]
                        ],
                    background_color='#eeeeee', pad=(0, 0), expand_x=True, expand_y=True),
                ],
            ], background_color='#eeeeee', title_color="#000", key="-4-"),
        ],
        [sg.StatusBar(f"Đã kết nối tới cổng {ser.name} ({ser_desc})", background_color='#eeeeee', text_color='#000', size=(100,1), pad=(0,0), relief=sg.RELIEF_FLAT, justification='right', visible=True,)]
    ]
    # tao cua so chuong trinh chinh
    win = sg.Window(f"Kết quả đo", layout, resizable=True, finalize=True, background_color='#eeeeee', size=(1400, 600))
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

    hl = plt.scatter(x, y, cmap=matplotlib.cm.spring, c='pink')
    plt.title(exp_temp["plot"]["name"])
    plt.xlabel(exp_temp["plot"]["x_name"])
    plt.ylabel(exp_temp["plot"]["y_name"])
    plt.grid()
    plt.xticks(np.arange(1, 7, 1.0))
    plt.yticks(np.arange(1, 7, 1.0))
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
            sg.Popup("Thiết bị đo đã ngắt kết nối!", title="Thông báo", background_color='#eeeeee', text_color='#000', button_color=('#fff', '#000'))
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
        if e == sg.WIN_CLOSED or e == "Thoát":
            break
        if e == "Xuất đồ thị...":
            dir = str(os.getcwd())
            name = datetime.datetime.now()
            name = name.strftime("%d%m%y_%H%M%S") + ".xlsx"
            layout = [
                [
                    sg.Text("Chọn thư mục: ", background_color='#eeeeee', text_color='#000'), 
                    sg.Input(key="-IN2-" ,change_submits=True, default_text=dir, background_color='#fff', text_color='#000', border_width=0), 
                    sg.FolderBrowse(key="-IN-", button_color=('#fff', '#000'))
                ],
                [
                    sg.Button("Chọn", key="Submit", button_color=('#fff', '#000'))
                ]
            ]
            exp_win = sg.Window("Xuất đồ thị", layout, finalize=True, background_color='#eeeeee')
            while True:
                event, values = exp_win.read()
                if event == sg.WIN_CLOSED or event=="Exit":
                    break
                elif event == "Submit":
                    dir = values["-IN2-"]
                    dir = dir + f"/{name}"
                    xuatfiledothi(data, dir)
                    sg.Popup(f"Đã xuất {name} tại đường dẫn {dir}.", title="Hoàn tất", background_color='#eeeeee', text_color='#000', button_color=('#fff', '#000'))
                    break
            exp_win.close()

    win.close()
