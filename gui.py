import tkinter as tk
from tkinter import StringVar, ttk, font
from tkinter.constants import CENTER
from ttkthemes import *
from prac import f_result



root = ThemedTk()
root.title('日曜日に勝つ競馬予想')
root.geometry('640x480+100+200')
#root.configure(bg="#FFA500")


label = tk.Label(root, text="日曜日に勝つ競馬予想", fg="black", font=("けいふぉんと",30))


s = ttk.Style()
s.theme_use('radiance')
frame1 = ttk.Frame(root)
label_frame1 = ttk.Labelframe(
    frame1,
    borderwidth=2,
    relief='solid',
    text='予想したい日',
    padding=8,
    )

label1 = ttk.Label(label_frame1, text='year', padding=(5, 2),font=('',12))

v1 = StringVar()

entry1 = ttk.Entry(
    label_frame1,
    textvariable=v1,
    width=4,
    font=('',15)
    )
entry1.insert(0,'2021')


label2 = ttk.Label(label_frame1, text='開催', padding=(5, 2),font=('',12))

v2 = StringVar()

entry2 = ttk.Entry(
    label_frame1,
    textvariable=v2,
    width=4,
    font=('',15)
    )
entry2.insert(0,'東京')


label3 = ttk.Label(label_frame1, text='回', padding=(5, 2),font=('',10))

v3 = StringVar()

entry3 = ttk.Entry(
    label_frame1,
    textvariable=v3,
    width=2,
    font=('',15)
    )
entry3.insert(0,'1')


label4 = ttk.Label(label_frame1, text='日目', padding=(5, 2),font=('',10))

v4 = StringVar()

entry4 = ttk.Entry(
    label_frame1,
    textvariable=v4,
    width=2,
    font=('',15)
    )
entry4.insert(0,'1')


def button_clicked():
    info = []
    year = v1.get()
    place = v2.get()
    num = v3.get()
    day = v4.get()
    info = [year,place,num,day]
    return info

Button = tk.Button(root,text='予想する',
    font=('けいふぉんと',20),
    command=lambda:[button_clicked(), f_result(button_clicked())]
    )


label.pack(pady=60)
frame1.pack(pady=0)
label_frame1.pack()

label1.pack()
entry1.pack()
label2.pack()
entry2.pack()
entry3.pack(side='left')
label3.pack(side='left')
entry4.pack(side='left')
label4.pack(side='left')

Button.pack(pady=30)

image = tk.PhotoImage(file="image\horse1.png")
canvas = tk.Canvas(root, bg="white", height=100, width=100)
canvas.place(x=525,y=25)
canvas.create_image(50, 50, image=image)


root.mainloop()