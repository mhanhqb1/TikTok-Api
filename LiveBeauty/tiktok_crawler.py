from LiveBeauty import mysql_connection
from TikTokApi import TikTokApi
from datetime import datetime
import asyncio
import os

ms_token = os.environ.get(
    "ms_token", None
)


async def get_user_data():
	today = datetime.today().strftime("%Y-%m-%d")
	limit = 1
	users = mysql_connection.select_normal('tiktok_users', ['user_name'], f"where crawl_at is null or crawl_at < '{today}' limit {limit}")
	user_items = []
	for user in users:
	    async with TikTokApi() as api:
	        await api.create_sessions(headless=False, ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
	        user = api.user(user[0])
	        user_data = await user.info()
	        user_stats = user_data['userInfo']['stats']
	        user_items.append((
	        	user_stats['followerCount'], 
	        	user_stats['followingCount'], 
	        	user_stats['friendCount'], 
	        	user_stats['heartCount'], 
	        	user_stats['videoCount'],
	        	user_data['userInfo']['user']['avatarLarger'],
	        	user_data['userInfo']['user']['id'],
	        	user_data['userInfo']['user']['nickname']
	        ))
	        videoCount = user_data['userInfo']['stats']['videoCount']
	        count = 0
	        async for video in user.videos(count=videoCount):
	        	print(video.as_dict)
	        	break
	            # count += 1
	            # print(count, video.as_dict['id'])


if __name__ == "__main__":
    asyncio.run(get_user_data())