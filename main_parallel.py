from Tournament import Tournament

import options

import getopt, sys
import math
import datetime

import multiprocessing as mp

SUPPORTED_RANKING_SYSTEMS = ['current', 'sum', 'yours', 'opr', 'u_plus_lose', 'inv_opr', 'random', 'new2019']

NUMBER_OF_THREADS = 4

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
			print('-r and --rankings are temporarily disabled\nedit ranking systems in options.py in the meantime\n')
			#options.ranking_systems = a.split(',')
		elif o in ('-c', '--ceiling'):
			print('-c and --ceiling are temporarily disabled as ceiling hits are not being computed correctly\n')
			#options.score_ceiling = int(a)
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

def run_one_tournament(number_of_teams, matches_per_team):
	sum_of_squared_residuals_all_list = {}
	sum_of_squared_residuals_top_4_list = {}

	tournament = Tournament(number_of_teams, matches_per_team)
	
	while not tournament.create_match_schedule(): continue
	
	tournament.run_tournament()

	for ranking_system in options.ranking_systems:

		tournament.reassign_tbp(ranking_system)

		# if the current system is new2019,
		#  tournament.rank has no way to tell the list sorting algorithm
		#  to modify each team's tiebreaker points
		if ranking_system == 'new2019':
			for t in tournament.teams:
				t.tp -= t.least_tp
				if (options.subtract_second_least_match): t.tp -= t.second_least_tp

		tournament.rank()

		sum_of_squared_residuals_all = 0
		sum_of_squared_residuals_top_4 = 0

		for t in range(number_of_teams):
			expected_rank = tournament.teams[t].number

			squared_residual = math.pow((t + 1) - expected_rank, 2)
			sum_of_squared_residuals_all += squared_residual
				
			# track the first four teams in an additional separate sum
			if (expected_rank < 5):
				sum_of_squared_residuals_top_4 += squared_residual
		
		#print(ranking_system, sum_of_squared_residuals_all)
		sum_of_squared_residuals_all_list[ranking_system] = sum_of_squared_residuals_all
		sum_of_squared_residuals_top_4_list[ranking_system] = sum_of_squared_residuals_top_4
	
	return (sum_of_squared_residuals_all_list, sum_of_squared_residuals_top_4_list, tournament.ceiling_hits, number_of_teams)

def accumulate_results(args):
	global active_workers

	sum_of_squared_residuals_all, sum_of_squared_residuals_top_4, ceiling_hits, number_of_teams = args

	#print('trying to get results from a tournament')

	for ranking_system in options.ranking_systems:
		collection_of_RMSDs_all_teams[ranking_system].put(math.sqrt(sum_of_squared_residuals_all[ranking_system]/(number_of_teams - 1)))
		collection_of_RMSDs_top_4_teams[ranking_system].put(math.sqrt(sum_of_squared_residuals_top_4[ranking_system]/(4 - 1))) # use '4 - 1' instead of 3 to mirror line above

		collection_of_ceiling_hits[ranking_system].put(ceiling_hits)
	
	active_workers -= 1

	#print('got results from a tournament')

def main():
	global collection_of_RMSDs_all_teams, collection_of_RMSDs_top_4_teams, collection_of_ceiling_hits, active_workers

	#options.init()

	number_of_teams, matches_per_team, tournaments = handle_args()

	# keep track of sum of RMSDs for each tournament,
	#  then divide by the number of tournaments at the end
	#  to report the average RMSD
	collection_of_RMSDs_all_teams = {}

	# keep a seperate running sum of RMSDs for the
	#  top 4 teams (by input rank) for each tournament
	collection_of_RMSDs_top_4_teams = {}

	collection_of_ceiling_hits = {}
	total_ceiling_hits = {}

	# initialize lists to track the sum of RMSDs outside the main nested loop
	for ranking_system in options.ranking_systems:
		collection_of_RMSDs_all_teams[ranking_system] = mp.Queue()
		collection_of_RMSDs_top_4_teams[ranking_system] = mp.Queue()
		collection_of_ceiling_hits[ranking_system] = mp.Queue()
		total_ceiling_hits[ranking_system] = 0

	# start execution time timer
	start = datetime.datetime.now()

	p = mp.Pool(NUMBER_OF_THREADS)

	i = 0
	active_workers = 0

	while True:
		while i < tournaments and active_workers < NUMBER_OF_THREADS:
			result = p.apply_async(func=run_one_tournament, args=(number_of_teams, matches_per_team), callback=accumulate_results)
			active_workers += 1
			i += 1
		
		#print('all workers are busy')
		#print(i == tournaments)

		if active_workers > 0:
			try:
				result.get()
			except mp.context.TimeoutError:
				pass
		else:
			active_workers = 0
			if i == tournaments:
				break

	average_RMSD_all_teams = {}
	average_RMSD_top_4_teams = {}

	for system in options.ranking_systems:
		total_all_teams = 0
		total_top_4_teams = 0

		# all these queues should be the same size
		while not collection_of_RMSDs_all_teams[system].empty():
			total_all_teams += collection_of_RMSDs_all_teams[system].get()
			total_top_4_teams += collection_of_RMSDs_top_4_teams[system].get()
			total_ceiling_hits[system] += collection_of_ceiling_hits[system].get()
		
		average_RMSD_all_teams[system] = total_all_teams / tournaments
		average_RMSD_top_4_teams[system] = total_top_4_teams / tournaments
	
	# stop execution time timer
	end = datetime.datetime.now()
	
	for system in options.ranking_systems:
		print("\nResults for '" + system + "' ranking system:")
	
		print('\nRMSD for all teams:', average_RMSD_all_teams[system])
		print('RMSD for top 4 teams (by OPR):', average_RMSD_top_4_teams[system])
		if(options.score_ceiling != -1):
			#total_number_of_matches = tournaments * Tournament.calculate_number_of_matches(number_of_teams, matches_per_team)
			total_number_of_matches = tournaments * number_of_teams * matches_per_team // 4
			print('Total ceiling hits / total number of matches:', total_ceiling_hits[system] / total_number_of_matches)

	execution_time = end - start
	# assume execution_time.days is 0
	human_readable_execution_time = execution_time.seconds + (execution_time.microseconds / 1e6)
	print('\nexecution time: %0.6f seconds' % (human_readable_execution_time))

	#time_spent_scheduling = time_spent_scheduling.seconds + (time_spent_scheduling.microseconds / 1e6)
	#print('scheduling time was %0.3f %% of execution time' % ((time_spent_scheduling / human_readable_execution_time) * 100))
	#print('total scheduling restarts:', scheduling_restarts)

if (__name__ == "__main__"):
	main()