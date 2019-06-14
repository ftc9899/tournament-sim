from Team import Team
from Tournament import Tournament

import options

import getopt, sys

import math

options.init()

try:
	opts, args = getopt.getopt(sys.argv[1:], "t:m:n:r:", ["teams=", "matches=", "tournaments=", "ranking="])
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
	elif o in ('-r', '--ranking'):
		options.ranking_system = a
	else:
		assert False, 'bad option'

assert teams > 0, 'number of teams expected but not given (-t or --teams)'
assert matches_per_team > 0, 'number of matches per team expected but not given (-m or --matches)'
assert tournaments > 0, 'number of tournaments expected but not given (-n or --tournaments)'

assert teams % 4 == 0, 'number of teams must be divisible by 4'

assert options.ranking_system == "current" or options.ranking_system == "sum" or options.ranking_system == "yours" or options.ranking_system == "opr" or options.ranking_system == "u_plus_lose", 'provided ranking system not recognized, options are "current", "sum", "yours", "opr", or "u_plus_lose"'

print('Running', tournaments, 'tournaments, all with', matches_per_team, 'matches each for', teams, 'teams\n')

teams_to_track = teams # track all teams for fairness

results = []
for i in range(0, teams_to_track):
	results.append([])

# keep track of sum of RMSDs for each tournament,
#  then divide by the number of tournaments at the end
#  to report the average RMSD
sum_of_RMSDs = 0

for i in range(0, tournaments):
	#first_line = first_line + ',T' + str(i + 1)
	
	test_tournament = Tournament(teams, matches_per_team)
	
	while not test_tournament.create_match_schedule(): continue
	
	test_tournament.run_tournament()
	
	test_tournament.rank()
	
	sum_of_squared_residuals = 0
	
	for r in range(1, teams_to_track + 1):
		for t in range(len(test_tournament.teams)):
			if (test_tournament.teams[t].number == r):
				sum_of_squared_residuals += math.pow((t + 1) - r, 2)
	
	sum_of_RMSDs += math.sqrt(sum_of_squared_residuals/(teams_to_track - 1))
	
	# TODO: This for loop could just loop through all the teams if
	#  all the teams will always be tracked
	for r in range(1, teams_to_track + 1):
		for t in range(len(test_tournament.teams)):
			if (test_tournament.teams[t].number == r):
				results[r - 1].append(t + 1)
				break
	
	if i == 0: print('Tournament', 1, 'done', end = '', flush = True)
	else: print('\rTournament', i + 1, 'done   ', end = '', flush = True)

print('\n\nRMSD for all teams:', sum_of_RMSDs / tournaments)
