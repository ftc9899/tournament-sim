def init():
	global ranking_system
	ranking_system = "current"
	
	global score_ceiling
	score_ceiling = -1
	
	# wta_proportion stands for winner-take-all proportion
	global wta_proportion
	wta_proportion = None
	
	# if matches_per_team is 7 or more, this will be set to True
	global subtract_second_least_match
	subtract_second_least_match = False
