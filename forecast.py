import re
import pandas as pd

from sat_races import SatRaces
from sun_race import SunRace
from sun_races import SunRaces
from deployment import deployment
import japanize_matplotlib

class Forecast:
	"""予想を組み立てる"""

	def __init__(self,sat_id):
		self.sat_id = sat_id
		sat_id_str = str(self.sat_id)
		day_id = sat_id_str[8:10]
		sun_day_id = str(int(day_id) + 1)
		if int(day_id) < 9:
			self.sun_id = sat_id_str[:8] + '0' +sun_day_id + sat_id_str[10:]
		else:
			self.sun_id = sat_id_str[:8] + sun_day_id + sat_id_str[10:]
		

		self.sat_races = SatRaces(self.sat_id)
		#satの穴レース
		self.sat_notices = self.sat_races.simple_nr()
		#sat穴レース一覧
		self.sat_day_simple_dark = self.sat_races.day_simple_dark()


	def forecast(self):
		#予想を表示する
		while True:
			print('土曜のレースと穴馬')
			sat_day_simple_dark = self.sat_day_simple_dark
			for i in sat_day_simple_dark:
				print(i)
			print('\n')
			data = sat_day_simple_dark
			df = pd.DataFrame(data=data)
			sat_id = self.sat_id
			df.to_csv(f'data/{sat_id}sat_races.csv', index=False, header=False)
		

			print('穴馬２頭以上のレース')
			sat_notices = self.sat_notices
			if sat_notices == None:
				print('ありません')
				break
			else:
				for i in sat_notices:
					print(i)
			print('\n')
			data = sat_notices
			df = pd.DataFrame(data=data)
			sat_id = self.sat_id
			df.to_csv(f'data/{sat_id}sat_notices.csv', index=False, header=False)


			print('日曜注目レース')
			sun_notice_race = self.sun_notice_race()
			if sun_notice_race:
				for i in sun_notice_race:
					print(i)
			else:
				print('ありません')
				break
			print('\n')
			data = sun_notice_race
			df = pd.DataFrame(data=data)
			sun_id = self.sun_id
			df.to_csv(f'data/{sun_id}sun_notices.csv', index=False, header=False)


			print('注目レース展開予想')
			notice_deployment = self.notice_deployment()
			for i in notice_deployment:
				print(i)
				race_id = i.keys()
				for race_id in race_id:
					race_id = race_id
				deployment(i, race_id)
			print('\n')
			data = notice_deployment
			df = pd.DataFrame(data=data)
			sun_id = self.sun_id
			df.to_csv(f'data/{sun_id}notices_deployment.csv', index=False, header=False)


			print('注目馬')
			notice_horse_leg = self.notice_horse_leg()
			for i in notice_horse_leg:
				print(i)
			data = notice_horse_leg
			df = pd.DataFrame(data=data)
			sun_id = self.sun_id
			df.to_csv(f'data/{sun_id}notce_horse_leg.csv', index=False, header=False)


			break
			

	def sun_notice_race(self):
		#土曜の穴レースから日曜の注目レースを返す
		sun_races = SunRaces(self.sun_id)
		day_all_info = sun_races.day_all_info()
		sn = self.sat_notices

		#土曜の穴レース+-200mのレースを抜粋
		sun_nr = []
		for s in sn:
			if '逃げ' not in s['有利脚質'] and '先行' not in s['有利脚質'] or '中団' not in s['有利脚質'] and '後方' not in s['有利脚質']:
				#芝かダートか
				s_cate = re.search(r'\S', s['距離']).group()
				#距離
				s_leng = re.search(r'\d+', s['距離']).group()
				for d in day_all_info:
					d_cate = re.search(r'\S', d[1]).group()
					d_leng = re.search(r'\d+', d[1]).group()
					leng_range = abs(int(s_leng) - int(d_leng))
					if s_cate == d_cate and leng_range <=200:
						sun_nr.append(d)
			else:
				pass

		#重複を消して、id順に並べ替える
		sun_notice_race = []
		for s in sun_nr:
			if s in sun_notice_race:
				pass
			else:
				sun_notice_race.append(s)
		sun_notice_race = sorted(sun_notice_race, key=lambda x: x[0])


		return sun_notice_race


	def notice_ids(self):
		#sun_notice_raceに注目馬を紐づける
		snrs = self.sun_notice_race()
		#idをリストに格納
		sun_ids = []
		for snr in snrs:
			sun_ids.append(snr[0])
		return sun_ids


	def notice_deployment(self):
		#idから展開を予想
		sun_ids = self.notice_ids()

		order = ['逃げ', '先行', '中団', '後方', 'データなし']
		notice_deployment = []
		for sun_id in sun_ids:
			sun_race = SunRace(sun_id)
			n_d = sun_race.forecast_legs()
			forecast_pace = sun_race.forecast_pace()
			clean_n_d = []
			for o in order:
				for n in n_d:
					if n[-1] == o:
						clean_n_d.append(n)
					else:
						pass
			notice_deployment.append({sun_id : clean_n_d})

		return notice_deployment


	def notice_horse_leg(self):
		#idから注目馬とその脚質をリストに格納
		sat_notices = self.sat_notices
		sun_ids = self.notice_ids()


		notice_horses = []
		for sun_id in sun_ids:
			sun_race = SunRace(sun_id)
			s_info = sun_race.info()
			sun_cate = re.search(r'\S', s_info[1]).group()
			sun_leng = re.search(r'\d+', s_info[1]).group()
			f_legs = sun_race.forecast_legs()


			for sat in sat_notices:
				sat_cate = re.search(r'\S', sat['距離']).group()
				sat_leng = re.search(r'\d+', sat['距離']).group()			
				leng_range = abs(int(sat_leng) - int(sun_leng))


				n_h = []
				for f_leg in f_legs:
					if sat_cate == sun_cate and leng_range <=200:
						if f_leg[-1] in sat['有利脚質']:
							n_h.append(f_leg) 
						else:
							pass
					else:
						pass
				if n_h:
					notice_horses.append({sun_race.race_id:n_h})
				else:
					pass

		#重複を削除
		notice_horses_leg = []
		for n in notice_horses:
			if n in notice_horses_leg:
				pass
			else:
				notice_horses_leg.append(n)


		return notice_horses_leg







"""ids = [202103010101,202110030101,202102010101]
for id in ids:
	forecast = Forecast(id)
	forecast.forecast()
"""

