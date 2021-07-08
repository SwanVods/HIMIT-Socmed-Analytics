from insights import getUserInsights, getUserMedia, getMediaInsights
from credentials import get_creds, makeApiCall

params = get_creds()
getUserInsights(params)
getMediaInsights(params)


# # store latest post id
# params['latest_media_id'] = response['json_data']['data'][0]['id']


