import requests
import json
from tqdm import tqdm

class Stats:
    def __init__(self, api_key, channel_id, date):
        self.api_key = api_key
        self.channel_id = channel_id
        self.date = date
        self.channel_stats = None
        self.video_data = None

    def get_channel_stats(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        json_url = requests.get(url) #return json format
        data = json_url.json()
        # data = json.loads(json_url.text) #convert to text
        try :
            data = data["items"][0]["statistics"]
        except : 
            data = None

        self.channel_stats = data
        return data


    def get_channel_video_data(self) :
        # # 1. Get Video ID
        channel_videos = self._get_channel_videos(limit=10)
        print(len(channel_videos))

        # 2. Get Video Stats
        parts = ['snippet', 'statistics']
        # for part in parts:
        #     data = self.get_videos_this_month(self.channel_id, parts, self.date)
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self.get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)
        
        self.video_data = channel_videos
        return channel_videos

    def get_videos_this_month(self, channel_id, date):
        url = f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={channel_id}&part=id&publishedAfter={date}'
        print(url)
        # json_url = requests.get(url)
        # data = json_url.json()
        # print(data)
        vid, npt = self._get_channel_videos_per_page(url)
        index = 0
        while(npt is not None and index < 10):
            nextUrl = url + "&pageToken=" + npt
            next_vid, npt = self._get_channel_videos_per_page(nextUrl)
            vid.update(next_vid)
            index += 1
        return vid


    def get_single_video_data(self, video_id, part):
        url = f'https://www.googleapis.com/youtube/v3/videos?key={self.api_key}&id={video_id}&part={part}'
        json_url = requests.get(url)
        data = json_url.json()
        try :
            data = data['items'][0][part]
        except:
            print('error')
            data = dict()

        return data

    def _get_channel_videos(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&publishedAfter={self.date}'
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
        # print(url)
        vid, npt = self._get_channel_videos_per_page(url)
        index = 0
        while(npt is not None and index < 10):
            nextUrl = url + "&pageToken=" + npt
            next_vid, npt = self._get_channel_videos_per_page(nextUrl)
            vid.update(next_vid)
            index+=1
        return vid

    def _get_channel_videos_per_page(self, url) :
        json_url = requests.get(url)
        data = json_url.json()
        channel_videos = dict()
        if 'items' not in data:
            return channel_videos, None

        item_data = data['items']
        nextPageToken = data.get("nextPageToken", None)
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = dict()
            except KeyError:
                print("Error!")
        return channel_videos, nextPageToken

    def dump(self) : # TODO : export to excel or dump to csv
        if self.channel_stats is None or self.video_data is None:
            print('data is empty')
            return

        fused_data = {self.channel_id:{"channel_statistics": self.channel_stats, "video_data": self.video_data}}
        
        channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id) #TODO Get channel name from data
        channel_title = channel_title.replace(" ", "_").lower()

        #export file
        file_name = channel_title + "ganti.json"
        with open(file_name, 'w') as f:
            json.dump(fused_data, f, indent=4)

        print("file dumped")
