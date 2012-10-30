from math import sqrt

# return a distance-based similarity score for two items
def sim_distance(all_preferences, item1, item2):
	# first get the list of shared items
	shared_items = {}
	for item in all_preferences[item1]:
		if item in all_preferences[item2]:
			shared_items[item] = 1

	# if there are no shared ratings, they have a 0 similarity
	if len(shared_items) == 0: return 0

	# distance uses the sum of the squares for the difference in each shared rating
	sum_of_squares = sum([pow(all_preferences[item1][item] - all_preferences[item2][item],2)
						  for item in all_preferences[item1] if item in all_preferences[item2]])

	# return a value between 0 and 1 by adding one to the sum (to avoid div by 0) and inverting
	return 1 / (1 + sum_of_squares) 

# return a Pearson similarity score
def sim_pearson(all_preferences, item1, item2):
	shared_items = {}
	for item in all_preferences[item1]:
		if item in all_preferences[item2]: shared_items[item] = 1

	num_shared_ratings = len(shared_items)

	if num_shared_ratings == 0: return 0

	# Pearson needs sum of prefs, some of squares of prefs, and sum of products
	sum_item1 = sum([all_preferences[item1][item] for item in shared_items])
	sum_item2 = sum([all_preferences[item2][item] for item in shared_items])

	sumSq_item1 = sum([pow(all_preferences[item1][item],2) for item in shared_items])
	sumSq_item2 = sum([pow(all_preferences[item2][item],2) for item in shared_items])

	sumProducts = sum([all_preferences[item1][item]*all_preferences[item2][item] for item in shared_items])

	# now ready to finally calculate the Pearson score
	numeratorPearson = sumProducts - (sum_item1 * sum_item2 / num_shared_ratings)
	denominatorPearson = sqrt((sumSq_item1-pow(sum_item1,2)/num_shared_ratings)*(sumSq_item2-pow(sum_item2,2)/num_shared_ratings))

	if denominatorPearson == 0: return 0

	return numeratorPearson / denominatorPearson


# Return the best - most similar - first-level item matches for a specified first-level item.
# If the all_preferences dict is set up with users as first-level items and
# items (products, say) as second-level items, then this function returns the most similar users;
# if that same all_preferences dict is transformed so items/products are the first-level
# items, then this function returns the items most similar to the specified item.
def most_similar_first_level_items(all_preferences, first_level_item_to_match, num_of_matches = 5, similarity_func = sim_pearson):
	scores = [(similarity_func(all_preferences, first_level_item_to_match, other_first_level_item), other_first_level_item) 
		for other_first_level_item in all_preferences if other_first_level_item != first_level_item_to_match]

	# sort resulting list so highest scores are first
	scores.sort()
	scores.reverse()

	return scores[0:num_of_matches]	

# Return the best/most similar second-level items for a specified first-level item.
# If the all_preferences dict is set up with users as first-level items and items/products
# as second-level items, this function returns the items/products (i.e., second-level items)
# that are most likely to be interesting to the user. 
# It does this using a weighted average of every other user's  ratings, so that ratings 
# from users that are more similar to the specified person (first-level item) hold
# more weight when determining the recommendation.
def most_similar_second_level_items(all_preferences, first_level_item, similarity_func = sim_pearson):
	totals = {}
	similarity_sums = {}

	for other_first_level_item in all_preferences:
		# don't compare the first-level item to the same first-level item
		if other_first_level_item == first_level_item: continue
		how_similar = similarity_func(all_preferences, first_level_item, other_first_level_item)

		# don't bother w/ similarity scores that are zero or less
		if how_similar <= 0: continue

		for second_level_item in all_preferences[other_first_level_item]:
			# only score second-level items the first-level item hasn't rated
			if second_level_item not in all_preferences[first_level_item] or all_preferences[first_level_item][second_level_item] == 0:
				totals.setdefault(second_level_item, 0)
				totals[second_level_item] += all_preferences[other_first_level_item][second_level_item] * how_similar

				similarity_sums.setdefault(second_level_item, 0)
				similarity_sums[second_level_item] += how_similar

	# create the normalized list of recommendations
	rankings = [(total / similarity_sums[second_level_item],second_level_item) for second_level_item,total in totals.items()]

	rankings.sort()
	rankings.reverse()
	return rankings

# Swap first index w/ second index, to enable matches and recommendations on the 
# second-level item; i.e., instead of first people and then movies (and matches and recs
# based on similar people), we'd have first movies and then people, and can get
# similarity matches and recommendations based on the similarity between movies.
def swap_first_and_second_indexes(all_preferences):
	swapped_prefs = {}
	for first_level_item in all_preferences:
		for second_level_item in all_preferences[first_level_item]:
			swapped_prefs.setdefault(second_level_item,{})
			swapped_prefs[second_level_item][first_level_item] = all_preferences[first_level_item][second_level_item]

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