from yelpapi import YelpAPI
import os
# import json
from pprint import pprint
import os


YELP_CONSUMER_KEY = os.environ.get("YELP_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
TOKEN = os.environ.get("TOKEN")
TOKEN_SECRET = os.environ.get("TOKEN_SECRET")


yelp_api = YelpAPI(YELP_CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)

# results = yelp_api.search_query(location = "San Francisco", term = "restaurant", category_fitler = "italian")
# resto_results = yelp_api.search_query(location = "San Francisco", term = "restaurant", limit = 20) #this is the original query

# resto_results = yelp_api.search_query(location = "San Francisco", term = "restaurant", sort = 1, limit = 20) #this returns 20 list of businesses with mixed categories

# park_results = yelp_api.search_query(location = "San Francisco", term = "parks", sort = 1, limit = 20)


#it worked!!)@(&!)@(*#&)(!*&@#)(!@&#)
#pprint(hotels_results) prints a clean version of the json file from the
#hotels_results query

location = ""
term = ""
category_fitler = ""
limit = 0


class Category(object):
	RESTAURANT = "restaurants"
	MUSEUM = "museums"
	HOTELS = "hotels"
	NIGHTLIFE = "nightlife"
	FESTIVALS = "festivals"



def search_attractions(location, term="tourist attraction"):
	"""Search by city or country and get top tourist attraction list"""	

	search_result = yelp_api.search_query(location=location, term=term, limit=6)

	return search_result['businesses']




def search_hotels(location, term="HOTELS"):
	"""Search by city or country and get top hotels"""	

	hotels_result = yelp_api.search_query(location=location, term=term, limit=6)

	return hotels_result['businesses']



def search_restaurants(location, term="RESTAURANT"):
	"""Search by city or country and get top restaurants"""	

	restaurants_result = yelp_api.search_query(location=location, term=term, limit=6)

	return restaurants_result['businesses']



def search_museums(location, term="MUSEUM"):
	"""Search by city or country and get top museums"""	

	museums_result = yelp_api.search_query(location=location, term=term, limit=6)

	return museums_result['businesses']




def search_festivals(location, term="FESTIVALS"):
	"""Search by city or country and get top festivals"""	

	festivals_result = yelp_api.search_query(location=location, term=term, limit=6)

	return festivals_result['businesses']






### function below are no longer needed. ###



def search_places(query, location, categories=None):
	"""Searches places based on the query. Optionally, can accept a location and
	categories to filter by

	Returns a list of places"""

	if categories:
		categories = ",".join(categories)
	query = yelp_api.search_query(term=query, location = location, category_filter=categories)

 	return query['businesses']
	


def search_city(location, category = "restaurant", limit = 20, offset = 20):
	"""A function that takes on a city and query YELP api filtered by restaurant"""

	resto_results = yelp_api.search_query(location = location, category = category, limit = limit, offset=offset)

	for business in resto_results['businesses']:
		resto_name = business['name']
		# resto_location = business['name']['location']
		print resto_name
	return resto_results['businesses']
 
	#two categories, pass to route ---> jinja (for loops)

def search_parks(location, category= "parks", term = "parks", limit = 20, offset = 20):
	"""This function returns list of parks based on location"""
	park_results = yelp_api.search_query(location = location, category= category, term = term, limit = limit, offset=offset)

	for business in park_results['businesses']:
		park_name = business['name']
		print park_name

	return park_results['businesses']




# def search_hotels(location, category= "hotels", term = "hotels", limit = 20, offset = 20):
# 	"""This function returns list of hotels based on location"""
# 	hotels_results = yelp_api.search_query(location = location, category= category, term = term, limit = limit, offset=offset)

# 	for business in hotels_results['businesses']:
# 		if business in hotels_results['businesses']:
# 			hotel_name = business['name']
# 			print hotel_name
			
# 	return hotel_results['businesses']



# def search_museums(location, term = "museums", limit = 20, offset = 20):
# 	"""This function returns list of parks based on location"""
# 	museum_results = yelp_api.search_query(location = location, term = term, limit = limit, offset=offset)

# 	for business in museum_results['businesses']:
# 		if business in museum_results['businesses']:
# 			museum_name = business['name']
# 			print museum_name
# 	return museum_results['businesses']



# def search_parks():





