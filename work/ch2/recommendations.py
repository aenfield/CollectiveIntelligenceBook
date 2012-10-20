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
		   			'Superman Returns:': 4.0}
		  }