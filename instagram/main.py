from insights import getUserInsights, getMediaInsights
from credentials import get_creds



params = get_creds()
getUserInsights(params, '1625072400', '1626076800')
getMediaInsights(params, '1625072400', '1626076800')



