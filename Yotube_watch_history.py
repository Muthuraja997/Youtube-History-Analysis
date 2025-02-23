from googleapiclient.discovery import build
from datetime import timedelta
import isodate

api_key = 'AIzaSyAjG02Z2c8Nvx_1QPf5Z-rejnXR_1AEZpY'
youtube = build('youtube', 'v3', developerKey=api_key)

def get_watch_history():
    request = youtube.activities().list(
        part='snippet,contentDetails',
        mine=True,
        maxResults=50
    )
    response = request.execute()
    return response['items']

def get_video_duration(video_id):
    request = youtube.videos().list(
        part='contentDetails',
        id=video_id
    )
    response = request.execute()
    duration = response['items'][0]['contentDetails']['duration']
    return isodate.parse_duration(duration).total_seconds()

# Fetch watch history
watch_history = get_watch_history()

# Extract video IDs and fetch durations
video_durations = {}
for item in watch_history:
    video_id = item['contentDetails']['upload']['videoId']
    duration = get_video_duration(video_id)
    video_durations[video_id] = duration
print(video_durations)


