import PySimpleGUI as sg

data = [[1, 100], [2, 200], [3, 300], [4, 400]]
headings = ["Lan Thu", "△t"]

layout = [[sg.Table(values=data, headings=headings, key="-t-", auto_size_columns=False,  def_col_width=10, num_rows=10, justification="center", )], ]
win = sg.Window("Test", layout, resizable=True)

while True:
    e, v = win.read()
    if e == sg.WIN_CLOSED:
        break

win.close()