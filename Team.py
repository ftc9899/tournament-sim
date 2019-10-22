import random

import options

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
	
	def __init__(self, nu, op, na=""):
		
		# a list of the partners this team has had (using team numbers)
		self.past_partners = []
		
		# a list of the opponents this team has had (using team numbers)
		self.past_opponents = []
		
		self.number = nu
		self.opr = op
		
		# don't allow a team to partner with themselves
		self.past_partners.append(nu)
		
		# don't allow a team to play against themselves
		self.past_opponents.append(nu)
		
		if na == "":
			self.name = str(nu)
		else:
			self.name = na
	
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
		if (options.ranking_system != "new2019"):
			return self.tp
		
		result = self.tp
		
		if (self.least_tp >= 0):
			result -= self.least_tp
		
		if (options.subtract_second_least_match and self.second_least_tp >= 0):
			result -= self.second_least_tp
		
		return result
	
	def get_points(self):
		#return self.opr
		
		# rand * 0.2 + 0.9 returns a value between 0.9 and 1.1
		return int(self.opr * (random.random() * 0.2 + 0.9))
	
	def stats(self):
		print('Team ' + self.name + ' ( ' + '{:0>5}'.format(self.number) + ' )')
		print('OPR: ' + str(self.opr))
		print('RP:  ' + str(self.rp))
		print('TP:  ' + str(self.get_tp()) + '\n')
	
	def win(self, w_points, l_points):
		self.rp += 2
		
		# TODO: Add eval (to call appropriate TBP method as a function)?
		if (options.ranking_system == "current"):
			self.tp += l_points
		elif (options.ranking_system == "sum"):
			self.tp += w_points + l_points
		elif (options.ranking_system == "yours"):
			self.tp += w_points
		elif (options.ranking_system == "opr"):
			self.tp += self.opr
		elif (options.ranking_system == "u_plus_lose"):
			self.tp += w_points + l_points
		elif (options.ranking_system == "inv_opr"):
			self.tp -= self.opr
		elif (options.ranking_system == "new2019"):
			self.tp += l_points
			
			if (self.least_tp == -1 or l_points < self.least_tp):
				self.least_tp = l_points
			elif (self.second_least_tp == -1 or l_points < self.second_least_tp):
				self.second_least_tp = l_points
	
	def lose(self, w_points, l_points):
		if (options.ranking_system == "current"):
			self.tp += l_points
		elif (options.ranking_system == "sum"):
			self.tp += w_points + l_points
		elif (options.ranking_system == "yours"):
			self.tp += l_points
		elif (options.ranking_system == "opr"):
			self.tp += self.opr
		elif (options.ranking_system == "u_plus_lose"):
			self.tp += l_points + l_points
		elif (options.ranking_system == "inv_opr"):
			self.tp -= self.opr
		elif (options.ranking_system == "new2019"):
			self.tp += l_points
			
			if (self.least_tp == -1 or l_points < self.least_tp):
				self.least_tp = l_points
			elif (self.second_least_tp == -1 or l_points < self.second_least_tp):
				self.second_least_tp = l_points
	
	def tie(self, w_points, l_points):
		self.rp += 1
		
		if (options.ranking_system == "current"):
			self.tp += l_points
		elif (options.ranking_system == "sum"):
			self.tp += w_points + l_points
		elif (options.ranking_system == "yours"):
			self.tp += w_points
		elif (options.ranking_system == "opr"):
			self.tp += self.opr
		elif (options.ranking_system == "u_plus_lose"):
			self.tp += w_points + l_points
		elif (options.ranking_system == "inv_opr"):
			self.tp -= self.opr
		elif (options.ranking_system == "new2019"):
			self.tp += l_points
			
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
