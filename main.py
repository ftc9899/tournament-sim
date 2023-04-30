from Team import Team
from Tournament import Tournament

import options

import getopt, sys

import math
import random

import datetime

def handle_args():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "t:m:n:r:c:w:", ["teams=", "matches=", "tournaments=", "ranking=", "ceiling=", "winner-take-all-proportion="])
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)

	for o, a in opts:
		if o in ('-t', '--teams'):
			teams = int(a)
		elif o in ('-m', '--matches'):
			matches_per_team = int(a)
		elif o in ('-n', '--tournaments'):
			tournaments = int(a)
		elif o in ('-r', '--ranking'):
			options.ranking_system = a
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

	assert options.ranking_system == "current" or options.ranking_system == "sum" or options.ranking_system == "yours" or options.ranking_system == "opr" or options.ranking_system == "u_plus_lose" or options.ranking_system == "inv_opr" or options.ranking_system == "random" or options.ranking_system == "new2019", 'provided ranking system not recognized, options are "current", "sum", "yours", "opr", "u_plus_lose", "inv_opr", "random", or "new2019"'

	print('Running', tournaments, 'tournaments, all with', matches_per_team, 'matches each for', teams, 'teams, using the', options.ranking_system, 'TBP method')

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
	
	random_TBP = False
	if (options.ranking_system == "random"):
		# run tournament with current system to speed through the cascading if/elif in Team.py,
		#  but then assign random TBP at the end
		options.ranking_system = "current"
		random_TBP = True

	if (matches_per_team >= 7):
		options.subtract_second_least_match = True
	
	return teams, matches_per_team, tournaments, random_TBP

def main():

	options.init()

	number_of_teams, matches_per_team, tournaments, random_TBP = handle_args()

	# keep track of sum of RMSDs for each tournament,
	#  then divide by the number of tournaments at the end
	#  to report the average RMSD
	sum_of_RMSDs_all_teams = 0

	# keep a seperate running sum of RMSDs for the
	#  top 4 teams (by input rank) for each tournament
	sum_of_RMSDs_top_4_teams = 0

	total_ceiling_hits = 0

	# declare eventual Tournament object outside for loop so the last tournament's values can be accessed
	test_tournament = -1

	# start execution time timer
	start = datetime.datetime.now()

	for i in range(0, tournaments):
		test_tournament = Tournament(number_of_teams, matches_per_team)

		while not test_tournament.create_match_schedule(): continue

		test_tournament.run_tournament()

		# if needed, assign random TBP
		if (random_TBP):
			for t in test_tournament.teams:
				t.tp = int(random.random() * 1000)

		# sort the tournament's list of teams based on their match performance and the specified ranking system
		test_tournament.rank()

		sum_of_squared_residuals_all = 0
		sum_of_squared_residuals_top_4 = 0

		for t in range(number_of_teams):
			expected_rank = test_tournament.teams[t].number

			squared_residual = math.pow((t + 1) - expected_rank, 2)
			sum_of_squared_residuals_all += squared_residual
			
			# track the first four teams in a separate sum
			if (expected_rank < 5):
				sum_of_squared_residuals_top_4 += squared_residual
				
		sum_of_RMSDs_all_teams += math.sqrt(sum_of_squared_residuals_all/(number_of_teams - 1))
		sum_of_RMSDs_top_4_teams += math.sqrt(sum_of_squared_residuals_top_4/(4 - 1)) # use '4 - 1' instead of 3 to mirror line above

		total_ceiling_hits += test_tournament.ceiling_hits
	
	# stop execution time timer
	end = datetime.datetime.now()

	execution_time = end - start
	# assume execution_time.days is 0
	print('execution time:', execution_time.seconds + (execution_time.microseconds / 1e6), 'seconds')

	print('RMSD for all teams:', sum_of_RMSDs_all_teams / tournaments)
	print('RMSD for top 4 teams (by OPR):', sum_of_RMSDs_top_4_teams / tournaments)
	if(options.score_ceiling != -1):
		print('\nTotal ceiling hits / total number of matches:', total_ceiling_hits / (tournaments * test_tournament.number_of_matches), '\n')

if (__name__ == "__main__"):
	main()