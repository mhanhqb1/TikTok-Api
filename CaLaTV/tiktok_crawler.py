from CaLaTV.configs import cfg
from TikTokApi import TikTokApi
from datetime import datetime
import asyncio
import os
import requests
import json

cfg.run()
apiUrl = os.environ.get('API_URL')
ms_token = os.environ.get(
    "ms_token", None
)

async def get_user_data():
	userApi = apiUrl + 'tiktoks'
	params = {
		'limit': 10
	}
	x = requests.get(userApi, params = params)
	users = x.json()
	user_items = []
	for _user in users:
	    async with TikTokApi() as api:
	        await api.create_sessions(headless=False, ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
	        user = api.user(_user['unique_id'])
	        user_data = await user.info()
	        user_stats = user_data['userInfo']['stats']
        	videoCount = user_data['userInfo']['stats']['videoCount']
	        count = 0
	        videos = []
	        async for video in user.videos(count=videoCount):
	        	v = video.as_dict
	        	tags = []
	        	if 'textExtra' in v:
		        	for tag in v['textExtra']:
		        		tags.append(tag['hashtagName'])
	        	videos.append({
	        		'unique_id': _user['unique_id'],
	        		'tiktok_id': v['id'],
	        		'description': v['desc'],
	        		'image': v['video']['cover'] if 'video' in v else '',
	        		'tags': ', '.join(tags),
	        		'publish_at': datetime.fromtimestamp(v['createTime']).strftime("%Y-%m-%d %H:%M:%S")
	        	})

	        user_items.append({
        		'id': _user['id'],
        		'unique_id': _user['unique_id'],
        		'image': user_data['userInfo']['user']['avatarLarger'],
        		'name': user_data['userInfo']['user']['nickname'],
        		'videos': videos
        	})

	x = requests.post(userApi, data = {'data': json.dumps(user_items)})
	print(x.json())


if __name__ == "__main__":
    asyncio.run(get_user_data())