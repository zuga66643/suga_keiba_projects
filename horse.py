import requests
from bs4 import BeautifulSoup
import re
import time


class Horse:
	"""馬の過去データ"""

	def __init__(self,horse_id):
		self.horse_id = horse_id
		self.url = f'https://db.netkeiba.com/horse/result/{self.horse_id}/'
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				}
		time.sleep(1)
		self.r = requests.get(self.url, timeout=(3.0, 0.75), headers=headers)
		self.r.encoding = 'EUC-JP'
		self.soup = BeautifulSoup(self.r.content, 'lxml')


	def past_data(self):
		#直近過去データ
		soup = self.soup.find("div", class_="db_main_deta mb30").find_all('tr')
		

		all_race = []
		for v in soup:
			race = re.findall(r'\S+', v.text)
			all_race.append(race) 
		

		ten_race = all_race[1:6]#5レース分		
		for race in ten_race:
			try:
				try_int = int(race[5])
			except ValueError:
				race.pop(5)
				try:
					try_int = int(race[5])
				except ValueError:
					race.pop(5)
					for v in race:
						if v == '**':
							race.remove('**')
						else:
							pass
				else:
					for v in race:
						if v == '**':
							race.remove('**')
						else:
							pass

			else:	
				for v in race:
					if v == '**':
						race.remove('**')
					else:
						pass
			

		removed_keys = ['映像','馬場指数','ﾀｲﾑ指数','厩舎ｺﾒﾝﾄ', '備考', 
						'勝ち馬(2着馬)', '賞金']
		no_data = [{'日付': '2200/01/09', '開催': '1中京2', '天気': '晴', 'R': '1', 'レース名': '3歳未勝利', '頭数': '16', '枠番': '2', '馬番': '3', 'オッズ': '12.7', '人気': '5', '着順': '6', '騎手': '加藤祥太', '斤量': '56', '距離': 'ダ4000', '馬場': '良', 'タイム': '1:56.5', '着差': '0.9', '通過': '4-5-6-5', 'ペース': '37.8-39.2', '上り': '39.6', '馬体重': '1000'}]
		for k in removed_keys:
			try:
				all_race[0].remove(k)
			except IndexError:
				return no_data
			
		past_data = []
		for race in ten_race:
			past_dict = {}
			for i in range(len(all_race[0])):
				try:
					past_dict[all_race[0][i]] = race[i]
				except IndexError:
					past_dict.clear()
					break
			if past_dict:
				past_data.append(past_dict)
			else:
				pass
		return past_data


	def simple_data(self):
		#past_dataから必要な情報のみ抽出
		past_data = self.past_data()
		simple_data = []
		poped_keys = ['天気','R','枠番','着差','馬体重']
		for data in past_data:
			for k in poped_keys:
				data.pop(k, None)
			simple_data.append(data)
		return simple_data


	def passing_data(self):
		#通過順予想のためのデータ
		past_data = self.past_data()
		simple_data = []
		poped_keys = [
			'日付','開催','R','レース名','枠番','馬番','オッズ','天気',
			'枠番','人気','着順','騎手','斤量','タイム','着差','上り','馬体重']
		for data in past_data:
			for k in poped_keys:
				data.pop(k, None)
			simple_data.append(data)


		pace_decision = self.pace_decision()
		legs = self.legs()
		i = 0
		for data in past_data:
			data['ペース判定'] = pace_decision[i]
			data['脚質'] = legs[i]
			i += 1

		return simple_data


	def pace_decision(self):
		#paceを判定する
		past_data = self.past_data()		
		pace_data = []
		for data in past_data:
			pace_data.append(data['ペース'].split('-'))
		pace_decision = []
		for pace in pace_data:
			d = round((float(pace[0]) - float(pace[1])), 1)
			if d > 0.8:
				pace_decision.append(f'S +{d}')
			elif d < -0.8:
				pace_decision.append(f'H {d}')
			else:
				if d == 0:
					pace_decision.append(f'M {d}')				
				elif d > 0:
					pace_decision.append(f'M +{d}')
				else:
					pace_decision.append(f'M {d}')

		return pace_decision

	def legs(self):
		#レースごとの脚質を判定
		past_data = self.past_data()
		legs = []
		for p in past_data:
			l_list = re.findall(r'\w+', p['通過'])
			leg = int(l_list[0])
			h_num = int(p['頭数'])
			if leg == 1:
				legs.append('逃げ')
			elif 1 < leg <= (h_num*1/3):
				legs.append('先行')
			elif (h_num*11/18) < leg:
				legs.append('後方')
			else:
				legs.append('中団')
		return legs

"""[{'日付': '2021/05/22', '開催': '2新潟5', '天気': '晴', 'R': '10', 
'レース名': '早苗賞(1勝クラス)', '頭数': '9', '枠番': '8', '馬番': '8', 
'オッズ': '10.9', '人気': '5', '着順': '1', '騎手': '亀田温心', '斤量': '54', 
'距離': '芝1800', '馬場': '稍', 'タイム': '1:49.3', '着差': '-0.3', 
'通過': '2-2', 'ペース': '35.5-37.7', '上り': '37.5', '馬体重': '456(0)'},
{'日付': '2020/12/03', '開催': '船橋', '天気': '曇', 'R': '6', 'レース名': 'C2', '頭数': '選抜馬', '枠番': '13', '馬番': '7', 'オッズ': '10', '人気': '1.4', '着順': '1', '騎手': '1', '斤量': '張田昂', '距離': '54', '馬場': 'ダ1000', 'タイム': '稍', '着差': '1:00.0', '通過': '-0.1', 'ペース': '2-2', '上り': '34.8-36.8', '馬体重': '36.5'}
"""

#horse = Horse(2018105555)
#print(horse.past_data())