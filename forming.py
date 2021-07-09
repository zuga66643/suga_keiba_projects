import tkinter as tk
from ttkthemes import *
import csv
from PIL import Image
import os

#['2021', '東京', '1', '1']
def f_result(info):
    #GUIフォームから該当のページを作成
    places = ['札幌','函館','福島','新潟','東京','中山','中京','京都','阪神','小倉']
    i = 0
    for place in places:
        i += 1
        if info[1] == place:
            p_id = i
        else:
            pass
    if p_id < 10:
        p_id = '0'+str(p_id)
    else:
        p_id = str(p_id)
    if int(info[2]) < 10:
        num = '0'+info[2]
    else:
        num = info[2]
    if int(info[3]) < 10:
        day = '0'+info[3]
    else:
        day = info[3]

    sunrace_id = info[0]+p_id+num+day

    satday = int(day)-1
    if satday < 10:
        satday = '0'+str(satday)
    satrace_id = info[0]+p_id+num+str(satday)

    files = os.listdir('data')
    sat_notices = False
    for file in files:
        if satrace_id in file and 'sat_notices.csv' in file:
            sat_notices = True
    sun_notices = False
    for file in files:
        if sunrace_id in file and 'sun_notices.csv' in file:
            sun_notices = True
    images = []
    for file in files:
        if sunrace_id in file and 'deployment.png' in file:
            file = 'data/'+file
            images.append(file)
    

    root = ThemedTk()
    root.title('日曜日に勝つ競馬予想')
    root.geometry('640x480+100+200')


    label1 = tk.Label(root, text="土曜の穴レース", fg="black", font=("けいふぉんと",20))

    if sat_notices:
        labels1 = []
        file_name = 'data/'+satrace_id+'01sat_notices.csv'
        with open(file_name,'r',encoding="utf-8") as f:
            reader = csv.reader(f)
            for r in reader:
                text = r
                label = tk.Label(root, text=text, fg="blue", font=('UD デジタル 教科書体 N-B',12))
                labels1.append(label)
    else:
        labels1 = [tk.Label(root, text='ありませんでした', fg="blue", font=('UD デジタル 教科書体 N-B',12))]


    label2 = tk.Label(root, text="日曜の注目レース", fg="black", font=("けいふぉんと",20))

    if sun_notices:
        labels2 = []
        file_name = 'data/'+sunrace_id+'01sun_notices.csv'
        with open(file_name,'r',encoding="utf-8") as f:
            reader = csv.reader(f)
            for r in reader:
                text = r
                label = tk.Label(root, text=text, fg="red", font=('UD デジタル 教科書体 N-B',12))
                labels2.append(label)
        
        for image in images:
            imgPIL = Image.open(image)
            imgPIL.show()
    else:
        labels2 = [tk.Label(root, text='ありませんでした', fg="red", font=('UD デジタル 教科書体 N-B',12))]




    label1.pack(pady=30)
    for label in labels1:
        label.pack()
    label2.pack(pady=30)
    for label in labels2:
        label.pack()


    root.mainloop()