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
import isodate

# -----------------------------
# Step 0: Read API key
# -----------------------------
api_key_path = os.path.join(".local", "youtube_api_key.txt")
try:
    with open(api_key_path, "r") as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    print(f"API key file not found at {api_key_path}")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python y.py <channel_name_or_handle>")
    sys.exit(1)

channel_name = sys.argv[1]

# -----------------------------
# Step 1: Get channel ID and uploads playlist ID
# -----------------------------
url_channel = "https://www.googleapis.com/youtube/v3/channels"
params_channel = {
    "key": API_KEY,
    "forUsername": channel_name,
    "part": "id,contentDetails"
}
response = requests.get(url_channel, params=params_channel).json()

if "items" in response and len(response["items"]) > 0:
    channel_id = response["items"][0]["id"]
    uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
else:
    # Try by handle
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
        # Get uploads playlist
        url_channel = "https://www.googleapis.com/youtube/v3/channels"
        params_channel = {
            "key": API_KEY,
            "id": channel_id,
            "part": "contentDetails"
        }
        resp2 = requests.get(url_channel, params=params_channel).json()
        uploads_playlist_id = resp2['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    else:
        print("Channel not found")
        sys.exit(1)

print(f"Found Channel ID: {channel_id}")
print(f"Uploads playlist ID: {uploads_playlist_id}")

# -----------------------------
# Step 2: Fetch videos >5 min from uploads playlist (latest first)
# -----------------------------
playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"
video_url = "https://www.googleapis.com/youtube/v3/videos"

medium_videos = []
next_page_token = None
max_to_fetch = 100

while len(medium_videos) < max_to_fetch:
    params = {
        "key": API_KEY,
        "playlistId": uploads_playlist_id,
        "part": "contentDetails,snippet",
        "maxResults": 50,
        "pageToken": next_page_token
    }
    resp = requests.get(playlist_url, params=params).json()
    if "items" not in resp or len(resp["items"]) == 0:
        break

    # Collect video IDs from this page
    batch_ids = [item["contentDetails"]["videoId"] for item in resp["items"]]

    # Fetch video durations in batches (max 50 per request)
    for i in range(0, len(batch_ids), 50):
        sub_ids = batch_ids[i:i+50]
        params_v = {
            "key": API_KEY,
            "id": ",".join(sub_ids),
            "part": "contentDetails"
        }
        resp_v = requests.get(video_url, params=params_v).json()
        for item in resp_v.get("items", []):
            duration_iso = item.get("contentDetails", {}).get("duration")
            if not duration_iso:
                continue
            try:
                duration_sec = int(isodate.parse_duration(duration_iso).total_seconds())
            except Exception:
                continue
            if duration_sec >= 300:  # 5+ minutes
                medium_videos.append(item["id"])
                if len(medium_videos) >= max_to_fetch:
                    break

    nextPage = resp.get("nextPageToken")
    if not nextPage or len(medium_videos) >= max_to_fetch:
        break
    next_page_token = nextPage

print(f"Collected {len(medium_videos)} videos ≥5 min")

# -----------------------------
# Step 3: Sort by latest upload
# -----------------------------
# Build id -> publishedAt mapping from first pages
id_to_date = {}
# Re-fetch snippet data for sorting (if needed)
for i in range(0, len(batch_ids), 50):
    sub_ids = batch_ids[i:i+50]
    params_v = {
        "key": API_KEY,
        "id": ",".join(sub_ids),
        "part": "snippet"
    }
    resp_v = requests.get(video_url, params=params_v).json()
    for item in resp_v.get("items", []):
        vid_id = item["id"]
        if vid_id in medium_videos:
            id_to_date[vid_id] = item["snippet"]["publishedAt"]

medium_videos.sort(key=lambda x: id_to_date.get(x, ""), reverse=True)

# -----------------------------
# Step 4: Save to .local/db/<channel_name>.txt
# -----------------------------
output_dir = os.path.join(".local", "db")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"{channel_name}.txt")

with open(output_file, "w") as f:
    for vid in medium_videos:
        f.write(f"{vid}\n")

print(f"Saved {len(medium_videos)} videos (>5 min) to {output_file}")