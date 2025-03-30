import os
import pandas as pd
from googleapiclient.discovery import build
from datetime import datetime
from dotenv import load_dotenv

# 🔐 Charger les clés depuis le fichier .env
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")

# 📦 Service YouTube
def get_service():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# 🔄 Récupérer toutes les vidéos d'une playlist
def get_all_videos(service):
    videos = []
    next_page_token = None

    while True:
        response = service.playlistItems().list(
            playlistId=PLAYLIST_ID,
            part="snippet",
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            title = item["snippet"]["title"]
            videos.append((video_id, title))

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

# 🔍 Récupérer les stats d'une liste de vidéos
def get_video_stats(service, videos):
    stats = []
    for i in range(0, len(videos), 50):
        chunk = videos[i:i + 50]
        ids = ",".join([v[0] for v in chunk])
        response = service.videos().list(
            id=ids,
            part="statistics"
        ).execute()

        for item in response["items"]:
            video_id = item["id"]
            like_count = int(item["statistics"].get("likeCount", 0))
            view_count = int(item["statistics"].get("viewCount", 0))
            title = next(v[1] for v in videos if v[0] == video_id)
            stats.append((video_id, title, like_count, view_count))
    return stats

# 🧠 Générer les fichiers CSV
def save_data(stats):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([{
        "timestamp": now,
        "video_id": s[0],
        "title": s[1],
        "likes": s[2],
        "rank": None
    } for s in stats])

    # Charger historique existant
    if os.path.exists("historique_complet.csv"):
        historique = pd.read_csv("historique_complet.csv")
        historique = pd.concat([historique, new_data], ignore_index=True)
        historique.drop_duplicates(subset=["timestamp", "video_id"], inplace=True)
    else:
        historique = new_data

    # Calculer les rangs
    latest = historique[historique["timestamp"] == now].copy()
    latest["rank"] = latest["likes"].rank(method="min", ascending=False).astype(int)
    historique.update(latest)

    # Enregistrer
    historique.to_csv("historique_complet.csv", index=False)

    classement = latest[["video_id", "title", "likes", "rank"]].sort_values(by="rank")
    classement.to_csv("classement_youtube.csv", index=False)

    print(f"✅ historique_complet.csv mis à jour avec {len(latest)} vidéos.")

# ▶️ Exécution principale
if __name__ == "__main__":
    service = get_service()
    videos = get_all_videos(service)
    stats = get_video_stats(service, videos)
    save_data(stats)
