import json
from credentials import get_creds, makeApiCall


# def getUserMediaWithInsights(params) :
# 	endpointParams = dict()
# 	endpointParams['fields'] = 'id,media_type'
# 	endpointParams['access_token'] = params['access_token']
# 	url = params['endpoint_base'] + \
# 		params['instagram_account_id'] + '/media'

# 	return makeApiCall(url, endpointParams, params['debug'])

def getUserMedia(params):
	""" Get users media
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict()  
	endpointParams['fields'] = 'id,media_type'
	endpointParams['access_token'] = params['access_token'] 
	url = params['endpoint_base'] + \
		params['instagram_account_id'] + '/media'

	return makeApiCall(url, endpointParams, params['debug'])  

	

def getMediaInsights(params):

	endpointParams = dict()  
	endpointParams['access_token'] = params['access_token']  

	medias = getUserMedia(params)

	# Get insights each media
	for media in medias['json_data']['data'] :
		if 'CAROUSEL_ALBUM' == media['media_type'] :
			params['metric'] = 'carousel_album_engagement,carousel_album_impressions,carousel_album_reach'
		else : 
			params['metric'] = 'engagement,impressions,reach,saved'

		endpointParams['metric'] = params['metric']
		params['latest_media_id'] = media['id']
		url = params['endpoint_base'] + params['latest_media_id'] + '/insights'

		response = makeApiCall(url, endpointParams, params['debug'])

		with open('result.json', 'a') as fp:
			json.dump([media, response['json_data']], fp)

		# for insight in response['json_data']['data']:  # loop over post insights
		# 	print ("\t" + insight['title'] + " (" + insight['period'] + "): " + str(insight['values'][0]['value']))
	print('Media dump success!')


def getUserInsights(params):
	""" Get insights for a users account
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict()  # parameter to send to the endpoint
	# fields to get back
	endpointParams['metric'] = 'follower_count,impressions,profile_views,reach'
	endpointParams['period'] = 'day'  # period
	endpointParams['access_token'] = params['access_token']  # access token

	url = params['endpoint_base'] + \
		params['instagram_account_id'] + '/insights'  # endpoint url

	response = makeApiCall(url, endpointParams, params['debug']) 

	with open('profile.json', 'w') as fp:
		json.dump(response['json_data'], fp)
	print('Profile Dump Success!')

	# print("\n---- MONTHLY USER ACCOUNT INSIGHTS -----\n")

	# for insight in response['json_data']['data']:  
	# 	print("\t" + insight['title'] + " (" + insight['period'] + "): " + str(insight['values'][0]['value'])
	# 	)
	# 	for value in insight['values']:  # loop over each value
	# 		# print out counts for the date
	# 		print("\t\t" + value['end_time'] + ": " + str(value['value']))

	
