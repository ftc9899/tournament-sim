import random
import time
import numpy as np

from Team import Team
from Match import Match

class Tournament:
	
	matches_per_team = 0
	number_of_matches = 0
	
	ceiling_hits = 0
	
	def __init__(self, te, ma):
		# set up the array of teams, which will also keep track of rankings
		self.teams = []
		if isinstance(te, int):
			self.generate_n_teams(te)
		else:
			self.teams = te
		
		self.rank()
		self.matches_per_team = ma
		#TODO: check that with the number of teams given, the requested amount of
		     # matches per team can be played without conflicts'''
		
		self.number_of_matches = len(self.teams) * self.matches_per_team // 4
		
		self.matches = []
	
	def create_match_schedule(self):
		for n in range(1, self.number_of_matches + 1):
			red1 = random.choice(self.teams)
			
			failures = 0
			
			while (red1.matches_scheduled >= self.matches_per_team):
				#print('red1:  ' + red1.name + ' has already been scheduled for ' + str(red1.matches_scheduled) + ' matches')
				failures += 1
				#if failures > len(self.teams):
				if failures > 3 * len(self.teams):
					self.reset()
					return False
				red1 = random.choice(self.teams)
			#print('red1  FINALIZED:', red1.name)
			
			assert red1.matches_scheduled < self.matches_per_team
			red1.matches_scheduled += 1
			
			red2 = random.choice(self.teams)
			
			failures = 0
			
			# check that there is such a team before entering the while loop
			while (red2.matches_scheduled >= self.matches_per_team or red2.number in red1.past_partners):
				'''if (red2.matches_scheduled >= self.matches_per_team):
					print('red2:  ' + red2.name + ' has already been scheduled for ' + str(red2.matches_scheduled) + ' matches')
				else:
					print('red2:  ' + red2.name + ' has already partnered with ' + red1.name)'''
				failures += 1
				#if failures > len(self.teams):
				if failures > 3 * len(self.teams):
					self.reset()
					return False
				red2 = random.choice(self.teams)
			#print('red2  FINALIZED:', red2.name)
			
			assert red2.matches_scheduled < self.matches_per_team
			assert red1.number != red2.number
			red2.matches_scheduled += 1
			
			red1.past_partners.append(red2.number)
			red2.past_partners.append(red1.number)
			
			blue1 = random.choice(self.teams)
			
			failures = 0
			
			# check that there is such a team before entering the while loop
			while (blue1.matches_scheduled >= self.matches_per_team or blue1.number in red1.past_opponents or blue1.number in red2.past_opponents):
				'''if (blue1.matches_scheduled >= self.matches_per_team):
					print('blue1: ' + blue1.name + ' has already been scheduled for ' + str(blue1.matches_scheduled) + ' matches')
				elif (blue1.number in red1.past_opponents):
					print('blue1: ' + blue1.name + ' has already played against ' + red1.name)
				else:
					print('blue1: ' + blue1.name + ' has already played against ' + red2.name)'''
				failures += 1
				#if failures > len(self.teams):
				if failures > 3 * len(self.teams):
					self.reset()
					return False
				blue1 = random.choice(self.teams)
			#print('blue1 FINALIZED:', blue1.name)
			
			assert blue1.matches_scheduled < self.matches_per_team
			assert red1.number != blue1.number
			assert red2.number != blue1.number
			blue1.matches_scheduled += 1
			
			blue2 = random.choice(self.teams)
			
			failures = 0
			
			# check that there is such a team before entering the while loop
			while (blue2.matches_scheduled >= self.matches_per_team or blue2.number in red1.past_opponents or blue2.number in red2.past_opponents or blue2.number in blue1.past_partners):
				'''if (blue2.matches_scheduled >= self.matches_per_team):
					print('blue2: ' + blue2.name + ' has already been scheduled for ' + str(blue2.matches_scheduled) + ' matches')
				elif (blue2.number in red1.past_opponents):
					print('blue2: ' + blue2.name + ' has already played against ' + red1.name)
				elif (blue2.number in red2.past_opponents):
					print('blue2: ' + blue2.name + ' has already played against ' + red2.name)
				else:
					print('blue2: ' + blue2.name + ' has already partnered with ' + blue1.name)'''
				failures += 1
				#if failures > len(self.teams):
				if failures > 3 * len(self.teams):
					self.reset()
					return False
				blue2 = random.choice(self.teams)
			#print('blue2 FINALIZED:', blue2.name)
			
			assert blue2.matches_scheduled < self.matches_per_team
			assert red1.number != blue2.number
			assert red2.number != blue2.number
			assert blue1.number != blue2.number
			blue2.matches_scheduled += 1
			
			blue1.past_partners.append(blue2.number)
			blue2.past_partners.append(blue1.number)
			
			red1.past_opponents.append(blue1.number)
			red1.past_opponents.append(blue2.number)
			
			red2.past_opponents.append(blue1.number)
			red2.past_opponents.append(blue2.number)
			
			blue1.past_opponents.append(red1.number)
			blue1.past_opponents.append(red2.number)
			
			blue2.past_opponents.append(red1.number)
			blue2.past_opponents.append(red2.number)
			
			m = Match([red1, red2], [blue1, blue2], n)
			
			self.matches.append(m)
			
		return True
	
	def generate_n_teams(self, n):
		oprs = []
		
		for i in range(1, n + 1):
			t = Team(i, -1)
			self.teams.append(t)
		
		# if more than 32 teams, use worlds-like distribution
		if (n > 32):
			oprs = np.random.normal(150, 55, n)
		# if 32 > n > 24, use state-like distribution
		elif (n > 24):
			oprs = np.random.normal(125, 55, n)
		# else for smaller tournaments, use qual-like distribution
		else:
			oprs = np.random.normal(100, 55, n)
		
		oprs.sort()
		o = 0
		for t in reversed(self.teams):
			temp = int(oprs[o])
			
			# min opr is 10, max is 450
			if temp < 10: temp = 10
			if temp > 450: temp = 450
			
			t.opr = temp
			o += 1
	
	def run_tournament(self):
		for m in self.matches:
			# run_match returns True if the "ceiling" was hit. Keep track of that
			if(m.run_match()): self.ceiling_hits += 1
	
	def rank(self):
		self.teams.sort()
	
	# TODO: add rank in front of team name
	def rankings(self):
		self.rank()
		
		print('{:^20}'.format('Team Name') + '|' + '{:^6}'.format('RP') + '|' + '{:^6}'.format('TP') + '|' + '{:^4}'.format('MP') + '|' + '{:^5}'.format('OPR'))
		print('{:->20}'.format('') + '|' + '{:->6}'.format('') + '|' + '{:->6}'.format('') + '|' + '{:->4}'.format('') + '|' + '{:->5}'.format(''))
		for t in self.teams:
			print('{:20}'.format(t.name) + '|' + '{:>6}'.format(t.rp) + '|' + '{:>6}'.format(t.get_tp()) + '|' + '{:>4}'.format(t.matches_played) + '|' + '{:>5}'.format(t.opr))
		print()
	
	def stats(self):
		for m in self.matches:
			m.stats()
	
	def reset(self):
		self.matches = []
		for t in self.teams:
			t.reset()
