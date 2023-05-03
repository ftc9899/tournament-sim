from Tournament import Tournament

import options

import getopt, sys
import math
import datetime

SUPPORTED_RANKING_SYSTEMS = ['current', 'sum', 'yours', 'opr', 'u_plus_lose', 'inv_opr', 'random', 'new2019']

def handle_args():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "t:m:n:r:c:w:", ["teams=", "matches=", "tournaments=", "rankings=", "ceiling=", "winner-take-all-proportion="])
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
		elif o in ('-r', '--rankings'):
			options.ranking_systems = a.split(',')
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

	for ranking_system in options.ranking_systems:
		if ranking_system not in SUPPORTED_RANKING_SYSTEMS:
			print('skipping ranking system "' + ranking_system + '", not recognized')
			options.ranking_systems.remove(ranking_system)

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
		print('Winner-take-all is DISABLED')

	if (matches_per_team >= 7):
		options.subtract_second_least_match = True
	
	return teams, matches_per_team, tournaments

def main():

	#options.init()

	number_of_teams, matches_per_team, tournaments = handle_args()

	# keep track of sum of RMSDs for each tournament,
	#  then divide by the number of tournaments at the end
	#  to report the average RMSD
	sum_of_RMSDs_all_teams = {}

	# keep a seperate running sum of RMSDs for the
	#  top 4 teams (by input rank) for each tournament
	sum_of_RMSDs_top_4_teams = {}

	total_ceiling_hits = {}

	# initialize lists to track the sum of RMSDs outside the main nested loop
	for ranking_system in options.ranking_systems:
		sum_of_RMSDs_all_teams[ranking_system] = 0
		sum_of_RMSDs_top_4_teams[ranking_system] = 0
		total_ceiling_hits[ranking_system] = 0

	# declare eventual Tournament object outside for loop so the last tournament's values can be accessed
	test_tournament = None

	# keep track of time spent scheduling
	time_spent_scheduling = datetime.timedelta(0)

	# start execution time timer
	start = datetime.datetime.now()

	#scheduling_restarts = 0

	for i in range(0, tournaments):
		test_tournament = Tournament(number_of_teams, matches_per_team)

		schedule_creation_start = datetime.datetime.now()

		while not test_tournament.create_match_schedule(): continue #scheduling_restarts += 1

		time_spent_scheduling += datetime.datetime.now() - schedule_creation_start

		#test_tournament.report_scheduling_failures()

		test_tournament.run_tournament()

		for ranking_system in options.ranking_systems:

			options.current_ranking_system = ranking_system

			test_tournament.reassign_tbp()
			
			if ranking_system == 'new2019':
				for t in test_tournament.teams:
					t.tp -= t.least_tp
					if (options.subtract_second_least_match): t.tp -= t.second_least_tp

			test_tournament.rank()

			sum_of_squared_residuals_all = 0
			sum_of_squared_residuals_top_4 = 0

			for t in range(number_of_teams):
				expected_rank = test_tournament.teams[t].number

				squared_residual = math.pow((t + 1) - expected_rank, 2)
				sum_of_squared_residuals_all += squared_residual
				
				# track the first four teams in an additional separate sum
				if (expected_rank < 5):
					sum_of_squared_residuals_top_4 += squared_residual

			sum_of_RMSDs_all_teams[ranking_system] += math.sqrt(sum_of_squared_residuals_all/(number_of_teams - 1))
			sum_of_RMSDs_top_4_teams[ranking_system] += math.sqrt(sum_of_squared_residuals_top_4/(4 - 1)) # use '4 - 1' instead of 3 to mirror line above

			total_ceiling_hits[ranking_system] += test_tournament.ceiling_hits

	# stop execution time timer
	end = datetime.datetime.now()
	
	for system in options.ranking_systems:
		print("\nResults for '" + system + "' ranking system:")
	
		print('\nRMSD for all teams:', sum_of_RMSDs_all_teams.get(system) / tournaments)
		print('RMSD for top 4 teams (by OPR):', sum_of_RMSDs_top_4_teams.get(system) / tournaments)
		if(options.score_ceiling != -1):
			print('Total ceiling hits / total number of matches:', total_ceiling_hits.get(system) / (tournaments * test_tournament.number_of_matches))

	execution_time = end - start
	# assume execution_time.days is 0
	human_readable_execution_time = execution_time.seconds + (execution_time.microseconds / 1e6)
	print('\nexecution time: %0.6f seconds' % (human_readable_execution_time))

	time_spent_scheduling = time_spent_scheduling.seconds + (time_spent_scheduling.microseconds / 1e6)
	print('scheduling time was %0.3f %% of execution time' % ((time_spent_scheduling / human_readable_execution_time) * 100))
	#print('total scheduling restarts:', scheduling_restarts)

if (__name__ == "__main__"):
	main()