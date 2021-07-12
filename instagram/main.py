from insights import getUserInsights, getUserMedia, getMediaInsights
from credentials import get_creds, makeApiCall
import matplotlib.pyplot as plt


params = get_creds()
getUserInsights(params)
# getMediaInsights(params)



