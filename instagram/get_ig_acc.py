from credentials import get_creds, makeApiCall


def getInstagramAccount(params):
	""" Get instagram account
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{page-id}?access_token={your-access-token}&fields=instagram_business_account
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict()  # parameter to send to the endpoint
	# tell facebook we want to exchange token
	endpointParams['access_token'] = params['access_token']
	endpointParams['fields'] = 'instagram_business_account'  # access token

	url = params['endpoint_base'] + params['page_id']  # endpoint url

	return makeApiCall(url, endpointParams, params['debug'])  # make the api call


params = get_creds()  # get creds
params['debug'] = 'no'  # set debug
params['page_id'] = '334593433285127'
response = getInstagramAccount(params)  # get debug info

print ("\n---- INSTAGRAM ACCOUNT INFO ----\n")
print ("Page Id:")  # label
print (response['json_data']['id'])  # display the page id
print ("\nInstagram Business Account Id:")  # label
# display the instagram account id
print (response['json_data']['instagram_business_account']['id'])
