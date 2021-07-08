import requests, json, os

def get_creds():
    """ Get creds required for use in the applications

        Returns:
                dictonary: credentials needed globally
        """

    creds = dict()  # dictionary to hold everything
    # access token for use with all api calls
    creds['access_token'] = os.getenv('TOKEN')
    # base domain for api calls
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v11.0'  # version of the api we are hitting
    creds['endpoint_base'] = creds['graph_domain'] + \
        creds['graph_version'] + '/'  # base endpoint with domain and version
    # users instagram account id
    creds['instagram_account_id'] = '17841403814122346'
    creds['debug'] = 'no'

    return creds


def makeApiCall(url, endpointParams, type):
    """ Request data from endpoint with params

    Args:
            url: string of the url endpoint to make request from
            endpointParams: dictionary keyed by the names of the url parameters
    Returns:
            object: data from the endpoint
    """

    if type == 'POST':  # post request
        data = requests.post(url, endpointParams)
    else:  # get request
        data = requests.get(url, endpointParams)


    response = dict()  # hold response info
    response['url'] = url  # url we are hitting
    response['endpoint_params'] = endpointParams  # parameters for the endpoint
    response['endpoint_params_pretty'] = json.dumps(
        endpointParams, indent=4)  # pretty print for cli
    response['json_data'] = data.json()  # response data from the api
    response['json_data_pretty'] = json.dumps(
        response['json_data'], indent=4)  # pretty print for cli

    return response  # get and return content
