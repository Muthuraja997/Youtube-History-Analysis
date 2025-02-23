import json
import re
import requests
import isodate
from datetime import datetime

# 🔑 Your YouTube Data API Key
API_KEY = "AIzaSyAjG02Z2c8Nvx_1QPf5Z-rejnXR_1AEZpY"

# 📂 Load the YouTube watch history JSON file
with open("watch-history.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    print("loading")
# 🔍 Extract video IDs from history
video_ids = []
video_data = {}

for entry in data:
    if "titleUrl" in entry:
        match = re.search(r"v=([a-zA-Z0-9_-]+)", entry["titleUrl"])
        if match:
            video_id = match.group(1)
            video_ids.append(video_id)
            video_data[video_id] = {
                "title": entry.get("title", "N/A"),
                "url": entry.get("titleUrl", "N/A"),
                "channel": entry["subtitles"][0]["name"] if "subtitles" in entry else "N/A",
                "timestamp": entry.get("time", "N/A"),
            }
print("data entry")
# 🕒 Function to get video durations & descriptions from YouTube API
def get_video_details(video_ids):
    try:
        video_details = {}
        for i in range(0, len(video_ids), 50):  # YouTube API allows 50 IDs per request
            batch_ids = video_ids[i : i + 50]
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={','.join(batch_ids)}&key={API_KEY}"
            
            response = requests.get(url).json()
            
            for item in response.get("items", []):
                video_id = item["id"]
                duration = item["contentDetails"]["duration"]
                description = item["snippet"]["description"]
                video_details[video_id] = {"duration": duration, "description": description}
        print("video details updated")
        return video_details
    except:
        print("ERROR")

# 📌 Fetch video durations & descriptions
video_details = get_video_details(video_ids)

# ⏳ Convert ISO 8601 duration to seconds
def convert_duration_to_seconds(duration):
    return int(isodate.parse_duration(duration).total_seconds())

video_durations_seconds = {vid: convert_duration_to_seconds(details["duration"]) for vid, details in video_details.items()}

# 📆 Function to convert timestamp to datetime
def parse_timestamp(timestamp):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

# ⏱️ Estimate watch time using timestamps
watch_time = {}

for i in range(len(data) - 1):
    video_id = re.search(r"v=([a-zA-Z0-9_-]+)", data[i].get("titleUrl", ""))
    if not video_id:
        continue
    video_id = video_id.group(1)

    if video_id in video_durations_seconds:
        # Get timestamps
        current_time = parse_timestamp(data[i]["time"])
        next_time = parse_timestamp(data[i + 1]["time"])

        # Calculate time difference
        time_spent = (next_time - current_time).total_seconds()
        estimated_watch_time = min(time_spent, video_durations_seconds[video_id])

        # Store watch time
        watch_time[video_id] = estimated_watch_time
print("store watch time")
# 🔄 Merge all data (history + durations + descriptions + watch time)
for video_id in video_data:
    video_data[video_id]["video_duration_seconds"] = video_durations_seconds.get(video_id, 0)
    video_data[video_id]["estimated_watch_time_seconds"] = watch_time.get(video_id, 0)
    video_data[video_id]["description"] = video_details.get(video_id, {}).get("description", "No description available.")
print("saving")
# 💾 Save final data as JSON
with open("youtube_watch_data.json", "w", encoding="utf-8") as outfile:
    json.dump(video_data, outfile, indent=4)

print("✅ YouTube watch history with durations & descriptions saved to 'youtube_watch_data.json'")



# import json
# import re
# import requests
# import isodate
# from datetime import datetime

# API_KEY = "AIzaSyAjG02Z2c8Nvx_1QPf5Z-rejnXR_1AEZpY"

# # Load the YouTube watch history JSON file
# with open("watch-history.json", "r", encoding="utf-8") as file:
#     data = json.load(file)
# print("data Loaded")
# # Extract video IDs from history
# video_ids = []
# video_data = {}

# for entry in data:
#     if "titleUrl" in entry:
#         match = re.search(r"v=([a-zA-Z0-9_-]+)", entry["titleUrl"])
#         if match:
#             video_id = match.group(1)
#             video_ids.append(video_id)
#             video_data[video_id] = {
#                 "title": entry.get("title", "N/A"),
#                 "url": entry.get("titleUrl", "N/A"),
#                 "channel": entry["subtitles"][0]["name"] if "subtitles" in entry else "N/A",
#                 "timestamp": entry.get("time", "N/A"),
#             }
# print("Data Entry completed")
# # Function to get video durations from YouTube API
# def get_video_durations(video_ids):
#     video_durations = {}

#     for i in range(0, len(video_ids), 50):  # YouTube API allows 50 IDs per request
#         batch_ids = video_ids[i : i + 50]
#         url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={','.join(batch_ids)}&key={API_KEY}"
        
#         response = requests.get(url).json()
        
#         for item in response.get("items", []):
#             video_id = item["id"]
#             duration = item["contentDetails"]["duration"]
#             video_durations[video_id] = duration
        

#     return video_durations
# print("Duration Got")
# # Fetch video durations
# video_durations = get_video_durations(video_ids)

# # Convert ISO 8601 duration to seconds
# def convert_duration_to_seconds(duration):
#     return int(isodate.parse_duration(duration).total_seconds())

# print("Colculted durations")
# video_durations_seconds = {vid: convert_duration_to_seconds(dur) for vid, dur in video_durations.items()}

# # Function to convert timestamp to datetime
# def parse_timestamp(timestamp):
#     return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

# # Estimate watch time using timestamps
# watch_time = {}

# for i in range(len(data) - 1):
#     video_id = re.search(r"v=([a-zA-Z0-9_-]+)", data[i].get("titleUrl", ""))
#     if not video_id:
#         continue
#     video_id = video_id.group(1)

#     if video_id in video_durations_seconds:
#         # Get timestamps
#         current_time = parse_timestamp(data[i]["time"])
#         next_time = parse_timestamp(data[i + 1]["time"])

#         # Calculate time difference
#         time_spent = (next_time - current_time).total_seconds()
#         estimated_watch_time = min(time_spent, video_durations_seconds[video_id])

#         # Store watch time
#         watch_time[video_id] = estimated_watch_time

# # Merge watch history, durations, and estimated watch time
# for video_id in video_data:
#     video_data[video_id]["video_duration_seconds"] = video_durations_seconds.get(video_id, 0)
#     video_data[video_id]["estimated_watch_time_seconds"] = watch_time.get(video_id, 0)
# print("Overall done")
# # Save final data as JSON
# with open("youtube_watch_data.json", "w", encoding="utf-8") as outfile:
#     json.dump(video_data, outfile, indent=4)

# print("✅ YouTube watch history with durations saved to 'youtube_watch_data.json'")
