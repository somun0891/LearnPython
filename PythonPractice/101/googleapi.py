from googleapiclient.discovery import build
from pprint import pprint
import re
import os
from datetime import timedelta

api_key = 'AIzaSyDqOTdMtP-jC-nl4UEyT-9CVOvIwCBYJO0' #os.environ.get('yt_api_key') #setx yt_api_key='AIzaSyDqOTdMtP-jC-nl4UEyT-9CVOvIwCBYJO0'
service = build('youtube', 'v3',developerKey=api_key)

request = service.channels().list(
    part='statistics',
    forUsername = 'schafer5'
)

response = request.execute()

# pprint('list all channels for a specific username....\n')
# print(response)

request = service.playlists().list(
    channelId = 'UCCezIgC97PvUuR4_gbFUs5g',
    part = 'id,status,contentDetails'
)

response = request.execute()

# pprint('Print details about all playlists in a specific channel....\n')
# pprint(response)

# for item in response['items']:
#     print(item)

minutes_pattern = re.compile(r'(\d+)M', flags=0)
seconds_pattern = re.compile(r'(\d+)S', flags=0)
hours_pattern = re.compile(r'(\d+)H', flags=0)
nextpagetoken = None
total_seconds = 0

while True:
    request = service.playlistItems().list(
        playlistId = 'PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU',
        part = 'id,status,contentDetails',
        maxResults = 50,
        pageToken = nextpagetoken
    )

    pprint('Print details about all videos in a playlist....')
    print('\n')
    response = request.execute()
    # pprint(response)

    videoidlist = []
    for item in response['items']:
        # print(item['contentDetails']['videoId'])
        # print(item['contentDetails']['videoPublishedAt'])   
        videoidlist.append(item['contentDetails']['videoId'])

    request = service.videos().list(
        id = ",".join(videoidlist),
        part = 'id,status,contentDetails,statistics'
    )

    response = request.execute()


    for item in response['items']:
        # print(item['id'])   
        # print(item['contentDetails']['duration'])
        # print(item['statistics']['viewCount'])
        # print(item['statistics']['likeCount']) 

        duration = item['contentDetails']['duration']

        hours = hours_pattern.search(duration)  
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)    

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0  
        seconds = int(seconds.group(1)) if seconds else 0    

        #print(hours , minutes ,seconds )

        vid_seconds = timedelta(hours = hours ,minutes = minutes , seconds = seconds ).total_seconds()
        total_seconds += vid_seconds

        #print(total_seconds)
    nextpagetoken = response.get('nextPageToken')

    if not nextpagetoken:
        break

total_seconds = int(total_seconds)
minutes , seconds = divmod(total_seconds , 60)
hours , minutes = divmod(minutes , 60)
print(f'{hours} hours {minutes} minutes {seconds} seconds')
       




