from pydelicious import get_popular,get_userposts,get_urlposts
import time

# get dictionary with a bunch of users, where each user has an empty dictionary ready to be filled
def initialize_user_dict(tag, count=5):
	user_dict = {}

	# get the top counts popular posts
	for popular_URL in get_popular(tag=tag)[0:count]:
		# find all users who posted this, by looking finding the matching post and getting the user from that
		for user_popular_URL in get_urlposts(popular_URL['url']):
			user = user_popular_URL['user']
			user_dict[user] = {}

	return user_dict


def fill_user_dict_with_rated_items(user_dict):
	all_items = {}

	# find links posted by all users
	for user in user_dict:
		for i in range(3):
			try:
				posts = get_userposts(user)
				break
			except:
				print "Failed user " + user + ", retrying..."
				time.sleep(4)

		for post in posts:
			url = post['url']
			user_dict[user][url] = 1.0	# user posted this link, so use a 1 (0 means the user didn't post)
			all_items[url] = 1
	
	# now fill in missing items with 0, since no one posted those links
	for ratings in user_dict.values():
		for item in all_items:
			if item not in ratings:
				ratings[item] = 0.0	
