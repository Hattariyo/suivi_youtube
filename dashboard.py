import streamlit as st
import pandas as pd
import plotly.express as px

# 🟡 Fichiers locaux (plus de Drive)
HISTORIQUE_PATH = "historique_complet.csv"
CLASSEMENT_PATH = "classement_youtube.csv"

# Chargement des données
@st.cache_data
def load_data():
    historique = pd.read_csv(HISTORIQUE_PATH)
    classement = pd.read_csv(CLASSEMENT_PATH)
    return historique, classement

historique, classement = load_data()

# 🎯 Vidéo Ulysse par défaut (recherche par mot-clé)
default_video = next((title for title in classement["title"] if "ulysse" in title.lower()), None)

# Titre
st.markdown("## 🎟️ Suivi du concours YouTube - Les Trésors d'Ulysse")

# Liste des vidéos
videos = classement["title"].tolist()
selected_videos = st.multiselect("Choisis les vidéos à afficher :", videos, default=[default_video] if default_video else videos[:1])

# Sélecteur de métrique
metric = st.radio("Afficher :", ["Likes", "Rang"], horizontal=True)

# 🔍 Filtrage
historique_selected = historique[historique["title"].isin(selected_videos)]

# 📈 Graphique principal
st.markdown("### 📊 Évolution des likes" if metric == "Likes" else "### 📉 Évolution du rang")
fig = px.line(
    historique_selected,
    x="timestamp",
    y="likes" if metric == "Likes" else "rank",
    color="title",
    height=500
)
if metric == "Rang":
    fig.update_yaxes(title="rang", autorange="reversed")
st.plotly_chart(fig, use_container_width=True)

# 🏆 Tableau du top 20
st.markdown("### 🏆 Classement actuel (Top 20)")
top20 = classement.sort_values("rank").head(20)[["rank", "title", "likes", "views"]]
top20 = top20.sort_values("rank")
top20.index = range(1, 21)
st.dataframe(top20, use_container_width=True)

# 📈 Graphique des likes (top 20)
st.markdown("### 📈 Évolution des likes (Top 20)")
top20_ids = top20["title"].tolist()
historique_top20 = historique[historique["title"].isin(top20_ids)]
fig_likes = px.line(
    historique_top20,
    x="timestamp",
    y="likes",
    color="title",
    height=600
)
st.plotly_chart(fig_likes, use_container_width=True)

# 📉 Graphique du classement (top 20)
st.markdown("### 📉 Classement dans le temps (Top 20)")
fig_rank = px.line(
    historique_top20,
    x="timestamp",
    y="rank",
    color="title",
    height=600
)
fig_rank.update_yaxes(title="rang", autorange="reversed")
st.plotly_chart(fig_rank, use_container_width=True)
