"""
Usage Example
    python get_videos.py mathantics

Generate your Youtube API key https://console.cloud.google.com/apis first

1. Reads your YouTube API key from .local/youtube_api_key.txt.
2. Takes a channel name as input
3. Finds the channel ID via YouTube API.
4. Fetches up to 100 video IDs from that channel.
5. Saves them in .local/db/youtube_channel.txt
6. Saved files acts as a local database for ASTRA to stream later.
"""

import requests
import sys
import os

# Step 0: Read API key from file in .local folder
api_key_path = os.path.join(".local", "youtube_api_key.txt")
try:
    with open(api_key_path, "r") as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    print(f"API key file not found at {api_key_path}")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python get_videos.py <channel_name_or_handle>")
    sys.exit(1)

channel_name = sys.argv[1]

# Step 1: Get channel ID from username or handle
url_channel = "https://www.googleapis.com/youtube/v3/channels"
params_channel = {
    "key": API_KEY,
    "forUsername": channel_name,  # for legacy usernames
    "part": "id"
}

response = requests.get(url_channel, params=params_channel).json()

if "items" in response and len(response["items"]) > 0:
    channel_id = response["items"][0]["id"]
else:
    # Try by handle (modern @handle)
    url_search = "https://www.googleapis.com/youtube/v3/search"
    params_search = {
        "key": API_KEY,
        "q": channel_name,
        "part": "snippet",
        "type": "channel",
        "maxResults": 1
    }
    response_search = requests.get(url_search, params=params_search).json()
    if "items" in response_search and len(response_search["items"]) > 0:
        channel_id = response_search["items"][0]["snippet"]["channelId"]
    else:
        print("Channel not found")
        sys.exit(1)

print(f"Found Channel ID: {channel_id}")

# Step 2: Fetch first 100 videos
video_ids = []
next_page_token = None
max_to_fetch = 100
base_url = "https://www.googleapis.com/youtube/v3/search"

while len(video_ids) < max_to_fetch:
    remaining = max_to_fetch - len(video_ids)
    max_results = 50 if remaining > 50 else remaining  # API max per page is 50

    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "id",
        "order": "date",
        "maxResults": max_results,
        "type": "video",
        "pageToken": next_page_token
    }
    resp = requests.get(base_url, params=params).json()
    for item in resp.get("items", []):
        video_ids.append(item["id"]["videoId"])

    next_page_token = resp.get("nextPageToken")
    if not next_page_token:
        break

# Step 3: Write video IDs to .local/db/<channel_name>.txt
output_dir = os.path.join(".local", "db")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"{channel_name}.txt")

with open(output_file, "w") as f:
    for vid in video_ids:
        f.write(f"{vid}\n")

print(f"Saved {len(video_ids)} video IDs to {output_file}")
