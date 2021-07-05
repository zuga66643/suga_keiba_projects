import requests
from bs4 import BeautifulSoup
import lxml
import re
import time


from sat_races import SatRaces
from horse import Horse


class SunRace:
	"""出馬表からの情報を格納"""

	def __init__(self, race_id):
		self.race_id = race_id
		self.url = f'https://race.netkeiba.com/race/shutuba.html?race_id={self.race_id}'
		

		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				}
		time.sleep(1)
		self.r = requests.get(self.url, timeout=(3.0, 7.5), headers=headers)
		self.r.encoding = 'EUC-JP'

		self.soup = BeautifulSoup(self.r.text, 'lxml')


	def info(self):
		"""レース情報をリストで返す"""
		data_intro = self.soup.find('div', class_='RaceList_Item02').find_all('span')
		intros = []
		for data in data_intro:
			intros.append(re.findall(r'\w+', data.text))
		info = []
		for intro in intros:
			for v in intro:
				info.append(v)
		infos = [self.race_id]
		for v in info:
			if v == '馬場':
				continue
			elif '金' in v:
				break
			else:
				infos.append(v)
		return infos


	def entry_horses(self):
		#馬番,名前,linkをリストで返す
		soup = self.soup.find("div", class_="RaceTableArea").find_all('tr')
		c_soup1 = []
		for v in soup:
			c_soup1.append(re.findall(r"\w+", v.text))
		c_soup1.pop(0)
		c_soup1.pop(0)


		horse_soup = self.soup.find('div', class_='RaceTableArea').find_all('a')
		horses_a = []
		for v in horse_soup:
			link = v.get('href')
			if "https://db.netkeiba.com/horse/" in link:
				horses_a.append(re.search(r'\d+', link).group())

		c_soup2 = []
		i = 0
		for vs in c_soup1:
			horse = []
			horse.append(vs[1])
			horse.append(vs[3])
			horse.append(horses_a[i])
			i += 1


			c_soup2.append(horse)


		return c_soup2


	def horses_data(self):
		#各馬の過去データをリストで返す
		horses = []
		for h in self.entry_horses():
			horse = Horse(h[-1])#インスタンス化した馬をリストに入れる
			horses.append(horse)
		horses_data = []
		for horse in horses:
			horses_data.append(horse.past_data())

		return horses_data


	def horses_passing_data(self):
		#各馬の過去通過データをリストで返す
		horses = []
		for h in self.entry_horses():
			horse = Horse(h[-1])#インスタンス化した馬をリストに入れる
			horses.append(horse)
		horses_data = []
		for horse in horses:
			horses_data.append(horse.passing_data())

		return horses_data


	def vaild_passing_data(self):
		#通過順位予想に有効なデータのみを返す
		course = self.info()[1]
		#芝かダートか
		course_cate = re.search(r'\S', course).group()
		#距離(後で+-200以内だけにする)
		course_leng = re.search(r'\d+', course).group()

		passing_datas = []
		for datas in self.horses_passing_data():
			horse_p = []
			for data in datas:
				data_leng = re.search(r'\d+', data['距離']).group()
				if course_cate in data['距離'] and abs(int(course_leng) - int(data_leng)) <= 200:
					horse_p.append(data)
			passing_datas.append(horse_p)
		return passing_datas


	def forecast_legs(self):
		#脚質を予想する
		v_p_data = self.vaild_passing_data()
		legs = []
		for vs in v_p_data:
			h_legs = []
			for v in vs:
				h_legs.append(v['脚質'])
			legs.append(h_legs)


		f_legs = []
		for leg in legs:
			n = leg.count('逃げ')
			s = leg.count('先行')
			c = leg.count('中団')
			k = leg.count('後方')
			leg_count = [n, s, c, k]
			leg_m = max(leg_count)
			#leg_m==0のときはデータなしとしたい
			if leg_m == 0:
				f_legs.append('データなし')
			elif leg_m == n:
				f_legs.append('逃げ')#カウントが同じ場合、上の脚質を優先
			elif leg_m == s:
				f_legs.append('先行')
			elif leg_m == c:
				f_legs.append('中団')
			else:
				f_legs.append('後方')
		legs_horses = self.entry_horses()
		i = 0
		for h in legs_horses:
			h.append(f_legs[i])
			i += 1
		return legs_horses


	def forecast_pace(self):
		#ペース予想
		forecast_legs = self.forecast_legs()
		n_count = []
		s_count = []
		c_count = []
		k_count = []
		for forecast_leg in forecast_legs:
			if forecast_leg[-1] == '逃げ':
				n_count.append(forecast_leg)
			elif forecast_leg[-1] == '先行':
				s_count.append(forecast_leg)
			elif forecast_leg[-1] == '中団':
				c_count.append(forecast_leg)
			else:
				k_count.append(forecast_leg)
		if len(n_count) + len(s_count) >= len(forecast_legs)*8/18:
			return 'H'
		elif len(n_count) + len(s_count) < len(forecast_legs)*4/18:
			return 'S'
		else:
			return 'M'



