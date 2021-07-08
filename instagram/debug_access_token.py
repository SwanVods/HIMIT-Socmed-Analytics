from credentials import get_creds, makeApiCall
import datetime


def debugAccessToken(params):
	""" Get info on an access token 
	
	API Endpoint:
		https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict()  # parameter to send to the endpoint
	# input token is the access token
	endpointParams['input_token'] = params['access_token']
	# access token to get debug info on
	endpointParams['access_token'] = params['access_token']

	url = params['graph_domain'] + '/debug_token'  # endpoint url

	return makeApiCall(url, endpointParams, params['debug'])  # make the api call


params = get_creds()  # get creds
params['debug'] = 'GET'  # set debug
response = debugAccessToken(params)  # hit the api for some data!

print ("\nData Access Expires at: ")  # label
# display out when the token expires
print (datetime.datetime.fromtimestamp(response['json_data']['data']['data_access_expires_at']))

print ("\nToken Expires at: ")  # label
# display out when the token expires
print (datetime.datetime.fromtimestamp(response['json_data']['data']['expires_at']))
