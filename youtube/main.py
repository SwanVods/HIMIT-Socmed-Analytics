from youtube_stats import Stats
from datetime import datetime
import os

today = datetime.today()
datem = datetime(2021, 1, 1)
dt = datetime.combine(datem, datetime.min.time())
date = dt.isoformat("T") + "Z"

yt = Stats(os.getenv("YT_API_KEY"), os.getenv('CHANNEL_ID'), date)
yt.get_channel_stats()
yt.get_channel_video_data()
yt.dump()

