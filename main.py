from Team import Team
from Tournament import Tournament

import options

import getopt, sys

import math
import random

options.init()

try:
	opts, args = getopt.getopt(sys.argv[1:], "t:m:n:r:c:w:", ["teams=", "matches=", "tournaments=", "rankings=", "ceiling=", "winner-take-all-proportion="])
except getopt.GetoptError as err:
	print(err)
	sys.exit(2)

teams = 0
matches_per_team = 0
tournaments = 0

for o, a in opts:
	if o in ('-t', '--teams'):
		teams = int(a)
	elif o in ('-m', '--matches'):
		matches_per_team = int(a)
	elif o in ('-n', '--tournaments'):
		tournaments = int(a)
	elif o in ('-r', '--rankings'):
		options.ranking_systems = a
	elif o in ('-c', '--ceiling'):
		options.score_ceiling = int(a)
	elif o in ('-w', '--winner-take-all-proportion'):
		options.wta_proportion = float(a)
	else:
		assert False, 'bad option'

assert teams > 0, 'number of teams expected but not given (-t or --teams)'
assert matches_per_team > 0, 'number of matches per team expected but not given (-m or --matches)'
assert tournaments > 0, 'number of tournaments expected but not given (-n or --tournaments)'

assert teams % 4 == 0, 'number of teams must be divisible by 4'

#assert options.ranking_system == "current" or options.ranking_system == "sum" or options.ranking_system == "yours" or options.ranking_system == "opr" or options.ranking_system == "u_plus_lose" or options.ranking_system == "inv_opr" or options.ranking_system == "random" or options.ranking_system == "new2019", 'provided ranking system not recognized, options are "current", "sum", "yours", "opr", "u_plus_lose", "inv_opr", "random", or "new2019"'

print('Running', tournaments, 'tournaments, all with', matches_per_team, 'matches each for', teams, 'teams, using the', options.ranking_systems, 'TBP method(s)')

if (options.score_ceiling != -1):
	print('Score ceiling is ENABLED and is set to', options.score_ceiling)
else:
	print('Score ceiling is DISABLED')

if (options.wta_proportion is not None):
	print('Winner-take-all is ENABLED and is set to +/-' + str(options.wta_proportion))
	if (math.fabs(options.wta_proportion) >= 1):
		print('WARNING: Winner-take-all proportion is set to', str(options.wta_proportion) + ', an absolute value greater than 100%')
	print()
else:
	print('Winner-take-all is DISABLED\n')

if (matches_per_team >= 7):
	options.subtract_second_least_match = True

teams_to_track = teams # track all teams for fairness

# keep track of sum of RMSDs for each tournament,
#  then divide by the number of tournaments at the end
#  to report the average RMSD
sum_of_RMSDs_all = 0

# keep a seperate running sum of RMSDs for the
#  top 4 teams (by input rank) for each tournament
sum_of_RMSDs_top_4 = 0

sum_of_ceiling_hits = 0

# declare eventual Tournament object outside for loop so the last tournament's values can be accessed
test_tournament = -1

for i in range(0, tournaments):
	#first_line = first_line + ',T' + str(i + 1)
	
	test_tournament = Tournament(teams, matches_per_team)
	
	while not test_tournament.create_match_schedule(): continue
	
	for ranking_system in options.ranking_systems.split(','):
		
		options.ranking_system = ranking_system
		
		random_TBP = False
		
		test_tournament.soft_reset()
		
		if not (ranking_system == "current" or ranking_system == "sum" or ranking_system == "yours" or ranking_system == "opr" or ranking_system == "u_plus_lose" or ranking_system == "inv_opr" or ranking_system == "random" or ranking_system == "new2019"):
			print('provided ranking system "' + str(ranking_system) + '" not recognized, options are "current", "sum", "yours", "opr", "u_plus_lose", "inv_opr", "random", or "new2019".\nSkipping to next ranking system...')
			continue
		
		if (ranking_system == "random"):
			# run tournament with current system to speed through the cascading if/elif in Team.py,
			#  but then assign random TBP at the end
			ranking_system = "current"
			random_TBP = True
	
		test_tournament.run_tournament()
	
		# if needed, assign random TBP
		if (random_TBP):
			for t in test_tournament.teams:
				t.tp = int(random.random() * 1000)
		
		test_tournament.rank()
		
		sum_of_squared_residuals_all = 0
		sum_of_squared_residuals_top_4 = 0
		
		for r in range(1, teams_to_track + 1):
			for t in range(len(test_tournament.teams)):
				if (test_tournament.teams[t].number == r):
					sum_of_squared_residuals_all += math.pow((t + 1) - r, 2)
					# track the first four teams in a separate sum
					if (r < 5):
						sum_of_squared_residuals_top_4 += math.pow((t + 1) - r, 2)
					break
		
		sum_of_RMSDs_all += math.sqrt(sum_of_squared_residuals_all/(teams_to_track - 1))
		sum_of_RMSDs_top_4 += math.sqrt(sum_of_squared_residuals_top_4/(4 - 1)) # use '4 - 1' instead of 3 to mirror line above
		
		sum_of_ceiling_hits += test_tournament.ceiling_hits
		
		if i == 0: print('Tournament', 1, 'done', end = '', flush = True)
		else: print('\rTournament', i + 1, 'done   ', end = '', flush = True)
		
		print('\n\nRMSD for all teams:', sum_of_RMSDs_all / tournaments)
		print('\nRMSD for top 4 teams (by OPR):', sum_of_RMSDs_top_4 / tournaments, '\n')
		if(options.score_ceiling != -1): print('Total ceiling hits / total number of matches:', sum_of_ceiling_hits / (tournaments * test_tournament.number_of_matches), '\n')
