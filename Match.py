class Match:
	
	red_score = -1
	red1 = -1; red2 = -1
	blue_score = -1
	blue1 = -1; blue2 = -1
	
	winner = "none"
	formatted_winner = "none"
	win1 = -1
	win2 = -1
	lose1 = -1
	lose2 = -1
	
	match_number = -1;
	
	win_score = -1
	lose_score = -1
	
	def __init__(self, red, blue, nu=-1):
		self.red_alliance = red
		self.red1 = self.red_alliance[0]
		self.red2 = self.red_alliance[1]
		
		self.blue_alliance = blue
		self.blue1 = self.blue_alliance[0]
		self.blue2 = self.blue_alliance[1]
		
		self.match_number = nu
	
	def run_match(self):
		# compute alliance scores from point distributions
		red_score = self.red1.get_points() + self.red2.get_points()
		blue_score = self.blue1.get_points() + self.blue2.get_points()
		
		self.red1.matches_played += 1
		self.red2.matches_played += 1
		self.blue1.matches_played += 1
		self.blue2.matches_played += 1
		
		if (red_score > blue_score):
			self.winner = "red"
			self.formatted_winner = "\x1b[41;38mred\x1b[0m"
			
			self.win1 = self.red1.number; self.win2 = self.red2.number
			self.lose1 = self.blue1.number; self.lose2 = self.blue2.number
			
			self.win_score = red_score
			self.lose_score = blue_score
		
		elif (red_score < blue_score):
			self.winner = "blue"
			self.formatted_winner = "\x1b[44;38mblue\x1b[0m"
			
			self.win1 = self.blue1.number; self.win2 = self.blue2.number
			self.lose1 = self.red1.number; self.lose2 = self.red2.number
			
			self.win_score = blue_score
			self.lose_score = red_score
		
		else:
			self.winner = "tie"
			self.formatted_winner = "tie"
			
			self.win1 = self.red1.number; self.win2 = self.red2.number
			self.lose1 = self.blue1.number; self.lose2 = self.blue2.number
			
			self.win_score = red_score
			self.lose_score = blue_score # sorry, blue
		
		# assign rp and tp given the result of the match
		self._give_points()
	
	def stats(self):
		print('Match number ' + str(self.match_number))
		print('Winner: ' + self.formatted_winner)
		print('Teams: ', self.red1.number, self.red2.number, self.blue1.number, self.blue2.number)
		print('Winning score: ' + str(self.win_score) + ' (teams ' + str(self.win1) + ' and ' + str(self.win2) + ')')
		print('Losing score:  ' + str(self.lose_score) + ' (teams ' + str(self.lose1) + ' and ' + str(self.lose2) + ')\n')
	
	def _give_points(self):
		if (self.winner == "red"):
			self.red1.win(self.win_score, self.lose_score)
			self.red2.win(self.win_score, self.lose_score)
			self.blue1.lose(self.win_score, self.lose_score)
			self.blue2.lose(self.win_score, self.lose_score)
			
		elif (self.winner == "blue"):
			self.red1.lose(self.win_score, self.lose_score)
			self.red2.lose(self.win_score, self.lose_score)
			self.blue1.win(self.win_score, self.lose_score)
			self.blue2.win(self.win_score, self.lose_score)
			
		else:
			self.red1.tie(self.win_score, self.lose_score)
			self.red2.tie(self.win_score, self.lose_score)
			self.blue1.tie(self.win_score, self.lose_score)
			self.blue2.tie(self.win_score, self.lose_score)
