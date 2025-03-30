
# suivi_concours_v2.py
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import pandas as pd
import plotly.graph_objects as go
from googleapiclient.discovery import build
from datetime import datetime
import matplotlib.pyplot as plt

# Chargement variables d'environnement
load_dotenv("youtube.env")

API_KEY = os.getenv("YOUTUBE_API_KEY")
PLAYLIST_ID = "PLXwku06I04tJ99s_CjPWJJV-5MnDqUlfZ"
VIDEO_ID_ULYSSE = "Ol91C4pV3kA"
HTML_OUTPUT = "classement_youtube.html"
HISTO_FILE = "historique.csv"
GRAPH_FILE = "graphique.html"
CSV_FILE = "classement_youtube.csv"
EXCEL_FILE = "classement_youtube.xlsx"
PDF_FILE = "classement_youtube.pdf"

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")  # La copine
EMAIL_ME = "viot.art@gmail.com"  # Toi

# Connexion API YouTube
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
            published_at = item["snippet"]["publishedAt"]
            videos.append({"video_id": video_id, "title": title, "published_at": published_at})
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
                "published_at": item["snippet"]["publishedAt"],
                "views": int(item["statistics"].get("viewCount", 0)),
                "likes": int(item["statistics"].get("likeCount", 0)),
                "url": f"https://www.youtube.com/watch?v={item['id']}"
            })
    return stats

def send_email(subject, body, files, to_address):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    for file_path in files:
        with open(file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)

def send_simple_email(subject, body, to_address):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)

# === SCRIPT PRINCIPAL ===
videos = get_videos_from_playlist(PLAYLIST_ID)
video_ids = [v["video_id"] for v in videos]
data = get_video_stats(video_ids)
df = pd.DataFrame(data)
df["published_at"] = pd.to_datetime(df["published_at"])
df = df[df["published_at"] > pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=15)]
df = df.sort_values(by="likes", ascending=False).reset_index(drop=True)
df["rank"] = df.index + 1

# Enregistrer CSV + Excel + HTML
df.to_csv(CSV_FILE, index=False)
df_copy = df.copy()
df_copy["published_at"] = df_copy["published_at"].dt.tz_localize(None)
df_copy.to_excel(EXCEL_FILE, index=False)
df_html = df.copy()
df_html["title"] = df_html.apply(lambda x: f"<a href='{x['url']}' target='_blank'>{x['title']}</a>", axis=1)
df_html[["rank", "title", "views", "likes"]].to_html(HTML_OUTPUT, escape=False, index=False)

# Export PDF
fig, ax = plt.subplots()
df.plot(kind='bar', x='rank', y='likes', ax=ax, legend=False)
plt.title("Classement des vidéos par likes")
plt.tight_layout()
plt.savefig(PDF_FILE)

# Suivi de la vidéo d'Ulysse
match = df[df["video_id"] == VIDEO_ID_ULYSSE]
if not match.empty:
    rang = int(match.iloc[0]["rank"])
    likes = int(match.iloc[0]["likes"])
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Historique
    histo_data = pd.DataFrame([{ "timestamp": date_now, "likes": likes, "rank": rang }])
    if os.path.exists(HISTO_FILE):
        historique = pd.read_csv(HISTO_FILE)
        if not ((historique['timestamp'] == date_now) & (historique['likes'] == likes)).any():
            historique = pd.concat([historique, histo_data], ignore_index=True)
    else:
        historique = histo_data
    historique.to_csv(HISTO_FILE, index=False)

    # Graphique interactif
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=historique['timestamp'], y=historique['likes'], name='likes', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=historique['timestamp'], y=historique['rank'], name='rank', mode='lines+markers', yaxis='y2'))
    fig.update_layout(
        title="Évolution des likes et du rang de la vidéo",
        xaxis=dict(title="timestamp"),
        yaxis=dict(title="likes"),
        yaxis2=dict(title="rank", overlaying='y', side='right', autorange="reversed")
    )
    fig.write_html(GRAPH_FILE)

    # Email si changement
    if os.path.exists(HISTO_FILE):
        last_rows = historique.tail(2)
        if len(last_rows) == 2 and last_rows.iloc[0]['rank'] != last_rows.iloc[1]['rank']:
            old_rank = int(last_rows.iloc[0]['rank'])
            new_rank = int(last_rows.iloc[1]['rank'])
            subject = "🚀 Changement de rang pour 'Les trésors d'Ulysse' !"
            body = f"Le rang de la vidéo est passé de {old_rank} à {new_rank}\nLikes : {likes}"

            # Envoi complet à toi
            send_email(subject, body, [CSV_FILE, HTML_OUTPUT, GRAPH_FILE, PDF_FILE], EMAIL_ME)

            # Envoi simple à ta copine si dans le top 20
            if new_rank <= 20:
                body_gentil = f"🎉 Bonne nouvelle !\n\nTa vidéo vient de changer de position dans le classement YouTube du concours Moovjee.\nElle est maintenant classée #{new_rank} avec {likes} likes 💪\n\nContinue comme ça, c'est super ! ❤️"
                send_simple_email("💡 Mise à jour du classement Moovjee", body_gentil, EMAIL_TO)
else:
    print("Vidéo non trouvée dans la playlist.")
