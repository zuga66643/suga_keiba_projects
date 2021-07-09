from sat_race import SatRace


class SatRaces:
	

	def __init__(self,race_id):
		str_race_id = str(race_id)
		day_id = str_race_id[:10]
		self.sat_races = []
		for i in range(1,13):
			if i <10:
				i = f'0{i}'
			#リストに一日分のRaceインスタンスを格納
			self.sat_races.append(SatRace(int(f'{day_id}{i}')))


	def day_show(self):
		#1日の結果を表示
		for race in self.sat_races: 
			print(race.race_id)
			print(race.info())
			print(race.result())
			print(race.lap())
			print(race.pace())
			print('\n')


	def day_dark_horses(self):
		#一日の穴馬を抜粋
		id_dark_horses = []
		for race in self.sat_races:
			if race.dark_horses():
				id_dark_horses.append({race.race_id:race.dark_horses()})
			else:
				pass
		return id_dark_horses


	def day_simple_dark(self):
		#一日のシンプルな穴馬情報
		day_simple_dark = []
		for race in self.sat_races:
			if race.simple_dark():
				day_simple_dark.append(race.simple_dark())
			else:
				pass
		return day_simple_dark


	def notice_races(self):
		#穴が2頭以上の多いレース
		n = []
		for race in self.day_simple_dark():
			if len(race)-9 >= 2:
				n.append(race)
		if n:
			return n
		else:
			return '今日は固い決着でした'


	def simple_nr(self):
		#notice_racesの簡略化
		notice = self.notice_races()
		if notice == '今日は固い決着でした':
			return None
		else:
			dark_legs = []
			for nl in notice:
				dark_leg = []
				for nv in nl:
					if type(nv) == dict:
						for v in nv.values():
							dark_leg.append(v['脚質'])
					else:
						pass
				dark_legs.append(dark_leg)

			simple_nr = []
			i = 0
			for nl in notice:
				nd = {'ID':nl[0],'開催':nl[1], '距離':nl[4], 'ペース判定':nl[6], 
					'有利脚質':dark_legs[i]}
				i += 1
				simple_nr.append(nd)


			return simple_nr

		


	