import requests
from bs4 import BeautifulSoup
import lxml
import re
import time



class SatRace:


	def __init__(self,race_id):
		self.race_id = race_id
		self.url = f"https://race.netkeiba.com/race/result.html?race_id={self.race_id}&rf=race_list"
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				}
		#htmlを読み込む
		time.sleep(1)		
		self.r = requests.get(self.url, timeout=(3.0, 7.5), headers=headers)
		self.r.encoding = 'EUC-JP'#文字化け解除
		#タグにアクセスできるようにする
		self.soup = BeautifulSoup(self.r.content, "lxml")


	def info(self):
		#レース情報をリストで返す
		data_intro = self.soup.find('div', class_='RaceList_Item02').find_all('span')
		intros = []
		for data in data_intro:
			intros.append(re.findall(r'\w+', data.text))
		info = []
		for intro in intros:
			for v in intro:
				info.append(v)
		infos = []
		for v in info:
			if v == '馬場':
				continue
			elif '金' in v:
				break
			else:
				infos.append(v)
		if '回' in infos[3]:
			infos.pop(2)
		return infos


	def result(self):
		all_results = self.soup.find('div', class_='ResultTableWrap').find_all('tr')
		

		all_result = []
		for i in range(4):
			v = re.findall(r'\S+', all_results[i].text)
			all_result.append(v)


		if  '新潟' in self.info()[0] and '1000m' in self.info()[0]:
			all_result[1].insert(8, 'なし')
			in_bettings = []
			for i in range(3):
				in_bettings.append({key: val for key, val in zip(all_result[0], all_result[i+1])})



		else:
			all_result[0].remove('コーナー通過順')
			all_result[1].insert(8, 'なし')
			

			in_bettings = []
			for i in range(3):
				in_bettings.append({key: val for key, val in zip(all_result[0], all_result[i+1])})
	

			first_p = ''
			secound_p = ''
			third_p = ''
			passings = self.passing()
			for passing in passings:
				for p in passing:
					for k, v in p.items():
						if in_bettings[0]['馬番'] in v:
							first_p += f'-{k}'
							if in_bettings[1]['馬番'] in v:
								secound_p += f'-{k}'
							if in_bettings[2]['馬番'] in v:
									third_p += f'-{k}'
						elif in_bettings[1]['馬番'] in v:
							secound_p += f'-{k}'
							if in_bettings[2]['馬番'] in v:
									third_p += f'-{k}'
						elif in_bettings[2]['馬番'] in v:
							third_p += f'-{k}'
						else:
							pass
			first_p = re.findall(r'\w+', first_p)
			secound_p = re.findall(r'\w+', secound_p)
			third_p = re.findall(r'\w+', third_p)


			in_bettings[0]['コーナー通過順'] = first_p
			in_bettings[1]['コーナー通過順'] = secound_p
			in_bettings[2]['コーナー通過順'] = third_p


		return in_bettings


	def passing(self):
		#通過順と馬番を辞書で返す(resultに反映)
		try:
			passings = self.soup.find('div', class_='ResultPayBackRightWrap').find_all('td')
		except AttributeError:
			return 'infoにて'

		else:
			passing = []
			for i in range(4):
				v = re.findall(r'\d+', passings[i].text)
				passing.append(v)
			orders = []
			for i in range(4):
				v = re.findall(r'\S+', passings[i].text)
				orders.append(v)
			order = []
			for vs in orders:
				for v in vs:
					v = v.replace(')(', '/')
					v = v.replace('(', '/')
					v = v.replace(')', '/')
					v = v.replace('=', '/')
					v = v.replace('*', '')
					v = v.replace('-', '/')
					v = v.replace(',', '-')
					order.append(v)
			
			p_ord = []
			for v in order:
				p_ord.append(v.split('/'))
			
			p_orders = []
			for vs in p_ord:
				i = 1
				p_order = []
				for v in vs:
					if v == '':
						continue
					elif '-' in v:
						p_order.append({i:v.split('-')})
						i += len(v.split('-'))
					else:
						p_order.append({i:[v]})
						i += 1
				p_orders.append(p_order)
			return p_orders


	def dark_horses(self):
		#穴馬を抜粋
		results = self.result()
		dark_horses = []
		for result in results:
			if int(result['人気']) > 5:
				dark_horses.append(result)
		return dark_horses


	def simple_dark(self):
		#シンプルな穴馬情報({id,info},{馬番,通過})
		dark_horses = self.dark_horses()
		info = []
		infos = self.info()
		info.append(self.race_id)
		info.append(infos[3])
		info.append(infos[5])
		info.append(infos[6])	
		info.append(infos[0])
		info.append(self.pace())
		info.append(self.pace_decision())
		info.append(infos[1])
		info.append(infos[-1])
		

		dark = []
		numin = {}
		for dark_horse in dark_horses:
			if dark_horses:
				first_p = dark_horse['コーナー通過順'][0]
				p = int(first_p)
				h_num = int(re.search(r'\d+',infos[-1]).group())
				if p == 1:
					leg = '逃げ'
				elif 1 < p <= (h_num*1/3):
					leg = '先行'
				elif (h_num*11/18) < p:
					leg = '後方'
				else:
					leg = '中団'


				numin = {f'馬番{dark_horse["馬番"]}':{'コーナー通過順':dark_horse['コーナー通過順'], 
				'脚質':leg, '人気':dark_horse['人気']}}
				dark.append(numin)
			else:
				pass
		
		dark = info + dark
		return dark


	def lap(self):
		#ラップをリストで返す
		try:
			lap_soup = self.soup.find('div', class_='Table_Scroll').find_all('tr')
		except AttributeError:
			return ['ペースデータなし']
		else:
			lap_soup = lap_soup[2].find_all('td')
			laps = []
			for l in lap_soup:
				lap = (str(l))
				lap = (lap.replace('<td>', ''))
				lap = (lap.replace('</td>', ''))
				laps.append(lap)
			return laps


	
	def pace(self):
		#ラップからペースを返す
		if self.lap() == ['ペースデータなし']:
			return 'ペースデータなし'
		else:
			pass
		lap = self.lap()
		race_pace = float(lap[0]) + float(lap[1]) + float(lap[2])
		race_pace = round(race_pace, 1)
		return race_pace


	def pace_decision(self):
		#ペース判定
		try:
			soup = self.soup.find('div', class_='RapPace_Title').find_all('span')
		except AttributeError:
			return '判定不能'
		else:
			soup = str(soup[0])
			pace = soup.replace('<span>', '')
			pd = pace.replace('</span>', '')
			return pd






