from math import sqrt

# return a distance-based similarity score for person1 and person2
def sim_distance(all_preferences, person1, person2):
	# first get the list of shared items
	shared_items = {}
	for item in all_preferences[person1]:
		if item in all_preferences[person2]:
			shared_items[item] = 1

	# if there are no shared ratings, they have a 0 similarity
	if len(shared_items) == 0: return 0

	# distance uses the sum of the squares for the difference in each shared rating
	sum_of_squares = sum([pow(all_preferences[person1][item] - all_preferences[person2][item],2)
						  for item in all_preferences[person1] if item in all_preferences[person2]])

	# return a value between 0 and 1 by adding one to the sum (to avoid div by 0) and inverting
	return 1 / (1 + sum_of_squares) 

# return a Pearson similarity score
def sim_pearson(all_preferences, person1, person2):
	shared_items = {}
	for item in all_preferences[person1]:
		if item in all_preferences[person2]: shared_items[item] = 1

	num_shared_ratings = len(shared_items)

	if num_shared_ratings == 0: return 0

	# Pearson needs sum of prefs, some of squares of prefs, and sum of products
	sum_person1 = sum([all_preferences[person1][item] for item in shared_items])
	sum_person2 = sum([all_preferences[person2][item] for item in shared_items])

	sumSq_person1 = sum([pow(all_preferences[person1][item],2) for item in shared_items])
	sumSq_person2 = sum([pow(all_preferences[person2][item],2) for item in shared_items])

	sumProducts = sum([all_preferences[person1][item]*all_preferences[person2][item] for item in shared_items])

	# now ready to finally calculate the Pearson score
	numeratorPearson = sumProducts - (sum_person1 * sum_person2 / num_shared_ratings)
	denominatorPearson = sqrt((sumSq_person1-pow(sum_person1,2)/num_shared_ratings)*(sumSq_person2-pow(sum_person2,2)/num_shared_ratings))

	if denominatorPearson == 0: return 0

	return numeratorPearson / denominatorPearson


# return the best - most similar - matches for a particular person
def top_matches(all_preferences, person, num_of_matches = 5, similarity_func = sim_pearson):
	scores = [(similarity_func(all_preferences, person, other_person),other_person) 
		for other_person in all_preferences if other_person != person]

	# sort resulting list so highest scores are first
	scores.sort()
	scores.reverse()

	return scores[0:num_of_matches]	

# get recommendations for a person using a weighted average of every other user's
# rating - so that ratings from someone that's more similar to the person hold
# more weight when determining a recommendation
def get_recommendations(all_preferences, person, similarity_func = sim_pearson):
	totals = {}
	similarity_sums = {}

	for other_person in all_preferences:
		# don't compare the person to himself
		if other_person == person: continue
		how_similar = similarity_func(all_preferences, person, other_person)

		# don't bother w/ similarity scores that are zero or less
		if how_similar <= 0: continue

		for item in all_preferences[other_person]:
			# only score movies the person hasn't seen
			if item not in all_preferences[person] or all_preferences[person][item] == 0:
				totals.setdefault(item, 0)
				totals[item] += all_preferences[other_person][item] * how_similar

				similarity_sums.setdefault(item, 0)
				similarity_sums[item] += how_similar

	# create the normalized list of recommendations
	rankings = [(total / similarity_sums[item],item) for item,total in totals.items()]

	rankings.sort()
	rankings.reverse()
	return rankings

# swap first index w/ second index, to enable matches and recommendations on the 
# second item; i.e., instead of first people and then movies (and matches and recs
# based on similar people), we'd have first movies and then people, and can get
# similarity matches and recommendations based on the similarity between movies
def swap_first_and_second_indexes(all_preferences):
	swapped_prefs = {}
	for first_item in all_preferences:
		for second_item in all_preferences[first_item]:
			swapped_prefs.setdefault(second_item,{})
			swapped_prefs[second_item][first_item] = all_preferences[first_item][second_item]

	return swapped_prefs



critics = {'Lisa Rose': {'Lady in the Water': 2.5, 
						 'Snakes on a Plane': 3.5,
						 'Just My Luck': 3.0,
						 'Superman Returns': 3.5,
						 'You, Me and Dupree': 2.5,
						 'The Night Listener': 3.0},
		   'Gene Seymour': {'Lady in the Water': 3.0, 
						 'Snakes on a Plane': 3.5,
						 'Just My Luck': 1.5,
						 'Superman Returns': 5.0,
						 'You, Me and Dupree': 3.5,
						 'The Night Listener': 3.0},
		   'Michael Phillips': {'Lady in the Water': 2.5, 
						 'Snakes on a Plane': 3.0,
						 'Superman Returns': 3.5,
						 'The Night Listener': 4.0},
		   'Claudia Puig': {'Snakes on a Plane': 3.5,
						 'Just My Luck': 3.0,
						 'Superman Returns': 4.0,
						 'You, Me and Dupree': 2.5,
						 'The Night Listener': 4.5},
		   'Mick LaSalle': {'Lady in the Water': 3.0, 
						 'Snakes on a Plane': 4.0,
						 'Just My Luck': 2.0,
						 'Superman Returns': 3.0,
						 'You, Me and Dupree': 2.5,
						 'The Night Listener': 3.0},
		   'Jack Matthews': {'Lady in the Water': 3.0, 
						 'Snakes on a Plane': 4.0,
						 'Just My Luck': 3.0,
						 'Superman Returns': 5.0,
						 'You, Me and Dupree': 3.5,
						 'The Night Listener': 3.0},
		   'Toby': {'Snakes on a Plane': 4.5, 
		   			'You, Me and Dupree': 1.0,
		   			'Superman Returns': 4.0}
		  }