import options

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
	
	def __init__(self, red, blue, number=-1):
		self.red_alliance = red
		self.red1 = self.red_alliance[0]
		self.red2 = self.red_alliance[1]
		
		self.blue_alliance = blue
		self.blue1 = self.blue_alliance[0]
		self.blue2 = self.blue_alliance[1]
		
		self.match_number = number
	
	def run_match(self):
		hit_ceiling = False
		
		# compute alliance scores from point distributions
		red_score = self.red1.get_points() + self.red2.get_points()
		blue_score = self.blue1.get_points() + self.blue2.get_points()
		
		self.red1.matches_played += 1
		self.red2.matches_played += 1
		self.blue1.matches_played += 1
		self.blue2.matches_played += 1
		
		# if score "ceiling" is enabled, do additional calculations:
		#  assume each team scores at 50% efficency after the score "ceiling" is reached,
		#  so find the theoretical point in the match where the "ceiling" was reached,
		#  and give each alliance 50% of points they earned above that "ceiling"
		if (options.score_ceiling != -1):
			score_total = red_score + blue_score
			if (score_total > options.score_ceiling):
				scale_factor = options.score_ceiling / score_total
				
				# calculate theoretical score at the point in the match when the teams hit the ceiling
				temp_red = red_score * scale_factor
				temp_blue = blue_score * scale_factor
				
				# assume that after the ceiling was hit, the teams scored at some percent of their normal efficiency
				red_score = temp_red + ((red_score - temp_red) * 0.5)
				blue_score = temp_blue + ((blue_score - temp_blue) * 0.5)
				
				hit_ceiling = True
		
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
		
		return hit_ceiling
	
	def stats(self):
		print('Match number ' + str(self.match_number))
		print('Winner: ' + self.formatted_winner)
		print('Teams: ', self.red1.number, self.red2.number, self.blue1.number, self.blue2.number)
		print('Winning score: ' + str(self.win_score) + ' (teams ' + str(self.win1) + ' and ' + str(self.win2) + ')')
		print('Losing score:  ' + str(self.lose_score) + ' (teams ' + str(self.lose1) + ' and ' + str(self.lose2) + ')\n')
	
	def _give_points(self):
		if (self.winner == "tie"):
			self.red1.tie(self.win_score, self.lose_score)
			self.red2.tie(self.win_score, self.lose_score)
			self.blue1.tie(self.win_score, self.lose_score)
			self.blue2.tie(self.win_score, self.lose_score)
			return
		
		# if winner-take-all is enabled, increase the win score by a specified percentage
		#  and decrease the lose score by the same specified percentage
		# Do this here because a tie should not be affected by this
		if (options.wta_proportion is not None):
			self.win_score *= (1 + options.wta_proportion)
			self.lose_score *= (1 - options.wta_proportion)
		
		if (self.winner == "red"):
			self.red1.win(self.win_score, self.lose_score)
			self.red2.win(self.win_score, self.lose_score)
			self.blue1.lose(self.win_score, self.lose_score)
			self.blue2.lose(self.win_score, self.lose_score)
			
		else:
			self.red1.lose(self.win_score, self.lose_score)
			self.red2.lose(self.win_score, self.lose_score)
			self.blue1.win(self.win_score, self.lose_score)
			self.blue2.win(self.win_score, self.lose_score)
