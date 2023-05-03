import random

TBP_METHOD_CALCULATIONS_FOR_WINNING_TEAM = {
	'current'     : 'l_points',
	'sum'         : ' w_points + l_points',
	'yours'       : 'w_points',
	'opr'         : 'self.opr',
	'u_plus_lose' : 'w_points + l_points',
	'inv_opr'     : '-self.opr',
	'random'      : '', # random tbp will be assigned later
	'new2019'     : 'l_points'
}

TBP_METHOD_CALCULATIONS_FOR_LOSING_TEAM = {
	'current'     : 'l_points',
	'sum'         : 'w_points + l_points',
	'yours'       : 'l_points',
	'opr'         : 'self.opr',
	'u_plus_lose' : 'l_points * 2',
	'inv_opr'     : '-self.opr',
	'random'      : '', # random tbp will be assigned later
	'new2019'     : 'l_points'
}

class Team:
	
	name = ""
	number = -1
	
	rp = 0
	tp = 0
	matches_played = 0
	matches_scheduled = 0
	opr = -1
	
	least_tp = -1
	second_least_tp = -1
	
	def __init__(self, number, opr, name=""):
		
		# a list of the partners this team has had (using team numbers)
		self.past_partners = []
		
		# a list of the opponents this team has had (using team numbers)
		self.past_opponents = []
		
		self.number = number
		self.opr = opr
		
		# don't allow a team to partner with themselves
		self.past_partners.append(number)
		
		# don't allow a team to play against themselves
		self.past_opponents.append(number)
		
		if name == "":
			self.name = str(number)
		else:
			self.name = name
	
	# if a team is less than another team, they rank above the other team
	def __lt__(self, other):
		if self.rp != other.rp:
			return self.rp > other.rp
		elif self.get_tp() != other.get_tp():
			return self.get_tp() > other.get_tp()
		else:
			return self.number < other.number
	
	# if a team is greater than another team, they rank below the other team
	def __gt__(self, other):
		if self.rp != other.rp:
			return self.rp < other.rp
		elif self.get_tp() != other.get_tp():
			return self.get_tp() < other.get_tp()
		else:
			return self.number > other.number
	
	def __eq__(self, other):
		return self.number == other.number
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def get_tp(self):
		return self.tp
	
	def get_points(self):
		#return self.opr
		
		# rand * 0.2 + 0.9 returns a value between 0.9 and 1.1
		return int(self.opr * (random.random() * 0.2 + 0.9))
	
	def stats(self):
		print('Team ' + self.name + ' ( ' + '{:0>5}'.format(self.number) + ' )')
		print('OPR: ' + str(self.opr))
		print('RP:  ' + str(self.rp))
		print('TP:  ' + str(self.get_tp()) + '\n')
	
	def win(self, w_points, l_points, tbp_method):
		self.rp += 2
		self.tp += eval(TBP_METHOD_CALCULATIONS_FOR_WINNING_TEAM[tbp_method])

		if tbp_method == 'new2019':
			if (self.least_tp == -1 or l_points < self.least_tp):
				self.least_tp = l_points
			elif (self.second_least_tp == -1 or l_points < self.second_least_tp):
				self.second_least_tp = l_points
	
	def lose(self, w_points, l_points, tbp_method):
		self.tp += eval(TBP_METHOD_CALCULATIONS_FOR_LOSING_TEAM[tbp_method])

		if tbp_method == 'new2019':
			if (self.least_tp == -1 or l_points < self.least_tp):
				self.least_tp = l_points
			elif (self.second_least_tp == -1 or l_points < self.second_least_tp):
				self.second_least_tp = l_points
	
	def tie(self, w_points, l_points, tbp_method):
		self.rp += 1
		self.tp += eval(TBP_METHOD_CALCULATIONS_FOR_WINNING_TEAM[tbp_method])

		if tbp_method == 'new2019':
			if (self.least_tp == -1 or l_points < self.least_tp):
				self.least_tp = l_points
			elif (self.second_least_tp == -1 or l_points < self.second_least_tp):
				self.second_least_tp = l_points
	
	def reset(self):
		self.rp = 0
		self.tp = 0
		self.least_tp = -1
		self.second_least_tp = -1
		self.matches_played = 0
		self.matches_scheduled = 0
		
		self.past_partners = []
		self.past_opponents = []
		
		# don't allow a team to partner with themselves
		self.past_partners.append(self.number)
		
		# don't allow a team to play against themselves
		self.past_opponents.append(self.number)
	
	def reset_tbp(self):
		self.tp = 0
		self.rp = 0
		self.least_tp = -1
		self.second_least_tp = -1
