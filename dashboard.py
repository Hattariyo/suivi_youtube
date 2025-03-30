import streamlit as st
import pandas as pd
import plotly.express as px

# Liens Google Drive en mode "téléchargement direct"
HISTORIQUE_URL = "https://drive.google.com/uc?id=1Oi5kWc173-Z4ecnySTkbz6hffuYigXri"
CLASSEMENT_URL = "https://drive.google.com/uc?id=1c0LeysCYhrKr6JaXD6w-XCHmPMwpXvAu"

# Chargement des données
@st.cache_data
def load_data():
    historique = pd.read_csv(HISTORIQUE_URL)
    classement = pd.read_csv(CLASSEMENT_URL)
    return historique, classement

historique, classement = load_data()

# Titre du dashboard
st.title("🎟️ Suivi du concours YouTube - Les Trésors d'Ulysse")

# 🎯 Focus sur Ulysse
st.header("🎯 Évolution pour la vidéo : Les Trésors d'Ulysse")
ulysse_data = historique[historique["title"].str.contains("Ulysse", case=False)]

# Choix métrique
metric = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True, key="ulysse_metric")
if metric == "Likes":
    fig = px.line(ulysse_data, x="timestamp", y="likes", title="Évolution des likes - Ulysse")
    fig.update_yaxes(title="Likes")
else:
    fig = px.line(ulysse_data, x="timestamp", y="rank", title="Évolution du rang - Ulysse")
    fig.update_yaxes(title="Rang", autorange="reversed")

st.plotly_chart(fig, use_container_width=True)

# 🏆 Classement général
st.header("🏆 Classement général - Top 20")
st.dataframe(classement.sort_values("rank").head(20)[["title", "likes", "rank"]], use_container_width=True)

# 📊 Graphique de l'évolution du classement des 20 premiers
st.header("📈 Évolution du classement - Top 20")
top20_ids = classement.sort_values("rank").head(20)["video_id"].tolist()
top20_hist = historique[historique["video_id"].isin(top20_ids)]

fig_rank = px.line(top20_hist, x="timestamp", y="rank", color="title", title="Classement dans le temps")
fig_rank.update_yaxes(title="Rang", autorange="reversed")
st.plotly_chart(fig_rank, use_container_width=True)

# 💖 Évolution des likes - Top 20
st.header("💖 Évolution des likes - Top 20")
fig_likes = px.line(top20_hist, x="timestamp", y="likes", color="title", title="Likes dans le temps")
fig_likes.update_yaxes(title="Likes")
st.plotly_chart(fig_likes, use_container_width=True)

# mise à jour automatique

# mise � jour automatique