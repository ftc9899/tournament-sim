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

assert options.ranking_system == "current" or options.ranking_system == "sum" or options.ranking_system == "yours" or options.ranking_system == "opr", 'provided ranking system not recognized, options are "current", "sum", "yours", or "opr"'

print('Running', tournaments, 'tournaments, all with', matches_per_team, 'matches each for', teams, 'teams\n')

teams_to_track = teams # track all teams for fairness

results = []
for i in range(0, teams_to_track):
	results.append([])

#results = [[1],[2],[3],[4],[5],[6],[7],[8]]
#first_line = 'Rank'

for i in range(0, tournaments):
	#first_line = first_line + ',T' + str(i + 1)
	
	test_tournament = Tournament(teams, matches_per_team)
	
	while not test_tournament.create_match_schedule(): continue
	
	test_tournament.run_tournament()
	
	test_tournament.rank()
	
	# TODO: This for loop could just loop through all the teams if
	#  all the teams will always be tracked
	for r in range(1, teams_to_track + 1):
		for t in range(len(test_tournament.teams)):
			if (test_tournament.teams[t].number == r):
				#print(str(r) + ',' + str(t + 1))
				results[r - 1].append(t + 1)
				break
	
	if i == 0: print('Tournament', 1, 'done', end = '', flush = True)
	else: print('\rTournament', i + 1, 'done   ', end = '', flush = True)

#print('\n' + first_line)

'''for i in results:
	line = ''
	for j in i:
		line = line + str(j) + ','
	print(line[:-1])'''

residuals = []

r = 1
for i in results:
	for j in i:
		residuals.append(j - r)
	r += 1

sum_of_squared_residuals = 0

for i in residuals:
	sum_of_squared_residuals += math.pow(i, 2)

RMSD = math.sqrt(sum_of_squared_residuals/((tournaments * teams_to_track) - 1))

print('\n\nRMSD for all teams:', RMSD)

residuals = []

r = 1
for i in results:
	for j in i:
		residuals.append(j - r)
	r += 1
	if r == 9: break

sum_of_squared_residuals = 0

for i in residuals:
	sum_of_squared_residuals += math.pow(i, 2)

RMSD = math.sqrt(sum_of_squared_residuals/((tournaments * 8) - 1))

print('\nRMSD for top 8 teams (by OPR):', RMSD)

residuals = []

r = 1
for i in results:
	for j in i:
		residuals.append(j - r)
	r += 1
	if r == 5: break

sum_of_squared_residuals = 0

for i in residuals:
	sum_of_squared_residuals += math.pow(i, 2)

RMSD = math.sqrt(sum_of_squared_residuals/((tournaments * 4) - 1))

print('\nRMSD for top 4 teams (by OPR):', RMSD)

'''residuals = []

r = 1
for i in results:
	for j in i:
		residuals.append(j - r)
	r += 1
	if r == 2: break

sum_of_squared_residuals = 0

for i in residuals:
	sum_of_squared_residuals += math.pow(i, 2)

RMSD = math.sqrt(sum_of_squared_residuals/((tournaments * 1) - 1))

print('\nRMSD for top team (by OPR):', RMSD)'''
