from Team import Team
from Match import Match

import options

import random
import numpy as np

class Tournament:
	
	matches_per_team = 0
	number_of_matches = 0
	
	ceiling_hits = 0
	
	def __init__(self, teams, matches_per_team):

		# tunable parameter added to the current match number that the scheduler is trying to schedule
		#  during refactoring, all scheduling resets happened when scheduling the last four matches
		#  however, some failures (i.e. picking a blue team that is already on the match's red alliance)
		#  can happen at any point in the scheduling process
		self.BASE_FAILURE_RESILIENCE = 5
		'''self.red1_failures = []
		self.red2_failures = []
		self.blue1_failures = []
		self.blue2_failures = []'''

		# set up the array of teams, which will also keep track of rankings
		self.teams = []
		if isinstance(teams, int):
			self.generate_n_teams(teams)
		else:
			self.teams = teams
		
		self.rank()
		self.matches_per_team = matches_per_team
		#TODO: check that with the number of teams given, the requested amount of
		#       matches per team can be played without conflicts'''
		
		self.number_of_matches = self.calculate_number_of_matches(len(self.teams), matches_per_team)
		
		self.matches = []
	
	def calculate_number_of_matches(self, t, m):
		return t * m // 4
	
	def create_match_schedule(self):
		# use a list of teams that have not yet been scheduled for all of their matches
		#  when a team is scheduled for its final match, remove it from this list
		#  .copy is used so thet the original list is not modified
		available_teams = self.teams.copy()

		for n in range(1, self.number_of_matches + 1):
			red1 = random.choice(available_teams)
			
			failures = 0
			
			'''while (red1.matches_scheduled >= self.matches_per_team):
				#print('red1:  ' + red1.name + ' has already been scheduled for ' + str(red1.matches_scheduled) + ' matches')
				failures += 1
				if failures > self.FAILURE_RESILIENCE:
					self.reset()
					return False
				red1 = random.choice(available_teams)
			#print('red1  FINALIZED:', red1.name)'''
			
			assert red1.matches_scheduled < self.matches_per_team
			red1.matches_scheduled += 1
			if (red1.matches_scheduled == self.matches_per_team): available_teams.remove(red1)
			#self.red1_failures.append(failures)
			
			red2 = random.choice(available_teams)
			
			failures = 0
			
			# check that there is such a team before entering the while loop
			#while (red2.matches_scheduled >= self.matches_per_team or red2.number in red1.past_partners):
			while (red2.number in red1.past_partners):
				'''if (red2.matches_scheduled >= self.matches_per_team):
					print('red2:  ' + red2.name + ' has already been scheduled for ' + str(red2.matches_scheduled) + ' matches')
				else:
					print('red2:  ' + red2.name + ' has already partnered with ' + red1.name)'''
				failures += 1
				if failures > self.BASE_FAILURE_RESILIENCE + n:
					self.reset()
					return False
				red2 = random.choice(available_teams)
			#print('red2  FINALIZED:', red2.name)
			
			assert red2.matches_scheduled < self.matches_per_team
			assert red1.number != red2.number
			red2.matches_scheduled += 1
			if (red2.matches_scheduled == self.matches_per_team): available_teams.remove(red2)
			#self.red2_failures.append(failures)
			
			red1.past_partners.append(red2.number)
			red2.past_partners.append(red1.number)
			
			blue1 = random.choice(available_teams)
			
			failures = 0
			
			# check that there is such a team before entering the while loop
			#while (blue1.matches_scheduled >= self.matches_per_team or blue1.number in red1.past_opponents or blue1.number in red2.past_opponents):
			while (blue1.number in red1.past_opponents or blue1.number in red2.past_opponents):
				'''if (blue1.matches_scheduled >= self.matches_per_team):
					print('blue1: ' + blue1.name + ' has already been scheduled for ' + str(blue1.matches_scheduled) + ' matches')
				elif (blue1.number in red1.past_opponents):
					print('blue1: ' + blue1.name + ' has already played against ' + red1.name)
				else:
					print('blue1: ' + blue1.name + ' has already played against ' + red2.name)'''
				failures += 1
				if failures > self.BASE_FAILURE_RESILIENCE + n:
					self.reset()
					return False
				blue1 = random.choice(available_teams)
			#print('blue1 FINALIZED:', blue1.name)
			
			assert blue1.matches_scheduled < self.matches_per_team
			assert red1.number != blue1.number
			assert red2.number != blue1.number
			blue1.matches_scheduled += 1
			if (blue1.matches_scheduled == self.matches_per_team): available_teams.remove(blue1)
			#self.blue1_failures.append(failures)
			
			blue2 = random.choice(available_teams)
			
			failures = 0
			
			#while (blue2.matches_scheduled >= self.matches_per_team or blue2.number in red1.past_opponents or blue2.number in red2.past_opponents or blue2.number in blue1.past_partners):
			while (blue2.number in red1.past_opponents or blue2.number in red2.past_opponents or blue2.number in blue1.past_partners):
				'''if (blue2.matches_scheduled >= self.matches_per_team):
					print('blue2: ' + blue2.name + ' has already been scheduled for ' + str(blue2.matches_scheduled) + ' matches')
				elif (blue2.number in red1.past_opponents):
					print('blue2: ' + blue2.name + ' has already played against ' + red1.name)
				elif (blue2.number in red2.past_opponents):
					print('blue2: ' + blue2.name + ' has already played against ' + red2.name)
				else:
					print('blue2: ' + blue2.name + ' has already partnered with ' + blue1.name)'''
				failures += 1
				if failures > self.BASE_FAILURE_RESILIENCE + n:
					self.reset()
					return False
				blue2 = random.choice(available_teams)
			#print('blue2 FINALIZED:', blue2.name)
			
			assert blue2.matches_scheduled < self.matches_per_team
			assert red1.number != blue2.number
			assert red2.number != blue2.number
			assert blue1.number != blue2.number
			blue2.matches_scheduled += 1
			if (blue2.matches_scheduled == self.matches_per_team): available_teams.remove(blue2)
			#self.blue2_failures.append(failures)
			
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

		#self.report_scheduling_failures()

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
		
		# set up for loop below
		oprs.sort()
		o = 0

		# assign highest opr to lowest team number, etc.
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
	
	# mostly used by create_match_schedule to restart schedule generation if it gets stuck
	def reset(self):
		#print('failure while creating match', len(self.matches) + 1, 'of', self.number_of_matches)
		#self.report_scheduling_failures()

		self.ceiling_hits = 0
		self.matches = []
		for t in self.teams:
			t.reset()
		
		'''self.red1_failures = []
		self.red2_failures = []
		self.blue1_failures = []
		self.blue2_failures = []'''
	
	'''def reassign_tbp(self):
		if options.current_ranking_system == 'random':
			for t in self.teams:
				t.tp = int(random.random() * 1000)
			return
		
		for t in self.teams:
			t.reset_tbp()

		for m in self.matches:
			m.reassign_tbp()'''
	
	def reassign_tbp(self, ranking_system = None):
		if ranking_system == None: ranking_system = options.current_ranking_system

		if ranking_system == 'random':
			for t in self.teams:
				t.tp = int(random.random() * 1000)
			return
		
		for t in self.teams:
			t.reset_tbp()

		for m in self.matches:
			m.reassign_tbp(ranking_system)

	def report_scheduling_failures(self):
		pass
		'''print('red1 failures: ', self.red1_failures)
		print('red2 failures: ', self.red2_failures)
		print('blue1 failures:', self.blue1_failures)
		print('blue2 failures:', self.blue2_failures)'''