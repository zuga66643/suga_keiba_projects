from sun_race import SunRace
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
from PIL import Image
import os



def deployment_data(race_id):
    #deploymentのためのデータを成形する
    sun_race = SunRace(race_id)
    legs = sun_race.forecast_legs()
    data = {}
    data[race_id] = legs
    return data


def deployment(data, race_id):
    #展開図を作成、djangoのimageに保存
    deployment_list = data[race_id]
    for v in deployment_list:
        v[0] = int(v[0])
    deployment_list = sorted(deployment_list)


    num = []
    name = []
    horse_id = []
    deployment = []
    for v in deployment_list:
        num.append(v[0])
        name.append(v[1])
        horse_id.append(v[2])
        if v[3] == 'データなし':
            deployment.append(0)
        if v[3] == '逃げ':
            deployment.append(4)
        if v[3] == '先行':
            deployment.append(3)
        if v[3] == '中団':
            deployment.append(2)
        if v[3] == '後方':
            deployment.append(1)


    fig = plt.figure()
    ax = fig.add_subplot(111, xlabel='馬番', ylabel='脚質')
    ax.grid(axis='x', color='y', linestyle='dotted', linewidth=1)
    ax.scatter(num, deployment, c='orange', s=300)
    i = 0
    for k in num:
        ax.annotate(k, xy=(num[i],deployment[i]))
        i += 1
    ax.set_axisbelow(True)
    #0を加えて、データなしとしたい
    ax.set_yticks([0,1,2,3,4])
    ax.set_yticklabels(['データなし','後方','中団','先行','逃げ'])
    ax.set_xticks(np.arange(1,20,1))
    ax.set_title(race_id)

    place = str(race_id)[4:6]
    if place in ['01','02','03','06','08','09','10']:
        plt.axis([18.5, 0.5, -0.2, 4.2])
    else:
        plt.axis([0.5, 18.5, -0.2, 4.2])

    p = f'/Users/puyol/Documents/django/keiba_forecast/keiba_forecasts/static/deployment/{race_id}deployment.png'
    fig.savefig(p)


def deployment_farecast(race_id):
    #個別レースの展開予想
    data = deployment_data(race_id)
    deployment(data, race_id)



def dayall_deployment_forecast(race_id_list):
    #djangoの更新（消去含む）
    png_removed()

    for race_id in race_id_list:
        day_id = str(race_id)[:10]
        dayall_race_ids = []
        for i in range(1,13):
            if i > 9:
                r_id = day_id + str(i)
            else:
                r_id = day_id + '0' + str(i)
            dayall_race_ids.append(r_id)

        for id in dayall_race_ids:
            data = deployment_data(id)
            deployment(data,id)


def add_dayall(race_id_list):
    #djangoの更新（追加のみ消去無し）
    for race_id in race_id_list:
        day_id = str(race_id)[:10]
        dayall_race_ids = []
        for i in range(1,13):
            if i > 9:
                r_id = day_id + str(i)
            else:
                r_id = day_id + '0' + str(i)
            dayall_race_ids.append(r_id)

        for id in dayall_race_ids:
            data = deployment_data(id)
            deployment(data,id)


def png_removed():
    #djangoのimageフォルダ内削除
    p = f'/Users/puyol/Documents/django/keiba_forecast/keiba_forecasts/static/deployment/'
    static = os.listdir(p)
    deployment_passes = []
    for file in static:
        if 'deployment' in file:
            p = f'/Users/puyol/Documents/django/keiba_forecast/keiba_forecasts/static/deployment/{file}'
            deployment_passes.append(p)
        else:
            pass
    for p in deployment_passes:
        os.remove(p)


#djangoの更新(金曜昼に土曜分か土日分)
#race_id_list = [202103010101,202110030101,202102010101]
#dayall_deployment_forecast(race_id_list)

#djangoの更新(土曜昼に日曜分)
#race_id_list = [202103010201,202110030201,202102010201]
#add_dayall(race_id_list)