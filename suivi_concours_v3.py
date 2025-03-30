# suivi_concours_v3.py
import os
import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime

load_dotenv("youtube.env")

API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST_ID = "PLXwku06I04tJ99s_CjPWJJV-5MnDqUlfZ"
HISTO_FILE = "historique_complet.csv"
VIDEO_ID_ULYSSE = "Ol91C4pV3kA"

# API YouTube
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_videos_from_playlist(playlist_id):
    videos = []
    next_page_token = None
    while True:
        res = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        for item in res["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            title = item["snippet"]["title"]
            videos.append({"video_id": video_id, "title": title})
        next_page_token = res.get("nextPageToken")
        if not next_page_token:
            break
    return videos

def get_video_stats(video_ids):
    stats = []
    for i in range(0, len(video_ids), 50):
        ids = ",".join(video_ids[i:i+50])
        res = youtube.videos().list(
            part="statistics,snippet",
            id=ids
        ).execute()
        for item in res["items"]:
            stats.append({
                "video_id": item["id"],
                "title": item["snippet"]["title"],
                "likes": int(item["statistics"].get("likeCount", 0)),
                "published_at": item["snippet"]["publishedAt"]
            })
    return stats

# === SCRIPT PRINCIPAL ===
videos = get_videos_from_playlist(PLAYLIST_ID)
video_ids = [v["video_id"] for v in videos]
stats = get_video_stats(video_ids)
df = pd.DataFrame(stats)
df = df.sort_values(by="likes", ascending=False).reset_index(drop=True)
df["rank"] = df.index + 1
df["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Historique complet
if os.path.exists(HISTO_FILE):
    historique = pd.read_csv(HISTO_FILE)
    df_concat = pd.concat([historique, df], ignore_index=True)
else:
    df_concat = df

# Enregistrer
cols = ["timestamp", "video_id", "title", "likes", "rank"]
df_concat[cols].to_csv(HISTO_FILE, index=False)

print("✅ historique_complet.csv mis à jour avec", len(df), "vidéos.")
