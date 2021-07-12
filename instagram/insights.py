import json
from credentials import get_creds, makeApiCall
from dateutil import parser

def getUserMedia(params, since = None, until = None):
	""" Get users media
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}&since={since}&until={until}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict()  
	endpointParams['fields'] = 'id,media_type'
	endpointParams['access_token'] = params['access_token'] 
	endpointParams['since'] = since
	endpointParams['until'] = until
	url = params['endpoint_base'] + \
		params['instagram_account_id'] + '/media'

	return makeApiCall(url, endpointParams, params['debug'])  


def getMediaInsights(params, since=None, until=None):
	""" Get users media

	API Endpoint:
		https://graph.facebook.com/v11.0/{ig-media-id}/insights?metric={metric}&access_token={access-token}&period={period}&since={since}&until={until}

	"""

	endpointParams = dict()  
	response = []
	medias = getUserMedia(params, since, until) # list of media

	# Get insights each media
	for media in medias['json_data']['data'] :
		if 'CAROUSEL_ALBUM' == media['media_type'] :
			params['metric'] = 'carousel_album_engagement,carousel_album_impressions,carousel_album_reach'
		else : 
			params['metric'] = 'engagement,impressions,reach'

		params['media_id'] = media['id']
		url = params['endpoint_base'] + params['media_id'] + '/insights'

		endpointParams['metric'] = params['metric']
		endpointParams['access_token'] = params['access_token']
		endpointParams['period'] = 'lifetime'
		res = makeApiCall(url, endpointParams, params['debug'])
		
		#add new key : media_id
		for data in res['json_data']['data'] :
			data['media_id'] = media['id']
			data['media_type'] = media['media_type']

		response.append(res['json_data']['data'])

	media_insight_dump(response)


def media_insight_dump(posts):
	"""
	Generates a JSON file 
	"""

	data = []

	for postMetrics in posts:
		postInsight = dict()
		for metric in postMetrics:
			postInsight['id'] = metric['media_id']

			if metric['media_type'] == 'IMAGE':
				if metric['name'] == 'engagement':
					postInsight['engagement'] = metric['values']
				elif metric['name'] == 'impressions':
					postInsight['impressions'] = metric['values']
				elif metric['name'] == 'reach':
					postInsight['reach'] = metric['values']

			elif metric['media_type'] == 'CAROUSEL_ALBUM':
				if metric['name'] == 'carousel_album_engagement':
					postInsight['engagement'] = metric['values']
				elif metric['name'] == 'carousel_album_impressions':
					postInsight['impressions'] = metric['values']
				elif metric['name'] == 'carousel_album_reach':
					postInsight['reach'] = metric['values']

		data.append(postInsight)
	
	with open('result.json', 'w') as fp:
		json.dump(data, fp)
	print('Media Dump Success!')


def getUserInsights(params, since = None, until = None):
	""" 
	Get insights for a users account

	Include the `since` and `until` parameters with Unix timestamps to define a range.
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}&since={since}&until={until}
		
	Returns:
		Generate a data inside json file
	"""

	endpointParams = dict()  # parameter to send to the endpoint
	# fields to get back
	endpointParams['metric'] = 'follower_count,impressions,profile_views,reach'
	endpointParams['period'] = 'day'  # period
	endpointParams['since'] = since
	endpointParams['until'] = until
	endpointParams['access_token'] = params['access_token']  # access token

	url = params['endpoint_base'] + \
		params['instagram_account_id'] + '/insights'  # endpoint url

	response = makeApiCall(url, endpointParams, params['debug']) 

	user_insight_dump(response)
	
def user_insight_dump(resDicts) :
	"""
	Generates a JSON File
	"""
	reslist = []

	for data in resDicts['json_data']['data']:
		data['total'] = 0
		for value in data['values']:
			data['total'] += value['value'] # summing values
			parsed = parser.parse(value['end_time']) 
			value['end_time'] = parsed.strftime("%d-%b-%Y") # converting date

		data['avg'] = data['total'] / len(data['values'])
		reslist.append(data)

	with open('profile.json', 'w') as fp:
		json.dump(reslist, fp)
	print('Profile Dump Success!')