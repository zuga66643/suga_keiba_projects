from sun_race import SunRace


class SunRaces:
	"""ねらい目のレースとねらいの馬を予想"""

	def __init__(self,race_id):
		day_id = str(race_id)[:10]
		self.sun_races = []
		for i in range(1,13):
			if i > 9:
				r_id = day_id + str(i)
			else:
				r_id = day_id + '0' + str(i)		
			self.sun_races.append(SunRace(int(f'{r_id}')))


	def day_all_info(self):
		#一日のsun_raceinfoを全て返す
		sun_races = self.sun_races
		d_a_info = []
		for race in sun_races:
			info = race.info()
			info.pop(5)
			info.pop(3)
			d_a_info.append(info)
		return d_a_info



