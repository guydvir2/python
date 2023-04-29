import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

# root window
root = tk.Tk()
root.title('Temperature Converter')
# root.geometry('400x70')
root.resizable(True, True)

# def fahrenheit_to_celsius(f):
#     """ Convert fahrenheit to celsius
#     """
#     return (f - 32) * 5/9
#
#
# frame
frame = ttk.Frame(root)

# field options
# options = {'padx': 5, 'pady': 5}

# radio1 = ttk.Checkbutton(frame, text="test1", )
# radio1.grid(column=0, row=0)
# radio2 = ttk.Checkbutton(frame, text="test2")
# radio2.grid(column=0, row=1)
# radio3 = ttk.Checkbutton(frame, text="test3")
# radio3.grid(column=0, row=2)

canvas = tk.Canvas(frame, background="dark grey")
canvas.pack()
# # temperature label
# temperature_label = ttk.Label(frame, text='Fahrenheit')
# temperature_label.grid(column=0, row=0, sticky='W', **options)
#
# # temperature entry
# temperature = tk.StringVar()
# temperature_entry = ttk.Entry(frame, textvariable=temperature,width=10)
# temperature_entry.grid(column=1, row=0, **options)
#
# temperature_entry.focus()
#
# # convert button
#
#
# def convert_button_clicked():
#     """  Handle convert button click event
#     """
#     try:
#         f = float(temperature.get())
#         c = fahrenheit_to_celsius(f)
#         result = f'{f} Fahrenheit = {c:.2f} Celsius'
#         result_label.config(text=result)
#     except ValueError as error:
#         showerror(title='Error', message=error)
#
#
# convert_button = ttk.Button(frame, text='Convert')
# convert_button.grid(column=2, row=0, sticky='W', **options)
# convert_button.configure(command=convert_button_clicked)
#
# # result label
# result_label = ttk.Label(frame)
# result_label.grid(row=1, columnspan=3, **options)
#
# # add padding to the frame and show it
frame.grid(padx=30, pady=10)

# start the app
root.mainloop()
